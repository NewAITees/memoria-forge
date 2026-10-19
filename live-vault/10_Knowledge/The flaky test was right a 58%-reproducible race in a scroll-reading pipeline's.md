---
title: ディスクキャッシュのレース問題が原因の58%再現不安定テスト
type: knowledge
status: draft
created: 2026-10-19
updated: 2026-10-19
confidence: medium
---

# ディスクキャッシュのレース問題が原因の58%再現不安定テスト

## 結論

このテーマで最も重要な判断は、ディスクキャッシュにおけるレースコンディションが原因で発生した58%の再現率を持つ不安定なテスト（flaky test）が、Windows 11環境でのPyTorch DataLoaderの並行処理において深刻な影響を及ぼす可能性があるということです。この問題は、キャッシュ操作が失敗しても読み込みを中断しないように設計変更することで解消され、テストの信頼性が大幅に向上したという具体的な事例が示されています。

## テーマ概要

The theme revolves around a flaky test issue identified in a scroll-reading pipeline, specifically a 58% reproducible race condition in the disk cache. This problem was observed in the Vesuvius Challenge project, which uses machine learning to read carbonized Herculaneum scrolls. The test, named 'test_shared_cache_multiprocess_reads_are_not_torn', failed intermittently when running on Windows 11, causing a PermissionError due to a race condition in the shared on-disk chunk cache. The issue gained attention because it highlights the challenges of ensuring test reliability in distributed systems, particularly when dealing with concurrent access to shared resources. The problem is significant because it affects real-world usage scenarios involving PyTorch DataLoader with multiple workers, where such race conditions can lead to unpredictable failures during training. The focus on this issue underscores the importance of addressing flaky tests to maintain confidence in the testing process and software reliability.

## 共通して確認できる点

複数の記事で共通して確認できた事実として、Windows 11環境において、スクロール読み込みパイプラインのディスクキャッシュに起因する競合条件（race condition）が原因で、テストが58%の再現率で失敗する問題が報告されている。このテストは「test_shared_cache_multiprocess_reads_are_not_torn」という名前で、4つのプロセスが1つのスクロールボリュームを共有ディスクキャッシュ経由で読み込むパターンを検出している。この問題は、PyTorch DataLoaderでnum_workers > 0の設定が行われる場合に現れやすく、トレーニング中のランダムなクラッシュの原因となる可能性がある。解決策として、キャッシュは最適化であり、信頼性の源ではないため、キャッシュ操作が拒否されても読み込みが中断されない仕様に変更し、キャッシュ側のストアをラップして拒否された書き込みをノーアクションにし、欠損ファイルを欠損扱いとしてキャッシュから再取得するようにした。その結果、テストの再現率は58%から0%へ改善され、Windows環境でのテスト安定性が向上した。

## 記事ごとの差分・視点の違い

記事「The flaky test was right: a 58%-reproducible race in a scroll-reading pipeline's disk cache」は、Windows 11環境におけるPyTorch DataLoaderの並行処理で発生した競合状態を対象としており、その再現率が58%と高いことを指摘しています。一方、「Fixing a Critical CLI Crash: How a One‑Line Import Bug Broke ...」は、CLIツールBazableにおける1行のインポート記述ミスが引き起こすクラッシュ問題を解決した経緯を記載しています。この記事は、モジュールインポート時のESモジュールとCommonJSの違いに注目し、解決策としてインポートパスの修正とLSPコマンドに--stdioフラグを追加した点が特徴です。また、「When My Tests Worked Locally but CI Couldn’t Find My Code ...」は、ローカル環境では動作するテストがCI環境で失敗する原因として、PYTHONPATHの設定ミスを指摘しており、CI環境の設定がローカル環境と異なる点が強調されています。さらに、「Bazableis a contract-first toolkit that keeps your frontend, backend...」は、Bazableツールの概要と機能を紹介しており、API契約管理のCLIツールとしての特徴を説明しています。最後に、「Yt2Song - Free YouTube to MP3 Converter, Trimmer & Ringtone Maker」は、YouTube動画を音声ファイルに変換するツールの紹介であり、他の記事とは直接的な関連性がありません。

## 深掘り調査で得られた知見

