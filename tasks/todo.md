## 運用ルール
1. タスクを追加するときはチェックボックス形式で書く
2. 完了したら [x] にする
3. セクションが全て完了したら、セクションごと削除してよい

## Wiki実モデル却下の追加調査（2026-10-30）
- [x] Fact ID重複をReviewer前に除去し、重複candidateを記録する
- [x] 関連・全pytest、ruff、format、mypyを確認する（全259 passed、feedparser DeprecationWarning 4件）
- [x] scheduled実行1回の生応答を保存・確認する（Fact重複は解消、ページはReviewer blockingで未保存。MOC更新はcommit/push済み）
- [x] Reviewerの矛盾応答に対し、単一ソースとmedium confidenceを根拠にblockしないこと、approvedとtyped issueの整合規則をプロンプトと回帰テストへ追加する
- [x] 修正後の実モデル検証を試行する（実行は`max_run_minutes=50`でtimeout。応答ログは5件で、Fact抽出・Reviewer判定まで到達した証拠なし）
- [ ] Reviewerまで到達した次回実行で判定を確認する（追加ライブ実行は未実施）

## 記憶エンジン Stage 2 RSS / Deep Research入力（2026-10-30）
- [x] RSSの本文とsummaryを区別し、summaryしかない場合に本文として保存しない
- [x] 取得できたRSS本文をページ生成成否と独立にMemoryStoreへ保存し、重複再投入が冪等であることを検証する
- [x] Deep Researchの全文JSON（統合結果と取得ページ本文を含む）をページ生成・Reviewer結果に関係なくMemoryStoreへ保存する
- [x] 関連66件、ruff、format、mypyを確認する（feedparser DeprecationWarning 4件）
- [ ] RSSがsummaryしか提供しない場合に記事全文を取得・保存する経路を実装・検証する
- [x] Stage 2のコード契約を含む全体pytestを再確認する（2026-10-30、273 passed、4 feedparser DeprecationWarning。RSS summaryだけの場合の記事全文取得は別途未実装）

## 記憶エンジン Stage 4 レビュー済み別名登録（2026-10-30）
- [x] Entity aliasの人手レビュー済み登録APIを追加し、空値・未知Entity・別Entityとの衝突を拒否する
- [x] reviewer/reason/timeをappend-only監査テーブルへ保存し、同一レビューの再送を冪等にする
- [x] schema v2→v3とv1→v3移行をテストする
- [x] memory store/pipeline/Dream worker関連40件、ruff、format、mypyを確認する
- [ ] 人向けalias審査UI/CLIを作成する

## 記憶エンジン Stage 5 source消去CLI（2026-10-30）
- [x] `--memory-sources`でsource ID・URI・状態などを一覧表示する
- [x] `--memory-erase-source`は確認フラグなしでは拒否し、確認付きで同一URIの全版と派生Dream jobを消去する
- [x] CLI一覧・確認拒否・確認オプション誤用・消去の回帰テストを追加する
- [x] memory store/CLI関連テストを実行する（現時点34件通過）
- [ ] Stage 5期限切れと旧.agent-state.sqlite3の歴史Fact監査を実装する

## 記憶ソース取り込み責務の局所リファクタリング（2026-10-30）
- [x] MemoryStoreへの汎用ソース保存、RSS本文、Deep Research JSON保存を`src/memory_sources.py`へ分離する
- [x] `wiki_agent.py`から既存の取り込み経路を使い、動作と失敗時のbest-effort方針を維持する
- [x] 関連49件、ruff、format、mypy、diff whitespaceを確認する
- [x] `run_agent.py`の記憶source一覧・消去操作を`src/memory_cli.py`へ分離する
- [x] CLI/store関連34件、ruff、format、mypy、diff whitespaceを確認する
- [x] 全体pytestを再確認する（273 passed、4 feedparser DeprecationWarning、30.49秒）
- [ ] 広範囲なWiki agent分割は実モデル生成の確認と作業ツリー整理後に判断する

