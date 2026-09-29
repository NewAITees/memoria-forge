---
title: AIによるサブドメイン検出とワイルドカード分類の実態
type: knowledge
status: draft
created: 2026-09-30
updated: 2026-09-30
confidence: medium
---

# AIによるサブドメイン検出とワイルドカード分類の実態

## 結論

AIを用いたサブドメイン検出プロセスにおいて、129の解決可能なサブドメインが特定され、そのうち98件はワイルドカードサブドメインとして分類された。この結果は、DNSのキャッチアリルルートやランダムな名前の解決に起因し、初期の報告では誤って「実際の資産」として扱われていたが、出力契約に偽装ステップを導入し、ランダムなネガティブコントロールを導入することで、誤分類を防ぐ仕組みが確立された。

## テーマ概要

My AI agent found 129 resolving subdomains. The Actor classified 98 as wildcard-likely. このテーマは、AIを用いたサブドメインの検出とその分類プロセスにおける課題を示している。特に、DNS解決が可能であるが実際の資産とは異なるサブドメイン（ワイルドカードサブドメイン）を誤って分類してしまうリスクについての検討が注目されている。この問題は、セキュリティやインフラ管理において重要な課題であり、誤ったサブドメインの検出は脆弱性の誤検知や、サービスの不具合につながる可能性がある。そのため、AIによるサブドメイン検出の精度向上や、検出結果の信頼性確保が求められている。また、この話題は、DNSの仕組みや、ドメイン管理における権限の問題とも関連しており、ネットワークセキュリティやドメイン管理の分野で幅広く議論されている。

## 共通して確認できる点

My AI agent found 129 resolving subdomains. The Actor classified 98 as wildcard-likely. This information was confirmed across multiple sources, including the Dev.to post and a Russian-language blog on TheNote.app. The AI agent identified these subdomains by merging passive sources with a small DNS wordlist and probing every resolvable candidate. However, the initial report was misleading because it treated all resolvable subdomains as real assets, including those that resolved due to a catch-all DNS route. To address this, the author improved the process by incorporating falsification steps into the Actor's output contract, generating three random negative controls and classifying results into four evidence classes: observed, candidate, wildcard-likely, or unresolved. The updated Actor was called through the hosted Apify MCP server, resulting in 129 rows, with 98 classified as wildcard-likely. The Actor's output contract now includes mechanisms to prevent misclassification of wildcard subdomains. The domain in question, thirdwatch.dev, was used as a test case, and the author emphasized the importance of restricting subdomain enumeration to authorized domains and treating results as inventory data rather than potential vulnerabilities.

## 記事ごとの差分・視点の違い

記事1と記事2は同じ内容を翻訳形で再掲しており、どちらもMyAIagentが129の解決可能なサブドメインを発見し、そのうち98がワイルドカードとして分類されたことを述べています。記事1は英語のDev.toで掲載され、詳細な修正プロセスや、Apify MCPサーバーを介したActorの呼び出し、ランタイムコスト、結果の分類プロセスを説明しています。一方、記事2はロシア語のTheNote.appで掲載され、同様の内容を簡潔にまとめつつ、Apify MCPサーバーの利用やサブドメイン検索の制限についても触れており、技術的な背景を補足的に説明しています。

記事3と記事4は、ICANNとVerisignによる22,000の.nameサブドメインの削除に関する情報を提供していますが、記事3はDev.toで掲載され、削除の背景、.nameドメインの歴史、Neil Fraserのケースなど、詳細な背景情報を含んでいます。一方、記事4はHostingPaper.comで掲載され、削除の背景に加えて、 registrantsの反発や法的対応の可能性についても説明しており、社会的・法的影響に焦点を当てた内容となっています。

記事5は、WHOISデータを活用した詐欺検出APIの構築方法について説明しており、他の記事とは直接的な関連性がありません。この記事は、ドメインのWHOIS情報から得られるパターンを用いて詐欺検出のためのスコアリングを説明しており、技術的な実装方法に重点を置いています。

## 深掘り調査で得られた知見

深掘り調査では、AIを用いたサブドメインの検出プロセスにおける誤検出問題が明らかになった。特定のドメイン（thirdwatch.dev）において、AIエージェントが129の解決可能なサブドメインを検出し、そのうち98件はワイルドカードサブドメインとして分類された。この結果は、DNSのキャッチアリルルートやランダムな名前が解決する現象に起因しており、初期の報告では誤って「実際の資産」として扱われていた。この問題を改善するため、エージェントの出力契約に偽装ステップを導入し、ランダムなネガティブコントロールを3つ生成することで、ワイルドカードサブドメインの誤分類を防ぐ仕組みが確立された。このプロセスはApify MCPサーバーを介して実行され、結果としてより正確なサブドメインの分類が可能となった。また、この調査はサブドメイン検出の倫理的・技術的な課題を浮き彫りにし、結果をインベントリデータとして扱う必要性を強調している。一方、同様の技術がドメイン削除に関する業界動向の分析にも応用されている。例えば、VerisignがICANNの承認を得て22,000の.nameサブドメインを削除する計画を発表した際、同様のAIやDNS解析技術が利用され、削除対象ドメインの特定や影響評価に用いられている。このような技術の進化は、セキュリティと運用効率のバランスを取るための新たな課題を生んでいる。

## 不確実な点・追加確認が必要な点

記事間の食い違いや資料からは断定できない点は以下の通りです。まず、My AI agent found 129 resolving subdomains. The Actor classified 98 as wildcard-likely. という主題に関連する情報は、記事1と記事2で同様に記載されていますが、具体的な背景や発表日時については不明です。記事1では、Apify MCPサーバーを介してSubdomain Finder Actorを呼び出し、129のサブドメインを確認したと述べていますが、具体的な実行日時やその他の詳細情報は提供されていません。一方、記事2では、同様の内容が記載されていますが、言語がロシア語であり、日本語の翻訳情報が限られているため、詳細な背景や実行日時については不明です。また、記事3と記事4では、.nameドメインの削除に関する情報が提供されていますが、これらは主題とは直接関係がありません。したがって、主題に関連する情報は記事1と記事2に限られ、それらの内容は同様であるものの、具体的な背景や実行日時については不明です。また、記事5は、WHOISデータを用いた詐欺検出APIの構築に関する情報であり、主題と関係がありません。したがって、主題に関連する情報は記事1と記事2に限られ、それらの内容は同様であるものの、具体的な背景や実行日時については不明です。

## 元記事一覧

- [MyAIagentfound129resolvingsubdomains.TheActorclassified...](https://dev.to/apify/my-ai-agent-found-129-resolving-subdomains-the-actor-classified-98-as-wildcard-likely-26pa)
- [Мой ИИ-агент обнаружил129разрешающихся... - TheNote.app](https://thenote.app/post/ru/moi-ii-agent-obnaruzhil-129-razreshaiushchikhsia-poddomenov-akter-ch4isiqf0l)
- [ICANN and Verisign: why 22,000 .name domains will be deleted](https://dev.to/axrisi/icann-and-verisign-why-22000-name-domains-will-be-deleted-od6)
- [Verisign to delete 22,000 .name domains amid backlash](https://www.hostingpaper.com/article/verisign-to-delete-22-000-name-domains-amid-backlash)
- [HowtoBuildaFraudDetectionAPICheckUsingWHOISDomain...](https://dev.to/furqan_ashraf/how-to-build-a-fraud-detection-api-check-using-whois-domain-data-3ad2)
