---
title: dev.toのコメント投稿におけるCSRFトークンの問題
type: knowledge
status: draft
created: 2026-10-08
updated: 2026-10-08
confidence: medium
---

# dev.toのコメント投稿におけるCSRFトークンの問題

## 結論

dev.toのコメント投稿機能において、CSRFトークンが「NOTHING」として初期化され、JavaScriptによって動的に上書きされるため、非JavaScriptクライアントではトークンを取得できず、投稿が失敗するという問題が確認されている。この問題は、/async_info/base_dataエンドポイントからトークンを取得し、セッションCookieと共に送信することで解決可能であり、CSRF保護の仕組みにおいて重要な役割を果たしている。

## テーマ概要

dev.toのコメント投稿機能において、CSRFトークンが「NOTHING」として埋め込まれている問題が報告されている。このトークンはJavaScriptによって動的に上書きされるため、非JavaScriptクライアントでは取得できず、curlなどのツールでの投稿が失敗する。また、トークンは/async_info/base_dataエンドポイントから取得可能であり、セッションCookieと共に送信することでコメント投稿が成功する。この問題は、セッションの有効期限切れや複数タブでのフォーム表示、ブラウザキャッシュ、OAuth2などの認証フローの不適切な処理などが原因で発生する可能性がある。2026年9月30日にこの問題が報告され、解決策としてトークンの取得方法が提案された。同様のCSRFトークン不一致の問題は2026年1月24日にガイドとして公開されており、その解決策としてセッションの有効期限切れや複数タブでのフォーム表示などが挙げられている。

## 共通して確認できる点

dev.toのコメント投稿機能において、CSRFトークンが「NOTHING」として初期化されていることが確認されました。このトークンは、JavaScriptによって動的に上書きされるため、非JavaScriptクライアントでは取得できず、curlなどのツールによる投稿が失敗する可能性があります。CSRFトークンの正しい値は、/async_info/base_dataエンドポイントから取得可能で、セッションCookieと共に送信することでコメント投稿が成功します。この問題は、2026年9月30日に報告され、その解決策としてトークンの取得方法が提案されました。また、CSRFトークンの不一致は、セッションの有効期限切れや複数タブでのフォーム表示、ブラウザキャッシュ、OAuth2などの認証フローの不適切な処理など、複数の原因で発生する可能性があることが指摘されています。

## 記事ごとの差分・視点の違い

記事「dev.to ships its comment CSRF token as value="NOTHING". Here's what that breaks」は、dev.toのコメント投稿機能におけるCSRFトークンの不適切な埋め込み方式に焦点を当て、技術的な問題点とその影響を詳細に説明している。この記事では、CSRFトークンがJavaScriptによって動的に上書きされるため、非JavaScriptクライアントではトークンを取得できず、curlなどのツールでの投稿が失敗するという現象を報告している。また、トークンを取得するためのエンドポイントや、解決策としてのセッションCookieの利用についても述べている。

記事「How to Fix 'CSRF Token Mismatch' Errors - oneuptime.com」は、CSRFトークン不一致エラーの一般的な原因とその解決策を幅広く解説しており、フレームワークごとの対処法やOAuth2での対応方法など、実践的なアドバイスを提供している。この記事は、開発者向けに技術的な解決策を提案しており、CSRF保護の仕組みや、セッション管理やキャッシュの問題など、幅広い観点から問題を分析している。

記事「How to structure your RSS Feed for DEV.to Ingestion」は、DEV.toに記事をインポートするためのRSSフィードの正しいフォーマットについて説明しており、特に`<content:encoded>`タグや絶対URLの使用など、インポートに必要な技術的な詳細を重視している。この記事は、RSSフィードの構造に特化しており、DEV.toのインポート要件を満たすための具体的な手順を提供している。

記事「Fixing RSS Feed Issues with DEV.to | Reclear posted on the... | LinkedIn」は、RSSフィードの技術的な妥当性だけでなく、 publishing platformとしてのDEV.toの要件を満たすための追加的な条件を強調しており、`content:encoded`や絶対URL、カノニカルリンクなどの要素がインポートに重要な役割を果たすことを指摘している。この記事は、LinkedInを通じて共有され、技術的な情報の共有とコミュニティのフィードバックが重視されている点が特徴的である。