## Dreaming retryの根拠引用検証修正（2026-10-28）
- [x] 10件の実行結果とretry理由を確認する（7 succeeded、3 retry、全件 `evidence_quote must appear verbatim in the source`）
- [x] 原因を確認する（抽出検証は正規化一致、保存は原文の完全一致を要求）
- [x] 正規化後だけ一致する引用を抽出段階で拒否するテストを先に追加する（修正前に失敗することを確認）
- [x] 抽出検証を原文部分文字列の完全一致にそろえ、保存時例外を防ぐ
- [x] 関連pytest、ruff、mypyを実行してレビューする（26 passed、ruff・対象format・mypy通過）
- [x] retry jobをライブDBで自動再実行せず、状態を比較する（実験前後ともretry 3件・attempts=1。ライブDB: 901 source、891 pending、3 retry、7 succeeded、active Fact 63、proposed Relation 50、承認済み日本語訳19）
- [x] retry 3件を読み取り専用バックアップから作ったインメモリ複製で実モデル再処理する（3件すべてsucceeded、Fact accepted 8/7/1件、Relation提案5/19/2件。複製: active 69、rejected 19、proposed Relation 76、evidence 88、根拠欠落0）
- [x] lessonsへ境界契約の学びを記録する

## Wikiページ却下の引用正規化修正（2026-10-28）
- [x] 直近のreview_rejected 6回のログと決定的却下理由を確認する
- [x] 引用完全一致の変更後に全候補が`quote_not_found_in_cited_source`となったことを特定する
- [x] 空白・HTML表現の違いを原文の厳密な部分文字列へ対応づけるテストを先に追加し、修正前に失敗することを確認する
- [x] 抽出時に根拠引用を原文の該当範囲へcanonicalizeし、誤引用は引き続き拒否する
- [x] パイプライン・worker回帰、全pytest、ruff、format、mypyを実行する（254 passed、関連28 passed、DeprecationWarning 4件）
- [x] lessons・todoへ結果を反映する
- [ ] 次回の定期実行ログで`insufficient_evidence`と`quote_not_found_in_cited_source`の発生数を確認する

## Wiki手動実行のdatabase locked調査（2026-10-29）
- [x] 読み取り専用でDB状態・実行中プロセス・ログを確認する（Win32_Process詳細はアクセス拒否。1:08:54にDB更新、00:57の定期実行ログは1:24:32完了で、手動実行と重なった可能性が高い。過去ログにも`discord_streak`のDB lockあり）
- [x] 定期実行と同じ`--scheduled`排他ロックを付けて手動実行を1回行う
- [x] DBの実行記録とVault差分を確認する（`insufficient_evidence`。14候補すべて`source_url_not_allowed`で、引用正規化の検証には至らず。新規Wikiなし。MOC 25件とcluster-mapが更新。JSON出力はWindows cp932のUnicodeEncodeError、Git保存は`.git/index.lock`アクセス拒否で失敗）

## Wiki候補のURL許可判定を修正し再実行（2026-10-30）
- [x] `source_url_not_allowed`の検証条件と候補URLの受け渡し経路を読み取り専用で追跡する
- [x] LLMにsource_idを選ばせ、コードで正規URLへ対応付ける
- [x] 応答と対応するsystem/promptをローカルJSONLへ保存し、ログ出力テストを追加する
- [x] 関連31件、全257件、ruff、format、実装4ファイルのmypyを確認する（全テストの既存feedparser DeprecationWarning 4件）
- [x] UTF-8・定期実行共通の排他ロック・応答ログを有効にしてWiki生成を1回実行する
- [x] DB・実モデル応答ログを確認する（URL検査通過14候補。7種類のFact IDが各2回重複し、Reviewerが同一IDをaccepted/rejected両方に返したため、fail-closedで0件採用。`insufficient_evidence`）
- [x] Reviewer前にFact IDを決定的に重複除去し、重複を記録する回帰テストを追加する
- [x] 重複除去後の関連テスト・全テスト・ruff・format・mypyを確認する
- [x] UTF-8・排他ロック・応答ログ付きで生成をもう1回実行し、ページと結果を確認する（Fact重複は解消したがReviewer却下。新ログ`logs/llm-response-dedup-20261030.jsonl`）

