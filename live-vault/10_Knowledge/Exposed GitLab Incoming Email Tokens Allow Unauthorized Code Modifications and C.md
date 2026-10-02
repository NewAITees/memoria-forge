---
title: GitLab Incoming Emailトークン漏洩によるコード変更リスク
type: knowledge
status: draft
created: 2026-10-02
updated: 2026-10-02
confidence: medium
---

# GitLab Incoming Emailトークン漏洩によるコード変更リスク

## 結論

GitLabのincoming emailトークンの漏洩により、不正な第三者がユーザーの権限でコードを変更し、CI/CDパイプラインを実行できるという重大なセキュリティリスクが確認されている。このトークンは永続的であり、明示的な期限が設定されていないため、不正利用の可能性が高く、ネットワークのIP制限を回避する手段としての脅威となる。また、GitHub Actionsにおいても同様のサプライチェーン攻撃が再発生し、15,000以上のリポジトリが影響を受けた可能性があることから、トークンやアドレスの管理、監視体制の強化が急務である。

## テーマ概要

GitLabのincoming emailトークンの漏洩が、不正なコードの変更やCI/CDパイプラインの実行を許可する脆弱性として注目されている。このトークンは、GitLabが提供する特定のメールアドレスに埋め込まれており、そのトークンを取得することで、ユーザーの権限で操作が可能になる。このメールアドレスの形式は「glimt-」で始まり、プロジェクトごとに異なる部分を持つが、トークン部分はユーザーごとに一意であり、複数のプロジェクトにわたって共通している。不正なメールアドレスを用いてmerge request宛のメールを送信することで、コードの変更とCI/CDパイプラインの実行が可能となり、この操作はユーザーの権限に基づいて行われる。この問題は、GitLabのメールアドレス機能の設計に起因し、トークンが永続的であり、明示的な期限が設定されていない点が原因として挙げられている。また、この問題はネットワークのIP制限を回避し、セキュリティ上非常に重大なリスクを引き起こす可能性がある。

## 共通して確認できる点

GitLabのincoming emailアドレスに埋め込まれたトークンが漏洩すると、不正な第三者がコードを変更し、CI/CDパイプラインを実行できるという問題が複数の記事で確認されている。このトークンは、GitLabが提供する特定のメールアドレスに含まれており、ユーザーの権限で操作が可能になる。メールアドレスの形式は「glimt-」で始まり、プロジェクトごとに異なる部分を持つが、トークン部分はユーザーごとに一意であり、複数のプロジェクトにわたって共通している。不正なメールアドレスを用いてmerge request宛のメールを送信することで、コードの変更とCI/CDパイプラインの実行が可能となり、この操作はユーザーの権限に基づいて行われる。また、このトークンは永続的であり、明示的な期限が設定されていないため、リスクが高まっている。GitLabは、セキュリティ研究者による報告後、インターフェースとドキュメンテーションを更新し、リスクと機能の説明を明確化したが、根本的なメール機能は停止されていない。この問題は、ネットワークのIP制限を回避し、セキュリティ上非常に重大なリスクを引き起こす可能性がある。不正なメールアドレスが存在する場合、組織はその影響範囲を特定し、メールを介したコード変更やCI/CD実行を監視・検出する必要がある。

## 記事ごとの差分・視点の違い

記事「Exposed GitLab Incoming Email Tokens Allow Unauthorized Code Modifications and CI Execution」は、GitLabのincoming emailトークンの漏洩がもたらすセキュリティリスクに焦点を当てており、特に不正なメールアドレスを用いてコード変更やCI/CDパイプラインの実行が可能になる点を強調している。この記事では、トークンの永続性と明示的な期限のない設計が原因として挙げられ、組織がトークンの管理と監視を徹底する必要があると述べている。

記事「GitLab Email Token Vulnerability: A Silent Security Threat」は、トークンの設計がユーザーの権限を越えて広範なアクセスを許可する可能性があることを指摘。具体的には、トークンがプロジェクト間で共通しており、単一プロジェクトに限定されない点を強調。また、メールアドレスの形式とトークンの構造について詳しく説明し、攻撃者がメールを介して直接コードを変更できる仕組みを解説している。

記事「MiniShai-HuludRe-Exposure:Re-EnabledGitHubAction...」は、GitHub Actionsの再起動による悪用リスクを主な論点としており、Mini Shai-Hulud攻撃の再現とその影響範囲を提示。特に、タグベースの参照が悪用され、不正なコードが再び実行される可能性を指摘し、開発者にタグの固定化やシークレットの回転を推奨している。

記事「GitHub Actions re-enabled with Mini Shai-Hulud payload still active」は、具体的な時間軸を提示し、攻撃が再発生した日時や、GitHubが再びアクションを無効にした日時を明記。また、影響を受けたリポジトリの数や、悪用されたタグの状態について詳細を述べており、事例ベースの分析が特徴。この記事では、攻撃の再発生がなぜ起こったのか、その背景に焦点を当てている。

