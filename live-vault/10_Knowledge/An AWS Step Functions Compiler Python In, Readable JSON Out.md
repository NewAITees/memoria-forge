---
title: AWS Step FunctionsでPythonをJSONにコンパイルする技術
type: knowledge
status: draft
created: 2026-10-04
updated: 2026-10-04
confidence: medium
---

# AWS Step FunctionsでPythonをJSONにコンパイルする技術

## 結論

AWS Step Functions において、Python コードを入力として受け取り、人間が読みやすい JSON 出力を作成するコンパイラツールとして、`pysfn.tools.compile` が具体的に実装されており、Python の制御フローを JSON に変換する機能を提供しています。このツールは、Python コードを AWS Step Functions で利用可能な JSON 定義に変換し、手動での JSON 編集を省略するための技術的アプローチとして位置づけられています。また、`sfnx` や `pystepfunction` などのツールも同様の目的で検討されており、Python を用いたワークフロー設計の効率化を図るための重要な手段として注目されています。

## テーマ概要

AWS Step Functions における Python コードを入力として受け取り、人間が読みやすい JSON 出力を作成するコンパイラの実装が注目されている。このテーマは、AWS Lambda と Step Functions を使用したサーレスレスなアーキテクチャにおいて、Python の柔軟性と JSON のシンプルな構造を組み合わせることで、ワークフローの設計・管理を効率化する目的を持つ。特に、pystepfunction や sfnx などのツールが、Python コードを JSON 定義に変換し、Step Functions で利用できるようにするという点で、開発者にとっての作業負荷を軽減する可能性がある。また、JSON の出力が読みやすく、ワークフローの可視化や修正が容易になるため、今後の AWS サービスの利用において重要な役割を果たすと期待されている。

## 共通して確認できる点

AWS Step Functions において、Python コードを JSON 定義に変換するコンパイラツールが存在することが確認されました。具体的には、`pysfn.tools.compile` というツールが Python コードを読み込み、指定されたエントリポイント関数の制御フローを JSON に変換します。この JSON は AWS Step Functions のステートマシンとして使用可能です。また、`pysfn.tools.gen_lambda` というツールは、Python コードを Lambda 関数としてパッケージ化し、Step Functions から呼び出すことができます。これらのツールは、Python コードを直接 Step Functions に組み込むことで、JSON の手動編集を省略できるように設計されています。

また、AWS SDK for Python (Boto3) を使用した Step Functions の操作例も確認され、ステートマシンの作成や実行、ステータス取得などの操作が示されています。さらに、CDK（Cloud Development Kit）を用いた Step Functions の例も存在し、Python と CDK の統合が可能であることが示されています。これらの情報は、Python を使用した Step Functions の実装方法を理解する上で重要な参考になります。

## 記事ごとの差分・視点の違い

記事1はAWS SDK for Python（Boto3）を用いたStep Functionsの基本操作を示すコード例を提供しており、Pythonでステートマシンを操作する方法を説明しています。この記事はAWSの公式ドキュメントであり、操作の手順やAPIの詳細を含むため、実装の基礎となる情報を得られます。一方で、PythonコードをJSONにコンパイルする機能は記述されておらず、Step Functionsの使用に際してJSONの直接的な編集が必要であることを示しています。

記事2はPythonコードをAWS Step Functionsのステートマシンとしてコンパイルするツール「pysfn.tools.compile」や、Lambda関数としてパッケージ化するツール「pysfn.tools.gen_lambda」について説明しています。この記事はGitHub上のプロジェクトであり、PythonコードをJSONに変換し、Step Functionsに組み込むための実装例を提供しています。また、このツールはGPLライセンスで公開されており、開発者自身が拡張や改善を行うことが可能です。この記事は、Pythonを直接Step Functionsに組み込むための技術的アプローチを示しており、コードの実行とステートマシンの動作の関係性についても触れており、実際の実装に近い情報を提供しています。

記事3と記事4はPingFederateに関する情報であり、Step Functionsとの直接的な関連性は見られません。記事3はPingFederateの概要と機能を説明し、記事4はPingFederateを用いたカスタムID-JAG（Identity-JWT Assertion Grant）の実装について述べています。これらの記事は、Step Functionsとは異なる認証・認可フレームワークの実装例として位置づけられ、本テーマとは異なる分野の情報となります。

記事5はPingFederateを用いたOne Tapの実装について記述しており、ユーザー認証のフローを説明しています。この記事は、PingFederateの認証処理における具体的なシナリオを示しており、Step Functionsとの関連性は薄いです。この記事は、認証フローの設計やセキュリティの観点から説明されており、本テーマの範囲外の情報となります。

