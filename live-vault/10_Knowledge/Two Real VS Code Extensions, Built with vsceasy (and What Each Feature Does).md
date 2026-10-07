---
title: vsceasyを活用したVS Code拡張の実例と機能解説
type: knowledge
status: draft
created: 2026-10-07
updated: 2026-10-07
confidence: medium
---

# vsceasyを活用したVS Code拡張の実例と機能解説

## 結論

vsceasyはVS Code拡張の開発を効率化するCLIとフレームワークであり、React webview、typed RPC橋、ファイルベースのルーティングなどの機能を提供し、拡張機能の構築を自動化しています。このツールを活用した実際の拡張機能の例として、MangaBarやDevGotchiが挙げられ、それぞれのユニークな機能や実装方法が紹介されています。これらの拡張機能は、VS Codeの柔軟性と拡張性を活かした新たな可能性を示しており、開発者にとってのツールとしての地位をさらに強化しています。

## テーマ概要

VS Code拡張の開発を簡素化するツールとして注目されているvsceasyは、React webview、typed RPC橋、ファイルベースのルーティングなどの機能を提供し、拡張機能の構築を自動化します。このツールを活用して作成された2つの実際のVS Code拡張機能が紹介されており、それぞれの機能や実装方法が解説されています。また、VS Code拡張の選定は開発者のワークフローとスタックに応じて異なり、AIコード補完、フォーマット、デバッグ、Gitワークフロー、テスト、リモート開発、デプロイメントなどの機能を提供する拡張が注目されています。さらに、VS Code内でのマンガやコミックの読み込みが可能になったMangaBarや、開発者向けのタマゴットチ風ゲームDevGotchiなど、VS Code拡張の多様な応用例が紹介されています。このような多様な拡張機能の登場により、VS Codeは開発者にとっての強力なツールとしての地位をさらに強化しています。

## 共通して確認できる点

vsceasyは、VS Code拡張の開発を簡素化するCLIとフレームワークであり、React webview、typed RPC橋、ファイルベースのルーティングなどの機能を提供します。このフレームワークは、拡張機能のプロジェクト構造を自動生成し、パネル、コマンド、メニュー、ツリービューなどの構成をpackage.jsonに自動で設定します。また、LLMクライアントやミニORM、エディタ表面の補助機能（幽霊テキスト、入力ガード、装飾）などの追加機能も提供します。vsce,asyは、拡張機能をパッケージ化する前に、package.jsonで参照されているすべての構文、スニペット、アイコンが実際に存在することを確認します。さらに、LLM（例：Claude、Codex、Cursor）を使用して拡張機能を構築する際、エージェントに必要なすべての情報提供を可能にします。また、生成された拡張機能は、実際にVS Codeで動作するように設計されており、テストやLLMの実行も可能です。

## 記事ごとの差分・視点の違い

記事ごとの差分・視点の違いは、それぞれの目的や対象読者層に応じて異なります。記事1は、vsceasyというツールを用いて実際にVS Code拡張を構築した経験を共有し、そのフレームワークの機能や構造を詳しく解説しています。この記事では、vsceasyが提供するReact webview、typed RPC橋、ファイルベースのルーティングなどの技術的な側面が強調されています。また、生成された拡張機能が実際に動作するように設計されている点も重要です。

記事2は、2026年の最新のVS Code拡張についてのランキングを紹介しており、AIコード補完、フォーマット、デバッグ、Gitワークフロー、テスト、リモート開発、デプロイメントなどの機能を持つ拡張を推薦しています。この記事では、開発者のワークフローとスタックに応じて適切な拡張を選ぶことが重要であると説明しています。

記事3は、VS Code内にインストール可能なマンガリーダー拡張「MangaBar」の開発経緯と特徴を紹介しています。この記事では、長時間のコンパイルやデバッグ中にマンガを読むために開発されたという背景が強調されており、ローカルでのオフラインダウンロードやズーム機能などの実用性に注目しています。

記事4は、MangaBarの公式マーケットプレイスページであり、その機能やサポートされるソース、ダウンロード方法、設定方法などを詳細に説明しています。この記事では、MangaBarが提供する350以上のソースと、オフラインでの利用が可能であることが特徴として強調されています。

記事5は、VS Code内にインストール可能な開発者向けのタマゴットチのようなゲーム「DevGotchi」の紹介記事で、コードを書くことで得られるXPやコーヒー豆、Burnoutメカニズム、Focus Sprints、Bug Bossなどの特徴が説明されています。この記事では、開発者のモチベーションを高めるためのユニークなアプローチが注目されています。