記事「SalesBleed: Zero-Click DNS Data Exfiltration from Agentforce...」は、別の攻撃手法であるSalesBleedを扱っており、AgentforceでのゼロクリックDNSデータ漏洩の仕組みを解説。この記事は、GitLabのトークン漏洩とは異なる攻撃手法を提示しており、セキュリティリスクの多様性を示している。

## 深掘り調査で得られた知見

深掘り調査により、GitLabのincoming emailトークンに関する脆弱性が複数のプラットフォームやプロジェクトに及ぼす影響が明らかになった。このトークンは、特定のメールアドレスに埋め込まれており、不正に取得されると、ユーザーの権限でコード変更やCI/CDパイプラインの実行が可能になる。この問題は、GitLabのメールアドレス機能の設計上、トークンが永続的であるため、明示的な期限が設定されていない点が原因とされている。また、ネットワークのIP制限を回避できるため、セキュリティ上非常に重大なリスクを引き起こす可能性がある。

同様の問題として、GitHub ActionsにおいてもMini Shai-Huludによるサプライチェーン攻撃が発覚し、攻撃者が不正にコードを挿入したアクションが再び有効化されるという事態が発生した。この攻撃では、15,000以上のリポジトリが影響を受けた可能性があり、CI/CDパイプラインから敏感な資産が漏洩する恐れがあった。また、GitHubの依存関係グラフでは、これらのアクションを参照しているリポジトリが多数確認されており、攻撃の影響範囲はさらに広がっている可能性がある。

これらの事例から、コード変更やCI/CDパイプラインの実行を制御するためのトークンやアドレスが、不正に取得されると重大なセキュリティリスクとなることが分かった。特に、トークンが永続的であり、明示的な期限が設定されていない場合、不正利用の可能性が高まる。そのため、企業はこうしたトークンやアドレスを管理し、漏洩時の影響範囲を特定・監視する仕組みを導入する必要がある。また、GitHub ActionsやCI/CD環境においては、アクションを特定のコミットSHAにピンするなどの安全な実装が求められている。

## 不確実な点・追加確認が必要な点

記事間の食い違いや、資料からは断定できない点を以下に示す。まず、GitLabのincoming emailトークンに関する問題については、記事1と記事2が同様の脆弱性を報告しているが、具体的な攻撃方法や影響範囲の詳細には違いがある。記事1では、メールアドレスに埋め込まれたトークンが公開されると、merge request宛のメールを送信することでコード変更やCI/CDパイプラインの実行が可能になるとしている。一方、記事2では、トークンが永続的であり、明示的な期限が設定されていない点が原因として挙げられており、IP制限を回避する手段としてのリスクが強調されている。ただし、記事2では具体的な攻撃例や検証結果が記載されていないため、現時点では断定的な情報は得られていない。

また、記事3と記事4はGitHub Actionsに関するもので、Mini Shai-Hulud攻撃の再発生を報告している。記事3では、15,000以上のリポジトリが影響を受けた可能性があるとされ、ただしこれは確認された侵害ではなく、依存関係の数であると明記されている。一方、記事4では、攻撃が再発生した日時（2026年9月16日から9月25日）や、GitHubが再びアクションを無効化した日（2026年9月25日）が明記されており、時系列的な情報が具体的に提供されている。ただし、記事3と記事4の情報は、どちらも2026年9月の情報であり、記事5（SalesBleed）は2026年9月24日に公開されているため、時間的な順序は明確だが、それぞれの脆弱性の関連性や相互の影響については資料からは断定できない。

## 元記事一覧

- [ExposedGitLabIncomingEmailTokensAllowUnauthorizedCode...](https://dev.to/anoymask/exposed-gitlab-incoming-email-tokens-allow-unauthorized-code-modifications-and-ci-execution-31i5)
- [GitLabEmailTokenVulnerability: A Silent Security Threat](https://meterpreter.org/gitlab-email-token-vulnerability/)
- [MiniShai-HuludRe-Exposure:Re-EnabledGitHubAction...](https://dev.to/anoymask/mini-shai-hulud-re-exposure-re-enabled-github-action-repositories-trigger-malicious-code-execution-5bop)
- [GitHubActionsre-enabledwithMiniShai-Huludpayload stillactive](https://www.bleepingcomputer.com/news/security/github-actions-re-enabled-with-mini-shai-hulud-payload-still-active/)
- [SalesBleed: Zero-Click DNS Data Exfiltration from Agentforce...](https://dev.to/anoymask/salesbleed-zero-click-chain-exfiltrating-data-via-dns-from-agentforce-via-indirect-prompt-injection-23d3)
