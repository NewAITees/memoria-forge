---
title: フェデレーテッド脅威インテリジェンスによるIOC共有 without コンテンツ共有
type: knowledge
status: draft
created: 2026-10-21
updated: 2026-10-21
confidence: medium
---

# フェデレーテッド脅威インテリジェンスによるIOC共有 without コンテンツ共有

## 結論

Federated Threat Intelligence Sharing IOCs Without Sharing Contentは、AIセキュリティ分野において、従来の脅威インテリジェンス共有の遅延問題を解消するための革新的なアプローチとして注目されている。AegisGateが採用する方法では、攻撃のパターンや技術を暗号化したSHA-256フィンガープリントとして共有し、機密情報やトレードシークレットを保護しながら、リアルタイムでの攻撃検出と防御が可能になる。この技術は、信頼ネットワークを構築し、各組織が検出した脅威を即座に全関係者に共有することで、攻撃の拡散を食い止める効果が期待されている。

## テーマ概要

Federated Threat Intelligence Sharing IOCs Without Sharing Content は、脅威インテリジェンスの共有において、具体的な攻撃情報（Indicators of Compromise: IOCs）を共有する一方で、攻撃の詳細な内容や機密情報（PII、トレードシークレット、内部ビジネスロジックなど）を共有しない方法を指します。このアプローチは、従来の脅威インテリジェンス共有の遅延問題を解決するためのものであり、組織間での信頼関係を築きながら、リアルタイムでの攻撃検出と防御を可能にします。特にAIセキュリティ分野では、攻撃が急速に進化するため、情報共有の遅延が大きなリスクとなるため、この方法が注目されています。AegisGateなどのプラットフォームがこの概念を実現しており、暗号化技術や信頼ネットワークを活用して、攻撃の検出を迅速化し、情報共有のプライバシーや信頼性を確保しています。

## 共通して確認できる点

AegisGateは、AIセキュリティ分野において、脅威インテリジェンスの共有においてコンテンツを共有せずにIOC（Indicators of Compromise）を共有するフェデレーテッドなアプローチを採用したプラットフォームとして注目されています。このアプローチでは、各組織が検出した脅威を暗号化したSHA-256フィンガープリントとして共有し、他の組織が同じフィンガープリントを持つIOCを検出することで、攻撃の確認と即時の対応が可能になります。この方法により、情報共有の遅延が解消され、攻撃が広がる前に防御が可能になります。また、AegisGateは、ECDSA P-256を用いた署名付きのIOCバンドルをHTTPゴシッププロトコルを通じて配信し、各インスタンスが独自のキーリングを保持し、ブートストラップペアリストを通じて他インスタンスの公開鍵を発見する仕組みを採用しています。これにより、中央権力を持たない信頼のネットワーク（トラストメッシュ）が構築され、各インスタンスが信頼度に基づいてIOCを処理します。さらに、AegisGateはTAXII 2.1とSTIX 2.1をサポートし、既存の脅威インテリジェンスプラットフォームとの互換性を確保しています。また、検出されたIOCは、他の組織の保護に即座に利用されるため、ネットワーク効果が発生し、全体のセキュリティ強化につながります。

## 記事ごとの差分・視点の違い

記事「FederatedThreatIntelligence:SharingIOCsWithoutSharingContent」は、AIセキュリティにおける脅威インテリジェンス共有の遅延問題を解決するためのフェデレーテッドインテリジェンス共有システムを提案しており、特にIOCs（インジケーター・オブ・コンプロムート）を共有する際のコンテンツ共有を避ける方法を強調しています。この記事では、ECDSA P-256による署名やHTTPゴシップ通信、信頼ネットワークの構築といった技術的設計が詳細に説明されています。

記事「FederatedIOC Store — Crowdsourced AIThreatIntelligence」は、AegisGateプラットフォームが提供するフェデレーテッドIOCsストアの仕組みを解説しており、AI特化の脅威インテリジェンス共有ネットワークの実現を目指しています。特に、STIX 2.1形式でのIOCsの配信や、TAXII 2.1との互換性が強調されており、企業向けの実装可能性が示されています。

記事「Schemagovernance and change-detectionlayer for modern data...」は、スキーマドリフトの検出と契約遵守を目的としたSchemaGuardツールの設計と機能を説明しており、データパイプラインの信頼性向上を主な目的としています。この記事では、YAMLベースのスキーマ契約の自動生成やSHA-256によるロック機能が特徴です。

