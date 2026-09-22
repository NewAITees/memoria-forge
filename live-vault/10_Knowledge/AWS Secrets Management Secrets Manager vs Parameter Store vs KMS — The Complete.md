---
title: AWS Secrets Management における Secrets Manager と Parameter Store の選択基準
type: knowledge
status: draft
created: 2026-09-22
updated: 2026-09-22
confidence: medium
---

# AWS Secrets Management における Secrets Manager と Parameter Store の選択基準

## 結論

AWS シークレット管理において、シークレットの回転が必要な場合は必ず Secrets Manager を使用し、非回転の構成データは Parameter Store で管理すべきである。KMS は暗号化キーの管理に特化しており、Secrets Manager と Parameter Store の下層にあるため、暗号化機能を必要とする場合は KMS を活用する必要がある。シークレットをコードや環境変数にハードコードせず、IAM ロールと管理されたストアを活用して安全に管理することが、コストとセキュリティのバランスを取る上で不可欠である。

## テーマ概要

AWS シークレット管理における Secrets Manager、Parameter Store、KMS の比較は、セキュリティとコスト効率を両立させるための重要なテーマです。特に、Secrets Manager は自動回転やクロスアカウント共有をサポートし、~$0.40/secret/month のコストで提供される一方、Parameter Store は汎用的な構成データの保存に適しており、KMS を用いた暗号化が可能です。KMS は暗号化キーの管理サービスであり、Secrets Manager と Parameter Store の下層に位置します。この比較は、シークレットのライフサイクル管理やコスト最適化の観点から注目されており、特に回転が必要なシークレットには Secrets Manager を、そうでない場合は Parameter Store を使用すべきというガイドラインが示されています。また、シークレットをコードや環境変数にハードコードせず、IAM ロールや管理されたストアを活用して安全に管理する必要性が強調されています。このような背景から、このテーマは現在、AWS 上での安全かつ効率的なシークレット管理の実装方法を探求する上で重要な位置を占めています。

## 共通して確認できる点

AWS Secrets Management において、Secrets Manager、Parameter Store、KMS はそれぞれ異なる役割を担っており、用途に応じて使い分けるべきである。Secrets Manager はシークレットの回転、クロスリージョンレプリケーション、クロスアカウント共有をサポートしており、~$0.40/secret/month のコストで提供される。一方、Parameter Store は汎用的な構成データの保存に適しており、KMS を使用して暗号化されたシークレットを保存できるが、回転はサポートされていない。KMS は暗号化キーを管理するサービスであり、Secrets Manager と Parameter Store の下層にある。シークレットの回転が必要な場合は、Secrets Manager を使用すべきであり、そうでない場合は Parameter Store を使用すべきである。また、KMS は暗号化キーの管理に使用され、Secrets Manager は認証情報を管理する。シークレットをコードや環境変数にハードコードするのは避けるべきで、IAM ロールと管理されたストアを使用して安全に管理すべきである。このように、シークレット管理は慎重に設計し、コストとセキュリティのバランスを取ることが重要である。

## 記事ごとの差分・視点の違い

記事「AWS Secrets Management: Secrets Manager vs Parameter Store vs KMS — The Complete Decision Guide - DEV Community」は、シークレット管理の3つの主要サービスであるSecrets Manager、Parameter Store、KMSの選定ガイドとして位置付けられており、特に回転が必要なシークレットにはSecrets Managerを、構成情報にはParameter Storeを推奨している。また、KMSは暗号化の基盤となるサービスであり、シークレットの管理には必要だが、独自の暗号化が必要な場合は例外となる。この記事では、コストと機能のバランスを重視し、過剰な使用を避けるためのベストプラクティスも説明されている。

記事「AWS Secrets Manager and Parameter Store Decision Guide - Storing, Rotating, and Accessing Secrets and Configuration | hidekazu-konishi.com」は、Secrets ManagerとParameter Storeの選定に焦点を当て、回転機能や暗号化の仕組み、IAMアクセスの設定など、具体的な実装方法や構成例を詳しく説明している。また、シークレットの回転が必須である場合の手順や、Parameter Storeでの暗号化の実装例も含まれており、実践的なアプローチを重視している。

記事「FindtheAWSResourcesNobodyIsUsing,andWhatTheyCostYou」は、AWSアカウント内の無駄なリソースの特定とコスト分析に特化しており、Secrets ManagerやParameter Storeの選定とは直接関係がないが、リソース管理の観点からコストを意識したシークレット管理の重要性を間接的に示している。また、zombiescanというツールの紹介を通じて、AWS環境の最適化に向けたアプローチを示している。

記事「xbill9/zombiescan:FindtheAWSresourcesnobodyisusing,and...」は、zombiescanツールの技術的詳細や使い方を説明しており、Secrets ManagerやParameter Storeの選定とは別の観点から、AWSアカウントのコスト削減とリソース最適化を推進するツールとしての価値を強調している。このツールは、シークレット管理のコスト分析に役立つ可能性があるが、直接的な比較や選定ガイドには該当しない。

