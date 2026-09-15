---
title: WAHAで89,479通のWhatsAppメッセージ処理とTwilio料金比較
type: knowledge
status: draft
created: 2026-09-15
updated: 2026-09-15
confidence: medium
---

# WAHAで89,479通のWhatsAppメッセージ処理とTwilio料金比較

## 結論

WAHAを用いた89,479通のWhatsAppメッセージの処理において、Twilioの料金体系に基づく推定金額は604ドルであり、これはMetaのテンプレートメッセージ料金とTwilioのメッセージ料金の2層構造を考慮した結果である。非テンプレートメッセージは無料となる条件が適用され、国ごとのMetaテンプレート料金の違いがコスト計算に影響を与えるため、正確な比較には国コードを考慮する必要がある。

## テーマ概要

このテーマは、WAHAを通じて89,479通のWhatsAppメッセージを処理した際のコスト分析に焦点を当てており、Twilioの料金が$604となったという実例が注目されている。WAHAはオープンソースのツールで、自前のサーバー上で動作し、制限がなく、JavaScript、Python、PHP、C#、Clojure、PowerShellなど複数の言語で利用可能である。この実験では、Metaのテンプレートメッセージ料金とTwilioのメッセージ料金の2層構造を比較し、非テンプレートメッセージは無料であることを明らかにした。特に、国によってMetaのテンプレート料金が異なるため、国ごとの比較が重要であることが指摘されている。このテーマは、自前インフラを構築する際のコスト削減や、メッセージングプラットフォームの料金体系の理解を深めるために注目されている。

## 共通して確認できる点

WAHAを通じて処理されたWhatsAppメッセージの数とTwilioの料金について、複数の記事で共通して確認できる事実がある。具体的には、89,479通のメッセージがWAHAを介して処理され、Twilioの料金として$604が発生したとされている。この数値は、30日間の期間内で、5つのWhatsAppインボックスから集約されたものである。WAHAはオープンソースであり、自前のサーバー上で実行可能で、制限が一切ない。また、WAHAはJavaScript、Python、PHP、C#、Clojure、PowerShellなど複数の言語で利用可能であり、WhatsApp Webを介してリアルなインスタンスを動作させることができる。Metaはテンプレートメッセージの送信にのみ料金を請求し、非テンプレートメッセージは無料である。Twilioの料金体系は、メッセージごとの料金とMetaのテンプレート料金の2層構造である。国によってMetaのテンプレート料金が異なるため、国ごとの比較が重要である。

## 記事ごとの差分・視点の違い

記事「IRan89,479WhatsAppMessagesThroughWAHA.Twilio: $604.」は、自前サーバーでのWhatsAppメッセージ処理のコスト実績を明らかにし、Twilioの料金と比較することで、自社インフラの経済性を示している。この記事では、WAHAを介したメッセージの処理量と、Metaのテンプレートメッセージ料金の国ごとの違いに注目し、正確な請求額を算出するための方法論を提示している。一方、記事「BuildingaReal-Time Multi-ToolAIAgentUsingLangChain&FastAPI」や「BuildinganaiagentpythonlangchainwithFastAPI· LogicLoopTech」は、AIエージェントの構築方法や技術的な実装について詳述しており、WAHAやTwilioの話題は扱っておらず、AI技術の応用例として位置付けている。記事「Retrieval-augmented generation - Wikipedia」は、RAG技術の定義と背景について解説し、WAHAやTwilioとの関連性はなく、AIモデルの情報取得方法の一つとして説明している。記事「StripeJustBoughtOpenRouterfor$7B+—andThatIstheMost...」は、OpenRouterの買収に関するニュースを伝えているが、WAHAやTwilioとの直接的な関係はなく、AIインフラストラクチャ市場の動向を扱っている。これらの記事は、それぞれ異なる視点や目的を持ち、WAHAやTwilioの話題を扱うか否かで区別される。

## 深掘り調査で得られた知見

WAHAを活用したWhatsAppメッセージの処理において、89,479通のメッセージが30日間の期間にわたって処理され、Twilioの料金体系に基づく推定金額は$604となった。この計算には、Metaのテンプレートメッセージ料金が適用されるタイミングと、非テンプレートメッセージが無料となる条件が反映されている。具体的には、非テンプレートメッセージは2024年11月1日から無料となり、2025年7月1日からは24時間以内のユーザー対応メッセージも無料となったため、実際の課金対象は、前日からのメッセージがなかった場合の出力メッセージに限られる。この結果、出力メッセージのうち67%が無料となり、課金対象は29,602通となった。Twilioのメッセージ料金は$0.005/メッセージで、Metaの国別テンプレート料金は受信先の国コードによって異なるため、国ごとの比較が重要となる。WAHAは自前のサーバーで実行可能で、JavaScript、Python、PHP、C#、Clojure、PowerShellなど複数の言語で利用可能であり、SwaggerドキュメンテーションとOpenAPIスキーマを提供しており、簡単に統合可能である。また、WAHAはWhatsApp Webを介してリアルなインスタンスを動作させ、ブロックされる可能性があるが、HTTP APIを通じてメッセージを送信および受信することができる。

## 不確実な点・追加確認が必要な点

記事間の食い違いや、資料からは断定できない点を具体的に書く。まず、「I Ran 89,479 WhatsApp Messages Through WAHA. Twilio: $604.」という記事では、WAHAを通じて30日間で89,479通のWhatsAppメッセージが処理され、Twilioの料金が$604と推定されていることが述べられている。ただし、この推定にはMetaのテンプレート料金とTwilioのメッセージ料金の2層構造を考慮した計算が含まれており、具体的な料金体系や国ごとの差異については、記事の内容に限っては明確に示されていない。また、WAHAの利用方法や設定に関する詳細な手順や、自前のサーバーでの実行環境についても、他の記事との整合性が確認されていない。さらに、RAG技術に関する記事では、その導入年月や具体的な実装例が記載されていないため、技術的詳細の断定は難しい。また、StripeがOpenRouterを買収した際の契約締結日や買収後の経営構造に関する情報は、すべての情報源で一致していないため、正確な断定は困難である。これらの点を踏まえると、各記事の内容はそれぞれ独立した情報源として捉え、統合的な分析を行う際には注意が必要である。

## 元記事一覧

- [BuildingaReal-Time Multi-ToolAIAgentUsingLangChain&FastAPI](https://manalisomani099.medium.com/building-a-real-time-multi-tool-ai-agent-using-langchain-fastapi-0377803b2022)
- [BuildinganaiagentpythonlangchainwithFastAPI· LogicLoopTech](https://www.logiclooptech.dev/building-an-ai-agent-python-langchain-with-fastapi/)
- [IRan89,479WhatsAppMessagesThroughWAHA.Twilio: $604.](https://dev.to/achiya-automation/i-ran-89479-whatsapp-messages-through-waha-twilio-604-3bog)
- [Retrieval-augmented generation - Wikipedia](https://en.wikipedia.org/wiki/Retrieval-augmented_generation)
- [StripeJustBoughtOpenRouterfor$7B+—andThatIstheMost...](https://dev.to/amrree/stripe-just-bought-openrouter-for-7b-and-that-is-the-most-important-ai-story-of-the-week-4kc9)
