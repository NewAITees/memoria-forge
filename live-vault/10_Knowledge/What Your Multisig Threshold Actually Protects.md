---
title: multisigの閾値が実際に保護するものとは
type: knowledge
status: draft
created: 2026-09-18
updated: 2026-09-18
confidence: medium
---

# multisigの閾値が実際に保護するものとは

## 結論

Multisigのセキュリティにおいて、閾値そのものではなく、モジュールやガード、フォールバックハンドラ、デリゲートコールなどの構成要素が、実際に資産を保護する上でより重要である。特に、モジュールは閾値を無視してトランザクションを実行できるため、不正なモジュールが存在する場合、閾値の設定は意味を失う。したがって、multisigのセキュリティを確保するためには、閾値だけでなく、これらの要素を総合的に検討する必要がある。

## テーマ概要

Multisig（マルチシグ）は、複数の署名が必要となるウォレット形式であり、資産のセキュリティを高めるための一般的な手法です。しかし、そのセキュリティの核心は「閾値（threshold）」だけに依存しているわけではありません。最近の調査では、閾値が実際に保護しているのは「シグネチャの数」ではなく、むしろ「モジュール」や「ガード」などの構成要素が重要であることが明らかになっています。特に、モジュールは、シグネチャなしでトランザクションを実行できるため、悪意のあるモジュールが存在すれば閾値の設定が意味を失います。また、ガードやフォールバックハンドラといった要素も、セキュリティに大きく影響するため、これらを含めた全体の設計が重要です。このような背景から、What Your Multisig Threshold Actually Protectsというテーマは、マルチシグのセキュリティを正しく理解し、適切に構築するための注目される話題となっています。

## 共通して確認できる点

Multisig wallets are designed to enhance security by requiring multiple signatures for transaction execution, with the threshold often seen as the primary security factor. However, the actual protection provided by the threshold is limited, as modules within multisig systems can bypass this requirement entirely. A module, which is a contract with authority to execute transactions, can perform any action without needing owner signatures, rendering the threshold irrelevant if the module is compromised. This highlights that the threshold is not the weakest link in most cases, and other elements like modules, guards, fallback handlers, and delegate calls play a more critical role in determining the overall security of a multisig wallet. Additionally, multisig offers threshold security, which can protect users from single points of failure, ensuring that no funds are lost if any one component of the setup is destroyed, misplaced, or stolen. Despite these benefits, the security of a multisig wallet depends on multiple factors, and it is essential to consider all elements when assessing the overall security of the wallet.

## 記事ごとの差分・視点の違い

記事「What Your Multisig Threshold Actually Protects」では、マルチシグのしきい値が実際に保護しているものについて詳しく説明されており、しきい値が単なるセキュリティの中心ではなく、他の要素（モジュール、ガード、フォールバックハンドラ、デリゲートコールなど）がより重要な役割を果たしていると指摘している。一方、「Multi-level thresholds: Why multisig always has a higher security ceiling」では、マルチシグのしきい値がセキュリティの上限を高める理由を説明し、個人と機関のそれぞれの資産管理戦略におけるマルチシグの利点を比較している。また、「Deltaencodingmultiplayergamestate」では、ゲームの状態同期におけるデルタエンコーディングの仕組みと、クライアントごとに異なる差分を送信する設計について述べている。一方、「hpx7/delta-pack」は、状態間の差分をエンコードし、それをもとに新しい状態を再構築するパッケージの仕様について説明している。最後に、「A 30-Day Atomic Swap Is a Free 688 bps Option. That Is the ...」では、原子交換における時間的要素とオプション価値の計算について解説しており、信頼を最小限に抑えながら取引を実現する仕組みを示している。各記事は、それぞれの分野において、技術的な詳細やセキュリティの観点、または通信効率の向上など、異なる視点から情報を提供している。

## 深掘り調査で得られた知見

Multisigのセキュリティにおいて、閾値（threshold）は多くの場合、主な保護要因として考えられがちですが、実際にはその他の要素がより重要な役割を果たしています。特に、モジュール（module）は閾値を無視してトランザクションを実行できるため、不正なモジュールが存在する場合、閾値の設定は意味を失います。例えば、Gnosis Safeでは、モジュールが存在する場合、そのモジュールが独自の権限を持つため、7-of-10の閾値設定であっても、モジュールが資金を独立して動かすことができれば、セキュリティは確保されません。また、ガード（guard）やフォールバックハンドラ（fallback handler）といった要素も、セキュリティに大きな影響を与えます。ガードは、閾値に加えて追加の検証を実施し、特定の操作を制限するなど、セキュリティを強化します。一方、フォールバックハンドラは、トークンの受け取り処理や再エントリーシーのリスクを生じる可能性があります。さらに、デリゲートコール（delegate call）は、ウォレットの実装を変更する可能性があり、不正な操作を許す危険性があります。これらの要素を考慮しない場合、単に閾値を高く設定しても、セキュリティは十分に確保されない可能性があります。したがって、multisigのセキュリティを評価する際には、閾値だけでなく、モジュール、ガード、フォールバックハンドラ、デリゲートコールといった要素を総合的に検討する必要があります。

## 不確実な点・追加確認が必要な点

記事間の食い違いや、資料からは断定できない点としては、テーマ「What Your Multisig Threshold Actually Protects」に関する情報が、一部の記事では具体的な技術的リスクやセキュリティ構造について詳しく解説されている一方で、他の記事ではその技術的側面に踏み込まず、むしろ多層的なセキュリティ戦略や、原子交換などの他の概念に焦点を当てている点が挙げられる。例えば、記事1では、マルチシグの閾値がセキュリティの主な保護対象ではないことを強調し、モジュールやガード、フォールバックハンドラ、デリゲートコールといった要素がセキュリティに与える影響を論じている。一方で、記事2は、マルチシグのセキュリティの上限について論じており、個人と機関の異なる運用戦略を比較している。また、記事5は、原子交換や前払いのコストについて述べており、マルチシグのセキュリティと直接的な関連性は薄い。このように、テーマに関連する記事は、それぞれ異なる視点からセキュリティや運用戦略を考察しており、技術的なセキュリティ構造に焦点を当てた情報は一部の記事に限定される。そのため、マルチシグの閾値が実際にどの程度のセキュリティを提供するかを断定するには、技術的な詳細を含む記事を参照する必要がある。

## 元記事一覧

- [What Your Multisig Threshold Actually Protects - DEV Community](https://dev.to/0xrivet/what-your-multisig-threshold-actually-protects-4jd)
- [Multi-level thresholds: Why multisig always has a higher security ceiling - Unchained](https://www.unchained.com/blog/multisig-security-ceiling)
- [Deltaencodingmultiplayergamestate- Old Light](https://oldlight.io/blog/anatomy-of-a-galaxy-delta/)
- [hpx7/delta-pack - npm](https://www.npmjs.com/package/@hpx7/delta-pack)
- [A 30-Day Atomic Swap Is a Free 688 bps Option. That Is the ...](https://dev.to/barissozen/a-30-day-atomic-swap-is-a-free-688-bps-option-that-is-the-honest-price-of-forward-settlement-4513)
