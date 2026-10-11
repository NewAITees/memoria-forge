---
title: JavaでQUICを純粋なJavaで実装する取り組み
type: knowledge
status: draft
created: 2026-10-11
updated: 2026-10-11
confidence: medium
---

# JavaでQUICを純粋なJavaで実装する取り組み

## 結論

JavaでQUICを純粋なJavaで実装する取り組みは、非ブロッキングI/Oを重視したフレームワークの要件に応えるための重要な技術的挑戦であり、既存のJavaエコシステムにおけるQUICサポートの不足を補うための自前の実装が求められている。この実装は、非同期イベントループを駆動し、パケット保護やQPACK、HTTP/3のサポートなど、QUICの主要な機能を提供する一方で、TLS 1.3やPQCの導入など、セキュリティ面での進化も検討されている。

## テーマ概要

Writing QUIC in Pure Java refers to the development of a QUIC (Quick UDP Internet Connections) protocol implementation using only Java, without relying on native libraries or external dependencies. This approach is significant because the Java ecosystem traditionally lacks native QUIC support, and existing implementations often depend on C-based libraries through JNI, which complicates the use of pure Java frameworks. The interest in this topic has grown due to the increasing demand for asynchronous, non-blocking I/O in modern web applications and the need for efficient transport protocols like QUIC, which underpins HTTP/3. The ability to implement QUIC in pure Java allows developers to integrate it seamlessly into Java-based frameworks, avoiding the limitations of thread-per-connection models and enabling high-performance, scalable applications. This has become a focus area as developers seek to leverage QUIC's benefits, such as reduced latency and improved congestion control, within fully Java-based environments.

## 共通して確認できる点

JavaでQUICを純粋なJavaで実装する取り組みは、非ブロッキングI/Oを重視したフレームワークの要件に応えるための試みとして注目されています。特に、gumdropという非同期のJavaサーバーフレームワークでは、QUICの実装がHTTP/3のサポートと同等の非ブロッキングイベントループを駆動する必要がありました。この実装では、パケット保護、ロス検出、NewRenoのコンゴースションコントロール、接続移動、0-RTT、QPACK、HTTP/3クライアントとサーバーなど、QUICの主要な機能がすべて非同期イベントループによって実現されています。また、DNS-over-QUIC（DoQ）もこのQUICスタックによってサポートされており、DNSリゾルバ自体も非同期で動作しています。この実装は、JavaエコシステムにおけるネイティブなQUICサポートの欠如を補う試みとして、非ブロッキングI/Oを前提としたフレームワークの設計に合致しています。さらに、TLS 1.3の実装はAgent15プロジェクトから提供され、今後はPQC（Post-Quantum Cryptography）をデフォルトとして導入する計画が進められています。

## 記事ごとの差分・視点の違い

記事「Writing QUIC in Pure Java - DEV Community」は、Javaの非ブロッキングI/OフレームワークであるgumdropにHTTP/3を統合するための純JavaでのQUIC実装に焦点を当てており、非同期処理や単一スレッドイベントループの重要性を強調しています。一方、「QUIC - Wikipedia」はQUICプロトコルの概要と歴史、および主にブラウザでのサポート状況を説明しており、技術的な実装よりもプロトコル自体の背景を重視しています。また、「You're importing pako to gzip data. `CompressionStream` does ...」は、JavaScriptにおけるデータ圧縮のための新しいネイティブAPIであるCompressionStreamを紹介し、従来のライブラリpakoとの比較をしています。これはQUICの実装とは直接関係ありませんが、同様にJavaScript環境における非ブロッキングI/Oの実装に触発されている可能性があります。「CompressionStream - Web APIs | MDN」は、CompressionStream APIの仕様や使用例を技術的に詳述しており、開発者向けの実装ガイドとしての役割を持っています。最後に、「Building a Leak-Safe gRPC Frame Decoder on ReactorNetty」は、gRPCフレームデコーダーの設計と実装に注力し、ネットワークプロトコル処理におけるメモリリーク防止の技術的課題を扱っており、QUICの実装とは異なる分野ですが、同様の非同期通信処理の設計思想を共有しています。

