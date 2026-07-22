"""Safe, single-run autonomous Obsidian wiki agent."""

from __future__ import annotations

import json
import re
import sqlite3
import subprocess
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, cast


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class Config:
    vault_path: Path
    ollama_url: str = "http://localhost:11434"
    model: str = "qwen3:8b"
    mode: str = "manual"
    max_searches: int = 8
    max_pages_fetched: int = 12
    max_files_changed: int = 5
    max_new_pages: int = 2
    timeout_seconds: int = 300
    git_enabled: bool = True
    auto_commit: bool = False

    @classmethod
    def load(cls, path: Path) -> Config:
        raw: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
        ollama = raw.get("ollama", {})
        agent = raw.get("agent", {})
        git = raw.get("git", {})
        return cls(
            Path(raw["vault_path"]),
            ollama.get("base_url", cls.ollama_url),
            ollama.get("model", cls.model),
            agent.get("mode", cls.mode),
            agent.get("max_searches", 8),
            agent.get("max_pages_fetched", 12),
            agent.get("max_files_changed", 5),
            agent.get("max_new_pages", 2),
            ollama.get("timeout_seconds", 300),
            git.get("enabled", True),
            git.get("auto_commit", False),
        )


class Vault:
    def __init__(self, root: Path) -> None:
        self.root = root.resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def safe(self, relative: str | Path) -> Path:
        candidate = (self.root / relative).resolve()
        if candidate != self.root and self.root not in candidate.parents:
            raise ValueError("path escapes vault")
        if candidate.exists() and candidate.is_symlink():
            raise ValueError("symlinks are not allowed")
        return candidate

    def pages(self) -> list[Path]:
        return [p for p in self.root.rglob("*.md") if not p.is_symlink()]

    def read(self, relative: str | Path) -> str:
        return self.safe(relative).read_text(encoding="utf-8")

    def write(self, relative: str | Path, content: str) -> Path:
        target = self.safe(relative)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8", newline="\n")
        return target

    def archive(self, relative: str | Path) -> Path:
        source = self.safe(relative)
        destination = self.safe(Path("80_Archive") / source.name)
        destination.parent.mkdir(parents=True, exist_ok=True)
        source.replace(destination)
        return destination


class StateDB:
    def __init__(self, path: Path) -> None:
        self.db = sqlite3.connect(path)
        self.db.executescript("""
        CREATE TABLE IF NOT EXISTS pages (page_path TEXT PRIMARY KEY, title TEXT, type TEXT, status TEXT, updated_at TEXT, word_count INTEGER, outgoing_links TEXT);
        CREATE TABLE IF NOT EXISTS tasks (task_id INTEGER PRIMARY KEY, task_type TEXT, target_page TEXT, priority REAL, status TEXT, created_at TEXT);
        CREATE TABLE IF NOT EXISTS runs (run_id TEXT PRIMARY KEY, model TEXT, start_time TEXT, end_time TEXT, result TEXT, search_count INTEGER, error_message TEXT);
        CREATE TABLE IF NOT EXISTS sources (url TEXT PRIMARY KEY, title TEXT, domain TEXT, fetched_at TEXT, source_type TEXT, reliability TEXT);
        CREATE TABLE IF NOT EXISTS reflections (run_id TEXT, problem TEXT, lesson TEXT, proposed_rule TEXT);
        """)
        self.db.commit()

    def sync_pages(self, vault: Vault) -> None:
        for path in vault.pages():
            text = path.read_text(encoding="utf-8")
            links = re.findall(r"\[\[([^]|]+)", text)
            self.db.execute(
                "INSERT OR REPLACE INTO pages VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    str(path.relative_to(vault.root)),
                    path.stem,
                    "knowledge",
                    "active",
                    now(),
                    len(text.split()),
                    json.dumps(links),
                ),
            )
        self.db.commit()


@dataclass(frozen=True)
class SearchResult:
    title: str
    url: str
    snippet: str = ""


