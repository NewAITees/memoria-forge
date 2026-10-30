# Memoria Forge ローカル記憶エンジン計画

作成日: 2026-10-25  
状態: Stage 1 完了、Stage 2 コアとVault Markdown入力を実装、RSS全文入力などは未完。Stage 3は新規ページ作成経路で実装済み  
対象: Memoria Forge のローカル記憶エンジン

## 目的

Supermemory の記憶ライフサイクルを参考に、文書を出典付きの原子的事実へ分解し、関係・時間・更新履歴を保持し、背景処理で再検討してから、質問時に必要な記憶をエージェントへ戻す仕組みを Memoria Forge 内に構築する。

これは Supermemory のホスト型サービス全体（Console、課金、複数テナント、OAuth コネクタ群）の複製ではない。Memoria Forge が既に扱う RSS、URL、Deep Research、Markdown/Vault を入力にするローカル単一プロジェクト向けの設計とする。

## 設計原則

1. **原文書を根拠の正本にする**: 原文と取得時点を保持し、事実・推論・ページから出典へ戻れるようにする。
2. **事実の言語と表示言語を分ける**: 内部主張は根拠の言語を保つ。日本語は検証後に表示用として生成し、原文引用は翻訳しない。
3. **関係の意味を区別する**: 同一、詳細追加、更新、矛盾、推論を別の関係として扱う。意味類似だけで更新や矛盾を作らない。
4. **現在と履歴を両立する**: 通常検索では有効な最新事実を優先し、過去の事実・根拠・更新履歴を監査・時点検索用に残す。
5. **背景処理中も原資料を検索できる**: Dreaming の完了を待たず原文書を取得可能にし、背景処理後に事実グラフを加える。
6. **忘却と消去を分ける**: 忘却は通常検索から外す操作、消去は文書とそこから派生したデータを永久削除する操作として区別する。
7. **不確実な推論を明示する**: 推論は元事実への由来、確信度、レビュー状態を保持し、明示された事実として扱わない。
8. **既存 DB を移行元にしない**: 新しい空の記憶 DB を使い、旧 DB の記憶データは移植しない。入力ソースから再取り込みできるものだけを再構築する。

## 7段階の実装計画

### Stage 1 — ドメイン契約と空の記憶ストア

**作業**

- Source document、Fact、Entity、Relation、Evidence、Event、Dream job の責務と状態遷移を定義する。
- スキーマバージョン付きの独立した SQLite 記憶ストアを新規作成する。既存 `.agent-state.sqlite3` のスキーマや内容は移行しない。
- 有効期間（valid time）とシステム記録時刻（recorded time）を分ける契約を決める。
- FK、ユニーク制約、トランザクション境界を設定する。

**成果物**: ドメインモデル、空 DB 初期化コード、スキーマ検証テスト。  
**合格条件**: 新規 DB のみで初期化・再起動でき、二重初期化でデータが増えず、FK と状態値が検証される。旧 DB には書き込まない。

### Stage 2 — 原資料の取り込み・保管・検索

**作業**

- RSS、URL/Deep Research、Markdown/Vault をソースアダプター経由で取り込む。
- 原文、URI、タイトル、MIME/種別、コンテンツハッシュ、取得日時、文書内日時を保存する。
- 変更された同一 URI は別バージョンとして記録し、同一内容の再送は冪等にする。
- Dreaming 待ちの job を作り、原文・チャンクは処理前から検索可能にする。

**成果物**: Source store、重複排除、チャンク化、取り込みキュー、原文検索。  
**合格条件**: 同一入力の再投入で重複せず、改訂入力は旧版を保持し、処理待ち中でも原文検索が成功する。

### Stage 3 — 原子的事実の抽出・証拠検証・日本語表示

**作業**

