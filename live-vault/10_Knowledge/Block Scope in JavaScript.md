---
title: JavaScriptのブロックスコープ
created: 2026-08-19
updated: 2026-08-19
---

# JavaScriptのブロックスコープ

## 概要
JavaScriptにおけるブロックスコープとは、コードブロック `{}` 内で `let` と `const` によって宣言した変数の可視範囲を指します。これらの変数は宣言されたブロック内からのみアクセスできるため、意図しない変数の上書きを防ぎ、コードを整理しやすくします。

## 詳細

- **ブロックスコープ**: ブロック内で `let` または `const` によって宣言した変数は、そのブロック内からのみアクセスできます。宣言前にアクセスすると（Temporal Dead Zone）、ReferenceErrorになります。
- **関数スコープ**: 関数内で `var` によって宣言した変数は関数スコープを持ち、入れ子のブロックに関係なく関数全体からアクセスできます。
- **グローバルスコープ**: 関数やブロックの外で宣言した変数はグローバルスコープを持ち、プログラム全体からアクセスできます。
- **ブロック文**: ブロック文は複数の文をまとめるもので、`if...else` や `for` ループなどの制御構文で使われます。JavaScriptが1つの文を期待する場所で、複数の文を使えるようにします。
- **ブロックスコープを持つ宣言**: `let`、`const`、`class` の宣言はブロックスコープを持ち、一時変数がグローバル名前空間を汚染するのを防ぎます。
- **非Strictモード**: 非Strictモードでは、ブロック内の `var` 宣言はブロックスコープではなく、関数スコープまたはグローバルスコープとして扱われます。
- **Strictモード**: Strictモードでは、ブロック内の `let` と `const` の宣言はブロックスコープを持ち、ブロック内の関数宣言もブロックにスコープされます。
- **モジュールスコープ**: ESモジュールでは、`var` はモジュールスコープ、`let` と `const` はブロックスコープを持ちます。

## 出典
- [JavaScript Scope - W3Schools](https://www.w3schools.com/js/js_scope.asp)
- [Block statement - JavaScript - MDNCode sample](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/block)
- [Scope of Variables in JavaScript - GeeksforGeeks](https://www.geeksforgeeks.org/javascript/javascript-scope/)
- [What is function and block scope in JavaScript?](https://www.educative.io/answers/what-is-function-and-block-scope-in-javascript)
- [Scope in JavaScript – Global vs Local vs Block Scope Explained](https://www.freecodecamp.org/news/scope-in-javascript-global-vs-local-vs-block-scope/)

## 未解決点
- 非Strictモードにおける `var` の正確な挙動は、環境によって異なる場合があります。
- 異なる環境におけるブロックスコープとモジュールスコープの相互作用については、さらなる確認が必要です。
- 変数管理とコード構造に対するブロックスコープの長期的な影響は、JavaScriptエコシステムでなお変化しています。

## 出典


## 未解決点

- 追加調査が必要です。