## ライブDBのretry 3件を限定再処理（2026-10-28）
- [x] 現在のjob状態を確認する（retry 3件、running 0件、pendingあり）
- [x] retry以外をclaimしないstore/worker/CLI経路をテスト先行で追加する（pendingが残るstore/workerテスト、retry限定はbatch必須）
- [x] retry限定コマンドをREADMEへ記載する
- [x] retry限定CLIで3件をライブ処理し、pendingを処理しないことを確認する（3 processed、3 succeeded、error 0、attempts=2、pending 891件維持）
- [x] Fact根拠・Relation提案・job件数を確認する（live: 901 source、10 succeeded、891 pending、active Fact 67、rejected 19、proposed Relation 59、承認済み日本語訳28、evidence 86/86原文・offset一致、根拠欠落0）
- [x] 全pytest・変更範囲ruff/format/mypyを実行する（253 passed、feedparser DeprecationWarning 4件）

## Supermemory memory graphのMemoria Forge適用調査（2026-10-23）
- [x] Memoria Forgeの現行記憶モデル・代謝・検索・履歴管理を確認する
- [x] Supermemory graph engineの公式発表・仕様・API・公開実装を確認する
- [x] 直接導入と設計応用を分けて適合性・リスク・工数を評価する
- [x] 最小導入案と採否を出典付きで報告する
- [x] 調査結果をtodoとlessonsへ反映する

## ローカル原子的事実グラフ実験（2026-10-23）
- [x] 実データから検証可能なクラスタを1件選定する
- [x] 出典引用付きの事実抽出・関係判定・SQLite保存を実験実装する
- [x] 事実グラフ経由の実験ページを生成する
- [x] 現行ページとの品質・出典対応・実行時間を比較する
- [x] pytest・ruff・mypyと自己レビューを実施する（191 passed、既存feedparser DeprecationWarning 4件、ruff/mypy通過）
- [x] 結果と学びを記録する

## ローカル原子的事実グラフ第2実験（2026-10-23）
- [x] 数値・日付・固有表現の引用内存在を決定的に検査する
- [x] 別モデルで主張と引用の含意を検査する
- [x] 関係候補を事前制限し`same / updates / contradicts`だけ判定する
- [x] 前回結果との品質・辺数・速度を比較する
- [x] pytest・ruff・mypyと自己レビューを実施する（194 passed、既存feedparser DeprecationWarning 4件、ruff/mypy通過）
- [x] 結果と学びを記録する

## 証拠付き原子的事実パイプライン旧案（2026-10-23、未完了・新設計へ置換）
- [ ] 本番用の事実型・保存・決定的検証をテスト先行で実装する
- [ ] deep_researchから検証済み事実を抽出する
- [ ] create_pageのWriter入力を検証済み事実へ変更する
- [ ] 新規ページを読みやすい5セクション形式へ変更する
- [ ] 証拠不足をinsufficient_evidenceとして安全停止する
- [ ] 実データコピーで新旧形式を比較する
- [ ] 全pytest・ruff・mypy・pre-commitを通す
- [ ] todo・lessons・READMEを更新する
- [ ] 今回の変更だけをコミット・pushする

