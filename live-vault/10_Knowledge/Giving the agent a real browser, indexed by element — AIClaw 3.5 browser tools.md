---
title: AIClaw 3.5 でブラウザを実行する際のライブラリ問題解説
type: knowledge
status: draft
created: 2026-09-29
updated: 2026-09-29
confidence: medium
---

# AIClaw 3.5 でブラウザを実行する際のライブラリ問題解説

## 結論

Playwright を利用する際、`libnspr4.so` などの共有ライブラリの不足は、特に制限された環境やサーバーレス環境で発生する典型的な問題であり、その解決には `apt-get download` と `dpkg-deb` を用いたローカルでのライブラリ展開や `LD_LIBRARY_PATH` の適切な設定が不可欠である。また、Vercel や類似のプラットフォームでは、`@sparticuz/chromium` と `playwright-core` の組み合わせを活用することで、依存関係の制限を回避し、安定した実行が可能となる。

## テーマ概要

Playwright は、AI エージェントが本物のブラウザを操作するためのツールとして注目されており、特に「Giving the agent a real browser, indexed by element — AIClaw 3.5 browser tools」といったテーマで議論されています。この背景には、AI がウェブページの要素を正確に識別・操作する必要性があり、そのためには本物のブラウザ環境が不可欠です。しかし、Playwright を使用する際には、`libnspr4.so` などの共有ライブラリの欠如により、実行中にエラーが発生する問題が頻繁に報告されています。特に、制限された環境（コンテナ、CI ランナー、Vercel など）では、管理者権限がないため、通常のインストール手順が適用できません。このような問題に対して、`apt-get download` や `dpkg-deb` を用いたローカルでのライブラリ展開、`LD_LIBRARY_PATH` の設定など、複数の解決策が提案されています。また、`sparticuz/chromium` などのパッケージの利用により、Vercel などのサーバーレス環境での実行が可能となるケースも確認されています。これらの技術的課題とその解決策は、AI エージェントが実際のブラウザ環境を操作するための実装において重要な要素となっています。

## 共通して確認できる点

Playwright を使用する際、`libnspr4.so` などの共有ライブラリが見つからないエラーが発生することが確認されています。この問題は、`apt-get install` を使用して必要なライブラリをインストールしようとする際に、管理者権限がない環境で発生するケースが多いため、特にコンテナや CI ランナー、Render/Replit/Streamlit Cloud などの制限された環境で頻繁に見られます。このような環境では、`apt-get download` を使用して `.deb` ファイルを取得し、`dpkg-deb -x` でローカルディレクトリに展開することで、管理者権限なしにライブラリをインストールすることが可能とされています。また、`LD_LIBRARY_PATH` 環境変数にライブラリのディレクトリを設定することで、アプリケーションが必要なライブラリを検索できるようにする方法も提案されています。さらに、`npx playwright install-deps chromium --dry-run` を使用して必要なパッケージリストを動的に取得し、手動で `apt-get download` を行う方法も紹介されています。これらの対策は、制限された環境で Playwright を使用する際の解決策として広く採用されています。

## 記事ごとの差分・視点の違い

記事ごとの立場や強調点、論点の違いは以下の通りです。

記事1は、管理者権限がない環境でのPlaywrightインストールにおける`libnspr4.so`のエラー解決策を提供しています。この記事では、`apt-get install`が管理者権限を必要とすることを前提に、代替手段として`apt-get download`と`dpkg-deb`を活用した方法を提案しています。また、この問題は制限された環境（コンテナ、CIランナーなど）でよく発生し、解決策としてスクリプト化による自動化が推奨されています。

記事2は、Ubuntu 24.04環境でのPlaywrightインストールにおけるシステム依存関係の欠如に関する問題を報告しています。この記事では、特定の環境でのみ発生する問題として、他の環境では問題がないという点を強調しており、依存関係のインストールが成功している場合の背景も示しています。

記事3は、Vercel上でのChromiumの実行における`libnspr4.so`のエラーを解決するためのガイドとして、Playwrightの使用を制限し、`playwright-core`と`@sparticuz/chromium`の組み合わせを推奨しています。この記事では、Vercelの制限（50MBの制限）と、サーバーレス環境での実行に適した解決策を強調しています。

記事4は、一般的な`libnspr4.so`のエラーを解決するための方法を紹介しており、Linux環境での共有ライブラリの問題を幅広く扱っています。この記事では、`LD_LIBRARY_PATH`の設定や、ライブラリファイルの存在確認といった基本的な解決策を提示しています。

