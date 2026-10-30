"""Run a shadow experiment: source documents -> verified atomic facts -> page."""

from __future__ import annotations

import argparse
import hashlib
import json
import sqlite3
import time
from dataclasses import asdict
from pathlib import Path
from typing import Any

from experiments.atomic_fact_graph import Fact, FactStore, RELATIONS, SourceDocument, normalize_evidence
from src.wiki_agent import Ollama


DEFAULT_CLUSTER_ID = 1718
DEFAULT_TARGET = "Kubernetes HPA on Amazon EKS: Scaling from 2 to 6 Pods Under Load"
SOURCE_LIMIT = 5

FACT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "facts": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "statement": {"type": "string"},
                    "evidence_quote": {"type": "string"},
                    "confidence": {"type": "number"},
                },
                "required": ["statement", "evidence_quote", "confidence"],
            },
        }
    },
    "required": ["facts"],
}

RELATION_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "relations": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "from_fact_id": {"type": "string"},
                    "to_fact_id": {"type": "string"},
                    "relation": {"type": "string", "enum": sorted(RELATIONS)},
                    "confidence": {"type": "number"},
                },
                "required": ["from_fact_id", "to_fact_id", "relation", "confidence"],
            },
        }
    },
    "required": ["relations"],
}

SELECTION_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "selected_fact_ids": {"type": "array", "items": {"type": "string"}},
        "excluded_fact_ids": {"type": "array", "items": {"type": "string"}},
        "reason": {"type": "string"},
    },
    "required": ["selected_fact_ids", "excluded_fact_ids", "reason"],
}


def _document_id(url: str) -> str:
    return "doc-" + hashlib.sha256(url.encode()).hexdigest()[:12]


def load_sources(database: Path, cluster_id: int, target: str) -> list[SourceDocument]:
    connection = sqlite3.connect(f"file:{database.as_posix()}?mode=ro", uri=True)
    rows = connection.execute(
        "SELECT r.url, r.title, r.snippet FROM cluster_members m "
        "JOIN rss_candidates r ON r.url = m.url WHERE m.cluster_id = ?",
        (cluster_id,),
    ).fetchall()
    connection.close()
    if not rows:
        raise ValueError(f"cluster {cluster_id} has no source documents")

    target_terms = {part.casefold() for part in target.split() if len(part) >= 3}

    def relevance(row: tuple[str, str, str]) -> tuple[int, int]:
        title_terms = {part.casefold() for part in row[1].split()}
        exact = int(row[1].casefold() == target.casefold())
        return exact, len(target_terms & title_terms)

    selected = sorted(rows, key=relevance, reverse=True)[:SOURCE_LIMIT]
    return [
        SourceDocument(_document_id(url), title, url, normalize_evidence(snippet))
        for url, title, snippet in selected
    ]


def extract_facts(client: Ollama, source: SourceDocument) -> list[Fact]:
    response = client.chat(
        "Extract atomic facts from one source. Return JSON only. Every evidence_quote must be "
        "a short verbatim substring copied from SOURCE. Do not infer, combine sentences, translate "
        "the quote, or add outside knowledge. Each statement must express exactly one fact. "
        "Return at most 8 high-value facts.",
        f"TITLE: {source.title}\nURL: {source.url}\nSOURCE:\n{source.content[:16000]}",
        FACT_SCHEMA,
    )
    facts: list[Fact] = []
    for index, item in enumerate(response.get("facts", [])):
        if not isinstance(item, dict):
            continue
        facts.append(
            Fact(
                fact_id=f"{source.document_id}-fact-{index + 1}",
                statement=str(item.get("statement", "")).strip(),
                evidence_quote=str(item.get("evidence_quote", "")).strip(),
                source_document_id=source.document_id,
                confidence=float(item.get("confidence", 0.0)),
            )
        )
    return facts


def link_facts(client: Ollama, facts: list[Fact]) -> list[dict[str, Any]]:
    compact = [{"fact_id": fact.fact_id, "statement": fact.statement} for fact in facts]
    response = client.chat(
        "Compare atomic facts. Return only meaningful relations: same for semantic duplicates, "
        "extends for compatible added detail, updates only when a later fact replaces an earlier "
        "state, and contradicts for claims that cannot both be true. Do not create topical-similarity "
        "edges. Return JSON only.",
        json.dumps(compact, ensure_ascii=False),
        RELATION_SCHEMA,
    )
    existing = {fact.fact_id for fact in facts}
    valid: list[dict[str, Any]] = []
    for relation in response.get("relations", []):
        if not isinstance(relation, dict):
            continue
        if (
            relation.get("from_fact_id") in existing
            and relation.get("to_fact_id") in existing
            and relation.get("relation") in RELATIONS
        ):
            valid.append(relation)
    return valid


