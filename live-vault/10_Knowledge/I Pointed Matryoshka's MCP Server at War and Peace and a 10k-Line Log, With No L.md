---
title: Matryoshka MCPサーバーでWar and Peaceを処理する方法
type: knowledge
status: draft
created: 2026-10-15
updated: 2026-10-15
confidence: medium
---

# Matryoshka MCPサーバーでWar and Peaceを処理する方法

## 結論

MatryoshkaのMCPサーバーは、LLMを必要とせず、大規模なテキストファイルを効率的に処理するための新しいアプローチを実現しており、War and Peaceのような大容量データを77万トークン以上処理可能な性能を示しています。この技術は、ゼロネットワークエグレスを実現する開発環境との連携も可能で、今後のAIエージェントやコード生成ツールにおける重要な基盤となる可能性があります。

## テーマ概要

Matryoshka は、Dmitri Sotnikov（yogthos）が開発したオープンソースの TypeScript プロジェクトで、MCP（Model Context Protocol）サーバーを提供し、大規模なテキストファイルを処理するための新しいアプローチを提案しています。このプロジェクトは、通常の LLM（大規模言語モデル）のコンテキストウィンドウを超える大容量ファイルを効率的に処理する方法として注目されています。特に、War and Peace などの大規模なテキストデータを分析する際、LLM の API キーを必要とせず、ローカルで処理可能な MCP サーバーを提供することで、コストやセキュリティ面での課題を解決する可能性があります。また、この技術は、開発者向けのツールや環境でのゼロネットワークエグレス（ネットワーク通信なし）の実現にも寄与しており、現代のソフトウェア開発において重要な役割を果たしています。

## 共通して確認できる点

Matryoshka は、Dmitri Sotnikov（yogthos）によって開発されたオープンソースの TypeScript プロジェクトで、Luminus Clojure フレームワークの作者としても知られている。このプロジェクトは、Recursive Language Models の論文に基づいており、Alex L. Zhang、Tim Kraska、Omar Khattab が MIT CSAIL で執筆した論文を独立して実装したものである。Matryoshka は、MCP サーバー lattice-mcp を提供し、LLM を必要としない仕組みを備えている。この MCP サーバーは、大規模なファイルをサーバー上で保持し、クエリを小規模な S-Expression 言語 Nucleus で処理することで、トークンの使用量を削減するという特徴がある。War and Peace というプロジェクト・ギュンタークのファイルを解析する実験では、3.36 MB のファイルで、66,041 行、566,333 単語、約 770,000 トークン（tiktoken の o200k_base では 769,825 トークン）を処理しており、多くのモデルのコンテキスト・ウィンドウをはるかに超える規模である。Matryoshka は Apache-2.0 ライセンスで公開されており、最新の npm リリースは matryoshka-rlm 0.2.40 で、2026 年 5 月 17 日にリリースされている。テスト環境では、Linux x86_64 系統、8 vCPU、15 GB RAM、Node.js 20.19.2 と pnpm 10.33.4 を使用しており、テストは 2.5 秒で完了し、node_modules は 220 MB に達した。また、npx を使用して lattice-mcp を実行する際には、関連するパッケージがダウンロードされる問題が発生したため、matryoshka-rlm のバイナリを使用することを推奨している。

## 記事ごとの差分・視点の違い

記事「I Pointed Matryoshka's MCP Server at War and Peace and a 10k-Line Log, With No LLM Key」は、MatryoshkaのMCPサーバーがLLMなしで大規模テキストを処理できるという技術的実験を主な焦点としており、特に大規模なテキストファイルを効率的に処理する方法を検証している。対照的に、「Awesome MCP Servers」は、MCPサーバーの種類や用途に焦点を当て、さまざまなAIエージェントやツールとの連携を可能にするサーバーのリストを提供している。また、「MCP.so - MCP Marketplace」は、MCPサーバーのマーケットプレイスとして機能し、ユーザーがサーバーを検索・利用するためのプラットフォームを提供している。一方、「Enforcing Zero Network Egress with Automated Sovereignty Tests」は、開発環境でのネットワーク流出を防ぐための自動テストとセキュリティポリシーの実装に注力し、TokenCapプロジェクトの取り組みを紹介している。最後に、「Air-Gap Mode - Zero Network Egress | Bodega One Code」は、AIコード編集環境でのネットワーク流出防止を目的とした「エアギャップモード」の詳細を説明し、その実装における9つの制限層を強調している。各記事は、それぞれ異なる視点や目的を持ち、MCP技術やネットワークセキュリティの分野における多様な取り組みを示している。

