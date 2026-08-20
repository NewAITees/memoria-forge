---
type: knowledge
status: draft
created: 2026-08-13
updated: 2026-08-13
confidence: medium
---

+++ 
created: 2026-08-13
updated: 2026-08-13
+++ 
# When Chain-of-Thought Helps and When It Hurts: An Empirical Investigation of the Serial-Depth Bottleneck in LLM Reasoning

## 概要
この研究は、チェーン・オブ・サウンド（CoT）プロンプティングがLLMの推論能力を普遍的に向上させるかどうかを検証する。CoTは、シリアル深度がトランスフォーマーの単一フォワードパス容量を超える場合に有効であり、その効果はタスクの深さに依存する。研究は、H_dp帯域幅制限の枠組みに基づき、LLMが単一パスで解決可能な問題と解決不可能な問題を区別する可能性を示唆している。

## 詳細
- **CoTの効果**: CoTは、シリアル深度が深いタスク（例: GSM8K, MATH）において、精度を大幅に向上させる（+54〜+68ポイント）。これに対して、浅いタスク（例: MMLU）では効果が限定的。
- **帯域幅制限**: トランスフォーマーの単一フォワードパス容量を超える問題では、CoTが有効。これは、LLMが複数のステップで推論を行う必要があるため。
- **LLMの制限**: CoTが常に推論の過程を正確に反映しない。Anthropicの研究では、モデルがヒントを無視して思考を生成することが確認されている。
- **自動生成**: Auto-CoTは、LLMを用いて推論チェーンを自動生成し、手動の努力を削減する。ただし、生成されたチェーンには誤りが含まれる可能性がある。

## 未解決の問題
- CoTが推論の過程を完全に反映するかどうか。
- モデルがヒントを無視する理由。
- CoTを用いた推論の信頼性。

## 背景
- CoTプロンプティングは、LLMの推論能力を向上させるための手法として広く採用されている。
- しかし、CoTが常に推論の過程を正確に反映するとは限らない。
- 研究は、LLMが単一フォワードパスで解決可能な問題と解決不可能な問題を区別する可能性を示唆している。

## 結論
CoTは、シリアル深度が深いタスクにおいて有効だが、浅いタスクでは効果が限定的。研究は、LLMが単一フォワードパスで解決可能な問題と解決不可能な問題を区別する可能性を示唆し、CoTプロンプティングの限界と可能性を明らかにしている。

## 出典

- [WhenChain-of-ThoughtHelpsandWhenItHurts:AnEmpirical...](https://arxiv.org/html/2608.09942)
- [[2608.09942]WhenChain-of-ThoughtHelpsandWhenItHurts:An...](https://arxiv.org/abs/2608.09942)
- [tandfonline.com/doi/abs/10.1080/713665670](https://www.tandfonline.com/doi/abs/10.1080/713665670)
- [Chain-of-ThoughtPrompting | Prompt Engineering Guide](https://www.promptingguide.ai/techniques/cot)
- [Anthropic FindsChain-of-ThoughtReasoningTraces May Omit Key...](https://www.deeplearning.ai/the-batch/anthropic-finds-chain-of-thought-reasoning-traces-may-omit-key-influences)

## 未解決点

