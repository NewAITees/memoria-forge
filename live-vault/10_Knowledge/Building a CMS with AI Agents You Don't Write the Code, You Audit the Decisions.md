---
title: AIエージェントでCMSを開発する仕組みとその課題
type: knowledge
status: draft
created: 2026-09-16
updated: 2026-09-16
confidence: medium
---

# AIエージェントでCMSを開発する仕組みとその課題

## 結論

AIを活用したCMS開発において、開発者の役割はコードの作成からコードの監査へと移行し、AIエージェントが生成したコードの品質をリアルタイムで確認することが不可欠である。このプロセスは、セキュリティリスクやパフォーマンスの問題を事前に検出・修正するためのガバナンスと透明性を重視しており、人間とAIの協働が今後のCMSの進化において中心的な役割を果たす。

## テーマ概要

AIを活用したCMS（コンテンツ管理システム）の構築が注目を集めている。このアプローチでは、開発者自身がコードを書くのではなく、AIエージェントにタスクを任せ、その決定を監査するという新しい開発スタイルが提案されている。具体的には、AIエージェントがコード変更を生成し、KanbanボードやGitサーバーなどを通じてレビューが行われる。これにより、セキュリティ上の脆弱性や不正確な権限チェックなどの問題を事前に検出できるようになる。また、agentic CMSは、SEO最適化やコンテンツ翻訳、コンプライアンスチェックなどの繰り返し作業を自動化し、開発効率を向上させる。このようなAIエージェントの導入は、コンテンツの管理からコンテンツの知能への移行を促進し、人間とAIの協働が重要な役割を果たしている。このテーマは、AI技術の進化に伴い、CMS開発における新たなワークフローとガバナンスの必要性を問う点で注目されている。

## 共通して確認できる点

AI agents are being integrated into content management systems (CMS) to automate repetitive tasks such as SEO optimization, content translation, and compliance checks. This shift allows developers to transition from code writers to code reviewers, focusing on auditing and ensuring the security and correctness of AI-generated code. The use of tools like Kanban boards (Kanboard), Git servers (Gitea), and an MCP orchestrator (Marcus) enables real-time review of code changes before they are merged into the main branch. This approach helps identify critical issues such as weak session stores, incorrect permission checks, and XSS vulnerabilities during the development process. Agentic CMS platforms emphasize structured content models, APIs, and governance frameworks to maintain consistency, security, and scalability. The integration of AI into CMS platforms is shifting the focus from content storage to content intelligence, enabling autonomous workflows and human-AI collaboration. However, challenges remain in inter-agent communication, particularly in parallel sessions, where issues like message provenance and security risks such as prompt injection attacks need to be addressed through reliable communication channels and governance mechanisms.

## 記事ごとの差分・視点の違い

記事1は「You Don't Write the Code, You Audit the Decisions」というテーマで、AIアーキテクトがCMSを構築するプロセスを描き、開発者としての役割がコードのレビューへと移行することを強調しています。具体的には、KanbanボードとGitサーバーを用いたAIエージェントの協働環境を紹介し、コード変更のレビューがセキュリティやパフォーマンスの確保において重要であることを示しています。  
記事2は「What is an agentic CMS?」というタイトルで、CMSにおけるAIエージェントの役割とその意義を定義しています。特に、AIがコンテンツ操作の繰り返し作業を自動化し、人間とAIの協働を可能にする点を強調し、企業におけるガバナンスとコンプライアンスの重要性にも言及しています。  
記事3は「How parallel AI agents should talk to each other」というタイトルで、複数のAIエージェントが並行して動作する際の通信問題に焦点を当てています。人間による中継がもたらすプロヴァイエンスの喪失や、プロンプトインジェクションのリスクを指摘し、信頼性のある通信プロトコルの必要性を論じています。  
記事4は「My AI Agents Talk to Each Other. Here's the Inter-Agent Communication Protocol」というタイトルで、AIエージェント間の通信プロトコルの設計と実装について述べています。特に、メッセージの送受信に際してのプロヴァイエンス検証や、メッセージの状態管理を重視しており、通信の信頼性向上を目指した実装例を紹介しています。  
記事5は「How to Prompt Coding Agents Without Losing Control of Your Codebase」というタイトルで、コードベースを制御しながらAIエージェントに指示を出す方法について説明しています。コードベースの制御を維持するためのプロンプト設計や、エージェントの行動を監視・制限する仕組みについて論じており、開発者とAIエージェントの協働におけるバランスを重視しています。

