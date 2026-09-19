---
title: AWS Serverlessの設計と実装におけるベストプラクティスとアンチパターン
type: knowledge
status: draft
created: 2026-09-20
updated: 2026-09-20
confidence: medium
---

# AWS Serverlessの設計と実装におけるベストプラクティスとアンチパターン

## 結論

AWS Serverlessの設計において最も重要な判断は、Lambda関数のステートレス性を維持し、/tmpディレクトリの制限を意識した設計を行うことである。ステートフルな設計や長時間実行タスクは、Step Functionsやキューを活用した分散処理に置き換えるべきであり、Lambda層のARN管理にはAWS Systems Manager Parameter Storeを活用することで、保守性と信頼性を確保する必要がある。

## テーマ概要

AWS Serverless Patterns and Anti-Patterns は、AWS Lambda や他のサーバーレスサービスを効果的に利用するためのベストプラクティスと逆パターンを明らかにするテーマです。このテーマは、Lambda 関数の設計や運用において、/tmp ディレクトリの制限、ステートフルな設計、長時間実行タスクの処理、IAM ロールの設定など、具体的な課題や回避策を検討します。また、AWS AppConfig Agent Lambda extension の ARN 管理や AWS Parameter Store の利用、Lambda Managed Instances の動作など、最新のベストプラクティスも含まれています。これらの内容は、サーバーレスアーキテクチャを安全かつ効率的に構築・運用するための実践的な知識を提供し、特に多様な環境やスケーラビリティの要求が高い現代のクラウドアプリケーションにおいて注目されています。

## 共通して確認できる点

AWS Lambda関数では、/tmpディレクトリに一時的なデータを保存することができるが、関数が終了するとそのデータは失われるため、ステートを保持する必要がある場合は外部ストレージ（例：DynamoDB、Cosmos DBなど）に保存するべきである。また、Lambda関数はステートレスであるべきであり、ステートフルな設計は避けるべきである。Lambda関数のタイムアウト制限は15分であり、長時間実行が必要なタスクはStep FunctionsやDurable Functions、キュー、コンテナ化されたワークフローに分解すべきである。AWS Systems Manager Parameter Storeは、Lambda層のARNなどの情報を最新で取得するための手段として推奨されており、ハードコードを避けてデプロイ時に最新の値を取得することができる。AWS Lambda Managed Instances（LMI）では、MinExecutionEnvironmentsとMaxExecutionEnvironmentsが両方0に設定された場合、関数バージョンが非アクティブ化され、呼び出しは失敗する。LMIではCapacity Providerが必須であり、関数とCapacity Providerのアーキテクチャが一致していないと関数の作成が拒否される。また、LMIは冷起動をサポートせず、非同期でスケーリングを行う。

## 記事ごとの差分・視点の違い

記事「Breaking Down Serverless Anti-Patterns」では、Lambda関数の/tmpディレクトリの制限や、ステートフルな設計の問題が強調されており、特に一時的なデータ保存に関する誤った実装がAnti-Patternとして取り上げられている。一方、「AWS Serverless patterns & best-practices in AWS | PPTX」では、Serverlessの誤解を解くためのMythを列挙し、ステートフルな設計やコストの誤った認識といった問題点を指摘している。また、「# Stop hardcoding AWS Lambda layer ARNs, and use AWS Systems Manager Parameter Store」では、LambdaレイヤーのARNをハードコードするリスクと、Parameter Storeを活用した柔軟な管理方法が議論されており、コードの保守性と運用の信頼性に焦点を当てている。さらに、「Stop hardcoding! Use AWS Parameter Store instead (Hands-On)」では、Parameter Storeの実装例を紹介し、環境変数や秘密情報の管理方法について実践的なアプローチを提示している。最後に、「AWS Lambda Managed Instances: What Min=0/Max=0 Actually Does in Production」では、LMIの設定におけるMin/Maxの動作と、関数バージョンの非アクティブ化の仕組みが詳しく説明されており、非連続的なワークロードの実行における課題が明示されている。各記事は、Serverlessアーキテクチャにおける設計の良し悪しや運用上の課題を異なる視点から掘り下げている。

## 深掘り調査で得られた知見

