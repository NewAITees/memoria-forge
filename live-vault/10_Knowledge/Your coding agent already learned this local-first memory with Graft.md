---
title: ローカルファーストでコード知識を記憶するGraftの仕組み
type: knowledge
status: draft
created: 2026-09-17
updated: 2026-09-17
confidence: medium
---

# ローカルファーストでコード知識を記憶するGraftの仕組み

## 結論

Graftは、コードベースの知識をローカルで永続的に保持し、AIコードアシスタントが過去の学習やプロジェクト知識を再利用できるようにする技術として、明確に位置づけられている。tree-sitterを用いたコード解析とシンボルの接続グラフ生成により、エージェントが効率的に情報を取得できる仕組みを提供し、SaaSやAPIキーに依存せずプライバシーを確保しながら機能する。この設計は、コードアーキテクトが実際の問題解決中に得た知識を長期的に保持し、再発見のコストを削減するための重要なソリューションである。

## テーマ概要

Graftは、コードベースの知識を永続的に保持し、コーディングアーキテクトが過去の学習やプロジェクト知識を再利用できるようにするローカルファーストのメモリソリューションです。この技術は、AIによるコーディングアシスタントが複数のセッションで同じ問題に直面した際に、過去の経験を活用して効率的に解決できるようにします。特に、プロジェクト固有の知識や修正点を再発見せずに利用できるため、リソースの無駄を減らし、作業時間を短縮します。Graftは、Claude Code、Codex、ChatGPTなどのコード生成ツールと連携し、ローカルでの実行とSQLiteベースのデータストレージを採用することで、SaaSやAPIキーに依存せず、プライバシーを保ちながら機能します。この技術が注目されている理由は、AIアシスタントが単なるツールではなく、実際の問題解決に貢献するパートナーとしての役割を果たすための、記憶保持機能の必要性が高まっているからです。

## 共通して確認できる点

複数の記事から共通して確認できた事実として、Graftはコードベースのマッピングを実現するためのツールであり、AIコードアーキテクトがプロジェクトの構造やシンボルの定義を理解するためのローカルなメモリを提供します。このツールは、各セッションで学んだ知識を保持し、後続のセッションで再利用できるようにすることで、再発見のコストを削減します。Graftはtree-sitterを使用してコードを解析し、シンボルの Wiring グラフを生成し、MCP（Model Context Protocol）を介して検索ツールを提供します。また、SaaSやAPIキーに依存せず、ローカルで動作する設計となっています。この仕組みにより、コードアーキテクトが過去の学習を活用して、効率的に問題を解決できるようになります。

## 記事ごとの差分・視点の違い

記事ごとの立場や強調点、論点の違いは以下の通りです。

記事1では、Graftがコードエージェントにローカルファーストの永続的なメモリを提供することを主に説明しています。GraftはSaaSやAPIキーに依存せず、SQLiteとsqlite-vecを用いて効率的な検索が可能で、コードベースの知識を保持してエージェントが再利用できるようにします。また、Graftはエージェントの推論を置き換えるものではなく、過去の学習をもとに判断を支援するツールとして位置づけられています。

記事2は、Graftがコードベースのマップとして機能し、エージェントが毎回新しいセッションでコードを探索する必要がないようにする点を強調しています。tree-sitterを用いてコードを解析し、シンボルの定義や呼び出し関係を記録することで、エージェントが効率的に情報を取得できるようにします。また、このアプローチはSaaSやゲートウェイではなく、ローカルのディスク上のマップとして実装されている点が特徴です。

記事3では、BlazorMemoryという別のプロジェクトが紹介されており、Blazorアプリケーション内でAIチャットアシスタントがローカルでの記憶を維持できるようにする点が主な焦点です。BlazorMemoryはIndexedDB、EF Core、pgvector、InMemoryなどのストレージバックエンドをサポートし、Ollamaとの組み合わせが特に推奨されています。また、開発中にストレージインターフェースが変更されるなど、設計上の課題も述べられています。

記事4はInstagramアプリのダウンロードに関する情報であり、Graftや他の技術とは直接関係がありません。この記事は、テーマとは異なるため、無視されます。

記事5では、DeepSeek Harnessがすべての機能をプラグインとして扱い、Cordis拡張の選択肢を提供している点が強調されています。プラグインとしてのアーキテクチャは、モデルアダプター、ツールレジストリ、セッションログ、エージェントループなど、さまざまなコンポーネントを含み、拡張性の高い設計となっています。ただし、Graftとの直接的な関連性は確認されていません。

