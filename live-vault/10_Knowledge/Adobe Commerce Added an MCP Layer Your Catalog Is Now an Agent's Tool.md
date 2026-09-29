---
title: Adobe Commerce MCPレイヤー導入でカタログがエージェントツールへ
type: knowledge
status: draft
created: 2026-09-29
updated: 2026-09-29
confidence: medium
---

# Adobe Commerce MCPレイヤー導入でカタログがエージェントツールへ

## 結論

Adobe Commerceは2026年4月にAdobe SummitでMCP（Machine Communication Protocol）レイヤーを導入し、カタログをAIエージェントが操作可能なツールとして再定義した。この変更により、カタログは名前付きのスキーマ定義された関数として扱われ、AIエージェントがリアルタイムで商品データにアクセスし、カート作成やチェックアウトなどのタスクを実行できるようになった。

## テーマ概要

Adobe CommerceがMCP（Machine Communication Protocol）レイヤーを導入し、カタログをAIエージェントのツールとして活用できるようにする動きが注目されている。この変更により、カタログは従来のデータとしてレンダリングされるのではなく、AIエージェントが呼び出せる名前付きの関数として扱われるようになった。これにより、リアルタイムでのカタログデータへのアクセスが可能となり、カート作成、チェックアウトの開始、在庫の確認、プロモーション情報の提供など、複数の業務プロセスをAIエージェントが実行できるようになった。この変更はAdobe Summit 2026で発表され、Commerce MCPサーバーの導入が中心となる。一方で、この機能の利用状況や具体的な導入時期については、Adobeの公式ドキュメントでは「Coming Soon」と表示されており、現時点では明確な情報は提供されていない。このような背景から、Adobe CommerceのAIファーストへの転換が注目されている。

## 共通して確認できる点

Adobe Commerce では、MCP（Machine Communication Protocol）レイヤーの導入により、カタログが AI アーセットとして扱われるようになった。この変更により、カタログは以前のようにフロントエンドでレンダリングされるデータから、AI アージェントが呼び出せる名前付きの、スキーマ定義された関数へと移行した。これにより、AI アージェントはリアルタイムで販売データとやりとりし、カート作成、チェックアウト開始、在庫確認、プロモーションなどのタスクを実行できるようになった。

この MCP サーバーの導入は、Adobe Summit 2026 で発表され、AI ファーストのプラットフォームとしての Experience Cloud の再ブランド化、CX Enterprise と称される新たな戦略に位置付けられた。ただし、MCP フィーチャーの利用状況や導入時期については、Adobe の Experience League では「Coming Soon」と表示されており、具体的な導入スケジュールや適用範囲は明示されていない。一部のパートナー企業では既にクライアントプロジェクトで利用されているとの情報もあるが、すべての導入環境に適用されるわけではない。PaaS やオンプレミスの Magento 環境では、特に注意が必要である。

## 記事ごとの差分・視点の違い

記事1は、MCP層の導入が実際にAIエージェントとのインターフェースとして機能し始めていることを示す具体例を提供しており、特にShopifyのケースを挙げて、変更前後の挙動の違いを明確に描写しています。この記事では、技術的な変更点とその影響を実際のデプロイ状況をもとに解説しており、開発者コミュニティの反応も踏まえた分析が含まれています。一方、記事2はAdobe Commerceの公式ドキュメントであり、MCPの概要とその目的を簡潔に説明し、今後の導入を示唆していますが、具体的な実装やデプロイ状況には触れていないため、技術的な詳細に偏りがちです。記事3は、Adobe Summit 2026での発表をもとに、MCPがデフォルトのエージェントプロトコルとして導入されたことを強調しており、AdobeがAIファーストのプラットフォームへと方向転換していることを論じています。記事4は、Adobe Summit 2026での発表内容をもとに、MCPサーバーの導入だけでなく、他のエージェント関連のアップグレードも含めて全体像を捉えています。記事5は、Adobe Commerce MCPと開発者エージェントの導入をもとに、具体的な実装例としてCommerce Developer Agentの紹介を行い、技術的な実装とその利用シーンを強調しています。各記事は、技術的詳細、導入背景、実装例、そして今後の展望という観点から、MCP導入の多角的な側面を描いています。

## 深掘り調査で得られた知見