## ローカル記憶エンジン再設計と実装（2026-10-25）
- [x] SupermemoryのDreaming・記憶ライフサイクルとMemoria Forge現状を比較する
- [x] 7段階のローカル記憶エンジン計画を`docs/local_memory_engine_plan_2026-10-25.md`に記録する
- [x] Stage 1: ドメイン契約と空の独立記憶DBを設計・実装する（pytest 5 passed、ruff/mypy通過）
- [x] Stage 2 コア: 原資料取り込み・版保存・即時FTS検索・Dreaming待ちjob
- [ ] Stage 2 完了条件: RSS本文全文・Deep Research全文を新ストアへ接続（Deep ResearchとRSS本文フィールドはページ成否から独立して保存。RSS summaryのみのフィードで全文を得る経路は未実装）
- [x] Vault内の可視Markdownを相対URI・内容hashで取り込み、FTS即時検索とDream jobへ接続する。隠し領域・symlink・junctionは除外
- [x] live-vaultの可視Markdown 886件を専用DBへ初回取込し、2回目で重複0件・既存Markdown差分なしを確認する（DB合計891 source/891 job、Markdown 1669 chunks）
- [x] 初回取込で作られたDream job 891件の処理速度を改善する（既定で1回につき最大10件、スケジューラ既定60分間隔）
- [x] バッチworkerは1回につき最大10件を処理し、失敗jobをretry状態へ移して後続jobを続行する
- [x] `--dream-batch` CLIと独立スケジューラを接続し、完了/idle/一部失敗をログと終了コードに反映する
- [x] バッチ上限・失敗継続・未処理job保持をテストし、README・計画・lessonsを更新する
- [x] Stage 2 Vault Markdown入力: 隠し状態とリンク先外を除外し、本文を内容版管理・FTS/Dream queueへ登録する（33 passed、ruff/mypy通過）
- [x] Stage 3 パイプライン基礎: 既存のFact抽出・決定的検証・独立レビュー・日本語翻訳レビューを専用ストアへ接続
- [x] Stage 3: 新規ページ生成経路で根拠付きFact/承認済み日本語表示を専用DBへ保存。Wikiは既存の5見出し投影を使用
- [x] 新規の根拠付きページ生成で取得済みソース抜粋とレビュー済みFactを専用DBへ冪等保存する
- [x] 専用DBをVault内の隠しローカル状態として配置し、Git対象外にする
- [x] 保存障害が既存Wiki生成を壊さず、失敗がログで確認できることをテストする
- [ ] Stage 4: Entity解決と意味関係グラフ
- [x] Stage 4 基礎: 正規化完全一致のEntity解決、Factリンク、レビュー前のproposed relation
- [x] Stage 4 関係レビュー: 承認/却下をイベント履歴に記録し、曖昧な別名や非active Factを拒否
- [ ] Stage 4 残り: レビュー済み別名の登録UI/CLI（登録APIと監査は実装済み。relation evaluator・Dreaming候補生成はStage 6スライスで完了）
- [ ] Stage 5: 時間・更新履歴・忘却・完全削除
- [x] 承認済みFactの置換を旧版保持・有効時刻・updates辺・イベント付きで一トランザクション処理する
- [x] 通常Recallは現在有効なactive Factだけを返し、as_of指定は有効期間から履歴Factを再現する
- [x] forget操作をイベント履歴へ記録し、通常/時点Recallの双方から除外する
- [ ] Stage 5 残り: UIからの消去対象選択、期限切れ、旧.agent-state.sqlite3の歴史Fact監査（CLI選択・確認付き消去は実装済み）
- [x] Stage 5 完全消去API: v1→v2で削除認可付きappend-onlyイベント制約へ移行し、URI全版と派生Fact/Edge/Job/Eventを一括消去
- [x] Stage 6 Recall接続: 承認済みFactをFTS検索し、引用と出典を添えてWiki Writerの調査コンテキストへ注入
- [x] 忘却済み・未承認・出典停止済みFactがRecallへ混ざらないことを検証する
- [ ] Stage 6: Dreaming背景処理・再試行・Recall/Context injection
- [x] Stage 6: Dream jobのatomic claim/lease、期限切れlease再取得、上限付き指数バックオフretryを実装
- [x] `run_agent.py --dream-once`で1件だけ処理できる独立workerを提供する（通常Wiki実行と分離）
- [x] 処理済みFactと関連Factをモデル評価し、確信度・ID・根拠を検証してrelationを`proposed`で登録する
- [x] 成功・失敗・再起動・二重実行の冪等性をテストし、全体回帰を検証する（248 passed、ruff/mypy対象ファイル通過）
- [ ] Stage 7: 評価・運用化・新しい空DBへの切替
- [x] Stage 7 固定受け入れシナリオ: Fact根拠、Recall、Relation、更新/履歴、Forget、完全消去、Dream retryを文書化して実行する（30 passed）
- [ ] Stage 7 残り: 実モデル用gold setでFact含意・日本語翻訳・Relation precision/recall・Recall失敗率・Dream遅延を測る
- [ ] Stage 7 残り: 実Task Scheduler再起動/shadow run、入力ソース拡張、旧DB監査、切替・復旧手順
- [ ] 全体ruff/mypyの既存失敗（tests/test_atomic_facts.py、tests/test_agent.py）と全体format差分を別タスクで整理する
- [x] 現段階の全テスト（248件）・ruff・mypy・レビューを行う（248 passed、対象ファイルruff/mypy通過。既存feedparser由来warning 4件）
- [ ] 段階ごとのテスト・ruff・mypy・レビューを行い、切替前に品質ゲートを通す

