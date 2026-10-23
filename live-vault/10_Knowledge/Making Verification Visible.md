---
title: フォームデータの可視化に関する考察
type: knowledge
status: draft
created: 2026-10-23
updated: 2026-10-23
confidence: medium
---

# フォームデータの可視化に関する考察

## 何が分かったか

このページでは、調査資料から直接確認できた3件の事実を整理する。

## 確認できた事実

- The jiraServiceManagement:portalRequestCreatePropertyPanel module is supposed to submit form data to Jira as a property that can be read back later. [^fact-316a4fdf4c920418]

- The shape of the payload object for view.submit() is not enforced by the @forge/bridge package, allowing any object to be submitted. [^fact-198b4941bf2dfa6e]

- Atlassian's documentation specifies the shape of the form data schema for the jiraServiceManagement:portalRequestCreatePropertyPanel module, including fields, isValid, key, and value. [^fact-346f46c5fa5ce404]

## それが意味すること

これらの事実は、フォームデータがJiraに送信され、後で読み取れる仕組みであることを示唆しています。ただし、フォームデータの構造は明示的に定義されていない可能性があり、柔軟な処理が可能であると解釈されます。

## まだ分からないこと

Atlassianのドキュメンテーションが具体的なフォームデータの構造を示しているものの、実際にどの形式で送信されるかは明確ではありません。また、送信されたデータがどのように処理されるかについての詳細は確認されていません。

## 出典

[^fact-316a4fdf4c920418]: [JSMPortal Request Create Property PanelSubmit| LeanZero](https://leanzero.net/tutorials/forge-jsm-portal-property-panel-submit)
  - 根拠引用: 「A jiraServiceManagement:portalRequestCreatePropertyPanel module is supposed to be one of the simpler Forge surfaces: a small form on the customer portal's request-creation screen, a call to view.submit() , and the value lands as a Jira issue property you can read back later.」
[^fact-198b4941bf2dfa6e]: [JSMPortal Request Create Property PanelSubmit| LeanZero](https://leanzero.net/tutorials/forge-jsm-portal-property-panel-submit)
  - 根拠引用: 「The @forge/bridge package won't stop you from making the same mistake. Its own shipped types declare submit as (payload?: any) => Promise<void> — any object compiles, any object resolves.」
[^fact-346f46c5fa5ce404]: [JSMPortal Request Create Property PanelSubmit| LeanZero](https://leanzero.net/tutorials/forge-jsm-portal-property-panel-submit)
  - 根拠引用: 「Atlassian's own manifest-reference page for the module documents the shape directly, in a "Form data schema" table: fields is a required list of field objects, isValid is a required boolean, and each field object needs a key (string) and a value (object).」
