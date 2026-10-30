---
title: サンドボックスのPython RestrictedPythonとDockerとPyodideの比較
type: knowledge
status: draft
created: 2026-10-30
updated: 2026-10-30
confidence: medium
---

# サンドボックスのPython RestrictedPythonとDockerとPyodideの比較

## 何が分かったか

LiteLLMのv1.107.0は公式ソースタグに悪意のあるファイルが含まれていないが、不正なアーティファクトは攻撃者制御のリポジトリから作成された[^fact-b1cca9a0ce7ae4f4][^fact-76ec0bcbe14f8d94]。攻撃はUTC午後12時06分にUpwindの研究者によって検出され[^fact-2e5b5b24ff6af5c2]。問題のあるバージョンはUTC午後1時23分に隔離され、感染ファイルはUTC午後2時20分までに削除または置き換えられた[^fact-fdedf4a3f6d9886d]。

## 確認できた事実

- GitHubの公式v1.107.0ソースタグには悪意のあるファイルが含まれていません。不正なアーティファクトは攻撃者によって制御されたリポジトリから構築されました。 [^fact-e3ec5c46257999b9]

- 攻撃はUpwindのセキュリティ研究者Lidor MachlufがUTC午後12時06分に検出されました。 [^fact-2e5b5b24ff6af5c2]

- Pythonプログラミング言語が起動するたびに自動的に実行されるように設計されており、Unixシステム用の資格情報の盗み取りツールとバックドアを含んでいました。 [^fact-a4c836f2af3c3771]

- 攻撃はUpwindのセキュリティ研究者Lidor MachlufがUTC午後12時06分に検出されました。 [^fact-2e5b5b24ff6af5c2]

- それ以降、UTC午後1時23分に最初のプラットフォームが問題のあるバージョンを隔離し、UTC午後2時20分までに残りのサービスが感染したファイルを削除または置き換えました。 [^fact-fdedf4a3f6d9886d]

- 不正なアーティファクトは攻撃者によって制御されたリポジトリから構築されました。 [^fact-76ec0bcbe14f8d94]

- GitHubの公式v1.107.0ソースタグには悪意のあるファイルが含まれていません。 [^fact-b1cca9a0ce7ae4f4]

- GitHubの公式v1.107.0ソースタグには悪意のあるファイルが含まれていません。 [^fact-b1cca9a0ce7ae4f4]

## それが意味すること

攻撃はリポジトリの制御を狙っており、サンドボックス技術はそのような不正なアーティファクトを防ぐ可能性がある。また、不正なアーティファクトが作成されたリポジトリの制御は、攻撃の成功に直結している。 [^fact-76ec0bcbe14f8d94] [^fact-fdedf4a3f6d9886d]

## まだ分からないこと

不正なアーティファクトがどのようにリポジトリから生成されたか、具体的な手順は不明である。また、サンドボックス技術が実際に攻撃を防ぐかどうかは明確に示されていない。

## 出典

[^fact-e3ec5c46257999b9]: [Contained: Oct 21, 2026LiteLLMrelease v1.107.0Compromised](https://docs.litellm.ai/blog/security-incident-oct-21-2026)
  - 根拠引用: 「The official v1.107.0 source tag in GitHub does not contain the malicious files. The compromised artifacts were built from an attacker-controlled repository.」
[^fact-2e5b5b24ff6af5c2]: [Hacker breached LiteLLM and uploaded malicious… | Hacks.gr](https://en.hacks.gr/chaker-paraviase-to-litellm-kai-anevase-kakovoyli-enimerosi-logismikoy/)
  - 根拠引用: 「The attack was detected by security researcher Lidor Machluf of Upwind at 12:06 PM UTC.」
[^fact-a4c836f2af3c3771]: [Hacker breached LiteLLM and uploaded malicious… | Hacks.gr](https://en.hacks.gr/chaker-paraviase-to-litellm-kai-anevase-kakovoyli-enimerosi-logismikoy/)
  - 根拠引用: 「The program was designed to run automatically when the Python programming language was started and included a credential-stealing tool and a backdoor for Unix systems.」
[^fact-2e5b5b24ff6af5c2]: [Hacker breached LiteLLM and uploaded malicious… | Hacks.gr](https://en.hacks.gr/chaker-paraviase-to-litellm-kai-anevase-kakovoyli-enimerosi-logismikoy/)
  - 根拠引用: 「The attack was detected by security researcher Lidor Machluf of Upwind at 12:06 PM UTC.」
[^fact-fdedf4a3f6d9886d]: [Hacker breached LiteLLM and uploaded malicious… | Hacks.gr](https://en.hacks.gr/chaker-paraviase-to-litellm-kai-anevase-kakovoyli-enimerosi-logismikoy/)
  - 根拠引用: 「Shortly thereafter, at 1:23 PM UTC, the first platform quarantined the problematic version, and by 2:20 PM UTC, the remaining services had removed or replaced the infected files.」
[^fact-76ec0bcbe14f8d94]: [Contained: Oct 21, 2026LiteLLMrelease v1.107.0Compromised](https://docs.litellm.ai/blog/security-incident-oct-21-2026)
  - 根拠引用: 「The compromised artifacts were built from an attacker-controlled repository.」
[^fact-b1cca9a0ce7ae4f4]: [Contained: Oct 21, 2026LiteLLMrelease v1.107.0Compromised](https://docs.litellm.ai/blog/security-incident-oct-21-2026)
  - 根拠引用: 「The official v1.107.0 source tag in GitHub does not contain the malicious files.」
[^fact-b1cca9a0ce7ae4f4]: [Contained: Oct 21, 2026LiteLLMrelease v1.107.0Compromised](https://docs.litellm.ai/blog/security-incident-oct-21-2026)
  - 根拠引用: 「The official v1.107.0 source tag in GitHub does not contain the malicious files.」
