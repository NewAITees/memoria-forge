---
title: .NET 10 での ActivitySamplingResult PropagationData の Recorded が False になる理由
type: knowledge
status: draft
created: 2026-10-20
updated: 2026-10-20
confidence: medium
---

# .NET 10 での ActivitySamplingResult PropagationData の Recorded が False になる理由

## 結論

.NET 10 では、ActivitySamplingResult.PropagationData の挙動が変更され、親アクティビティが Recorded に設定されていた場合でも、子アクティビティが自動的に Recorded とみなされることが廃止されました。これにより、ローカルのサンプリング結果が優先され、PropagationData で生成される子アクティビティの Recorded と IsAllDataRequested はどちらも false に設定されるようになりました。この変更は OpenTelemetry の仕様と整合性を保つため行われ、カスタムサマッパーまたはエクスポートツールが以前の挙動に依存していた場合、トレース情報が不完全になる可能性があります。

## テーマ概要

.NET 10 で導入された ActivitySamplingResult.PropagationData の挙動変更が注目されている。以前は親アクティビティが Recorded に設定されていた場合、子アクティビティも自動的に Recorded とみなされていたが、.NET 10 からはこの継承が廃止され、ローカルのサンプリング結果が優先されるようになった。この変更は OpenTelemetry の仕様に合わせたもので、トレースの識別情報は引き続き流れるが、ローカルでのサンプリング決定が重要視されるようになった。この変更により、カスタムサマッパーやエクスポーターが以前の挙動に依存していた場合、トレースのスパンが欠落したり、データが未設定になるなどの問題が発生する可能性がある。また、この変更は .NET 10 のリリース日である 2026 年 8 月 27 日に導入され、ドキュメンテーションでは 2026 年 9 月 30 日に更新されている。

## 共通して確認できる点

.NET 10 では、ActivitySamplingResult の PropagationData が変更され、子アクティビティが親の Recorded フラグを継承する仕様が廃止されました。以前は親アクティビティが Recorded に設定されていた場合、子アクティビティも自動的に Recorded とみなされていましたが、この挙動は OpenTelemetry の仕様と一致しないと判断され、変更されました。結果として、子アクティビティの Recorded と IsAllDataRequested はどちらも false に設定されるようになりました。この変更により、カスタムサマッパーまたはエクスポートツールが以前の挙動に依存していた場合、トレース情報が不完全になる可能性があります。Microsoft はこの変更を .NET 10 の互換性ノートで明記しており、以前の挙動を再現するには Activity.ActivityTraceFlags を Recorded に設定する必要があると説明しています。この変更は 2026 年 8 月 27 日に導入され、2026 年 9 月 30 日にドキュメントで確認されています。

## 記事ごとの差分・視点の違い

記事ごとの立場や強調点、論点の違いは以下の通りです。

記事1では、.NET 10におけるActivitySamplingResult.PropagationDataの挙動変更が、カスタムサマッパーとエクスポーターに与える影響を重点的に説明しています。特に、親の Recorded フラグが子に引き継がれなくなったことによる、トレース情報の欠落やデータの未設定といった問題点を挙げ、Microsoftが提供する回避策も紹介しています。また、この変更が.NET 10のリリース日である2026年8月27日に導入されたことを明示しています。

記事2は、同様の変更点を説明していますが、より技術的な観点から、ローカルのサンプリング決定が親のフラグを上書きする仕組みについて詳しく解説しています。また、この変更がOpenTelemetryの仕様と整合性を保つために行われたものであることを強調しており、カスタムリスナーの設計における Recorded と IsAllDataRequested の違いについても説明しています。

記事3と記事4は、.NET 10におけるBufferedStream.WriteByteの挙動変更について述べていますが、記事3は開発者向けのコミュニティ記事であり、具体的なサンプルコードやテストケースを通じて変更点を解説しています。一方、記事4はMicrosoft Learnの公式ドキュメントであり、変更の背景と影響範囲をより公式な立場で説明しています。また、記事4では、この変更が.NET 10 LTSの安定機能として採用されていることを明記しています。

