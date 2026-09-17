---
title: AIエージェントの承認プロセスにおける記録保持の課題
type: knowledge
status: draft
created: 2026-09-17
updated: 2026-09-17
confidence: medium
---

# AIエージェントの承認プロセスにおける記録保持の課題

## 結論

AIアーキテクチャにおいて、承認プロセスの透明性と人間の判断の記録保持は、特に規制業界では必須の課題である。現状では、AIエージェントが提案を出し、レビュワーが修正して承認しても、その変更内容や判断理由が記録されないことが多く、後続の監査や責任追及が困難である。このような問題に対応するため、CHAPプロトコルなどの新しいアプローチが提案されており、承認プロセスの可視化と記録保持の重要性が強調されている。

## テーマ概要

AIアーキテクチャにおける承認プロセスの透明性と記録保持が注目されている。特に、AIエージェントが承認を求める際、その回答がどこに保存されているのかという疑問が生じている。これは、AIエージェントが業務プロセスに組み込まれるにつれて、人間の判断を正確に記録し、追跡可能な形で残す必要性が高まっているためである。例えば、返金承認のような業務では、エージェントが提案を出し、レビュワーが修正し承認したが、その修正内容や判断理由が記録されていないケースが問題視されている。このような状況では、後で承認の痕跡を確認できず、監査や責任追及が困難になる。このため、CHAPプロトコルなどの新しいアプローチが提案されており、AIエージェントの承認プロセスにおける透明性と記録保持の重要性が強調されている。

## 共通して確認できる点

複数の記事で共通して確認できた事実として、AIアジェントが承認プロセスにおいて人間の判断を記録・追跡できていないという問題が指摘されている。具体的には、アジェントが提案を作成し、レビュー者がその内容を変更して承認した場合、変更内容や承認理由が記録されず、後からその決定の根拠を確認することが困難である。例えば、返金処理の例では、アジェントが作成した案と、レビュー者が変更した最終的な金額や理由が分離され、その違いが記録されていない。このような状態は、監査や責任追及において重大な課題となる。また、Microsoft EntraにおけるAIアジェントのアクセス制御に関しても、承認フローの可視化や権限の明確化が求められており、従来の二択式の承認モデルではスケーラビリティが確保できないことが指摘されている。

## 記事ごとの差分・視点の違い

記事「Your agent asked for approval. Where did the answer go?」は、AIエージェントのワークフローにおける人間の判断の記録と透明性の欠如に焦点を当てている。エージェントが処理を進め、レビュー者が修正を加えて承認する過程で、最終的な決定や変更の理由が記録されないという問題を指摘。このような情報の欠如は、規制業界においては証拠としての価値を持たず、監査や再現性が困難になるという実務上の課題を強調している。また、既存のプロトコル（MCPやA2A）がガバナンス機能をサポートしていないこと、代替としてCHAPプロトコルが提案されている点も説明している。

一方、記事「How long do agents take to read full manuscripts? (& why silence isn’t always bad news)」は、文学エージェントが原稿を読む際の時間が長くなる理由を解説しており、その遅れが必ずしも否定的な意味を持つわけではないことを示している。エージェントが慎重に評価し、フィードバックを準備している可能性があり、そのような遅れは評価の深さを示す兆候であると説明している。

記事「Flexibility with admin consent in Entra: how to scale consent flows for AI agents」は、Microsoft Entraにおける管理者承認の柔軟性とスケーラビリティについて論じている。従来の二択的な承認モデルではなく、アプリケーション承認ポリシーをカスタムディレクトリロールにバインドし、承認権限を限定的に委譲する方法を提案。これにより、AIエージェントが増える中での承認管理の課題を解決するためのアプローチを提示している。

記事「Microsoft Entra: AI Agent Access Guide」は、Microsoft EntraにおけるAIエージェントのアクセス制御と権限管理について解説しており、エージェントIDモデルが導入され、セキュリティと監査可能なアクセスが可能になった点を強調。実際の権限の付与はRRA（Required Resource Access）の信号ではなく、採用時や動的リクエスト時に発生するという仕組みを説明している。

