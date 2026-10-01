---
title: LLMフレームワークが同じツールオブジェクトを再構築する現象
type: knowledge
status: draft
created: 2026-10-01
updated: 2026-10-01
confidence: medium
---

# LLMフレームワークが同じツールオブジェクトを再構築する現象

## 結論

LLMフレームワークでは、ツールオブジェクトの本質的な機能が共通しており、各フレームワークでは異なるラッパー関数を用いてその実装を再構築している。Standard Schemaの導入により、ツールの入出力スキーマが一貫して表現され、ライブラリ間での互換性が確保されている。このような標準化は、ツールの再利用性を高め、フレームワークごとの違いを補う役割を果たしている。

## テーマ概要

LLMフレームワークにおいて、同じツールオブジェクトが再構築されている現象が注目されている。このツールオブジェクトは、関数、名前、説明、入出力のスキーマを含み、モデルが呼び出す際の必要条件を提供する。各フレームワークでは、`tool()`、`registerTool`、`defineTool`などのラッパー関数が異なるが、実際の機能は共通している。このような一貫性は、Standard Schemaという共通のスキーマ形式を採用しているためであり、Zod、Valibot、ArkTypeなどのライブラリで実装され、60以上のツールで利用されている。この標準化により、ライブラリ間のアダプターを必要とせず、ツールの再利用性が高まっている。また、Makiなどのフレームワークは、ローカルモデルやホストAPIを統合的にサポートし、マルチエージェントアプリケーションの開発を効率化している。このような背景から、LLMフレームワークにおけるツールオブジェクトの再構築が注目されている。

## 共通して確認できる点

LLMフレームワークでは、同じツールオブジェクトが再構築されているが、ラッパー関数はフレームワークごとに異なっている。ツールは関数、名前、説明、入出力のスキーマを含み、モデルが呼び出す際の必要条件を提供する。Standard SchemaはZod、Valibot、ArkTypeなどのライブラリで共通して使用され、コードがStandard Schemaを受け入れることでライブラリ間のアダプターを必要としない。Standard JSON SchemaはJSONスキーマを生成し、モデルがツールを呼び出す際の引数を定義する必要がある。Standard Schemaは30以上のライブラリで実装され、60以上のツールで使用されている。MakiはPythonベースのマルチエージェントLLMフレームワークで、ローカルモデルやホストAPI（OpenAI、Anthropicなど）をサポートし、MITライセンスで開発されている。

## 記事ごとの差分・視点の違い

記事「Every LLM framework rebuilt the same tool object」では、LLMフレームワークが共通のツールオブジェクトを再構築している現象が強調されている。この記事では、ツールの本質が関数とその必要な情報（名前、説明、スキーマ）であり、フレームワークごとにラッパー関数が異なる点に注目している。また、Standard Schemaの標準化により、ツールの移植性が向上しているという点も述べられている。

記事「Maki - Python Multi Agent LLM Framework」は、PythonベースのマルチエージェントLLMフレームワークとしてのMakiの特徴を紹介している。この記事では、MakiがローカルモデルやホストAPIをサポートし、MITライセンスで開発されていること、また、フレームワークの設計思想やインフラ層の構成について詳しく説明している。

記事「TypeScript 6.0 `--noPropertyAccessFromIndexSignature`: The Flag That Forces Honest API Contracts」では、TypeScript 6.0で導入された`--noPropertyAccessFromIndexSignature`フラグについて解説している。このフラグは、インデックスシグネチャで定義されたプロパティにドット記法を使用することを禁止し、ブラケット記法に統一することで、API契約の信頼性を高めることを目的としている。

記事「TSConfig Option: noPropertyAccessFromIndexSignature - TypeScript」は、`noPropertyAccessFromIndexSignature`設定の仕組みと目的を説明している。この設定により、ドット記法でアクセス可能なプロパティとインデックス記法でアクセス可能なプロパティの違いを明確にし、コードの信頼性を向上させることが目的である。

記事「TypeScript 6.0 Strict Function Types: Why Contravariance Breaks Your Existing Callbacks」では、TypeScript 6.0における`strictFunctionTypes`の導入と、共変性と反変性に関する問題点を説明している。この記事では、関数型の変換がどのように既存のコールバックに影響を与えるか、また、その対応策について述べている。

## 深掘り調査で得られた知見

LLMフレームワークでは、ツールオブジェクトの実装が共通化されている傾向が確認されている。たとえば、記事1では、AI SDKのtool()、GenkitのdefineTool、MCP SDKのregisterToolといったラッパー関数が異なるが、実際のツールの機能は共通しており、同じ処理を実行する。このような設計は、ツールを複数のフレームワーク間で再利用可能にするための標準化を目的としている。Standard SchemaやStandard JSON Schemaなどの仕様が利用され、これによりツールの入出力スキーマが一貫して表現され、ライブラリ間での互換性が確保されている。Standard SchemaはZod、Valibot、ArkTypeなど30以上のライブラリで実装され、60以上のツールで利用されている。このような標準化により、ツールの実装はフレームワークに依存せず、コードの再利用性が高まっている。

また、MakiというPythonベースのフレームワークが、ローカルモデルやホストAPI（OpenAI、Anthropicなど）をサポートしており、MITライセンスで開発されている。Makiでは、ローカル推論（Ollama）をホストAPIと同等の第一級バックエンドとして扱い、バックエンドの切り替えは1つのオブジェクトの変更で実現可能である。これにより、フレームワーク間でのツールの再利用性が高まり、開発効率が向上している。また、Makiでは、セキュリティ機能がデフォルトで有効化されており、不正な操作を防ぐ仕組みが備わっている。

## 不確実な点・追加確認が必要な点

LLMフレームワーク間で同じツールオブジェクトが再構築されているという主張は、記事1で具体的に述べられている。しかし、他の記事にはこのテーマに関する直接的な記述は見られず、関連性が低い。記事2のMakiはPythonベースのマルチエージェントLLMフレームワークであり、ツールオブジェクトの実装についての詳細は提供されていない。記事3や記事4、記事5はTypeScript 6.0の新機能について説明しており、LLMフレームワークやツールオブジェクトとの関連性は明示されていない。したがって、記事間での一致や差異は確認できず、このテーマに関する断定的な主張は避けなければならない。また、記事1の情報は、ツールオブジェクトの標準化やラッパー関数の違いについて述べているが、他の記事ではこの点を補足する情報が見られないので、独立した事実として扱う必要がある。

## 元記事一覧

- [EveryLLMframeworkrebuiltthesametoolobject- DEV Community](https://dev.to/finom/every-llm-framework-rebuilt-the-same-tool-object-13cj)
- [Maki - Python Multi AgentLLMFramework| EveryDev.ai](https://www.everydev.ai/tools/maki-framework)
- [TypeScript 6.0 `--noPropertyAccessFromIndexSignature`: The ...](https://jsmanifest.com/typescript-nopropertyaccessfromindexsignature-strict-api-contracts)
- [TSConfig Option: noPropertyAccessFromIndexSignature - TypeScript](https://www.typescriptlang.org/tsconfig/noPropertyAccessFromIndexSignature.html)
- [TypeScript6.0StrictFunctionTypes:WhyContravarianceBreaks...](https://dev.to/jsmanifest/typescript-60-strict-function-types-why-contravariance-breaks-your-existing-callbacks-5enk)
