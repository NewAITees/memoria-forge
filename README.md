# 自律Wiki構築AI

Ollama、Web検索、Obsidian Vault、SQLite、Gitを接続する安全優先の最小実装です。

## 起動

```powershell
Copy-Item config.example.json config.json
uv run python run_agent.py --config config.json
```

初期モードは `manual` で、候補の提案だけを返します。自動適用する場合は `agent.mode` を `autonomous_safe` にし、Git自動コミットは明示的に有効化してください。Vault内に `STOP_AGENT` が存在する場合、処理は停止します。

現在の初期版は、Vault境界検証、ページ一覧同期、候補選択、作成、SQLite実行ログ、Git連携を提供します。Ollamaと検索APIは `Ollama` / `Researcher` の境界に分離しており、次の実装でPlanner・Writer・Reviewerを接続できます。
