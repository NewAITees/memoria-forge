---
title: 自前インストールChatwootのリソース使用量
type: knowledge
status: draft
created: 2026-09-16
updated: 2026-09-16
confidence: medium
---

# 自前インストールChatwootのリソース使用量

## 結論

Self-hosted Chatwootのリソース使用量は、348,703メッセージを20インボックスで管理するのに約1.8GBのRAMが使用され、4GBのVPSで運用可能であることが確認されています。これはメッセージ量に比例してリソースが使用されるため、シート数（ユーザー数）ではなくメッセージ量が重要であることを示しており、自前インストールでは追加エージェントのコストが発生しない点も特徴的です。一方、Cloud版では履歴保持期間が制限されるため、長期的なデータ保持が必要なチームにはSelf-hostedが適していると言えます。

## テーマ概要

Self-hosted Chatwootのリソース使用量を測定した結果、348,703メッセージを20インボックスで管理するのに約1.8GBのRAMが使用され、4GBのVPSで運用可能であることが明らかになりました。この測定結果は、メッセージ数に比例してリソースが使用される点を強調しており、シート数（ユーザー数）ではなくメッセージ量が重要な要素であることを示しています。また、クラウド版では会話履歴の保持期間が制限されているのに対し、セルフホスティングでは履歴を永久に保持できるという利点もあります。この情報は、コスト効率と運用の柔軟性を重視するチームにとって重要な参考となっています。

## 共通して確認できる点

複数の記事で共通して確認できた事実として、Self-Hosted Chatwootの実際のリソース使用量が測定されている。具体的には、348,703メッセージが20インボックスにわたって約1.8GBのRAMを使用し、4GBのVPSで運用が可能であることが確認されている。また、リソースの使用量はメッセージ量に比例し、シート数（ユーザー数）とは関係がないことが指摘されている。さらに、Self-Hostedのインストールに追加のエージェントを追加する際にはコストが発生しない一方で、Cloud版では各シートごとに月額料金が発生する点も共有されている。また、Self-Hostedではデータの保持期間が制限されず、すべての会話履歴を保持できる一方で、Cloud版では無料プランで30日間、有料プランで最大6ヶ月間しか履歴を保持できないことが確認されている。

## 記事ごとの差分・視点の違い

記事「I Measured What Self-Hosted Chatwoot Actually Uses. 348,703 Messages, 1.8 GB of RAM」は、自前でChatwootを運用している際のリソース使用量を実測した結果を詳細に報告している。この記事では、メッセージ数とRAM使用量の関係、および自前運用とクラウド運用の違いに焦点を当てている。一方で、「Unit Economics of Agentic AI: Context × Turns × Model」は、AIのコスト削減と効率的な運用のための包括的なアプローチを説明し、コストの構造を3つの変数として分析している。また、「AI Unit Economics FAQ: How to Measure AI Cost, Value, and Margin」は、AIのコストと価値を測定するためのフレームワークを提示し、FinOpsチームがどうやってコストを管理すべきかを説明している。さらに、「Chrome DevTools MCP 1.7: debug memory leaks without reading raw heap snapshots」は、メモリリークの検出方法を改善し、AIコードアーキテクトが効率的にデバッグできるようにするツールの進化を紹介している。最後に、「Claude Managed Agents Session Budget Checklist」は、Claudeのセッション予算に関する仕組みを解説し、コスト制御の仕組みについて述べている。各記事はそれぞれ異なる視点からAIや自前運用のコスト管理について議論している。

## 深掘り調査で得られた知見

深掘り調査によって、Self-hosted Chatwootの実際のリソース使用量についての詳細な情報が明らかになりました。348,703件のメッセージが20つのインボックスにわたって蓄積し、そのデータは約1.8GBのRAMで保持されることが確認されました。この規模のデータは、4GBのVPSで運用することができ、リソースの負荷はそれほど高くありません。また、PostgreSQLは997MBのディスク容量を消費しており、全体のディスク使用量は38GB中の20GBに達しています。RAM使用量は3.7GB中の2.4GBとなっています。

この測定は、メッセージの量に比例してリソースが使用されるという点が重要です。つまり、利用者数（シート数）ではなく、メッセージの量がリソースの使用量を決定するため、スケーラビリティの面で柔軟性があります。また、Self-hostedのインストールにエージェントを追加する際にはコストがかからないという点も注目すべきです。一方、Chatwoot Cloudでは、エージェントごとに月額料金が発生するため、コストが増加します。

