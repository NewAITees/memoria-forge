---
type: knowledge
status: draft
created: 2026-08-19
updated: 2026-08-19
confidence: medium
---

+++ 
created: 2026-08-19
updated: 2026-08-19
+++ 
# Month More

## 概要
AWSのコスト異常に関する報道が集中的に発生。代表的な記事として「Everything Was Working. AWS Wanted $1,665/Month More.」が掲載され、AWSのコスト異常検出機能が問題を指摘したが、根本的な原因はインフラストラクチャのドリフトによるものとされている。また、AWSのコストエクスプローラーに起因する、顧客が trillion ドル規模の請求を表示された問題も発覚。実際の請求は影響を受けず、修正が進んでいる。

## 詳細

### AWSのコスト異常
- 「Everything Was Working. AWS Wanted $1,665/Month More.」では、EKSとRDSのサポートの終了により、予期せぬコスト増加が発生した事例が紹介されている。
- クラスターバージョンがサポート終了日に達したことで、AWSがサポート料を請求開始した。
- クラスターアドオンが更新されていないことにより、インフラストラクチャドリフトが進行していた。
- コスト異常検出機能は異常を検出していたが、根本的な原因解明にはエンジニアリング作業が必要だった。

### AWSの請求計算エラー
- 「AWS's Trillion-Dollar Billing Bug Resists First Fix」では、コストエクスプローラーの計算ミスにより、顧客が trillion ドル規模の請求を表示された事例が報告されている。
- 実際の請求は影響を受けず、AWSは修正作業を進めている。
- 原因は「unit pricing」の計算ミスとされ、修正が複数の方法で試みられたが、一時的に修正が失敗した。
- 顧客は誤った請求に驚き、一部ではセキュリティ違反を疑うケースもあった。

### その他関連情報
- 「AWS Cost Explorer Bug Shows Customers Trillion-Dollar Billing Estimates」では、AWSのコストエクスプローラーの誤計算により、顧客が trillion ドル規模の請求を表示された事例が報告されている。
- 「Indian AWS User Left Stunned by $1.5 Trillion Bill」では、インドのAWSユーザーが1.5兆ドルの請求を表示し、ショックを受けた事例が紹介されている。
- 「AWS Billing Bug Shows Customers Trillion-Dollar Estimates While ... - InfoQ」では、AWSのコスト計算システムの設定変更が原因で、顧客に trillion ドル規模の請求が表示された事例が報告されている。

## ソース
- [Everything Was Working. AWS Wanted $1,665/Month More.](https://example.com)
- [AWS's Trillion-Dollar Billing Bug Resists First Fix](https://example.com)
- [AWS Cost Explorer Bug Shows Customers Trillion-Dollar Billing Estimates](https://example.com)
- [Indian AWS User Left Stunned by $1.5 Trillion Bill](https://example.com)
- [AWS Billing Bug Shows Customers Trillion-Dollar Estimates While ... - InfoQ](https://example.com)

## 留意点
- AWSのコスト異常や請求計算ミスは、インフラストラクチャのドリフトや設定ミスが原因となることがある。
- 顧客は誤った請求に驚くため、適切な監視と対応が求められる。
- AWSのコスト管理機能は重要だが、根本的な原因解明にはエンジニアリング作業が必要である。

## 出典

- [Everything Was Working. AWS Wanted $1,665/Month More.](https://dev.to/aws-builders/everything-was-working-aws-wanted-1665month-more-45h)
- [AWS's Trillion-Dollar Billing Bug Resists First Fix](https://www.cyberkendra.com/2026/07/awss-trillion-dollar-billing-bug.html)
- [AWS Cost Explorer Bug Shows Customers Trillion-Dollar Billing Estimates](https://cyberpress.org/aws-cost-explorer-bug/)
- [Indian AWS User Left Stunned by $1.5 Trillion Bill: Here Is Why Amazon ...](https://gadgetsnow.indiatimes.com/tech-news/indian-aws-user-left-stunned-by-1-5-trillion-bill-here-is-why-amazon-cloud-customers-saw-massive-charges/articleshow/132521308.cms)
- [AWS Billing Bug Shows Customers Trillion-Dollar Estimates While ... - InfoQ](https://www.infoq.com/news/2026/07/aws-billing-estimates-incident/)

## 未解決点

- 追加調査が必要です。
