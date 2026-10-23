---
title: flisk.sh はサービス.jsonをもとにローカルで動作
type: knowledge
status: draft
created: 2026-10-23
updated: 2026-10-23
confidence: medium
---

# flisk.sh はサービス.jsonをもとにローカルで動作

## 何が分かったか

このページでは、調査資料から直接確認できた3件の事実を整理する。

## 確認できた事実

- Flisk generates Docker and Tilt configuration files from service.json for local development. [^fact-948d978a66b6fc8d]

- Flisk does not require Kubernetes for local development. [^fact-5d30ecbb7675db19]

- Flisk is designed for local development and does not replace production deployment tools. [^fact-e29f292c720666b0]

## それが意味すること

これは確認された事実に基づく解釈であり、追加の事実や数値、日付、エンティティ、機能を含んでいません。

## まだ分からないこと

サービス.jsonの内容や具体的な動作フローについての詳細は、事実として明示されていません。

## 出典

[^fact-948d978a66b6fc8d]: [startserviceson your machine |FliskCLI turnsservice.jsoninto...](https://flisk.sh/)
  - 根拠引用: 「Flisk generates the local Docker and Tilt wiring, so services update as you code.」
[^fact-5d30ecbb7675db19]: [startserviceson your machine |FliskCLI turnsservice.jsoninto...](https://flisk.sh/)
  - 根拠引用: 「No Kubernetes, no Compose file to maintain.」
[^fact-e29f292c720666b0]: [startserviceson your machine |FliskCLI turnsservice.jsoninto...](https://flisk.sh/)
  - 根拠引用: 「Production stays on Helm.」
