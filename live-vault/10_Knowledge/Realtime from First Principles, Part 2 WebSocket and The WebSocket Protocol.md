---
title: リアルタイム通信の基礎からWebSocketプロトコルまで
type: knowledge
status: draft
created: 2026-09-23
updated: 2026-09-23
confidence: medium
---

# リアルタイム通信の基礎からWebSocketプロトコルまで

## 結論

WebSocketは、クライアントとサーバー間で双方向のフルダイクス通信を可能にするプロトコルであり、HTTPのリクエスト応答モデルを越えて、接続が確立されると両者が任意のタイミングでデータを送信できる。このプロトコルは、ポーリングやロングポーリングなどのHTTPベースの代替手段の制限を克服し、リアルタイム通信の標準として広く採用されている。ただし、WebSocketはステートフルで永続的な接続を必要とし、スケーリングやロードバランシングに影響を与えるため、運用上の負担が大きい。そのため、一方向の更新に特化したServer-Sent Events（SSE）などの代替技術も活用されることがある。

## テーマ概要

WebSocketは、クライアントとサーバー間での双方向通信を可能にするプロトコルであり、従来のHTTPのリクエスト応答モデルを越えて、一方向ではなく両方向でのデータ送信を実現します。このプロトコルは、TCP上に構築され、接続が確立されるとその状態を維持し、必要に応じてどちらの側からもデータを送信できるフルダブル通信をサポートします。WebSocketは、HTTPのポーリングやロングポーリングなどの代替手段の限界を克服し、より効率的なリアルタイム通信を実現するため、特にブラウザとサーバー間のリアルタイム通信で標準となっています。この技術は、チャットアプリ、コラボレーションツール、金融情報のリアルタイム配信、IoTデバイスのテレメトリーなど、リアルタイム性が求められる分野で注目されています。また、WebSocketはHTTP/2やHTTP/3といった最新のプロトコルとの連携も可能であり、パフォーマンス向上やスケーラビリティの向上にも寄与しています。これらの要素から、WebSocketは現代のリアルタイム通信の基盤として重要な役割を果たしています。

## 共通して確認できる点

WebSocketは、クライアントとサーバー間で双方向のフルダイクス通信を可能にするプロトコルであり、HTTPのリクエスト応答モデルとは異なり、接続が確立されると両者が任意のタイミングでデータを送信できる。WebSocketプロトコルは、3つのフェーズを経る。最初のフェーズは、通常のHTTP接続をWebSocket接続へアップグレードするオープニングハンドシェイク、次にデータのやり取りを行うデータ転送フェーズ、最後に接続を終了するクロージングハンドシェイクである。このプロトコルは、ポーリングやロングポーリングといったHTTPベースの代替手段の限界を克服するため設計され、より効率的な通信チャネルを提供する。WebSocketは、通常のHTTPポート（80/443）で動作し、ファイアウォールがWebトラフィックを許可している環境で動作する。ブラウザはWebSocket APIを提供しているが、HTTP/2フレーミングは提供していないため、WebSocketがブラウザとサーバー間のリアルタイム通信の標準である。一方で、WebSocketは他のリアルタイム通信技術（例えば、Server-Sent Events）と比較して、より複雑な運用を必要とし、スケーリングやロードバランシングに影響を与える。WebSocketは、リアルタイムの双方向通信を必要とするアプリケーションに特に適しており、その実装には状態を保持する必要がある。

## 記事ごとの差分・視点の違い

記事「Realtime from First Principles, Part 2: WebSocket and The WebSocket Protocol」では、WebSocketプロトコルの基本的な仕組みと、HTTPとの違いを詳しく解説しています。特に、WebSocketが双方向通信を可能にするフルダブルスルーの特性や、HTTPとの通信モデルの違いを強調しています。また、WebSocketがリアルタイム通信を実現する上で重要な役割を果たす理由を説明し、他の技術との比較も行っています。

記事「WebSockets & Real-Time · Chapter 24 · Backend from First Principles」では、WebSocketsがHTTPの制限をどのように克服したかを焦点にしています。特に、HTTPの単方向通信の問題を解決し、サーバーからクライアントへのプッシュ通知を可能にした点を強調しています。また、WebSocketsの利点と欠点、そして他の技術（SSEなど）との比較も論じています。

記事「Enabling HTTP/2 and HTTP/3 for Your Laravel App: A Practical Nginx Guide」では、HTTP/2とHTTP/3の導入がLaravelアプリケーションに与えるパフォーマンス改善について詳しく説明しています。特に、HTTP/2とHTTP/3がそれぞれ解決した通信上の課題や、実際の導入手順が記載されています。

記事「Optimizing Laravel on AWS EC2: A Guide to Activating HTTP/2 & HTTP/3 Using Nginx」では、AWS EC2環境でのLaravelアプリケーションにおけるHTTP/2とHTTP/3の導入方法について実践的なガイドが提供されています。特に、Nginxを用いた設定手順や、導入後のパフォーマンス改善の検証方法が詳しく説明されています。

記事「Scaling Real-Time APIs to 100k+ Concurrent Connections: WebSockets, SSE, and Redis Pub/Sub」では、リアルタイム通信のための技術の選択肢（WebSockets、SSE、Redis Pub/Sub）について比較し、それぞれの特徴や適用範囲を説明しています。特に、大規模な接続数を扱う場合の技術選定のポイントが強調されています。

