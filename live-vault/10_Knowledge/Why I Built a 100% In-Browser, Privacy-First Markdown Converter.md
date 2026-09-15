---
title: 「なぜ私は100%ブラウザ内でのプライバシー優先Markdownコンバーターを作ったのか」
type: knowledge
status: draft
created: 2026-09-15
updated: 2026-09-15
confidence: medium
---

# 「なぜ私は100%ブラウザ内でのプライバシー優先Markdownコンバーターを作ったのか」

## 結論

MD-Convertの開発は、現代のクラウドベースのファイルコンバーターが抱えるデータプライバシーの課題を解決するための明確な動機に基づいており、すべての処理をユーザーのブラウザ内でローカルで行うことで、機密情報の漏洩リスクを回避する点で、技術的に信頼性の高いソリューションとして位置づけられている。

## テーマ概要

Markdownの変換ツールとして注目されている「MD-Convert」は、ユーザーのブラウザ内で完全にローカルで動作するプライバシーファースト型のユーティリティです。このツールは、PDF、DOCX、Jupyterノートブック、スプレッドシート、JSON、YAML、XML、URLなど、幅広いファイル形式をサポートし、それらをクリーンなMarkdownに変換します。特に、現代のクラウドベースの変換ツールではデータプライバシーが大きな懸念とされている中、MD-Convertはすべての処理をユーザーのデバイス上で行い、サーバーにデータをアップロードすることはありません。このプライバシーへの配慮と、操作の簡便性から、今注目を集めています。

## 共通して確認できる点

複数の記事で共通して確認できた事実として、Markdownの利用は技術ドキュメンテーションや静的サイトジェネレータ、LLMのプロンプトコンテキスト（RAGパイプライン）など、さまざまな場面で広く採用されている。しかし、現実のドキュメントからMarkdownへの変換は、CLIツールの必要性や、敏感なデータをオンラインコンバーターにアップロードするリスク、手動でのクリーンアップ作業などの課題を抱えている。これらの問題を解決するために、MD-Convertというプライバシーを最優先にしたブラウザ内でのMarkdownコンバーターが開発された。このツールは、PDF、DOCX、Jupyterノートブック、スプレッドシート、JSON、YAML、XML、URLなど、幅広いファイル形式をサポートし、すべての処理をユーザーのデバイス上で実行することで、データの漏洩を防いでいる。また、YAMLフロントマター、目次、AIおよびRAGパイプライン向けのエクスポート機能など、便利な機能も備えている。

## 記事ごとの差分・視点の違い

記事「Why I Built a 100% In-Browser, Privacy-First Markdown Converter」は、Markdown変換ツールの開発動機とそのプライバシーへの配慮を強調している。一方で、記事「Your firewall is your AI policy — I probed 18 major sites to read it」は、AIクローラーの動作とウェブサイトのセキュリティポリシーの関係を分析し、ファイアウォール設定が企業のビジネス文書としての重要性を持つことを指摘している。また、「Fan-out auditing: making AI coding agents actually read your entire codebase」は、AIによるコードベースの検証において、並列処理ではなく詳細な検証を重視するアプローチを提案しており、AIの性能低下を考慮した設計を強調している。さらに、「Cloud infrastructure management: the 90% nobody warns you about」は、クラウドインフラの運用における困難な側面を掘り下げ、インフラをコードで管理する重要性を説いている。最後に、「Multilingual prompt injection: Your LLM’s safety net has a language problem」は、LLMのセキュリティ対策が多言語環境に対応していない問題を指摘し、攻撃者が言語を変えてpayloadを送る可能性を示している。各記事は、それぞれ異なる技術的・セキュリティ的・運用的な視点から、現代のデジタル環境における課題と対応策を論じている。

## 深掘り調査で得られた知見

