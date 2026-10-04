---
title: SSHをパスワード認証で使う方法とセキュリティ対策
type: knowledge
status: draft
created: 2026-10-04
updated: 2026-10-04
confidence: medium
---

# SSHをパスワード認証で使う方法とセキュリティ対策

## 結論

SSHクライアントをパスワード認証のみで使用するには、`-o PreferredAuthentications=password`オプションを指定する方法が一般的に推奨されているが、その効果は一貫していない可能性がある。一方で、AWS Systems Manager（SSM）を活用したEC2へのアクセス方法は、セキュリティを高め、ポート22の開放を避けることが可能であり、特にCI/CD環境での利用が注目されている。ただし、SSMの導入には特定のバージョンのSSM Agentが必要な場合があり、環境によっては追加の設定や注意点が生じる。

## テーマ概要

SSHをパスワード認証のみで使用する方法についての質問は、SSHの認証メカニズムにおける柔軟性やセキュリティ設定の変更を求める技術的なニーズから生まれています。このテーマは、特にSSH接続を管理する際のセキュリティと運用のバランスを考慮する上で注目されています。例えば、EC2インスタンスへのアクセスにおいて、ポート22を開けることなくSSH接続を実現する方法として、AWS Systems Manager（SSM）の利用が提案されています。これは、セキュリティリスクを低減し、長期的なSSHキーの管理を回避するための現代的なアプローチです。また、SSHの認証方法をパスワードに限定する必要性は、特定の環境下での制限や、セキュリティポリシーの遵守を求めるケースでも見られます。このような背景から、このテーマは現在、ネットワークセキュリティと運用効率の観点から注目されています。

## 共通して確認できる点

複数の記事で共通して確認できた事実としては、SSHクライアントをパスワード認証のみで接続させる方法として、`-o PreferredAuthentications=password`オプションが挙げられている。このオプションを指定することで、SSHクライアントがパスワード認証を優先的に使用するようになる。また、`PubkeyAuthentication=no`オプションは、クライアント側で公開鍵認証を無効にするが、`PreferredAuthentications=password`が設定されている場合、このオプションは必須ではない。ただし、サーバー側で公開鍵認証のみを許可している場合、クライアントがパスワード認証を試行しても接続が拒否される可能性がある。また、接続時の詳細な情報を確認するには、`-vv`オプションを使用したverboseモードが推奨されている。一部のソースでは、colon trick（コロントリック）が提案されているが、その効果は不確実である。

## 記事ごとの差分・視点の違い

記事「How do I force SSH to use password instead of key?」では、SSHクライアント側でパスワード認証を優先的に使用する方法が説明されており、-o PreferredAuthentications=passwordオプションの使用が推奨されている。一方、「How to force ssh client to use only password auth? - Unix ...」では、このオプションの信頼性が疑われており、代替案としてcolon trickが提案されているが、その効果は不確実であると指摘されている。また、「Stop Whitelisting Port 22: SSH into Private EC2 from GitHub ...」では、SSHではなくAWS Systems Manager（SSM）を用いたEC2へのアクセス方法が紹介されており、ポート22を開ける必要がなく、セキュリティを高めることができるという視点が強調されている。「Deploy to EC2 from GitHub Actions without opening port 22」では、SSMを活用したデプロイ方法が詳しく説明されており、セキュリティと管理性の向上が主なメリットとして挙げられている。最後に、「Error: Permission denied (publickey) - GitHub Docs」では、SSH接続時の認証エラーの原因と解決策が説明されており、パスワード認証の使用が推奨される場面が示されている。各記事は、SSHの認証方法に関する視点や対象環境に応じた解決策をそれぞれ強調している。

## 深掘り調査で得られた知見

SSHクライアントをパスワード認証に限定して使用する方法として、`-o PreferredAuthentications=password`オプションが推奨されています。このオプションはSSHクライアントがパスワード認証を優先的に試行するように指定します。また、`PubkeyAuthentication=no`オプションを設定することで、クライアントが公開鍵認証を試行しないようにできますが、`PreferredAuthentications=password`がすでに設定されているため、このオプションは必須ではありません。ただし、サーバー側で公開鍵認証のみを許可している場合、クライアントがパスワード認証を試行しても接続が拒否される可能性があります。接続時の詳細な情報を確認するには、`-vv`オプションを使用してverboseモードを有効にします。一部のソースでは、colon trick（コロントリック）が提案されていますが、その効果は不確実です。

