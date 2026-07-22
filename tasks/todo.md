## 運用ルール
1. タスクを追加するときはチェックボックス形式で書く
2. 完了したら [x] にする
3. セクションが全て完了したら、セクションごと削除してよい

## 初期実装
- [x] プロジェクト基盤と設定を作成する
- [x] Vault安全境界・SQLite・Git操作を実装する
- [x] Observer/Planner/Researcher/Writer/Reviewerを実装する
- [x] 実行CLIとログを実装する
- [x] テストとドキュメントを追加する
- [x] 全検証を実行し、Lessonsを更新する

## 安全性・品質改善（設定検証・重複検出）
- [x] `Config.validate()`を追加し、`mode`・`ollama_url`・`model`・各種上限値を起動時に検証する
- [x] `find_similar_page()`を追加し、`create_page`前に類似タイトルの既存ページへ`improve_page`として自動リダイレクトする
- [x] `Git`クラスの操作対象を`Path.cwd()`からVault側（`vault.root`）へ修正し、非gitリポジトリでは安全に何もしないようにする
- [x] 上記の回帰テストを追加する
- ロールバック機能（変更前後の検索品質比較・悪化時の自動復元）は今回見送り。理由: 本来の要件は検索品質ベースの比較であり、単純な例外時ファイル復元では不十分。別プロセスが`experiments/`配下で検索実験を進めているため、その成果を踏まえて改めて検討する。

## モデル比較計画
- [x] `qwen3:8b`を初期正式モデルとして継続使用する
- [x] `qwen3.5:4b`を追加取得する
- [x] 同一課題で5モデルを実データ比較する（本番Vaultは変更せず一時コピーを使用）
- [x] 推論速度を比較する
- [x] JSON出力の安定性を比較する
- [ ] 日本語品質を比較する
- [x] Planner / Writer / Reviewer適性を実Ollamaで確認する
- [x] 結果をLessonsへ記録する
- [ ] 比較結果に基づき採用モデルを決定する

## Vaultのコミット・push（外部からWikiの変化を確認できるように）
- [x] `.gitignore`から`live-vault/`の除外を解除し、`.agent-state.sqlite3`のみ除外する
- [x] `Config`に`git.auto_push`を追加する
- [x] `Git.push()`を追加し、現在のブランチを`origin`へpushする（force無し）
- [x] `Git.status()`をVaultディレクトリへのpathspecでスコープし、リポジトリ全体の無関係な差分に反応しないようにする
- [x] `commit_and_push()`を追加し、`create_page`/`improve_page`/`expand_knowledge`/`create_structure`いずれの成功パスでも、Vaultに実際の変更がある場合だけコミット・pushする
- [x] 回帰テストを追加する（bareリモートを使ったpush実証を含む）
- [x] READMEに方針と理由（失敗や未成熟なページも含めて成長過程を記録・公開する）を明記する
- [x] 別プロセスとのpush競合（non-fast-forward）でrun全体がクラッシュしないよう、`Git.push()`にfetch+rebaseの1回リトライを実装し、成功／失敗を`commit_and_push()`の戻り値として返す（例外を投げない）
- [x] `run_once()`の結果に`git_status`（`skipped`/`committed`/`pushed`/`push_failed`）を含める
- [x] push競合・rebase失敗の回帰テストを追加する（2つのクローンから同じbareリモートへ競合push/非競合pushの両方を再現）

## 反省・失敗の自動記録
- [x] `StateDB.record_reflection()`を追加し、`reflections`テーブルへ書き込めるようにする
- [x] `plan_rejected`（repair_plan失敗時）で反省を記録する
- [x] `create_structure`/`expand_knowledge`のReviewer拒否で`runs`記録の欠落を修正し、反省も記録する
- [x] `create_page`/`improve_page`のReviewer拒否で反省を記録する
- [x] `push_failed`時に反省を記録する
- [x] 回帰テストを追加する

## 鮮度管理
- [x] `sync_pages()`の`updated_at`を`now()`からファイルの実mtimeへ修正する（毎回上書きされ鮮度判定が機能しない不具合を修正）
- [x] `StateDB.stale_pages(days)`を追加し、閾値より古いページを検出する
- [x] `Config.stale_days`（既定30日）を追加し、`validate()`・`config.example.json`に反映する
- [x] `choose_candidate()`が`db`を受け取れるようにし、staleなページがあれば優先的に`improve_page`候補にする
- [x] `Ollama.plan()`のプロンプト/ペイロードに`stale_pages`を追加し、autonomous_safeモードのPlannerも古いページを考慮できるようにする
- [x] 回帰テストを追加する

## 実行監視（ヘルスレポート）
- [x] `StateDB.status_summary(stale_days, recent_limit)`を追加する（直近run・result別件数・stale件数・reflection件数）
- [x] `run_agent.py --status`を追加し、エージェントを実行せず読み取り専用でレポートを出力する
- [x] 回帰テストを追加する
- [x] 実際の`live-vault`に対して`--status`を実行し、動作確認する

## 知識拡張方針
- [x] `expand_knowledge`を主要タスクとして実装する
- [ ] 改善結果が変わらない場合でも新規知識を追加できるようにする
- [x] 1回の実行で1〜3ページを作成・更新する制限を実装する
- [x] 新規ページへ概要・詳細・出典・信頼度・未解決点・関連リンクを付与する
- [x] `expanded` / `improved` / `expanded_and_improved`を実行結果に記録する
- [x] AIがWiki構造を自律的に選択・変更できるようにする
- [x] 知識拡張と構造改善を別タスクとして継続実行する
- [x] 固定MOC/Index条件を廃止し、Vaultスナップショットに基づくLLM判断へ移行する
- [x] 欠落したアクション項目を1回だけ再計画する
- [x] qwen3構造化タスクのthinkingを無効化する
