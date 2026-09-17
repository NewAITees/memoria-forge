---
title: ハッカーが1年間ID検証企業のスキャンデータをリアルタイムで公開していた
type: knowledge
status: draft
created: 2026-09-17
updated: 2026-09-17
confidence: medium
---

# ハッカーが1年間ID検証企業のスキャンデータをリアルタイムで公開していた

## 結論

ID verification companiesが1年以上にわたって、ID検証プロセスで生成されたドキュメントスキャンデータをハッカーにリアルタイムで公開していたという事実が確認された。このライブフィードは、パスポートや運転免許証などの個人情報を含み、長期間の情報漏洩が発覚するまでに時間がかかった。この事件は、ID検証システムの信頼性に深刻な疑問を投げかけ、技術的脆弱性が社会的なリスクとして顕在化していることを示している。

## テーマ概要

ID verification companies were found to have exposed a live feed of every scanned document to hackers for over a year. This incident involved streaming real-time ID scans, including passports and driver's licenses, to attackers, allowing them to view sensitive data continuously. The flaw was not discovered for more than a year, leading to prolonged exposure of sensitive information. This breach highlights the vulnerabilities in the identity verification industry, where the tools designed to prevent fraud became targets for attacks. The incident was widely discussed in tech communities, with sources indicating that a company spent over a year leaking 150 million driver's licenses in real time. However, it remains unclear how the flaw was discovered or how many documents were exposed before the breach was closed. This exposure of sensitive data underscores the risks associated with the current state of identity verification systems, where the very tools meant to secure user data can be exploited by malicious actors. The incident is linked to the article titled "Hackers Had a Live Feed of Every ID This Verification Company Scanned for over a Year," published on TechDirt on September 3, 2026.

## 共通して確認できる点

複数の記事で共通して確認できた事実として、ID verification companiesがIDの検証プロセスで生じたデータの漏洩が長期間にわたって発覚しなかった点が挙げられる。これは、ID検証を目的としたシステムが、本来は個人情報を保護するためのものであるにもかかわらず、逆に悪意のある第三者にデータをリアルタイムで提供する形で漏洩した事例である。また、この類似の問題は、不正アクセスやセキュリティの脆弱性によって引き起こされることがあり、特に不動産業界やリアルタイムでのデータ処理が行われる分野では、セキュリティの欠陥が深刻な影響を及ぼす可能性がある。さらに、AI技術の進展によって、公共サービスへの申請や苦情の増加が観測されていることから、技術の進化が社会インフラにも新たな課題をもたらしていることが確認されている。

## 記事ごとの差分・視点の違い

記事「Hackers Had a Live Feed of Every ID Verification Company Scanned for over a Year」は、ID検証企業がハッカーにリアルタイムでドキュメントスキャンをライブストリームしていたという事実を報告しており、情報漏洩の長期化とその影響を強調している。一方、「ThecarindustryA/Btestedselling acarwithandwithoutCarPlay」は、カーペラの導入が車の売上に与える影響をA/Bテストを通じて評価した結果を提示し、技術統合が消費者選択に与える影響に焦点を当てている。「ABlackstonerealestatecompanyexposedSSNdigits,DOBs...」は、不動産業界におけるセキュリティの脆弱性と、特定の企業がSSNやDOBなどの個人情報の漏洩を経験した事例を紹介し、セキュリティ対策の欠如が問題視されている。「AI agents are flooding public services with new requests | TechCrunch」は、AIによる公的サービスへの申請増加という社会的な現象を分析し、AIが人々の行動に与える影響を論じている。最後に、「QBittorrent breaks out of sandbox to commit crimes | daily.dev」は、QBittorrentがサンドボックスを突破し著作権侵害をしたとされる技術的な報告を紹介し、ソフトウェアのセキュリティに関する懸念を提示している。各記事はそれぞれ異なる分野や視点から、技術的・社会的な課題を提示しており、それぞれの文脈や背景に応じた情報が提供されている。

## 深掘り調査で得られた知見

深掘り調査により、ID検証業界におけるセキュリティ脆弱性が明らかになった。特定の企業が1年以上にわたって、ID検証の際のスキャンデータをリアルタイムでハッカーに公開していたことが判明した。このライブフィードは、パスポートや運転免許証などの個人情報を含み、長期間の暴露が発覚するまでに時間がかかった。この事件は、ID検証システムの信頼性に大きな疑問を投げかけた。また、同様の問題が他のセクターにも見られる可能性があり、特に不動産業界では、セキュリティの欠如がデータ漏洩を引き起こしているとの指摘もされている。さらに、AIが公共サービスへの申請を増加させている現象も確認され、これは技術の進化による新たな課題として注目されている。QBittorrentがサンドボックスから脱出し、著作権侵害をしたとの報告も複数のソースで確認されているが、具体的な状況は不明である。これらの事例は、セキュリティと技術の進化がもたらすリスクと課題を浮き彫りにしている。

## 不確実な点・追加確認が必要な点

記事間の食い違いや、資料からは断定できない点を具体的に書く場合、以下の内容が挙げられる。  

まず、記事1と記事4のテーマは一見関連性が見られないが、どちらも技術的脆弱性やセキュリティリスクに関する話題である。記事1はID検証企業におけるライブフィードの漏洩を扱い、記事4はAIアーキテクトが公共サービスへの申請を増加させている現象を分析している。両者のテーマは異なるが、どちらも技術的な問題が社会的な影響を及ぼしているという点で共通している。  

また、記事3と記事5は、それぞれ異なる業界（不動産とビットコイン関連ソフトウェア）を題材にしているが、どちらもセキュリティに関する問題を扱っている。記事3はBlackstoneという不動産企業がSSNや住所などの個人情報の漏洩を経験したとされるが、具体的な原因や対応策については明確にされていない。一方、記事5はQBittorrentがサンドボックスから脱出し、著作権侵害をしたとされる行動をしたとされているが、その実際の行動や法的影響については不明瞭である。  

さらに、記事2は自動車業界におけるCarPlayの導入が消費者の選好に与える影響を分析しているが、そのA/Bテストの詳細や、結果の正確性については不明である。また、記事4の研究者Chris SchmitzがAIの影響を「agentic flooding」と呼んでいるが、この現象がAIの直接的な影響であるか、それとも他の要因が絡んでいる可能性があるかは明確にはされていない。  

以上のように、各記事は異なる業界やテーマを扱っているが、技術的脆弱性やセキュリティリスク、あるいはAIの影響といった共通の課題を浮き彫りにしている。しかし、それぞれの記事が提示する情報は、詳細な事実や因果関係が明確にされていないため、断定的な結論を導くことはできない。

## 元記事一覧

- [HackersHadALiveFeedOfEveryIDThisVerificationCompany...](https://www.techdirt.com/2026/09/03/hackers-had-a-live-feed-of-every-id-this-verification-company-scanned-for-over-a-year/)
- [ThecarindustryA/Btestedselling acarwithandwithoutCarPlay](https://news.ycombinator.com/item?id=49590225)
- [ABlackstonerealestatecompanyexposedSSNdigits,DOBs...](https://news.ycombinator.com/item?id=49422204)
- [AI agents are flooding public services with new requests | TechCrunch](https://techcrunch.com/2026/09/10/ai-agents-are-flooding-public-services-with-new-requests/)
- [QBittorrent breaks out of sandbox to commit crimes | daily.dev](https://daily.dev/posts/qbittorrent-breaks-out-of-sandbox-to-commit-crimes-ka9biosdq)