Adobe Commerce は、AI アーカイブの進化に伴い、MCP（Machine Communication Protocol）レイヤーを導入し、カタログを AI エージェントが操作可能なツールとして再定義する重要な変更を実施しました。この変更により、カタログはかつてはフロントエンドによってレンダリングされるデータから、AI エージェントが呼び出せる名前付きの、スキーマベースの関数へと移行しました。これにより、AI エージェントはリアルタイムで販売データとやりとりし、カート作成、チェックアウト開始、在庫確認、プロモーションなどのタスクを実行できるようになりました。

この変更は、Adobe Summit 2026 で発表され、Commerce MCP サーバーが提供する機能を通じて、AI エージェントがカタログ、カート、価格、在庫、プロモーション、チェックアウト、注文管理、購入後のフローにアクセスできるようにするものでした。これは、Adobe が AI ファーストのプラットフォームへと方向転換する一環として、Experience Cloud を CX Enterprise へと再ブランド化する動きの一端を担っています。

ただし、MCP フィーチャーの利用状況や導入スケジュールについては、現時点では明確ではありません。Adobe の Experience League では「Coming Soon」と表示されており、変更の詳細や導入対象は明示されていません。一方で、一部のパートナーは既にクライアントプロジェクトにおいて MCP を導入していると報告しており、導入の進捗や実装の詳細については、開発者や企業が継続的に情報を収集していく必要があります。

## 不確実な点・追加確認が必要な点

記事間では、Adobe CommerceがMCP（Machine Communication Protocol）レイヤーを導入したことでカタログがAIエージェントのツールとなるという点では一致していますが、具体的な実装時期や状態についての情報が食い違っています。記事1では、2026年4月9日にAIエージェントがShopifyのStorefront MCPエンドポイントで`search_shop_catalog`を呼び出せたものの、4月10日にそのツールが見つからなくなったという事実が記載されています。これは、ShopifyがカタログツールをUniversal Commerce Protocolに移行し、`search_catalog`に名前を変更したことを示しています。この変更はAdobe CommerceのMCPレイヤー導入と関連している可能性がありますが、明確な因果関係は示されていません。

一方、記事3と記事4は、Adobe Summit 2026（2026年4月20日）での発表をもとに、Commerce MCPサーバーが正式に導入され、Experience CloudがCX Enterpriseとして再ブランド化されたと述べています。また、記事5では、Commerce Developer Agent（今後リリース予定）がAIを活用したツールセットとして、既存のCommerce実装を分析し、Adobe Commerce as a Cloud Service（ACCS）への移行をサポートするものであると説明されています。これらの情報は、MCPの導入が2026年4月のAdobe Summitで正式に発表されたことを示しており、その時点で既に一部のプロジェクトで導入されている可能性があります。

しかし、記事2のAdobe Commerce Experience Leagueページでは、MCPが「Coming Soon」と表示されており、まだ正式にリリースされていない可能性があります。また、記事1では、AdobeのExperience Leagueページが「Coming Soon」と表示されているにもかかわらず、一部のパートナーがすでにクライアントプロジェクトで使用していると述べられており、導入の進捗や利用状況についての明確な情報は得られていません。このように、MCP導入の実装時期や利用状況については、各記事で異なった情報が示されており、断定的な結論は避けられる必要があります。

## 元記事一覧

- [Adobe Commerce Added an MCP Layer: Your Catalog Is Now an ...](https://dev.to/andriiboyko/adobe-commerce-added-an-mcp-layer-your-catalog-is-now-an-agents-tool-13co)
- [Commerce MCP overview | Adobe Commerce - Experience League](https://experienceleague.adobe.com/en/docs/commerce-learn/ai-and-agentic-commerce/commerce-mcp/commerce-mcp-overview)
- [Adobe Just Made MCP the Default Agent Protocol for Commerce ...](https://www.paz.ai/blog/adobe-mcp-commerce-default-agent-protocol)
- [Adobe Commerce Summit 2026 Unveils Agentic Upgrades: Reducing ...](https://stellagent.ai/insights/adobe-commerce-summit-agentic-upgrades)
- [Adobe Summit 2026: Adobe Commerce MCP & Developer Agent | antegma](https://www.antegma.com/en/insights/2026/04/22/adobe-summit-2026-adobe-commerce-recap/)
