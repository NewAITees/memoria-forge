---
title: Polymarket botにプライベートキーを渡す前のチェックリスト
type: knowledge
status: draft
created: 2026-10-02
updated: 2026-10-02
confidence: medium
---

# Polymarket botにプライベートキーを渡す前のチェックリスト

## 結論

2026年の調査結果から、Polymarket botにプライベートキーを提供する際には、そのbotがどのような用途でキーを使用するかを明確に理解し、信頼できるコードの動作を確認することが不可欠である。特に、JavaScript/TypeScriptプロジェクトでは類似パッケージやダウンロード数の少ないライブラリに注意し、RustプロジェクトではCargo.lockファイルの確認や変数名のチェックを行うことで、セキュリティリスクを最小限に抑えることができる。

## テーマ概要

2026年現在、Polymarketのコピー取引ボットは、GitHubやnpmなどのパッケージリポジトリにおいて、悪意のあるアカウントによって偽装されたマルウェアとして広く利用されるようになっています。特に、悪意のあるボットは、ユーザーのプライベートキーを盗み取るための隠れた依存関係を含む形で配布され、セキュリティ上のリスクを高めています。このような背景から、「Before you give a Polymarket bot your private key: a 15-minute checklist」という記事は、ボットの信頼性を評価し、プライベートキーを提供する際のセキュリティチェックリストを提供しています。このテーマは、ユーザーが自らの資産を守るために、ボットの動作を慎重に検証する必要性を強調しており、特に暗号通貨取引において重要な課題となっています。

## 共通して確認できる点

2026年8月20日、Rustパッケージリポジトリcrates.io上に、arrayrefという人気の小さなcrateのバージョン0.3.10が不正に公開されました。このバージョンは、本物のproc-macro2と名前をそっくりにしたtyposquat crateであるproc-macro1への依存関係を追加し、そのbuild.rsファイルがコンパイル中にリモートのバイナリをダウンロード・実行するマルウェアを実行しました。このマルウェアは、UTC時刻07:15に公開され、86分後に86分後の08:41に削除されました。この攻撃は、arrayrefの広範な使用により、2億4500万回以上のダウンロードを経て、多くのプロジェクトに影響を与えました。また、攻撃は北朝鮮の国家支援活動グループUNC1069と関連付けられ、マルウェアのペイロードはbase64のフラグメントとして保存され、コンパイル時に再構成されてリモートサーバーに接続してバイナリをダウンロード・実行しました。このインシデントにより、Rustプロジェクトにおけるビルドスクリプトのリスクが再認識され、Rustセキュリティレスポンスチームと独立研究者が関与しました。

## 記事ごとの差分・視点の違い

記事「Before you give a Polymarket bot your private key: a 15-minute checklist」は、Polymarket botの利用において私鍵を渡す際のセキュリティチェックリストを提供し、botの挙動を理解する重要性を強調している。一方、「APolymarketBotMade $438,000 In 30 Days. - YouTube」は、botの運用によって得られた利益を示す動画であり、botの実用性と収益性に焦点を当てている。また、「Rust malware in arrayref: how a build.rs ran a payload at compile time」は、Rustプロジェクトにおけるbuild.rsスクリプトの悪用によるマルウェア感染の事例を解説し、Rustのセキュリティリスクを分析している。さらに、「Malicious Rust Crate arrayref Runs a Build-Time Payload」は、arrayrefというRustパッケージの不正利用を詳細に説明し、build-time payloadの仕組みと影響範囲を明示している。最後に、「TanStack npm supply-chain attack: how a Dependabot bump spread a worm」は、npmパッケージのサプライチェーン攻撃の手法とその拡散のスピードを示し、JavaScript/TypeScriptプロジェクトにおけるセキュリティ脅威を論じている。各記事はそれぞれ異なる視点から、技術的なリスクやセキュリティ対策、そして実際の攻撃事例を提示している。

## 深掘り調査で得られた知見

深掘り調査により、Polymarket botの利用に関連するリスクと対策について新たな知見が得られた。2026年には、GitHub上で「Polymarket copy-trading bot」として偽装されたマルウェアが複数投稿され、ユーザーのプライベートキーを盗む攻撃が行われた。特に、npmの隠し依存関係を悪用した攻撃が多発し、.envファイルからキーを読み取り、SSHバックドアを開くという手口が確認されている。また、自前のトレーディングbotを運用する際には、プライベートキーが必要となるため、ユーザーが「決してbotにキーを渡さない」というアドバイスは現実的ではなく、代わりにbotがキーをどのように利用するかを明確に理解することが求められる。  

