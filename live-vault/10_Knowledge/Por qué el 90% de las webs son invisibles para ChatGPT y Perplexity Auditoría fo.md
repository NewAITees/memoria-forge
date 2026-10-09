---
title: AI検索エンジンが90%のウェブサイトを無視する理由
type: knowledge
status: draft
created: 2026-10-10
updated: 2026-10-10
confidence: medium
---

# AI検索エンジンが90%のウェブサイトを無視する理由

## 結論

AI検索エンジンが多くのウェブサイトを無視する現象は、主にWAFやHTTP 403エラーの設定によってAIクローラーがブロックされている技術的要因が原因である。特に、CloudflareやAWS WAFなどのファイアウォールツールがデフォルトでスクラブラーをブロックする設定になっているため、OpenAIやPerplexityのクローラーがアクセスを拒否されるケースが確認されている。このため、企業はウェブサイトのインフラストラクチャを再評価し、AI検索エンジンのクローラーがアクセスできる環境を整える必要がある。

## テーマ概要

AI検索エンジンであるChatGPTやPerplexityが、多くのウェブサイトのコンテンツを読み取ることができない現象が注目されている。この現象は、90%以上の企業サイトがこれらのAI検索エンジンに対して「不可視」であるという調査結果を背景にしている。その理由として、ウェブサイトのインフラストラクチャーやセキュリティ設定がAI検索エンジンのクローラーをブロックしている可能性が指摘されている。特に、WAF（Web Application Firewall）やHTTP 403エラーの設定が原因で、AI検索エンジンがウェブサイトにアクセスできず、情報収集を妨げているとされている。また、SEO（検索エンジン最適化）が従来の検索エンジン向けに設計されており、AI検索エンジンの特性に合っていないことも問題として挙げられている。このため、企業はウェブサイトのアーキテクチャやコンテンツ構造の再設計を検討する必要があるとされている。

## 共通して確認できる点

AI検索エンジン（例：ChatGPT、Perplexity）が多くのウェブサイトを無視している現象について、複数の記事で共通して確認された事実は、ウェブサイトのインフラストラクチャがAI検索エンジンのクローラーをブロックしている可能性が高いということです。特に、WAF（Web Application Firewall）やHTTP 403エラーの設定が、AI検索エンジンのクローラーを自動的に拒否していることが指摘されています。これにより、クローラーがウェブサイトにアクセスできず、コンテンツがAI検索エンジンにインデックス化されない状態になっています。

また、SEO（検索エンジン最適化）の手法では、AI検索エンジンの要件に合致していないため、従来のSEO戦略では効果が薄いとされています。AI検索エンジンは、構造化されたコンテンツや短い文節に分断された情報に優れており、従来の長文の記事形式では情報がうまく抽出されない可能性があります。そのため、ウェブサイトのアーキテクチャやコンテンツ構造の再設計が必要とされているとされています。

さらに、AI検索エンジンは、コンテンツの質や信頼性、密度、構造に基づいて情報を選択するため、単なるキーワードの密度ではなく、情報の整合性と信頼性が重要視されています。企業がAI検索エンジンで可視化するためには、これらの要素を意識したコンテンツ制作とサイト構造の見直しが求められているとされています。

## 記事ごとの差分・視点の違い

記事「Por qué el 90% de las webs son invisibles para ChatGPT y Perplexity: Auditoría forense de RAG y WAF」は、AI検索エンジンが多くのウェブサイトを無視する技術的な原因を深掘りしている。WAFやHTTP 403エラーの設定がAIクローラーをブロックしていることが主な焦点で、特にOpenAIやPerplexityのクローラーがアクセスを拒否される現象を具体例として挙げている。また、SEOの限界やRAG（Recuperación Aumentada por Generación）のインフラストラクチャの問題も論じており、ウェブサイトのアーキテクチャやコンテンツ構造の再設計が推奨されている。

記事「Bloquear bots de IA: el error que deja tu web invisible en ChatGPT」は、ウェブサイトがAI検索エンジンに不可視になる理由として、特にWAFやBot Fight Modeの設定が挙げられている。この記事はYouTubeの動画形式で公開されており、視覚的な説明も含めて、ブロックされる仕組みやその影響を簡潔に解説している。ただし、具体的な技術的根拠や解決策については詳しく触れていない。

