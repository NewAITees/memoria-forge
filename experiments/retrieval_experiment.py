"""Self-generated retrieval experiments over the current Vault."""

from __future__ import annotations

import json
import math
import re
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol, cast


def tokens(text: str) -> set[str]:
    lowered = text.casefold()
    words = set(re.findall(r"[a-z0-9_]{2,}", lowered))
    kana = re.findall(r"[一-龯ぁ-んァ-ヶー]", lowered)
    return words | {"".join(kana[i : i + 2]) for i in range(len(kana) - 1)}


@dataclass(frozen=True)
class Document:
    path: str
    title: str
    text: str
    links: tuple[str, ...]


class Retriever(Protocol):
    def search(self, query: str, limit: int = 5) -> list[str]: ...


class Corpus:
    def __init__(self, root: Path) -> None:
        self.root = root.resolve()
        self.documents: dict[str, Document] = {}
        for path in self.root.rglob("*.md"):
            if path.is_symlink():
                continue
            text = path.read_text(encoding="utf-8")
            relative = str(path.relative_to(self.root)).replace("\\", "/")
            self.documents[relative] = Document(
                relative,
                path.stem,
                text,
                tuple(re.findall(r"\[\[([^]|]+)", text)),
            )


class KeywordRetriever:
    def __init__(self, corpus: Corpus) -> None:
        self.corpus = corpus

    def search(self, query: str, limit: int = 5) -> list[str]:
        query_tokens = tokens(query)
        scored: list[tuple[float, str]] = []
        for path, document in self.corpus.documents.items():
            score = len(query_tokens & tokens(document.title + " " + document.text)) / max(
                len(query_tokens), 1
            )
            if score:
                scored.append((score, path))
        return [path for _, path in sorted(scored, reverse=True)[:limit]]


class MOCLinkRetriever:
    def __init__(self, corpus: Corpus) -> None:
        self.corpus = corpus

    def search(self, query: str, limit: int = 5) -> list[str]:
        query_tokens = tokens(query)
        mocs = [
            doc
            for doc in self.corpus.documents.values()
            if "moc" in doc.title.casefold() or "index" in doc.title.casefold()
        ]
        ranked = sorted(
            mocs, key=lambda doc: len(query_tokens & tokens(doc.title + doc.text)), reverse=True
        )
        found: list[str] = []
        for moc in ranked:
            for link in moc.links:
                path = next(
                    (
                        p
                        for p, doc in self.corpus.documents.items()
                        if doc.title == link or p == link
                    ),
                    None,
                )
                if path and path not in found:
                    found.append(path)
        return found[:limit]


class HybridRetriever:
    def __init__(self, corpus: Corpus) -> None:
        self.keyword = KeywordRetriever(corpus)
        self.moc = MOCLinkRetriever(corpus)

    def search(self, query: str, limit: int = 5) -> list[str]:
        return list(
            dict.fromkeys(self.keyword.search(query, limit) + self.moc.search(query, limit))
        )[:limit]


class OllamaVectorRetriever:
    def __init__(self, corpus: Corpus, base_url: str, model: str) -> None:
        self.corpus, self.base_url, self.model = corpus, base_url.rstrip("/"), model

    def _embed(self, texts: list[str]) -> list[list[float]]:
        payload = json.dumps({"model": self.model, "input": texts}).encode()
        request = urllib.request.Request(
            self.base_url + "/api/embed", data=payload, headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(request, timeout=300) as response:
            body: dict[str, Any] = json.loads(response.read())
        return cast(list[list[float]], body["embeddings"])

    def search(self, query: str, limit: int = 5) -> list[str]:
        paths = list(self.corpus.documents)
        vectors = self._embed(
            [query]
            + [self.corpus.documents[p].title + "\n" + self.corpus.documents[p].text for p in paths]
        )
        scores = [
            (self._cosine(vectors[0], vector), path) for path, vector in zip(paths, vectors[1:])
        ]
        return [path for _, path in sorted(scores, reverse=True)[:limit]]

    @staticmethod
    def _cosine(left: list[float], right: list[float]) -> float:
        denominator = math.sqrt(sum(x * x for x in left)) * math.sqrt(sum(x * x for x in right))
        return sum(x * y for x, y in zip(left, right)) / denominator if denominator else 0.0


def evaluate(
    retriever: Retriever, questions: list[dict[str, Any]], limit: int = 5
) -> dict[str, float]:
    recalls: list[float] = []
    ranks: list[float] = []
    for question in questions:
        results = retriever.search(question["query"], limit)
        relevant = set(question["relevant"])
        hits = [index for index, path in enumerate(results, 1) if path in relevant]
        recalls.append(1.0 if hits else 0.0)
        ranks.append(1 / hits[0] if hits else 0.0)
    return (
        {"recall_at_k": sum(recalls) / len(recalls), "mrr": sum(ranks) / len(ranks)}
        if questions
        else {"recall_at_k": 0.0, "mrr": 0.0}
    )


def generate_questions(client: Any, corpus: Corpus, count: int = 5) -> list[dict[str, Any]]:
    pages = [
        {"path": d.path, "title": d.title, "excerpt": d.text[:500]}
        for d in corpus.documents.values()
    ]
    result = client.chat(
        "Create retrieval evaluation questions from the current wiki. Return JSON with a questions array. Each question must contain query and relevant paths. Use only provided paths.",
        json.dumps({"pages": pages, "count": count}, ensure_ascii=False),
    )
    questions = result.get("questions", [])
    return [q for q in questions if isinstance(q, dict) and q.get("query") and q.get("relevant")]


def run_live_benchmark(corpus_root: Path, client: Any) -> dict[str, Any]:
    corpus = Corpus(corpus_root)
    if len(corpus.documents) < 3:
        return {
            "status": "insufficient_corpus",
            "document_count": len(corpus.documents),
            "questions": [],
            "next_action": "Create or improve connected wiki pages before comparing retrieval methods.",
        }
    questions = generate_questions(client, corpus)
    results: dict[str, Any] = {
        "status": "evaluated" if questions else "question_generation_failed",
        "document_count": len(corpus.documents),
        "questions": questions,
        "keyword": evaluate(KeywordRetriever(corpus), questions),
        "moc": evaluate(MOCLinkRetriever(corpus), questions),
        "hybrid": evaluate(HybridRetriever(corpus), questions),
    }
    return results


def propose_next_action(
    client: Any, corpus_root: Path, benchmark: dict[str, Any]
) -> dict[str, Any]:
    corpus = Corpus(corpus_root)
    return cast(
        dict[str, Any],
        client.chat(
            "Inspect the current wiki experiment result and propose exactly one next wiki improvement. Return JSON with action, target, reason, and expected_changes.",
            json.dumps(
                {"pages": list(corpus.documents), "benchmark": benchmark}, ensure_ascii=False
            ),
        ),
    )


def write_report(corpus_root: Path, benchmark: dict[str, Any], proposal: dict[str, Any]) -> Path:
    report_dir = corpus_root / "90_System" / "Experiments"
    report_dir.mkdir(parents=True, exist_ok=True)
    report = report_dir / "Latest Retrieval Experiment.md"
    report.write_text(
        "# Latest Retrieval Experiment\n\n## Result\n\n```json\n"
        + json.dumps(benchmark, ensure_ascii=False, indent=2)
        + "\n```\n\n## Next AI-Selected Action\n\n```json\n"
        + json.dumps(proposal, ensure_ascii=False, indent=2)
        + "\n```\n",
        encoding="utf-8",
    )
    return report
