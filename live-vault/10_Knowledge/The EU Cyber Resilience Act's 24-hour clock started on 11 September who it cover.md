---
title: EU Cyber Resilience Actの24時間報告義務開始と適用範囲
type: knowledge
status: draft
created: 2026-09-23
updated: 2026-09-23
confidence: medium
---

# EU Cyber Resilience Actの24時間報告義務開始と適用範囲

## 結論

EU Cyber Resilience Act（CRA）の24時間の脆弱性報告義務は、2026年9月11日に正式に開始され、EU市場に提供される「デジタル要素を持つ製品」の製造業者が、アクティブに悪用されている脆弱性を24時間以内にENISAに報告する義務を負うようになりました。この義務は、ゲーム、アプリ、デスクトップソフトウェア、プラグインなどに適用され、SaaSやクラウドサービスは対象外です。違反した場合の罰則は、最大で15百万ユーロまたは年間売上高の2.5％に達する可能性があります。

## テーマ概要

EU Cyber Resilience Act（CRA）は、2024年12月10日に施行され、2026年9月11日から一部の義務が適用 began しました。この日から、EU市場で販売される「デジタル要素を持つ製品」の製造業者は、アクティブに悪用されている脆弱性や重大なセキュリティインシデントを24時間以内にENISA（欧州サイバーセキュリティ機関）に報告する義務が発生しました。この制度は、ソフトウェアやハードウェア、それらが遠隔でデータ処理を行うことのできる製品を対象とし、特にゲーム、アプリ、デスクトップソフトウェア、プラグインなどに適用されます。一方で、SaaS（ソフトウェア即サービス）やクラウドサービスは対象外とされており、NIS2指令によって規制されています。CRAの適用は、2027年12月11日に完全に実施される予定で、その間、SBOM（ソフトウェア製品一覧）の提供やセキュリティアップデートの5年間の維持なども求められます。この制度は、欧州市場での製品販売に関わる企業だけでなく、グローバルに影響を及ぼしており、非EU企業もEU市場に製品を販売する際には遵守する必要があります。24時間の報告義務は、セキュリティリスクの早期対応を促進するための重要な措置として注目されています。

## 共通して確認できる点

EU Cyber Resilience Act（CRA）の24時間の脆弱性報告義務は、2026年9月11日に正式に開始されました。この日から、EU市場に提供される「デジタル要素を持つ製品」の製造元は、脆弱性が実際に悪用されている場合、24時間以内にENISA（欧州ネットワークと情報セキュリティ局）に早期警告を提出する義務が生じました。72時間以内に詳細な通知を、14日以内に修正措置の最終報告を提出する必要があります。この義務は、EU内外の製造元に適用され、SaaS（ソフトウェア即サービス）やクラウドサービスは対象外です。また、報告義務は製品がEU市場にすでに提供されている場合にも適用されます。CRAは2027年11月11日からさらに多くの義務が導入され、セキュリティ設計やCEマークの取得が求められるようになります。違反した場合の罰則は、最大で15百万ユーロまたは年間売上高の2.5％まで及びます。

## 記事ごとの差分・視点の違い

記事「The EU Cyber Resilience Act's 24-hour clock started on 11 September: who it covers, and a free way to check your dependencies」は、CRAの24時間報告義務が開始された背景と適用範囲を解説し、実務的なチェック方法を提示しています。この記事では、特に中小開発者や個人事業主が対象となる可能性を強調しており、具体的なツールや方法論を紹介しています。一方、「EU's Cyber Resilience Act starts the 24-hour vulnerability clock」は、より広範な観点からCRAの影響を論じており、業界団体やセキュリティ専門家の見解を引用して、法規制の意義と実務への影響を説明しています。また、「I built a vulnerability scanner that refuses to lie to me」は、セキュリティツールの信頼性について議論し、secfixという独自のツールの開発経緯とその特徴を詳細に説明しています。この記事は技術的な視点から、ツールの信頼性と実用性を重視しており、セキュリティ分析の信頼性向上を目指しています。「Highly Accurate Website Scanner | Try a Free Vulnerability Scan」は、Webアプリケーションの脆弱性スキャンツールを紹介し、その精度と検出能力を強調しています。この記事は、ネットワークセキュリティの実務における具体的なツールの活用を目的としており、検出対象の範囲や検出精度について詳しく解説しています。「ASecurityScannerIsEasy. Building One You Can Actually Trust Is Not」は、セキュリティスキャナの信頼性の重要性を指摘し、セキュリティ分析ツールの設計における課題を論じています。この記事は、ツールの信頼性を確保するためには、コード構造への理解や実行による検証が不可欠であると主張しており、セキュリティツールの開発プロセスにおける課題を掘り下げています。