一方、Rustプロジェクトにおいては、`arrayref`という人気のcrateが悪用されたケースが発覚した。2026年8月20日に、`arrayref`のバージョン0.3.10に不正な依存関係`proc-macro1`が追加され、そのビルドスクリプトがコンパイル時にリモートからバイナリをダウンロードして実行するマルウェアが含まれていた。この攻撃は、Rustの`cargo build`が依存関係のコードを実行する仕組みを悪用したもので、開発者やCI環境で実行されると、攻撃者が機器にアクセスできるようになった。  

これらの事例から、開発者はコードの依存関係を厳密にチェックし、非公式なパッケージや不審な名前のライブラリに注意する必要がある。特に、JavaScript/TypeScriptプロジェクトでは、名前が類似しているパッケージやダウンロード数が極めて少ないパッケージに警戒を向け、Rustプロジェクトでは`Cargo.lock`ファイルの確認や、変数名が`signing`に関連するかをチェックするなどの対策が有効である。また、botの動作をテストする際には、仮想のキーを使用して実行し、ログに現れる情報が適切にマスクされているかを確認することが重要である。

## 不確実な点・追加確認が必要な点

記事間の食い違いや資料からは断定できない点を具体的に書くと、以下の通りです。  

まず、記事1では、2026年にPolymarketのコピー取引ボットがGitHub上での主要な罠として利用されていると述べられており、そのようなボットが暗号資産のプライベートキーを盗む手段としてnpmの隠し依存関係を活用していることが示されています。しかし、記事2はYouTube動画であり、具体的な情報は提供されていません。動画の公開日時や取得日時が不明であるため、情報の新旧や信頼性を評価することが困難です。  

記事3と記事4はRust関連のセキュリティインシデントについて述べています。記事3では、arrayrefというRustパッケージが悪意のある依存関係を含むことで、ビルド時にマルウェアが実行されることが報告されています。記事4では、このインシデントが2026年8月20日に発生し、悪意のあるcrateが削除されたことが記載されています。しかし、記事3の公開日時や取得日時が不明なため、情報の正確性や時点の正確性を確認することができません。  

記事5はnpmのサプライチェーン攻撃について述べており、依存関係のバージョンアップによってマルウェアが広がった例が示されています。ただし、記事5の公開日時や取得日時が不明なため、情報の信頼性や時系列的な位置づけを明確にするのが難しいです。  

また、記事1では、Polymarketボットのセキュリティチェックリストが提示されていますが、その内容が他の記事と整合性を保っているかは不明です。例えば、記事1では、JavaScript/TypeScriptプロジェクトでは特定のパッケージ名やダウンロード数に注意すべきと述べていますが、記事3や記事4ではRustプロジェクトに焦点を当てた情報が提供されているため、技術スタックごとのセキュリティ対策の違いが明確化されています。  

これらの記事は、それぞれ異なる技術分野（Polymarketボット、Rustセキュリティ、npmサプライチェーン攻撃）に焦点を当てており、それぞれの技術スタックに対するセキュリティリスクを示しています。しかし、時間的な整合性や情報の信頼性については、公開日時や取得日時が不明であるため、断定的な結論を出すことはできません。

## 元記事一覧

- [BeforeyougiveaPolymarketbotyourprivatekey:a15-minute...](https://dev.to/andreyschurko/before-you-give-a-polymarket-bot-your-private-key-a-15-minute-checklist-1774)
- [APolymarketBotMade $438,000 In 30 Days. - YouTube](https://www.youtube.com/watch?v=BiqG3it0gY0)
- [Rustmalwareinarrayref:howabuild.rsranapayloadatcompile...](https://dev.to/axrisi/rust-malware-in-arrayref-how-a-buildrs-ran-a-payload-at-compile-time-e7f)
- [MaliciousRustCratearrayrefRunsaBuild-TimePayload](https://safedep.io/arrayref-proc-macro1-rust-build-time-malware/)
- [TanStacknpmsupply-chainattack: how aDependabotbump...](https://dev.to/axrisi/tanstack-npm-supply-chain-attack-how-a-dependabot-bump-spread-a-worm-1h4l)
