# 自律Wiki構築AI

Ollama、Web検索、Obsidian Vault、SQLite、Gitを接続する安全優先の最小実装です。

## 起動

```powershell
Copy-Item config.example.json config.json
uv run python run_agent.py --config config.json --once
```

初期モードは `manual` で、候補の提案だけを返します。自動適用する場合は `agent.mode` を `autonomous_safe` にし、Git自動コミットは明示的に有効化してください。Vault内に `STOP_AGENT` が存在する場合、処理は停止します。

現在の初期版は、Vault境界検証、ページ一覧同期、候補選択、作成、SQLite実行ログ、Git連携を提供します。Ollamaと検索APIは `Ollama` / `Researcher` の境界に分離しており、次の実装でPlanner・Writer・Reviewerを接続できます。

定期実行は次で開始できます。停止する場合はVault直下に`STOP_AGENT`を作成してください。

```powershell
uv run python run_agent.py --config config.json --interval-hours 24
```

現在のVaultを使って検索方式を自動評価し、AI自身に次のWiki改善を提案させるには次を実行します。

```powershell
uv run python -m experiments.run_benchmark --vault live-vault --model qwen3:8b
```

この処理は固定Corpusを使わず、現在のMarkdown・内部リンク・実Ollamaから評価質問と次の改善案を生成し、結果を`90_System/Experiments/Latest Retrieval Experiment.md`へ保存します。

Windows Task SchedulerやWSLのsystemd timerから`--once`を定期起動する方法も推奨します。
