---
title: Apple SiliconでのFP8モデル実行対策：BF16とGGUFのワークアラウンド
type: knowledge
status: draft
created: 2026-09-15
updated: 2026-09-15
confidence: medium
---

# Apple SiliconでのFP8モデル実行対策：BF16とGGUFのワークアラウンド

## 結論

Apple SiliconではFP8（float8_e4m3fn）形式のモデルが動作しない問題は、MPSバックエンドが該形式をサポートしていないための技術的制約であり、FLUX.2やKrea 2 Turbo、Wan 2.2などのモデルではBF16への置き換えやGGUF形式への変換が必須のワークアラウンドとなる。GGUF形式はLLMの世界で生まれた技術だが、ComfyUI-GGUFを介して画像生成モデルでも利用可能であり、Apple Siliconでの実行環境を確保するための現実的な選択肢として位置づけられている。

## テーマ概要

Apple Silicon向けのFP8（float8_e4m3fn）モデルの実行において、型定義がされていないエラー「Undefined type Float8_e4m3fn」が発生している問題が注目されている。この問題は、Apple SiliconのMPSバックエンドがFP8形式をサポートしていないため、FP8で量子化されたモデルをロードする際に起る。特に、FLUX.2やKrea 2 Turboなどの画像生成モデルでは、BF16形式への変換やGGUF形式への変換によるワークアラウンドが求められている。また、Wan 2.2などのモデルでは、GGUF形式を採用することでApple Siliconでの実行が可能となっている。この問題は、Apple Siliconのハードウェア制限とFP8形式の互換性が原因であり、ユーザーがモデルの実行環境を調整する必要があるため、現在のAIモデルの実行環境において重要な課題となっている。

## 共通して確認できる点

FP8（float8_e4m3fn）はNVIDIA GPU向けの量子化形式であり、Apple SiliconのMPSバックエンドではサポートされていないため、FP8で量子化されたモデルをロードしようとすると「Undefined type Float8_e4m3fn」というエラーが発生する。この問題はApple Siliconマシンで動作する際の主要な障害となる。実際、FLUX.2やKrea 2 TurboといったFP8モデルは、Apple Siliconで動作しなかった。FLUX.2はBF16形式に変更することで動作を確保し、Krea 2 TurboはGGUF形式の構築（Q6_K）とローダーのパッチを適用することで解決した。また、Wan 2.2もFP8では動作しないため、GGUF形式で実行する必要があった。GGUFはLLMの世界で生まれた量子化形式だが、ComfyUI-GGUFを通じて画像生成モデルにも適用可能である。BF16形式はFP8よりファイルサイズが大きいが、32GBの統合メモリを持つマシンでは運用可能である。Qwen 3.8 27BのGGUFファイルは2026年8月にリリースされ、さまざまな量子化レベルが提供されており、llama.cppやOllamaとの互換性も確認されている。これらはApple Siliconでの動作を確保するための有効なワークアラウンドとなる。

## 記事ごとの差分・視点の違い

記事「Undefined type Float8_e4m3fn on Apple Silicon: BF16 and GGUF Workarounds for FP8 Models」は、Apple Silicon向けにFP8モデルが動作しない問題とその対処法を実例ベースで紹介している。この記事では、FLUX.2とKrea 2 Turboという2つのモデルがFP8形式で動作せず、それぞれBF16への置き換えとGGUF形式への変換という異なるワークアラウンドを採用した経緯を詳述している。また、GGUF形式の導入がMac向けに実用的な選択肢であることを強調している。

記事「LTX-2 vs Wan 2.2 on M1 Max 64GB: FP8 fails on Metal, GGUF Wan...」は、Apple SiliconでのFP8実行不可の問題を前提に、LTX-2とWan 2.2という2つのモデルの性能比較と実行環境における課題を論じている。Wan 2.2はGGUF形式での実行が可能であるが、生成時間の長さが課題であり、M1 Max 64GBでも82分かかるという現状を指摘している。また、GGUF形式の導入にはComfyUI-GGUFの導入が必要である点も強調している。

記事「BDH-CQ Uses Recurrent Latent Reasoning to Cut ARC-AGI Inference Costs」は、FP8に関する技術的課題とは異なる視点で、視覚的推論タスクにおける大規模言語モデルの不適切さと、BDH-CQという新しいモデルのコスト効率性を論じている。この記事では、モデルが内部のメモリ状態にデモンストレーションを吸収し、中間推論トークンを生成せずに問題を解決する仕組みを説明し、ARC-AGI-1ベンチマークでの性能とコスト効率の改善点を示している。

記事「Paper page - BDH-CQ: In-Context Learning with Recurrent Latent...」は、BDH-CQモデルの技術的な詳細を論文形式でまとめている。この論文では、モデルがインコンテキスト学習と再帰的な潜在空間の推論を組み合わせることで、ARC-AGI-1ベンチマークでのコストと精度のトレードオフを改善していることを示し、150Mパラメータの設定で29.5% pass@2の結果を達成している。また、論文では実験の再現性や他のモデルとの比較が不足している点も指摘されている。

