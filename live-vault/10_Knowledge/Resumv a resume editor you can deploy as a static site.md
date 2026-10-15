---
title: Resumv: 静的サイトでデプロイ可能な履歴書編集ツール
type: knowledge
status: draft
created: 2026-10-15
updated: 2026-10-15
confidence: medium
---

# Resumv: 静的サイトでデプロイ可能な履歴書編集ツール

## 結論

Resumvは、静的サイトとしてデプロイ可能なオープンソースの履歴書編集ツールであり、AstroとReactを技術スタックとして採用している。ユーザーはブラウザ上で履歴書を編集・出力でき、サーバーに依存せずローカルストレージを使用してデータを保存する。PDF、DOCX、Markdown、JSONなどの形式での出力が可能で、プライバシーを重視した設計がなされている。

## テーマ概要

Resumvは、静的サイトとしてデプロイ可能なオープンソースの履歴書編集ツールであり、AstroとReactを技術スタックとして採用している。このツールは、ユーザーがブラウザ上で履歴書を編集・出力できるようにし、サーバー側に依存せずローカルストレージを使用してデータを保存する点が特徴である。ResumvはMITライセンスで公開されており、PDF、DOCX、Markdown、JSONなどの形式での出力が可能で、プライバシーを重視した設計がなされている。また、履歴書のテンプレートやサンプルを含み、カバーレター編集やキャリアアドバイスなどの機能も備えている。このような特徴から、静的サイトのホスティングを検討している開発者や、プライバシーを重視するユーザーから注目されている。

## 共通して確認できる点

Resumvは、AstroとReactをベースに構築されたオープンソースの履歴書編集ツールであり、静的サイトとしてデプロイすることが可能である。このツールは、Reactive Resumeの15のテンプレートやPDFレンダリング機能、スキーマ、サンプル履歴書をベースにした独立した実装であり、公式リリースとは異なる。履歴書の編集と出力はすべてブラウザ上で行われ、サーバー側に依存しない。PDFの生成やプレビュー、DOCX、Markdown、JSONの出力もすべてクライアントサイドで実行される。ローカルストレージを使用しているため、クラウド同期や暗号化された保存はできない。Resumvは、プライバシーを重視しており、オンライン履歴書プラットフォームから履歴書を離すことで設計されており、自前の履歴書ビルダーのホスティングを目的としている。Node.js 22.12またはそれ以降とBunをインストールした環境で、git cloneとnpm install、npm run buildコマンドにより構築が可能で、生成されたdistディレクトリを静的ウェブサーバーで提供することでデプロイが可能である。

## 記事ごとの差分・視点の違い

記事「Resumv: a resume editor you can deploy as a static...」では、Resumvが静的サイトとしてデプロイ可能であるという点を強調し、AstroとReactを用いた技術スタックや、ローカルストレージでの履歴書保存、PDFやDOCXなどの出力方法が主な論点となっている。また、プライバシーへの配慮や、クラウドに依存せず自前のホスティングを目的としている点も強調されている。一方、「ResumvAlternatives and Reviews」では、Resumvの代替製品や評価情報が紹介されており、Resumv自体の技術的詳細よりも、市場での位置付けやユーザーからの評価に焦点が当てられている。また、ResumvがTypeScriptで開発されていることや、MITライセンスによるオープンソースとしての特徴も触れている。記事「How I Built a 50-State US Statutory Probate Calculator with ...」では、Resumvの技術スタックや静的サイトデプロイの概念を参考にした、別のプロジェクトの開発経緯が記載されており、Resumvの技術的アプローチが他のプロジェクトにも影響を与えていることを示している。記事「Installing TailwindCSS with Vite」は、Tailwind CSSのインストール方法やViteでの導入について技術的な説明が中心で、Resumvと直接的な関連は少ないが、技術スタックの一部として関連性がある。記事「How SkyBuild Technologies Built EduSky: Scalable School Management System」では、Resumvの技術スタック（AstroやReact）が他のプロジェクトにも応用されていることを示しており、Resumvの技術的影響力が広がっていることを示している。