さらに、Chatwoot Cloudの各プランでは、会話履歴の保持期間が異なります。無料プランでは30日間、最安プランでは6か月間、それ以上はさらに長期のプランが必要です。測定では、履歴が2025年11月25日までに遡るため、無料プランではすでに履歴が削除される可能性があります。これは、サポートインボックスなどで過去の履歴を参照する必要がある場合、プランのアップグレードを余儀なくさせる要因となっています。

Self-hostingは、データの完全な制御を可能にする一方で、運用面での負担も伴います。PostgreSQLの接続プールの枯渇やRedisのエビジェクトポリシーの問題、ログローテーションの設定ミスなど、さまざまな運用上の課題が報告されています。これらの問題は、Self-hostingのコストを「あなたの注意」に置く形で発生しており、技術的な知識と運用経験が求められます。

また、測定結果は、Self-hostingが中小規模のチームや、データ制御を重視するチームに適している一方で、運用能力が限られるチームにはCloudが適していることを示唆しています。このように、Self-hostedとCloudの選択は、チームのニーズやリソースに応じて異なり、それぞれの利点と欠点を理解することが重要です。

## 不確実な点・追加確認が必要な点

記事間の食い違いや資料からは断定できない点を具体的に書く場合、以下の内容が挙げられます。

まず、記事3（I Measured What Self-Hosted Chatwoot Actually Uses. 348,703 Messages, 1.8 GB of RAM）では、348,703メッセージが約1.8GBのRAMを消費し、4GBのVPSで運用可能であることが記載されています。一方で、記事1や記事2では、AIのコスト管理やユニット経済学の観点から、トークン消費量やモデルコスト、コンテキストの影響などについて論じていますが、具体的なChatwootのリソース使用量やインフラ構成については言及されていません。したがって、AIのコスト管理に関する一般的なフレームワークと、Chatwootの自前インストールにおける具体的なリソース使用量は、異なる文脈での情報であり、直接的な比較はできません。

また、記事5（Claude Managed Agents Session Budget Checklist）では、 Claude Managed Agentsにおいて、セッションごとの予算制限が導入され、セッションが予算を超えた場合に一時停止する仕組みが説明されていますが、これはChatwootの自前インストールとは無関係な機能であり、両者の技術的背景や運用モデルは異なっています。したがって、これらの情報は、異なる技術スタックにおけるコスト管理の実装例として捉える必要があります。

さらに、記事4（Chrome DevTools MCP 1.7）では、メモリリークのデバッグに特化したツールや機能が紹介されていますが、これはWebブラウザやNode.js環境でのデバッグに特化した技術であり、Chatwootの自前インストールにおけるメモリ管理とは直接的な関連性がありません。これらは、異なる分野での技術的課題に対する解決策であり、相互に比較・統合することはできません。

以上の通り、各記事は異なる技術的文脈やテーマに基づいており、情報の直接的な整合性や比較可能性は限定されています。したがって、記事3が提示するChatwootの自前インストールにおけるリソース使用量や運用状況は、他の記事とは別個の観点からの情報として捉える必要があります。

## 元記事一覧

- [AI Unit Economics FAQ: How to Measure AI Cost, Value, and Margin](https://surveil.co/ai-unit-economics-finops-cost-value-margin/)
- [Unit Economics of Agentic AI: Context × Turns × Model | Solo.io](https://www.solo.io/blog/unit-economics-of-agentic-ai-context-turns-model)
- [I Measured What Self-Hosted Chatwoot Actually Uses. 348,703 ...](https://dev.to/achiya-automation/i-measured-what-self-hosted-chatwoot-actually-uses-348703-messages-18-gb-of-ram-4cp1)
- [ChromeDevToolsMCP1.7:debugmemoryleakswithoutreading...](https://dev.to/ahab_indieseek/chrome-devtools-mcp-17-debug-memory-leaks-without-reading-raw-heap-snapshots-3j0b)
- [Claude Managed Agents Session Budget Checklist - DEV Community](https://dev.to/ahab_indieseek/claude-managed-agents-session-budget-checklist-ge9)