記事「Paper page - Macaron-V1: Towards Open Continual Learning with Self-Improvement and Mixture-of-LoRA」は、FP8やGGUFといった量化形式とは関係のない、継続学習と自己改善をテーマにしたモデルについて論じている。この論文では、Macaron-V1というオープンなエージェントモデルファミリーや、Mixture-of-LoRAアーキテクチャ、再帰的な自己改善を用いた継続学習の実現について述べており、FP8やGGUFの技術的課題とは別系統の技術的進展を提示している。

## 深掘り調査で得られた知見

FP8（float8_e4m3fn）はNVIDIA GPU向けの量子化形式であり、Apple SiliconのMPSバックエンドではサポートされていないため、FP8で量子化されたモデルをロードすると「Undefined type Float8_e4m3fn」というエラーが発生する。この問題は、FLUX.2やKrea 2 Turboなどの画像生成モデルで確認され、それぞれ異なる対応策が求められた。FLUX.2ではBF16形式への切り替えにより解決され、Krea 2 TurboではGGUF形式のビルドとローダーのパッチを組み合わせた対応が行われた。また、Wan 2.2もFP8では動作しないため、GGUF形式を採用する必要があった。GGUFはLLM世界で生まれた量子化形式だが、ComfyUI-GGUFを介して画像生成モデルにも適用可能である。Apple SiliconではFP8が使えないため、GGUFはファイルサイズを抑えながらも動作を確保するための現実的なワークアラウンドとなる。Qwen 3.8 27BのGGUFファイルは2026年8月にリリースされ、さまざまな量子化レベルが提供されており、llama.cppやOllamaとの互換性も確認されている。これらの情報は、Apple SiliconでのFP8モデルの実行に向けた技術的対応策を示す重要な指針となる。

## 不確実な点・追加確認が必要な点

記事間の食い違いや、資料からは断定できない点を具体的に書く。  

記事1と記事2の内容は、FP8形式がApple Silicon上で動作しないという点では一致しているが、具体的な対応策や背景に違いがある。記事1では、FLUX.2とKrea 2 Turboという2つのモデルがFP8形式で起動時にエラーを発生し、それぞれBF16形式への置き換えやGGUF形式への変換という異なる対応策を取ったことが記載されている。一方、記事2では、Wan 2.2モデルがFP8形式では動作せず、GGUF形式での実行が必須であると説明されており、BF16への置き換えは推奨されていない。これは、モデルごとの実行環境や対応可能な形式に違いがある可能性を示唆している。  

また、記事1では、GGUF形式のモデルがComfyUI-GGUFプラグインを介して動作可能であることが明記されているが、記事2では、GGUF形式のモデルをComfyUI標準のローダーで読み込むことができず、カスタムノードの導入が必要であると説明されている。これにより、GGUF形式のモデルを動作させるための環境設定や構成の違いが生じている可能性がある。  

さらに、記事4と記事5は、FP8形式との関連性は薄く、主にモデルの構造や学習方法に関する技術的詳細を提供している。記事4では、BDH-CQモデルがFP8形式とは関係なく、再帰的な潜在空間での論理処理を用いてコスト効率を向上させていると述べられている。一方、記事5では、Macaron-V1モデルがLoRAアーキテクチャと自己改善機能を活用した継続学習を可能にしていると説明されている。これらは、FP8形式の問題とは直接関係はないが、Apple Siliconでのモデル実行に影響を与える技術的背景として考慮する必要がある。  

したがって、FP8形式がApple Siliconで動作しない問題に対しては、モデルごとに異なる対応策が求められ、GGUF形式やBF16形式の選択はモデルの特性や実行環境に依存する可能性が高い。また、GGUF形式の実行にはComfyUIの拡張機能や特定の設定が不可欠であるため、環境構築の手間が増えるという課題も存在する。

## 元記事一覧

- [UndefinedtypeFloat8_e4m3fnonAppleSilicon:BF16andGGUF...](https://dev.to/acs_developer/undefined-type-float8e4m3fn-on-apple-silicon-bf16-and-gguf-workarounds-for-fp8-models-7oj)
- [LTX-2 vs Wan 2.2 on M1 Max 64GB:FP8fails on Metal,GGUFWan...](https://lilting.ch/en/articles/ltx2-wan22-mac-local-video-gen)
- [BDH-CQUsesRecurrentLatentReasoningtoCutARC-AGI...](https://dev.to/aimodels-fyi/bdh-cq-uses-recurrent-latent-reasoning-to-cut-arc-agi-inference-costs-2hk7)
- [Paper page -BDH-CQ: In-Context Learning withRecurrentLatent...](https://huggingface.co/papers/2608.09888)
- [Paper page - Macaron-V1: Towards Open Continual Learning with Self-Improvement and Mixture-of-LoRA](https://huggingface.co/papers/2608.09819)