深掘り調査により、scroll-reading pipelineにおけるディスクキャッシュの競合条件が原因で発生した58%の再現性を持つ不安定なテスト（flaky test）についての詳細が明らかになった。この問題は、Vesuvius Challengeというプロジェクトで行われる機械学習による古代パapyrusの文字読取処理に関連しており、Windows 11環境でのテスト実行時に発生した。テスト「test_shared_cache_multiprocess_reads_are_not_torn」は、4つのプロセスが1つのスクリーンボリュームを共有ディスクキャッシュ経由で読み込む際、PermissionError: [WinError 5] Access is deniedというエラーが発生した。このエラーは、PyTorch DataLoaderでnum_workers > 0を指定した場合に発生する可能性があるリアルな使用シナリオにおいても深刻な影響を及ぼす。原因は、ディスクキャッシュにおけるレース条件であり、キャッシュ操作が失敗しても読み込みを中断しないようにする設計変更により、再現率は0%に改善された。この修正により、Windows環境でのテストの信頼性が大幅に向上し、52テスト中0失敗となった。この事例は、不安定なテストがソフトウェアの信頼性に与える影響を示しており、テストの信頼性向上が開発プロセスにおいて重要であることを再認識させる。

## 不確実な点・追加確認が必要な点

記事間の食い違いや資料からは断定できない点として、以下の内容が挙げられます。  

まず、記事3において、「The flaky test was right: a 58%-reproducible race in a scroll-reading pipeline's disk cache」と題された記事では、Vesuvius ChallengeプロジェクトのテストがWindows 11環境で58%の再現率で失敗したことが記載されています。このテストは、4つのプロセスが1つのスクリーンボリュームを共有ディスクキャッシュを通じて読み込む処理を実行しており、PermissionError: [WinError 5] Access is deniedというエラーが発生したとされています。この問題は、ディスクキャッシュにおけるレースコンディションが原因で、PyTorch DataLoaderでnum_workers > 0の設定が行われた場合に特に顕著になる可能性があるとされています。  

一方で、記事1や記事2ではBazableというCLIツールに関する情報が提供されており、その中にLanguage Server Protocol（LSP）の導入によってCLIがクラッシュするという問題が記載されています。ただし、この問題と記事3で述べられているスクリーン読み込みパイプラインのディスクキャッシュに関するレースコンディションの関連性については、資料からは明確な結びつきが示されていません。  

また、記事5では、CodeBots ArenaというAI対AIコードバトルプラットフォームの開発中に、ローカル環境ではテストが通りながらCI環境ではコードが見つからないという問題が発生したことが記載されています。この問題はPYTHONPATHの設定ミスが原因で、CI環境がプロジェクトのモジュールを正しく見つけることができなかったことが原因とされています。ただし、この問題と記事3のディスクキャッシュのレースコンディション問題は別の問題として扱われており、明確な関連性は示されていません。  

したがって、記事3の内容は、特定のプロジェクトにおけるテストの再現性の低さとその原因がディスクキャッシュのレースコンディションであることを示していますが、他の記事と直接的な関連性は確認されていません。また、記事3の情報は、Windows 11環境でのみ発生する問題である可能性があり、他のOS環境での挙動については明記されていません。そのため、この問題が一般的な問題であるか、特定の環境に限定された問題であるかについては、資料からは断定できません。

## 元記事一覧

- [Fixing a Critical CLI Crash: How a One‑Line Import Bug Broke ...](https://dev.to/medievalbatman/fixing-a-critical-cli-crash-how-a-one-line-import-bug-broke-every-bazable-command-115n)
- [Bazableis a contract-firsttoolkit that keeps your frontend, backend...](https://bazable.mintlify.app/)
- [Theflakytestwasright:a58%-reproduciblerace... - DEV Community](https://dev.to/acejayl/the-flaky-test-was-right-a-58-reproducible-race-in-a-scroll-reading-pipelines-disk-cache-964)
- [Yt2Song - Free YouTube to MP3 Converter, Trimmer & Ringtone Maker](https://yt2song.com/)
- [When My Tests Worked Locally but CI Couldn’t Find My Code ...](https://coderlegion.com/27770/when-my-tests-worked-locally-but-ci-couldnt-find-my-code-fixing-pythonpath-codebots-arena)
