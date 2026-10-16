---
title: Microsoft、MAI Playground拡充で画像・音声・推論モデルを提供
type: knowledge
status: draft
created: 2026-10-17
updated: 2026-10-17
confidence: medium
---

# Microsoft、MAI Playground拡充で画像・音声・推論モデルを提供

## 結論

MicrosoftはMAI Playgroundを拡充し、画像生成、音声処理、音声認識、論理的推論の4つのモデルを提供しており、MAI-Image-2.6はArenaのテキストから画像生成のレーダーで2位を獲得。また、MAI-Thinking-1は350億のアクティブパラメータを備えた論理的推論モデルとして、企業向けのタスクに適した環境で利用可能となっている。これらのモデルはMicrosoft FoundryとMAI Playgroundを通じて提供され、一部の顧客にはAPI経由でのアクセスが可能である。

## テーマ概要

MicrosoftはMAI Playgroundを拡充し、画像生成、音声処理、音声認識、論理的推論などのモデルを提供しています。この拡充により、ユーザーはMicrosoftが開発したMAIファミリのモデルをテストできる限られたプレビュー環境を手に入れました。特に、MAI-Image-2.5とMAI-Image-2.6といった画像生成モデルは、PowerPointやOneDriveなどのツールで利用され、実際の業務フローでの適用が期待されています。また、MAI-Thinking-1は350億のアクティブパラメータを備えた論理的推論モデルで、企業向けのタスクに適しています。これらのモデルはMicrosoft FoundryとMAI Playgroundを通じて提供されており、一部の顧客にはAPI経由でのアクセスが可能となっています。この動きは、MicrosoftがOpenAIへの依存を減らし、自社のAI技術を強化する戦略の一環として注目されています。

## 共通して確認できる点

MicrosoftはMAI Playgroundを拡充し、画像生成、音声処理、音声認識、論理推論のモデルを搭載した限定プレビュー環境として提供しています。この環境では、ユーザーがMicrosoftが開発したモデルをテストできる場が設けられており、APIや広範な開発者への提供は段階的に進められています。特に画像生成は明確な利用ケースとして挙げられ、MAI-Image-2.5やMAI-Image-2.6がその代表例です。MAI-Image-2.5はPowerPointやOneDriveなどのツールで利用されており、MAI-Image-2.6はArenaのテキストから画像生成のレーダーで2位を記録しています。また、MAI-Thinking-1は論理推論モデルとして350億のアクティブパラメータを搭載し、128,000トークンのコンテキストウィンドウをサポートしています。これらのモデルはMicrosoft FoundryおよびMAI Playgroundを通じて提供されており、一部の顧客にはAPI経由でアクセスが可能となっています。

## 記事ごとの差分・視点の違い

記事1はMicrosoftがMAI Playgroundを拡充し、画像生成、音声、音声認識、論理推論のモデルを提供していることを紹介しています。重点はモデルの種類と利用環境（限定プレビュー）にあります。また、MAI-Thinking-1やMAI-Image-2.5、MAI-Image-2.6の存在を示しつつ、モデルの詳細な性能比較やコスト情報は提示されていません。記事2は同様の内容を伝えていますが、情報量が少なく、主にMAI Playgroundの拡張とモデルのラインナップを強調しています。記事3はMAI-Image-2.6の性能をArenaでの順位で示し、テキスト生成の改善を強調しています。記事4はMAI-Image-2.6-Flashの導入と、高効率なプロダクションワークロードへの適応を主な論点としています。記事5はMAI-Thinking-1がパブリックプレビューで提供され、Foundryを通じて利用可能になったことを伝えています。各記事は、モデルの種類や性能、利用環境、およびMicrosoftのAI戦略の一部としての位置づけをそれぞれ異なる角度から伝えています。

## 深掘り調査で得られた知見

MicrosoftはMAI Playgroundを拡充し、画像生成、音声処理、音声書き起こし、論理的推論の4つのモデルを導入しました。この拡充により、ユーザーはMicrosoftが開発したMAIファミリのモデルをテストするための限られたプレビュー環境を活用できます。特に、画像生成においてはMAI-Image-2.5とMAI-Image-2.6が利用可能で、MAI-Image-2.6はArenaのテキストから画像生成のレーダーで2位を獲得しています。また、MAI-Image-2.6はテキスト描画において91 Eloポイントの向上を実現し、ビジネス用途での画像ワークフローにおいては、製品のプロトタイプやキャンペーン資産、サインのコンセプト、ブランドグラフィックなど、正確で読みやすいテキストが求められる場面で特に有用です。

MAI-Image-2.6-Flashという高速バージョンも導入され、マルチ画像参照編集やウェブ接地、ダイナミックなアスペクト比をサポートしています。これは、レイテンシーに敏感で高 throughput の生産ワークロードに適したモデルです。MAI-Thinking-1は、企業向けの論理的推論モデルとして公開され、350億のアクティブパラメータと10000億の総パラメータを持つスパースのMixture-of-Experts（MoE）モデルです。256,000トークンのコンテキストウィンドウをサポートし、Chat Completions APIとの互換性もあります。

これらのモデルは、Microsoft FoundryとMAI Playgroundを通じて提供されており、一部のモデルは選択された顧客に対してAPIを通じて利用可能となっています。また、WPP（World Public Policy）はこれらのモデルの早期導入者として挙げられています。Microsoftはこれらのモデルのリリースを段階的に進め、APIや開発者向けの広範な利用を段階的に拡大していく予定です。これにより、MicrosoftはOpenAIへの依存を減らす戦略の一環として、自社のAIモデルを強化しています。

## 不確実な点・追加確認が必要な点

記事間の情報にはいくつかの食い違いや断定できない点が確認されている。まず、MAI Playgroundの拡張について、記事1と記事2では同様に画像生成、音声、音声認識、論理推論モデルが追加されたと記述されているが、具体的なモデル名やバージョンについては一貫性が欠けている。記事1ではMAI-Image-2.5とMAI-Image-2.6が挙げられている一方で、記事2ではMAI-Image-2の名前が使われており、バージョン番号の違いが指摘されている。また、記事3と記事4ではMAI-Image-2.6の詳細な性能向上が記載されており、その改善点としてテキストレンダリングの Elo スコアが +91 上昇していることが明記されている。しかし、これらの改善が実際にどの業務フローにどれほど適用されるかについては、明確なベンチマークや保証が提示されていない。さらに、記事5ではMAI-Thinking-1が公開プレビュー開始されていることが示されているが、その具体的な機能やパラメータ数、コンテキストウィンドウの長さについては、記事1や記事4の記述と整合性が取れていない。また、モデルのコストや導入に関する詳細情報、企業向けの導入スケジュールについても、どの記事にも明確な記述が見られず、今後の情報が必要である。

## 元記事一覧

- [MicrosoftMAIPlayground:Models, Access and Governance](https://scalevise.com/resources/microsoft-mai-playground-models-access-governance/)
- [#microsoftarticles | Hashnode](https://hashnode.com/tag/microsoft)
- [MAI-Image-2.6 launches at No. 2 on Arena ahead of Google ...](https://microsoft.ai/news/mai-image-2-6-launches-at-no-2-on-arena-ahead-of-google-meta-and-xai/)
- [Pushing the quality-cost frontier with MAI-Image-2.6 ...](https://microsoft.ai/news/pushing-the-quality-cost-frontier-with-mai-image-2-6/)
- [MicrosoftMAI-Thinking-1EntersPublicPreview](https://scalevise.com/resources/microsoft-mai-thinking-1-public-preview-foundry-playground/)
