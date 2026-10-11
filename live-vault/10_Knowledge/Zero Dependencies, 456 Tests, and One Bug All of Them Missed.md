---
title: ゼロ依存性の罠――darkroomのQRコードトラブル
type: knowledge
status: draft
created: 2026-10-11
updated: 2026-10-11
confidence: medium
---

# ゼロ依存性の罠――darkroomのQRコードトラブル

## 結論

Rustでゼロ依存性を実現したプロジェクト「darkroom」は、QRコードエンコード機能のテストがすべてパスしていたにもかかわらず、実際にはスマートフォンのカメラでスキャンできないという問題を抱えていたが、ISO/IEC 18004規格への準拠を確認し修正することで、最終的に動作を確保した。この事例は、テストの網羅性と実世界での動作の乖離を示しており、ゼロ依存性の実現には技術的な厳密さが求められることを明らかにしている。

## テーマ概要

Rust言語を用いてゼロ依存性を実現したプロジェクト「darkroom」が注目されている。このプロジェクトは、フォルダ内の写真をWi-Fiでスマートフォンに表示する機能を持つツールで、JPEGデコーダー、PNGエンコーダー、DEFLATE圧縮、EXIF解析、QRコードジェネレーター、HTTPサーバーなど、すべての機能をRust標準ライブラリではなくプロジェクト内に実装している。456のテストケースを備えているにもかかわらず、QRコードエンコード機能のテストでは、エンコーダーがISO/IEC 18004規格に準拠していないことが判明し、修正後、実際のスキャンで動作するようになった。このプロジェクトは、ゼロ依存性と高品質なテストケースを実現したことで、Rustコミュニティ内で話題となり、今注目されている。

## 共通して確認できる点

複数の記事で共通して確認できた事実として、Zero Dependencies、456 Tests、そしてOne Bug All of Them Missedというテーマに関連するプロジェクトが存在することが明らかになっています。このプロジェクトは、Rust標準ライブラリに依存せず、すべての機能をプロジェクト内に実装したツールであり、QRコードエンコード機能のテストではすべてのテストケースが通過していましたが、実際にはスマートフォンのカメラでスキャンできないという問題がありました。この問題は、QRコードエンコード機能がISO/IEC 18004規格に準拠していないことが原因であり、修正後、実際のスキャンで動作するようになりました。また、このプロジェクトはMITライセンスで配布されており、ドキュメントや設計文書が公開されています。

## 記事ごとの差分・視点の違い

記事「AllPythonRevolver Skins -Rust- YouTube」は、Pythonのスキン製品をRustで作成したデモ動画を紹介しており、主に製品の視覚的な表現や価格帯を強調しています。一方、「Top 30PythonLibrariesToKnow in 2026」は、2026年のPythonライブラリのトレンドとその用途を解説し、学習者向けの情報提供が目的です。また、「ZeroDependencies,456Tests,andOneBugAllofThemMissed」は、Rustでゼロ依存性を実現したプロジェクトの開発過程と、テストが通りながらも実際には動作しなかったQRコードエンコードの問題を詳細に検証しています。この記事は、技術的な挑戦とテストの限界について議論しています。  

「WeShippedanOptimizationOurOwnBenchmarkSaidNotTo」は、並列処理によるパフォーマンス向上を実現したlogqというツールの開発経緯を紹介しており、自社のベンチマーク結果に基づいた最適化を実施した点が特徴です。一方、「IbenchmarkedmylanguageagainstRustandZig,anddeletedmy...」は、自ら開発した言語「machin」をRustとZigと比較し、ベンチマーク結果の再評価を通じて誤った性能評価を修正した経緯を語っています。これらは、それぞれ異なる視点から、技術的な実装とベンチマークの信頼性について論じています。

## 深掘り調査で得られた知見

