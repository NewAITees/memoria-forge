---
title: ChatGPT Agentが自前コンピュータで動作するしくみ
type: knowledge
status: draft
created: 2026-10-08
updated: 2026-10-08
confidence: medium
---

# ChatGPT Agentが自前コンピュータで動作するしくみ

## 結論

OpenAIは2025年7月にChatGPT agentをリリースし、2026年9月にはDotsを導入して、ユーザーが独自のクラウドコンピューター環境でエージェントを運用できる仕組みを提供しています。これにより、ユーザーは重要なアクションを承認フローで制御し、MCP Eventsを通じてリアルタイムでの更新を受けることが可能となり、自前での実装が求められる状況となっています。

## テーマ概要

ChatGPT agent は、ユーザーが独自のコンピューター環境で動作するように設計されており、OpenAI が提供する Responses API を利用することで、同様の機能を自前で構築することが可能となっています。2025年7月に Pro, Plus, Team ユーザー向けにリリースされ、2026年9月には Pro および Business Premium ユーザー向けに Dots が導入され、常に動作するアーキテクチャが提供されました。Dots は個別にクラウドコンピューターを持ち、ユーザーが動作を監視できる仕組みとなっています。また、MCP Events は、OpenAI が2026年9月の DevDay で導入した仕組みで、MCP サーバーが変更を検知して ChatGPT にプッシュする仕組みであり、エージェントが常に最新の情報を取得できるようにしています。これらの技術的進展により、ChatGPT agent の独自環境での動作を再現し、自前で構築する必要性が高まっています。

## 共通して確認できる点

OpenAI は 2025 年 7 月 17 日から Pro, Plus, Team ユーザー向けに ChatGPT agent をリリースし、2026 年 9 月 29 日には Pro および Business Premium ユーザー向けに Dots を導入しました。Dots は個別にクラウドコンピュータを持ち、ユーザーはその動作を監視できます。重要なアクションはユーザーの明示的な承認を待って実行され、パスワード入力は 'takeover mode' でユーザーが直接入力します。OpenAI は開発者向けに Responses API と Computer Use Tool を提供し、Agents API は Codex harness を使用して自動的なコンテキストコンパクションやマルチエージェントオーケストレーションを提供しています。MCP Events は 2026 年 9 月 29 日の DevDay で導入され、ChatGPT は Protokollversion 2026-07-28 (MCP 2.0) でサポートしており、Webhook を用いて MCP サーバーから更新をプッシュします。OpenAI は 4 つの API（Agents API、Responses API、Agents SDK、AgentKit）を提供し、それぞれ異なるレイヤーで動作し、エージェントループの実行責任が異なります。

## 記事ごとの差分・視点の違い

記事「ChatGPT agent works on its own computer. Build the same with ...」は、OpenAIが提供するChatGPT agentが独自のコンピュータ環境で動作する仕組みを説明し、それを自前のシステムに実装する方法を解説しています。特に、ユーザーが直接操作できる環境や承認フローの重要性を強調しています。また、BurrowboxがOpenAIとは無関係に、独自のMCPエンドポイントを通じてOpenAI Responses APIを直接呼び出す仕組みも紹介されています。

記事「From model to agent: Equipping the Responses API ... - OpenAI」は、OpenAIが提供するResponses APIの仕組みと、それを用いてコンピュータ環境を構築する方法について説明しています。特に、MCP Eventsの導入によって、エージェントが情報の取得を待つ必要がなくなる点を強調しており、効率的なワークフローの実現が目的としています。

記事「MCPEventserklärt: Webhook-MCP-Server für ChatGPT erstellen...」は、MCP Eventsの仕様とその実装方法を詳しく解説しています。OpenAIがDevDayで発表したMCP Eventsの仕様と、それを実装するためのWebhookの使い方、認証方法などを具体的に紹介しており、技術的な実装に焦点を当てています。

記事「MCPCenter - Build Your Own Enterprise MCP Registry」は、MCP（Microsoft Cloud Platform）を用いて企業向けのMCPレジストリを構築する方法について説明しています。Azure API Centerを活用したスケーラブルなソリューションの構築が目的で、主に企業向けのインフラ構築に焦点を当てています。

記事「OpenAI Agents API vs Responses API vs Agents SDK vs AgentKit ...」は、OpenAIが提供する4つのAPI（Agents API、Responses API、Agents SDK、AgentKit）の違いと選択基準を比較しています。それぞれのAPIが提供する機能や制御レベル、推奨される使用ケースなどを詳細に説明し、開発者にとっての選択肢を明確にしています。

## 深掘り調査で得られた知見

