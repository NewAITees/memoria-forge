---
title: アジャェント開発の進化とブラウザエージェントの課題
type: knowledge
status: draft
created: 2026-10-11
updated: 2026-10-11
confidence: medium
---

# アジャェント開発の進化とブラウザエージェントの課題

## 結論

Agentic coding は、開発プロセスにおける実装コストを大幅に削減し、設計やアーキテクチャに焦点を移す新たな開発スタイルとして確立しつつあるが、ブラウザエージェントの信頼性向上にはセマンティックレイヤーの導入が不可欠であり、現代のSPAが機械解析に不向きな構造を採用しているため、その課題は今後も継続的に取り組まれる必要がある。

## テーマ概要

Agentic coding（エージェント型コーディング）は、AIを活用した開発手法として、近年急速に注目を集めている。このアプローチでは、AIエージェントがコードの実装、テスト、修正などの作業を自動化し、開発者は設計やアーキテクチャの決定、検証といった戦略的な役割に専念する。2年前からこの手法を実践している開発者によると、実装のコストが大幅に低下し、開発プロセス全体が設計段階にシフトしている。しかし、生成されたコードの品質やセキュリティに関する懸念も指摘されており、コードレビューにおいてもテストの精度向上が求められている。また、ブラウザエージェントの活用においては、現代のSPA（シングルページアプリケーション）が機械が理解しにくいDOM構造を採用しているため、セマンティックレイヤーの導入が不可欠であることが明確にされている。このような背景から、agentic codingは開発の効率化と信頼性向上を目的とした新たな技術革新として注目されている。

## 共通して確認できる点

Agentic coding has significantly shifted the focus of software development from direct code implementation to higher-level design and orchestration. Developers now spend more time on strategic decisions, such as defining the intent, methodology, architecture, and verification of the system, while AI agents handle the actual implementation. This transition has made the implementation phase much more efficient, as agents can generate code based on high-level descriptions, reducing the manual effort required. However, this shift also introduces new challenges, such as ensuring the quality and security of generated code, which requires increased oversight and review processes. 

Despite these changes, the core principles of software engineering remain essential. Developers must still understand the design, how components fit together, and potential issues that may arise as the system scales. The role of the developer is evolving from being a code writer to a system architect and overseer, with a greater emphasis on decision-making and quality control. While agentic coding is not a completely new programming paradigm, it represents a shift in the development stack, similar to how C++ evolved from assembly language. 

At the same time, browser agents face significant challenges in production environments due to the structure of modern web applications. These applications are optimized for human users, with DOM structures that are deeply nested and use auto-generated class names, making it difficult for machine parsers to reliably interpret and interact with the page. Without semantic layers that provide a deterministic contract between the frontend and AI agents, browser agents often fail due to issues like coordinate drift, DOM restructuring, and timing mismatches. These problems highlight the need for more robust architectural solutions and the integration of semantic attributes to improve the reliability and precision of AI-driven interactions.

## 記事ごとの差分・視点の違い

記事「What Two Years of Agentic Coding Changed for Me」では、アジェンティックコーディングが導入されてからの2年間で、開発プロセスにおける役割の移行が強調されている。具体的には、実装作業がAIエージェントに委譲され、開発者は設計やアーキテクチャに注力するようになった点が中心となる。また、コードのレビューも従来と同様だが、テストの重要性が高まっていると述べられている。この記事では、アジェンティックコーディングが新たなプログラミング方法ではなく、スタックの上位に移動した開発スタイルとして捉えられている。

記事「Agentic Coding: What It Is and Why It Still Needs You [2026]」では、AIがコードを生成し、テストを行う一方で、開発者が意図や方法論、アーキテクチャ、検証を決定する役割を担うことが強調されている。この記事は、AIが実装を担うが、人間の判断が不可欠であると指摘し、AIが決定するべきではない分野を明確にしている。また、AIが生成したコードの品質やセキュリティについての懸念も触れている。

記事「Why Browser Agents Fail in Production Without Semantic Layers」では、ブラウザエージェントが生産環境で失敗する理由として、現代のウェブアプリケーションが人間向けに最適化されたDOM構造を採用していることが挙げられている。この構造は機械が理解するためのセマンティック情報を削減しており、エージェントがDOMの変化やCSSハッシュの変化に適応できない原因となっている。この記事では、セマンティックレイヤーの導入がエージェントの信頼性と再現性を高める鍵であると強調している。

