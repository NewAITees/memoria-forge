"""Test AIBackgroundWorker-style unconstrained final Markdown generation."""

from __future__ import annotations

import json
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.wiki_agent import (  # noqa: E402
    Config,
    create_reviewer_client,
    format_deep_research,
    normalize_page,
    review_is_blocking,
    validate_page_content,
)


def main() -> None:
    output = ROOT / "experiments" / "document_quality_result"
    deep = json.loads((output / "research.json").read_text(encoding="utf-8"))
    context, sources = format_deep_research(deep)
    config = Config.load(ROOT / "config.json")
    system = (
        "あなたは技術調査レポートの編集者です。根拠にない内容は書かず、製品世代と比較軸を混同しません。"
        "調査材料の見出しをコピーせず、CS-4に直接関係する事実を中心に日本語Markdownを完成させてください。"
        "frontmatterにはtitle,type,status,created,updated,confidenceを含めます。本文は順に # 日本語タイトル、"
        "## 概要、## 詳細、## 出典、## 未解決点。詳細内は順に ### 結論、### 根拠から確認できる事実、"
        "### 情報源ごとの差分、### 時系列、### 制約と適用範囲。結論は1〜3文。"
        "CS-3以前の情報はCS-4の事実として扱いません。比較値は比較対象と条件を併記します。"
        "本文中に最低2件のMarkdownリンクを置き、出典一覧にも同じURLを記載します。"
    )
    prompt = (
        "テーマ: Cerebras CS-4の推論性能、GPU比較、導入上の制約\n\n"
        "次の調査材料だけを使ってレポートを作成してください。\n\n" + context
    )
    payload = {
        "model": config.model,
        "stream": False,
        "think": False,
        "keep_alive": "10m",
        "options": {"temperature": 0.5, "num_predict": -1},
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": prompt}],
    }
    request = urllib.request.Request(
        config.ollama_url.rstrip("/") + "/api/chat",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=None) as response:
        raw = json.loads(response.read())["message"]["content"]
    page = normalize_page(Path("Cerebras CS-4.md"), raw, sources)
    (output / "plain-markdown.md").write_text(page, encoding="utf-8")
    verdict: dict[str, object] = {}
    try:
        validate_page_content(page, sources)
        verdict["deterministic"] = "passed"
        review = create_reviewer_client(config).review(page, context)
        verdict["review"] = review
        verdict["accepted"] = not review_is_blocking(review)
    except ValueError as error:
        verdict = {"deterministic": "failed", "accepted": False, "error": str(error)}
    (output / "plain-verdict.json").write_text(
        json.dumps(verdict, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(verdict, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
