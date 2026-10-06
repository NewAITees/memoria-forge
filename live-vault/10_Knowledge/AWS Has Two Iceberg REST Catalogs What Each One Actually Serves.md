---
title: AWSが提供するApache Iceberg RESTカタログの2つの実装とその違い
type: knowledge
status: draft
created: 2026-10-06
updated: 2026-10-06
confidence: medium
---

# AWSが提供するApache Iceberg RESTカタログの2つの実装とその違い

## 結論

AWSが提供するApache Iceberg RESTカタログには、AWS GlueとAmazon S3 Tablesという2つの実装があり、これらは同じ仕様に基づいておりながらも、テーブル作成時のテーブルロケーションの指定やネームスペース名の大小文字の制限、ルーティングプレフィックスの形式などの13の点で動作が異なっている。この違いは、開発者がどちらのサービスを選ぶか、あるいはクライアントが両方のサービスに対応する必要がある場合に重要な判断材料となる。

## テーマ概要

AWSが提供するApache Iceberg RESTカタログには、2つの実装が存在しており、それらは同じ仕様を実装しているものの、動作においていくつかの違いがある。このテーマは、AWS GlueとAmazon S3 Tablesの2つのRESTカタログがそれぞれどのような用途に使われ、どのような違いがあるかを明らかにする。この情報は、開発者がどちらのサービスを選ぶか、またはクライアントが両方のサービスに対応する必要がある場合に、重要な判断材料となる。特に、AWS Glueはテーブル作成時に明示的なテーブルロケーションを必要とし、他のカタログはその情報を自動的に推論する点が違いとして挙げられる。また、ネームスペース名の大小文字の取り扱いや、ルーティングプレフィックスの形式なども異なる。このような違いは、クライアントの設計やデータの管理に影響を及ぼす可能性があるため、現在注目されている。

## 共通して確認できる点

AWSでは、Iceberg RESTカタログの実装として2つのサービスが提供されており、それらは同一の仕様に基づいておりながらも、いくつかの点で振る舞いが異なっている。この2つのサービスは、AWS GlueとAmazon S3 Tablesである。どちらもマネージドサービスであり、SigV4署名をサポートしており、Iceberg RESTカタログの公開仕様に従っている。ただし、特定の操作においては、例えばテーブル作成時のテーブルロケーションの指定や、ネームスペース名の大小文字の制限など、13の点で振る舞いが異なる。これらの違いは、開発者がどちらのサービスを選ぶか、またはクライアントがどちらのサービスにも対応する必要がある場合に特に重要となる。また、両サービスは、リクエストの処理において異なるレスポンス形式を返すこともあり、クライアントの設計においてはその違いを考慮する必要がある。調査では、2026年9月3日に実施され、アカウントルートで実行され、権限関連の影響を排除した結果が得られている。

## 記事ごとの差分・視点の違い

記事ごとの立場や強調点、論点の違いは以下の通りです。

記事「AWS Has Two Iceberg REST Catalogs: What Each One Actually Serves」では、AWSが提供するIceberg RESTカタログの2つの実装（AWS GlueとAmazon S3 Tables）の違いを詳細に比較分析しています。この記事は、技術的な観点から、両サービスが同じ仕様を実装しているにもかかわらず、13の点で挙げられる動作の違いに注目し、Pythonによるプローブハーキスを用いた実験結果をもとに、実際の挙動を明らかにしています。また、この記事では、カタログの役割やREST APIの仕様についての背景知識も提供し、開発者がどちらのサービスを選ぶか、あるいはクライアントを両方に対応させる必要がある場合の選択肢を提示しています。

記事「AWS Builder Center」は、AWSの開発者向けコミュニティであるBuilder Centerのコンテンツとして掲載されており、Iceberg RESTカタログの2つの実装についての情報を提供しています。この記事は、他の記事に比べて技術的な詳細が少なく、むしろコミュニティでの情報共有と交流を促進するためのプラットフォームとしての役割を強調しています。また、この記事は、AWS Builder Centerのコンテンツとして、開発者間でのフィードバックや意見交換の場を提供している点が特徴です。

記事「AWSTransformNow Supports Block Storage Migration to FSx for ONTAP」では、AWS Transformが提供するブロックストレージの移行機能に焦点を当て、FSx for ONTAPへの直接的な移行が可能になったことについて述べています。この記事は、技術的な実装や移行プロセスにおける課題、特にネットワーク設定やコストに関する注意点を強調しています。また、この記事は、FSx for ONTAPの導入が企業のストレージ戦略において重要な役割を果たすことを示唆しており、移行の実際の手順や考慮すべき点を具体的に説明しています。