MD-Convertは、ユーザーのブラウザ内で完全にローカルで動作するため、データのプライバシーを確保する点で注目を集めている。このツールは、PDF、DOCX、Jupyterノートブック、スプレッドシート、JSON、YAML、XML、URLなどの多様なファイル形式をサポートしており、すべての処理がユーザーのデバイス上で行われるため、サーバーにデータをアップロードする必要がなくなる。これにより、企業の機密情報を含むドキュメントの変換にも適しており、特にデータ漏洩のリスクを回避したいユーザーにとって魅力的な選択肢となる。  

また、MD-Convertは、YAMLフロントマター、目次、AIやRAGパイプライン向けのエクスポート機能など、豊富な機能を備えている。ただし、複雑なPDFレイアウトや画像参照の保持といった課題にはまだ対応していない。これらの制限は、今後の改善点として挙げられており、開発者はユーザーからのフィードバックを反映しながらツールの精度を高めていく予定である。  

このツールの開発背景には、現代のクラウドベースのファイルコンバーターのデータプライバシーの欠如が挙げられる。ユーザーが企業文書や内部スプレッドシートをオンラインツールにアップロードする際、データが外部サーバーに送られるリスクがある。MD-Convertは、こうした懸念を解消し、ユーザーが安心してドキュメントを変換できる環境を提供することを目的としている。

## 不確実な点・追加確認が必要な点

記事間の食い違いや資料からは断定できない点を具体的に述べると、以下の通りです。まず、MD-Convertというツールの開発動機について、記事5（Why I Built a 100% In-Browser, Privacy-First Markdown Converter）では、現代のクラウドファイルコンバーターの最大の欠点としてデータプライバシーを挙げています。このツールは、すべての解析アルゴリズムと変換がユーザーのブラウザ内でローカルで行われ、データがサーバーにアップロードされることはありません。しかし、記事の深掘り調査結果では、このツールの動作メカニズムについて、Mozillaのpdf.jsをWeb Worker内で使用し、OCRエンジンやバックエンドサーバーを介さないため、選択可能なテキストストリームのみを抽出していることが明記されています。これにより、複雑なレイアウトやスキャンされたページのテキスト出力が雑になる可能性があるとされています。

また、記事5では、URLからMarkdownへの変換機能について、Mozilla ReadabilityとTurndownを使用して、広告やメディアを除去した純粋な記事テキストを抽出していると説明していますが、画像参照（![alt/url）を保持する機能は今後のアップデートで実装される予定であると述べています。これは、別の記事やコメントからのフィードバックに基づく改善計画であり、現時点では機能していないことが確認されています。

さらに、記事1（Your firewall is your AI policy — I probed 18 major sites to read it）では、AIクローラーがJavaScriptを実行しないことや、robots.txtの内容と実際のWAFの対応が一致しない例が示されています。これは、AIクローラーの検出や制御に関する技術的課題を示しており、MD-Convertのようなツールのプライバシー保護の重要性と、AI技術の制限についての理解を深める背景として関連性があります。ただし、これらの情報はMD-Convertの開発動機とは直接的な関係がなく、異なる技術的課題を扱っているため、断定してはなりません。

## 元記事一覧

- [Your firewall is yourAIpolicy — I probed 18majorsitesto read it](https://dev.to/abouchard11/your-firewall-is-your-ai-policy-i-probed-18-major-sites-to-read-it-5552)
- [Fan-out auditing: making AI coding agents actually read your ...](https://dev.to/lachiejames/fan-out-auditing-making-ai-coding-agents-actually-read-your-entire-codebase-31ba)
- [Cloudinfrastructuremanagement:the90%nobodywarnsyouabout](https://dev.to/nodevguy/cloud-infrastructure-management-the-90-nobody-warns-you-about-2976)
- [Multilingual Prompt Injection: Your LLM’s Safety Net Has a Language Problem | by Nwosu Rosemary | Medium](https://nwosunneoma.medium.com/multilingual-prompt-injection-your-llms-safety-net-has-a-language-problem-440d9aaa8bac)
- [Why I Built a 100% In-Browser, Privacy-First Markdown Converter](https://dev.to/__7b51d76b10fdb4b/why-i-built-a-100-in-browser-privacy-first-markdown-converter-3coe)
