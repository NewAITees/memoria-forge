---
title: Ant Designアクセシビリティ検出の限界と対応策
type: knowledge
status: draft
created: 2026-10-11
updated: 2026-10-11
confidence: medium
---

# Ant Designアクセシビリティ検出の限界と対応策

## 結論

Ant Designのアクセシビリティ検出において、jsx-a11yやaxeといったツールはそれぞれの限界を示しており、特にAnt Design特有の問題は検出が困難である。このため、静的解析とランタイムチェックを組み合わせたGitHub Action「antd-a11y-action」が開発され、Pull Requestの品質向上を支援している。また、1:1のコントラスト比のテキストや暗黒モードでのアクセシビリティ問題など、ツールの検出漏れが生じるケースも報告されており、アクセシビリティツールの補完と手動テストの重要性が再認識されている。

## テーマ概要

jsx-a11yとaxeなどのアクセシビリティ検出ツールは、Ant Designのアクセシビリティ問題を検出する際に限界を示している。jsx-a11yはプレーンなJSX要素しか理解できず、Ant Designの内部構造を把握できないため、特定のアクセシビリティの問題を検出できない。一方、axeはレンダリングされたDOMをスキャンするため、Ant Designの問題を検出できるが、ファイルと行番号を特定できない。このため、Ant Designのアクセシビリティ問題はツールの設定によって検出される可能性が異なる。このような限界を補うため、cstayyabが開発したGitHub Action「antd-a11y-action」が注目されている。このActionは、Ant Designのアクセシビリティ問題を検出するために静的解析とランタイムチェックを組み合わせており、Pull Requestの品質向上を支援する。また、1:1のコントラスト比のテキストがaxeで検出されない現象も報告されており、アクセシビリティツールの限界が再認識される。このような背景から、Ant Designのアクセシビリティ検出の課題は現在、開発者やアクセシビリティツールの改善に注目されている。

## 共通して確認できる点

jsx-a11yとaxeは、Ant Designのアクセシビリティの問題を検出する際、それぞれ異なる限界を持つ。jsx-a11yは、プレーンなJSX要素しか理解できず、Ant Designが内部でレンダリングする要素構造を把握できず、その結果としてアクセシビリティの問題を検出できない。一方、axeはレンダリングされたDOMをスキャンするため、Ant Designの問題を検出できるが、ファイルと行番号を特定できず、検出結果の可視化が難しい。このため、Ant Design特有のアクセシビリティの問題は、ツールの設定によって検出される可能性が異なる。また、1:1のコントラスト比のテキストは、axeが「incomplete」と分類し、違反とは見なさない。これは、背景の色が不確定なため、ツールが誤検出を避けるための保守的な判断である。このような「incomplete」の結果は、CIパイプラインで無視されがちだが、実際には重要なアクセシビリティの問題である可能性がある。そのため、CIパイプラインでは「incomplete」の結果も明確に表示し、対応を促す必要がある。

## 記事ごとの差分・視点の違い

記事「Why axe and jsx-a11y miss Ant Design accessibility bugs (and a GitHub Action that catches them)」は、Ant Designのアクセシビリティ問題がjsx-a11yやaxeといったツールで検出されない理由を解説し、そのギャップを補うGitHub Actionの開発を紹介している。一方、「GitHub- cstayyab/antd-a11y-action·GitHub」は、そのGitHub Actionの実装と機能を具体的に説明し、静的解析とランタイムチェックの両方を組み合わせた設計について述べている。  

「Text at 1:1 contrast is not an axe violation. It is incomplete.」では、axe-coreが1:1のコントラストを「incomplete」として分類する理由を論じており、その限界と、CIパイプラインでの扱いの問題を指摘している。また、「How to test dark mode accessibility in CI with Playwright and axe-core」は、dark modeでのアクセシビリティテストの重要性を強調し、Playwrightとaxe-coreを組み合わせたテストアプローチを提案している。  

