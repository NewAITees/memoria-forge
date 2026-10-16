---
title: AWS Lambdaのwarm startにおける状態保持問題
type: knowledge
status: draft
created: 2026-10-17
updated: 2026-10-17
confidence: medium
---

# AWS Lambdaのwarm startにおける状態保持問題

## 結論

AWS Lambda において、warm start では実行環境が再利用されるため、前回の呼び出しで生成された状態が次の呼び出しでも保持される可能性があります。このため、リクエストごとの状態を保つ必要があり、コードが「stateless」と見なされても、実際には状態が保持されるケースがあります。特に、キャッシュされたトークンやインメモリカウンター、ミュータブルな変数などの設定が、warm start では前回の呼び出しで残るため、リクエストごとの初期化が求められます。

## テーマ概要

AWS Lambda の「warm start でのみ発生するバグ」は、Lambda が実行環境を再利用する仕組みを誤解している開発者が引き起こす問題です。通常、Lambda は冷起動（cold start）では新しい環境を生成し、初期化コストがかかりますが、warm start では前の呼び出しで生成された環境を再利用します。このため、前回の呼び出しで生成された状態（例えばキャッシュされたトークンやインメモリカウンターなど）が次の呼び出しでも保持される可能性があります。これにより、開発者が「stateless」と仮定してコードを書いた場合、warm start では予期せぬ状態が残り、バグが発生する可能性があります。このようなバグは、テスト環境では再現しにくく、本番環境でのみ発覚するため、注意が必要です。このテーマは、Lambda の実行環境再利用の仕組みを理解し、状態管理を正しく行うことで、このような問題を回避するための知見を提供しています。特に、2025年8月から AWS が INIT 階段を課金開始したことで、冷起動のコストが直接的なコストとして考慮されるようになり、このような問題の重要性が増しています。

## 共通して確認できる点

AWS Lambda では、warm start が発生する際、実行環境が再利用されるため、前回の呼び出しで生成された状態が保持される可能性があります。これにより、リクエストごとの状態を保つ必要があり、特定のコードが「stateless」と見なされても、実際には状態が保持されるケースがあります。例えば、キャッシュされたトークンやインメモリカウンター、ミュータブルな変数などの設定が、前回の呼び出しで残るため、リクエストごとの初期化が求められます。

また、Lambda は「stateless」とされることが多いですが、実際には実行環境が再利用されるため、状態が保持される可能性があります。このため、リクエストごとの状態を保つ必要があり、リクエストごとの初期化が求められる場合があります。特に、warm start では、前回の呼び出しで生成された状態が残るため、リクエストごとの状態を保つ必要があります。

さらに、Lambda の cold start では、初期化コストが発生しますが、warm start ではそのコストが回避されます。しかし、warm start では、前回の呼び出しで生成された状態が残るため、リクエストごとの初期化が必要な場合があります。このため、warm start では、前回の呼び出しで生成された状態が残るため、リクエストごとの状態を保つ必要があります。

## 記事ごとの差分・視点の違い

記事「TheLambdaBugThatOnlyShowsUponWarmStarts」では、Lambdaのwarm startにおける実行環境の再利用によって、前回の呼び出しで生成された状態が残る可能性があることを説明し、それに基づくバグの発生メカニズムを示している。特に、キャッシュされたトークンやインメモリカウンタなど、リクエストごとの状態を保持するコードがwarm startでは問題になる可能性があると指摘している。

記事「A Subtle AWSLambdaBugCaused by “Stateless” Assumptions」では、Lambdaが「stateless」と見なされるが、実際には実行環境が再利用されるため、状態が保持される可能性がある点を強調している。特に、ログコンテキストのシングルトンによるtenant情報のリークという具体的な事例を挙げ、その原因が実行環境の再利用にあることを明らかにしている。

記事「WeCutLambdaColdStarts56% —ThreeWrongTurnsBeforethe...」では、Lambdaのcold start問題を解決するための具体的な取り組みとその結果を述べている。SnapStartの導入は効果があったものの、根本的な原因はinitフェーズとhandlerフェーズの分離にあるとし、initフェーズで必要な処理を事前に実行することで冷起動時間を大幅に削減した経験を紹介している。

記事「AWSLambdaColdStarts: Impact and How to Reduce Them」では、Lambdaのcold startの発生条件とその影響、特に2025年8月からのINITフェーズの課金がもたらすコストの変化について解説している。また、ランタイムの選択や処理の最適化がcold startの影響を軽減する重要な要素であると指摘している。

