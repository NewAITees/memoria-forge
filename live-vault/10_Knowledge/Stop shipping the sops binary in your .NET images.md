---
title: sopsバイナリのコンテナイメージ配布中止
type: knowledge
status: draft
created: 2026-10-25
updated: 2026-10-25
confidence: medium
---

# sopsバイナリのコンテナイメージ配布中止

## 何が分かったか

Debianベースのコンテナイメージは特定の主要サービスに必要な依存関係を含んでいます [^fact-6f3051d4ae221948]。Alpineベースのイメージはサイズが小さいが、これらの依存関係は含まれていません [^fact-6f3051d4ae221948]。sopsバイナリはDebian（slim）とAlpine Linuxベースのコンテナイメージとして利用可能です [^fact-63bff011df49a3af]。

## 確認できた事実

- Debianベースのコンテナイメージは特定の主要サービスを使用するために必要な依存関係を含んでいます。一方、Alpineベースのイメージはサイズが小さいですが、これらの依存関係は含まれていません。 [^fact-6f3051d4ae221948]

- sopsバイナリはDebian（slim）とAlpine Linuxベースのコンテナイメージとして利用可能です。 [^fact-63bff011df49a3af]

- コンテナイメージはCosignとGitHub OIDCを使用して署名されています。 [^fact-ee2ee0cbb7722174]

- これらのリリースに関連するアーティファクト内に、バイナリ、パッケージ、SBOMのSLSAプロヴァイアンスが含まれています。 [^fact-55fb4b365bbecac5]

- sopsバイナリはDebian（slim）とAlpine Linuxベースのコンテナイメージとして利用可能です。 [^fact-63bff011df49a3af]

- コンテナイメージにはSLSAプロヴァイアンスの attestations が含まれています。 [^fact-6d485a23224b91d4]

- このリリースに関連するアーティファクト内に含まれるチェックサムファイルはCosignとGitHub OIDCを使用して署名されています。 [^fact-a2bee1b9234e77b6]

## それが意味すること

コンテナイメージはCosignとGitHub OIDCを使用して署名されており、信頼性が確保されています [^fact-ee2ee0cbb7722174]。SLSAプロヴァイアンスや attestations が含まれており、アーティファクトの信頼性が検証可能です [^fact-55fb4b365bbecac5]。チェックサムファイルも同様にCosignとGitHub OIDCで署名されています [^fact-a2bee1b9234e77b6]。 [^fact-ee2ee0cbb7722174] [^fact-55fb4b365bbecac5] [^fact-a2bee1b9234e77b6]

## まだ分からないこと

具体的な依存関係の内容や、Alpineベースのイメージが欠いている機能は明示されていません。

## 出典

[^fact-6f3051d4ae221948]: [Releases · getsops/sops· GitHub](https://github.com/getsops/sops/releases)
  - 根拠引用: 「The Debian-based container images include any dependencies which may be required to make use of certain key services, such as GnuPG, AWS KMS, Azure Key Vault, and Google Cloud KMS. The Alpine-based container images are smaller in size, but do not include these dependencies.」
[^fact-63bff011df49a3af]: [Releases · getsops/sops· GitHub](https://github.com/getsops/sops/releases)
  - 根拠引用: 「The sops binaries are also available as container images, based on Debian (slim) and Alpine Linux.」
[^fact-ee2ee0cbb7722174]: [Releases · getsops/sops· GitHub](https://github.com/getsops/sops/releases)
  - 根拠引用: 「The container images are signed using Cosign with GitHub OIDC.」
[^fact-55fb4b365bbecac5]: [Releases · getsops/sops· GitHub](https://github.com/getsops/sops/releases)
  - 根拠引用: 「The SLSA provenance of the binaries, packages, and SBOMs can be found within the artifacts associated with this release.」
[^fact-63bff011df49a3af]: [Releases · getsops/sops· GitHub](https://github.com/getsops/sops/releases)
  - 根拠引用: 「The sops binaries are also available as container images, based on Debian (slim) and Alpine Linux.」
[^fact-6d485a23224b91d4]: [Releases · getsops/sops· GitHub](https://github.com/getsops/sops/releases)
  - 根拠引用: 「The container images include SLSA provenance attestations.」
[^fact-a2bee1b9234e77b6]: [Releases · getsops/sops· GitHub](https://github.com/getsops/sops/releases)
  - 根拠引用: 「The checksums file provided within the artifacts attached to this release is signed using Cosign with GitHub OIDC.」
