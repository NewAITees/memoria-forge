---
title: ローカルSLMによる閉ループAIエージェントの設計とMCP活用
type: knowledge
status: draft
created: 2026-09-19
updated: 2026-09-19
confidence: medium
---

# ローカルSLMによる閉ループAIエージェントの設計とMCP活用

## 結論

小規模言語モデル（SLM）をローカルで実行し、業務データに接続する際には、決定的なPythonコードによる検証が数学的誤りや帳簿の虚偽を防止するための不可欠な要素である。このアプローチは、人間のフィードバックを連続的に学習する仕組みと組み合わせることで、信頼性と正確性を担保したAIエージェントの設計が可能となる。また、Model Context Protocol（MCP）を活用した外部システムとの連携は、コンテキストの衛生性を高め、AIアプリケーションの効率性と信頼性を向上させる重要な技術的基盤を提供している。

## テーマ概要

このテーマは、ローカルで実行される小規模言語モデル（SLM）を用いた閉ループAIエージェントの設計と、その信頼性向上のための技術的アプローチを扱っている。特に、Llama 3.2 3BなどのSLMをローカルで動作させ、業務データに接続する際の数学的誤りや帳簿の虚偽を防止するための決定的なPythonコードによる検証、トリステートゲートウェイ、QWK（二次的加重カッパ）による評価校正、および人間からのフィードバックを連続的に学習する仕組みが注目されている。このような設計は、プライバシーの確保とコスト効率を重視しながら、信頼性と正確性を担保するAIエージェントの実現を目指しており、特に敏感な業務プロセスでの利用が期待されている。

## 共通して確認できる点

複数の記事から共通して確認できた事実として、ローカルで実行される小規模言語モデル（SLM）を用いたAIエージェントの設計において、数学的誤りや帳簿の虚偽を防ぐための決定的なPythonコードによる検証が重要であることが明確に示されている。Llama 3.2 3BなどのSLMは、プライバシーを確保しながら高速で動作するが、実際の業務データに接続されると誤った情報を生成する可能性がある。この問題を解決するためには、生成内容を検証する仕組みを導入し、人間のフィードバックを連続的に学習する設計が求められている。また、Model Context Protocol（MCP）は、AIアプリケーションが外部システムと接続するためのオープンソース標準であり、リソースやプロンプトをオンデマンドで取得する仕組みを提供し、コンテキストの衛生性を高める。さらに、Agentic Tool-Useアーキテクチャは、LLMがツールを呼び出す際のJSON形式のステップ定義に基づき、バックエンドがツールを実行し結果をコンテキストに注入する仕組みを備えており、リアルタイムデータを取得するためのMVPとしての実装が示されている。

## 記事ごとの差分・視点の違い

記事「Beyond Vibes: Architecting Closed-Loop AI Agents with Local SLMs, Deterministic Evals, and Human Learning Loops」は、ローカルで実行される小規模言語モデル（SLM）を用いた閉ループAIエージェントの設計に焦点を当てている。特に、数学的誤りや帳簿の虚偽を防ぐための決定的なPythonコードによる検証や、人間のフィードバックを連続的に学習する仕組みを強調している。  

記事「GitHub - AkshatSoni26/closed-loop-slm-agent: Production-grade...」は、実際のコードベースとアーキテクチャの詳細を提供しており、エージェントが生成した drafts を検証し、人間の決定を学習して改善する仕組みを具体的に示している。また、コードの実行環境や必要なライブラリ、設定方法についても明記している。  

記事「Teaching an LLM to pull MCP Resources and Prompts on demand...」は、Model Context Protocol (MCP) を用いたリソースやプロンプトのオンデマンド取得方法を説明し、LLMが必要な情報を選択的に取得する仕組みを提案している。これにより、コンテキストの肥大化や無駄なデータの包含を防ぐという点で、MCP の利点を強調している。  

記事「What is the Model Context Protocol (MCP)? - ModelContextProtocol」は、MCP そのものの概要と、AI アプリケーションが外部システムと連携するための3つの機能（tools, resources, prompts）を説明している。この記事は MCP の基本的な概念を提供し、他の記事で述べられている技術的詳細を補完する役割を果たしている。  

