---
title: Tododo: 友人向けプライベートタスクアプリの開発とGemma+Ollamaの活用
type: knowledge
status: draft
created: 2026-10-05
updated: 2026-10-05
confidence: medium
---

# Tododo: 友人向けプライベートタスクアプリの開発とGemma+Ollamaの活用

## 結論

Tododoは、友人Yathurshanのために開発されたプライベートなタスク管理アプリであり、Gemmaモデル（Ollamaを通じてローカルで実行）を活用して自然言語からタスク情報を抽出する仕組みを備えている。アプリはローカルで動作し、クラウドに依存せず、タスクの繰り返しルールに基づいた自動処理やサブタスクの管理機能を提供している。

## テーマ概要

Tododoは、友人Yathurshanのために開発されたプライベートな ToDo アプリで、複雑かつ繰り返しのタスクを効率的に管理するためのツールです。このアプリは、Gemma（Ollama経由）を活用して自然言語の入力からタスクのタイトル、サブタスク、繰り返しルールを抽出し、ユーザーが確認できる形で表示します。また、タスクが繰り返し実行される際には、サブタスクが自動的に未チェック状態に戻るなどの機能を備えています。アプリはローカルで動作し、クラウドへの依存がありません。Gemma4などのモデルは、Ollamaを通じてローカルで実行可能で、テキストや画像の処理が可能です。これらの技術の組み合わせにより、Tododoはプライバシーを重視しつつ、柔軟で効率的なタスク管理を実現しています。

## 共通して確認できる点

Tododoは、友人Yathurshanのために開発されたプライベートなタスク管理アプリで、複雑な繰り返しタスクやサブタスクを効率的に管理するための設計されている。アプリはGemmaモデル（Ollamaを通じてローカルで実行）を活用し、自然言語入力からタスクのタイトル、サブタスク、繰り返しルールを抽出する機能を備えている。ユーザーはタスクを保存する前に、Gemmaが理解した内容を確認できる編集可能なカードで表示されるため、誤った解釈を防ぐことができる。また、アプリはオフラインで動作し、Ollamaが利用できない場合でも、ルールベースのパーサーを用いて動作を維持する設計となっている。Gemma4はOllama上で実行可能なモデルで、2Bから31Bパラメータのバージョンが提供されており、テキストおよび画像の入力処理が可能である。TododoはPythonとSQLiteを用いたオープンソースのアプリケーションであり、クラウドに依存せずローカルで動作するため、プライベートなタスク管理ソリューションとして機能している。

## 記事ごとの差分・視点の違い

記事「Tododo: A Private To-Do App I Built for My Friend with Gemma + Ollama」は、友人のためのプライベートなタスク管理アプリの開発経緯とその仕組みを主に紹介しており、GemmaとOllamaを活用した自然言語処理の実装に注力しています。一方、「gemma4」の記事は、Gemmaモデルの最新版であるGemma4の仕様や、Ollamaプラットフォームでの利用方法、モデルの特徴について詳しく解説しており、技術的な側面に焦点を当てています。また、「Sanitycheck- Wikipedia」では、 Sanityチェックの定義とその用途、例を含む一般的な説明が行われており、概念的な解説が中心です。記事「An AI hardware advisor that walks every path—and gets its math-checked by the rules in Sanity」は、AIを用いたハードウェア選定アドバイザーの実装方法と、Sanityデータベースを活用した数学的検証の仕組みを説明しており、応用例に重点を置いた内容となっています。最後に、「I don't watch F1, so I built a quiz where the AI isn't allowed to grade me」は、F1レースに関するクイズアプリの開発背景と、AIが評価をしない仕組みについて述べており、教育的・自己学習目的での利用が強調されています。各記事はそれぞれ異なる視点や目的を持ち、技術的実装、概念解説、応用例、教育的用途など、幅広い角度からテーマに関連する内容を提供しています。

## 深掘り調査で得られた知見

Tododoは、友人Yathurshanのために開発されたプライベートなtodoアプリで、複雑な繰り返しタスクを扱うための設計がなされている。アプリは自然言語入力を受け取り、Gemma（Ollama経由）を用いてタイトル、サブタスク、繰り返しルールを抽出する。ユーザーは保存前にモデルが理解した内容を確認できる編集可能なカードを表示する仕組みがある。繰り返しルールとして毎日、毎週、毎月がサポートされており、サイクルが終了するたびにサブタスクが自動的に未チェック状態に戻る。アプリはPythonとSQLiteをベースに構築されており、クラウドに依存せずローカルで動作する。Gemma4はOllamaを通じて利用できるモデルで、2Bから31Bパラメータのバージョンが存在し、テキストと画像の入力に対応している。Ollamaはローカルでのモデル実行を可能にし、GPUアクセラレーションにより推論速度を向上させる。Tododoはオープンソースであり、ローカルマシンで動作するため、プライベートで運用可能なソリューションを提供する。

## 不確実な点・追加確認が必要な点

記事間の食い違いや資料からは断定できない点を以下に示します。まず、Tododoというプライベートなタスク管理アプリについての情報は、記事1のみに記載されており、他の記事は関連性が低いため、Tododoの詳細な機能や設計についての記述はこの1記事に依存しています。また、Gemma4に関する情報は記事2で提供されており、Gemma4はOllamaを通じてローカルで実行可能で、最大310億パラメータのモデルが提供されていることが確認されています。しかし、Gemma4がTododoアプリで実際に使用されているかどうかは、記事1の内容からは明確ではありません。また、Sanityチェックに関する情報は記事3および記事4に記載されており、Sanityチェックは主に数学的・論理的な検証を目的とした簡易なテスト手法であり、AIハードウェアアドバイザーの開発において、計算結果をルールベースのデータベースと照合する機能として使用されていることが示されています。しかし、TododoアプリとSanityチェックの間の直接的な関連性は、資料からは確認できません。さらに、記事5ではF1に関するクイズアプリの開発が記載されており、これはTododoアプリとは関連性が低いため、今回のテーマと直接的な関連性は見られません。したがって、Tododoアプリに関する情報は記事1にのみ集中しており、他の記事は関連性が低いことが確認されています。

## 元記事一覧

- [Tododo: A PrivateTo-DoAppI Built for MyFriend... - DEV Community](https://dev.to/abishethvarman/tododo-a-private-to-do-app-i-built-for-my-friend-with-gemma-ollama-3p18)
- [gemma4](https://ollama.com/library/gemma4)
- [Sanitycheck- Wikipedia](https://en.wikipedia.org/wiki/Sanity_check)
- [AnAIhardwareadvisorthatwalkseverypath—andgetsitsmath...](https://dev.to/helgard_orlm/an-ai-hardware-advisor-that-walks-every-path-and-gets-its-math-checked-by-the-rules-in-sanity-21db)
- [Idon'twatchF1,soIbuiltaquizwheretheAIisn'tallowedto...](https://dev.to/hempun10/i-dont-watch-f1-so-i-built-a-quiz-where-the-ai-isnt-allowed-to-grade-me-b0b)