記事「[Boost] - DEV Community」は、DEV.toのAnalyticsツールが動作していない可能性を報告しており、特定の投稿のトラフィックソースが不正確であることに困惑しているユーザーの声を反映している。この記事は、DEV.toのプラットフォームのトラフィック分析機能に関する問題を指摘しており、コミュニティ全体での確認や対応が求められている状況を示している。

## 深掘り調査で得られた知見

dev.toのコメント投稿機能におけるCSRFトークンの扱いは、技術的な課題を引き起こしている。コメントフォームでは、CSRFトークンが「NOTHING」として初期化され、JavaScriptによって動的に上書きされる。このため、非JavaScript環境ではトークンを取得できず、curlなどのツールでの投稿が失敗する。トークンは、/async_info/base_dataエンドポイントから取得可能で、セッションCookieと共に送信することでコメント投稿が成功する。CSRFトークンの検証は、セッションCookieと同源性のチェックに依存しており、クロスサイトリクエストフォージェリ（CSRF）防御において重要な役割を果たしている。

CSRFトークンの不一致は、セッションの有効期限切れ、複数タブでのフォーム表示、ブラウザキャッシュ、OAuth2などの認証フローの不適切な処理など、複数の原因で発生する可能性がある。2026年9月30日に、この問題が報告され、解決策として/async_info/base_dataエンドポイントからのトークン取得が提案された。また、2026年1月24日に、CSRFトークンの不一致に関するガイドが公開され、その解決策としてセッションの有効期限切れや複数タブでのフォーム表示などの原因が挙げられている。さらに、2026年6月27日に、CSRFトークンの検証失敗に関するガイドが公開され、同様の原因が示されている。

## 不確実な点・追加確認が必要な点

dev.toのコメント投稿フォームにおけるCSRFトークンの処理について、複数の記事で触れられているが、具体的な原因や対応策については一貫性が見られない。記事1では、CSRFトークンが「NOTHING」として埋め込まれており、JavaScriptによって動的に上書きされることが確認されており、非JavaScriptクライアントではトークンを取得できないことが指摘されている。一方で、記事2ではCSRFトークンの不一致が発生する原因として、セッションの有効期限切れや複数タブでのフォーム表示、ブラウザキャッシュ、OAuth2の認証フローの不適切な処理などが挙げられているが、これらはdev.toの特定の問題とは直接関係していない可能性がある。また、記事3と記事4ではRSSフィードの構造について説明されており、DEV.toのインゴステーションに必要なフォーマットや設定についての情報が提供されているが、これらはCSRFトークンの問題とは関係ない。記事5では、DEV.toのAnalyticsツールが動作していない可能性についての報告がされているが、これもCSRFトークンの問題とは無関係である。したがって、CSRFトークンの問題に関する情報は記事1に集中しており、他の記事では関連性のない内容が含まれている。そのため、記事間での整合性や一貫性が確認されていない点がある。

## 元記事一覧

- [dev.to ships its comment CSRF token as value="NOTHING". Here ...](https://dev.to/cael_ilands/devto-ships-its-comment-csrf-token-as-valuenothing-heres-what-that-breaks-5flg)
- [How to Fix 'CSRF Token Mismatch' Errors - oneuptime.com](https://oneuptime.com/blog/post/2026-01-24-fix-csrf-token-mismatch/view)
- [HowtostructureyourRSSFeedforDEV.toIngestion](https://dev.to/reclear/how-to-structure-your-rss-feed-for-devto-ingestion-mnc)
- [FixingRSSFeedIssues withDEV.to| Reclear posted on the... | LinkedIn](https://www.linkedin.com/posts/reclear_how-to-structure-your-rss-feed-for-devto-activity-7497762943456022528-jTjH)
- [[Boost] -DEVCommunity](https://dev.to/anthonymax/-dan)
