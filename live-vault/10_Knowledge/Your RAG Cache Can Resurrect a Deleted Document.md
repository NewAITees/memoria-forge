---
title: 削除されたドキュメントを再現するRAGキャッシュ
type: knowledge
status: draft
created: 2026-10-28
updated: 2026-10-28
confidence: medium
---

# 削除されたドキュメントを再現するRAGキャッシュ

## 何が分かったか

DEVはRailsサーバーレンダリング、Fastlyエッジキャッシング、InstantClickによるクライアントサイドナビゲーションを組み合わせたハイブリッドアーキテクチャを使用しています[^fact-2034dc0d91d35e61]。PR #23789は?i=iクエリパラメータをFastlyでのキャッシュパーティション化に再利用することで、長期にわたるキャッシュ不一致問題を解決しています[^fact-531e48113f6ca658]。?i=iはFastlyのエッジ構成で安全なパラメータとして使用され、自然なキャッシュパーティション化を可能にしています[^fact-80eacf4074af2121]。

## 確認できた事実

- DEV（オープンソースのForemコードベースで構築）は、Railsサーバーレンダリング、Fastlyエッジキャッシング、軽量クライアントサイドナビゲーション（InstantClickを介して）を組み合わせたハイブリッドアーキテクチャを使用しています。 [^fact-2034dc0d91d35e61]

- PR #23789 は、長期にわたるキャッシングの不一致問題を解決するために、?i=i クエリパラメータをFastlyでのキャッシュパーティション化に再利用しています。 [^fact-531e48113f6ca658]

- ?i=i クエリパラメータは、Fastlyのエッジ構成で安全なパラメータとして使用され、自然なキャッシュパーティション化を可能にしています。 [^fact-80eacf4074af2121]

- ?i=i クエリパラメータは、レンダリングではなくキャッシュバケットを選択するために使用され、キャッシュパーティション化を保証しています。 [^fact-bca0ba5dc326ab8a]

- 特定の記事に対して404エラーが発生したのは、まだ古いバージョンを提供していたキャッシュされた応答のためです。 [^fact-4d60dbd9b726688e]

## それが意味すること

キャッシュバケットを選択するための?i=iパラメータは、古いバージョンのコンテンツを提供する可能性があるため、正確性や一貫性に悪影響を及ぼす可能性があります[^fact-bca0ba5dc326ab8a]。404エラーが発生した原因は、まだ古いバージョンを提供していたキャッシュされた応答でした[^fact-4d60dbd9b726688e]。 [^fact-bca0ba5dc326ab8a] [^fact-4d60dbd9b726688e]

## まだ分からないこと

キャッシュバケット選択の?i=iパラメータの適用範囲や、どの記事にも適用されるか、または特定の条件に依存するかについての情報は提供されていません。

## 出典

[^fact-2034dc0d91d35e61]: [Fixing Delicate Cache Mismatches in a Brownfield SPA: A ...](https://dev.to/devteam/fixing-delicate-cache-mismatches-in-a-brownfield-spa-a-pragmatic-solution-dk9)
  - 根拠引用: 「On DEV (powered by the open-source Forem codebase), we have a hybrid architecture that blends Rails server rendering, Fastly edge caching, and lightweight client-side navigation (via InstantClick ).」
[^fact-531e48113f6ca658]: [Fixing Delicate Cache Mismatches in a Brownfield SPA: A ...](https://dev.to/devteam/fixing-delicate-cache-mismatches-in-a-brownfield-spa-a-pragmatic-solution-dk9)
  - 根拠引用: 「In PR #23789 , we repurposed this parameter: (If data-style-fingerprint is missing—such as on tabs open during deploy cutover—it gracefully falls back to ?i=i ). Natural Cache Partitioning at Fastly: Fastly's edge configuration already whitelists i in its safe parameter list. Because the query parameter is part of the cache key:」
[^fact-80eacf4074af2121]: [Fixing Delicate Cache Mismatches in a Brownfield SPA: A ...](https://dev.to/devteam/fixing-delicate-cache-mismatches-in-a-brownfield-spa-a-pragmatic-solution-dk9)
  - 根拠引用: 「Natural Cache Partitioning at Fastly: Fastly's edge configuration already whitelists i in its safe parameter list. Because the query parameter is part of the cache key:」
[^fact-bca0ba5dc326ab8a]: [Fixing Delicate Cache Mismatches in a Brownfield SPA: A ...](https://dev.to/devteam/fixing-delicate-cache-mismatches-in-a-brownfield-spa-a-pragmatic-solution-dk9)
  - 根拠引用: 「The guarantee is bounded by whether the key hits, because the parameter selects a bucket rather than a rendering.」
[^fact-4d60dbd9b726688e]: [The404onlywecouldsee:23.8hoursinsideacacheentrywe...](https://dev.to/rulestack/the-404-only-we-could-see-238-hours-inside-a-cache-entry-we-made-ourselves-2i36)
  - 根拠引用: 「Our 404 came back with x-cache: HIT and age: 85673 . That is a cached response, and 85,673 seconds is 23.8 hours old.」