記事5は、`libnspr4.so`が見つからない問題のリポジトリでの報告であり、特定の環境（Sparticuz/chromiumの使用）における問題として、他の要因が原因である可能性を示唆しています。この記事では、問題の原因が`sparticuz/chromium`ではなく、他の要因である可能性を指摘しており、問題の解決に向けた方向性を示しています。

## 深掘り調査で得られた知見

Playwright を使用する際、`libnspr4.so` などの共有ライブラリが見つからないエラーが発生する問題は、特に制限された環境（コンテナ、CI ランナー、Render/Replit/Streamlit Cloud など）で頻繁に発生しています。この問題は、`apt-get install` を使用する必要があるため、管理者権限がない環境では解決が困難です。その対処法として、`apt-get download` を用いて `.deb` ファイルを取得し、`dpkg-deb -x` でローカルディレクトリに展開することで、管理者権限なしにライブラリをインストールする方法が提案されています。また、`LD_LIBRARY_PATH` 環境変数にライブラリのディレクトリを設定することで、アプリケーションが必要なライブラリを検索できるようになります。

Vercel などのサーバーレス環境では、`sparticuz/chromium` が `AWS_LAMBDA_JS_RUNTIME` 環境変数をチェックするタイミングが原因で、エラーが発生することがあります。この問題を解決するためには、環境変数を Vercel ダッシュボードで設定し、コード内で設定するよりも早めに読み込まれるようにする必要があります。また、`LD_LIBRARY_PATH` を Chromium の実行ファイルとライブラリが存在するディレクトリに設定することで、共有ライブラリの読み込みが成功します。

これらの対処法は、制限された環境での Playwright の使用を可能にするための実用的な解決策として広く採用されており、特に AI コード作成エージェントやブラウザ操作を必要とするツールの開発において重要です。

## 不確実な点・追加確認が必要な点

記事間の食い違いや、資料からは断定できない点を具体的に書くと、以下の通りです。

各記事では「libnspr4.so」などの共有ライブラリの欠如に関する問題が取り上げられていますが、具体的な原因や解決策の背景にはある程度の違いがあります。記事1では、管理者権限がない環境でのPlaywrightインストールにおける共有ライブラリの不足が問題であり、`apt-get download`や`dpkg-deb`を使用したローカルでのライブラリ展開が推奨されています。一方、記事3では、Vercel環境でのPlaywrightとChromiumの利用に関する問題が焦点となっており、`LD_LIBRARY_PATH`の設定や、`@sparticuz/chromium`の使用が解決策として提示されています。また、記事5では、`libnspr4.so`の欠如がSparticuz/chromiumパッケージの問題ではない可能性が指摘されており、環境設定や依存関係の構成が原因である可能性が示唆されています。

これらの記事は、それぞれ異なる環境や設定下での問題解決策を提示しており、一概にどの方法が最適であるとは言えません。また、記事2や記事4では、共有ライブラリの不足が一般的なLinux環境での問題として取り上げられており、`apt-get`や`LD_LIBRARY_PATH`の設定が一般的な解決策として紹介されています。しかし、すべての記事が同一の環境や状況を想定しているわけではなく、それぞれの文脈に応じた解決策が提案されています。そのため、特定の環境や設定に合わせて、適切な解決策を選択する必要があります。

## 元記事一覧

- [Fixing "errorwhile loading shared libraries:libnspr4.so" for...](https://dev.to/loosechangelabs/fixing-error-while-loading-shared-libraries-libnspr4so-for-playwright-with-no-root-access-2fg0)
- [Playwright install fails on Ubuntu 24.04 due to missing ...](https://stackoverflow.com/questions/79597399/playwright-install-fails-on-ubuntu-24-04-due-to-missing-system-dependencies-eve)
- [How to Fix Chromium on Vercel: A Complete Guide to Solving ...](https://dev.to/qudratullahdev/how-to-fix-chromium-on-vercel-a-complete-guide-to-solving-the-libnspr4so-error-4i9j)
- [How to Fix “error while loading shared libraries: cannot open ...](https://allthings.how/how-to-fix-error-while-loading-shared-libraries-cannot-open-shared-object-file-no-such-file-or-directory/)
- [[BUG] missing `libnspr4.so` · Issue #343 · Sparticuz/chromium](https://github.com/Sparticuz/chromium/issues/343)
