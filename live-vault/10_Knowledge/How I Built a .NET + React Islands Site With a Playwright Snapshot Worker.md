---
title: .NETとReact Islandsで構築するサイトの技術解説
type: knowledge
status: draft
created: 2026-10-22
updated: 2026-10-22
confidence: medium
---

# .NETとReact Islandsで構築するサイトの技術解説

## 結論

.NETとReact Islandsを組み合わせたサイトの構築方法は、SEO対策とユーザー体験の両立を目指す新しいアプローチとして注目されており、ASP.NET Core 10 Razor Pages、React islands、PostgreSQL、およびNode.jsとPlaywrightを組み合わせたバックグラウンドワーカーによって実現されている。この技術は、ブラウザの実行を公開時に移動させ、Razor PagesでHTMLを生成し、Playwrightを用いたバックグラウンドプロセスでReactの島をレンダリングし、結果をPostgreSQLに保存することで、パフォーマンスとコストを最適化している。

## テーマ概要

.NETとReact Islandsを組み合わせたサイトの構築方法についての記事は、2026年9月に公開された。この技術は、検索エンジン向けにクロール可能なHTMLを生成し、同時にユーザーのブラウザでReactのハイドレーションを行うことで、SEOとユーザー体験の両立を目指している。このアプローチは、ASP.NET Core 10 Razor Pages、React Islands、PostgreSQL、およびNode.jsとPlaywrightを組み合わせたバックグラウンドワーカーによって実現されている。この技術は、ブラウザでのレンダリングを訪問者ごとに実行するのではなく、公開時点でブラウザを実行し、HTMLを生成して保存することで、パフォーマンスとコストを最適化している。このような技術は、特に高負荷のウェブサイトや、検索エンジン最適化（SEO）とインタラクティブなUIを両立させる必要があるプロジェクトにおいて注目されている。

## 共通して確認できる点

複数の記事で共通して確認できた事実として、ASP.NET CoreとReact Islandsを組み合わせた技術スタックが、SEO対策とユーザー体験のバランスを取るための新しいアプローチとして注目されている。このアプローチでは、ブラウザの実行を公開時に移し、Razor PagesでHTMLを生成し、その後にPlaywrightを用いたバックグラウンドプロセスでReactの島（islands）をレンダリングし、結果をPostgreSQLに保存する。公開されたHTMLは、訪問者に提供され、ブラウザがそのHTMLをhydratingしてインタラクティブなUIを構築する。この方法は、サーバーサイドレンダリング（SSR）ではなく、ブラウザでレンダリングされたReactを使用し、Chromiumは訪問者のリクエストパスに含まれない。また、このアプローチは、コンテンツとコントロールの区別を重視し、Razorはコンテンツを、Reactはインタラクティブなコントロールをそれぞれ担当する。このような設計により、検索エンジン対応とユーザー体験の両立が可能となる。

## 記事ごとの差分・視点の違い

記事「How I Built a .NET + React Islands Site With a Playwright Snapshot Worker」では、ASP.NET Core 10 Razor PagesとReact islandsを組み合わせて、検索エンジン対応とユーザー体験を両立させるためのアーキテクチャ設計が重点となる。この記事では、ブラウザの実行を公開時に移動させ、ChromiumプロセスでReactコンポーネントをレンダリングし、結果をPostgreSQLに保存する仕組みが説明されている。また、公開されたHTMLは直接クライアントに送信され、JavaScriptでインタラクションが実現されるという点が特徴的である。

記事「React Powered Pages with ASP.NET Core and Playwright」では、Reactを用いたページがHTMLにコンテンツを事前に含ませることで、ブラウザでのJavaScript実行を省略する仕組みが強調されている。このアプローチは、検索エンジンの可検索性を確保しつつ、ユーザー体験を保つための技術として位置づけられている。また、この記事では、SSR（サーバーサイドレンダリング）、SSG（スタティックサイトジェネレーション）、ISR（インクリメンタルスタティック再生）、PPR（部分ページ再取得）などの技術と比較しながら、このアプローチの利点と課題が論じられている。

記事「BootstrapforBlazor:Stylingthe Task Tracker」では、BlazorアプリケーションにBootstrapを適用することで、UIの見た目の改善が図られている。この記事では、BootstrapのCSSフレームワークを活用し、ナビバー、カード、ボタンなどのUIコンポーネントを簡単に実装できる点が強調されている。また、Bootstrapのグリッドシステムやレイアウトの仕組みが説明され、Blazorアプリケーションの見た目を美しくするための方法が示されている。

記事「Blazor Fundamentals: Making the Task Tracker Interactive」では、Blazorを用いてタスクトラッカーのUIをインタラクティブにする方法が説明されている。この記事では、C#を用いた@onclickや@bindなどのディレクティブにより、JavaScriptを用いないでDOMイベントを処理する仕組みが解説されており、BlazorがJavaScriptに依存しないWebアプリケーション開発を可能にする点が強調されている。また、Blazorの2つのホストモデルであるBlazor ServerとBlazor WebAssemblyの違いについても触れられており、それぞれの特徴と選択肢が論じられている。

記事「RazorSyntaxFundamentals:RenderingtheTaskTracker」では、Razorの基本的な構文とその使い方について説明されている。この記事では、RazorがHTMLとC#を混在させることで、単一ファイルでUI構造と論理を記述できる点が強調されており、ASP.NET Core MVCやBlazorなどのフレームワークで使用されるRazorの特徴が解説されている。また、Razorがコンパイル時に変換され、生成されたC#クラスが実行される仕組みについても触れられており、動的なWebページ生成の仕組みが説明されている。

## 深掘り調査で得られた知見

