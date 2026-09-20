---
title: 20,000人以上が同じ座席をクリックしたときの設計対応
type: knowledge
status: draft
created: 2026-09-21
updated: 2026-09-21
confidence: medium
---

# 20,000人以上が同じ座席をクリックしたときの設計対応

## 結論

座席選択システムにおいて、20,000人以上のユーザーが同時に同じ座席をクリックした場合、RedisとPostgreSQLを組み合わせた設計により、競合状態を回避し、重複販売を防ぐことが可能である。Redisはホルド管理に適し、PostgreSQLは排他制約によって最終的なデータ整合性を保証する。この設計は、高負荷の販売状況でもシステムの信頼性とスケーラビリティを確保するための有効な手段である。

## テーマ概要

テーマ「What Happens When 20,000 People Click the Same Seat」は、大規模イベントやライブの座席選択システムにおける競合状態を扱った話題である。このテーマが注目されている理由は、同時に多数のユーザーが同じ座席を選択しようとした場合に発生する技術的な課題と、それを解決するための設計・実装の複雑さに起因する。具体的には、座席の確保と販売を分離した設計、RedisとPostgreSQLを組み合わせた実装、競合状態を防ぐためのアルゴリズムや制約の導入などが含まれる。このような課題は、高負荷のオンライン販売システムにおいて非常に重要であり、システムの信頼性とスケーラビリティを確保する上で不可欠な要素となる。

## 共通して確認できる点

複数の記事で共通して確認できた事実として、座席選択システムにおける競合処理の課題が強調されています。特に、20,000人以上のユーザーが同時に同じ座席をクリックした場合、システムが適切に対応できない可能性があります。この問題は、座席マップの構築よりも難しいとされており、多くの開発者にとって重要な課題となっています。RedisとPostgreSQLの2つのデータベースを組み合わせることで、座席の確保と販売を分離した設計が採用されています。Redisはキャッシュとして機能し、PostgreSQLは最終的なデータベースとして機能します。座席の販売では、RedisのTTL（タイムトゥーライフ）によってホルドが自動的に削除されるため、手動のクリーンアップが不要です。また、Redisのホッドが失敗した場合でも、PostgreSQLの制約により重複販売が防がれます。

## 記事ごとの差分・視点の違い

記事「SQL Service Broker suddenly stops working – SQLServerCentral Forums」は、SQL ServerのService Brokerが突然動作しなくなる問題の対処法を具体的に説明しています。投稿者は、サービスブローカーのキューが表示されなくなった原因を解決するためにALTER QUEUEコマンドを実行した経験を共有しており、技術的なトラブルシューティングの手順に焦点を当てています。一方、「SQL Server Service Broker – Error Handling」は、Service Brokerにおけるエラー処理と、特に「poison message（毒メッセージ）」の概念を深く掘り下げています。この記事では、メッセージ処理中に発生するエラーが繰り返し発生する場合の対応策や、メッセージの再送信やエラー通知の仕組みについて説明しています。  

記事「WhatHappensWhen20,000PeopleClicktheSameSeat」は、座席選択システムにおける高負荷の状況下での競合問題を実例として取り上げ、RedisとPostgreSQLを組み合わせた設計がどのように問題を解決するかを説明しています。この記事では、座席のホルドと販売の分離、RedisのTTLによる自動クリーンアップ、PostgreSQLの制約による重複販売防止といった技術的設計が強調されています。  

記事「Virtual threads didn't scale your app. They just moved the crash to your database. - DEV Community」は、Java 21のVirtual Threadsの導入によってアプリケーション層でパフォーマンスが向上した一方で、データベースなどのリソース制限が新たなボトルネックとなる現象を指摘しています。この記事では、Virtual Threadsの導入が接続プールの制限を引き起こす可能性があることや、リソースコンカレンシーの限界について議論しています。  

記事「The Transactional Outbox Pattern: Dual-Write Consistency in ...」は、分散システムにおけるデータ一貫性を保つための「トランザクショナルアウトボックスパターン」について説明しています。この記事では、データベース更新とメッセージ送信を一括処理として実行する仕組みや、Change Data Capture（CDC）を活用した実装方法が強調されており、システム全体の信頼性向上に向けた設計思想が述べられています。

## 深掘り調査で得られた知見

深掘り調査により、20,000人以上のユーザーが同時に同じ座席を選択する状況における技術的課題が明らかになりました。座席選択システムでは、ユーザーが座席をクリックした際に、その座席を一時的に確保する「ホルド」機能が重要です。このホルドはRedisなどのキャッシュ技術を用いて実現され、最終的な販売はPostgreSQLなどの永続化データベースに反映されます。Redisはホルドの管理に適しており、TTL（タイムトゥーライフ）によって自動的に削除されるため、手動のクリーンアップが不要です。一方で、PostgreSQLには排他制約が設定されており、ホルドが失敗した場合でも重複販売を防ぐ仕組みが備わっています。

この設計は、座席選択の競合状態を回避するための重要な手段であり、特に大規模なイベントでの座席販売においては不可欠です。また、Redisのホルドが失敗した場合でも、PostgreSQLの制約によってシステムの整合性が維持されることが確認されています。このような設計は、高負荷状態でのシステム安定性を確保するためのベストプラクティスとして注目されています。

## 不確実な点・追加確認が必要な点

記事間で一致しない点として、座席選択システムの設計における競合処理の対応方法について、いくつかの記事で異なるアプローチが提案されている。例えば、「What Happens When 20,000 People Click the Same Seat」では、RedisとPostgreSQLを併用し、座席のホルドをRedisで管理し、最終的な販売をPostgreSQLで処理する方法が説明されている。一方で、他の記事では、Redisのホルドが失敗した場合でもPostgreSQLの制約によって重複販売を防ぐ仕組みが強調されている。また、「Virtual threads didn't scale your app. They just moved the crash to your database.」では、Java 21のVirtual Threadsがアプリケーション層でパフォーマンスを向上させたものの、データベース層でのリソースコンカレンシーの制限によりスケーリングがうまくいかなかったという点が指摘されている。これらの記事は、それぞれ異なる技術的背景や課題を扱っているため、設計や実装の選択肢が異なっていることが確認できる。

## 元記事一覧

- [SQL Service Broker suddenly stops working – SQLServerCentral Forums](https://www.sqlservercentral.com/forums/topic/sql-service-broker-suddenly-stops-working)
- [SQL Server Service Broker – Error Handling | Fortified Data: The Leading Database Managed Services Provider](https://www.fortifieddata.com/sql-server-service-broker-error-handling/)
- [WhatHappensWhen20,000PeopleClicktheSameSeat](https://dev.to/aboalynx/what-happens-when-20000-people-click-the-same-seat-245n)
- [Virtual threads didn't scale your app. They just moved the crash to your database. - DEV Community](https://dev.to/adioof/virtual-threads-didnt-scale-your-app-they-just-moved-the-crash-to-your-database-p7i)
- [The Transactional Outbox Pattern: Dual-Write Consistency in ...](https://dev.to/amasen/the-transactional-outbox-pattern-dual-write-consistency-in-distributed-systems-3e5p)
