---
title: Eventra CLIがVue・Svelte・Astroをサポートするまでに
type: knowledge
status: draft
created: 2026-10-18
updated: 2026-10-18
confidence: medium
---

# Eventra CLIがVue・Svelte・Astroをサポートするまでに

## 結論

EventraのCLIは、JavaScript/TypeScriptのコードベースをスキャンし、実際に使用されている機能を特定する機能を持っていますが、Vue、Svelte、Astroなどのフレームワークで使用されるファイル形式（.vue、.svelte、.astro）は、CLIのコアエンジンが認識しないため解析対象から除外されていました。この問題は、各フレームワークごとに別個のプラグインを追加することで解決され、フレームワークのファイル形式をTypeScriptの仮想モジュールに変換し、コアエンジンが処理できるようにする仕組みが導入されました。これにより、CLIのコアエンジンにフレームワークの知識を教える必要がなく、拡張性が高まりました。2026年8月21日に、この改善が実装されたことがTechspindle.aiの記事で報告されています。

## テーマ概要

EventraのCLIツールは、JavaScript/TypeScriptのコードベースをスキャンし、どの機能が実際に使用されているかを分析する機能を持っています。しかし、Vue、Svelte、Astroなどのフレームワークで使用されるファイル形式（.vue、.svelte、.astro）は、CLIのコアエンジンが認識しないため、解析対象から除外されていました。これにより、これらのフレームワークを使用しているプロジェクトでは、コードの使用状況が正確に把握できず、不要なコードの除去が困難な状況がありました。この問題は、CLIのコアエンジンを変更することなく、各フレームワークごとに別個のプラグインを追加することで解決されました。各プラグインは、フレームワークのファイル形式をTypeScriptの仮想モジュールに変換し、コアエンジンがそれらを処理できるようにするという仕組みです。この改善により、EventraのCLIはVue、Svelte、Astroをサポートし、フレームワークごとの解析が可能となりました。2026年8月21日に、この機能拡張が実装されたことがTechspindle.aiの記事で報告されており、フレームワークの多様化に伴う開発環境の柔軟性向上が求められている背景があります。

## 共通して確認できる点

EventraのCLIは、JavaScript/TypeScriptのコードベースをスキャンし、どの機能が実際に使用されているかを報告するツールとして設計されていました。しかし、Vue、Svelte、Astroなどのフレームワークのファイル形式（.vue、.svelte、.astro）は、CLIのコアエンジンが認識しないため、解析対象から除外されていました。これにより、フレームワークを採用しているプロジェクトでは、CLIがこれらのファイルを無視してスキャン結果を出力してしまうという問題がありました。Techspindle.aiの記事では、2026年8月21日にEventraのCLIがVue、Svelte、Astroをサポートするようになったことが記載されており、この改善により、フレームワークごとに別個のプラグインを追加することで、コアエンジンに直接変更を加えることなく、解析対象を拡張することができました。各プラグインは、フレームワークのファイル形式をTypeScriptの仮想モジュールに変換し、コアエンジンがそれらを処理できるようにするという仕組みでした。これにより、CLIのコアエンジンはフレームワークの知識を必要とせず、拡張性が高まりました。Dev.toの記事では、2024年7月4日にEventra.devのCLIがVue、Svelte、Astroをサポートするための改善が進められていることが記載されており、この改善はCLIのコアエンジンに影響を与えることなく、フレームワークごとに独立した処理を実行できるようにしました。

## 記事ごとの差分・視点の違い

記事「Your feature-usage scanner doesn't know Vue, Svelte, or Astro exist. Here's how we fixed that without touching its core」では、EventraのCLIがJavaScript/TypeScriptのコードベースをスキャンする際、Vue、Svelte、Astroなどのフレームワークのファイル形式を認識できず、解析対象から除外されていた問題を解決した具体的な方法が説明されている。この記事では、CLIのコアエンジンに直接変更を加えることなく、各フレームワークごとに別個のプラグインを追加することで、フレームワークのファイル形式をTypeScriptの仮想モジュールに変換し、コアエンジンが処理できるようにした点が強調されている。また、この解決策がCLIのコアエンジンにフレームワークの知識を教える必要がなく、拡張性が高まった点にも注目されている。

記事「Your feature-usage scanner doesn't know Vue, Svelte, or Astro ...」では、Techspindle.aiがEventraのCLIがVue、Svelte、Astroをサポートするようになったことを報じており、この改善が2026年8月21日に実施されたことが明記されている。この記事では、技術的な改善だけでなく、その影響が実際の開発プロセスやプロジェクトに与える価値についても言及しており、ImpactとInnovationという観点からその重要性を強調している。また、この改善が開発者にとってどのような利点をもたらすかを、読者に理解を促す形で説明している。

## 深掘り調査で得られた知見

EventraのCLIは、JavaScript/TypeScriptのコードベースをスキャンし、どの機能が実際に使用されているかを報告するツールとして設計されていたが、Vue、Svelte、Astroなどのフレームワークのファイル形式（.vue、.svelte、.astro）は、CLIのコアエンジンが認識しないため解析対象から除外されていた。この問題は、CLIのコアエンジンに直接変更を加えることなく、各フレームワークごとに別個のプラグインを追加することで解決された。各プラグインは、フレームワークのファイル形式をTypeScriptの仮想モジュールに変換し、コアエンジイがそれらを処理できるようにする。この解決策は、CLIのコアエンジンにフレームワークの知識を教える必要がなく、フレームワークごとに独立した処理を実行できるため、拡張性が高まった。Techspindle.aiの記事では、2026年8月21日にEventraのCLIがVue、Svelte、Astroをサポートするようになったことが記載されている。一方、Dev.toの記事では、2024年7月4日にEventra.devのCLIがVue、Svelte、Astroをサポートするための改善が進められていることが記載されている。

## 不確実な点・追加確認が必要な点

記事間の食い違いとしては、記事1と記事2においてEventraのCLIがVue、Svelte、Astroをサポートしたタイミングが異なっている点が挙げられる。記事1ではDev.toの記事に記載されている2024年7月4日に改善が進められていることが記載されているのに対し、記事2ではTechspindle.aiの記事に記載されている2026年8月21日にサポートが開始されたことが示されている。このことから、改善の進捗やリリースタイミングに差がある可能性がある。また、記事1ではCLIのコアエンジンに直接変更を加えることなく、各フレームワークごとに別個のプラグインを追加することで解決したとされているが、記事2ではこの解決策が採用されたことが明記されていないため、どの記事が正確な情報を提供しているかは不明である。さらに、記事5においては「Lying Prose」問題に対する解決策としてカスタムCIリンターの導入が述べられているが、その実装内容や具体的な効果については詳細が不足している。これらの点から、各記事の内容を比較・検証する必要がある。

## 元記事一覧

- [Your feature-usagescannerdoesn't knowVue,Svelte, orAstroexist.](https://dev.to/__c500e8ac9bc2/your-feature-usage-scanner-doesnt-know-vue-svelte-or-astro-exist-heres-how-we-fixed-that-1eif)
- [Your feature-usage scanner doesn't know Vue, Svelte, or Astro ...](https://www.techspindle.ai/story/55083)
- [ContractMonthCodes](https://www.cmegroup.com/month-codes.html)
- [Smartcontracts: What are they and their benefits | ethereum.org](https://ethereum.org/smart-contracts/)
- [The"LyingProse"Problem:WhyWeBuiltaCustomCILinterto...](https://dev.to/cksmct/the-lying-prose-problem-why-we-built-a-custom-ci-linter-to-stop-documentation-from-contradicting-322g)
