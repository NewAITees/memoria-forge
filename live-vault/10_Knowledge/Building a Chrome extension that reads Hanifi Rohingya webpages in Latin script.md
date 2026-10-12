---
title: Chrome拡張でHanifi Rohingyaをラテン文字に変換する技術
type: knowledge
status: draft
created: 2026-10-13
updated: 2026-10-13
confidence: medium
---

# Chrome拡張でHanifi Rohingyaをラテン文字に変換する技術

## 結論

Rohingya Reader拡張機能は、Hanifi Rohingya文字をラテン文字に即時変換するための技術的実装として、ページの機能を破壊することなくローカルで動作し、逆変換を可能にする設計が特徴です。また、この拡張機能はUnicode標準に採用されたHanifi Rohingya文字を扱うための信頼性の高い変換器を使用しており、オンラインツールと同一の処理をローカルで実現しています。

## テーマ概要

Rohingya言語は、ハニフィ・ロヒンギャスクリプト、アラビア語ベースのロヒンギャアルファベット、およびラテンアルファベットの3つの文字体系で書かれる。このうち、ハニフィ・ロヒンギャスクリプトは2018年6月にUnicode標準に採用され、U+10D00–U+10D3Fのブロックで表される。一方で、ラテンアルファベットを用いたロヒンギャスクリプト（ロヒンギャリッシュ）は、多くのロヒンギャ話者が読みやすいが、一部の話者にとってはハニフィスクリプトの読み書きが困難である。このような背景から、Chrome拡張機能「Rohingya Reader」が開発され、ウェブページ上のハニフィテキストをラテンアルファベットに変換する機能を提供している。この拡張機能は、ページの機能を破壊することなく、ローカルで動作し、逆変換を可能にするなど、厳格な要件を満たしている。また、このテーマは、ロヒンギャ言語の多様な文字体系を扱う技術的な課題と、それを解決するためのオープンソースツールや拡張機能の開発が注目されている点が背景にある。

## 共通して確認できる点

Hanifi Rohingya スクリプトは、ロヒンギャ語を書くための統一された文字体系であり、Unicode標準に2018年6月に採用されました（バージョン11.0でブロックU+10D00–U+10D3Fとして）。ロヒンギャ語は現在、Hanifi Rohingya、アラビア文字ベースのロヒンギャアラビア文字、およびラテン文字ベースの Rohingyalish の3つの文字体系で書かれています。Hanifi Rohingya は右から左へ書く方向性を持ち、すべての母音は独立した文字として表記されますが、常に子音と結びついて使用されるため、母音同士の組み合わせによるダイフチョンはできません。また、トーンマーカーは母音の上に置かれるディアクリティクスとして表示されます。このスクリプトは、ロヒンギャ語の読み書きを容易にするために、Googleによって2019年に仮想キーボードとして開発されました。また、Hanifi Rohingya と Rohingyalish の相互変換を行うためのツールとして、オンラインツールやChrome拡張機能が存在しており、ウェブページ上でHanifiテキストをラテン文字に変換する機能を提供しています。

## 記事ごとの差分・視点の違い

記事「Hanifi Rohingya script - Wikipedia」は、Hanifi Rohingya文字の歴史的背景とUnicodeへの採用について説明しており、Rohingya言語の現状を理解するための基礎知識を提供しています。一方、「Building a Chrome extension that reads Hanifi Rohingya webpages in Latin script」は、実際の技術的課題と解決策に焦点を当てており、Chrome拡張機能の開発プロセスやその技術的工夫を詳細に説明しています。また、「Translating a content app into 46 languages without a translation API」は、翻訳のコストと品質のトレードオフについて議論し、オープンソースの翻訳モデルを用いたオフライン翻訳の実装方法を紹介しています。これらの記事はそれぞれ異なる視点から、Rohingya言語の文字体系やその処理に関連する技術的課題を扱っており、それぞれの目的や対象読者層が異なっています。

## 深掘り調査で得られた知見

Hanifi Rohingyaは、ロヒンギャ語を書くための右から左への文字体系であり、Unicode標準に2018年6月に採用されました（バージョン11.0、ブロックU+10D00–U+10D3F）。ロヒンギャ語は、アラビア文字、ラテン文字（ロヒンギャリッシュ）の3つの文字体系で書かれています。多くのロヒンギャ話者はラテン文字を読むことに慣れているが、Hanifi文字には苦労する傾向があります。この問題に対処するため、Chrome拡張機能「Rohingya Reader」が開発されました。この拡張機能は、ユーザーが読んでいるページ内のHanifi文字を、ロヒンギャリッシュに即時変換します。変換はローカルで行われ、バックエンドやAPI、分析機能を必要とせず、ページの機能を破壊することなく動作します。変換結果は元のテキストに戻すことが可能で、ウェブサイトのテキストが変更された場合でも、その最新版が優先されます。この拡張機能はChrome Web Storeで審査中で、今後公開予定です。また、この拡張機能は、オンラインツール、そのツールは少なくとも2019年から利用可能となっています。

## 不確実な点・追加確認が必要な点

記事間の食い違いや、資料からは断定できない点を具体的に書くと、以下の通りです。

まず、Hanifi Rohingya文字のUnicode採用について、記事1と記事2で共通して言及されています。記事1では、Hanifi RohingyaがUnicode標準に2018年6月に採用されたと明記されており、記事2でも同様の情報が含まれています。ただし、記事1では具体的なUnicodeブロック（U+10D00–U+10D3F）が記載されており、記事2ではその記載がありません。このため、記事2ではUnicodeブロックの情報が断定できません。

また、Chrome拡張の開発に関する記事2では、Rohingya Reader拡張の開発が行われていることや、その動作仕様（例：text nodeの処理、MutationObserverの使用など）が詳細に記載されています。一方、記事1では、オンラインツールのURL（）が記載されており、そのツールがRohingya Reader拡張で使用されていることが示されていますが、記事2ではそのツールの存在が明記されていません。このため、記事2ではオンラインツールの存在を断定できません。

さらに、記事5では、46言語への翻訳に際して、商用翻訳APIを避けてオープンソースモデルを使用した経験が紹介されていますが、これはRohingya文字の扱いとは直接関係ありません。したがって、Rohingya Reader拡張の開発と翻訳APIの選択肢との関連性は明確ではありません。

最後に、記事4は、Keys.soのアカウント登録ページであり、Rohingya文字やChrome拡張とは関係がありません。したがって、この記事は本テーマと直接的な関連性を持たないことが確認されています。

## 元記事一覧

- [HanifiRohingyascript- Wikipedia](https://en.wikipedia.org/wiki/Hanifi_Rohingya_script)
- [Building aChromeextensionthatreadsHanifiRohingyawebpages...](https://dev.to/abaziz/building-a-chrome-extension-that-reads-hanifi-rohingya-webpages-in-latin-script-35e1)
- [Thesaurus.plus - Online Thesaurus Dictionary of the English language](https://thesaurus.plus/)
- [Cоздайте аккаунт для работы с сервисомKeys.so](https://www.keys.so/ru/registration)
- [Translating a content app into 46 languages without a ...](https://dev.to/dizijpg/translating-a-content-app-into-46-languages-without-a-translation-api-bill-34a1)
