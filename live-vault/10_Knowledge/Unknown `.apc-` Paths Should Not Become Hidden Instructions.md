---
title: 未知の.apc/パスが隠し指示にならないように
type: knowledge
status: draft
created: 2026-09-28
updated: 2026-09-28
confidence: medium
---

# 未知の.apc/パスが隠し指示にならないように

## 結論

APC（Agent Project Context）のフォルダ構造に関する仕様では、未知の `.apc/` パスは消費者によって無視されることが明記されており、これによりチームが実験的なファイルを自由に作成できる環境が提供されている。しかし、未知のパスが誤ってプロジェクトのポリシーとして扱われることを防ぐため、明示的な定義が必要であり、APC パスの使用に関する具体的なガイドラインは不足している。また、APC と MCP（Model Context Protocol）の関連性や、コンフォーマンス検証ツールの開発が進む中、APC の役割とセキュリティ確保が今後の技術動向でさらに注目される。

## テーマ概要

APC（Agent Project Context）に関する「Unknown `.apc/` Paths Should Not Become Hidden Instructions」は、プロジェクトのコンテキストを共有するための portable context layer としての APC の仕様に関する重要な議論を示しています。APC フォルダ構造の仕様では、消費者が未知の `.apc/` パスを無視するよう規定されており、これによりチームが実験を行う自由を確保しています。しかし、未知のパスが誤ってプロジェクトのポリシーとして扱われるリスクがあり、その回避が求められています。このテーマは、APC と APX（Agent Project eXecution）の役割、APC パスの定義方法、および未知のパスの扱いに関するガイドラインの明確化が求められている点に注目しています。APC の仕様が今注目されている理由は、MCP（Model Context Protocol）との連携や、セキュリティ、コンフォーマンス、レジリエンスの観点からの検証ツールの開発が進んでいるためです。これらのツールや仕様の進展により、APC と MCP の相互運用性やセキュリティ確保がより重要になっており、その議論が注目されています。

## 共通して確認できる点

APC（Agent Project Context）のフォルダ構造に関する仕様では、消費者が未知の `.apc/` パスを無視するよう規定されており、これはチームが実験を行うための自由を提供する。この仕様により、`.apc/` フォルダ内に存在するファイルが必ずしも APC 合約に含まれる必要はなく、明示的な拡張によって定義されていない限り、消費者はそのファイルを無視するべきである。APC は、AGENTS.md および定義された `.apc/` パスを介して、互換性のあるツール間でプロジェクト所有のコンテキストを共有する。一方で、未知の `.apc/` パスの扱いに関する明確なガイドラインが存在しないことから、チームは慎重に `.apc/` フォルダ内のファイルの意味を定義し、未知のパスを無視する必要がある。また、APC パスの定義に関する具体的な例が不足しており、実際の運用における曖昧さが生じる可能性がある。

## 記事ごとの差分・視点の違い

記事「Unknown `.apc/` Paths Should Not Become Hidden Instructions」では、APCフォルダ構造の仕様について説明し、未知のパスが消費者に無視されるべきであると述べている。一方、「Built an open-source MCP Conformance Scanner」では、MCPサーバーのコンフォーマンス検証を自動化するツールの開発について語り、開発者向けの無料ツールとしての価値を強調している。また、「GitHub - kogtug/Crucible: An open-source MCP conformance and ...」では、MCPの新しい仕様に応じたコンフォーマンステストとレジリエンステストを実施するツールの機能と設計について説明している。さらに、「TheCloudflareKVracethatbrokeourMCPOAuthatrandom(and...)」では、Cloudflare KVの競合状態を回避するための実際の問題とその解決策について述べており、OAuthフローにおけるセキュリティ上の課題を具体的に提示している。一方、「Unknown`.apc/`PathsShouldNotBecomeHiddenInstructions」では、APCフォルダ構造の仕様と未知のパスの扱いについて再び強調し、実際の運用における曖昧さを指摘している。

