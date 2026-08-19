---
title: Block Scope in JavaScript
created: 2026-08-19
updated: 2026-08-19
---

# Block Scope in JavaScript

## Overview
Block scope in JavaScript refers to the accessibility of variables declared with `let` and `const` within a code block `{}`. These variables are only accessible within the block they are defined, which helps prevent unintended variable overwrites and improves code organization.

## Details

- **Block Scope**: Variables declared with `let` or `const` inside a block are accessible only within that block. Accessing them before declaration (Temporal Dead Zone) results in a ReferenceError.
- **Function Scope**: Variables declared with `var` inside a function have function scope and are accessible throughout the function, regardless of nested blocks.
- **Global Scope**: Variables declared outside any function or block have global scope and are accessible throughout the entire program.
- **Block Statements**: A block statement groups multiple statements and is used with control flow constructs like `if...else` and `for` loops. It allows the use of multiple statements where JavaScript expects a single statement.
- **Block-Scoped Declarations**: `let`, `const`, and `class` declarations are block-scoped and help prevent temporary variables from polluting the global namespace.
- **Non-Strict Mode**: In non-strict mode, `var` declarations inside blocks are treated as having function or global scope, not block scope.
- **Strict Mode**: In strict mode, `let` and `const` declarations inside blocks are block-scoped, and function declarations inside blocks are scoped to the block.
- **Module Scope**: In ES modules, `var` is module-scoped, while `let` and `const` are block-scoped.

## Sources
- [JavaScript Scope - W3Schools](https://www.w3schools.com/js/js_scope.asp)
- [Block statement - JavaScript - MDNCode sample](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/block)
- [Scope of Variables in JavaScript - GeeksforGeeks](https://www.geeksforgeeks.org/javascript/javascript-scope/)
- [What is function and block scope in JavaScript?](https://www.educative.io/answers/what-is-function-and-block-scope-in-javascript)
- [Scope in JavaScript – Global vs Local vs Block Scope Explained](https://www.freecodecamp.org/news/scope-in-javascript-global-vs-local-vs-block-scope/)

## Unresolved Points
- The exact behavior of `var` in non-strict mode may vary across environments.
- The interaction between block scope and module scope in different environments requires further clarification.
- The long-term implications of block scope on variable management and code structure are still evolving in the JavaScript ecosystem.

## 出典


## 未解決点

- 追加調査が必要です。
