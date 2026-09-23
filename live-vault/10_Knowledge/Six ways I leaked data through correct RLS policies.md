---
title: 正しく設定されたRLSでもデータ漏洩のリスク
type: knowledge
status: draft
created: 2026-09-24
updated: 2026-09-24
confidence: medium
---

# 正しく設定されたRLSでもデータ漏洩のリスク

## 結論

RLS（Row Level Security）はPostgreSQLにおける行レベルのアクセス制御機能として設計されているが、その実装や設計のミスにより、正しく設定されているにもかかわらずデータ漏洩が発生する可能性がある。特に、匿名ユーザーがデフォルトでPUBLICに権限を継承する点や、ビューを通じた権限継承、新しいカラム追加時の権限設定の抜け漏れなどが、漏洩の原因となる。これらの問題は、RLS単独では防ぎきれず、他のセキュリティメカニズムとの組み合わせが必須である。

## テーマ概要

Row Level Security（RLS）はPostgreSQLにおいて、行レベルのアクセス制御を実現するための機能として設計されているが、その設計と実装の限界が指摘されている。特に、RLSポリシーが正しく設定されているにもかかわらず、データ漏洩が発生したケースが報告されており、技術的に複雑な問題として注目されている。このテーマは、RLSを導入したシステムにおいても、セキュリティの穴が存在する可能性を示し、RLSを単独で信頼してはならないという警告を含んでいる。また、RLSポリシーの検証方法や、漏洩を防ぐための具体的な対策が求められている。このような背景から、RLSの設計と実装の理解がより深まっている。

## 共通して確認できる点

Row Level Security（RLS）はPostgreSQLにおいて、テーブルレベルでのデータアクセス制御を実現する機能として設計されているが、実装や設計のミスによりデータ漏洩の原因となるケースが複数の記事で指摘されている。特に、RLSポリシーが正しく設定されていても、PostgreSQLの権限システムやPostgRESTなどの他のコンポーネントとの接続部分で漏洩が発生する可能性がある。例えば、匿名ユーザー（anon）はデフォルトでPUBLICに権限を継承し、関数やトリガーのEXECUTE権限をrevokeしても匿名ユーザーが呼び出せる可能性がある。また、ビューを用いたRLS制限の実装では、PostgreSQL 15以上ではビューが所有者の権限を継承するため、意図しないデータが表示されるリスクがある。さらに、新しいカラムを追加する際には、読み取りと書き込みの権限を分けて確認する必要があり、特に書き込み権限はトリガーも含めて検討する必要がある。Supabaseの2026年の変更により、新しいテーブルが自動的にData APIに露出するようになったため、明示的にGRANTを設定する必要がある。RLSはセキュリティの一部であり、完全な保護には他のセキュリティメカニズムとの組み合わせが必要である。

## 記事ごとの差分・視点の違い

記事「Enumeration Attacks: How Exposed Identifiers Enable Abuse」は、識別子が漏洩することで行われる列挙攻撃の仕組みと検出方法を説明しており、特にAPIでの実装例やエラーレスポンスの違いが情報漏洩を促す点を強調している。一方、「API Enumeration Detection Guide for SREs & Security」は、SREやセキュリティエンジニアがAPI列挙攻撃を検出するためのチェックリストやワークフローを提供し、4xxエラーレートやリクエストパターンの分析に焦点を当てている。  

記事「Six ways I leaked data through correct RLS policies」は、RLS（Row Level Security）を導入してもデータ漏洩が発生する事例を実体験として紹介し、PostgreSQLの権限システムやトリガー、ビューの設計における問題点を具体的に分析している。また、「Test your Supabase RLS before you ship: a free red/green fixture and the 9 SQL checks a linter cannot run」は、RLSポリシーのテスト方法を具体的に示し、テスト環境の構築やSQLクエリによるポリシーの検証手段を提供している。  

「The Pretender Gem: User Impersonation in Rails」は、Ruby on Railsでのユーザーインパーセンション機能を紹介しており、管理者アカウントから他のユーザーを擬装する技術の実装例を説明しているが、RLSやデータ漏洩に直接的な関連性はなく、他のセキュリティ課題として位置付けられている。

## 深掘り調査で得られた知見