- 文書を、単独で理解できる一つの主張ずつに分割する。
- 主張に原文引用、Source ID、言語、時点、Fact/Preference/Episode/Inference 種別、確信度を付ける。
- 引用が指定ソースに実在すること、数値・固有名詞・否定・条件の不一致を決定的に検査し、独立 Reviewer で含意を確認する。
- 検証後に日本語表示文を作り、元主張・引用との翻訳忠実性をレビューする。
- Obsidian の5見出しページを記憶の正本ではなく人間向けの投影として生成する。

**成果物**: Fact extraction/verifier/localizer、根拠台帳、日本語 Wiki projection。  
**合格条件**: 各公開主張から引用・文書へたどれる。翻訳失敗、出典不一致、根拠不足の場合は公開せず理由を記録する。合成データと複数の実文書で同じ品質ゲートを通る。

### Stage 4 — Entity 解決と関係グラフ

**作業**

- 同一対象の表記ゆれ・別名を Entity ID に解決する。
- Fact 間の関係を `same`、`extends`、`updates`、`contradicts`、`derived_from` として記録する。
- 関係に確信度、作成理由、支持証拠、レビュー状態を持たせる。
- 自動判定が曖昧なら関係を作らず、保留状態にする。

**成果物**: Entity resolver、edge store、relation evaluator。  
**合格条件**: 同一・追加・置換・矛盾の評価セットで誤辺を集計し、類似トピックだけの事実を結ばない。推論辺は元 Fact に必ずたどれる。

### Stage 5 — 時間、更新、履歴、忘却

**作業**

- 新 Fact が旧 Fact を更新するとき、旧 Fact を削除せず `superseded` と置換先・有効終了時刻を記録する。
- 詳細追加は既存 Fact と併存させる。矛盾はどちらかを勝手に消さず、競合として保持する。
- 現在状態検索と時点指定検索を分ける。
- 忘却・期限切れは通常 Recall から除外し、監査履歴を保つ。完全消去要求ではソースと派生データの削除範囲を追跡する。

**成果物**: append-only event history、current-state projection、forget/expire/delete 操作。  
**合格条件**: 更新後の現在質問は新 Fact を返し、過去時点質問は旧 Fact を返す。忘却済み Fact は通常検索に出ず、完全消去後は派生 Fact/Edge/Cache も残らない。

### Stage 6 — Dynamic Dreaming と Recall/Context injection

**作業**

- 新しいソースが届いたとき・一定量たまったとき・処理が静穏になったときに、関連文書をまとまり単位で背景再検討する。
- 既存 Fact との同一性、追加、更新、矛盾、推論を再評価し、確信度を根拠に応じて調整する。
- job を冪等・再試行可能にし、失敗した batch が新しい batch を止めないようにする。
- 質問時は Fact、近傍 Edge、原文チャンクを組み合わせて Recall し、必要な記憶だけを Planner/Writer に注入する。
- プロジェクト常時プロフィール（安定設定）と質問依存 Recall（動的情報）を区別する。

**成果物**: Dream worker、再試行キュー、進捗/失敗記録、graph-aware Recall、agent adapter。  
**合格条件**: Dreaming の完了前でも直近ソースに回答でき、完了後は更新・関係・根拠を含む回答になる。background job の停止・再起動・再試行で重複 Fact/Edge を作らない。通常の agent 実行を長時間ブロックしない。

### Stage 7 — 評価、運用化、空 DB への切替

**作業**

- 「単純事実」「複数文書の追加」「更新」「矛盾」「時間」「忘却」「根拠付き推論」「未処理文書のRecall」を含む固定評価セットを作る。
- 引用精度、翻訳忠実性、Entity/Relation 精度、古い情報の誤検索、Recall 成功率、Dreaming 遅延、再試行率を測る。
- コピー DB で shadow run し、合格後に新しい空記憶 DB を通常運用へ切り替える。
- 旧 DB は記憶データの移行元にはしない。RSS/クラスタ/運用状態を再利用するか削除するかは、切替時に実ファイル一覧と再生成可能性を照合する。

