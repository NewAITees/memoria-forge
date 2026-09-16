---
title: C++23でstd::moveを使わないムーブの仕組み
type: knowledge
status: draft
created: 2026-09-16
updated: 2026-09-16
confidence: medium
---

# C++23でstd::moveを使わないムーブの仕組み

## 結論

C++23では、特定のケースにおいて`std::move`を明示的に使用する必要がなくなった。これは、RVO（Return Value Optimization）やNRVO（Named Return Value Optimization）によるコピーとムーブの自動最適化、およびC++23で導入された暗黙的なムーブの仕様が原因であり、パフォーマンス最適化を重視する開発者にとって重要な変化をもたらしている。

## テーマ概要

C++において、`std::move`を明示的に使用しないでムーブ semantics を実現する方法が注目を集めている。これは、C++23の導入により、特定のケースで暗黙的なムーブが行われるようになったためである。例えば、関数が rval reference を受け取り、そのオブジェクトを返す場合、`std::move`を明示的に書く必要がなくなった。これは、RVO（Return Value Optimization）やNRVO（Named Return Value Optimization）によるコピーの省略と、C++23で導入された暗黙的なムーブの仕様によるものである。この傾向は、パフォーマンス最適化を重視する開発者にとって重要な変化であり、`std::move`の使用頻度を減らすことを推奨している。また、このテーマは、C++の進化に伴う最適化技術の変化を反映しており、今後の開発において重要な役割を果たしうる。

## 共通して確認できる点

C++23では、特定のケースにおいて`std::move`を明示的に使用する必要がなくなることが確認されている。Andreas Fertigのブログでは、C++23モードに切り替えることで、関数の返却値に対して暗黙的なムーブが行われるとしており、これはRVO（Return Value Optimization）やNRVO（Named Return Value Optimization）による最適化の結果である。RVOでは、関数内で返されるオブジェクトが呼び出し側で作成されるため、コピーとムーブが省略される。NRVOでは、名前付きの返却値の最適化が行われるが、コピーが行われる可能性がある。C++23では、これらの最適化により、`std::move`を明示的に書く必要がなくなった。また、Hacker Newsのコメントでは、C++における性能最適化に関する議論が行われており、`std::move`の使用頻度についての議論がされている。

## 記事ごとの差分・視点の違い

記事ごとの差分・視点の違いは、それぞれの著者やプラットフォームの特性に応じて異なっている。Andreas Fertigのブログでは、C++23におけるstd::moveの不要性と、RVO、NRVOによる最適化の重要性が強調されている。これは、パフォーマンス最適化に重点を置いた技術的な視点からのアプローチである。一方、Hacker Newsのコメントでは、C++の性能最適化に関する議論が行われており、標準ライブラリの自動生成による深コピーのコストや、カスタムコンストラクタ・代入演算子の定義の必要性が論じられている。この視点は、より広い開発者コミュニティの意見を反映しており、技術的な深みと実践的な観点が混在している。また、XとBest CAD papersの記事では、WebAssemblyの統合に1年間の開発期間が費やされたという事実が伝えられており、技術的課題や開発プロセスの複雑さが強調されている。これは、実際のプロジェクトにおける技術的困難とその影響を示す実例としての視点である。最後に、arXivの論文では、C⋆という言語設計が紹介され、プログラミングと検証の統合についての理論的アプローチが説明されている。この視点は、形式的検証の重要性と、その実装における技術的挑戦を論じる学術的な視点を提供している。

## 深掘り調査で得られた知見

C++23では、特定のケースにおいて`std::move`を明示的に書く必要がなくなったという情報が確認されている。Andreas Fertigのブログでは、C++23モードに切り替えることで、関数内で返されるオブジェクトがスタック上ではなく、呼び出し側で作成されるため、コピーとムーブが省略されることが示されている。これはRVO（Return Value Optimization）とNRVO（Named Return Value Optimization）による最適化の結果であり、`std::move`を明示的に使用する必要がなくなる。また、`std::move`はコピーを避けるためのキャストであり、実際のムーブ操作はムーブコンストラクタやムーブ代入演算子によって行われる。このように、C++23では、いくつかのケースで暗黙的なムーブが行われるため、`std::move`を明示的に書く必要がなくなる。WebAssemblyの統合には1年間の開発期間が費やされ、Anubisプラットフォームにおける統合には、数百のコミット、5世代のプルリクエスト、数十のテスト、Rustでのコード再実装など、多くの技術的課題が伴った。また、C⋆（C star）は、C言語におけるプログラミングと検証を統合した言語設計であり、形式的検証を実現するためのツールとして注目されている。

## 不確実な点・追加確認が必要な点

記事間の食い違いや、資料からは断定できない点を具体的に書く。  
まず、Move in C++ without a std::moveというテーマは、C++のムーブ semanticsに関する最適化技術についての議論であり、特にC++23における変化が注目されている。Andreas Fertigのブログでは、C++23モードに切り替えることで、特定のケースでstd::moveを明示的に書く必要がなくなることが示されている。これは、RVO（Return Value Optimization）やNRVO（Named Return Value Optimization）によるコピーとムーブの自動最適化が原因である。しかし、Hacker Newsのコメントでは、C++の性能最適化に関する議論が行われており、std::moveの使用頻度や、コピーを避けるための最適な方法についての議論がされている。  

一方で、WebAssemblyの統合に1年間の開発期間が費やされたという情報は、複数のソースで一致している。Hacker NewsのコメントやBest CAD papersの記事によれば、AnubisプラットフォームにおけるWebAssemblyの統合には、数百のコミットや5世代のプルリクエスト、数十のテスト、Rustでのコード再実装が必要だったとされている。これらの情報は、WebAssemblyの統合における技術的複雑さを示しているが、具体的な技術的課題や解決策については詳しくは記載されていない。  

また、C⋆（C star）に関する論文では、C++のプログラミングと検証を統合するための言語設計が提案されている。この論文では、C⋆が実装され、小規模なCプログラムや実際のケーススタディ（pKVMの buddy allocatorの attach関数）で評価されているとされている。しかし、C⋆の具体的な実装や、今後の展開については、論文内では詳しく説明されていない。  

以上のように、各記事は異なるテーマや焦点をもっており、Move in C++ without a std::moveに関する議論は、C++の最適化技術に限らず、WebAssemblyの統合やC⋆の開発など、広範な技術的背景を含んでいる。これらの情報は、それぞれ独立して検討される必要があるが、統合的な視点から見ると、C++の最適化技術が現代のソフトウェア開発において重要な役割を果たしていることが示唆されている。

## 元記事一覧

- [Move in C++ without a std::move - Andreas Fertig's Blog](https://andreasfertig.com/blog/2026/09/move-in-cpp-without-a-stdmove/)
- [MoveinC++withoutastd:move| Hacker News](https://web.archive.org/web/20260904101025/https://news.ycombinator.com/item?id=49521590)
- [Hacker News 20 on X: "It took a year to ship WebAssembly in Anubis  ()" / X](https://x.com/betterhn20/status/2096786532812083500)
- [It Took A Year To Ship WebAssembly In Anubis - Best CAD papers](https://bestcadpapers.com/art-and-society/it-took-a-year-to-ship-webassembly-in-anubis/)
- [[2504.02246]C*:UnifyingProgrammingandVerificationinC](https://arxiv.org/abs/2504.02246)
