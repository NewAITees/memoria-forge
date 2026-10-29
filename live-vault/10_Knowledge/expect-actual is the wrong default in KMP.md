---
title: KMPにおけるexpect-actualのデフォルトとしての不適切性
type: knowledge
status: draft
created: 2026-10-29
updated: 2026-10-29
confidence: medium
---

# KMPにおけるexpect-actualのデフォルトとしての不適切性

## 何が分かったか

expect / actualは特定の用途には有効だが、一般的なデフォルトとして適切ではない [^fact-bd3a13bd89620ab7]。各プラットフォームで実装を提供し、DIグラフを通じて渡すことで、共通コードがインターフェースに依存しテスト可能になる [^fact-4d86c49b2df0f554]。KMPの主な課題は共通コードに何を渡すかであり、プラットフォームボディをインジェクトする方式が推奨される [^fact-c8c1d0035d779163]

## 確認できた事実

- expect / actualは狭い用途に適した良いツールであるが、ほとんどのケースでは適切なデフォルトではない。 [^fact-bd3a13bd89620ab7]

- 各プラットフォームごとに実際のものを提供し、DIグラフ（我々の場合はKoin）を通して渡す: 同じプラットフォームボディ。同じ挙動。しかし、共通コードは所有するインターフェースに依存し、プラットフォーム宣言ではなく、テストもワンラインで可能になる。 [^fact-4d86c49b2df0f554]

- KMPの質問は「どうやってプラットフォームにアクセスするか」ではなく、「共通コードに何を渡すか」である。所有するインターフェースを渡し、プラットフォームボディをインジェクトする。実際のところだけにweldを用いるためにexpect / actualを残す。 [^fact-c8c1d0035d779163]

## それが意味すること

インターフェースベースのアプローチはプラットフォームの依存を減らし、テスト性を高める可能性がある。 [^fact-4d86c49b2df0f554] [^fact-c8c1d0035d779163]

## まだ分からないこと

expect / actualの具体的な利点や、他のアプローチとの比較は、提供された情報では明示されていない。

## 出典

[^fact-bd3a13bd89620ab7]: [expect/actualisthewrongdefaultinKMP- DEV Community](https://dev.to/darkpandawarrior/expectactual-is-the-wrong-default-in-kmp-5g7p)
  - 根拠引用: 「expect / actual is a fine tool for a narrow job, and the wrong default for most of them.」
[^fact-4d86c49b2df0f554]: [expect/actualisthewrongdefaultinKMP- DEV Community](https://dev.to/darkpandawarrior/expectactual-is-the-wrong-default-in-kmp-5g7p)
  - 根拠引用: 「Provide the real thing per platform, and hand it in through your DI graph (Koin, in our case): Same platform bodies. Same behavior. But now the common code depends on an interface it owns, not on a platform declaration, and it is testable in one line.」
[^fact-c8c1d0035d779163]: [expect/actualisthewrongdefaultinKMP- DEV Community](https://dev.to/darkpandawarrior/expectactual-is-the-wrong-default-in-kmp-5g7p)
  - 根拠引用: 「The KMP question is rarely "how do I reach the platform." It is "what do I hand my common code." Hand it an interface it owns, and inject the platform body. Keep expect / actual for the handful of places you actually want a weld.」