記事「Building an MVP Agentic Tool-Use Bot with Node.js and...」は、Node.js と OpenRouter を用いたリアルタイム天気データ取得のための MVP アーキテクチャを示しており、LLM がツールを呼び出す仕組みや、バックエンドでの処理フローについて説明している。この記事は、Agentic Tool-Use アーキテクチャの概念的なデモンストレーションとして位置付けられている。

## 深掘り調査で得られた知見

小規模言語モデル（SLM）をローカルで実行し、業務データに接続する際の信頼性と正確性を確保するためには、決定的なPythonコードによる検証が不可欠である。Llama 3.2 3Bのようなモデルは、プライバシーを確保しながら高速で動作するが、実際の業務データに接続されると、数学的誤りや帳簿の虚偽を生成する可能性がある。この問題を解決するためには、生成内容を検証する仕組みを導入し、統計的評価の一致や長さバイアスの検証を行う必要がある。また、人間のフィードバックを連続的に学習する仕組みを導入することで、エージェントの改善を実現する。このような設計により、SLMをローカルで実行し、業務データに接続する際の信頼性と正確性を確保することが可能になる。さらに、Model Context Protocol（MCP）を活用した外部システムとの連携が可能となり、AIアプリケーションがデータソースやツールにアクセスする際の効率性と信頼性が向上している。また、Agentic Tool-Useアーキテクチャを採用したMausam AIのようなプロジェクトも、リアルタイムデータを取得し、ユーザーに提供するための新しいアプローチを示している。

## 不確実な点・追加確認が必要な点

記事間の食い違いや、資料からは断定できない点を具体的に述べると、以下の通りです。  

まず、記事1と記事2は同作者によるものであり、記事1ではLlama 3.2 3Bをローカルで実行し、業務データに接続する際の数学的誤りや帳簿の虚偽を生成する可能性を指摘しています。記事2では、その問題を解決するためのローカルファーストのアーキテクチャが提案されており、人間のフィードバックを連続的に学習する仕組みが導入されています。しかし、記事2の公開日時や取得日時が不明なため、これらの技術がどの時点で実装されたかは明確ではありません。  

記事3では、Model Context Protocol (MCP)を活用したLLMのリソースやプロンプトのオンデマンド取得方法が説明されています。MCPは、LLMが外部システムと接続するためのオープンソース標準であり、リソースやプロンプトを合成し、自動承認されたLLMツールとして扱うことで、コンテキストの肥大化を防ぐことが目的です。ただし、記事4のMCP公式サイトでは、具体的な実装例や技術的な詳細が提示されておらず、記事3の内容がMCPの公式ドキュメントと一致しているかは不明です。  

記事5では、Node.jsとOpenRouterを用いたMVPアーキテクチャが紹介されており、リアルタイムの天気情報を取得する例が挙げられています。ただし、この記事はMVPとしての概念的なデモンストレーションであり、プロダクション用のアプリケーションにはなっていません。また、記事5の実装はOpenRouterを介して数百のAIモデルにアクセス可能であることが述べられていますが、具体的なモデルやその選定基準については記述がありません。  

以上のように、各記事が提示する技術や実装は、それぞれの文脈や目的に応じて異なり、一部の技術や実装の詳細については資料からは断定できません。また、記事間の時系列的関係や実装の進化についても、公開日時や取得日時の情報が不明なため、明確な結論は導き出すことができません。

## 元記事一覧

- [Beyond Vibes: ArchitectingClosed-LoopAIAgentswithLocalSLMs...](https://dev.to/akshatsoni26/beyond-vibes-architecting-closed-loop-ai-agents-with-local-slms-deterministic-evals-and-human-3kkf)
- [GitHub - AkshatSoni26/closed-loop-slm-agent: Production-grade...](https://github.com/AkshatSoni26/closed-loop-slm-agent)
- [TeachinganLLMtopullMCPResourcesandPromptson demand...](https://dev.to/anirbaan_chowdhury_58a600/teaching-an-llm-to-pull-mcp-resources-and-prompts-on-demand-instead-of-drowning-it-in-context-591l)
- [What is the ModelContextProtocol (MCP)? - ModelContextProtocol](https://modelcontextprotocol.io/)
- [BuildinganMVPAgenticTool-UseBotwithNode.jsand...](https://dev.to/ankit_halder_7840b622b962/building-an-mvp-ai-weather-agent-with-nodejs-and-openrouter-49eg)
