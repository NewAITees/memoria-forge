---
title: Exploring Sentry: Reducing Load Time 🐢
created: 2026-08-10
updated: 2026-08-10
---

# Exploring Sentry: Reducing Load Time 🐢

## 概要
Sentryは、アプリケーションのパフォーマンスを監視し、パーセンタイル（p95）のロードタイムを改善するためのツールとして利用されています。特に、キャッシュ戦略の変更により、パフォーマンスの改善が確認されています。

## 詳細
- **キャッシュ戦略の変更**: `proxy_cache_background_update`と`proxy_cache_use_stale`の使用により、15分のTTLが切れた後、次の訪問者は既存のコピーをすぐに取得し、バックグラウンドで更新が行われる。これにより、ユーザーが待機する必要がなくなる。
- **ロードタイムの改善**: あるプロジェクトでは、8月4日から8月5日にかけて、p50の値が約60%改善されました。
- **API呼び出しのキャッシュ**: `GET /api/devto`は、キャッシュにより外部APIへの呼び出しが不要となり、ロードタイムが大幅に短縮されました。
- **Sentryの機能**: Tracingにより、フレームワークやライブラリのパフォーマンスデータを自動的に収集し、アプリケーション全体のスタックを監視します。

## ソース
- [Exploring Sentry: Reducing Load Time - DEV Community](https://dev.to/annavi11arrea1/exploring-sentry-reducing-load-time-52gf)
- [Application Performance Monitoring (APM) Solution | Sentry](https://sentry.io/solutions/application-performance-monitoring/?content=467860165334)
- [Performance Monitoring - Sentry](https://docs.sentry.io/product/sentry-basics/performance-monitoring/)
- [Making Performance Monitoring More Actionable with Sentry](https://blog.sentry.io/making-performance-monitoring-more-actionable-with-sentry/)
- [docs.sentry.io](https://docs.sentry.io/product/sentry-basics/performance-monitoring.md)

## 不明点
- キャッシュ戦略の変更が具体的にどのように実装されたかは不明。
- 他のキャッシュ戦略やパフォーマンス改善手法の比較は行われていない。

## 未解決の点
- 他のキャッシュ戦略やパフォーマンス改善手法の効果を比較する情報が不足している。
- ロードタイム改善の他の要因（例：Webpack最適化、レイジー読み込み）がどう影響したか不明。

## 出典


## 未解決点

- 追加調査が必要です。
