---
title: PingFederateによるトランザクショントークン交換の実装
type: knowledge
status: draft
created: 2026-10-01
updated: 2026-10-01
confidence: medium
---

# PingFederateによるトランザクショントークン交換の実装

## 結論

PingFederateはTokenetesアーキテクチャにおいてTransaction Token Service（TTS）として機能し、RFC 8693のtoken exchangeプロトコルを用いてTxn-Tokenを発行する技術的実装を提供しており、ユーザーのアクセストークンとエージェントのワークロード証明を独立して検証することで、相互に代替できない信頼性を確保しています。この設計により、トランザクションコンテキストを安全に伝達し、エンドツーエンドでの信頼性を実現する仕組みが構築されています。

## テーマ概要

Trusted AI Agent Transactions, Part 2: PingFederate Token Exchange は、AIエージェント間の信頼されたトランザクション処理における技術的実装を説明する記事です。このテーマでは、PingFederateがTransaction Token Service（TTS）として機能し、RFC 8693のtoken exchangeプロトコルを用いてTxn-Tokenを発行する仕組みが中心です。ユーザーのアクセストークンとエージェントのワークロード証明（JWT-SVID）を交換し、それぞれの役割を明確に分離することで、ユーザーの承認とワークロードの証明が相互に代替できないようにしています。この設計により、トランザクションのコンテキストを安全に伝達し、エンドツーエンドの信頼性を確保する仕組みが構築されています。このような技術は、複数のAIエージェントが協調して動作する環境でのセキュリティと信頼性を高めるため、現在注目されています。

## 共通して確認できる点

PingFederateは、TokenetesアーキテクチャにおいてTransaction Token Service（TTS）として機能し、RFC 8693のtoken exchangeプロトコルを使用してTxn-Tokenを発行しています。このプロセスでは、エージェントがユーザーのアクセストークン（サブジェクトトークン）とワークロードのJWT-SVID（アクタートークン）をPingFederateに送信し、両方のトークンが独立して検証されます。サブジェクトトークンは外部呼び出しの承認者を示し、アクタートークンは attestされたワークロードを証明します。いずれのトークンも他方の代替として受け入れられず、PingFederateは論理的なAIエージェントをランタイムワークロードにバインディングします。Txn-TokenはES256署名で署名され、`txntoken+jwt`というタイプで、リクエストワークロードとトランザクションコンテキストを含み、MCPゲートウェイ、MCPサーバー、保護されたAPIを通じて変更なしに伝播されます。検証プロセスでは、署名、発行者、受信者、時間、キーID、アルゴリズムが確認され、SPIFFE IDがマッピングされます。生のトークンはアプリケーションや監査ログに記録されず、TLSで検証されたリクエストボディにのみ含まれます。また、この設計ではユーザーのトークンとワークロードの証明が互いに代替できないようにし、トランザクションコンテキストをシステム全体に伝播させています。

## 記事ごとの差分・視点の違い

記事「Trusted AI Agent Transactions, Part 2: PingFederate Token Exchange」では、PingFederateがTransaction Token Service（TTS）として機能し、RFC 8693のtoken exchangeプロトコルを使用してTxn-Tokenを生成する仕組みを説明しています。主に技術的な実装とPingFederateのロールに焦点を当てており、ユーザーのトークンとワークロードの証明が相互に代替できない点を強調しています。また、Txn-Tokenの構造や検証プロセス、トークンの転送経路について詳しく解説しています。

記事「Two tokens, one exchange: binding a user's consent to an ...」は、ユーザーの同意とワークロードの証明を一つのトークン交換プロセスで結びつける仕組みを論じています。特に、トークンの有効期間や検証プロセス、トークンがアプリケーションログに記録されないというセキュリティ上の考慮点を強調しています。また、PingFederateの内部マッピングテーブルが論理エージェントを決定する重要な役割を果たしている点も指摘しています。

記事「TrustedAIAgentTransactions,Part5:End-to-EndProof」は、前記事で説明された技術を統合したエンドツーエンドの証明プロセスを検証するテストスイートの設計について述べています。ユーザー認証からトランザクションの検証、API呼び出し、イベントログの関連付けまでを網羅し、セキュリティとトレーサビリティを確保するための設計原則を強調しています。また、トークンがアプリケーションログに記録されないという点も再確認しています。

記事「From Zero to Your FirstAIAgentin 25 Minutes (No Coding) - YouTube」は、AIエージェントの構築に必要な技術的プロセスを簡潔に紹介しており、実際の実装やデプロイメントの手順を示すものではありません。したがって、この記事は他の技術記事とは異なり、実装の詳細ではなく、概要と導入に焦点を当てています。

記事「Scaling AI Safety for a Multi-Agent World - Schmidt Sciences」は、AIエージェントが複数のエージェントと協働する環境での安全性確保に焦点を当てています。特に、大規模なエージェントネットワークにおけるリスクや、ゼロトラストセキュリティの実装、オープンソースのAegisSwarmフレームワークの導入など、より広範な安全基盤の構築に言及しています。他の記事とは異なり、技術的な実装ではなく、システム全体の安全性と信頼性の確保に注力しています。

## 深掘り調査で得られた知見