## Dreamingの独立定期実行
- [x] Dream worker専用のPowerShell実行スクリプトを追加し、JSON結果と失敗をログへ記録する
- [x] Wiki Task Schedulerと独立したDreaming用スケジューラ登録手順を追加する
- [x] READMEに登録・状態確認・解除とretry動作を記載する
- [x] PowerShell構文/引数を確認し、関連Python回帰・ruff・mypyを実行する（248 passed、変更Pythonファイルのチェック通過）

## Stage 7 記憶エンジン受け入れ評価
- [x] 根拠付きFact・Recall・更新/履歴・Forget/消去・Dream retry/Relationの固定シナリオと合格条件を文書化する
- [x] 各シナリオに既存pytestを対応付けて実行し、結果を評価レポートへ記録する（30 passed）
- [x] LLM意味精度などモックで測定できない項目を未測定として切替前の残課題にする
- [x] todo・計画書・lessonsを更新し、変更範囲のruff/mypyと差分レビューを行う

## Discord Webhook通知（レポート生成時）
- [x] `tasks/alignment.md`を作成する
- [x] 通知条件・結論抜粋・マップ差分の失敗するテストを書く
- [x] `src/discord_notify.py`を実装する（URLは環境変数`DISCORD_WEBHOOK_URL`）
- [x] `run_agent.py`の実行後処理から呼び出し、前回マップ値を`.cluster-map-stats.json`へ保存する
- [x] `.gitignore`へ`.cluster-map-stats.json`を追加する
- [x] pytest（153件）・ruff・mypyを実行してコミットする
- [x] Webhook URLの読み込み元を環境変数から`config/discord_webhook.txt`（gitignore済み）へ変更する
- [x] `config/discord_webhook.txt`へ実際のWebhook URLを書き、実送信を確認する（手動スクリプトで送信成功）

## 作業→push→通知の一本化（push_failed常態化の修正）
- [x] 原因特定: 111.6MBの`live-vault/.agent-state.sqlite3.pre-stage3`が09-05のコミットに混入し、GH001で全pushが拒否されていた
- [x] 未push14件から該当ファイルを除去（filter-branch）。消えた実ファイルはgitオブジェクトから復元済み
- [x] `.gitignore`を`live-vault/.agent-state.sqlite3*`へ拡大
- [x] pushの失敗理由を保持する（`Git.last_push_error`）
- [x] 実行末尾で`push_pending`（MOC等の残り変更をコミット＋未pushをpush）を呼ぶ
- [x] 通知に`@everyone`、push成功時のみGitHubリンク、失敗時は理由を表示
- [x] pytest（161件）・ruff・mypy後にコミット
- [ ] `scripts/run_scheduled.ps1`を定期実行と同じ引数で実行し、自動経路でpush・通知を確認する
- [x] 調査: 2026-09-14 19:57の`database is locked` → 手動の送信テストスクリプトが同DBを約40秒読んでいたため（StateDBのtimeoutは既定5秒）

## ページ生成が通らない問題（09-01以降 review_rejected 212回 / success 4回）
- [x] 却下理由の集計: 必須セクション欠落562件（共通点133・差分124…、全7欠落が28回）、H1 79、捏造URL 70
- [x] 却下されたWriter出力と理由を`logs/rejected/`へ保存する（テスト先行、pytest 162件）
- [x] 定期実行タスクを1回起動し、保存された実出力を読む
- [x] 実出力に基づいて修正案を提示し、y/n確認を取る（Codexにも相談）
- [x] 本来の問題を特定: 08-19〜20の合格基準引き上げ（7161516等）以降ほぼ全却下。08-18以前のページ45枚も現基準で0枚合格
- [x] 方針決定: 形式はコードが組み立て、LLMは中身だけ（案2）＋基準見直し（案3）＋改善し続ける仕組み

