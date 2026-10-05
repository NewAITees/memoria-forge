---
title: OAuth 2 と Spring Security の統合実装
type: knowledge
status: draft
created: 2026-10-05
updated: 2026-10-05
confidence: medium
---

# OAuth 2 と Spring Security の統合実装

## 結論

OAuth 2 は、現代のアプリケーションにおける認証と認可の基盤となるフレームワークであり、特に OpenID Connect と併用することで、ユーザーの認証情報を安全に提供する仕組みを実現している。また、Spring Security との統合においては、JWT と OAuth2 の導入により、セキュリティの向上と柔軟な認証機制の実現が可能となり、既存のセキュリティ設計を維持しながらの導入が可能であることが確認されている。

## テーマ概要

OAuth 2 は、現代のアプリケーションにおける認証と認可の基盤となるフレームワークであり、特に OpenID Connect と組み合わせて広く利用されている。このプロトコルは、ユーザーが Google や他のサービスを介してサインインする際の背景で動作し、API 呼び出しや SaaS など多様なシナリオに適用可能である。OAuth 2 は、クライアント、ユーザー、認証サーバー、リソースサーバーの4つの役割をもとに設計されており、セキュリティを高めるために PKCE（Proof Key for Code Exchange）などの拡張が導入されている。近年では、2026 年からすべてのクライアントで PKCE の導入が必須となり、セキュリティの強化が求められている。また、OAuth 2 と OpenID Connect の統合により、ユーザー認証の柔軟性と信頼性が向上しており、特に多様なデバイスや環境での利用が増加している。

## 共通して確認できる点

OAuth 2.0 は、認証と認可を実現するフレームワークであり、OpenID Connect と併用されることで、ユーザーが Google や他のサービスにサインインする際の背景処理を担う。このプロトコルは、API 呼び出しにおいて広く採用されており、モバイルアプリ、Web アプリケーション、SaaS などに適用される。OAuth 2.0 は、認証フローにおいてクライアント、ユーザー、認証サーバー、リソースサーバーの 4 つの役割を有し、ID トークンやアクセストークンを用いて認証を行う。ユーザーの同意は必須であり、認証プロセスにおいて中心的な役割を果たす。2026 年からは、すべてのクライアントで PKCE（Proof Key for Code Exchange）が必須となり、モバイルやパブリッククライアントでの認証コードの盗難を防ぐための対策として導入されている。Google は OAuth 2.0 を認証と認可に利用しており、Google Cloud Console でプロジェクトを設定し、クライアント ID とシークレットを取得する必要がある。認証プロセスには、リダイレクト URI の設定やユーザーの同意画面のカスタマイズが含まれる。OAuth 2.0 と OpenID Connect の境界線は明確であり、OpenID Connect は OAuth 2.0 上に構築され、ユーザーの認証情報を提供する。

## 記事ごとの差分・視点の違い

記事「Replacing Basic Auth with JWT and OAuth2 in Spring Security」は、Spring Security において基本認証を JWT と OAuth2 に置き換える技術的実装とその利点を説明しています。特に、基本認証の欠点であるパスワードの毎回送信やセッション管理の欠如を解消するため、JWT を導入し、OAuth2 を併用することで柔軟な認証機制とセキュリティ向上を実現しています。また、RBAC（ロールベースアクセス制御）層が認証メカニズムの変更に影響を受けない点も強調しており、既存のセキュリティ設計を維持しながらの導入が可能であることを示しています。

記事「How to disable spring-security login screen? | Codemia」は、Spring Security のログイン画面を無効にし、代替の認証メカニズム（例として HTTP Basic 認証や JWT、OAuth2 など）を導入する方法を解説しています。この記事は、セキュリティ設定の柔軟性と、開発環境でのテスト目的での無効化を目的とした場合の注意点を含み、本番環境ではセキュリティのため無効化を避けるべきであることを指摘しています。

記事「Why Keycloak roles fail in Spring Security and how to fix them」は、Keycloak と Spring Security の統合において、Keycloak が提供するロール情報が Spring Security で正しく処理されない問題を指摘し、その原因と解決策を詳述しています。特に、Spring Security のデフォルトの JwtAuthenticationConverter が Keycloak のロール構造を理解していないこと、およびその解決策としてカスタムの JwtAuthenticationConverter の作成が求められることを強調しています。

