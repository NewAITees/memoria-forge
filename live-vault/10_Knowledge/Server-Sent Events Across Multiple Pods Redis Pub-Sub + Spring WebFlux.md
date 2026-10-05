---
title: Server-Sent Events 跨 Pod における Redis Pub/Sub と Spring WebFlux の実装
type: knowledge
status: draft
created: 2026-10-05
updated: 2026-10-05
confidence: medium
---

# Server-Sent Events 跨 Pod における Redis Pub/Sub と Spring WebFlux の実装

## 結論

Server-Sent Events（SSE）を複数のPod間で実装するには、Redis Pub/SubとSpring WebFluxの組み合わせが有効で、イベントの横断的な伝達を可能にする。ただし、Redis Pub/Subの接続失敗やイベント漏れといった課題があり、ローカルのSinkへのイベントemitやハートビート、再接続メカニズムなどの対策が必要となる。この技術は、マイクロサービスアーキテクチャにおけるリアルタイム通信や高負荷での非同期データフロー処理において重要な役割を果たしている。

## テーマ概要

Server-Sent Events (SSE) を複数の Pod にわたって実装する技術が注目されている。このアプローチでは、Spring WebFlux と Redis Pub/Sub を組み合わせることで、リアルタイムな通知やイベント伝達を実現する。単一の Pod では SSE は比較的簡単だが、複数の Pod にわたる場合、イベントが他の Pod のサブスクライバーに届くようにする必要がある。Redis Pub/Sub はこのような横断的な通信を可能にする。しかし、Pod 間でのイベント伝達には課題があり、例えば Redis Pub/Sub 接続の失敗やイベントの漏れといった問題が生じる可能性がある。そのため、ローカルのシンクにイベントを常にemitし、失敗時のデータの一貫性を確保するなどの対策が求められる。この技術は、マイクロサービスアーキテクチャにおけるリアルタイム通信や通知システムの実装に重要な役割を果たしており、特に高負荷や非同期データフローを扱う現代のWebアプリケーションにおいて注目されている。

## 共通して確認できる点

Server-Sent Events（SSE）を複数のPod間で利用する際、Redis Pub/SubとSpring WebFluxを組み合わせる手法が検討されている。記事1では、単一PodでのSSE実装は簡潔だが、複数Pod環境ではイベントの伝播が複雑になる点が指摘されている。PodAで発生したイベントがPodBのサブスクライバーに届くようにするため、Redis Pub/Subが利用される。ただし、Redis Pub/Subの接続が失敗する可能性があり、その場合イベントが届かないリスクがある。そのため、ローカルのSinkにイベントをemitする仕組みが導入されている。また、SSE接続の管理にはハートビート、X-Accel-Bufferingヘッダー、30分での接続終了といった仕組みが用意されている。  

Redis Pub/Subは、マイクロサービスアーキテクチャにおけるサービス間通信に適した非同期メッセージングモデルとして、記事2で説明されている。発行者（Publisher）がチャネルにメッセージを配信し、サブスクライバー（Subscriber）がそのメッセージを受信する仕組みである。ただし、PubSubモデルには制限があり、例えばメッセージの再配信や遅延処理などは考慮が必要となる。  

一方、CLIENT TRACKINGはRedis 6で導入され、クライアントサイドキャッシュの正確性を確保するための機能である。記事3および記事4によると、Redis Open SourceではCLIENT TRACKINGがサポートされており、Redis SoftwareやRedis Cloudでは7.4以降のバージョンでサポートされるが、2つの接続モードやREDIRECTオプションは非対応である。StackExchange.RedisはCLIENT TRACKINGを実装していないため、RedisNearCacheなどのサードパーティ製パッケージが提供している。  

これらの技術は、リアルタイム通信やキャッシュ管理の最適化に貢献しており、複数の記事で共通して確認できた事実である。

## 記事ごとの差分・視点の違い

記事「Server-Sent Events Across Multiple Pods: Redis Pub/Sub + Spring WebFlux」は、SSEを用いたリアルタイム通知システムの実装に焦点を当てており、特に複数のPod間でのイベント伝達の課題を詳しく説明しています。一方、「Redis PubSub with Spring Boot」は、Redis Pub/Subをマイクロサービスアーキテクチャにおけるサービス間通信に利用する基本的な例を紹介しており、実装例と動作を簡潔に説明しています。また、「CLIENT TRACKING landed in Redis 6 four years ago ...」は、Redis 6で導入されたCLIENT TRACKING機能と、StackExchange.Redisにおける非対応の問題、およびRedisNearCacheなどの代替ソリューションについて論じています。さらに、「Client-side caching compatibility with Redis Software and ...」は、Redis SoftwareとRedis Cloudにおけるクライアントサイドキャッシュのサポート状況と、Redis Open Sourceとの違いを明確にしています。最後に、「Redora 0.3.1 — Redis for NestJS」は、NestJSにおけるRedisとの統合を支援するRedoraというライブラリの紹介で、キャッシュ、ロック、レートリミットなどの機能拡張を目的としています。各記事は、Redisを用いたリアルタイム通信やクライアントサイドキャッシュの実装にかかわる異なる視点と技術的課題を提示しています。