## フェーズ1: 測る仕組み（本番と同じ処理でN件評価）
- [x] 書く→検証→Reviewerのループを`write_and_review`へ切り出し、run_onceと評価で共用する
- [x] `experiments/writer_eval.py`（状態DBのコピーで動かし、Vault/Git/本番DBを汚さない）
- [x] 現行Writerの基準値を測る → 2026-09-15 00:35 **0/5合格**（H1欠落2、必須セクション欠落5件分、順序違い1、捏造URL1。1件103〜196秒）
- [x] フェーズ2・3・5を同条件で評価 → 2/5合格（残りはセクション単位で英語化。原因はnum_ctx未指定の切り詰め）
- [x] num_ctx=16384を加えて再評価 → **5/5合格、切り詰め0件**（1件156〜270秒、GTX1070でGPU 83%）

## フェーズ2: 形式はコードが組み立てる
- [x] 各セクションの中身だけをLLMに書かせ、結論は最後、日本語タイトルは別呼び出し
- [x] H1・7見出し・順序・元記事一覧のURLはコードが組み立てる

## フェーズ3: 合格基準の見直し
- [x] 作り上げられたURLは本文から取り除き警告として記録（決定: B）
- [x] 本文の日本語判定、空セクション却下、700文字以上、定型文禁止、Reviewer、情報量非減少は維持

## フェーズ4: 評価してから本番へ
- [x] 評価5件中3件以上合格を確認してから本番投入（2026-09-15 02:46 master へマージ 32aa42e）
- [x] 定期実行（02:57〜03:10）でページ生成・push・Discord通知を確認 → result=success、git_final=pushed、discord=sent、切り詰め0件（約4週間ぶりの自動生成）

## 切り口のあるレポート（feature/theme-selection、実装はCodex）
- [x] 実例の調査: ケーキ2等分ページはクラスタ#27（81件）で、材料5件中ケーキ関連1件。近傍には「バビロニアの台形分割」(0.840)など本当に近い記事があった
- [ ] 材料を代表記事＋埋め込みで近い上位4件から選ぶ（元のRSS記事も出典に入れる）
- [ ] 書く前に「切り口」（日本語タイトル・共通の問い・支える記事・外す記事）を決める
- [ ] 切り口が立たない（支える記事が2件未満）なら代表記事1本を深く掘り下げる（ユーザー決定: A）
- [ ] 評価に mode・切り口・使った記事数を記録し、合格ページの中身を読んで組み合わせができているか確認してから本番へ

## 監視の抜け（2026-09-15 23:33 発見）
- [ ] 定期実行ログが半数近く欠落: 09-15はページのコミット19件に対し `logs/scheduled-*.log` は11件（03:57・04:57・10:57〜13:57・15:57・16:57・18:57・19:57・21:57の実行はページがあるのにログなし）。原因未調査（ログは実行終盤に作成される）
- [ ] 別アプリがOllamaで`qwen3.5:4b`を`/api/generate`経由で同時に使っており、GPU(8GB)を取り合って定期実行が遅くなる（22:57の実行は35分以上）

## 次の改善候補（評価の合格ページを読んで見つけたもの）
- [ ] 専門用語の誤訳（NER→「名詞句認識」、AI agents→「AIアーキテクチャ」）
- [ ] 「不確実な点」に推測表現（〜と推測される）が残る
- [ ] 元記事一覧のタイトルの空白欠落（検索結果側のタイトル）
- [ ] 使われなくなった`templates/prompt/info_theme_report_*.txt`と`build_theme_report_prompt`の削除確認

## フェーズ5: 改善し続ける仕組み
- [x] 却下が6回続いたらDiscordへ警告（直近の却下理由の要約付き）
- [x] 失敗したクラスタを24時間後回しにする
- [x] 却下連続数・理由集計・6回ごとのDiscord通知を実装する
- [x] 失敗ページの記録と24時間クールダウンを実装する
- [x] pytest・ruff・mypyを通し、feature/sectioned-writerへコミットする

## Ollamaコンテキスト切り詰めの解消と評価記録
- [x] `Config.num_ctx`を追加し、Ollamaの生成・チャット両payloadへ渡す
- [x] 設定読み込み・検証・HTTP payloadの回帰テストを追加する
- [x] Writer評価で実行後の切り詰め件数を集計し、レポートへ保存する
- [x] Writer評価で合格ページ本文を`accepted/`へ保存する
- [x] `count_truncations`の回帰テストを追加する
- [x] ruff・mypyを実行する

