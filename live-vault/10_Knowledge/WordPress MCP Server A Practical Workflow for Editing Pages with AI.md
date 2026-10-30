---
title: WordPress MCPサーバーでAIによるページ編集の実践フロー
type: knowledge
status: draft
created: 2026-10-30
updated: 2026-10-30
confidence: medium
---

# WordPress MCPサーバーでAIによるページ編集の実践フロー

## 何が分かったか

WordPress MCPサーバーは、ターミナルからWordPressを操作可能にし、AIエージェントと連携して状態を読み込み、WP-CLIやPHPを実行し、ブラウザを使わずにコンテンツを編集できます[^fact-119d66d3f12ca805]。MCPアダプターは、WordPressのAbilities APIで登録した能力をMCPクライアントが利用できる形式にします[^fact-436c605e3059b152]。利用可能な動詞を確認し、破壊的な操作を行う前にバックアップを取ることが重要です[^fact-d1aac38c3f642455]。

## 確認できた事実

- ターミナルからモデルコンテキストプロトコルを通じてWordPressを操作するための実用ガイド: 状態の読み込み、GutenbergとElementorの編集、WP-CLIとPHPの実行、そしてスキップするとページが壊れる可能性があるポイントについて。 [^fact-a2d1e1ab46a1c51f]

- MCPはインターフェースを変更します。これはWordPress MCPが行うことです: MCPサーバープラグインはWordPressを呼び出せるツールのセットとして公開するため、AIエージェント（またはターミナルから直接操作）をWordPressに接続して状態を読み込み、WP-CLIを実行、PHPを実行し、ブラウザを使わずにコンテンツを編集できます。 [^fact-119d66d3f12ca805]

- スモークテスト: 401は資格情報が不正、404はMCPプラグインがアクティブになっていないことを意味し、接続タイムアウトは通常CDNやホストがリクエストをブロックしていることを意味します。 [^fact-f3201bd5683d0aa0]

- 利用可能な動詞を発見する: 呼び出す前に能力のスキーマを調べます。ここでは破壊的なフラグを読み取って、最初にバックアップするかどうかを判断します: [^fact-d1aac38c3f642455]

- 実行する: 出力は標準出力で純粋なJSONなので、応答を保存してください: [^fact-fd900ad75bbefcbe]

- WordPress MCPアダプターはClaude CodeやCursorなどのAIツールがWordPressサイト上で動作するアクションを検出・実行できます。これはAbilities APIで登録した能力をModel Context Protocol（MCP）を通して共有します。 [^fact-0d6baac54d6ac85b]

- MCPはAIアプリが外部ツールやデータに接続するための共有された方法を提供するオープンスタンダードです。MCPサーバーは提供するツールをリストします。MCPクライアント（Claude CodeやCursorなど）はそのリストを読み取り、それを呼び出すことができます。 [^fact-436c605e3059b152]

- WordPressはすでに自身のアクションを記述する方法を持っています。それはAbilities APIと呼ばれます。私は最初のAbilities API統合投稿でこれを説明しました。各能力には名前、入力スキーマ、出力スキーマ、権限チェック、コールバックがあります。MCPアダプターはこれらの能力をMCPクライアントが読み取れる形式にします。 [^fact-47ade490feaea89c]

- WordPress MCPアダプターはあなたのサイトとAIツール（Claude CodeやCursorなど）の間に位置しています。 [^fact-1ef91d9c0359cc39]

- アダプターはまだコアに含まれていませんので、自分で追加する必要があります。プラグインとしてインストールできますが、自分のプラグイン内でComposerパッケージとしてバンドルすることもできます。最初のテストでは、プラグインを選びましょう。それはより簡単です。 [^fact-f4493f5f2cb559da]

- 注意: アダプターはまだバージョン1.0未満なので、名前やコマンドはリリースごとに変更される可能性があります。以下をコピーする前に、インストールしたバージョンのREADMEを読みます。 [^fact-d9defc65052e65de]

- 能力を登録しても、AIツールに共有されるわけではありません。自分で「mcp」=> array( 'public' => true )を能力のメタ配列内に追加して、オプトインする必要があります。 [^fact-62c044a7a7e57e79]

- ここに小さな例があります。これはデータのみを読み込むものです。サイト名とタグラインを返しますし、投稿を編集できるユーザーのみが実行できます。 [^fact-9cf9c16fc9415177]

- 読み取り専用アノテーションは、この能力が何もないことをクライアントに伝えます。権限チェック関数はすべての呼び出しで実行され、リクエストがAIツールから来た場合も例外ではありません。 [^fact-ce7e6ce34d190cc3]

## それが意味すること

MCPはAIツールとWordPressを接続するためのオープンスタンダードであり、AIエージェントがWordPressの機能を操作できるようにします[^fact-436c605e3059b152]。アダプターはWordPressとAIツールの間に位置し、能力を共有します[^fact-1ef91d9c0359cc39]。 [^fact-436c605e3059b152] [^fact-1ef91d9c0359cc39]

## まだ分からないこと

MCPアダプターはまだバージョン1.0未満であり、名前やコマンドがリリースごとに変更される可能性があります[^fact-d9defc65052e65de]。アダプターのインストール方法や設定手順、トラブルシューティング情報は提供されていません[^fact-f4493f5f2cb559da]。

## 出典

