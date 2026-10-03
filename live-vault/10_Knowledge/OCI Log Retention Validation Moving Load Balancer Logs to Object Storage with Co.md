---
title: OCIログの長期保持確認とオブジェクトストレージへの移行方法
type: knowledge
status: draft
created: 2026-10-04
updated: 2026-10-04
confidence: medium
---

# OCIログの長期保持確認とオブジェクトストレージへの移行方法

## 結論

OCI Log Retention Validation において最も重要な判断は、ログの長期的な保持と取得可能性を確保するためには、OCI Logging と Object Storage のそれぞれの保持期間を独立して確認する必要があるということです。これにより、ログが Logging から削除された後でも Object Storage に保存されている可能性があるため、両方の設定を検証することが必須です。また、Connector Hub を通じたログのルーティングとライフサイクルルールの適切な設定が、ログの信頼性と運用上の要件を満たすために不可欠です。

## テーマ概要

OCI Log Retention Validation は、Oracle Cloud Infrastructure（OCI）におけるログの長期的な保存と取得可能性を確保するための検証プロセスを指します。このテーマは、特にLoad BalancerのログをOCI LoggingからObject Storageへ転送する際のロギングフローの検証に焦点を当てており、ログが適切に収集され、ルーティングされ、保存され、必要なときに取得できるかを確認する必要があります。OCI Loggingは、ログの収集と管理を担当し、Connector Hubを介してObject Storageへログを転送する仕組みを提供しています。一方、Object Storageは長期的な保存を目的としたストレージとして機能します。しかし、それぞれのサービスには独立した保持期間があり、ログがOCI Loggingから削除されてもObject Storageに保存されている可能性があるため、両方の保持期間を確認する必要があります。この検証プロセスは、コンプライアンスや運用上の要件を満たすために重要であり、特にログの保持期間やライフサイクルルールの設定が適切に行われているかを確認する必要があります。また、このテーマは、OCIのログ管理におけるベストプラクティスを理解し、実装時の検証をより正確かつ効率的に行うための参考となる情報として注目されています。

## 共通して確認できる点

Oracle Cloud Infrastructure (OCI) の Logging サービスは、リソースやカスタムアプリケーションからのログを収集・管理・分析するための重要な機能です。特に、Load Balancer のログは Logging で収集され、Connector Hub を経由して Object Storage に転送される仕組みが確認されています。このプロセスにおいて、ログの収集、ルーティング、保存、長期的な保持がそれぞれ独立した「保持時計」で管理される点が重要です。Logging サービスではログの保持期間が設定されていますが、Object Storage に保存されるコピーは別途のライフサイクルルールによって保持されます。そのため、ログが Logging から削除される一方で、Object Storage に保存されたコピーは依然として保持される可能性があります。このように、ログの保持期間は Logging と Object Storage の両方の設定を確認する必要があります。また、ログの収集・保存・保持の各段階で検証が求められ、ログがいつでも必要なときに取得できるようにする必要があります。これはコンプライアンスや運用上の目的において非常に重要です。 OCI の Logging サービスは、Connector Hub を使って Object Storage へのログ保存をサポートしており、ライフサイクルルールによってログの保持期間を管理しています。

## 記事ごとの差分・視点の違い

記事「OCI Log Retention Validation: Moving Load Balancer Logs to Object Storage with Connector Hub」は、具体的な実装例と検証プロセスに焦点を当てており、ログの収集から保存までの流れを検証するためのチェックリストを提供しています。この記事では、OCI LoggingとObject Storageの2つの保持時刻の違いに注意を払い、ログが適切に保存されているかを確認する必要性を強調しています。一方、「Logging provides access to logs from Oracle Cloud Infrastructure...」は、OCI Loggingサービスの基本的な機能と構造を説明し、ログの種類や管理方法、およびConnector Hubとの統合について解説しています。この記事はより一般的な観点から、ログの管理と利用方法を紹介しており、実装例よりも概念的な説明に重きを置いています。また、「FlowScript 0.1: A semantic language for describing applications before implementation」は、アプリケーションのセマンティックモデルを事前に記述するための言語としてのFlowScriptの概念と設計思想を説明しており、実装とは別な抽象的な視点からアプリケーション設計を考察しています。この記事では、アプリケーションの構造や動作を記述するための抽象的な言語としてFlowScriptが提案されており、実際の技術的な実装とは異なる視点を提供しています。他の記事は、それぞれ異なる目的と視点を持ち、OCI Loggingの検証、ログ管理の基本知識、アプリケーション設計の抽象表現というそれぞれのテーマに沿って内容が展開されています。

## 深掘り調査で得られた知見

