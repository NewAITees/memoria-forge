---
type: knowledge
status: draft
created: 2026-08-11
updated: 2026-08-11
confidence: medium
---

+++
title: Your firewall is your AI policy — I probed 18 major sites to read it
created: 2026-08-11
updated: 2026-08-11
+++

## 概要

この記事では、AIクローラーがウェブサイトのコンテンツを取得できるかを調査し、ファイアウォール設定がAIポリシーにどのように反映されているかを明らかにしています。18の主要なウェブサイトをプローブし、各AIクローラー（GPTBot、OAI-SearchBot、ClaudeBot、PerplexityBotなど）のアクセス状況を分析しました。

## 詳細

### 調査方法

- AIクローラーのユーザーエージェントを用いて、各サイトへのアクセスを試しました。
- クローラーがJavaScriptを実行するかを確認し、HTMLの内容を取得するかを測定しました。
- ファイアウォール設定がどのようにAIポリシーに影響しているかを分析しました。

### 主な発見

- **The Guardian** はGPTBot、OAI-SearchBot、ChatGPT-Userに200を返していますが、ClaudeBot、PerplexityBot、CCBotには403を返しています。
- **The New York Times** はほぼすべてのAIクローラーに403を返していますが、bingbotとAmazonbotは200を返しています。
- **Reddit** はrobots.txtでAIクローラーをすべてブロックしていますが、実際のWAFでブロックされていない場合があります。
- **Figma** はすべてのAIクローラーに200を返しています。

### 注意点

- ステータスコードはブロックされたクローラーを示すが、具体的な理由は不明である。
- ファイアウォール設定はビジネス文書として読めるが、詳細な理由は不明である。
- プローブは特定のベンダーのIP範囲ではなく、一般的なプローブに基づいているため、実際の結果は異なる可能性がある。

## ソース

- [Your firewall is your AI policy — I probed 18 major sites to read it](https://example.com)
- [AIVisibilityCheck: Run This 10-Minute Test Before You Buy Anything](https://aeoeye.com/blog/ai-visibility-check)
- [Brand Not in AI Search? Here's Why + How to Fix](https://www.outriggerai.com/blog/brand-not-appearing-ai-search-fix)
- [Windows 11: Allow/Block Apps in Firewall](https://www.technipages.com/block-unblock-programs-in-windows-firewall)

## 解決策

- AIクローラーをブロックしていないかを確認し、ファイアウォール設定を調整する。
- ブランドの外部信号を増やすため、高権限のプラットフォームで自然なメンションを生成する。
- ブランドの情報が不一致していないかを確認し、統一されたプロファイルを構築する。

## 未解決の問題

- AIクローラーのブロック設定がファイアウォールに正確に反映されているか。
- 各AIエンジンのAI可視性の測定方法が一貫しているか。
- プローブの結果が実際の結果と一致しているか。

## 結論

ファイアウォール設定はAIポリシーに強く関係しており、クローラーのアクセスを制御するための重要な要素です。AI可視性を高めるためには、外部信号の増加と情報の一貫性が重要です。

+++

# Your firewall is your AI policy — I probed 18 major sites to read it


## 出典

- [Your firewall is yourAIpolicy — I probed 18majorsitesto read it](https://dev.to/abouchard11/your-firewall-is-your-ai-policy-i-probed-18-major-sites-to-read-it-5552)
- [CanAIsee yoursite? — freeAIcrawler audit](https://readablebyai.com/)
- [A10AIFirewallProtection in Action | A10 Networks, Inc... | LinkedIn](https://www.linkedin.com/posts/a10networks_seeing-ai-firewall-protection-in-action-is-activity-7488580423518744576-9cK3)
- [Anubis: WebAIFirewallUtility | Anubis](https://anubis.techaro.lol/)
- [Windows 11: Allow/Block Apps inFirewall](https://www.technipages.com/block-unblock-programs-in-windows-firewall/)

## 未解決点

- 追加調査が必要です。