PingFederateは、TokenetesアーキテクチャにおいてTransaction Token Service（TTS）として機能し、RFC 8693に基づくトークン交換プロトコルを用いてTxn-Tokenを発行しています。このプロセスでは、ユーザーのアクセストークン（subject token）とエージェントのワークロード証明（actor token）がPingFederateに送信され、それぞれが独立して検証されます。subject tokenは外部呼び出しの承認者を示し、actor tokenは attestされたワークロードを証明します。両者とも相手を代わる substitutes として認められず、PingFederateが論理的なAIエージェントをそのランタイムワークロードにバインドします。Txn-TokenはES256で署名され、`txntoken+jwt`の形式で、リクエストワークロードとトランザクションコンテキストを含み、MCPゲートウェイ、MCPサーバー、保護されたAPIを通じて変更なしに伝達されます。検証では、署名、発行者、受信者、時間、キーID、アルゴリズムがチェックされ、SPIFFE IDがマッピングされます。生のトークンはアプリケーションや監査ログに書き込まれず、TLSで検証されたリクエストボディにのみ含まれます。この設計により、ユーザーのトークンとワークロードの証明が相互に代替できないため、セキュリティとトレーサビリティが確保されています。また、Txn-Tokenはブラウザセッショントークンとして使用されず、イベントの選択を通じて、安全なリクエストとレスポンスメタデータ、デコードされた許可リストのトークンクレームが表示されます。PingFederateの起動では、カスタムトークンプロセッサプラグインの構築とテストが行われ、Terraform構成は別途のステップとして残ります。同様に、PingAuthorizeはリポジトリ所有のデプロイメントパッケージから開始され、コンテナは予期されるローカルアプリケーションブリッジネットワークにのみ参加します。シークレットやライセンス、生成された証明書、プライベートキー、Terraformステート、ディスカバリー出力はGitの外に残されます。エンドツーエンドのテストスイートは成功ケースだけでなく、偽造されたトランザクショントークンによる拒否や、MCPサーバーのみが許可される直接エージェントへのAPIアクセスを証明する必要があります。トランザクションIDはすべての予期されるホップで一貫しており、キャプチャされたログには生のトークンマテリアルが含まれていません。PingFederateのクリーンブートストラップテストでは、孤立したボリュームとTerraformステート、管理されたTLS、ライブ交換、改ざんされたアクタートークンの拒否、そしてランダムに名付けられたリソースのクリーンアップが再現されます。エージェントセキュリティはエージェントIDクレームの追加やユーザートークンのダウンストリームでの通過では解決されず、実装にはユーザー、論理エージェント、ワークロード、トランザクション、および即時コールラーのそれぞれの証拠が必要です。PingFederateは制御された委任境界を提供し、SPIREはランタイムアイデンティティを証明し、PingAuthorizeは検証されたアクションコンテキストを評価します。ゲートウェイはアイデンティティ検証、ルーティング、ポリシーアウトフォースの境界を保持し、これらはエージェントアクションを説明可能でテスト可能にします。誰が承認したか、どのエージェントが承認されたか、どのワークロードが実行したか、なぜトランザクションが存在するのか、どのサービスが各呼び出しを行ったか、どのポリシーが操作を許可または拒否したかといった点が明確にされます。

## 不確実な点・追加確認が必要な点

記事間の食い違いや資料からは断定できない点を以下のように具体化できます。

記事1と記事2はともにPingFederateがRFC 8693 token exchangeプロトコルを用いてTxn-Tokenを生成するプロセスについて述べていますが、記事1ではPingFederateがTransaction Token Service（TTS）として動作し、ユーザーのトークンとワークロードの証明を別々に検証するプロセスが詳細に説明されています。一方、記事2では、ユーザーのトークンとワークロードの証明が同一の交換プロセスで処理され、それぞれの有効期限や検証条件が異なる点が強調されています。しかし、記事2では具体的な検証ステップやトークンの構造についての詳細は提示されていません。

記事3は、Trusted AI Agent Transactionsの最終部分として、エンドツーエンドの証明プロセスを説明しており、Txn-Tokenの検証やトランザクションIDの一致、イベントの関連付けなどに関する詳細な情報が含まれています。ただし、この記事は他の記事とは異なるセクションであり、PingFederateやSPIRE、PingAuthorizeなどの技術の統合に焦点を当てています。そのため、記事1や記事2の内容とは一部重複しており、また、他の記事には含まれていない独自の情報も含まれています。

記事4は、AIエージェントの構築方法についての動画の紹介であり、Trusted AI Agent Transactionsに関する直接的な情報は含まれていません。記事5は、多エージェント環境におけるAI安全性の重要性を論じており、PingFederateやSPIREなどの技術がどのように安全性を確保するかについての説明は含まれていません。したがって、記事5は他の記事と比べて、技術的な実装やプロセスについての詳細は提示されていません。

また、記事1と記事3では、Txn-Tokenの検証プロセスやトランザクションIDの一致、イベントの関連付けなど、いくつかの点で重複しているにもかかわらず、それぞれの記事が提供する情報は異なるため、全体像を把握するには複数の記事を参照する必要があります。一方で、記事2や記事5では、他の記事に記載されていない独自の情報や、技術的な実装についての詳細が含まれていないため、他の記事と比べて情報量が少ないという点も確認できます。

## 元記事一覧

- [Trusted AI Agent Transactions, Part 2: PingFederate Token ...](https://www.webnuz.com/article/2026-08-23/Trusted+AI+Agent+Transactions,+Part+2:+PingFederate+Token+Exchange)
- [Two tokens, one exchange: binding a user's consent to an ...](https://theclarity.today/story/trusted-ai-agent-transactions-part-2-pingfederate-token-exchange-65aae471)
- [TrustedAIAgentTransactions,Part5:End-to-EndProof](https://dev.to/darkedges/trusted-ai-agent-transactions-part-5-end-to-end-proof-44b5)
- [From Zero to Your FirstAIAgentin 25 Minutes (No Coding) - YouTube](https://www.youtube.com/watch?v=EH5jx5qPabU)
- [Scaling AI Safety for a Multi-Agent World - Schmidt Sciences](https://www.schmidtsciences.org/multi-agent-ai/)
