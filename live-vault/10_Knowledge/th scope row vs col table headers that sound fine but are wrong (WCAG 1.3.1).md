---
title: th scope row vs col: テーブルヘッダーの誤った設定とWCAG 1.3.1準拠の重要性
type: knowledge
status: draft
created: 2026-10-21
updated: 2026-10-21
confidence: medium
---

# th scope row vs col: テーブルヘッダーの誤った設定とWCAG 1.3.1準拠の重要性

## 結論

WCAG 1.3.1 に準拠するテーブル構造を実装するためには、`<th>` 要素に `scope` 属性を正しく設定することが不可欠であり、その欠如はスクリーンリーダーがヘッダーとデータセルの関係を誤って解釈する原因となる。特に、複数行のヘッダーを持つテーブルでは、`scope` 属性が設定されていないと、情報の誤解やナビゲーションの困難さが生じる可能性がある。そのため、テーブルのアクセシビリティを確保するためには、`<th>` 要素と `scope` 属性の適切な使用が必須である。

## テーマ概要

WCAG 1.3.1 は、テーブルの情報と関係性をスクリーンリーダーが正確に理解できるようにするための基準です。しかし、`<th>` 要素に `scope` 属性を正しく指定しない場合、スクリーンリーダーがヘッダーとデータセルの関係を誤って解釈してしまうことがあります。このような誤ったヘッダー構造は、ユーザーがテーブルのデータを正しく理解できず、情報の誤解を招く可能性があります。特に、`th` 要素が行スコープ（`row`）や列スコープ（`col`）を正しく指定しないと、スクリーンリーダーがデータをナビゲートする際の論理的な関係が崩れ、アクセシビリティに重大な影響を与えます。この問題は、WCAG 1.3.1 の違反として検出されやすく、修正が比較的容易ですが、手動での確認も必要です。そのため、テーブル構造を設計する際には、`<th>` 要素と `scope` 属性を正しく使用することが重要です。

## 共通して確認できる点

WCAG 1.3.1 は、テーブルの情報と関係性をスクリーンリーダーに正確に伝えるための基準であり、情報が正しく表示されない場合、ユーザーはデータを理解できず、混乱を招く可能性があります。テーブルヘッダーの `<th>` 要素に `scope` 属性を指定しないと、スクリーンリーダーがヘッダーとデータセルの関係を正しく理解できず、テーブルが意味を持たなくなる可能性があります。スクリーンリーダーがテーブルをナビゲートする際、ヘッダー情報が表示されないと、ユーザーがデータの意味を理解できず、情報の誤解を招く可能性があります。また、複数の記事で確認された事実として、`<th>` 要素に `scope` 属性が不足している場合、スクリーンリーダーがデータとヘッダーの関係を正しく把握できず、テーブルの内容が誤って解釈されることがあります。この問題は、WCAG 1.3.1 の違反として自動化ツールによって検出されることが多く、修正が比較的容易であるとされています。ただし、修正後も手動での確認が必要です。

## 記事ごとの差分・視点の違い

記事「Accessible (I Think) Split-Cell Table Headers– Eric’s Archived Thoughts」は、テーブルのアクセシビリティに関する具体的な構造設計の課題を扱い、`<th>`要素と`scope`属性の必要性を強調しています。特に、複数行のヘッダーを持つテーブルにおいて、`scope`属性が欠如しているとWCAG 1.3.1に違反することを指摘しています。一方、「HTMLTableHeaders:WCAGFailures and Fixes |accessibility.chat」は、WCAG 1.3.1の違反が実際にどのようにユーザーに影響を与えるかを実例を交えて説明し、自動化ツールによる検出や修正の重要性を論じています。また、「A CancelledStreamNeedsaGeneration Guard... - DEV Community」や「A Superseded AIStreamNeedsaStable Status... - DEV Community」は、アクセシビリティの問題がテーブルに限らず、ストリーム処理やUI状態の管理にも及ぶことを示し、スクリーンリーダーが古いテキストを読み続ける問題を具体的なシナリオで説明しています。最後に、「Decoding the Accessibility Tree in Shadow DOM: Challenges and...」は、Shadow DOMの導入がアクセシビリティツリーの構築に与える影響を考察し、スクリーンリーダーがshadow boundaryを正しく理解できない可能性を指摘しています。各記事は、アクセシビリティの課題を異なる観点から掘り下げており、技術的・実践的な側面をそれぞれ強調しています。

## 深掘り調査で得られた知見

WCAG 1.3.1 に関する深掘り調査では、テーブルヘッダーの `scope` 属性が正しく使用されていない場合、スクリーンリーダーがデータセルとヘッダーの関係を誤って解釈してしまうことが確認されました。例えば、記事 1 では、`<th>` 要素に `scope` 属性が設定されていないことで、アクセシビリティ専門家が WCAG 1.3.3 に違反していると指摘しています。これは、テーブルの構造が不完全で、ユーザーがデータを正しく理解できなくなる原因となります。記事 2 でも、`<th>` 要素に `scope` 属性が欠如していることで、スクリーンリーダーがヘッダーとデータセルの関係を把握できず、情報の誤解を招く可能性があると述べています。また、`<caption>` が欠如している場合、複数のテーブルが存在するページでは、ユーザーがどのテーブルを参照しているのかを判断できなくなるという問題も指摘されています。これらの事例から、テーブル構造のアクセシビリティを確保するためには、`<th>` 要素に `scope` 属性を正しく設定し、必要に応じて `<caption>` を使用することが重要であることがわかります。

## 不確実な点・追加確認が必要な点

記事間の食い違いや資料からは断定できない点として、WCAG 1.3.1 に違反するテーブル構造の具体例や修正方法について、各記事の記述が一貫していない点が挙げられる。例えば、記事 1 では、`<th>` 要素に `scope` 属性を指定しないことで WCAG 1.3.3 に違反する可能性があると指摘されているが、記事 2 では WCAG 1.3.1 に該当する問題として `th` に `scope` が欠如していることが述べられている。このように、WCAG 1.3.1 と 1.3.3 が混同されている可能性がある。また、記事 2 では、`<th>` 要素に `scope` 属性を正しく使用することで、スクリーンリーダーがヘッダーとデータセルの関係を正しく理解できるようになると説明されているが、記事 1 では、`scope` 属性を適用した場合でも、テーブルナビゲーションが完全には改善されないという記述がある。このように、各記事の記述には一貫性が見られず、具体的な修正方法や WCAG 1.3.1 に該当する問題の詳細については、さらなる調査が必要である。

## 元記事一覧

- [Accessible (I Think) Split-CellTableHeaders– Eric’s Archived Thoughts](https://meyerweb.com/eric/thoughts/2026/05/28/accessible-i-think-split-cell-table-headers/)
- [HTMLTableHeaders:WCAGFailures and Fixes |accessibility.chat](https://www.accessibility.chat/articles/table-headers-a-small-tag-with-big-consequences)
- [A CancelledStreamNeedsaGeneration Guard... - DEV Community](https://dev.to/babycat/a-cancelled-stream-needs-a-generation-guard-not-just-a-stop-button-hea)
- [A Superseded AIStreamNeedsaStable Status... - DEV Community](https://dev.to/babycat/a-superseded-ai-stream-needs-a-stable-status-region-not-a-focus-stealing-toast-4hgp)
- [DecodingtheAccessibilityTreeinShadowDOM:Challengesand...](https://dev.to/mspk97/decoding-the-accessibility-tree-in-shadow-dom-challenges-and-solutions-ahm)