## 深掘り調査で得られた知見

AIを活用したCMS（コンテンツ管理システム）の開発において、開発者自身がコードを書くのではなく、AIエージェントが生成したコードを監査するという新しいワークフローが注目されています。このアプローチでは、Kanbanボード（Kanboard）やGitサーバー（Gitea）を活用し、MCPオーケストレータ（Marcus）を介してAIエージェントがタスクを処理します。生成されたコードの変更点をリアルタイムで確認し、セッションストアの脆弱性や権限チェックの誤り、XSSのリスクなど、重要な決定を監査する必要があります。このプロセスにより、コードがマスターブランチにマージされる前に、セキュリティやパフォーマンスの問題を修正できるようになります。

また、agentic CMSは、AIエージェントがコンテンツのSEO最適化、翻訳、コンプライアンスチェックなどの繰り返し作業を自動化することで、従来の手動作業に代わる効率的なワークフローを実現しています。しかし、AIエージェントが生成するコンテンツの品質を保つためには、ガバナンスフレームワークや構造化されたコンテンツモデル、APIの統合が不可欠です。これにより、一貫性、セキュリティ、拡張性が確保されます。

一方で、複数のAIエージェントが並行して動作する際の通信問題も指摘されています。人間を介したメッセージ転送は、メッセージの出所を確認できず、プロンプトインジェクション攻撃と似たリスクを生じる可能性があります。これを解決するためには、コミットされたアーティファクトへの参照を送信し、メッセージの信頼性を検証する仕組みが必要です。また、メッセージのステータス管理や、各エージェントが自身のメールボックスを特定するための命名規則も重要です。これらの技術的工夫により、AIエージェント同士の信頼性ある通信が実現されています。

## 不確実な点・追加確認が必要な点

記事間では、AIアーキテクチャにおけるCMSの開発プロセスにおける役割分担や、AIエージェントのコミュニケーションメカニズムに関するいくつかの違いが確認されている。例えば、記事1では、AIエージェントがコードを生成し、人間がそのコードをレビューし、最終的にマージするプロセスが強調されている。一方で、記事2では、agentic CMSの概念として、AIエージェントが自動的にSEO最適化や翻訳、コンプライアンスチェックなどのタスクを実行する仕組みが説明されている。これらは、CMSの開発におけるAIエージェントの役割を異なる角度から捉えている。

また、記事3と記事4では、AIエージェント同士のコミュニケーションにおける課題とその解決策が論じられている。記事3では、人間による中継が失敗する理由として、情報の出所が不明瞭であることや、プロンプトインジェクション攻撃に似たリスクがあることが指摘されている。一方で、記事4では、メッセージの参照先をコミットされたアーティファクトにすることで、情報の信頼性を確保する方法が提案されている。これらの議論は、AIエージェント同士の通信において、信頼性と効率性を確保するための技術的アプローチの違いを示している。

さらに、記事5では、コードベースを制御しながらAIエージェントを操作する方法が提案されており、これはAIエージェントの動作を人間がより直接的に制御するためのアプローチである。これに対して、記事1や記事2では、AIエージェントの動作を監視・レビューするためのプロセスが重視されている。これらの違いは、AIエージェントの導入によって開発プロセスがどのように変化するかを示す重要なポイントである。

## 元記事一覧

- [Building a CMS with AI Agents: You Don't Write the Code, You Audit the Decisions - DEV Community](https://dev.to/aak/building-a-cms-with-ai-agents-you-dont-write-the-code-you-audit-the-decisions-535m)
- [What is an agentic CMS? Definition, benefits, and why it matters | Hygraph](https://hygraph.com/blog/agentic-cms)
- [How parallel AI agents should talk to each other (and the bug that proved it) - DEV Community](https://dev.to/ahmadammar/how-parallel-ai-agents-should-talk-to-each-other-and-the-bug-that-proved-it-2mh1)
- [My AI Agents Talk to Each Other. Here's the Inter-Agent Communication Protocol - DEV Community](https://dev.to/setas/my-ai-agents-talk-to-each-other-heres-the-inter-agent-communication-protocol-36j3)
- [How to Prompt Coding Agents Without Losing Control of Your ...](https://dev.to/aicodesmart/how-to-prompt-coding-agents-without-losing-control-of-your-codebase-1afi)
