---
title: モロッコのEコマースでWordPressからNext.js16への移行実績
type: knowledge
status: draft
created: 2026-10-01
updated: 2026-10-01
confidence: medium
---

# モロッコのEコマースでWordPressからNext.js16への移行実績

## 結論

Next.js 16 の導入により、モロッコの高トラフィックEコマースサイトでは、モバイルでのパフォーマンス向上とユーザー体験の改善が実現されました。特に、First Contentful Paint（FCP）が3.5〜5.2秒から0.8〜1.5秒に短縮され、Lighthouseスコアも50〜70から90〜100に向上し、コンバージョン率の向上と収益増加に直接つながりました。また、CMIによるオンラインカード処理においても、Next.jsのAPIルートハンドラーやサーバーアクションを活用することで、銀行取引の確認時間がミリ秒単位に短縮され、セキュリティ検証も可能となりました。

## テーマ概要

モロッコの高トラフィックなECサイトでWordPressからNext.js 16への移行が注目されている理由は、モバイル優先な市場におけるウェブパフォーマンスの重要性が高まっているためです。モロッコではオンライン取引の78%がモバイル4G/3G接続で行われており、遅いロードタイムはコンバージョン率や収益に大きな影響を与えます。多くのデジタルエージェンシーが依然としてモノリシックなWordPress/WooCommerceテーマを採用しており、35以上のプラグインを搭載した結果、First Contentful Paint（FCP）が3.5〜5.2秒と遅く、ユーザー体験を阻害しています。これに対し、TripleWというエンジニアリングチームはNext.js 16（Turbopack、App Router）とクラウドエッジアーキテクチャを導入し、パフォーマンスを大幅に改善しました。特に、5,000SKUのカタログをWooCommerceからNext.js 16へ移行し、静的生成（generateStaticParams）とインクリメンタルキャッシュ無効化を活用することで、LCP（Largest Contentful Paint）が2.5〜4秒から0.8〜1.5秒まで短縮され、Lighthouseスコアも50〜70から90〜100に向上しました。また、モロッコ市場におけるオンラインカード処理の課題であるCMI（Centre Monétique Interbancaire）への対応においても、Next.jsのAPIルートハンドラーやサーバーアクションを活用することで、銀行取引の確認がミリ秒単位で完了し、セキュリティ検証も行えるようになりました。このような改善により、ユーザー体験の向上と収益の増加が実現され、モロッコのEC事業においてNext.js 16の採用が急速に広がっています。

## 共通して確認できる点

複数の記事で共通して確認できた事実として、モロッコの高トラフィックEコマースサイトにおいて、WordPressからNext.js 16への移行が行われたことが挙げられる。この移行は、特にモバイルでの利用が主流であるモロッコ市場において、ウェブパフォーマンスの向上を目的としている。モバイルでのオンライン取引は4G/3G接続で行われており、First Contentful Paint（FCP）の平均値が3.5〜5.2秒と遅く、これはコンバージョン率や収益に大きな影響を及ぼしている。Next.js 16の導入により、5,000SKUのカタログを静的生成（generateStaticParams）とインクリメンタルなキャッシュ無効化を用いて移行し、パフォーマンスが大幅に改善した。LCP（Largest Contentful Paint）は2.5〜4秒から0.8〜1.5秒に、Lighthouseスコアは50〜70から90〜100に改善された。また、Next.js APIルートハンドラーやサーバーアクションを活用することで、CMI（Centre Monétique Interbancaire）によるオンラインカード処理がミリ秒単位で完了し、セキュリティの高い暗号化署名検証が可能となった。さらに、Next.js 16はSEO最適化やスピード向上に適しており、多くの販売者がWooCommerceのバックエンドをNext.jsのフロントエンドから分離するなど、柔軟なアーキテクチャを採用している。また、Third-partyスクリプトの扱いにおいて、Next.jsのnext/scriptコンポーネントを活用することで、レンダリングブロッキングを回避し、パフォーマンスとセキュリティの両面で改善が図られている。

## 記事ごとの差分・視点の違い

記事「WhyWeReplacedWordPresswithNext.js16forHigh-Traffic...」は、モロッコの高トラフィックECサイトにおけるWordPressからNext.js 16への移行を主にテーマにし、特にモバイルユーザーの行動とウェブパフォーマンスの関係を強調しています。記事では、モロッコのオンライン取引が主にモバイル4G/3Gで行われており、First Contentful Paint（FCP）が3.5〜5.2秒に及ぶ現状を指摘し、Next.js 16の導入によってLCPが0.8〜1.5秒に改善したという実績を示しています。また、モロッコのオンラインカード処理におけるCMI（Centre Monétique Interbancaire）の課題にも言及し、Next.jsのAPIルートハンドラーによる即時銀行取引確認が挙げられています。

記事「WhyWeReplacedWordPresswithNext.js16(And How...) | Digital FX」は、SEOとパフォーマンスの観点からWordPressとNext.jsの比較をしています。特に、WordPressのプラグイン数やSQLクエリの増加、パフォーマンスの悪化を指摘し、Next.jsのApp Routerや動的パラメータによる効率的なページ生成を強調しています。この記事では、Next.jsの導入によりSEOランクの向上や広告費の削減が可能になると述べており、ビジネスの利益に直結する点を強調しています。