## 深掘り調査で得られた知見

APC（Agent Project Context）に関する議論では、.apc/ フォルダ内に存在するファイルが自動的にAPC契約に含まれるわけではないという明確なガイドラインが示されている。APCフォルダ構造の仕様では、消費者が未知のパスを無視するよう規定されており、これはチームが実験を行う自由を確保するための設計である。このルールにより、チームはローカルのファイルをすべてのエージェントの指示として扱う必要がないため、柔軟な開発が可能となる。しかし、未知のパスが誤ってプロジェクトポリシーとして扱われてしまうリスクを防ぐため、明示的な定義が必要である。APCの契約はAGENTS.mdや定義された.apc/パスを通じて、互換性のあるツール間でプロジェクトのコンテキストを共有する。APX（Agent Project eXecution）は、APC契約を読み取り、実行状態を保持するランタイムおよびツールインフラストラクチャを提供する。

一方で、MCP（Model Context Protocol）に関する技術動向では、コンフォーマンス検証ツールの開発が進んでいる。MCP Conformance Scannerは、MCPサーバーの仕様書に基づいたテストを自動化し、セキュリティやマルチモデル互換性などの指標でスコアを算出するオープンソースツールである。Crucibleは、MCPの新しい仕様に応じたコンフォーマンステストとレジリエンステストを実施し、サーバーの動作を検証する。MCPの仕様変更に伴い、既存のツールが新しい機能を正しく実装しているかの検証が求められており、Crucibleはそのギャップを埋める役割を果たしている。

また、MCPのセキュリティに関する実例として、Cloudflare KVの競合状態がOAuthフローに影響を与える問題が報告されている。この問題では、OAuthリクエストの投稿とコールバックの読み取りが異なるエッジロケーションで行われることで、KVの最終的な整合性が保証されず、ランダムな失敗が発生した。その解決策として、コールバックでの読み取りを廃止し、投稿時にOAuthリクエストを完了するようにした。この対応により、ランダムな失敗が解消された。このケースは、MCPにおけるセキュリティと信頼性の重要性を再認識させる事例として注目されている。

## 不確実な点・追加確認が必要な点

記事間での情報の整合性を確認すると、APCフォルダ構造に関する説明は複数の記事で共有されており、基本的なルールは一貫している。しかし、具体的な実装例やAPCパスの使用に関する明確なガイドラインについては、どの記事にも詳細な記述が見られず、実際の運用における曖昧さが生じる可能性がある。また、APCとMCPの関連性については、APCがMCPの一部として機能している可能性があるが、明確な説明は見られない。さらに、MCPコンフォーマンス検証ツールの開発背景や、Crucibleの最終仕様確定日（2026年7月28日）については、記事3と記事4の情報が一致しているが、その他の詳細な情報は確認されていない。また、Cloudflare KVの競合状態に関する問題は、記事5で具体的な解決策が示されているが、その背景にある技術的な要因については、他の記事では触れられていない。

## 元記事一覧

- [Unknown `.apc/` Paths Should Not Become Hidden Instructions](https://dev.to/agentprojectcontext/unknown-apc-paths-should-not-become-hidden-instructions-2d36)
- [Unknown`.apc/`PathsShouldNotBecomeHiddenInstructions](https://tsecurity.de/de/4160314/sichere-programmierung/unknown-apc-paths-should-not-become-hidden-instructions/)
- [Built an open-source MCP Conformance Scanner - DEV Community](https://dev.to/ak1ng/built-an-open-source-mcp-conformance-scanner-7op)
- [GitHub - kogtug/Crucible: An open-source MCP conformance and ...](https://github.com/kogtug/Crucible)
- [TheCloudflareKVracethatbrokeourMCPOAuthatrandom(and...)](https://dev.to/anthony_builds/the-cloudflare-kv-race-that-broke-our-mcp-oauth-at-random-and-how-we-killed-it-a1g)