記事「PreventSchemaDriftwithSchemaGuard| Anil Solanki... | LinkedIn」は、SchemaGuardツールの実装例とCI/CDとの統合について詳しく紹介しており、データエンジニア向けの実践的な導入方法が示されています。この記事では、多種のデータベースサポートや自動通知機能が強調されており、実装の利便性が重視されています。

記事「Transport Layer Security - Wikipedia」は、TLSプロトコルの技術的概要とその応用範囲について解説しており、セキュリティとスケーラビリティのバランスに関する課題を提示しています。この記事では、TLSの限界とその対応策としてのレート制限や行動分析の必要性が述べられています。

## 深掘り調査で得られた知見

深掘り調査により、フェデラーテッド脅威インテリジェンス共有におけるIOC（Indicators of Compromise）の共有なしでの実現が、特にAIセキュリティ分野で注目されていることが明確になった。AegisGateが開発したフェデラーテッド脅威インテリジェンスシステムは、従来の脅威情報共有の遅延問題を解消するための革新的なアプローチとして、業界内で広く検討されている。このシステムでは、IOCをSHA-256でハッシュ化し、ECDSA P-256で署名することで、攻撃のパターンや技術を共有する一方で、機密情報やトレードシークレットを保護する。これにより、企業間での信頼関係を築くことが可能となり、攻撃が発覚した時点で即座に全関係者に通知される仕組みが実現されている。

また、このアプローチは、AI攻撃の迅速な変異に対応するための必要不可欠な手段として位置付けられており、攻撃者が新しい技術を用いて複数の企業に同時に攻撃を仕掛けるようなケースでも、検出後すぐに全関係者にIOCを共有することで、攻撃の拡散を食い止めることが可能となる。さらに、このシステムは、TAXII 2.1とSTIX 2.1をサポートしており、既存の脅威情報共有プラットフォームとの連携も可能であるため、広範な導入が期待されている。このような技術の進化は、セキュリティ分野におけるデータ共有の新たなモデルとして、今後も注目される可能性が高い。

## 不確実な点・追加確認が必要な点

記事間の食い違いや資料からは断定できない点として、以下の内容が挙げられます。まず、Federated Threat Intelligence Sharing IOCs Without Sharing Contentというテーマに関連する記事1と記事2は、同一体系の技術を説明していますが、具体的な実装や運用の詳細については曖昧な部分があります。記事1では、AegisGateが開発したフェデラルな脅威インテリジェンス共有システムについて、暗号化されたIOCの共有や信頼メッシュの構築が述べられていますが、その実際の運用環境やスケーラビリティについては明示されていません。一方、記事2では、Federated IOC Storeが提供するサービスについて、リアルタイムでのIOC配信やTAXII 2.1の互換性が強調されていますが、具体的な導入事例や実績データは提示されていません。また、記事3と記事4は、スキーマガードというツールについての説明であり、データパイプラインでのスキーマドリフト防止のための技術的なアプローチを紹介していますが、これらのツールがFederated Threat Intelligenceと直接的な関連性を持つのかについては明確ではありません。さらに、記事5のTLSに関する説明は、セキュリティプロトコルの基本的な仕組みを述べていますが、Federated Threat Intelligenceやその他の技術との関連性は提示されていません。このような点から、各記事が提示する技術や概念の間には、明確な関連性や整合性が確認できない部分があり、さらなる調査や情報収集が必要です。

## 元記事一覧

- [FederatedThreatIntelligence:SharingIOCsWithoutSharing...](https://dev.to/aegisgate/federated-threat-intelligence-sharing-iocs-without-sharing-content-bpk)
- [FederatedIOC Store — Crowdsourced AIThreatIntelligence](https://aegisgatesecurity.io/federated-ioc/)
- [Schemagovernance and change-detectionlayer for modern data...](https://pypi.org/project/pyschemaguard/)
- [PreventSchemaDriftwithSchemaGuard| Anil Solanki... | LinkedIn](https://www.linkedin.com/posts/anilsolanki-dataengineer_github-anilsolanki2645schema-guard-a-activity-7474449029691793408-QWgH)
- [Transport Layer Security - Wikipedia](https://en.wikipedia.org/wiki/Transport_Layer_Security)