「Your axe run is green and your dark mode has 1.04:1 contrast」では、1.04:1のコントラスト比が実質的に見えない状態であるにもかかわらず、axeがそれを検出しない現象を示し、CIが緑のままになる理由を分析している。各記事は、アクセシビリティツールの限界とその対応策、テスト環境の設定、そして具体的な問題事例に焦点を当て、それぞれ異なる視点から議論している。

## 深掘り調査で得られた知見

Ant Designのアクセシビリティ検出において、jsx-a11yやaxeなどのツールが検出を漏らす理由は、Ant Designが内部で複雑なDOM構造を生成するためです。jsx-a11yはプレーンなJSX要素にしか対応できず、Ant Designのコンポーネントがレンダリングされる過程を理解できません。一方、axeはレンダリング後のDOMをスキャンするため、Ant Designの問題を検出できますが、ファイルや行番号を特定できないため、修正が困難です。この限界を補うため、cstayyabが開発したGitHub Action「antd-a11y-action」は、静的解析とランタイムチェックを組み合わせ、Ant Design特有のアクセシビリティ問題を検出します。このツールは、Ant Designのバージョンごとに検出ルールを確認し、WCAG 2.2の成功基準に違反している可能性がある問題を特定します。また、1:1のコントラスト比のテキストはaxeが「incomplete」と分類し、違反とは見なしませんが、これはツールの保守的な判断であり、実際にはアクセシビリティに重大な影響を与える可能性があります。このようなケースでは、手動テストや「a11y-matrix」などのツールを用いて、さまざまな状態でのアクセシビリティを確認する必要があります。

## 不確実な点・追加確認が必要な点

記事間の食い違いや資料からは断定できない点を以下に示す。まず、jsx-a11yとaxeの限界について、Ant Designのアクセシビリティ問題を検出できない理由が説明されている。jsx-a11yはプレーンなJSX要素にしか対応できず、Ant Designの内部構造を理解できない。一方、axeはレンダリングされたDOMをスキャンするため、Ant Designのアクセシビリティ問題を検出できるが、ファイルと行番号を特定できない。このため、Ant Designのアクセシビリティ問題はツールの設定によって検出される可能性が異なる。

また、1:1のコントラスト比率のテキストがaxeで「incomplete」と分類される理由についても説明されている。axeは実際にレンダリングされた色chemeを評価するため、背景色が不明な場合、結果を「incomplete」として扱う。これは、誤検出を避けるための保守的なアプローチであり、しかし、CIパイプラインでは「incomplete」を無視する傾向があり、潜在的なアクセシビリティ問題が見逃される可能性がある。

さらに、暗黒モードでのアクセシビリティテストの重要性が強調されている。Playwrightとaxe-coreを組み合わせることで、暗黒モードでのアクセシビリティをテストすることができるが、CIパイプラインでは通常の色cheme（明るい）のみをテストするため、暗黒モードでの問題が見逃される可能性がある。このため、CIパイプラインでのテストを拡張し、暗黒モードでのアクセシビリティを評価する必要がある。

これらの点は、アクセシビリティツールの限界と、CIパイプラインでのテストの課題を示しており、アクセシビリティの確保にはツールの補完と手動テストの重要性が強調されている。

## 元記事一覧

- [Whyaxeandjsx-a11ymissAntDesignaccessibilitybugs...](https://dev.to/cstayyab/why-axe-and-jsx-a11y-miss-ant-design-accessibility-bugs-and-a-github-action-that-catches-them-cn0)
- [GitHub- cstayyab/antd-a11y-action·GitHub](https://github.com/cstayyab/antd-a11y-action)
- [Textat1:1contrastisnotanaxeviolation.Itisincomplete.](https://dev.to/henrique_yuri_f42f2fca47a/text-at-11-contrast-is-not-an-axe-violation-it-is-incomplete-436c)
- [How to test dark mode accessibility in CI with Playwright andaxe-core](https://dev.to/henrique_yuri_f42f2fca47a/how-to-test-dark-mode-accessibility-in-ci-with-playwright-and-axe-core-54lg)
- [Youraxerunisgreenandyourdarkmodehas1.04:1contrast](https://dev.to/henrique_yuri_f42f2fca47a/your-axe-run-is-green-and-your-dark-mode-has-1041-contrast-36i4)