AWS Serverlessの設計と実装において、いくつかの重要な実践と注意点が明らかになりました。特に、Lambda関数の使用においては、/tmpディレクトリの制限や、ステートフルな設計の回避が重要です。AWS Lambdaでは、/tmpディレクトリは一時的なデータ保存に限られ、関数が終了するとデータが失われるため、DynamoDBやCosmos DBなどの外部ストレージを活用してステートを保存する必要があります。また、Lambda関数はステートレスであるべきであり、インメモリでのステート保持は避けるべきです。

さらに、Lambda層のARNをハードコードするのではなく、AWS Systems Manager Parameter Storeを活用することで、最新のARNを取得し、デプロイ時のバージョン管理を容易にします。これにより、AWSが更新した場合でも、自動的に最新のバージョンを使用できるため、保守作業が簡素化されます。また、Parameter Storeはパブリックパラメータとして利用可能で、どのAWSアカウントからでも読み取ることができます。

AWS Lambda Managed Instances（LMI）では、MinExecutionEnvironmentsとMaxExecutionEnvironmentsを両方0に設定すると、関数バージョンが非アクティブ化され、呼び出しは失敗します。これは標準LambdaのConcurrency Throttlingとは異なり、非連続的なワークロードには不向きです。LMIではCapacity Providerが必要であり、関数とCapacity Providerのアーキテクチャが一致していないと関数の作成が拒否されます。また、LMIは冷起動をサポートせず、非同期でスケーリングします。これらは、LMIの運用において注意が必要な点です。

## 不確実な点・追加確認が必要な点

AWS Serverless Patterns and Anti-Patternsに関する調査では、いくつかの記事間で情報の整合性や明確性に違いが見られ、特定の点については断定できない部分も確認されました。まず、Lambda関数の/ tmpディレクトリに関する記述は、記事1と記事5の深掘り調査結果で一致しています。AWS Lambdaでは、/ tmpディレクトリは一時的なデータ保存にのみ使用でき、関数が終了するとデータが失われるため、外部ストレージへのステート保存が推奨されています。しかし、記事2のスライド資料では、Lambdaのステートフルな設計に関する記述が含まれており、この点については、具体的な実装や問題点についての詳細な情報が不足しています。

また、AWS Parameter Storeの利用に関する記述は、記事3と記事4で一致しています。LambdaレイヤーのARNや、AMI IDなどの情報をハードコードせず、Parameter Storeから取得する方法が推奨されており、これによりバージョンアップ時の静的ドリフトを防ぐことが可能になります。ただし、記事3では、x86とx86_64の区別について言及されており、この点は他の記事では触れられていません。そのため、この区別がどの程度重要か、あるいは他のアーキテクチャでも同様の扱いがあるのかについては、断定できません。

さらに、AWS Lambda Managed Instances（LMI）に関する記事5では、MinExecutionEnvironmentsとMaxExecutionEnvironmentsが両方0に設定された場合の挙動が詳細に記述されています。この設定では、関数バージョンが非アクティブ化され、呼び出しは失敗するという現象が確認されています。ただし、この動作はAWSドキュメンテーションでは明記されておらず、実際の動作を確認するには、特定の環境でのテストが必要であることが示されています。そのため、LMIの運用に関する詳細なガイドラインやベストプラクティスについては、今後のAWSからの情報が求められます。

これらの点から、AWS Serverlessのパターンとアンパタンの情報は、一部の記事では明確に記述されているものの、他の記事では情報が不足している部分もあり、今後の更新や補完が必要であることがわかります。

## 元記事一覧

- [Breaking Down Serverless Anti-Patterns](https://blog.thundra.io/breaking-down-serverless-anti-patterns)
- [AWS Serverless patterns & best-practices in AWS | PPTX](https://www.slideshare.net/slideshow/aws-serverless-patterns-bestpractices-in-aws/250971533)
- [# Stop hardcodingAWSLambdalayer ARNs, and useAWSSystems...](https://dev.to/aparkris/-stop-hardcoding-aws-lambda-layer-arns-and-use-aws-systems-manager-parameter-store-public-p70)
- [Stophardcoding!UseAWSParameterStoreinstead(Hands-On)](https://aws.plainenglish.io/stop-hardcoding-use-aws-parameter-store-instead-hands-on-45a771ad3897)
- [AWSLambdaManagedInstances: WhatMin=0/Max=0Actually...](https://dev.to/aws_sa_sg/aws-lambda-managed-instances-what-min0max0-actually-does-in-production-en1)