def select_facts(client: Ollama, target: str, facts: list[Fact]) -> tuple[list[Fact], dict[str, Any]]:
    compact = [
        {"fact_id": fact.fact_id, "statement": fact.statement, "source": fact.source_document_id}
        for fact in facts
    ]
    response = client.chat(
        "Select only facts that directly answer the requested page topic. Exclude facts that merely "
        "share a broad technology such as Kubernetes. Do not add facts. Return JSON only.",
        f"TOPIC: {target}\nFACTS:\n{json.dumps(compact, ensure_ascii=False)}",
        SELECTION_SCHEMA,
    )
    chosen = set(response.get("selected_fact_ids", []))
    return [fact for fact in facts if fact.fact_id in chosen], response


def render_page(target: str, facts: list[Fact], sources: dict[str, SourceDocument]) -> str:
    lines = [f"# {target} — 原子的事実グラフ実験", "", "## 検証済みの事実", ""]
    for fact in facts:
        source = sources[fact.source_document_id]
        lines.extend(
            [
                f"- {fact.statement} [^{fact.fact_id}]",
                f"  - 根拠: 「{fact.evidence_quote}」",
                "",
            ]
        )
    lines.extend(["## 出典", ""])
    for fact in facts:
        source = sources[fact.source_document_id]
        lines.append(f"[^{fact.fact_id}]: [{source.title}]({source.url})")
    return "\n".join(lines).rstrip() + "\n"


def run(args: argparse.Namespace) -> dict[str, Any]:
    started = time.perf_counter()
    args.output.mkdir(parents=True, exist_ok=True)
    sources = load_sources(args.database, args.cluster_id, args.target)
    client = Ollama(args.ollama_url, args.model, timeout=None, num_ctx=16384)
    database = args.output / "atomic-facts.sqlite3"
    if database.exists():
        database.unlink()

    verified: list[Fact] = []
    with FactStore(database) as store:
        for source in sources:
            store.add_source(source)
            for fact in extract_facts(client, source):
                if store.add_fact(fact):
                    verified.append(fact)
        relations = link_facts(client, verified)
        for relation in relations:
            store.add_relation(
                str(relation["from_fact_id"]),
                str(relation["to_fact_id"]),
                str(relation["relation"]),
                float(relation["confidence"]),
            )
        rejected_count = store.rejected_count()
        relation_count = store.relation_count()

    selected, selection = select_facts(client, args.target, verified)
    source_map = {source.document_id: source for source in sources}
    page = render_page(args.target, selected, source_map)
    (args.output / "fact-grounded-page.md").write_text(page, encoding="utf-8", newline="\n")
    result = {
        "cluster_id": args.cluster_id,
        "target": args.target,
        "source_count": len(sources),
        "verified_fact_count": len(verified),
        "rejected_fact_count": rejected_count,
        "relation_count": relation_count,
        "selected_fact_count": len(selected),
        "verified_fact_ratio": len(verified) / (len(verified) + rejected_count)
        if verified or rejected_count
        else 0.0,
        "selected_facts": [asdict(fact) for fact in selected],
        "selection": selection,
        "sources": [asdict(source) | {"content": "[omitted]"} for source in sources],
        "elapsed_seconds": round(time.perf_counter() - started, 2),
        "comparison": {
            "current_page_claim_to_evidence_links": 0,
            "fact_grounded_page_claim_to_evidence_links": len(selected),
            "current_page_known_issue": (
                "The page states that only one listed article directly relates to its topic, "
                "yet synthesizes unrelated GPU cost, Kubeflow, GKE upgrade, and security material."
            ),
        },
    }
    (args.output / "result.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n"
    )
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--database", type=Path, default=Path("live-vault/.agent-state.sqlite3"))
    parser.add_argument("--cluster-id", type=int, default=DEFAULT_CLUSTER_ID)
    parser.add_argument("--target", default=DEFAULT_TARGET)
    parser.add_argument("--ollama-url", default="http://localhost:11434")
    parser.add_argument("--model", default="qwen3:8b")
    parser.add_argument("--output", type=Path, default=Path("experiments/atomic_fact_result"))
    args = parser.parse_args()
    print(json.dumps(run(args), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
