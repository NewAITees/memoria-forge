# 自律Wiki構築AI

## このプロジェクトの大きなゴール

このプロジェクトの目的は、単にMarkdownページを自動生成することではありません。

AI自身が、自分にとって見直しやすく、検索しやすく、後から再利用しやすい構造化Wikiを調査・設計・構築・改善し続けることが目的です。

AIは次の作業を自律的に行います。

- 現在のWikiを読む
- 情報の不足、重複、孤立、リンク不足、見直しにくさを発見する
- Wikiの構造や情報整理方法をWebで調査する
- 必要な情報を自分で調査し、ページとして記録する
- 既存ページを改善する
- ページ間の関連を判断して内部リンクを追加する
- IndexやMOCを更新する
- 出典、信頼度、未解決点、失敗、判断理由を保存する
- Wikiの構築方法そのものを改善する

WikiはAIの外部記憶であり、知識を保存するだけでなく、AIが次回以降の判断に使える構造を持つ必要があります。

### 知識を増やすことを最優先にする

このシステムは既存ページの改善だけを目的にしません。検索方式や構造の改善結果が変わらない場合でも、まだ調査していない関連情報があれば、新しい知識ページを作成します。

AIは次のタスクを状況に応じて選択します。

```text
expand_knowledge       新しい知識を追加
improve_page            既存ページを改善
add_links               関連ページを接続
build_structure         Wiki構造を作成・変更
research_method         Wiki構築方法を調査
review_old              古い情報を再調査
```

1回の実行では、通常1〜3ページ程度の新規作成または更新を行います。新規ページには、目的、概要、詳細、出典、信頼度、未解決点、関連リンクを含めます。

実行結果は、検索品質の改善だけでなく、知識の増加も評価します。

```text
expanded
improved
expanded_and_improved
unchanged
insufficient_evidence
blocked
```

`unchanged`であっても、新しい知識を発見できる場合は処理を継続します。Wikiの構造は固定せず、AIが調査と実験を通じて判断します。

## 構造を決め打ちしない

RAG、MOC、Markdown、キーワード検索、SQLite全文検索、ベクトル検索、ハイブリッド検索のどれが最適かは、最初から決めません。

AI自身が現在のWikiを使って実験し、次の観点から比較します。

- 必要な情報を見つけられるか
- 関連ページへ辿れるか
- 表記ゆれや日本語・英語の違いに対応できるか
- 出典まで到達できるか
- 複数ページの情報を統合できるか
- 検索結果の理由を説明できるか
- ページ追加後も検索品質を維持できるか
- 更新や保守が容易か

実験結果に基づいて、Wikiのページ構造、MOC、リンク設計、検索方式、RAG方式を選択します。採用しなかった方法と、その理由もWikiへ保存します。

## 自己改善ループ

```text
現在のWikiを読む
↓
Wikiの問題を発見する
↓
改善方法をWebで調査する
↓
実験方法と成功条件を自分で決める
↓
現在のWikiから評価質問を生成する
↓
複数の検索・構造化方式を比較する
↓
Wikiを小さく変更する
↓
変更前後を評価する
↓
良かった構造・失敗・判断理由を保存する
↓
次の改善候補を生成する
```

固定した実験用Corpusや固定した正解を前提にせず、実際に存在するVaultの内容から評価対象と質問を生成します。

## Wikiに保存する情報

- 知識と用語の定義
- 概念間の関係
- 再利用可能な手順
- 判断基準とポリシー
- 出典と取得日時
- 信頼度
- 未解決の疑問
- 調査履歴
- 失敗事例
- Wiki構造の実験結果
- 採用・不採用にした構築方法
- 次に試す改善案

つまり、知識そのものだけでなく、「どう整理すればAIが使いやすいか」というメタ知識も蓄積します。

## 現在の実装

Ollama、Web検索、Obsidian Vault、SQLite、Gitを接続する安全優先の実装です。

## 起動

```powershell
Copy-Item config.example.json config.json
uv run python run_agent.py --config config.json --once
```

初期モードは `manual` で、候補の提案だけを返します。自動適用する場合は `agent.mode` を `autonomous_safe` にし、Git自動コミットは明示的に有効化してください。Vault内に `STOP_AGENT` が存在する場合、処理は停止します。

現在の実装は、Vault境界検証、ページ一覧同期、候補選択、Planner・Writer・Reviewer、実Web検索、SQLite実行ログ、Git連携を提供します。検索方式の動的比較と、AI自身による次の改善案生成も実装しています。

### Vaultの変更をこのプロジェクトの一部としてコミット・push する

Wikiがこのマシンの外からでも「その日どう構造が変化したか」を追える状態にするため、Vault（`vault_path`が指すディレクトリ）はこのプロジェクトのリポジトリの一部として扱います。`.gitignore`ではVault内のMarkdownを除外していません（`.agent-state.sqlite3`のみ除外）。

`git.auto_commit`を有効にすると、ページが実際に書き込まれた回（`create_page` / `improve_page` / `expand_knowledge` / `create_structure`）ごとにVault配下の変更だけをコミットします。さらに`git.auto_push`を有効にすると、そのコミットを`origin`へpushします。push先はVaultが属するリポジトリ（＝このプロジェクト自身）で、pushはVaultディレクトリの変更が実際にある場合のみ行われ、force pushは行いません。

```json
"git": {"enabled": true, "auto_commit": true, "auto_push": true}
```

レビューに合格した内容だけがVaultへ書き込まれるため、push対象になるのは「Reviewerを通過したページ」のみです。ただしReviewerは完璧さではなく致命的な問題（プレースホルダー・出典欠落・事実誤認・安全性）だけを`blocking`として弾く設計なので、内容が浅い・改善途中のページがpushされることもあります。これは意図的な仕様です。失敗や未成熟な状態も含めてWikiの成長過程として記録・公開する、というこのプロジェクトの方針（「失敗事例」「未解決点」を削除せず保存する）に沿っています。

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

### Windows Task Schedulerへの登録

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\scripts\install_scheduler.ps1 -IntervalHours 24 -MaxRunMinutes 20
.\scripts\status_scheduler.ps1
```

登録されたタスクは、1回の処理が終了するとプロセスを終了し、次回の時刻に新しいプロセスとして起動します。失敗時は5分間隔で最大3回再起動します。解除は次で行います。

```powershell
.\scripts\uninstall_scheduler.ps1
```