記事「Microsoft 365 Agents SDK vs. Bot Framework: Rebuilding the Same Bot as an Agent」は、Microsoft 365のエージェントSDKとBot Frameworkの違いをコードレベルで比較し、エージェントとしての実装における論理の再構築とツール駆動型の計画への移行を強調。この記事は技術的実装の観点から、エージェントの設計と運用における変化を示している。

## 深掘り調査で得られた知見

AIアーキテクチャにおける承認プロセスの透明性欠如が問題視されている。あるケースでは、AIエージェントが返金承認の決定を草案として作成し、レビュワーが金額を変更しコメントを追加して承認したにもかかわらず、最終的な承認履歴は記録されていない。これは、AIエージェントのワークフローで人間の判断を追跡・記録する仕組みが欠如しているためである。この問題は、特に規制業界では深刻で、クライアントが後から承認の証拠を提示を求められることがある。例えば、あるエージェントが返金処理を完了した後、6か月後に誰が承認したのか、金額変更の理由が分からないという状況が実際に発生している。

このような課題に対応するため、CHAPプロトコルが提案されている。CHAPは、人間の判断を記録し、追跡可能な仕組みを提供する。これにより、承認プロセスの透明性が確保され、後続の検証や監査が可能となる。また、Microsoft EntraにおけるAIエージェントのアクセス管理では、Required Resource Access（RRA）が承認の信号として機能し、実際の権限付与はエージェントの採用または動的リクエスト時に発生する。これにより、権限の管理がより柔軟かつスケーラブルとなる。さらに、Authorization Fabricなどのランタイム認可フレームワークは、ビジネスポリシーやコンプライアンスを遵守しながら、承認閾値を実行するための決定をサポートしている。これらの取り組みは、AIエージェントの透明性とセキュリティを高めるために重要である。

## 不確実な点・追加確認が必要な点

記事間では、AIアーキテクチャにおける承認プロセスの透明性に関する認識の違いが見られる。記事1では、AIエージェントが承認を求める際、その結果が記録されない状況が具体的に描かれており、人間の判断が記録されないことが問題視されている。一方で、記事4では、Microsoft EntraにおけるAIエージェントのアクセス制御について説明されており、RRA（Required Resource Access）が承認の信号であり、実際の権限付与はエージェントの採用や動的リクエスト時に発生するという仕組みが述べられている。このように、記事1は承認プロセスの記録不足に焦点を当てているのに対し、記事4は権限の流れそのものに注目している。また、記事3では、AIエージェントが承認リクエストを評価し、組織ポリシーと比較して承認を推奨できるかを判断する仕組みが提案されているが、現状ではエージェントが承認決定を担うことはできないとされている。これらの記事は、AIエージェントの承認プロセスにおける課題とその解決策について異なる視点から述べており、具体的な実装や制限についての情報が分離している。そのため、これらの内容を統合的に理解するには、さらに詳細な情報や実際の実装例が必要である。

## 元記事一覧

- [Your agent asked for approval. Where did the answer go? - DEV Community](https://dev.to/arsalan_shahid116/your-agent-asked-for-approval-where-did-the-answer-go-47m8)
- [How long do agents take to read full manuscripts? (& why silence isn’t always bad news) - Book Mama](https://bookmama.com/blog/how-long-do-agents-take-to-read-full-manuscripts-why-silence-isnt-always-bad-news/)
- [Flexibility with admin consent in Entra: how to scale consent flows for AI agents - DEV Community](https://dev.to/astaykov/flexibility-with-admin-consent-in-entra-how-to-scale-consent-flows-for-ai-agents-2h1p)
- [Microsoft Entra: AI Agent Access Guide](https://www.hubsite365.com/en-ww/crm-pages/how-ai-agent-identity-permissions-work-in-microsoft-entra-full-walkthrough.htm)
- [Microsoft 365 Agents SDK vs. Bot Framework: Rebuilding the Same Bot as an Agent - DEV Community](https://dev.to/avinash247/microsoft-365-agents-sdk-vs-bot-framework-rebuilding-the-same-bot-as-an-agent-2f8)