深掘り調査により、Zero Dependencies かつ 456 テストケースを備えた Rust プロジェクト「darkroom」の開発過程が明らかになった。このプロジェクトでは、JPEG デコーダー、PNG エンコーダー、DEFLATE 圧縮、EXIF 解析、QR コードジェネレーター、HTTP サーバーなど、すべての機能が Rust 標準ライブラリではなく、プロジェクト内に実装されている。QR コードエンコード機能では、テストケースがすべてパスしているにもかかわらず、実際にはスマートフォンのカメラでスキャンできないという問題が発生した。その原因は、エンコーダーが ISO/IEC 18004 規格に準拠していないことが判明し、修正後、実際のスキャンで動作するようになった。このプロジェクトは MIT ライセンスで配布されており、ドキュメントや設計文書が公開されている。また、同様のゼロ依存性を追求したプロジェクトとして、logq も注目される。logq は JSONL/logfmt/plain-text ファイルのフィルタリング、グループ化、カウント、パーセンタイル、タイムウィンドウなどの機能を持つコマンドラインベースのログクエリツールで、ゼロサードパーティ依存関係の静的バイナリで構築されている。8 個のゴルーチンで並列処理を実行するフラグを追加し、76.3MB の実際のファイルに対して 7.558 秒で完了させた。一方、1 個のワーカーで同じクエリを実行した場合、6.535 秒で完了した。この結果、8 個のワーカーを使用した場合、1 個のワーカーに比べて 16% 遅くなった。また、machin という Go 風の型推論言語の開発者も、Rust と Zig と比較して性能を評価したが、結果は誤解を招くものだった。ベンチマークの実行方法が原因で、初期の結果は誤っており、修正後は性能差が最小限に抑えられた。これらの事例は、ゼロ依存性を追求する開発が技術的にどれだけ複雑であるかを示している。

## 不確実な点・追加確認が必要な点

記事間の食い違いや、資料からは断定できない点を具体的に書く。  
まず、記事3「ZeroDependencies, 456Tests, and OneBugAll of Them Missed」では、QRコードエンコード機能のテストがすべてパスしているにもかかわらず、実際にはスマートフォンのカメラでスキャンできないという問題があったことが明記されている。この問題は、QRコードエンコード機能がISO/IEC 18004規格に準拠していないことが原因であり、修正後、実際のスキャンで動作するようになった。ただし、この修正の詳細や、どのバージョンから修正されたかは記載されていない。  

一方、記事4「WeShippedanOptimizationOurOwnBenchmarkSaidNotTo」では、logqというツールが8つのゴルーチンで並列処理を実行するフラグを追加し、76.3MBのファイルを7.558秒で処理したことが記載されている。ただし、この処理時間はどのバージョンから導入されたのか、また、CI（継続的インテグレーション）の導入とその影響についての詳細は明記されていない。  

また、記事5「IbenchmarkedmylanguageagainstRustandZig,anddeletedmy...」では、machinという言語がRustやZigと比較して特定のベンチマークで20-25%のパフォーマンス優位性を示したとされていたが、後にこの結果が誤っていたことが判明した。ただし、どのベンチマークでどの程度の誤差があったのか、具体的な修正内容や、どのバージョンで結果が再評価されたかは記載されていない。  

これらの記事では、それぞれのツールや言語の設計・実装に関する詳細な情報が提供されているが、特定のバージョンや修正履歴、ベンチマークの詳細な評価方法については明確な情報が不足している。そのため、これらの内容を断定的に記述することはできない。

## 元記事一覧

- [AllPythonRevolver Skins -Rust- YouTube](https://www.youtube.com/watch?v=V01Lx81TCX0)
- [Top 30PythonLibrariesToKnow in 2026](https://www.mygreatlearning.com/blog/open-source-python-libraries/)
- [ZeroDependencies,456Tests,andOneBugAllofThemMissed](https://dev.to/abhishek_jha_4287a6f8711f/zero-dependencies-456-tests-and-one-bug-all-of-them-missed-13jn)
- [WeShippedanOptimizationOurOwnBenchmarkSaidNotTo](https://dev.to/conqueror_queen/we-shipped-an-optimization-our-own-benchmark-said-not-to-3883)
- [IbenchmarkedmylanguageagainstRustandZig,anddeletedmy...](https://dev.to/javimosch/i-benchmarked-my-language-against-rust-and-zig-and-deleted-my-best-number-a9h)