一方、AWS Systems Manager (SSM) を使用することで、EC2インスタンスへのSSH接続をより安全かつ効率的に実現できます。SSM Agentがインスタンス上で動作し、AWSへの外出先HTTPS接続を確立します。この接続を介して、セッションがブロケットされ、SSH接続が実現されます。これにより、ポート22の開放やパブリックIPの使用を必要としなくなり、セキュリティリスクが軽減されます。EC2 Instance Connectを使用することで、一時的なSSHキーをインスタンスにプッシュし、60秒の有効期限で使用することができ、長期的なキー管理の必要性が解消されます。GitHub Actionsでの利用例として、`ankurk91/setup-ssh-over-ssm-action`というアクションが提供されており、SSH設定のセットアップとクリーンアップを自動化しています。このアクションは、一時的なSSHキーを生成し、EC2 Instance Connectを介してインスタンスにプッシュし、`.ssh/config`ファイルに`ProxyCommand`を設定して接続を実現します。ジョブ終了後には、SSH設定を削除し、キーを削除し、セッションを終了します。これにより、セキュリティ、監査性、コンプライアンス面でより良い結果が得られます。

SSH接続時の「Permission denied (publickey)」エラーは、サーバーが公開鍵認証を拒否している場合に発生します。このエラーはネットワーク関連の問題（例：接続拒否、タイムアウト）とは異なり、認証ステップでの失敗を示します。サーバーは、authorized_keysファイルの存在と権限、一致する公開鍵の有無、正しい秘密鍵のペアリングなどを確認します。このエラーの主な原因として、authorized_keysファイルの権限が不適切、authorized_keysファイルが存在しない、または鍵が不一致であることが挙げられます。解決策としては、サーバー側のauthorized_keysファイルの権限を確認し、正しい鍵を使用しているかを確認し、SSH設定を確認することが重要です。SSHコマンドのverboseモード（`-vvv`）は、エラーの詳細な原因を特定するのに役立ちます。一部のソースでは、一時的にパスワード認証を使用する方法が提案されていますが、セキュリティ上の懸念から推奨されていません。具体的な解決策は、設定や環境に応じて異なります。

## 不確実な点・追加確認が必要な点

記事間では、SSHをパスワード認証のみで使用する方法に関する情報がいくつか異なっている。例えば、記事1と記事2では、`-o PreferredAuthentications=password`オプションを用いることでSSHクライアントがパスワード認証を優先的に使用するよう指定できることが示されているが、その効果は一貫して確認されていない。記事2では、このオプションが一時的な解決策として提案されており、一貫した動作を保証するものではないとされている。

一方で、記事3と記事4では、EC2インスタンスへのSSH接続に公開鍵認証を用いる代わりに、AWS Systems Manager (SSM)を活用した方法が提案されている。このアプローチでは、SSH接続を経由せず、SSM Agentを通じてHTTPS経由で接続することができ、ポート22を開ける必要がなくなる。この方法はセキュリティ面でより優れているとされているが、一部のソースではEC2 Instance Connectの使用が必須であるとし、他のソースではその必要性が疑問視されている。また、SSM Agentのバージョンに関する情報も不一致があり、最小バージョンが明示されているものとそうでないものがある。

さらに、記事5では、SSH接続時に「Permission denied (publickey)」エラーが発生する原因とその解決策が説明されているが、このエラーは認証の失敗を示すものであり、パスワード認証を強制する必要性とは別物である。記事5では、一時的にパスワード認証を試す方法が提案されているが、セキュリティ上のリスクがあるため、推奨されていない。そのため、記事間で示される解決策は、状況や環境によって異なる可能性がある。

## 元記事一覧

- [How do I force SSH to use password instead of key?](https://superuser.com/questions/1376201/how-do-i-force-ssh-to-use-password-instead-of-key)
- [How to force ssh client to use only password auth? - Unix ...](https://unix.stackexchange.com/questions/15138/how-to-force-ssh-client-to-use-only-password-auth)
- [Stop Whitelisting Port 22: SSH into Private EC2 from GitHub ...](https://dev.to/ankurk91/stop-whitelisting-port-22-ssh-into-private-ec2-from-github-actions-via-aws-ssm-cj4)
- [Deploy to EC2 from GitHub Actions without opening port 22](https://dev.to/ankurk91/deploy-to-ec2-from-github-actions-without-opening-port-22-5269)
- [Error:Permissiondenied(publickey) - GitHub Docs](https://docs.github.com/en/authentication/troubleshooting-ssh/error-permission-denied-publickey)