OCI Log Retention Validation に関する深掘り調査では、ログの収集から長期的な保存までのプロセスが重要であることが明確に示されました。特に、OCI Load BalancerのログをObject Storageに移行する際には、Connector Hubを介したルーティングが必須であり、その際のログの保持期間は2つの retention clocks（Logging サービスとObject Storage）によって異なります。このため、単にログを有効にしたからといって、長期的な保存が保証されるわけではなく、各ステップでの検証が求められます。例えば、ロググループの設定、コンネクタの動作確認、バケットのライフサイクルルールの適用など、すべての要素が正しく動作しているかを確認する必要があります。

また、OCI Logging サービスは、リソースごとのログカテゴリを提供しており、それぞれのサービス（例: Object Storage、API Gateway）で異なるカテゴリが設定されています。これにより、特定のリソースのログを取得する際には、適切なカテゴリを有効化しておく必要があります。さらに、Logging サービスとObject Storageの統合により、ログの長期保存が可能となり、ライフサイクルルールを活用することで、自動的なアーカイブや削除が実現可能です。

このようなログ管理の実装では、コンプライアンスやセキュリティの観点からも、ログの可用性が極めて重要です。そのため、検証プロセスにおいては、ログがいつ、どこに保存されているか、そして必要なときに取得できるかを確認する必要があります。また、FlowScript 0.1 などの新しいツールやアプローチが登場することで、アプリケーションのセマンティックモデルを事前に定義し、実装に応じて柔軟に対応する手法も注目されています。これにより、ログ管理の設計段階での明確なモデルが求められるようになっており、技術的な実装だけでなく、業務上の要件も反映されるようになる可能性があります。

## 不確実な点・追加確認が必要な点

記事間での情報の整合性や断定できない点について、以下のように整理できます。

記事1では、OCI Load BalancerのログをOCI LoggingからObject Storageへ Connector Hubを介して移動するプロセスについて、実践的な検証チェックリストが提示されています。この記事は、ログの収集、ルーティング、保存、保持、およびレビュー可能な状態を確認するための手順を提供しており、特に「保持時刻の2つ」（LoggingサービスとObject Storageのそれぞれ）について強調しています。これは、ログがOCI LoggingからObject Storageへ移動した後でも、保持期間が異なる可能性があることを示しています。

一方で、記事2では、OCI Loggingサービスの概要と、OCIのネイティブサービス（API Gateway、Events、Functions、Load Balancer、Object Storage、VCN Flow Logsなど）から出力されるサービスログについて説明しています。記事2は、各サービスごとに事前に定義されたログカテゴリがあり、それらを有効化・無効化できる点を強調しています。しかし、記事2には、Connector Hubを介したログの移動やObject Storageへの長期保存に関する具体的な情報は含まれていません。

記事3や記事4は、アプリケーションのセマンティックモデルを記述するためのFlowScriptという言語について述べていますが、これらはOCIログの保持や移動とは直接関係がありません。記事5は、システムの失敗を含む設計についての話であり、OCIログの保持とは関連性がありません。

したがって、記事1と記事2の間に、OCI LoggingとObject Storageの連携についての情報が異なる点があり、特に記事1ではConnector Hubを介したログの移動と保持の検証が強調されているのに対し、記事2はログの収集とカテゴリの有効化に焦点を当てています。このため、記事1の内容は、OCI LoggingとObject Storageの連携に関する実践的な検証プロセスを示しており、記事2はその背景となるサービスの仕様を説明しています。そのため、記事1の検証プロセスが実際にどのようにOCI LoggingとObject Storageを連携させるかを示している一方で、記事2はその仕組みの背後にあるサービスの仕様を説明していると解釈できます。ただし、記事1で述べられているConnector Hubを介した移動や保持の検証が、記事2の情報と整合しているかは、明確な根拠が提示されていないため、断定することはできません。

## 元記事一覧

- [OCI Log Retention Validation: Moving Load Balancer Logs to ...](https://dev.to/arnold_infant/oci-log-retention-validation-moving-load-balancer-logs-to-object-storage-with-connector-hub-2hja)
- [Loggingprovides access tologsfromOracleCloud Infrastructure...](https://docs.oracle.com/en-us/iaas/Content/Logging/Concepts/loggingoverview.htm)
- [FlowScript 0.1: A semantic language for describing ...](https://dev.to/erland_kjensli_e3e4076039/flowscript-01-a-semantic-language-for-describing-applications-before-implementation-3pn3)
- [FlowScript | Reasoning Memory for AI Agents](https://flowscript.org/learn)
- [Speaker-DesigningSystemsThatContainFailure-CSWeekPerú...](https://dev.to/frostcore/designing-systems-that-contain-failure-cs-week-peru-2026-2703)
