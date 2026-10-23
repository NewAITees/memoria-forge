---
title: なぜRuby LSPをやめたのか
type: knowledge
status: draft
created: 2026-10-24
updated: 2026-10-24
confidence: medium
---

# なぜRuby LSPをやめたのか

## 何が分かったか

このページでは、調査資料から直接確認できた3件の事実を整理する。

## 確認できた事実

- Ruby Symbol Search provides fuzzy symbol search, allowing developers to find Ruby symbols even if they misspell or abbreviate the name. [^fact-24588591b95a2840]

- Ruby Symbol Search includes features such as Go to Definition, an Outline View, and native Workspace Symbol Search (Ctrl/Cmd + T), all backed by a lightweight, instantly-built index. [^fact-b3dd56c4497f6213]

- Ruby Symbol Search provides a typo-tolerant fuzzy search for Ruby symbols without requiring Ruby LSP setup. [^fact-d89d42c4c9f3b1d3]

## それが意味すること

これらの事実は、Ruby Symbol SearchがRubyシンボルの検索をより柔軟に実行できる可能性を示唆しています。ただし、これは事実に基づく解釈であり、具体的な機能や設定に関する詳細は含まれていません。

## まだ分からないこと

Ruby LSPの必要性や、Ruby Symbol Searchがどのように実装されているかについての具体的な情報は提供されていません。

## 出典

[^fact-24588591b95a2840]: [RubySymbolSearch- Visual Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=vscode-bkaz.ruby-symbol-search)
  - 根拠引用: 「Ruby Symbol Search brings instant, typo-tolerant fuzzy search for Ruby classes, modules, methods, and more straight into VS Code — with zero Ruby LSP setup required.」
[^fact-b3dd56c4497f6213]: [RubySymbolSearch- Visual Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=vscode-bkaz.ruby-symbol-search)
  - 根拠引用: 「This extension also provides Go to Definition, an Outline View, File-level Symbol Navigation, and native Workspace Symbol Search (Ctrl/Cmd + T) — all backed by the same lightweight, instantly-built index, with no language server to install or keep running.」
[^fact-d89d42c4c9f3b1d3]: [RubySymbolSearch- Visual Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=vscode-bkaz.ruby-symbol-search)
  - 根拠引用: 「Ruby Symbol Search brings instant, typo-tolerant fuzzy search for Ruby classes, modules, methods, and more straight into VS Code — with zero Ruby LSP setup required.」