## 深掘り調査で得られた知見

Matryoshka は、Dmitri Sotnikov（yogthos）が開発したオープンソースの TypeScript プロジェクトで、Luminus Clojure フレームワークの著者としても知られている。このプロジェクトは、MCP（Model Context Protocol）サーバーとして機能し、LLM（大規模言語モデル）を必要とせず、大容量のファイルを処理するためのアプローチを提供している。特に、War and Peace のような大規模なテキストファイルを分析する際、LLM のコンテキストウィンドウを超えるデータを効率的に処理する手段として注目されている。このテストでは、Matryoshka の MCP サーバーが、3.36 MB で 66,041 行ある War and Peace を処理し、トークンの使用量を大幅に削減するという主張がされている。ただし、この結果は著者がベンチマークしていないため、信頼性については注意が必要である。また、テスト環境では Linux x86_64 システムを使用し、Node.js 20.19.2 と pnpm 10.33.4 が使われていた。Matryoshka は Apache-2.0 ライセンスで配布されており、最新の npm リリースは 2026 年 5 月 17 日に matryoshka-rlm 0.2.40 が公開されている。プロジェクトは、Lattice エンジンによって Nucleus という S-expression 言語を用いたクエリ処理をサポートしており、結果は SQLite で一時的に保存される。このように、Matryoshka は大規模なデータを処理するための新しいアプローチとして注目されている。

## 不確実な点・追加確認が必要な点

記事間の食い違いや、資料からは断定できない点を具体的に書くと、以下の通りです。

MatryoshkaのMCPサーバーに関する記事（記事1）では、War and Peaceのテキストファイルを処理する際、LLMのAPIキーを必要とせず、ローカルで動作するMCPサーバーを使用したテストが行われています。このテストでは、NucleusというS-expression言語を用いてクエリを実行し、結果をサーバー側で保持してクライアントにハンドルを返す仕組みが説明されています。ただし、このテスト結果のトークン節約率（97%以上、80%以上）はプロジェクト側の主張であり、著者がベンチマークを実施していない点が明記されています。

一方、他の記事（記事2、記事3）では、MCPサーバーの市場や選定ガイドについて紹介されており、MatryoshkaのMCPサーバーがその中で一つの選択肢として挙げられています。ただし、これらの記事はMatryoshkaの技術的詳細や実装について述べるものではなく、一般的なMCPサーバーの利用方法や比較情報に焦点を当てています。

また、記事4と記事5では、ゼロネットワークエグレスを実現するための設計原則や、Air-Gapモードの実装について説明されており、これらはMatryoshkaのMCPサーバーとは直接関係ありませんが、開発環境におけるネットワーク制限の重要性を示す背景情報として参考になります。これらの記事では、MatryoshkaのMCPサーバーがゼロネットワークエグレスを実現しているかどうかは触れていません。したがって、MatryoshkaのMCPサーバーがゼロネットワークエグレスを達成しているという主張は、記事1の内容に限られます。

さらに、記事1の実験環境では、Node.jsとpnpmが使用されており、特定のバージョン（Node 20.19.2、pnpm 10.33.4）が記録されています。ただし、これらの環境設定が他の記事の情報と整合性を保っているかどうかは明記されていません。また、記事1では、MCPサーバーの使用に際して、npxコマンドでlattice-mcpを実行する際の問題が報告されており、その対処法としてmatryoshka-rlmのバイナリを使用することを推奨しています。この情報は、Matryoshkaプロジェクトの実装や利用方法に関する具体的な手順を示していますが、他の記事ではこのような実装詳細が扱われていません。

## 元記事一覧

- [IPointedMatryoshka'sMCPServeratWarandPeaceand...](https://dev.to/ishank-dev/i-pointed-matryoshkas-mcp-server-at-war-and-peace-and-a-10k-line-log-with-no-llm-key-4f9g)
- [AwesomeMCPServers](https://mcpservers.org/)
- [MCP.so -MCPMarketplace](https://mcp.so/)
- [EnforcingZeroNetworkEgresswithAutomatedSovereigntyTests](https://dev.to/vansharora21/enforcing-zero-network-egress-with-automated-sovereignty-tests-g91)
- [Air-Gap Mode -ZeroNetworkEgress| Bodega One Code](https://www.bodegaone.ai/air-gap)