記事5は、.NET 10における汎用数学関数のシフト演算に関する変更点を扱っていますが、本テーマとは直接関係がありません。したがって、この記事は他のテーマのレポートに属するため、本セクションでは対象外とします。

## 深掘り調査で得られた知見

.NET 10 では、ActivitySamplingResult.PropagationData の挙動が変更され、子アクティビティが親の Recorded フラグを継承する仕様が廃止されました。以前は親アクティビティが Recorded に設定されていた場合、子アクティビティも自動的に Recorded とみなされていましたが、この変更により、親の Recorded フラグは子アクティビティの Recorded 状態に影響を与えなくなりました。代わりに、ローカルのサンプリング決定が優先されるようになり、PropagationData で生成された子アクティビティは Recorded と IsAllDataRequested の両方が false に設定されます。この変更は OpenTelemetry の仕様と整合性を保つため行われ、Microsoft が .NET 10 の互換性ノートで明記しています。また、この変更により、カスタムサマッパーやエクスポートツールが以前の挙動に依存していた場合、トレーシングシステムでスパンが不足したり、データが未設定になるといった問題が生じる可能性があります。Microsoft は、この挙動を復元するためのワークアラウンドとして、Activity.ActivityTraceFlags を Recorded に設定する方法を提供しています。この変更は 2026 年 8 月 27 日に .NET 10 で導入され、9 月 30 日に .NET のドキュメンテーションに反映されました。

## 不確実な点・追加確認が必要な点

.NET 10 における ActivitySamplingResult.PropagationData の挙動変更について、複数の資料が記載しているが、記事間で若干の表現の違いが確認されている。記事 1 と記事 2 は、.NET 10 で子アクティビティが親の Recorded フラグを継承しなくなった点を共通認識としており、その理由として OpenTelemetry の仕様との整合性を挙げている。一方で、記事 1 では「Microsoft の互換性ノートがこの変更を明記している」と述べているが、記事 2 では「Microsoft の互換性ノートがこの変更を明記している」と同様に記載しているため、両者間の記述は一致している。ただし、記事 1 では「 Recorded == false かつ IsAllDataRequested == false が設定される」と明記されているが、記事 2 では「 Recorded が false に設定され、 IsAllDataRequested は false のまま」と記載しているため、 IsAllDataRequested の状態についての記述が微妙に異なっている。また、記事 1 では「Microsoft は .NET 10 互換性ノートでこの変更を明記している」と記載されているが、記事 2 では「Microsoft の互換性ノートがこの変更を明記している」と記載しており、具体的なノートの URL や公開日時については記載されていないため、断定的な記述は避けている。また、記事 1 では「 Recorded フラグが継承されなくなったことで、カスタムリスナーが影響を受ける可能性がある」と述べているが、記事 2 では「カスタムサンプラーがこの変更により影響を受ける可能性がある」と記載しており、表現の違いが確認されている。これらの点から、記事間には若干の表現の違いが存在しており、断定的な記述は避けている。

## 元記事一覧

- [.NET 10 ActivitySamplingResult PropagationData: Why Recorded ...](https://dev.to/ssukhpinder/net-10-activitysamplingresult-propagationdata-why-recorded-turns-false-d1g)
- [.NET 10 ActivitySamplingResult PropagationData: Why Recorded ...](https://dnt.co.il/net-10-activitysamplingresult-propagationdata-why-recorded-turns-false/)
- [NET10BufferedStreamWriteByte:FlushFull... - DEV Community](https://dev.to/ssukhpinder/net-10-bufferedstream-writebyte-flush-full-buffers-explicitly-45a2)
- [Breaking change -BufferedStream.WriteByteno... | Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/core/compatibility/core-libraries/10.0/bufferedstream-writebyte-flush)
- [NET10GenericMathShiftMasking: Catch... - DEV Community](https://dev.to/ssukhpinder/net-10-generic-math-shift-masking-catch-overshifts-that-now-wrap-1612)