**成果物**: 評価レポート、運用手順、切替・復旧手順。  
**合格条件**: 事前に定めた各品質ゲートを満たし、再起動後も履歴・queue・Recall が整合する。切替直後に原文検索・最新事実検索・履歴検索が動作する。

## 依存関係

```text
Stage 1 → Stage 2 → Stage 3 → Stage 4 → Stage 5 → Stage 6 → Stage 7
```

Stage 2 と Stage 3 は原文検索を早期に利用可能にするため段階的に接続する。Stage 4 以降の自動更新・推論・Forget は Stage 3 の証拠品質ゲートに合格するまで有効化しない。

## 実装状況（2026-10-26）

- **Stage 1 完了**: `src/memory_store.py` に独立 SQLite スキーマを作成。アプリケーション ID とスキーマ版を検証し、未知の既存 DB は変更せず拒否する。
- **Stage 2 コア完了**: 原文・ハッシュ・取得日時・チャンクを保存し、同一 URI の改訂を別バージョンとして保持する。同一内容の再投入は冪等。FTS5 検索と `new_source` Dreaming job を同一トランザクションで登録する。
- **Stage 2 部分接続**: 通常の新規ページ作成が使う検索結果の抜粋を `text/x-web-excerpt` として専用DBへ保存する。RSS/Deep Research 由来の検索結果もこの経路に乗る。`src/memory_ingest.py` で明示したVault内の可視Markdownを専用DBへ取り込める。Vault相対URIと内容hashで同一内容を冪等に扱い、変更版は別sourceとしてFTSチャンクとDream jobを登録する。隠しパス・symlink・junction・空/不正UTF-8ファイルは除外する。2026-10-28に`live-vault`の可視Markdown 886件を初回取り込みし、再実行で886件がunchanged、重複source/jobは0件。専用DB全体はsource 891件、Dream job 891件（全件pending）、Markdown chunk 1669件。Dream schedulerは1回の起動で最大10件を処理するため、既定の1時間間隔なら処理可能jobがすべて成功した場合でも約4日以上かかる見込み。失敗・再試行・実行時間によって延びる。RSS raw body全文とDeep Research全文は未接続で、ファイル削除時にDB記憶を自動消去しない。
- **Stage 3 完了（新規ページ作成経路）**: 既存の原子的事実抽出、決定的検査、含意レビュー、日本語翻訳、日本語翻訳レビューを通過したFactを、ページ作成時に専用DBへ保存する。Vault内の `.memory-engine.sqlite3` は既存 `.agent-state.sqlite3` と別管理し、Git対象外。Fact根拠が取得済み抜粋に見つからない場合は保存しない。既存の5見出しWiki投影を使う。既存ページ更新時のFact再構築は残課題。
- **Stage 4 基礎実装**: Entity名のUnicode正規化完全一致、別名衝突時の保留、active FactへのEntityリンク、関係の`proposed`保存、承認/却下イベントを実装。曖昧な意味類似による自動同一視や辺の自動確定はしない。別名の人手登録UIは未実装。
- **Stage 5 基礎実装**: `supersede_fact` が旧Factを履歴に残し、有効終了/開始時刻、`updates`辺、レビュー付きイベントを一トランザクションで保存する。`list_recall_facts` は現在検索と`as_of`時点検索を分け、忘却済みFactはどちらにも返さない。Forget操作もイベント付きで冪等。
- **Stage 5 消去基礎完了**: `erase_source` が同一URIの全バージョン、根拠Factと`derived_from`子孫、Edge、孤立Entity、Dream job、識別可能なイベントを削除し、識別子を持たない`source_deleted` tombstoneだけ残す。append-onlyイベント制約は消去処理中だけ制御関数で解除する。DB v1からv2への移行も実装。
- **Stage 5 残り**: CLI/画面から消去対象を選ぶ入口、期限切れ、旧`.agent-state.sqlite3`の歴史Factの監査は未実装。VaultのMarkdownページはユーザー文書として消去APIでは変更しない。
- **Stage 6 Recall接続済み、Dream worker基礎実装済み**: 承認済み・現在有効・日本語表示審査済みのFactを根拠文とURL付きでFTS検索し、Wiki Writerの調査コンテキストへ注入する。未承認、Forget済み、無効ソースのFactは検索結果から除外する。`run_agent.py --dream-once`は1件、`--dream-batch`は既定最大10件を処理する。個々のjobはatomic claimし、期限切れleaseを再取得し、失敗を上限付き指数バックオフでretryする。batchは失敗jobをretry状態にして次のready jobを続ける。Fact抽出・独立レビュー・日本語表示レビュー後に、最大20件のactive Factと関係候補を評価し、ID/型/確信度/根拠を検証したRelationだけを`proposed`で保存する。Relation自動承認、batch/quiet-period trigger、profile injection、再重み付けは未実装。
- **Stage 7 部分完了（2026-10-28）**: [固定受け入れ評価](memory_engine_evaluation_2026-10-28.md)を作り、根拠付きFact、Recall、Relation、時点履歴、Forget、完全消去、Dream retryを含むpytest 30件を実行し全件通過。これは決定的な保存・状態遷移の契約テストであり、実モデルの意味精度を測っていない。gold setによる実モデル評価、実Task Scheduler/shadow run、旧DB監査、切替・復旧は未実施のため運用DB切替は未承認。