RazorはASP.NET Core MVCで導入され、ASPXとの比較で簡潔な構文が特徴である。Razorは@記号を用いてC#モードに切り替わり、HTMLとC#の混在を可能にする。これにより、単一ファイルでUI構造と論理を記述できる。Razorはコンパイル時に変換され、生成されたC#クラスが実行される。これにより、動的なWebページを生成することができる。Razorは@modelディレクティブを用いてビューが期待するモデルを指定し、データバインディングを実現する。また、RazorはBlazorでも使用され、C#を用いてインタラクティブなWeb UIを構築するためのフレームワークとして機能している。  

同様に、React islandsはASP.NET Coreと組み合わせて使用され、Reactコンポーネントをページ内に埋め込むことで、パフォーマンスとSEOのバランスを取る手法として注目されている。このアプローチでは、Razorで生成されたHTMLにReactコンポーネントを埋め込み、ブラウザでJavaScriptが実行されるようにする。これにより、検索エンジンが最初のHTMLを読み取ることができ、ユーザーがページにアクセスした際にはReactがDOMをハイドレートしてインタラクティブなUIを提供する。  

また、PlaywrightはNode.jsベースの自動化ツールであり、ブラウザを操作してページをレンダリングし、その結果をスナップショットとして保存する。この技術は、ASP.NET Coreと組み合わせて使用され、サーバーサイドでHTMLを生成し、Reactコンポーネントを埋め込むことで、SEO対策とユーザー体験の両立を図る。Playwrightは、ブラウザを起動し、JavaScriptを実行してページをレンダリングし、その結果を保存する。これにより、検索エンジンが最初のHTMLを読み取ることができ、ユーザーがページにアクセスした際にはReactがDOMをハイドレートしてインタラクティブなUIを提供する。  

このアプローチは、Reactのサーバーサイドレンダリング（SSR）とは異なり、ブラウザでJavaScriptが実行されるため、パフォーマンスとSEOのバランスを取る。また、Playwrightは、ブラウザを起動し、JavaScriptを実行してページをレンダリングし、その結果を保存する。これにより、検索エンジンが最初のHTMLを読み取ることができ、ユーザーがページにアクセスした際にはReactがDOMをハイドレートしてインタラクティブなUIを提供する。  

この技術は、ホテルやエディトリアルサイトなど、コンテンツが豊富でインタラクティブな要素を含むサイトに特に有効である。Razorで生成されたHTMLにReactコンポーネントを埋め込み、Playwrightでレンダリングし、その結果を保存することで、検索エンジンが最初のHTMLを読み取ることができ、ユーザーがページにアクセスした際にはReactがDOMをハイドレートしてインタラクティブなUIを提供する。このアプローチは、SEO対策とユーザー体験の両立を図るための一つの解決策として注目されている。

## 不確実な点・追加確認が必要な点

記事間では、技術スタックや実装の目的、およびアーキテクチャの設計に関するいくつかの違いや曖昧な点が確認されている。まず、記事1と記事2は同一名前のプロジェクトについて書かれているが、記事1ではASP.NET Core 10 Razor Pages、React islands、PostgreSQL、Node/Playwright workerを用いたホテルとエディトリアルサイトの構築が記述されている。一方で記事2は、React powered pagesを実現するためのアプローチとして、ASP.NET Core、Razor Pages、React islands、Playwright snapshot workerを用いた方法が説明されており、具体的なプロジェクト名や目的は記述されていない。このため、記事1と記事2は同一のプロジェクトを扱っている可能性があるが、詳細な情報が不足しているため断定できない。

また、記事4と記事5はBlazorを用いたタスクトラッカーの実装について述べており、記事5ではRazor構文を用いてタスクトラッカーのUIを生成し、機能的なインターフェースを実現していることが説明されている。一方で記事4では、Blazorを用いてタスクトラッカーをインタラクティブにし、Bootstrapを適用して見た目の改善を行っていることが記述されている。このため、記事4と記事5は同一体系のプロジェクトを扱っている可能性が高いが、具体的な関連性や時系列的な順序については明確な説明が見られない。

さらに、記事3はBlazorアプリケーションにBootstrapを適用する方法について述べており、BootstrapがCSSフレームワークとして提供するレイアウトやUIコンポーネントの利用方法が説明されている。この記事は他の記事とは異なるテーマを扱っているが、BlazorとBootstrapの関連性を示す重要な情報として位置づけられる。しかし、記事3は他の記事との関連性や時系列的な位置づけが明確でないため、全体の構成を把握するにはさらなる情報が必要である。

これらの記事は、.NET技術スタックにおける異なるアプローチや実装方法を示しており、それぞれが独自の目的と設計思想を持っている可能性がある。しかし、記事間の関連性や時系列的な順序についての明確な情報は不足しているため、断定的な結論を導き出すことは困難である。

## 元記事一覧

- [How I Built a .NET + React Islands Site With a Playwright ...](https://dev.to/frorning/how-i-built-a-net-react-islands-site-with-a-playwright-snapshot-worker-56h7)
- [React Powered Pages with ASP.NET Core and Playwright](https://www.linkedin.com/posts/piyushchauhan2011_how-i-built-a-net-react-islands-site-with-activity-7509637917967970304-g0e2)
- [BootstrapforBlazor:Stylingthe Task Tracker - DEV Community](https://dev.to/manoharij/bootstrap-for-blazor-styling-the-task-tracker-3po9)
- [Blazor Fundamentals: Making the Task Tracker Interactive](https://dev.to/manoharij/blazor-fundamentals-making-the-task-tracker-interactive-2iha)
- [RazorSyntaxFundamentals:RenderingtheTaskTracker](https://dev.to/manoharij/razor-syntax-fundamentals-rendering-the-task-tracker-34o7)