OpenAIは2025年7月17日にChatGPT agentをPro、Plus、Teamユーザー向けにリリースし、2026年9月29日にDotsを導入して、ProおよびBusiness Premiumユーザー向けに常に動作するアーキテクチャを提供しました。Dotsは個別にクラウドコンピュータを持ち、ユーザーはその動作を監視できます。ユーザーはDotsが独自に実行できるアクションと承認が必要なアクションを設定できます。OpenAIは開発者向けにComputer-UsingAgent (CUA)モデルを活用したResponses APIとComputer Use Toolを提供しており、Agents APIはCodex harnessを使用し、自動的なコンテキストコンパクション、マルチエージェントオーケストレーション、プログラム化されたツール呼び出し、MCPサーバーのサポートを提供しています。Agents SDKはデプロイメント、ストレージ、承認、ランタイム統合の制御をアプリケーションに提供します。Self-hosted sandboxでは、ユーザー自身が環境を管理し、OpenAIがエージェントハルベストを実行します。

MCP Eventsは、OpenAIが2026年9月29日のDevDayで導入した仕様で、MCPサーバーがChatGPTに変更をプッシュできるようにし、エージェントが毎回確認を行う必要がありません。MCP EventsはProtokollversion 2026-07-28 (MCP 2.0)で実装され、ChatGPTはすべてのプランでサポートしています。MCPサーバーはevents/list、events/subscribe、events/unsubscribeを実装し、Callbackエンドポイントを検証し、標準Webhooks HMACで各配信を署名します。ChatGPTはWebhookによる配信のみを受け入れ、この仕様は実験的であり、コードは2026-07-28のバージョンにピンする必要があります。

OpenAIはエージェントの構築に4つのAPIを提供しています：Agents API、Responses API、Agents SDK、AgentKit。これらは異なるレイヤーで動作し、それぞれ異なる責任と制御境界を持ちます。Agents APIはOpenAIのCodex harness上で実行され、長時間セッション、コンテキストコンパクション、サブエージェントなどの機能を提供します。Responses APIは開発者がエージェントループを自分で実装できる低レイヤーのモデルエンドポイントであり、OpenAIが新プロジェクトを推奨しています。Agents SDKはTypeScriptとPythonのライブラリで、アプリケーション内でエージェントループを処理し、ツール実行、ガードレール、ハンドオフなどの機能を提供します。AgentKitはAgent Builder、ChatKit、Connector Registry、Evalsを含むツールのパッケージで、Agent Builderは2026年11月30日に終了します。APIの選択は制御レベル、コンプライアンス要件、望ましいランタイム環境に依存します。長時間稼働するクラウドエージェントにはAgents APIが推奨され、直接モデル制御とコンプライアンスが必要なアプリケーションにはResponses APIが推奨されます。

## 不確実な点・追加確認が必要な点

記事間の食い違いや資料からは断定できない点を以下のように具体的に述べます。

記事1と記事2の内容は、OpenAIが提供するChatGPT agentの動作環境やAPIの利用方法について述べていますが、具体的な実装の詳細や、どのAPIがどの環境で動作するかについては明確ではありません。記事1では、Dotsの導入や独自のクラウドコンピュータの利用が説明されていますが、記事2ではResponses APIやAgents APIの違い、それぞれの用途や制御方法が説明されています。しかし、どのAPIがどの環境で動作するか、あるいはどのAPIが特定の機能を提供するかについては、明確な結論は得られていません。

記事3と記事4は、MCP（Microsoft Cloud Platform）関連の技術について述べていますが、これらの技術がOpenAIのChatGPT agentとどのように統合されているか、あるいはMCP EventsがResponses APIやAgents APIとどのように関係しているかについては、明確な説明は見られません。記事3では、Webhookを用いたMCP Eventsの仕様が説明されていますが、その実装方法や、ChatGPT agentとの連携方法については、詳細が不足しています。

記事5では、OpenAIが提供する4つのAPI（Agents API、Responses API、Agents SDK、AgentKit）の違いと用途が説明されていますが、どのAPIが特定のタスクに適しているか、あるいはどのAPIがどの環境で動作するかについては、明確な指針が提示されていません。また、AgentKitの一部機能が2026年11月30日に終了するという情報はありますが、その影響範囲や代替案については、説明が十分ではありません。

以上の点から、各記事が提供する情報はそれぞれの観点から有用ですが、全体として一貫した技術的枠組みや実装方法については明確ではありません。今後の情報公開や技術ドキュメントの更新によって、これらの点が補完される可能性があります。

## 元記事一覧

- [ChatGPT agent works on its own computer. Build the same with ...](https://burrowbox.dev/blog/chatgpt-agent-own-computer)
- [From model to agent: Equipping the Responses API ... - OpenAI](https://openai.com/index/equip-responses-api-computer-environment/)
- [MCPEventserklärt:Webhook-MCP-ServerfürChatGPTerstellen...](https://apidog.com/de/blog/mcp-events/)
- [MCPCenter - Build Your Own EnterpriseMCPRegistry](https://mcp.microsoft.com/)
- [OpenAI Agents API vs Responses API vs Agents SDK vs AgentKit ...](https://dev.to/hassann/openai-agents-api-vs-responses-api-vs-agents-sdk-vs-agentkit-which-one-to-build-on-46d9)
