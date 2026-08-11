---
type: knowledge
status: draft
created: 2026-08-11
updated: 2026-08-11
confidence: medium
---

+++ 
created: 2026-08-11
updated: 2026-08-11

# Reconstructing Lesion Parameters from Aphasic Picture Naming Error Profiles in Large Language Models

## 概要
この研究では、大規模言語モデル（LLM）に「脳損傷」をシミュレーションし、アファジー（失語症）患者の画像命名エラーのパターンを再現する方法が検討されました。LLMに制御された「損傷」を適用し、患者の命名エラーと一致する結果を達成しました。

## 詳細
研究者はLLaVA 1.6というマルチモーダル言語モデルを使用し、画像命名テスト（PNT）の結果を再現しました。モデルに層ごとの損傷を適用し、エラーの種類を7つに分類しました。結果として、モデルは6つのエラー種類を再現でき、7種類のうち1つ（形式的パラフィア）は除外されました。

研究では、患者の個別エラープロファイルに一致するモデルのパラメータ配置が見出され、97.8%の患者で6種類以上のエラーが一致し、79.5%の患者ではすべてのエラーが一致しました。統計的検定により、この一致は偶然ではなく、エラーの構造に起因することを確認しました。

## ソース
- [2608.06429]RecoveringLesionParametersfromAphasic Picture... (https://arxiv.org/abs/2608.06429)
- [2608.06429]RecoveringLesionParametersfromAphasic Picture NamingError... (https://arxiv.org/pdf/2608.06429)
- Lesioned MultimodalLanguageModelsReproduce Aphas... (https://franklineh.com/learn/research/yRHUkyAQfD33RLESmjLx)
- Voxel-basedlesion-parametermapping: Identifying the neural... (https://pmc.ncbi.nlm.nih.gov/articles/PMC3709005/)
- Frontiers |Picturenamingtest through the prism of cognitive... (https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2024.1332391/full)

## 解決されていない点
- 形式的パラフィアの再現がなぜ失敗したのかは未解決。
- モデルのパラメータ空間における具体的な配置は明確にされていない。
- 脳損傷のシミュレーションと実際の患者の脳損傷との関係は不明。

## その他
研究は、LLMが言語間で性能を維持するための新たなアプローチを示唆しており、言語モデルのクロス言語理解の改善に貢献する可能性があります。

## 出典


## 未解決点

- 追加調査が必要です。
