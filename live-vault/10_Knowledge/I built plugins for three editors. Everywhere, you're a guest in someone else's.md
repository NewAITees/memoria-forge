---
title: AIを活用した自愈テストとUI検出の課題
type: knowledge
status: draft
created: 2026-09-20
updated: 2026-09-20
confidence: medium
---

# AIを活用した自愈テストとUI検出の課題

## 結論

AIを活用した自愈テストは、UI変更に伴う選択器の破損を自動的に修正し、テストメンテナンス負担を最大で80％削減する効果があるが、テスト実行速度の低下や誤った修復の可能性があるため、視覚テストとの併用が推奨される。一方で、AIコードエージェントはUIデザインにおいて視覚的な変更を検出できず、微細なUIエラーを捕捉できないため、視覚テストの導入が不可欠である。これらの技術的課題と解決策は、開発効率と品質管理の向上に大きく貢献している。

## テーマ概要

テーマ「I built plugins for three editors. Everywhere, you're a guest in someone else's house」は、デザインツールのプラグイン開発における技術的課題と、AIを活用した自愈テストの導入が注目されている現状を反映しています。このテーマは、複数のエディタ（Sketch、Figma、Adobe XDなど）でプラグインを統一的に開発するための技術的挑戦、プラグイン環境の違いによる開発コストの増加、そしてUIの変更に伴うテストの維持コストの高さを背景にしています。特に、AIを活用した自愈テストは、UI変更に起因するテスト失敗を自動的に修正する技術として、企業での導入が進んでおり、テスト自動化の効率化と信頼性向上を実現するための重要な手段として注目されています。また、AIコードエージェントがUI設計において視覚的な変更を検出できないという課題も指摘されており、これに対応するための視覚テストの導入が求められています。

## 共通して確認できる点

複数の記事で共通して確認できた事実として、デザインツール向けのプラグイン開発において、各ツールが独自のAPIや開発環境を採用しているため、一括して複数のエディタで動作するプラグインを構築するのは技術的に困難であることが挙げられる。FigmaやAdobe XD、Sketchなどのツールでは、選択ノードの処理やUI制限、APIとの連携が開発の主要な課題となる。また、AIを活用した自愈テスト技術は、UI変更による選択器の破損を自動的に修復し、テストメンテナンス負担を大幅に削減する可能性がある。ただし、自愈テストはテスト実行速度の低下や誤った修復の可能性といった副作用を伴うため、他のテスト方法と併用することが推奨される。さらに、AIコードエージェントはバックエンド開発では効果的だが、UIデザインや視覚テストでは視覚的な変更を検出できないため、視覚テストの導入が求められる。

## 記事ごとの差分・視点の違い

記事「Is it possible to build plugins for multiple design tools with a single code base?」では、複数のデザインツール（Sketch、Figma、Adobe XD）向けにプラグインを開発する際の技術的課題と、単一のコードベースで複数ツールに適用する可能性について議論されている。筆者はDTPMというツールを紹介し、プラグイン開発の統一APIの必要性を強調している。一方で、「Use plugins in Claude」では、Claude AIが提供するプラグイン機能の利用方法と、共有プラグインの共有・アクセス方法が説明されており、主にプラグインの運用・共有に関する情報が中心となっている。

記事「Playwright Self-Healing Tests: How AI Fixes Broken Selectors (2026)」では、AIを活用した自愈テストの仕組みとその効果が詳細に説明されており、特にPlaywrightでの実装例や、AIが選択器を自動修正する仕組みに焦点を当てている。一方、「Self-Healing Tests: How AI Fixes Broken Playwright/Selenium Tests (2026)」は、自愈テストの実装コストとメリット・デメリットを比較し、実際のテストケースでの効果を示しながら、テスト自動化におけるAIの役割を検討している。

記事「Your coding agent can write the UI. It can't see that it broke it.」では、AIコードエージェントがUI変更を検出できず、UIデザインにおける微細なエラー（例：ボタンのサイズ変化、カードのレイアウト変化など）が検出されない問題点が指摘されており、視覚テストの必要性を強調している。この記事は、AIの制限と、UIテストにおける人間の検証の重要性を論じている。

## 深掘り調査で得られた知見

深掘り調査により、デザインツールのプラグイン開発における課題と、自愈テスト技術の現状が明らかとなった。Figma、Sketch、Adobe XDなどのエディタでは、それぞれ異なるAPI仕様や制限があり、単一のコードベースで複数のプラグインを構築するには、各プラットフォームの特性を理解し、柔軟な設計が求められる。特にFigmaでは、ノード選択やUI制限、APIとの連携が開発の中心課題となった。一方、自愈テストは、UI変更によって破綻する選択子をAIが自動的に修復する技術であり、PlaywrightやSeleniumでの導入が進んでいる。実装により、テストメンテナンス時間は60〜80％削減されるが、テスト実行速度の低下や誤修復の可能性があるため、視覚テストとの併用が推奨される。また、AIコードエージェントはバックエンド開発では有効だが、UIデザインでは視覚的検証が欠かせないため、変更の差分をクラウドで取得し、プルリクエストごとに比較する手法が提案されている。これらの技術動向は、開発効率と品質管理の向上に寄与している。

## 不確実な点・追加確認が必要な点

記事間の情報にはいくつかの不一致や不明点が確認されている。まず、記事1では2020年2月にDTPMがSketch、Figma、Adobe XDのプラグイン開発をサポートしていると記載されており、この時点ではInVision Studioのサポートは未実装だった。一方で、記事5は2026年2月頃の情報に基づき、AIコードエージェントがUI変更を検出できない問題を指摘している。このように、プラグイン開発やAIテスト技術の進化に伴い、情報のタイミングが異なるため、各記事の内容を単独で断定することは難しい。

また、記事3と記事4は2026年の情報として掲載されているが、具体的な公開日時や取得日時が不明であり、情報の信頼性や時系列的な位置づけを明確にするには追加調査が求められる。さらに、記事2の Claude プラグインに関する情報は、5日前の更新情報に基づいているが、その内容が他の記事と整合性を保つかは不明である。これらの点から、記事間の整合性を確認するためには、各記事の公開日時や取得日時を明確にしたうえで、時系列的に情報の新旧を比較する必要がある。

## 元記事一覧

- [Is it possible to build plugins for multiple design tools with a single code base? - DEV Community](https://dev.to/jody/is-it-possible-to-build-plugins-for-multiple-design-tools-with-a-single-code-base-49o4)
- [Use plugins in Claude | Claude Help Center](https://support.claude.com/en/articles/13837440-use-plugins-in-claude)
- [Playwright Self-Healing Tests: How AI Fixes Broken Selectors (2026)](https://playwright.aims-ai.com/blog/playwright-self-healing-locators)
- [Self-Healing Tests: How AI Fixes Broken Playwright/Selenium Tests (2026)](https://tayyabakmal.com/blog/self-healing-tests-ai-playwright-selenium/)
- [Your coding agent can write the UI. It can't see that it broke it. - DEV Community](https://dev.to/igrlk/your-coding-agent-can-write-the-ui-it-cant-see-that-it-broke-it-3bi)