記事「Designing AWS Modernization with VMware Migration as the Entry Point」では、VMwareワークロードの現代化戦略に焦点を当て、AWS TransformとFSx for ONTAPの役割を説明しています。この記事は、単なる移行ではなく、アプリケーションやデータの再設計を含む現代化のプロセスを強調しており、ストレージの継続性と拡張性が現代化の鍵であることを論じています。また、この記事は、AWSが提供する現代化の5つの道筋を紹介し、ストレージ戦略が現代化の中心であることを示しています。

記事「What a Stack Deletion Leaves Behind — Nx Plugin for AWS 1.0, AWS Blocks and Amplify Gen 2 Compared」では、AWSの開発ツールやプラグインに関する情報を提供し、Nx Plugin for AWSやAWS Blocks、Amplify Gen 2の比較をしています。この記事は、AWSの新しい開発手法やツールの進化に注目し、開発者が選ぶべき最適なツールやアプローチについて考察しています。また、この記事は、スタック削除後に残るリソースやその影響についても言及しており、開発者がリソース管理を適切に行う必要があることを示唆しています。

## 深掘り調査で得られた知見

AWSが提供するIceberg RESTカタログには、AWS GlueとAmazon S3 Tablesの2つの実装があることが確認されている。両者は同じ公開された仕様に基づいており、35の操作を定義しているが、実際に動作する際には13の点で挙げられる違いがある。例えば、AWS Glueではテーブル作成時に明示的なテーブルロケーションが必要であり、他のカタログではその情報をワーキングから推論する。また、ネームスペース名には大文字が許容されず、タイムスタンプを含む一時的なネームスペースでは問題が生じる可能性がある。さらに、/v1/configのルーティングプレフィックスの返却形状が異なるため、クライアントが特定のフォーマットを想定している場合に問題が発生する可能性がある。これらの違いは、開発者がどちらのサービスを選ぶか、またはクライアントがどちらにも対応する必要がある場合に重要となる。調査は2026年9月3日に実施され、アカウントルートで実行されたため、権限関連のアーティファクトの影響を排除している。具体的な違いの詳細は、GitHubリポジトリ（xbill9/lakehouse-iceberg-2026）に記録されている。また、読み取り面では7つのカタログが一致していることが確認されており、これは異なるクラウドプロバイダー間でのIceberg RESTカタログの実装の一貫性を理解する上で重要な洞察となる。

## 不確実な点・追加確認が必要な点

記事間の食い違いや、資料からは断定できない点を具体的に挙げると、以下の通りです。  

まず、記事1と記事2は同内容の記事と思われるが、記事2は具体的な技術的比較や実験結果を含まないため、記事1に依拠する情報が主となります。記事1では、AWS GlueとAmazon S3 Tablesの2つのIceberg REST catalogが存在し、両者が同じ仕様を実装しているものの、13ヶ所の動作が異なることが明らかにされています。しかし、記事2にはこの違いの詳細が記載されておらず、技術的な比較や実験結果が見られません。  

また、記事3と記事4はFSx for ONTAPに関する内容で、AWS Transformの新機能について説明していますが、Iceberg REST catalogとは直接関係ありません。記事5はAWSのスタック削除に関する話題で、Iceberg REST catalogとは関係がありません。  

したがって、Iceberg REST catalogに関する情報は、記事1と記事2の内容に限定され、記事3〜5は関連性が低いため、このセクションでは無視します。また、記事1の調査結果では、AWS GlueとAmazon S3 Tablesの違いが特定されていますが、それらの違いが実際にどのような影響を及ぼすのか、あるいは他のAWSのIceberg REST catalogが存在する可能性についての情報は提示されていません。そのため、断定的な結論は避け、調査結果に基づいた事実のみを記載する必要があります。

## 元記事一覧

- [AWSHasTwoIcebergRESTCatalogs:WhatEachOneActually...](https://dev.to/aws-builders/aws-has-two-iceberg-rest-catalogs-what-each-one-actually-serves-2bob)
- [AWSBuilder Center](https://builder.aws.com/content/3Is77qtI7rNFlnhMn4K2oGRVJAR/aws-has-two-iceberg-rest-catalogs-what-each-one-actually-serves)
- [AWSTransformNow SupportsBlockStorageMigrationtoFSxfor...](https://dev.to/aws-builders/aws-transform-now-supports-block-storage-migration-to-fsx-for-ontap-benefits-and-pitfalls-from-a-1hhe)
- [DesigningAWSModernization with VMwareMigrationas the Entry...](https://dev.to/aws-builders/designing-aws-modernization-with-vmware-migration-as-the-entry-point-why-fsx-for-ontap-as-the-3k24)
- [What astackdeletionleavesbehind —NxPluginforAWS1.0,AWS...](https://dev.to/aws-builders/what-a-stack-deletion-leaves-behind-nx-plugin-for-aws-10-aws-blocks-and-amplify-gen-2-compared-10fg)
