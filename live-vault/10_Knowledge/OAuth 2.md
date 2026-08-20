---
title: OAuth 2
created: 2026-08-10
updated: 2026-08-10
---

# OAuth 2

## 概要
OAuth 2.0 は、認証と認可を実現するフレームワークであり、OpenID Connect と組み合わせて利用される。ユーザーが Google や他のサービスにサインインする際、OAuth 2.0 が背景で動作し、OpenID Connect が認証情報を提供する。OAuth 2.0 は API 呼び出しで広く使用され、モバイル、Web アプリケーション、SaaS などに適用される。

## 詳細

### フローとメカニズム
OAuth 2.0 は、4 つの主要な役割（クライアント、ユーザー、認証サーバー、リソースサーバー）を含む。認証には、ID トークンやアクセストークンが使用され、ユーザーの同意が必須である。OpenID Connect は OAuth 2.0 上に構築され、ユーザーの認証情報を提供する。

### セキュリティと拡張
PKCE（Proof Key for Code Exchange）は、モバイルやパブリッククライアントでの認証コードの盗難を防ぐために導入された。2026 年から、すべてのクライアントで PKCE が必須である。

### サービスと実装
Google は OAuth 2.0 を認証と認可に利用し、Google Cloud Console でプロジェクトを設定し、クライアント ID とシークレットを取得する必要がある。認証には、リダイレクト URI の設定とユーザーの同意画面のカスタマイズが含まれる。

## ソース
- [OpenID Connect | Sign in with Google | Google for Developers](https://developers.google.com/identity/openid-connect/openid-connect)
- [OAuth 2.0 and OpenID Connect — How Modern Login Actually ...](https://rakeshnarayan.com/articles/oauth-2-and-openid-connect-how-modern-login-actually-works/)
- [OAuth 2.0 and OpenID Connect — The Protocols Behind 'Sign in ...](https://thinkidentity.github.io/iam/2026/05/14/oauth2-openid-connect-protocols-explained.html)
- [Understanding OAuth 2.0 and OpenID Connect: A Step-by-Step Guide](https://sachintolay.substack.com/p/understanding-oauth-20-and-openid)
- [OAuth2 SSO Guide: OpenID Connect, PKCE & Secure Login](https://www.weweb.io/blog/single-sign-on-using-oauth2-developer-guide)

## 未解決事項
- PKCE がすべてのクライアントで必須である理由
- OpenID Connect と OAuth 2.0 の境界線の明確化
- モバイルクライアントでの認証フローの詳細

## 出典


## 未解決点