## 深掘り調査で得られた知見

vsceasyは、VS Code拡張の開発を効率化するCLIツールとフレームワークであり、React webview、typed RPC橋、ファイルベースのルーティングなどの機能を提供します。このツールは、拡張機能の構築に必要なパッケージの設定、コマンド、パネル、メニュー、ツリービューなどの構成を自動的に生成し、手動での編集を必要としません。また、LLMクライアントやミニORM、エディタ表面の補助機能（幽霊テキスト、入力ガード、装飾）などの追加機能も提供しています。生成された拡張機能は、実際にVS Codeで動作するように設計されており、テストやLLMの実行も可能です。特定のプロジェクトタイプ（例：言語ベースの拡張）をサポートし、TextMate構文や言語構成ファイル、スニペット、ファイルアイコンなどの生成を可能にします。また、拡張機能をパッケージ化する前に、package.jsonで参照されているすべての構文、スニペット、アイコンが実際に存在することを確認します。LLM（例：Claude、Codex、Cursor）を使用して拡張機能を構築する際には、エージェントに必要なすべての情報提供を可能にします。拡張機能を構築した場合、リポジトリリンクを提供することで、ショーケースページに掲載する可能性があります。VS Code拡張には、GitHub Copilot、Prettier、ESLint、GitLens、Error Lens、Playwright Test for VS Codeなどの拡張が推奨されており、これらの拡張はAIコード補完、フォーマット、デバッグ、Gitワークフロー、テスト、リモート開発、デプロイメントなどの機能を提供します。VS Code拡張の選定は、開発者のワークフローとスタックに応じて異なり、最も役立つ拡張はコードの速度、デバッグ、テスト、バージョン管理、リモート開発、デプロイメントを向上させるものです。

## 不確実な点・追加確認が必要な点

記事間で確認された情報にはいくつかの食い違いや不一致が見られます。まず、記事1ではvsceasyがVS Code拡張開発を支援するCLIとフレームワークであり、React webviewやtyped RPC橋、ファイルベースのルーティングなどの機能を提供していると述べられています。一方で、記事3と記事4はMangaBarという拡張機能について説明しており、記事3ではMangaBarがVS Code、Cursor、Windsurf、VSCodiumで動作し、MangaDexやKeiyoushi/Tachiyomi拡張からコンテンツを取得するという内容が記載されています。記事4では、MangaBarが350以上のソースをサポートしており、オフラインダウンロードやズーム、パン機能を備えていると明記されています。しかし、記事1や記事2にはMangaBarに関する情報は含まれていません。また、記事5ではDevGotchiというVS Code拡張について説明されており、コードを書くことでステータスが減る仕組みや、Burnoutメカニクス、Focus Sprints、Bug Bossなどの機能が記載されています。しかし、これらの拡張機能がvsceasyで構築されたかどうかは明記されていません。そのため、記事1で述べられたvsceasyの利用例としてのTwo Real VS Code Extensionsが、記事3や記事4で説明されているMangaBarと同一であるかどうかは断定できません。また、記事2では2026年9月15日に公開された16のVS Code拡張が紹介されていますが、その中にMangaBarやDevGotchiが含まれているかどうかは明示されていません。したがって、記事間での情報の整合性や関連性を確認するためには、さらなる調査や情報収集が必要です。

## 元記事一覧

- [TwoRealVSCodeExtensions, Built withvsceasy... - DEV Community](https://dev.to/jairofernandez/two-real-vs-code-extensions-built-with-vsceasy-and-what-each-feature-does-3opc)
- [16 best VS Code extensions for developers in 2026 - Hostinger](https://www.hostinger.com/tutorials/best-vs-code-extensions/)
- [I built an offline manga reader inside VS Code and Cursor](https://dev.to/jayesh_99/i-built-an-offline-manga-reader-inside-vs-code-and-cursor-2ocb)
- [MangaBar — Manga, Manhwa & Comic Reader for Any IDE (VS Code ...](https://marketplace.visualstudio.com/items?itemName=j-a-y-e-s-h.mangabar)
- [IBuiltaTamagotchiforDevelopers—ItLivesinVSCodeand...](https://dev.to/johnfacey/i-built-a-tamagotchi-for-developers-it-lives-in-vs-code-and-judges-your-work-ethic-47nl)
