---
title: LM Studio 0.3.17 での MCP サーバー利用
type: knowledge
status: draft
created: 2026-10-25
updated: 2026-10-25
confidence: medium
---

# LM Studio 0.3.17 での MCP サーバー利用

## 何が分かったか

LM Studio 0.3.17 からは MCP ホストとして動作し、MCP サーバーをアプリに接続してモデルに利用可能にできます[^fact-10f5482f9287ac7d]。信頼できないソースからの MCP サーバーインストールは避けてください[^fact-60aa3f4a7310b90c]。ローカルおよびリモートの MCP サーバーをサポートしており、mcp.json ファイルの編集やアプリ内から追加できます[^fact-69058978948d21f6]。

## 確認できた事実

- LM Studio 0.3.17 から、LM Studio は Model Context Protocol (MCP) ホストとして動作します。これは、MCP サーバーをアプリに接続し、モデルに利用可能にすることができます。 [^fact-10f5482f9287ac7d]

- 信頼できないソースからの MCP サーバーはインストールしないでください。一部の MCP は、あなたのシステムに対して広範なアクセスを持つことがあります。 [^fact-60aa3f4a7310b90c]

- 0.3.17 (b10) から、LM Studio はローカルおよびリモートの MCP サーバーの両方をサポートします。MCP を追加するには、アプリの mcp.json ファイルを編集するか、または [^fact-69058978948d21f6]

## それが意味すること

MCP サーバーの利用は、モデルの機能拡張に役立つ可能性がありますが、システムへのアクセス権限の拡大を伴うため注意が必要です。

## まだ分からないこと

MCP サーバーの具体的な動作や影響範囲について、提供された情報では明示されていません。

## 出典

[^fact-10f5482f9287ac7d]: [UseMCPServers | LMStudio](https://lmstudio.ai/docs/app/mcp)
  - 根拠引用: 「Starting LM Studio 0.3.17, LM Studio acts as an Model Context Protocol (MCP) Host . This means you can connect MCP servers to the app and make them available to your models.」
[^fact-60aa3f4a7310b90c]: [UseMCPServers | LMStudio](https://lmstudio.ai/docs/app/mcp)
  - 根拠引用: 「Never install MCP servers from untrusted sources. Some MCPs can have far reaching access to your system.」
[^fact-69058978948d21f6]: [UseMCPServers | LMStudio](https://lmstudio.ai/docs/app/mcp)
  - 根拠引用: 「Starting 0.3.17 (b10), LM Studio supports both local and remote MCP servers. You can add MCPs by editing the app's mcp.json file or via the」