記事「The Lambda Latency Trap: Why Your “12ms” Go API Can Suddenly ...」では、Goで構築されたLambda関数が突然遅くなる原因として、cold startの初期処理が原因であることを説明している。特に、初期処理がhandlerフェーズで実行され、初めてのリクエストで遅延が発生するという現象を示しており、warm startでは問題が発生しないという特性を強調している。

## 深掘り調査で得られた知見

AWS Lambda における「warm start」の特性は、アプリケーションの挙動に重大な影響を与える可能性がある。特に、warm start では実行環境が再利用されるため、前回の呼び出しで生成された状態が残ることがあり、リクエストごとの状態を保持する必要がある。この現象は、Lambda が「stateless」と見なされる一方で、実際には実行環境が再利用されるため、状態が保持される可能性があるという点で矛盾している。

例えば、DynamoDB クライアントやキャッシュされたトークン、インメモリカウンタ、ミュータブル変数などのリソースは、handler 外部で初期化されることが推奨されている。しかし、warm start ではこれらの状態が保持されるため、リクエストごとの初期化が求められる。これにより、コードが「clean slate」を前提で書かれていた場合、warm start では予期せぬ挙動が発生する可能性がある。

このような状況は、実際の運用で深刻な問題となる。例えば、ある企業では、ログメッセージに AWS アカウント ID が不正確に表示されるという問題が発生した。これは、ログコンテキストがシングルトンとして実装されており、warm start でリクエスト間で状態が再利用されたためだった。この問題は、Lambda の実行環境が再利用される仕組みを誤解していたため、発生した。

また、AWS Lambda における cold start は、アプリケーションのパフォーマンスに大きな影響を与える。特に、August 2025 以降、AWS は INIT フェーズを課金対象に含めるようになり、cold start はコストの直接的な問題となった。この変更により、Lambda の初期化処理を最適化する必要性が高まった。

CloudWise は、SnapStart を活用して cold start の時間を大幅に短縮したが、初期の試行では改善が見られなかった。その後、init フェーズで処理を事前に実行することで、cold start 時のパフォーマンスを改善した。このように、Lambda の冷起動を改善するには、init フェーズと handler フェーズの区別が重要であり、適切な設計が求められる。

## 不確実な点・追加確認が必要な点

記事間の食い違いや、資料からは断定できない点を具体的に書く。

いくつかの記事では、AWS Lambda の warm start において、実行環境が再利用されるため、前回の呼び出しで生成された状態が残る可能性があることが指摘されている。これは、リクエストごとの状態を保つ必要があるという警告として示されている。例えば、キャッシュされたトークンやインメモリカウンタ、ミュータブル変数などは、warm start で前回の呼び出しで生成された状態を保持するため、リクエストごとの状態を保つ必要があるとされている。

一方で、記事 3 では、SnapStart が有効になっていても、warm start では init フェーズの処理がまだ残っていることが指摘されており、その結果として、warm start では初期化処理がまだ行われていない場合がある。このため、warm start では、init フェーズで行われる処理が、リクエストハンドラの処理に含まれている可能性がある。この点は、他の記事では明示されていないため、断定することはできない。

また、記事 5 では、warm start では、リクエストハンドラの処理が前回の呼び出しで生成された状態を保持している可能性があることが示されている。これは、warm start では、リクエストハンドラの処理が前回の呼び出しで生成された状態を保持しているため、リクエストごとの状態を保つ必要があるとされている。この点は、他の記事では明示されていないため、断定することはできない。

これらの記事では、warm start において、リクエストハンドラの処理が前回の呼び出しで生成された状態を保持している可能性があることが指摘されているが、具体的な原因や解決策については、明示されていない。そのため、これらの点は、断定するには十分な根拠が不足している。

## 元記事一覧

- [TheLambdaBugThatOnlyShowsUponWarmStarts](https://dev.to/aws-builders/the-lambda-bug-that-only-shows-up-on-warm-starts-2in)
- [A Subtle AWSLambdaBugCaused by “Stateless” Assumptions](https://www.linkedin.com/pulse/subtle-aws-lambda-bug-caused-stateless-assumptions-ashutosh-mehta-nutte)
- [WeCutLambdaColdStarts56% —ThreeWrongTurnsBeforethe...](https://dev.to/cloudwiseteam/we-cut-lambda-cold-starts-56-three-wrong-turns-before-the-real-snapstart-fix-1bd1)
- [AWSLambdaColdStarts: Impact and How to Reduce Them](https://edgedelta.com/company/knowledge-center/aws-lambda-cold-start-cost)
- [The Lambda Latency Trap: Why Your “12ms” Go API Can Suddenly ...](https://dev.to/harsh_8ee3e7db8b88fa3b447/the-lambda-latency-trap-why-your-12ms-go-api-can-suddenly-take-800ms-jhn)
