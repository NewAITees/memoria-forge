---
title: 純CSSでラーダーチャートを実装する技術
type: knowledge
status: draft
created: 2026-10-17
updated: 2026-10-17
confidence: medium
---

# 純CSSでラーダーチャートを実装する技術

## 結論

Pure CSSでラーダーチャートを描画する技術は、SVGやJavaScriptライブラリに依存せず、CSS変数と`clip-path: polygon()`を活用することで軽量かつ高性能な実装が可能である。st-core.fscss v2では、配列形式でデータを処理し、CSSカスタムプロパティを出力してポリゴンを描画し、リングやスポークをグラデーションで生成する手法が採用されており、コンパイル後のCSSファイルは約1キロバイトと非常に軽量である。この技術は、製品UIや現代のダッシュボードに適したスタイルとして位置付けられており、JavaScriptライブラリに依存することなく、CSSの柔軟性とパフォーマンスを活かした新しい表現として注目されている。

## テーマ概要

Pure CSSでラーダーチャートを描画する技術は、SVGやJavaScriptライブラリを使わずに軽量かつ高性能な表現を実現するため、注目を集めています。st-core.fscss v2では、CSS変数と`clip-path: polygon()`を活用し、配列形式でデータを処理することで、ポリゴンを描画し、リングやスポークをグラデーションで生成しています。これにより、現代のダッシュボードや製品UIに適したスタイルが可能となり、JavaScriptライブラリに依存することなく、コンパイルされたCSSで描画が可能です。また、アニメーションは`transition: clip-path`で実現でき、コンパイル後のCSSファイルは1キロバイト程度と非常に軽量です。このような技術は、CSSの柔軟性とパフォーマンスを活かした新しい表現として、今注目されています。

## 共通して確認できる点

FSCSSを用いた純CSSでのラーダーチャートの実装は、SVGやJavaScriptライブラリを一切使用せずに、CSS変数と`clip-path: polygon()`を活用することで実現されています。この技術は、st-core.fscssというFSCSSモジュールにおいて、配列形式でデータを扱い、CSSカスタムプロパティを出力することで、ポリゴンを画面に描画しています。最大半径はボックスの42%として設定され、アニメーションは`transition: clip-path`で実現可能です。コンパイル後のCSSサイズは約1キロバイトと非常に軽量で、ページの描画に際してJavaScriptライブラリを一切使用しないため、パフォーマンスが非常に高いとされています。また、複数のシリーズを描画する場合、各シリーズに対して1つのホストを割り当てる必要があり、これは多系列のラインチャートと同様のパターンです。ラーダーチャートでは、CSS変数を用いて値を保存し、fill、line、dotsなどのスタイルがそれらを継承することで、柔軟な表現が可能です。また、`clip-path: polygon()`は形状を埋めることは可能ですが、ストロークを描画することはできないため、FSCSSの配列メソッドを用いたダブルパス技術が採用されています。この技術は、データを前進方向と後進方向で処理し、線幅分の平行なエッジを生成することで、薄い帯状の領域を埋めることでストロークを模倣しています。

## 記事ごとの差分・視点の違い

記事「PureCSSSpider /RadarChartsAre Here in st-core.fscssv2」は、st-core.fscss v2が純CSSでラーダーチャートを描画する技術を提供している点を強調しています。特に、CSS変数とclip-path: polygon()を用いてポリゴンを描画し、リングとスポークをグラデーションで生成する方法が注目されています。また、この技術は軽量でパフォーマンスが高いとされ、JavaScriptライブラリと比較してその特徴が強調されています。

記事「Radarcharts— chaarts」は、CSS変数を用いてラーダーチャートを構築する方法を紹介しており、CSS側での複雑な計算が必要であることを指摘しています。また、Chromiumにおけるborder-spacingプロパティのバグについても触れられており、Chromeユーザーには注意が必要であるとされています。

記事「How to build an FSCSS module like st-core.fscss」は、FSCSSモジュールの構築方法を説明しており、再利用可能なスタイル定義を含むスタイルシートとしてのFSCSSモジュールの特徴を強調しています。また、パブリックAPIの設計やパラメータの読み込み方法、ドキュメンテーションの重要性についても述べられています。

記事「FSCSS Modules & Libraries Guide | Build, Publish & Import ...」は、FSCSSモジュールとライブラリの構築・公開・インポートに関するガイドを提供しており、FSCSSライブラリの構造や登録方法、インポート方法について説明しています。また、FSCSSの特徴や用途についても触れられており、純CSSで統計チャートやダッシュボードを実現する可能性を示しています。

記事「How to Build Dual-Pass Strokes with FSCSS Array Methods」は、clip-path: polygon()の制限を克服するためのダブルパス技法について説明しており、FSCSSの配列メソッドを用いたチャートラインの描画方法を紹介しています。また、この技法がst-coreなどのライブラリでどのように利用されているかについても触れられており、FSCSSの柔軟性と強力な機能を示しています。