RLS（Row Level Security）はPostgreSQLにおけるセキュリティ機能として設計されているが、その設計と実装の問題点が指摘されている。匿名ユーザー（anon）はデフォルトでPUBLICに権限を継承するため、関数やトリガーのEXECUTE権限をREVOKEしても、匿名ユーザーが呼び出せる可能性がある。また、ビューを用いてRLSで制限されたカラムを読み込む際、PostgreSQL 15以上ではビューが所有者の権限を継承するため、意図しないデータが表示される可能性がある。新しいカラムを追加する際、読み取りと書き込みの権限を分けて確認する必要があり、特に書き込み権限はトリガーも含めて検討する必要がある。Supabaseの2026年の変更により、新しいテーブルが自動的にData APIに露出するようになったため、明示的にGRANTを設定する必要がある。RLSはセキュリティの一部であり、完全な保護には他のセキュリティメカニズム（権限システム、ビュー、トリガーなど）との組み合わせが必要である。これらの問題点は、RLSの設計と実装の理解を深める上で重要な考慮点である。

## 不確実な点・追加確認が必要な点

記事間の食い違いや、資料からは断定できない点を以下のように具体的に述べることができる。

まず、記事3「Six ways I leaked data through correct RLS policies」では、RLS（Row Level Security）が正しく設定されているにもかかわらず、データ漏洩が発生した事例が紹介されている。この記事では、匿名ユーザー（anon）がデフォルトで PUBLIC に権限を継承するため、関数やトリガーの EXECUTE 権限を revoke しても、匿名ユーザーが呼び出せる可能性があることが指摘されている。また、ビューを用いた場合、PostgreSQL 15 以上ではビューが所有者の権限を継承するため、意図しないデータが表示される可能性があるとされている。

一方で、記事4「Test your Supabase RLS before you ship: a free red/green fixture and the 9 SQL checks a linter cannot run - DEV Community」では、RLS ポリシーのテスト方法が紹介されており、Supabase の RLS ポリシーをテストするための「red/green fixture」というツールが利用可能であることが示されている。また、この記事では、RLS ポリシーのテストに「audit/rls-audit.sql」という9つの読み取り専用クエリが提供されており、これらは Supabase SQL エディタで利用可能であるとされている。ただし、このファイルは SQL エディタでは RLS をバイパスするため、実際のテストには別のアプローチが必要であるとされている。

また、記事1「Enumeration Attacks: How Exposed Identifiers Enable Abuse | Azion」や記事2「API Enumeration Detection Guide for SREs & Security」では、API における ENUMERATION 攻撃の検出方法や、その特徴について説明されている。これらの記事では、ENUMERATION 攻撃は低速で進行し、通常のトラフィックと区別がつきにくいが、4xx エラーの比率や特定の ID の連続的なアクセスなどのパターンから検出できるとされている。ただし、これらの記事は RLS と直接関係する内容ではなく、一般的なセキュリティリスクについて述べている。

したがって、RLS に関連するデータ漏洩の原因や、その検出・防止方法については、記事3と記事4の内容が中心となるが、記事1や記事2の ENUMERATION 攻撃の検出方法は、RLS と連携して検討する必要がある。また、記事5「The Pretender Gem: User Impersonation in Rails - YouTube」では、Ruby on Rails の Pretender Gem を用いたユーザーの偽装が紹介されているが、これは RLS と直接的な関連性は見られず、他のセキュリティツールや手法に分類される。

## 元記事一覧

- [Enumeration Attacks: How Exposed Identifiers Enable Abuse | Azion](https://www.azion.com/en/blog/enumeration-attacks-exposed-identifiers-security/)
- [API Enumeration Detection Guide for SREs & Security](https://www.indusface.com/learning/api-enumeration-detection-guide/)
- [SixwaysIleakeddatathroughcorrectRLSpolicies](https://dev.to/basildrazarch/six-ways-i-leaked-data-through-correct-rls-policies-3l39)
- [Test your Supabase RLS before you ship: a free red/green fixture and the 9 SQL checks a linter cannot run - DEV Community](https://dev.to/cekuu35/test-your-supabase-rls-before-you-ship-a-free-redgreen-fixture-and-the-9-sql-checks-a-linter-388d)
- [The Pretender Gem:UserImpersonationinRails- YouTube](https://www.youtube.com/watch?v=qn0k408GRZg)