記事「[ES] Deja de escribir DDL de ClickHouse a mano: Un modelo Pydantic v2 es suficiente」は、ClickHouseとの統合を目的としたPydantic v2のモデルの活用について述べている。この記事は技術的実装に重点を置き、DDLの手動作成を自動化する方法を説明しているが、AI検索エンジンに関する議論は含まれていない。

記事「Un ejemplo práctico de cliente de Python... - ClickHouse Documentation」は、PythonでClickHouseに接続する方法を例示しており、技術的な実装例を提供している。この記事は公式ドキュメントに基づく情報であり、AI検索エンジンとの関連性は見られない。

記事「[ES] Deja de escribir el boilerplate de Kafka a pie: Un decorador es suficiente」は、Kafkaのコンシューマー実装におけるコードの簡素化を目的としており、WKafkaというライブラリの紹介をしている。この記事も技術的実装に焦点を当てており、AI検索エンジンとの関連性は見られない。

## 深掘り調査で得られた知見

AI検索エンジン（ChatGPT、Perplexityなど）が多くのウェブサイトを無視している現象は、技術的な要因が主な原因であることが確認されている。特に、WAF（Web Application Firewall）やHTTP 403エラーの設定が、AIクローラーのアクセスをブロックしている可能性が指摘されている。例えば、CloudflareやAWS WAFなどのファイアウォールツールが、デフォルトでスクラブラーをブロックする設定になっているため、OpenAIやPerplexityのクローラーがアクセスを拒否されるケースが確認されている。これにより、AI検索エンジンがウェブサイトのコンテンツを読み取ることができず、結果として検索結果に表示されない状態になっている。

また、SEO（検索エンジン最適化）の手法がAI検索エンジンの最適化（GEO）には対応しきれていないことも判明。従来のSEOでは、長文のコンテンツやキーワードの密度に重きを置いたが、AI検索エンジンは構造化された情報や短い文節に分断された内容に優れている。そのため、従来のSEO戦略では、AI検索エンジンでの可視化が難しくなっている。このため、ウェブサイトのアーキテクチャやコンテンツ構造の再設計が求められている。

さらに、AI検索エンジンは、コンテンツの質や信頼性、密度、構造に基づいて情報を選択する傾向がある。そのため、企業がAI検索エンジンで可視化するためには、情報の整理や構造化が重要となる。これは、従来の検索エンジンとの違いを反映しており、新たなSEO戦略の必要性を示している。

## 不確実な点・追加確認が必要な点

記事間の食い違いや、資料からは断定できない点を具体的に書くと、以下の通りです。

各記事はテーマに関連しているものの、具体的な背景や原因の説明が不十分な部分があります。例えば、記事1ではWAFやHTTP 403エラーがAI検索エンジンのクローラーをブロックしている可能性があると指摘されていますが、他の記事ではその影響が限定的であると述べる資料もあります。また、AI検索エンジンのクローラーがウェブサイトのコンテンツを読み取る際の具体的な動作や、SEOの最適化に必要な新しいアプローチの詳細については、一貫性が欠けています。さらに、記事5ではKafkaのコンシューマー実装に関する情報が提供されていますが、その内容は他の記事とは関連性が低く、全体のテーマと整合性が取れていない点も確認できます。これらの点から、各記事の内容が一貫していないことや、特定の事実を断定的に述べていないことが明らかです。

## 元記事一覧

- [Porquéel90%delaswebssoninvisiblesparaChatGPT...](https://dev.to/kusiai/por-que-el-90-de-las-webs-son-invisibles-para-chatgpt-y-perplexity-auditoria-forense-de-rag-y-waf-2gbd)
- [Bloquear bots de IA: el errorquedeja tuwebinvisibleenChatGPT...](https://www.youtube.com/watch?v=2gpbqMWnCyI)
- [[ES]DejadeescribirDDLdeClickHouseamano:Unmodelo...](https://dev.to/william_rodriguez_65a5898/es-deja-de-escribir-ddl-de-clickhouse-a-mano-un-modelo-pydantic-v2-es-suficiente-46ch)
- [Un ejemplo práctico de cliente de Python... -ClickHouseDocumentation](https://clickhouse.com/docs/es/resources/support-center/knowledge-base/integrations/python-clickhouse-connect-example)
- [[ES] Deja de escribir el boilerplate de Kafka a pie: Un ...](https://dev.to/william_rodriguez_65a5898/es-deja-de-escribir-el-boilerplate-de-kafka-a-pie-un-decorador-es-suficiente-510)