## 深掘り調査で得られた知見

JavaでQUICを純粋なJavaで実装する取り組みは、非ブロッキングI/Oを基盤とするフレームワークの拡張として注目されています。この実装は、既存のJavaエコシステムにおけるQUICサポートの不足を補うため、独自の実装が求められています。JDKの実験的なサポート（JEP 517）はクライアントのみに限られ、NettyのようなライブラリはJNI経由でquiche + BoringSSLを使用しています。これにより、純粋なJavaフレームワークではネイティブな実装が望まれるため、自前のQUIC実装が検討されました。

この実装は、gumdropという非同期I/Oフレームワーク内で動作し、パケット保護、ロス検出、NewRenoの congestion control、接続移動、0-RTT、QPACK、HTTP/3クライアントとサーバーを含む一連の機能を提供します。これらはすべて、非ブロッキングイベントループによって駆動されています。また、DNS-over-QUIC（DoQ）もこのQUICスタックによってサポートされ、DNSリゾルバは非同期で動作し、InetAddress.getByName()のブロッキング操作を避けています。

さらに、TLS 1.3はAgent15プロジェクトから導入されており、今後はPQC（Post-Quantum Cryptography）がデフォルトとして統合される計画です。この実装は、一般的な非同期I/Oフレームワークとしてのgumdropの一部であり、QUICは単なるトランスポートプロトコルとして位置付けられています。これにより、単線程での接続処理を避けることで、スケーラビリティとパフォーマンスの向上が期待されています。

## 不確実な点・追加確認が必要な点

記事間での情報の整合性や断定できない点について、以下のようにまとめることができます。

記事1と記事2は、QUICの純Java実装に関する情報を提供していますが、記事1はQUICの一般的な概要とその導入経緯を説明しており、記事2は具体的な実装への取り組みとその背景を述べています。記事2では、JavaエコシステムにおけるQUICのサポート不足や、NettyがJNI経由でquiche + BoringSSLを使用している点が述べられており、これは記事1で述べられているQUICの導入と実装の現状とは異なる側面を示しています。

記事3と記事4は、CompressionStreamとDecompressionStreamの利用について述べており、記事3は2026年8月に公開された記事であることが明記されており、記事4はMDNのドキュメンテーションで2026年9月28日に更新されていることが確認されています。これにより、CompressionStream APIの導入時期とその利用状況が明確になっていますが、QUICの純Java実装との関連性は直接的に示されていません。

記事5は、gRPCフレームデコーダーの設計と実装について述べており、QUICやHTTP/3との直接的な関連性は示されていません。そのため、QUICの純Java実装とgRPCフレームデコーダーの関連性については、資料からは断定できません。

また、記事2で述べられている純JavaでのQUIC実装は、GitHubリポジトリがアーカイブされていることや、Kwikの使用が推奨されていることから、その実装の現状や今後の展開については、明確な情報が提示されていません。そのため、QUICの純Java実装の現在の状況や今後の方向性については、断定的な記述は避けられる必要があります。

## 元記事一覧

- [QUIC- Wikipedia](https://en.wikipedia.org/wiki/QUIC)
- [WritingQUICinPureJava- DEV Community](https://dev.to/cpkb/writing-quic-in-pure-java-2536)
- [You're importing pako to gzip data. `CompressionStream` does ...](https://bestpractic.org/blog/compressionstream-native-gzip)
- [CompressionStream- Web APIs | MDN](https://developer.mozilla.org/en-US/docs/Web/API/CompressionStream)
- [BuildingaLeak-SafegRPCFrameDecoderonReactorNetty](https://dev.to/qianwj/building-a-leak-safe-grpc-frame-decoder-on-reactor-netty-po7)
