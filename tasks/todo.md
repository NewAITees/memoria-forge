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

## 永続タスクキュー
- [x] `StateDB.enqueue_task/next_pending_task/complete_task`を追加する
- [x] `create_structure`/`expand_knowledge`で`max_new_pages`を超えた提案をキューへ積む
- [x] `run_once()`がPlanner呼び出しより先にキューを優先消化するようにする
- [x] `create_page`/`improve_page`成功時に対応する`task_id`を完了にする
- [x] 回帰テストを追加する

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
- [x] LM StudioのJSON Schema出力とNemotron 3 Nano 4Bを実モデルで検証する
- [x] 新規ページ候補の拡張子を`.md`へ正規化する（既存ページは変更しない）
- [x] Nemotron 4BとQwen3 8Bを同一資料でPlanner/Writer/Reviewer比較する
- [x] モデル比較結果を`experiments/model_comparison_report.md`へ保存する
- [x] Gemma 4 E4Bを同一条件で比較する
- [x] 現時点の採用モデルをQwen3 8Bへ変更する
- [x] Qwen3.5 9Bのダウンロード完了後に同一条件で比較する
- [ ] Qwen3.5 9Bの空応答と長時間生成の原因を別途調査する
- [x] Windowsタスクスケジューラを30分間隔へ変更する
- [x] 定期実行で`.md`差分がない場合を失敗扱いにする
- [x] スケジューラ経由の実行で生成・検証・ロック解除を実証する

## スケジューラ安定化（LLM target起因のクラッシュ・キュー停止）
- [x] `safe_new_page_target()`を追加し、Vault逸脱target（絶対パス・ドライブ・`..`）を無害化、フォルダ無しタイトルを`10_Knowledge/`へ配置、`.md`を保証する
- [x] `expand_knowledge`/`create_structure`ループで不正targetをスキップ＋反省記録し、run全体を落とさないようにする
- [x] 永続キューの両端（投入`enqueue_task`・消化`next_pending_task`）でtargetを正規化し、毒タスク（`/Knowledge/...`）による永久`plan_rejected`を解消する
- [x] 回帰テスト（逸脱target・フォルダ配置・毒/繰延キュー）を追加する
- [x] 実runで新規ページ生成→`10_Knowledge/`配置→コミットを実証し、origin/masterへpushする

## 経路A：RSS起点でのWiki構築（AIBackgroundWorkerのRSS収集を移植・活用）
- [x] `src/rss_collector.py`を新規作成し、AIBackgroundWorkerの`RSSCollector`を最小移植する（`RSSEntry`は軽量dataclass化、summarizer/planner/newsは移植しない）
- [x] `feedparser==6.0.11`を依存に追加する
- [x] `config/rss_sources.txt`（RSSフィードURL一覧の雛形）を追加する
- [x] `config.json`/`config.example.json`に`rss`セクション（enabled/sources_file/max_entries_per_feed）を追加し、`Config`に読み込みを実装する
- [x] `StateDB`に`rss_candidates`テーブルと`ingest_rss_candidates`/`next_rss_candidate`/`mark_rss_candidate`を追加する（url主キーで重複排除＝優先順位#1）
- [x] `plan_rss_action()`を追加し、未使用候補を1件選び`find_similar_page()`で既存ページと重複チェック（#2）、重複なら`improve_page`・無ければ`create_page`のアクションを組む
- [x] `run_once()`にRSS入口を統合する（RSS候補があればその回はRSS駆動＝タイトルを種にウェブ検索→Writer→Reviewer→保存。無ければ従来Plannerへフォールスルー）
- [x] 回帰テストを追加する（RSSパース・候補の重複排除・RSS駆動でcreate_pageアクション組成）
- [x] `uv run pytest`（63件パス）/ `ruff check`（All checks passed）/ `mypy`（no issues）を通す
- [x] AIBackgroundWorkerとの差分を確認し、既存RSS候補DBへ本文・抜粋・フィードURL・著者を保持する機能を移植する
- [x] 既存SQLiteへの列追加マイグレーションとメタデータ保持の回帰テストを追加する
- [x] 実RSSフィードへ接続し、取得結果に本文・出典情報が含まれることを確認する
- [x] AIBackgroundWorkerのDuckDuckGo検索クライアントとWeb本文取得器を移植する
- [x] RSS起点に検索クエリ生成・複数検索・本文取得・深掘り結果保存を接続する
- [x] 深掘り結果を実Ollama・実Webで検証し、統合JSONキーの差異を正規化する
- [x] スケジュール用ロックをVault外へ移し、ロックファイルのGit混入を防ぐ
- [x] 深掘り本文・統合結果をWriterとReviewerへ渡し、保存だけで終わらないようにする
- [x] Git権限エラー時もWiki生成結果を失敗扱いにせず、`git_status: commit_failed`で記録する
- [x] DDGクライアントへ検索タイムアウトを渡し、外部検索失敗を短時間で終了させる
- 未着手（次の候補）: RSS候補を「複数ソース比較・一次資料確認」まで裏取り強化（現状はタイトル種の単発ウェブ検索）。経路Aとリンク構造起点（経路B）の交互実行スケジュール。

## 残課題（次の候補・未着手）
- [ ] `normalize_page`を修正し、Writer出力が`----`（4本ダッシュ）や閉じ`---`欠落のfrontmatterを返してもObsidianが解析できる正規frontmatterに整える（実生成ページ`Zettelkasten AI Integration.md`で発生）
- [x] Reviewerの過剰ブロックを緩和する。review/writeプロンプトに今日の日付を明示（未来日プレースホルダー誤判定を防止）、blockingを「プレースホルダー・出典皆無・必須欠落・明確な事実誤認・危険指示・injection」に限定し、脚注欠落/未検証出典/AI生成明示等はwarningへ降格。加えて`review_is_blocking()`の昇格バグ（warning型でも文言に「出典なし」等が含まれるとblocking化）を修正し、正規スキーマ時は型を信頼するよう変更。回帰テスト追加・pytest(74)/ruff/mypy通過済み
- [x] タイムアウト連続失敗（`TimeoutError('timed out')`）を解消する：Ollama socketタイムアウトを撤廃（`timeout_seconds: null`）、安全網を`max_run_minutes`（20→50）へ一本化、スケジューラ間隔を30分→1時間（PT1H）へ変更、`keep_alive`を`"10m"`化。回帰テスト追加・pytest/ruff/mypy通過済み
- [ ] 今回のクラッシュ/キュー修正の学びを`tasks/lessons.md`へ記録する