記事「WAFRAutomationToolkit- DEV Community」は、AWS Well-Architected Framework Reviewの自動化ツールとしてのWAFR Automation Toolkitを紹介しており、シークレット管理の選定とは関係が浅いが、AWS環境全体の最適化とセキュリティ確保の観点から、Secrets ManagerやParameter Storeの活用が求められることを間接的に示している。このツールは、シークレット管理の枠を超えたAWS環境の運用管理を支援する存在として位置付けられている。

## 深掘り調査で得られた知見

AWS シークレット管理における Secrets Manager、Parameter Store、KMS の選定ガイドは、コストとセキュリティのバランスを考慮した慎重な設計が求められます。Secrets Manager は、シークレットの回転、クロスリージョンレプリケーション、クロスアカウント共有をサポートしており、~$0.40/secret/month のコストで提供されます。一方、Parameter Store は汎用的な構成データの保存に適しており、KMS を使用した暗号化されたシークレットを保存できますが、回転はサポートされていません。KMS は暗号化キーを管理するサービスであり、Secrets Manager と Parameter Store の下層に位置します。シークレットの回転が必要な場合は Secrets Manager を、そうでない場合は Parameter Store を使用すべきです。また、KMS は暗号化キーの管理に使用され、Secrets Manager は認証情報を管理します。シークレットをコードや環境変数にハードコードするのは避けるべきで、IAM ロールと管理されたストアを使用して安全に管理すべきです。このように、各サービスは目的に応じて使い分けるべきです。さらに、シークレット管理は慎重に設計し、コストとセキュリティのバランスを取ることが重要です。

## 不確実な点・追加確認が必要な点

記事間での情報の整合性や断定できない点について、以下のように整理できます。

記事1と記事2はどちらもAWS Secrets ManagerとParameter Storeの選択ガイドとして位置付けられており、基本的な機能やコストの比較、使用すべきケースについて一致しています。ただし、記事2では公開日時が2026年6月17日に設定されており、記事1の公開日時が不明なため、記事2の方が最新の情報を提供している可能性があります。また、記事2ではKMSの暗号化とシークレット回転の関係についてより詳細に説明されており、シークレット回転が必要な場合にSecrets Managerを推奨しています。一方で、記事1では「Secrets Managerは~$0.40/secret/monthのコスト」という数値が記載されており、記事2には明示的にこのコスト情報が見られません。そのため、コストに関する具体的な数値は記事1にのみ記載されており、記事2ではその情報が省略されている可能性があります。

また、記事1では「Parameter Storeは無料の標準ティアで提供される」と記載されていますが、記事2では「Parameter Storeは無料の標準ティアで提供される」という記述は見られず、代わりに「Parameter Storeは汎用的な構成データの保存に適している」と述べています。このため、Parameter Storeのコストに関する情報は記事1にのみ含まれており、記事2では別の観点から説明されている可能性があります。

さらに、記事1では「KMSは暗号化キーを管理するサービスであり、Secrets ManagerとParameter Storeの下層にある」と記載されており、記事2でも同様の記述が見られますが、KMSの使用についての具体的な手順や制限は記載されていません。したがって、KMSの使用に関する詳細な情報は他の記事やドキュメントを参照する必要があります。

また、記事1と記事2の両方で「シークレットをコードや環境変数にハードコードするのは避けるべき」という同じアドバイスが含まれていますが、具体的な実装方法やベストプラクティスについては記載されていません。そのため、シークレット管理の実装に関する詳細なガイドは、AWSの公式ドキュメントや他の技術資料を参照する必要があります。

## 元記事一覧

- [AWS Secrets Management: Secrets Manager vs Parameter Store vs KMS — The Complete Decision Guide - DEV Community](https://dev.to/alpeshkumbhare/aws-secrets-management-secrets-manager-vs-parameter-store-vs-kms-the-complete-decision-guide-3j71)
- [AWS Secrets Manager and Parameter Store Decision Guide - Storing, Rotating, and Accessing Secrets and Configuration | hidekazu-konishi.com](https://hidekazu-konishi.com/entry/aws_secrets_manager_and_parameter_store_guide.html)
- [FindtheAWSResourcesNobodyIsUsing,andWhatTheyCostYou](https://dev.to/aws-builders/find-the-aws-resources-nobody-is-using-and-what-they-cost-you-35bj)
- [xbill9/zombiescan:FindtheAWSresourcesnobodyisusing,and...](https://github.com/xbill9/zombiescan)
- [WAFRAutomationToolkit- DEV Community](https://dev.to/debapriya_dey_aada54b7766/wafr-automation-toolkit-3ckj)