記事「BrowserAgentsinProduction: The DOM Fragility Tax」では、ブラウザエージェントが生産環境で失敗する理由として、DOMの脆弱性が原因であることが指摘されている。特に、DOMの構造が動的に変化するため、エージェントがクリック位置を正確に把握できず、意図しない操作が発生する可能性がある。また、エージェントが複数ステップのタスクを実行する際、コンテキストの劣化により目標がずれる可能性があると述べられている。この記事では、エージェントの信頼性を高めるためには、セマンティックレイヤーの導入が不可欠であると結論付けている。

## 深掘り調査で得られた知見

深掘り調査によって明らかになった知見は、アジェンティックコーディングの導入がソフトウェア開発のプロセスを根本的に変化させているという点である。従来は実装に多くの時間を費やしていた開発作業は、アジェンティックエージェントによって高レベルの指示からコードを生成するようになり、実装コストが大幅に削減されている。これにより、開発者は設計やアーキテクチャの構築に注力できるようになった。しかし、生成されたコードの品質やセキュリティ面での課題も指摘されており、コードレビューではテストの冗長性に注意を払う必要がある。また、アジェンティックコーディングは新たなプログラミングスタイルではなく、スタックの上位に移動した新たな開発アプローチと捉えられる。

一方、ブラウザエージェントの導入においては、現代のウェブアプリケーションが人間向けに最適化されたDOM構造を採用しているため、機械が理解するためのセマンティック情報を提供していないという課題が浮き彫りになった。これにより、エージェントがDOMの変更やCSSハッシュの変化に適応できず、動作が不安定になるケースが報告されている。セマンティックレイヤーの導入によって、エージェントがウェブアプリケーションを正確に操作できるようになり、信頼性が向上する。しかし、DOMの脆弱性による「DOM Fragility Tax」と呼ばれる課題も存在し、生産環境での運用にはさらなる工夫が必要である。具体的には、座標のずれやレイアウトの変化によってクリック位置がずれ、意図しない操作が発生する可能性がある。また、エージェントが複数ステップのタスクを実行する際、コンテキストの劣化により目標がずれる問題も確認されている。これらの課題は、アジェンティックコーディングやブラウザエージェントの信頼性と安全性に深刻な影響を及ぼしており、今後の開発においてはセマンティックレイヤーの導入やアーキテクチャの改善が求められている。

## 不確実な点・追加確認が必要な点

Agentic coding は、開発プロセスにおいて実装のコストを削減し、設計やアーキテクチャに焦点を移すように変化させている。しかし、この変化は完全な新しいプログラミング方法ではなく、プログラミングスタックの上位に移動した形態と捉えられる。一方で、ブラウザエージェントは、現代のSPA（シングルページアプリケーション）のDOM構造が機械解析に不向きであるため、生産環境で信頼性の高い動作を保証することが難しい。特に、DOMの変化やCSSハッシュの自動生成により、エージェントが意図した要素を正確に識別できず、操作ミスや不正確な実行が生じる可能性がある。このような課題に対処するためには、セマンティックレイヤーの導入が求められており、明示的なセマンティック属性（例：data-agent）を提供することで、エージェントの信頼性と再現性を向上させることが可能である。ただし、セマンティックレイヤーの導入に伴うコストや、アーキテクチャの選択がエージェントの成功に与える影響については、資料間で一貫性が見られない。また、エージェントが状態を正確に把握せず、進捗を完成と誤認してしまった場合、誤った行動を取る可能性がある。これらの問題は、生産環境でのブラウザエージェントの信頼性と安全性を脅かしており、今後はアーキテクチャの改善とセマンティックレイヤーの導入が不可欠である。

## 元記事一覧

- [What Two Years of Agentic Coding Changed for Me](https://dev.to/mark_kolodkin_4b39d571d41/what-two-years-of-agentic-coding-changed-for-me-2lao)
- [Agentic Coding: What It Is and Why It Still Needs You [2026]](https://app.stationx.net/articles/agentic-coding)
- [Why Browser Agents Fail in Production Without Semantic Layers](https://dev.to/parvejshah/why-browser-agents-fail-in-production-without-semantic-layers-35hk)
- [Why Browser Agents Fail in Production Without Semantic Layers](https://aiwithghost.com/news/news-why-browser-agents-fail-in-production-without-semantic-layers-1/)
- [BrowserAgentsinProduction: The DOM Fragility Tax](https://tianpan.co/blog/2026/04/19/browser-agents-dom-fragility-production)