## 深掘り調査で得られた知見

st-core.fscss v2 は、純CSSでラーダーチャートを描画する技術を提供しており、SVGやJavaScriptライブラリを使わずに軽量かつ高性能な実装が可能である。この技術は、CSS変数(--st-sxN, --st-syN)と clip-path: polygon() を用いてポリゴンを描画し、リングとスポークをグラデーションで生成する。データはFSCSSの配列として扱われ、最大半径はボックスの42%として設定されている。アニメーションは transition: clip-path で実現可能で、コンパイルされたCSSは約1キロバイトと非常に軽量である。この技術は、製品UIに適しており、現代のダッシュボードに適したスタイルとして位置付けられている。

また、FSCSSモジュールは、再利用可能なスタイル定義を含むスタイルシートであり、他のFSCSSファイルからインポート可能である。st-core.fscssは、デザイントークン、レイアウトヘルパーやチャート、統計カード、進行バーなど、FSCSS CLIでコンパイルおよびテストできるパターンに従っている。FSCSSモジュールの構造には、プライベートなデザイントークンとヘルパーロジック、パブリックなミックスイン、パラメータデフォルト、セレクター引数、ドキュメンテーションと例、そしてプロダクション用のコンパイル済みCSSが含まれる。パブリックAPIは、名前空間を使用して衝突を避ける必要があり、パラメータは @use() で読み込む必要がある。

clip-path: polygon() は形状を埋めることが可能だが、ストロークを描くことはできないため、FSCSSでは双方向のポリゴン技術を用いる。この技術は、データを前進方向で描画し、平行なエッジを逆方向で描画することで、ストロークの幅を再現する。FSCSSの配列メソッド(@arr, inline(), $, count(), .reverse) を使用して、この双方向のポリゴンを生成する。このような技術は、st-core.fscss などのライブラリでラーダーチャートや極座標空間のチャートラインに利用されている。FSCSS配列は、文字列ネイティブのデータ構造であり、CSS生成を効率化するために値を保存し、再利用することができる。

## 不確実な点・追加確認が必要な点

記事間では、Pure CSSでラーダーチャートを実装する技術の詳細や実装方法についての一致と不一致が確認されています。例えば、st-core.fscss v2は、CSS変数とclip-path: polygon()を用いてラーダーチャートを描画し、JavaScriptやSVGを一切使用しないことが明記されています。一方で、別のライブラリや技術では、SVGベースのJavaScriptライブラリを用いる場合があります。このため、CSS技術は軽量でパフォーマンスが高いという特徴を持ち、JavaScriptライブラリはより複雑な機能を提供するという違いがあります。

また、FSCSSモジュールの構造や実装方法についても、記事によって若干の違いがあります。例えば、st-core.fscssは、CSS変数とclip-path: polygon()を用いてチャートを描画し、データはFSCSSの配列として扱われます。一方で、別の記事では、FSCSSモジュールは再利用可能なスタイル定義を含むスタイルシートであり、他のFSCSSファイルからインポート可能であることが説明されています。また、FSCSSモジュールの構造には、プライベートなデザイントークンとヘルパーロジック、パブリックなミックスイン、パラメータデフォルト、セレクター引数、ドキュメンテーションと例、そしてプロダクション用のコンパイル済みCSSが含まれるという説明もあります。

さらに、clip-path: polygon()は形状を塗りつぶすことができますが、ストロークを描くことはできません。そのため、FSCSSでは、dual-pass polygon技術を用いてチャートラインを擬似ストロークとして描画する方法が説明されています。この技術は、FSCSSの配列メソッドを用いて実現され、st-core.fscssなどのライブラリで使用されていることが確認されています。ただし、FSCSSのバージョンや具体的なメソッドの使用に関する詳細は、一部の記事では明記されていません。そのため、これらの技術の詳細については、さらなる確認が必要です。

## 元記事一覧

- [PureCSSSpider /RadarChartsAre Here in st-core.fscssv2](https://dev.to/fscss/pure-css-spider-radar-charts-are-here-in-st-corefscss-v2-24on)
- [Radarcharts— chaarts](https://ffoodd.github.io/chaarts/radar-charts.html)
- [HowtobuildanFSCSSmodulelikest-core.fscss- DEV Community](https://dev.to/fscss/how-to-build-an-fscss-module-like-st-corefscss-1d6l)
- [FSCSS Modules & Libraries Guide | Build, Publish & Import ...](https://fscss.devtem.org/modules-guide)
- [How to Build Dual-Pass Strokes with FSCSS Array Methods](https://dev.to/fscss/how-to-build-dual-pass-strokes-with-fscss-array-methods-20oo)