class Researcher:
    def __init__(self, max_searches: int = 8) -> None:
        self.max_searches = max_searches
        self.count = 0

    def search(self, query: str, max_results: int = 5) -> list[SearchResult]:
        if self.count >= self.max_searches:
            return []
        self.count += 1
        # DuckDuckGo HTML is a deliberately small default provider; production deployments can replace it.
        url = "https://html.duckduckgo.com/html/?" + urllib.parse.urlencode({"q": query})
        request = urllib.request.Request(url, headers={"User-Agent": "autonomous-wiki-agent/0.1"})
        with urllib.request.urlopen(request, timeout=20) as response:
            html = response.read(2_000_000).decode("utf-8", errors="replace")
        results: list[SearchResult] = []
        for match in re.finditer(r'class="result__a" href="([^"]+)"[^>]*>(.*?)</a>', html):
            if len(results) >= max_results:
                break
            results.append(SearchResult(re.sub("<.*?>", "", match.group(2)), match.group(1)))
        return results


class Ollama:
    def __init__(self, base_url: str, model: str, timeout: int = 300) -> None:
        self.base_url, self.model, self.timeout = base_url.rstrip("/"), model, timeout

    def chat(self, system: str, prompt: str) -> dict[str, Any]:
        payload = {
            "model": self.model,
            "stream": False,
            "format": "json",
            "keep_alive": 0,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
        }
        request = urllib.request.Request(
            self.base_url + "/api/chat",
            data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(request, timeout=self.timeout) as response:
            body: dict[str, Any] = json.loads(response.read())
        return cast(dict[str, Any], json.loads(body["message"]["content"]))


class Git:
    def __init__(self, root: Path) -> None:
        self.root = root

    def status(self) -> str:
        return subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=self.root,
            capture_output=True,
            text=True,
            check=True,
        ).stdout

    def commit(self, message: str) -> None:
        subprocess.run(["git", "add", "--", str(self.root)], cwd=self.root, check=True)
        subprocess.run(["git", "commit", "-m", message], cwd=self.root, check=True)


def choose_candidate(vault: Vault) -> dict[str, Any]:
    pages = vault.pages()
    if not pages:
        return {
            "action": "create_page",
            "target": "10_Knowledge/自律Wiki構築AI.md",
            "reason": "Vault is empty",
            "search_queries": [],
        }
    shallow = min(pages, key=lambda p: p.stat().st_size)
    return {
        "action": "improve_page",
        "target": str(shallow.relative_to(vault.root)),
        "reason": "Smallest page is a review candidate",
        "search_queries": [],
    }


def validate_action(action: dict[str, Any], config: Config) -> None:
    allowed = {"create_page", "improve_page", "add_links", "add_sources"}
    if action.get("action") not in allowed or not action.get("target"):
        raise ValueError("invalid action")
    Vault(config.vault_path).safe(action["target"])


def run_once(config: Config) -> dict[str, Any]:
    vault = Vault(config.vault_path)
    db = StateDB(vault.root / ".agent-state.sqlite3")
    db.sync_pages(vault)
    if (vault.root / "STOP_AGENT").exists():
        return {"result": "stopped"}
    action = choose_candidate(vault)
    validate_action(action, config)
    if config.mode == "manual":
        return {"result": "proposal", "action": action}
    target = Path(action["target"])
    if action["action"] == "create_page":
        vault.write(
            target,
            f"---\ntype: knowledge\nstatus: draft\ncreated: {datetime.now().date()}\nconfidence: low\n---\n\n# {target.stem}\n\n## 概要\n\n調査待ちのページです。\n\n## 未解決点\n\n- 追加調査が必要です。\n",
        )
    run_id = now()
    db.db.execute(
        "INSERT INTO runs VALUES (?, ?, ?, ?, ?, ?, ?)",
        (run_id, config.model, run_id, now(), "success", 0, None),
    )
    db.db.commit()
    if config.git_enabled and config.auto_commit and not Git(Path.cwd()).status():
        Git(Path.cwd()).commit("wiki: create initial autonomous wiki page")
    return {"result": "success", "action": action, "run_id": run_id}