## 深掘り調査で得られた知見

AWS Step Functions における Python コードを JSON にコンパイルする技術は、複数の開発者やコミュニティによって検討されており、その実装はいくつかの方向性で進められている。例えば、`pystepfunction` は Python コードを AWS Step Functions に必要な JSON 形式に変換するツールとして機能しており、Python の制御フローを JSON に反映する。このツールは、Python コードの正常な実行を保証しつつ、ステップ関数の定義に必要な JSON を生成する。一方、`sfnx` は Python を使用したステップ関数のワークフロー記述を可能にし、人間が読みやすい JSON 定義を出力する。これらは、手動で JSON を編集する必要を減らすための手段として位置付けられている。

また、AWS SDK for Python (Boto3) を使用した Step Functions の操作例は、AWS の公式ドキュメントに記載されており、ステートマシンの作成や実行、状態の取得など、基本的な操作を示している。しかし、Python コードを直接ステップ関数に変換するには、`pystepfunction` や `sfnx` のようなツールが利用される。これらのツールは、Python コードの構造を JSON に変換し、AWS Step Functions で利用可能な形式に変換する。このプロセスでは、Python コードの制御フローを JSON のステートマシンとして表現する必要がある。

さらに、CDK（Cloud Development Kit）を用いた Step Functions の例は、2023 年 9 月に提供されており、Python と CDK の統合が可能であることが確認されている。このことから、Python を使用した Step Functions の実装は、AWS サービスとの統合においても重要な役割を果たしている。一方で、`sfnx` と `pystepfunction` が JSONata を使用しているかという点については、情報が矛盾しており、明確な結論は得られていない。これらのツールの実装詳細や、JSON への変換プロセスについての情報は、今後の調査が必要である。

## 不確実な点・追加確認が必要な点

記事間での情報の整合性や断定できない点について、以下のように整理されます。

AWS Step Functions に関連する Python コードを JSON にコンパイルするツールについての情報は、複数の記事で取り上げられていますが、どのツールが「Python In, Readable JSON Out」を実現しているかについては明確ではありません。記事 2 では、`pysfn.tools.compile` が Python コードを JSON に変換し、Step Functions に利用可能であると記載されています。一方で、記事 1 では AWS SDK for Python (Boto3) を使用した Step Functions の操作例が紹介されており、Python コードを JSON に変換するツールの存在は示されていません。また、記事 1 と 2 では、どちらが JSONata を使用しているかについても矛盾しています。記事 1 では JSONata が利用されているとされ、記事 2 では JSONata と Python コードの関連性が曖昧です。

さらに、記事 5 では PingFederate に関する情報が含まれており、その中で ID-JAG（Identity Assertion JWT Authorization Grant）の実装に関する記述がありますが、これは AWS Step Functions と直接的な関連性は持ちません。また、記事 4 では PingFederate における ID-JAG の生成に関する説明が含まれていますが、これも AWS Step Functions とは関係ありません。

したがって、記事 1 と 2 では、Python コードを JSON に変換するツールの存在やその仕様についての記載が異なり、断定的な情報は得られていません。また、JSONata との関連性についても明確ではありません。このため、これらの記事をもとに「An AWS Step Functions Compiler: Python In, Readable JSON Out」というテーマについての断定的な記述は避け、情報の違いや不明点を明記する必要があります。

## 元記事一覧

- [Step Functions examples using SDK for Python (Boto3)](https://docs.aws.amazon.com/code-library/latest/ug/python_3_sfn_code_examples.html)
- [Compiling Python into AWS Lambda / Step Function - GitHubProcessing input and output in Step Functions - AWS Step ...pystepfunction · PyPIaws-cdk-examples/python/stepfunctions/README.md at main - GitHubstepscribe · PyPIHow do I use JSON Lambda output in Step Functions | AWS re:Post](https://github.com/bennorth/pyawssfn)
- [PingFederate: Federated SSO and Authentication | Ping Identity](https://www.pingidentity.com/en/product/pingfederate.html)
- [Custom ID-JAG onPingFederate, Part 1: Can... - DEV Community](https://dev.to/darkedges/custom-id-jag-on-pingfederate-part-1-can-pingfederate-1233-issue-an-id-jag-1eom)
- [Building One Tap for PingFederate, Part 1: Architecture and ...](https://dev.to/darkedges/building-one-tap-for-pingfederate-part-1-architecture-and-the-secure-account-bridge-3ed4)
