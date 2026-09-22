---
title: Lean4を用いたスルーヴィルのノワンドリングドメイン定理の形式化
type: knowledge
status: draft
created: 2026-09-22
updated: 2026-09-22
confidence: medium
---

# Lean4を用いたスルーヴィルのノワンドリングドメイン定理の形式化

## 結論

Lean 4 を用いた Sullivan の No Wandering Domains 定理の形式化は、複素動力学における基本的な結果を数学的厳密性のもとで表現し、AI 生成コードの検証や高信頼性システムにおける形式検証の実用性を示す重要な研究である。この形式化には、正規族、Montel-Carathéodory 定理、Julia および Fatou 集合、可測リーマン写像定理などの複雑な数学的理論が関与しており、Lean 4 の機能を最大限に活用した証明構造が構築されている。

## テーマ概要

Formalization of Sullivan's No Wandering Domains Theorem in Lean は、数学の定理を形式的に証明するためのプログラミング言語と証明支援ツールである Lean 4 を用いた研究です。この定理は、リーマン球面上の次数が2以上の有理写像の Fatou 成分が最終的に周期的であることを主張しており、複素動力学の分野における基本的な結果です。この定理の形式化には、正規族、Montel-Carathéodory 定理、Julia および Fatou 集合、ローカル Sobolev 定常性、Wirtinger 微分、Cauchy および Beurling 変換、解析的と幾何学的な準正則性の同等性、可測リーマン写像定理などの数学的理論が関与しています。Lean 4 を用いた形式化は、複雑な数学的構造を正確に表現し、AI 生成コードの検証にも応用可能な技術として注目されています。この研究は、形式検証が数学やコンピュータサイエンスにおいて重要な役割を果たすことを示しており、特に航空、医療ソフトウェア、金融システムなどの高コストエラーが発生する分野での応用が期待されています。

## 共通して確認できる点

複数の記事で共通して確認できた事実として、SullivanのNo Wandering Domains定理がLean 4を用いて形式化されたことが挙げられる。この定理は、リーマン球面上の次数が2以上の有理写像のFatou成分が最終的に周期的であることを示している。この形式化には、正規族、Montel-Carathéodory定理、Julia集合とFatou集合、ローカルSobolev正則性、Wirtinger微分、Cauchy変換とBeurling変換、解析的および幾何学的な擬正則性の同等性、可測リーマン写像定理などの数学的理論が含まれていた。また、Lean 4は形式証明のためのオープンソースのプログラミング言語および証明支援ツールであり、数学的定理の形式化やAI生成コードの検証に利用されている。さらに、この研究は形式検証の重要性を強調しており、航空、医療ソフトウェア、金融システムなどの高コストエラーの分野での標準的なツールとしてのLean 4の利用が挙げられている。

## 記事ごとの差分・視点の違い

記事「Formalization of Sullivan's No Wandering Domains Theorem in Lean」は、SullivanのNo Wandering Domains定理をLean 4で形式化した研究であり、その数学的背景と証明構造を詳細に説明している。この論文では、正規族、Montel-Carathéodory定理、Julia集合とFatou集合、局所Sobolev正則性、Wirtinger微分、Cauchy変換やBeurling変換、解析的と幾何学的擬正則性の同値、可測リーマン写像定理などの理論を扱っている。また、Lean 4による形式化プロセスや、再利用可能なコンポーネント、自動形式化ワークフローについても述べている。この研究は形式検証の重要性を強調し、特に航空・医療ソフトウェア・金融システムなどの高コストエラーを伴う分野での応用を示している。

記事「On the Reconstruction of SAS from Other Triangle Congruence Criteria」は、ヒルベルト平面において、SAS合同の公理を除去した状態で、他の三角形合同条件からSASを再構成する可能性を検討している。この論文では、ASA合同条件と射線対応原理を用いることでSASを再構成可能であることを示し、SSSやAAAなどの条件でも再構成が可能だが、それぞれ補助的な原理が必要であることを論じている。また、Pons Asinorumや斜辺角条件などの独立性も分析しており、三角形合同条件の論理構造を深く掘り下げている。

記事「[2609.16485] Certified Inference and Training for Deep Equilibrium Networks」は、Deep Equilibrium Networks（DEQ）における認証された推論とトレーニングフレームワークの開発を目的としている。この研究では、精度 $2^{-b}$ に達するように interpolation を形式化し、コンパクトな入力ホモトピーを用いて一意な枝を選択する仕組みを提案している。トレーニングではローカルプラスローランク再帰を拡張し、認証されたゲート実現や列安定性、正定義な推論、有限アップデートエラー予算などの要件を満たす必要がある。また、Lean 4が論文の定量的コアと具体的な推論バックエンドを検証しており、数値比較もロードされたメカニズムを示している。

## 深掘り調査で得られた知見

深掘り調査により、SullivanのNo Wandering Domains定理のLeanでの形式化に関する研究が進められていることが確認された。この定理は、リーマン球面上の次数が2以上である有理写像のFatou成分が最終的に周期的であることを主張しており、その形式化には、正規族、Montel-Carathéodory定理、Julia集合とFatou集合、局所Sobolev正則性、Wirtinger微分、Cauchy変換やBeurling変換、解析的・幾何学的準共形性の同等性、可測リーマン写像定理など、複数の数学的理論が関与している。Lean4というオープンソースのプログラミング言語と証明支援ツールを用いた形式化は、複雑なシステムの正しさを保証するための形式検証の重要性を浮き彫りにしている。また、Lean4は航空、医療ソフトウェア、金融システムなどの高コストエラーが発生する分野で標準的なツールとして利用されている。さらに、AI生成コードの利用が急増しており、2025年にはスタートアップの40%以上がAI生成コードを採用しており、2026年には60%以上に達すると予測されている。この研究は、数学とコンピュータサイエンスの交差点で形式検証の実用性を示しており、今後の技術革新に向けた重要な基盤となる。

## 不確実な点・追加確認が必要な点

記事間の食い違いや、資料からは断定できない点を以下のように具体的に述べる。まず、記事1と記事2は同一の論文を異なる形式で提供しており、両者が同一のURLを指していることから、同一の論文のPDFとAbstractの形式違いである可能性が高い。ただし、両者が同一の論文であるかは明確に確認されていないため、区別はできない。また、記事3と記事4はタイトルが類似しており、内容もほぼ同じであるため、同一の論文である可能性が高いが、URLが異なるため、区別はできない。記事5は他のテーマに関する論文であり、Sullivanの定理とは無関係である。したがって、記事1と記事2、記事3と記事4は同一の論文である可能性が高いが、断定はできない。また、各論文の公開日時や取得日時が不明であるため、時系列的な優先順位を判断することができない。さらに、各論文の内容が異なるため、テーマごとの深掘りが必要である。

## 元記事一覧

- [FormalizationofSullivan'sNo Wandering DomainsTheoreminLean](https://arxiv.org/abs/2609.16027)
- [FormalizationofSullivan'sNoWanderingDomainsTheoreminLean](https://arxiv.org/pdf/2609.16027)
- [OntheReconstructionofSASfromOtherTriangleCongruence...](https://arxiv.org/pdf/2609.16039)
- [OntheReconstructionofSASfromOtherTriangleCongruence...](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7447142)
- [[2609.16485]CertifiedInferenceandTrainingforDeepEquilibrium...](https://arxiv.org/abs/2609.16485)