専用ストアとパイプラインは `src/memory_store.py`、`src/memory_pipeline.py`、`src/memory_ingest.py`、`src/dream_worker.py`、関連テストで管理する。2026-10-28時点で記憶機能回帰36 passed、全体pytest 248 passed（既存feedparser DeprecationWarning 4件）。今回の変更ファイルのruff/format/mypyも通過。全体ruff/mypyは `tests/test_atomic_facts.py` と `tests/test_agent.py` に既存エラーがあり、全体formatは23ファイルに差分があるため未通過。Windows用の独立Task Scheduler登録手順は用意済みだが、タスク自体は未登録。既存ページ更新・RSS全文/Vault直接取り込み・profile injection・切替評価は残っている。

## DB リセット方針

- 新記憶エンジンは、専用の新規 DB ファイルを空の状態から作る。既存 Fact/Edge を移植しない。
- 既存 `.agent-state.sqlite3` は RSS 候補、クラスタ、task queue など記憶以外の運用状態も持つ可能性があるため、Stage 1 では変更・削除しない。
- Stage 7 で、どのデータをソースから再生成できるか確認した後に切替を行う。旧 DB の削除対象・時期は、実パスと内容を確認してから実行する。
- Vault の Markdown は元情報として残し、再取り込み可能な source document として扱う。

## Supermemory との対応と対象外

| Supermemory の機能 | Memoria Forge で対応する段階 |
|---|---|
| Document ingest / atomic memories | Stage 2–3 |
| Entity と意味のある graph relations | Stage 4 |
| Updates / extensions / contradictions / history / forget | Stage 5 |
| Dynamic Dreaming / reweighting / derivations | Stage 6 |
| Hybrid recall / graph traversal / profile injection | Stage 6 |
| connectors、Console、課金、マルチテナント SaaS | 対象外。既存 RSS/Web/Vault を利用するローカル単一プロジェクト向け |

## 参照

- [Supermemory Product: memory graph, lifecycle, profiles, recall](https://supermemory.ai/product/)
- [Introducing Dynamic Dreaming](https://supermemory.ai/blog/introducing-dynamic-dreaming-supermemory-now-connects-the-dots-for-you/)
- [How AI memory actually works](https://supermemory.ai/blog/how-ai-memory-works/)
- [Memory Graph Relationships: Updates, Extensions, and Inferences](https://supermemory.ai/blog/memory-graph-relationship-semantics/)