## 深掘り調査で得られた知見

Graftは、コードベースの知識をローカルで永続的に保存し、AIコードアーキテクトが過去の学習成果を再利用できるようにするツールとして注目されている。このツールは、Claude Code、Codex、ChatGPTなど複数のコード生成モデルと連携しており、モデルのセッション間での記憶喪失を補う役割を果たす。Graftは、コードの構造をtree-sitterで解析し、マークダウンノードとシンボルの接続グラフを生成することで、コードベースのマッピングを実現している。このマッピングにより、コードの探索作業が効率化され、モデルが同じ問題に直面した際には、過去の学習成果をすぐに参照できるようになる。

また、GraftはSaaSやAPIキーに依存せず、ローカルで動作するため、セキュリティやプライバシーの観点からも優れている。SQLiteとsqlite-vecを使用したデータベース設計により、高速な検索が可能であり、特にプロジェクト固有の知識や課題の再発見を避けることに特化している。これは、大規模なドキュメントインデックス化には向かないが、コードアーキテクトが実際の問題解決中に得た知識を長期的に保持するには最適な設計である。

一方で、BlazorMemoryという別のプロジェクトは、Blazorアプリケーション内でAIチャットアシスタントがローカルで記憶を保持できるようにするためのライブラリとして開発されている。BlazorMemoryは、IndexedDB、EF Core、pgvector、InMemoryの4つのストレージバックエンドをサポートし、OpenAI、Anthropic、Azure OpenAI、Ollamaの4つのAIプロバイダーに対応している。特にOllamaは、ローカルでの動作とコスト効率の高さから注目されている。このプロジェクトは、ローカルでの記憶保持を実現するための技術的課題とその解決策を示しており、Graftと同様に、AIアシスタントがユーザーのニーズに応じて適切に過去の情報を活用できるようにする技術の一つとして位置づけられている。

## 不確実な点・追加確認が必要な点

記事間の食い違いや、資料からは断定できない点を具体的に書く。  

Graftに関する情報は、GitHubリポジトリやSSD Nodesの記事、DEV Communityの投稿など複数のソースから確認されているが、具体的な公開日時や取得日時については不明である。記事1のGitHubリポジトリでは、Graftが「local-first memory」を提供し、SaaSやAPIキーを必要としないローカルの知識保存を強調している。一方、記事2のSSD Nodesでは、Graftがコードベースのマップとして機能し、モデルのコンテキストプロトコル（MCP）を介して検索ツールを提供していると述べられている。この点では、Graftの技術的実装と用途が明確にされている。  

一方で、記事3のBlazorMemory1.0は、Blazorアプリケーション内でAIチャットアシスタントがローカルで記憶を保持するためのライブラリとして開発されたが、Graftとは異なるアプローチを取っている。BlazorMemoryは、IndexedDBやEF Coreなど複数のストレージバックエンドをサポートし、AIプロバイダーとの連携も可能であるが、Graftのようなコードベースの知識保存とは異なり、ユーザーのインタラクションや記憶の管理に焦点を当てている。  

また、記事5のDeepSeek Harnessに関する情報は、プラグインベースのアーキテクチャを採用し、Cordis拡張の選択肢を提供しているが、Graftとの直接的な関連性は不明瞭である。このため、各記事が提示する技術的特徴や用途は明確だが、Graftの具体的なバージョンや更新履歴、さらには他のツールとの比較については、資料からは断定できない点が多い。

## 元記事一覧

- [GitHub - AEndrix03/Graft: Your coding agents forget. Graft doesn't. Persistent local memory that brings back fixes, decisions and project knowledge when they matter — across Claude Code, Codex, ChatGPT and more. Local-first. No SaaS. No API key.](https://github.com/AEndrix03/Graft)
- [Graft: a codebase map for coding agents · SSD Nodes](https://www.ssdnodes.com/learn/graft-codebase-graph-for-agents)
- [BlazorMemory1.0isout.Tenmonths,14packages,andwhatIgot...](https://dev.to/aftabkh4n/blazormemory-10-is-out-ten-months-14-packages-and-what-i-got-wrong-along-the-way-1548)
- [Download Instagram 446.0.0.49.77 for Android (Free)](https://instagram.en.divxland.org/download/)
- [DeepSeek Harness “Everything Is a Plugin”: choose the right Cordis extension seam - DEV Community](https://dev.to/ahab_indieseek/deepseek-harness-everything-is-a-plugin-choose-the-right-cordis-extension-seam-4773)