## 保留（記録のみ）
- [ ] 巨大クラスタ問題（最大414点、50点以上43個）でタイトルと材料が噛み合わない

## クラスタリング・構成の可視化
- [x] 既存のクラスタリング処理・永続データ・構成情報を調査する
- [x] 分布・ばらつき・クラスタ間関係を確認できる最小可視化を実装する
- [x] 実データで表示内容を検証する（673クラスタ・7,648要素・近接関係468本）
- [x] pytest（134件）・ruff・mypyを実行する（既存feedparser由来のDeprecationWarning 4件）
- [x] 実装上の学びを`tasks/lessons.md`へ記録する

## MOC・DB・Markdownの3層構造
- [x] 既存Markdown・Wikiリンク・クラスタ接続状況を分析する
- [x] MOCとMarkdownの所属関係をDBへ保存する
- [x] 自動生成MOCを専用領域へ出力する
- [x] 可視化へMOC別表示とクラスタ→Markdown→MOCの関係を追加する
- [x] エージェント実行後にMOCと可視化を自動更新する
- [x] 実データ（8 MOC・17所属・61未所属）、pytest（138件）、ruff、mypyで検証する
- [x] 実装上の学びを`tasks/lessons.md`へ記録する

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
- [x] AIBackgroundWorkerの多段調査（本文取得→中間統合→最終Writer）を通常ページ生成へ移植する
- [x] 中間調査結果に主要発見・共通点・差分・矛盾・時系列・確信度を保持する
- [x] 最終文書の詳細を結論・確認事実・情報源差分・時系列・制約へ構造化する
- [x] RSS本文と公開日時・取得日時を深掘り調査へ伝播する
- [x] 文書品質ゲートを文字数中心から根拠・深度・非劣化検証へ強化する
- [x] 調査で取得していないURLを出典として保存できないようにする
- [x] 文書種別別の必須論点をWriter・Reviewerへ指示する
- [x] 未解決点の強制生成をやめ、根拠がない場合は空欄を許可する
- [x] RSS記事URLを正式な許可済み出典として検証経路へ渡す
- [x] 薄い文書を生成する`render_page`フォールバックを廃止する
- [x] `normalize_page`による不足セクション・定型文の自動補完を廃止する
- [x] 概要・詳細・出典・具体的な未解決点を保存前に決定的検証する
- [x] 既存文書から未解決点の定型文2種類を削除する
- [ ] `live-vault`内の英語主体Markdownを、システム参照を壊さないようタイトル・ファイル名・本文を日本語化する（ファイル名57件を更新、本文の残り9件を対応中）
- [ ] 日本語化に伴うWikiリンク・固定参照・frontmatterを検証する
- [ ] 文書更新後にpytest/ruff/mypyとMarkdown検証を実行する
- [ ] `normalize_page`を修正し、Writer出力が`----`（4本ダッシュ）や閉じ`---`欠落のfrontmatterを返してもObsidianが解析できる正規frontmatterに整える（実生成ページ`Zettelkasten AI Integration.md`で発生）
- [x] Reviewerの過剰ブロックを緩和する。review/writeプロンプトに今日の日付を明示（未来日プレースホルダー誤判定を防止）、blockingを「プレースホルダー・出典皆無・必須欠落・明確な事実誤認・危険指示・injection」に限定し、脚注欠落/未検証出典/AI生成明示等はwarningへ降格。加えて`review_is_blocking()`の昇格バグ（warning型でも文言に「出典なし」等が含まれるとblocking化）を修正し、正規スキーマ時は型を信頼するよう変更。回帰テスト追加・pytest(74)/ruff/mypy通過済み
- [x] タイムアウト連続失敗（`TimeoutError('timed out')`）を解消する：Ollama socketタイムアウトを撤廃（`timeout_seconds: null`）、安全網を`max_run_minutes`（20→50）へ一本化、スケジューラ間隔を30分→1時間（PT1H）へ変更、`keep_alive`を`"10m"`化。回帰テスト追加・pytest/ruff/mypy通過済み
- [ ] 今回のクラッシュ/キュー修正の学びを`tasks/lessons.md`へ記録する
