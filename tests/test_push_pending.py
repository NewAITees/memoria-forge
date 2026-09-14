import subprocess
from pathlib import Path

from src.wiki_agent import Config, Vault, push_pending


def _git(*args: str) -> str:
    return subprocess.run(["git", *args], check=True, capture_output=True, text=True).stdout


def _repo_with_remote(tmp_path: Path) -> tuple[Path, Path]:
    remote_dir = tmp_path / "remote.git"
    _git("init", "--bare", str(remote_dir))
    _git("--git-dir", str(remote_dir), "symbolic-ref", "HEAD", "refs/heads/main")
    repo_dir = tmp_path / "repo"
    _git("init", str(repo_dir))
    _git("-C", str(repo_dir), "symbolic-ref", "HEAD", "refs/heads/main")
    _git("-C", str(repo_dir), "config", "user.email", "test@example.com")
    _git("-C", str(repo_dir), "config", "user.name", "Test")
    _git("-C", str(repo_dir), "remote", "add", "origin", str(remote_dir))
    return repo_dir, remote_dir


def _config(tmp_path: Path, auto_push: bool = True) -> Config:
    return Config(
        tmp_path / "unused-vault", git_enabled=True, auto_commit=True, auto_push=auto_push
    )


def test_push_pending_commits_leftover_changes_and_pushes_earlier_commits(tmp_path: Path) -> None:
    repo_dir, remote_dir = _repo_with_remote(tmp_path)
    vault = Vault(repo_dir)
    vault.write("page.md", "# Page")
    _git("-C", str(repo_dir), "add", "-A")
    _git("-C", str(repo_dir), "commit", "-m", "wiki: page committed earlier")
    vault.write("20_MOC/MOC-001.md", "# MOC")

    assert push_pending(vault, _config(tmp_path)) == {"status": "pushed", "error": ""}

    remote_log = _git("--git-dir", str(remote_dir), "log", "--oneline", "main")
    assert "wiki: page committed earlier" in remote_log
    assert "chore: refresh generated MOC pages" in remote_log
    assert _git("-C", str(repo_dir), "status", "--porcelain") == ""


def test_push_pending_reports_the_push_error(tmp_path: Path) -> None:
    repo_dir, _ = _repo_with_remote(tmp_path)
    _git("-C", str(repo_dir), "remote", "set-url", "origin", str(tmp_path / "missing.git"))
    vault = Vault(repo_dir)
    vault.write("page.md", "# Page")

    status = push_pending(vault, _config(tmp_path))

    assert status["status"] == "push_failed"
    assert "missing.git" in status["error"]


def test_push_pending_skips_when_auto_push_is_off(tmp_path: Path) -> None:
    repo_dir, _ = _repo_with_remote(tmp_path)
    vault = Vault(repo_dir)
    vault.write("page.md", "# Page")
    assert push_pending(vault, _config(tmp_path, auto_push=False)) == {
        "status": "skipped",
        "error": "",
    }