## 深掘り調査で得られた知見

EUのサイバーレジリエンス法（CRA）の24時間時計が2026年9月11日に開始されたことについて、深掘り調査では具体的な適用範囲や義務の詳細が明らかになった。CRAは、EU市場に提供される「デジタル要素を備えた製品」のセキュリティを強化するための規制であり、製造元がアクティブに悪用されている脆弱性を発見した場合、24時間以内にENISA（欧州サイバーセキュリティ機関）に早期警告を提出する義務がある。これは、単なるゲーム開発者やアプリ提供者から大規模な企業まで、すべての製造元に適用される。また、重大なセキュリティインシデントの報告も同様の期限が設定されている。CRAは、2026年11月11日からソフトウェアのBill of Materials（SBOM）やCE認証などの他の義務が適用されるが、24時間の報告義務はすでに施行されている。この義務は、EU市場に製品を提供するすべての製造元、包括して非EUの企業も含む。違反行為には最大で1億5000万ユーロまたは年間収益の2.5％の罰金が科される可能性がある。また、CRAはSaaSやクラウドサービスを除き、他の製品に適用される。さらに、既にEU市場に流通している製品にも適用されるため、企業は早期の対応が求められている。この法の施行は、グローバルなサイバーセキュリティの強化に向けた重要な一歩となる。

## 不確実な点・追加確認が必要な点

記事間の食い違いや資料からは断定できない点を具体的に書くと、以下の通りです。

記事1と記事2はともにEU Cyber Resilience Act（CRA）の24時間の脆弱性報告義務が2026年9月11日に開始されたことを確認しています。ただし、記事1ではCRAの一部の義務がすでに適用されていることを明示し、特にArticle 14（メーカーの報告義務）が11 September 2026から適用されるとしています。一方、記事2は同様の内容を述べていますが、具体的な記事の公開日時や取得日時が不明のため、どちらがより最新の情報を提供しているかは明確ではありません。また、記事1ではCRAの他の義務（SBOM、CEマーキングなど）が2027年12月11日に開始されることも記載されていますが、記事2にはその情報は含まれていません。

記事3は脆弱性スキャナの開発に関する内容であり、CRAとの直接的な関連性は明示されていません。記事4と記事5も同様に、CRAの直接的な情報は含まれていません。したがって、これらの記事はCRAの報告義務に関する情報とは別に、脆弱性検出ツールの開発や利用についての内容を提供しています。そのため、CRAに関する情報とこれらのツールの関連性は、資料からは断定できません。また、記事4では2026年7月23日に公開されたとされているため、記事1や記事2よりも古い情報である可能性があります。このため、情報の信頼性や最新性を比較する際には、各記事の公開日時や取得日時の情報が重要となります。

## 元記事一覧

- [The EU Cyber Resilience Act's 24-hour clock started on 11 September: who it covers, and a free way to check your dependencies - DEV Community](https://dev.to/abin_johnson/the-eu-cyber-resilience-acts-24-hour-clock-started-on-11-september-who-it-covers-and-a-free-way-g2a)
- [EU's Cyber Resilience Act starts the 24-hour vulnerability clock](https://www.theregister.com/security/2026/09/11/eus-cyber-resilience-act-starts-the-24-hour-vulnerability-clock/5295821)
- [I builtavulnerabilityscannerthatrefuses to lie to... - DEV Community](https://dev.to/balbaks/i-built-a-vulnerability-scanner-that-refuses-to-lie-to-me-22fl)
- [Highly Accurate Website Scanner | Try a Free Vulnerability Scan](https://pentest-tools.com/website-vulnerability-scanning/website-scanner)
- [ASecurityScannerIsEasy. Building One You Can... - DEV Community](https://dev.to/danish_ahmad_bd75f47f787f/a-security-scanner-is-easy-building-one-you-can-actually-trust-is-not-2m)
