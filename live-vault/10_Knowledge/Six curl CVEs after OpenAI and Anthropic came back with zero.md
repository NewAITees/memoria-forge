---
title: AISLE AIがcurlで6つのCVEを発見　OpenAI・Anthropicはゼロ
type: knowledge
status: draft
created: 2026-09-15
updated: 2026-09-15
confidence: medium
---

# AISLE AIがcurlで6つのCVEを発見　OpenAI・Anthropicはゼロ

## 結論

AISLEのAIシステムがcurlにおいて6つのCVEを発見し、そのうち6つがCVEとして承認された事実は、専門的なAIシステムがフロンティアAIモデルよりもゼロデイ脆弱性の発見において優れている可能性を示している。この結果は、AIを用いたセキュリティ検証の新たな方向性を示しており、技術コミュニティにおいてAI駆動のセキュリティ対策の今後の展開について議論を呼んでいる。

## テーマ概要

このテーマは、OpenAIとAnthropicがcurlの脆弱性を発見できなかった一方で、AISLEというセキュリティ企業が6つのCVE（Common Vulnerabilities and Exposures）を発見した事実に基づいています。curlは世界中で200億インスタンス以上に導入されている広く使用されるソフトウェアで、そのセキュリティの重要性から注目を集めています。AISLEが独自のAIシステムを用いてcurlのコードを分析し、6つの脆弱性を特定したことは、AIを用いたゼロデイ脆弱性発見の新たな可能性を示す重要な出来事です。また、この事象は、大規模言語モデル（LLM）を駆使したセキュリティ検証の限界や、専門的なAIシステムがより効果的な脆弱性発見に貢献できる可能性を浮き彫りにしています。このため、技術コミュニティでは、AIを活用したセキュリティ対策の今後の方向性について議論が広がっています。

## 共通して確認できる点

AISLEは、curlの脆弱性を6つ発見し、そのうち6つがCVEとして承認された。この結果は、OpenAI Codex SecurityおよびAnthropic Mythosがcurlの脆弱性をゼロ個見つけることになったことに対して発生した。curlの開発者であるDaniel Stenbergは、8月24日にcurlの次回リリースに向けて待機中のCVEが3つしかないと発表し、その後Anthropic MythosとOpenAI Codex Securityの結果がゼロだったと報告した。AISLEの自動AIシステムは29の報告書を生成し、そのうち6つがcurlセキュリティチームによって確認され、curl 8.22.0でのCVEとして承認された。これらの脆弱性はすべてLowセキュリティの評価であり、curlの高品質なエンジニアリングにより、影響の範囲が限定されている。また、AISLEの報告書は、curlの維持管理者がそれぞれの報告が本物であるか、CVEとしての必要性を判断した。この比較では、基準が公開され、タイムスタンプされたため、公平性が保たれた。この結果は、専門的なAIシステムが、フロンティアAIモデルよりもゼロデイの発見において有効であることを示唆している。

## 記事ごとの差分・視点の違い

記事「AISLE Discovered Six curl CVEs After OpenAI and Anthropic Found Zero」は、AISLEのAIシステムがcurlに6つのCVEを発見した経緯を詳細に記し、OpenAI Codex SecurityおよびAnthropic Mythosの結果がゼロだったことと比較して、専門的なAIシステムの有効性を強調している。一方、「Six curl CVEs after OpenAI and Anthropic came back with zero」は、この結果を背景に、AIベースのセキュリティ検出ツールの競争状況や、モデルの違いによる検出能力の差を論じるコメントが寄せられている。また、「[2608.21423] Agentic Security: A Systematization of Tools, Failure Modes, and Design Laws for LLM-Driven Penetration Testing」は、LLM駆動のセキュリティ検出システムの設計法則や失敗モードを体系化し、アグェントセキュリティの実装と課題を論じている。さらに、「Agentic Security: A Systematization of Tools, Failure Modes, and Design Laws for LLM-Driven Penetration Testing」は、具体的な実装例やツールの評価結果を含む技術的な内容を提供している。最後に、「Bringing the cybersecurity capabilities of Claude Mythos 5 to more ...」は、Claude Mythos 5の拡張とセキュリティ機能の利用範囲拡大を主に説明し、他のモデルとの比較ではなく、実際の防御への応用を強調している。