[^fact-a2d1e1ab46a1c51f]: [DrivingWordPressHeadlessly withMCP: HowAIAgents Operate...](https://asyncdot.com/blog/headless-wordpress-mcp/)
  - 根拠引用: 「A practical guide to operating WordPress from the terminal through the Model Context Protocol: reading state, editing Gutenberg and Elementor, running WP-CLI and PHP, and the gotchas that break pages if you skip them.」
[^fact-119d66d3f12ca805]: [DrivingWordPressHeadlessly withMCP: HowAIAgents Operate...](https://asyncdot.com/blog/headless-wordpress-mcp/)
  - 根拠引用: 「MCP changes the interface. This is what WordPress MCP does: an MCP server plugin exposes WordPress as a set of callable tools, so you can connect an AI agent to WordPress (or drive it yourself from a terminal) to read state, run WP-CLI, execute PHP, and edit content without touching the browser.」
[^fact-f3201bd5683d0aa0]: [DrivingWordPressHeadlessly withMCP: HowAIAgents Operate...](https://asyncdot.com/blog/headless-wordpress-mcp/)
  - 根拠引用: 「Smoke test: A 401 means bad credentials, a 404 means the MCP plugin is not active, and a connect timeout usually means a CDN or host is blocking the request.」
[^fact-d1aac38c3f642455]: [DrivingWordPressHeadlessly withMCP: HowAIAgents Operate...](https://asyncdot.com/blog/headless-wordpress-mcp/)
  - 根拠引用: 「Discover the available verbs: Inspect an ability’s schema before you call it. This is where you read the destructive flag that tells you whether to back up first:」
[^fact-fd900ad75bbefcbe]: [DrivingWordPressHeadlessly withMCP: HowAIAgents Operate...](https://asyncdot.com/blog/headless-wordpress-mcp/)
  - 根拠引用: 「Execute it: Save the response, since output is plain JSON on stdout:」
[^fact-0d6baac54d6ac85b]: [WordPressMCPAdapter: ConnectClaudeCodeandCursorto Your...](https://dev.to/matthummeldev/wordpress-mcp-adapter-connect-claude-code-and-cursor-to-your-site-3kee)
  - 根拠引用: 「The WordPress MCP Adapter lets AI tools like Claude Code and Cursor find and run actions on your WordPress site. It takes the abilities you register with the Abilities API and shares them over the Model Context Protocol (MCP).」
[^fact-436c605e3059b152]: [WordPressMCPAdapter: ConnectClaudeCodeandCursorto Your...](https://dev.to/matthummeldev/wordpress-mcp-adapter-connect-claude-code-and-cursor-to-your-site-3kee)
  - 根拠引用: 「MCP is an open standard that gives AI apps a shared way to connect to outside tools and data. An MCP server lists the tools it offers. An MCP client, like Claude Code or Cursor, reads that list and can call those tools when you ask it to.」
[^fact-47ade490feaea89c]: [WordPressMCPAdapter: ConnectClaudeCodeandCursorto Your...](https://dev.to/matthummeldev/wordpress-mcp-adapter-connect-claude-code-and-cursor-to-your-site-3kee)
  - 根拠引用: 「WordPress already has its own way to describe actions, called the Abilities API. I covered it in my first Abilities API integration post. Each ability has a name, an input schema, an output schema, a permission check, and a callback. The MCP Adapter takes those abilities and puts them in a form an MCP client can read.」
[^fact-1ef91d9c0359cc39]: [WordPressMCPAdapter: ConnectClaudeCodeandCursorto Your...](https://dev.to/matthummeldev/wordpress-mcp-adapter-connect-claude-code-and-cursor-to-your-site-3kee)
  - 根拠引用: 「The WordPress MCP Adapter sits between your site and AI tools like Claude Code and Cursor.」
[^fact-f4493f5f2cb559da]: [WordPressMCPAdapter: ConnectClaudeCodeandCursorto Your...](https://dev.to/matthummeldev/wordpress-mcp-adapter-connect-claude-code-and-cursor-to-your-site-3kee)
  - 根拠引用: 「The adapter isn’t in core yet, so you add it yourself. You can install it as a plugin, or bundle it inside your own plugin as a Composer package. For a first test, I’d go with the plugin because it’s simpler.」
[^fact-d9defc65052e65de]: [WordPressMCPAdapter: ConnectClaudeCodeandCursorto Your...](https://dev.to/matthummeldev/wordpress-mcp-adapter-connect-claude-code-and-cursor-to-your-site-3kee)
  - 根拠引用: 「Heads up: the adapter is still under version 1.0, so names and commands may change from one release to the next. Before you copy anything below, read the README for the version you installed.」
[^fact-62c044a7a7e57e79]: [WordPressMCPAdapter: ConnectClaudeCodeandCursorto Your...](https://dev.to/matthummeldev/wordpress-mcp-adapter-connect-claude-code-and-cursor-to-your-site-3kee)
  - 根拠引用: 「Registering an ability won’t share it with AI tools by itself. You have to opt in by adding 'mcp' => array( 'public' => true ) inside the ability’s meta array.」
[^fact-9cf9c16fc9415177]: [WordPressMCPAdapter: ConnectClaudeCodeandCursorto Your...](https://dev.to/matthummeldev/wordpress-mcp-adapter-connect-claude-code-and-cursor-to-your-site-3kee)
  - 根拠引用: 「Here’s a small example that only reads data. It returns the site name and tagline, and it only runs for users who can edit posts.」
[^fact-ce7e6ce34d190cc3]: [WordPressMCPAdapter: ConnectClaudeCodeandCursorto Your...](https://dev.to/matthummeldev/wordpress-mcp-adapter-connect-claude-code-and-cursor-to-your-site-3kee)
  - 根拠引用: 「The readonly annotation tells clients this ability doesn’t change anything. The permission callback runs on every call, even when the request comes from an AI tool.」