記事「Your Keycloak roles aren't working in Spring Security. Here's ...」は、Keycloak と Spring Security の統合におけるロール処理の問題を再確認し、具体的な解決策としてカスタムの JwtAuthenticationConverter の実装を示しています。また、この問題が多くの Spring Boot プロジェクトで発生しており、それを解決するためのライブラリ「spring-keycloak-toolkit」の導入も提案しています。

記事「How to secure a Spark Java client application with OpenID...」は、Spark Java アプリケーションにおいて OpenID Connect（OIDC）を用いたセキュリティ設定の実装方法を説明しています。特に、pac4j を使用した SecurityFilter の設定、コールバックルート、ログアウトルート、ユーザー情報取得の流れを具体的に解説しており、OIDC を導入する際の実装例として参考になります。

## 深掘り調査で得られた知見

深掘り調査により、OAuth 2 と Spring Security の統合における課題と対応策が明らかになった。特に、Keycloak と Spring Security の連携において、JWT トークン内のロール情報が Spring Security によって正しく処理されない問題が確認された。これは、Spring Security のデフォルトの JwtAuthenticationConverter が Keycloak のロール構造を理解していないためであり、Keycloak が使用する realm_access.roles と resource_access.<clientId>.roles といったネストされた構造を処理しないことで起きていた。この問題を解決するためには、カスタムの JwtAuthenticationConverter を作成し、Keycloak のロール情報を Spring Security が期待する ROLE_ 前置の権限に変換する必要がある。また、spring-keycloak-toolkit というライブラリが、この問題を解決するための自動設定モジュールとして提供されており、複数のサービスで再利用可能である。さらに、Spring Security が生成する 401 と 403 レスポンスが空のボディを持つため、エラーの原因を特定するのが難しいという問題も存在する。この問題を解決するためには、カスタムの JwtAuthenticationConverter を作成し、Keycloak のロール情報を ROLE_ 前置の権限に変換する必要がある。また、OAuth 2 と JWT の導入により、セキュリティの向上と柔軟な認証機制の実現が可能となり、アプリケーションの信頼性が高まっている。

## 不確実な点・追加確認が必要な点

記事間では、OAuth 2 と Keycloak との統合におけるロール処理の違いや、Spring Security における JWT 認証の設定方法について、いくつかの食い違いが確認されている。例えば、記事 3 と記事 4 では、Keycloak で生成されるトークン内のロール構造が Spring Security で正しく処理されない原因について、共通の問題として挙げられているが、解決策としてカスタムの JwtAuthenticationConverter の導入が推奨されている。一方で、記事 1 では、JWT と OAuth2 の導入によって、セキュリティの向上と柔軟な認証機制が実現可能であることを説明しており、具体的な設定方法やロールの処理については触れていない。また、記事 5 では、Spark Java アプリケーションにおける OpenID Connect の実装について述べられているが、Keycloak との統合や Spring Security との関連性については言及されていない。これらの違いから、OAuth 2 の実装方法や Keycloak との統合における課題については、さらに詳しい情報が必要である。

## 元記事一覧

- [ReplacingBasicAuthwithJWTandOAuth2inSpringSecurity](https://dev.to/bilal_bukhari_75aeb34a969/replacing-basic-auth-with-jwt-and-oauth2-in-spring-security-h9k)
- [Howtodisablespring-securitylogin screen? | Codemia](https://codemia.io/knowledge-hub/path/how_to_disable_spring-security_login_screen)
- [Why Keycloak roles fail in Spring Security and how to fix them](https://itoverdose.com/en/news/your-keycloak-roles-arent-working-in-spring-security-heres-the-actual-reason-a3650c6b)
- [Your Keycloak roles aren't working in Spring Security. Here's ...](https://dev.to/jihedbfrart/your-keycloak-roles-arent-working-in-spring-security-heres-the-actual-reason-8fo)
- [HowtosecureaSparkJavaclientapplicationwithOpenID...](https://dev.to/jleleu/how-to-secure-a-spark-java-client-application-with-openid-connect-oidc-using-pac4j-1nb1)