記事「That Third-Party Script Tag You Copy-Pasted Is Probably ...」は、Next.jsにおけるサードパーティスクリプトの扱いについて述べています。特に、通常の<script>タグをそのまま使用した場合のレンダリングブロッキングの問題を指摘し、next/scriptコンポーネントの使用が推奨されています。この記事では、スクリプトの読み込み戦略（beforeInteractive、afterInteractive、lazyOnload）の選択がパフォーマンスに与える影響を詳しく説明しており、Next.jsの柔軟性を強調しています。

記事「Third-party script hijack: dead and compromised CDNs ...」は、サードパーティスクリプトのセキュリティリスクをテーマにしています。特に、polyfill.ioなどのCDNがハッキングされ、悪意のあるコードが注入された事例を紹介しています。この記事では、サードパーティスクリプトの使用がサイトのセキュリティに与える影響を指摘し、次世代のウェブ開発における注意点を示しています。

記事「How We Achieved a 99 PageSpeed Score: A Real-World Web ...」は、ウェブパフォーマンスの最適化に焦点を当てています。特に、モバイルでのパフォーマンス改善をテーマにし、PageSpeedスコアの99を達成した実例を紹介しています。この記事では、Next.jsの導入によるパフォーマンス向上と、その結果としてのユーザー体験の改善が強調されています。また、SEOとパフォーマンスの両面からの改善が示されています。

## 深掘り調査で得られた知見

Next.js 16 の導入により、モロッコの高トラフィックEコマースサイトでは大幅なパフォーマンス改善が実現されました。特に、モバイルユーザー比率が高いモロッコでは、4G/3G接続での平均First Contentful Paint（FCP）が3.5〜5.2秒から、0.8〜1.5秒に短縮されました。この改善により、ユーザーの離脱率が減少し、コンバージョン率が向上しました。また、Next.js 16 の静的生成（generateStaticParams）とインクリメンタルキャッシュ無効化を活用することで、5,000SKUのカタログの移行が可能となりました。さらに、Next.js API ルートハンドラーやサーバーアクションを用いることで、モロッコのオンラインカード処理（CMI）での銀行取引の確認時間がミリ秒単位に短縮され、セキュリティ面でも完全な暗号署名検証が可能となりました。このような技術的改善により、モロッコのEC事業者はパフォーマンスとユーザー体験の向上を実現し、収益向上に貢献しています。また、Next.js 16 はSEO最適化にも貢献し、多くのEC事業者がWooCommerceのバックエンドをNext.jsのフロントエンドと分離して運用する動きが広がっています。さらに、Next.js 16 は柔軟性とコスト効率が高く、Shopify Hydrogenなどの代替技術よりも優れているとされています。Third-partyスクリプトの適切な管理も重要で、Next.js の next/script コンポーネントを活用することで、レンダリングブロッキングを回避し、パフォーマンスとセキュリティを向上させることが可能です。

## 不確実な点・追加確認が必要な点

記事間では、Next.js 16 への移行が高トラフィックなモロッコのECサイトで行われたという共通の背景が示されていますが、具体的な実施時期や詳細な移行プロセスについては明確ではありません。例えば、記事1では、移行後におけるLCP（Largest Contentful Paint）の改善が記載されており、LCPが2.5〜4秒から0.8〜1.5秒へと改善したとされていますが、この改善がいつから観測されたのか、具体的な測定期間やデータソースが提示されていません。また、記事2では、Next.js 16がTurbopackを使用し、Edgeキャッシュを活用して150ms未満でページを提供していると述べられていますが、この情報の取得日や、どのクライアントやプロジェクトを基にしたデータかが明示されていません。さらに、記事4では、2024年6月に起きたCDNのハッキング事件が記載されており、これはNext.jsの導入と直接的な関連性は示されていませんが、第三パーティスクリプトのリスクが強調されている点は、Next.js移行の背景として考慮する必要があります。これらの記事は、Next.jsの導入がECサイトのパフォーマンス改善とセキュリティ強化に寄与している可能性を示唆していますが、具体的な移行時期や詳細なケーススタディについては、各記事の情報が断片的であり、一貫性が欠けています。そのため、これらの情報は参考として捉えつつ、断定的な主張は避けた方が適切です。

## 元記事一覧

- [WhyWeReplacedWordPresswithNext.js16forHigh-Traffic...](https://dev.to/amsomr/why-we-replaced-wordpress-with-nextjs-16-for-high-traffic-e-commerce-in-morocco-4gj0)
- [WhyWeReplacedWordPresswithNext.js16(And How...) | Digital FX](https://www.digitalfx.in/blog/nextjs-vs-wordpress-seo-performance)
- [That Third-Party Script Tag You Copy-Pasted Is Probably ...](https://dev.to/anas_sheikh_2/that-third-party-script-tag-you-copy-pasted-is-probably-hurting-4pfi)
- [Third-party script hijack: dead and compromised CDNs ...](https://surfacecheckr.com/learn/attack-surface/third-party-script-supply-chain-hijack)
- [How We Achieved a 99 PageSpeed Score: A Real-World Web ...](https://dnt.co.il/how-we-achieved-a-99-pagespeed-score-a-real-world-web-performance-case-study/)