## 深掘り調査で得られた知見

Server-Sent Events (SSE) を複数の Pod にわたって実装する際、Redis Pub/Sub と Spring WebFlux を組み合わせるアプローチが採用されている。この方法では、単一の Pod では Flux でイベントを生成するシンプルな実装が可能だが、複数の Pod にわたる通信では、Pod A で行われた書き込みが Pod B のサブスクライバーに届くようにする必要がある。そのため、Redis Pub/Sub を利用してイベントを複数のインスタンスにブロードキャストする。しかし、Redis Pub/Sub との接続が失敗すると、他の Pod のサブスクライバーがイベントを受信できなくなる可能性があるため、ローカルの Sink にイベントを Emit する仕組みが導入されている。また、SSE 接続の管理には、30秒ごとの Heartbeat と X-Accel-Buffering ヘッダーの設定が重要で、プロキシや CDN のバッファリングを回避する。さらに、30分後にサーバーが接続を終了し、クライアントが JWT を再取得して再接続する仕組みも実装されている。

Redis Pub/Sub は、マイクロサービスアーキテクチャにおいてサービス間での非同期通信に適したメカニズムとして利用される。しかし、Redis Pub/Sub にはいくつかの制限があり、例えば、特定のチャネルにサブスクライブする Subscriber がメッセージを受信するタイミングや、メッセージの順序保証が求められないなどの点が挙げられる。このような制限を補うため、Spring WebFlux と組み合わせて SSE を利用する方法が提案されている。また、Redis 6 で導入された CLIENT TRACKING は、クライアントサイドキャッシュの正確性を保つために重要だが、StackExchange.Redis ではまだ実装されていない。その代替として、RedisNearCache というサードパーティ製パッケージが提供されており、既存の Multiplexer と併用してトラッキングと無効化の処理を行っている。Redis Software と Redis Cloud では、CLIENT TRACKING はサポートされていないが、無効化テーブルを用いた代替手段が採用されている。

## 不確実な点・追加確認が必要な点

記事間では、Server-Sent Events (SSE) を複数 Pod にわたって実装する際のアプローチや技術選択についての違いが見られる。記事 1 では、Redis Pub/Sub を利用して、Pod A で発行されたイベントが Pod B のサブスクライバーに届くようにする必要性が強調されており、その実装には Spring WebFlux と Flux を用いた非同期処理が中心となる。一方で、記事 2 では、Redis Pub/Sub がマイクロサービスアーキテクチャ内でサービス間でのメッセージ送信に利用されることが説明されており、具体的な実装例として、パブリッシャーとサブスクライバーの 2 つの Spring Boot アプリケーションが挙げられている。この記事では、SSE ではなく、単純なメッセージ送信の例が提示されており、SSE と Redis Pub/Sub の関連性は明示されていない。

また、記事 3 と 4 では、Redis の CLIENT TRACKING 機能とそのサポート状況が議論されており、Redis 6 で導入されたこの機能は、クライアントサイドキャッシュの正確性を保つために重要であるが、StackExchange.Redis では未対応であることが指摘されている。一方で、Redis Software と Redis Cloud では、CLIENT TRACKING のサポートが制限されており、代わりに無効化テーブルを用いたアプローチが採用されている。これらは、Redis Pub/Sub と SSE の実装とは直接的な関係はなく、キャッシュ連携や無効化処理に関する技術的課題である。

記事 5 では、NestJS 用の Redis クライアントライブラリ Redora の紹介がされているが、SSE と Redis Pub/Sub の実装とは無関係な内容であり、SSE と Redis に関する実装例としては関連性が薄い。したがって、記事間では、SSE と Redis Pub/Sub の実装に焦点を当てた内容が一部に見られ、他の記事では関連する技術（CLIENT TRACKING やキャッシュ連携など）が取り上げられているため、それぞれの記事が異なる観点から技術的な課題や実装方法を説明していることが確認できる。

## 元記事一覧

- [Server-SentEventsAcrossMultiplePods:RedisPub/Sub+Spring...](https://dev.to/anand_rathnas_d5b608cc3de/server-sent-events-across-multiple-pods-redis-pubsub-spring-webflux-g0o)
- [RedisPubSubWithSpringBoot | Vinsguru](https://blog.vinsguru.com/redis-pubsub-spring-boot/)
- [CLIENT TRACKING landed in Redis 6 four years ago ...](https://dev.to/magnanz/client-tracking-landed-in-redis-6-four-years-ago-stackexchangeredis-still-doesnt-support-it-199j)
- [Client-side caching compatibility with Redis Software and ...](https://redis.io/docs/latest/operate/rs/references/compatibility/client-side-caching/)
- [Redora 0.3.1 — Redis for NestJS - DEV Community](https://dev.to/neba/redora-031-redis-for-nestjs-2blh)