## 深掘り調査で得られた知見

Resumvは、AstroとReactを組み合わせた静的サイトとしてのデプロイが可能であるオープンソースの履歴書編集ツールであり、MITライセンスで公開されている。このツールは、Reactive ResumeのテンプレートやPDFレンダリング機能を適応させた独立した実装であり、公式リリースとは異なる。履歴書の編集と出力はすべてブラウザ上で行われ、サーバーに依存しない。PDFの生成やプレビュー、DOCX、Markdown、JSONの出力もすべてクライアントサイドで処理される。ローカルストレージを使用しているため、クラウド同期や暗号化された保存は行えない。Resumvは、履歴書の編集に加えて、カバーレターの作成や履歴書チェック、キャリアアドバイス、要約作成ツールなども提供している。プライバシーを重視しており、オンライン履歴書プラットフォームから履歴書を離すことで設計されており、自前の履歴書ビルダーのホスティングを目的としている。Node.js 22.12以降とBunをインストールした環境で構築可能で、git cloneとnpm install、npm run buildコマンドによりビルドが行える。生成されたdistディレクトリを静的ウェブサーバーで提供することでデプロイが可能である。ローカルストレージはブラウザプロファイルとオリジンに依存しており、データの消失リスクがある。PDFプレビューはPDF出力の参考となるが、DOCXは装飾やページ送りが異なる可能性がある。現在はラテン文字スクリプトの履歴書に主にサポートされており、中国語のフォントサポートは未実装である。テンプレートカードの選択により、そのテンプレートの完全な例が読み込まれるが、編集履歴の復元やJSONバックアップの導入が推奨されている。履歴書の内容は外部のAIプロバイダーやバックエンドに送信されず、フォントはローカルにバンドルされている。GitHubのスター数や最新のmainコミットはセッションストレージで15分間キャッシュされ、履歴書の内容はGitHubに送信されない。Resumvは、プライバシーを重視し、オンライン履歴書プラットフォームから履歴書を離すことで設計されており、自前の履歴書ビルダーのホスティングを目的としている。

## 不確実な点・追加確認が必要な点

記事間では、Resumvに関する情報がいくつかの矛盾や曖昧な点を含んでおり、断定的な記述は避けたほうがよい。例えば、記事1ではResumvがAstroとReactを用いて構築され、静的サイトとしてデプロイ可能であると明記されているが、記事2では「liusha-com/resumvはオープンソースプロジェクトでMITライセンスで許可されている」と記述されており、技術スタックやライセンス情報の整合性が確認できない。また、記事3の「US Probate Calculator」はAstroとTailwind CSSを用いているとされているが、Resumvとの関連性は明示されていない。さらに、記事4のTailwind CSSのインストール方法や記事5のEduSkyの技術スタックは、Resumvの開発に直接関係するものではなく、技術的な背景情報としてのみ提供されている。したがって、Resumvの技術的特徴や構築方法について正確な断定を行うには、さらなる情報の収集や確認が必要である。

## 元記事一覧

- [Resumv: aresumeeditor you can deploy as a static... - DEV Community](https://dev.to/help_gud/resumv-a-resume-editor-you-can-deploy-as-a-static-site-55k2)
- [ResumvAlternatives and Reviews](https://www.libhunt.com/r/resumv)
- [How I Built a 50-State US Statutory Probate Calculator with ...](https://dev.to/logicpilgrim/how-i-built-a-50-state-us-statutory-probate-calculator-with-astro-and-tailwind-css-3p0b)
- [InstallingTailwindCSSwith Vite -TailwindCSS](https://tailwindcss.com/docs/installation/using-vite)
- [HowSkyBuildTechnologiesBuiltEduSky:ScalableSchool...](https://dev.to/sb-tech/how-skybuild-technologies-built-edusky-scalable-school-management-system-1dc6)