## 深掘り調査で得られた知見

WebSocketは、クライアントとサーバー間で双方向のフルダイクス通信を可能にするプロトコルであり、HTTPとは異なり、接続が確立されるとその状態を維持し、両者が任意のタイミングでデータを送信できる。このプロトコルは、通常のHTTP通信の制限を克服するためのもので、特にリアルタイム通信に適している。WebSocketの通信は、3段階のプロセスで行われる。最初の段階はオープニングハンドシェイクで、通常のHTTP接続がWebSocket接続にアップグレードされる。次の段階はデータ転送で、両者が同時にデータを送信できる。最後の段階はクロージングハンドシェイクで、接続が終了される。WebSocketは、ポーリングやロングポーリングといったHTTPベースの代替手段の制限を克服し、より効率的な通信を実現する。また、WebSocketはHTTPのポート（80/443）で動作するため、ファイアウォールの制限を乗り越えることができる。このプロトコルは、ブラウザが提供するクリーンなAPIを通じて、ブラウザとサーバー間のリアルタイム通信の標準として広く採用されている。ただし、WebSocketは一方向の更新にはSSE（Server-Sent Events）がより適している。WebSocketは、リアルタイム通信のための最も機能的な選択肢だが、その状態維持と永続的な接続により、スケーリングやロードバランシング、デプロイメントにおいて操作的な負担が大きい。WebSocketのプロトコルは、HTTP/2やHTTP/3の導入とともに、パフォーマンスの向上を図るための技術として注目されている。特に、HTTP/3はUDPベースのQUICを採用し、パケットロストによる遅延を軽減する効果が確認されており、モバイルネットワークや遅延のある環境で特に効果が顕著である。Laravelアプリケーションにおいて、HTTP/2とHTTP/3の導入により、リソースの読み込み速度が向上し、ユーザー体験が改善される可能性がある。ただし、導入の効果はネットワーク環境やブラウザのサポートに大きく依存するため、特定の条件では改善効果が限定的である可能性がある。Nginxを用いたHTTP/2とHTTP/3の設定手順は、Ubuntu 24.04での導入が可能であり、具体的な設定が示されている。

## 不確実な点・追加確認が必要な点

WebSocketプロトコルは、クライアントとサーバー間で双方向のフルダイクス通信を可能にする通信プロトコルであり、HTTPのリクエスト応答モデルとは異なり、接続が確立されると一方または他方がデータを送信できるようにする。このプロトコルは、3つのフェーズに分かれており、最初はHTTP接続をWebSocket接続にアップグレードするオープニングハンドシェイク、次にデータ転送、最後に接続を終了するクロージングハンドシェイクである。WebSocketは、ポーリングやロングポーリング、HTTPストリーミングなどのHTTPベースの代替手段の制限を克服するために設計された。しかし、WebSocket接続はステートフルで永続的であり、スケーリングやロードバランシング、デプロイメントを複雑にする。また、WebSocketはブラウザが提供するクリーンなAPIを通じてブラウザとサーバー間のリアルタイム通信の標準であり、ブラウザがraw HTTP/2フレーミングを提供しないことから、ネイティブのgRPC通信も可能でない。一方で、WebSocketはリアルタイム通信のための最も機能的な選択肢であり、その一方で運用上の負荷が高い。他のリアルタイム通信技術として、サーバーからクライアントへの一方向通信に特化したServer-Sent Events（SSE）が簡潔で、WebSocketよりも簡単な場合もある。記事の内容から、WebSocketの通信モデルやプロトコルフェーズ、使用例、他のリアルタイム通信技術との比較が明確に説明されている。ただし、記事の公開日時や取得日時が不明であるため、情報の新旧を正確に判断することはできない。また、記事1のURLから取得した情報と、記事2のURLから取得した情報には、WebSocketプロトコルの目的や使用例についての一致点と相違点が存在する。例えば、記事1ではWebSocketがリアルタイム通信の標準であることを強調しているのに対し、記事2ではWebSocketが唯一の選択肢ではなく、SSEなどの他の技術も存在することを指摘している。このような情報の違いは、読者にとって理解を深めるための重要な要素となる。

## 元記事一覧

- [Realtime from First Principles, Part 2: WebSocket and The ...](https://dev.to/abdulmalikalayande/realtime-from-first-principles-part-2-websocket-and-the-websocket-protocol-2ddg)
- [WebSockets & Real-Time · Chapter 24 · Backend from First ...](https://backend-from-first-principle.vercel.app/24-websockets-and-real-time/)
- [Enabling HTTP/2 and HTTP/3 for Your Laravel App: A Practical Nginx Guide - DEV Community](https://dev.to/deploynix/enabling-http2-and-http3-for-your-laravel-app-a-practical-nginx-guide-1n0c)
- [Optimizing Laravel on AWS EC2: A Guide to Activating HTTP/2 & HTTP/3 Using Nginx - laraveldiary.com](https://laraveldiary.com/posts/optimizing-laravel-on-aws-ec2-a-guide-to-activating-http2-http3-using-nginx)
- [ScalingReal-TimeAPIsto100k+ConcurrentConnections...](https://dev.to/dzakiamriz/scaling-real-time-apis-to-100k-concurrent-connections-websockets-sse-and-redis-pubsub-5hhm)