## 深掘り調査で得られた知見

深掘り調査では、OpenAI Codex SecurityとAnthropic Mythosがcurlの脆弱性をゼロ個報告した一方で、AISLEのAIシステムが6つのCVEを発見した事実が明確に確認されました。これらのCVEは、TLSおよびクッキー処理に関連し、OpenSSLプロバイダーの使用後の解放やOpenSSLピンニング回避など、低深刻度の脆弱性でした。curlのメンテナであるDaniel Stenbergは、8月24日に3つのCVEが待機状態であると報告し、その後AISLEのAIが29の報告を行い、そのうち6つがCVEとして承認されました。この結果は、専門的なAIシステムが大規模なAIモデルよりもゼロデイの発見において優れている可能性を示唆しています。また、Linux内核のメンテナであるGreg Kroah-Hartmanも同様のパターンを報告しており、専門AIの効果が広範なセキュリティ検証にわたって確認されています。さらに、AISLEのAIは、curlのコードベースを分析し、脆弱性の検出と修正に成功したことで、AI駆動のセキュリティ検証ツールの実用化が進んでいることを示しています。

## 不確実な点・追加確認が必要な点

記事間の情報にはいくつかの食い違いや、調査資料から断定できない点が確認されている。まず、記事1ではAISLEがcurlの6つのCVEを発見したと明記されており、そのうち6つがcurl 8.22.0で公表されたとされている。また、Daniel Stenbergが8月24日に公開したゼロ結果のタイムスタンプがベースとなり、AISLEの結果がその後に発表されたことが明示されている。しかし、記事2ではOpenAIとAnthropicがゼロ結果を報告したという記述はあり、AISLEの結果がその後に発生したとされているが、具体的な日時やCVEの詳細については述べられていない。このため、記事1と記事2の間に、AISLEの結果がどの時点で公表されたか、あるいはCVEの公表日が正確にどの日付かについての情報のズレが生じている。

また、記事3と記事4は同一篇のarXiv論文を示しており、記事3は抽象ページ、記事4は本文ページを示している。記事3の概要には「1 month ago」という情報があり、記事4の概要には「2 years from demonstration to deployed product」という記述があるが、具体的な公開日時や取得日時が不明であるため、時系列の正確な位置づけは困難である。さらに、記事5ではClaude Mythos 5の拡張に関する情報が述べられているが、その内容はAISLEのCVE発見と直接的な関係はなく、むしろセキュリティモデルの進化についての話題である。このため、記事1と記事5の間に、どちらがより新しい情報かを判断するためには追加の情報が必要である。また、記事1と記事4の間に、LLM駆動のセキュリティ検証システムに関する一般的な論点が述べられているが、具体的なCVEの発見や比較については明示されていない。このため、記事1の内容を根拠にした分析が他の記事と整合性を保つためには、さらなる情報の確認が必要である。

## 元記事一覧

- [AISLE DiscoveredSixcurlCVEsAfterOpenAIandAnthropicFound...](https://aisle.com/blog/aisle-discovered-six-curl-cves-after-openai-and-anthropic-found-zero)
- [SixcurlCVEsafterOpenAIandAnthropiccamebackwithzero](https://news.ycombinator.com/item?id=49536114)
- [[2608.21423] Agentic Security: A Systematization of Tools, Failure Modes, and Design Laws for LLM-Driven Penetration Testing](https://arxiv.org/abs/2608.21423)
- [Agentic Security: A Systematization of Tools, Failure Modes, and Design Laws for LLM-Driven Penetration Testing](https://arxiv.org/html/2608.21423)
- [Bringing the cybersecurity capabilities of Claude Mythos 5 to more ...](https://claude.com/blog/bringing-claude-mythos-5-to-more-defenders)
