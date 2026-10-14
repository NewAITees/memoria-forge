---
title: Cloudflare 2019年障害：正規表現が引き起こす502エラー
type: knowledge
status: draft
created: 2026-10-15
updated: 2026-10-15
confidence: medium
---

# Cloudflare 2019年障害：正規表現が引き起こす502エラー

## 結論

Cloudflareの2019年の障害は、誤った正規表現の設計により、HTTP処理用のCPUコアを100%にまで押し付け、27分間の502エラーを引き起こした。この問題は、CPU制限の欠如と一括展開時の実行速度が原因であり、セキュリティ攻撃ではなく技術的なミスによるものであることが明確に確認されている。

## テーマ概要

2019年のCloudflareの障害は、誤った正規表現（regex）の設計が原因で発生した。この正規表現はバックトラックを過度に実行し、HTTP処理用のCPUコアを100%にまで押し付け、結果として27分間の502エラーが発生した。この障害はセキュリティ攻撃ではなく、技術的なミスによるものであり、CPU制限の欠如や一括展開時の実行速度が問題となった。この出来事は、Cloudflareの技術的な透明性と問題解決への取り組みを注目させるきっかけとなり、今なお技術コミュニティで議論されている。

## 共通して確認できる点

Cloudflareの2019年の障害は、誤った正規表現の設計により発生した。2019年7月2日13:42 UTCに、Cloudflareの全サーバーに同時に適用された新しいファイアウォールルールが原因で、27分間の502エラーが発生した。このルールには、バックトラックを過度に実行する正規表現が含まれており、HTTP処理用のCPUコアを100%にまで押し付けた。この問題は、CPU制限の欠如、正規表現の不適切な設計、および一括展開の実行速度が原因である。正規表現の一部である「.*(?:.*=.*)」が、バックトラックを引き起こし、処理が遅延した。WAFルールはsimulateモードで動作していたが、依然としてCPUを大量消費していた。14:07 UTCに問題が解決し、CEO Matthew Princeは14:36 UTCに最初の原因を公表した。10日後、CTO John Graham-Cummingが技術的なポストモルテムを公開した。この障害は、セキュリティ攻撃によるものではなく、誤った正規表現の設計によるものであると指摘されている。

## 記事ごとの差分・視点の違い

記事「Cloudflareoutage2019: how oneregexcaused27 minutes of502s」は、2019年7月2日に発生したCloudflareのサービス停止について、技術的な詳細を解説しており、正規表現の設計ミスが原因だったことを明確に説明している。この記事では、CPU使用率の急激な上昇や、ルールの実行速度が問題を悪化させた点を強調している。一方、記事「"Cloudflarefixes issuecausingglobaloutagesfor..." | LinkedIn」は、Cloudflareが過去の問題を修正したことを紹介しており、その修正がChatGPTやSpotifyなどのサービスに影響を与えたことを述べている。この記事は、問題の解決とその影響範囲に焦点を当てている。記事「When Cloudflare WAF detections fail, choose a rule response ...」は、Cloudflareが導入した新機能cf.appsec.request.failed_detectionsについて解説し、検出失敗をルールで処理する方法を説明している。この記事は、セキュリティ検出の失敗をどのようにルールに反映するかという技術的な視点を重視している。記事「cf.appsec.request.failed_detections·CloudflareRuleset Engine docs」は、cf.appsec.request.failed_detectionsフィールドの仕様と利用方法をドキュメンテーション形式で説明しており、技術的な実装の詳細を提供している。最後に、記事「CloudflareSettingsThatBlockPaidAPI Clients | ForgeMesh」は、Cloudflareの設定がAPIクライアントを不正にブロックしてしまう問題を指摘し、具体的な設定の影響を示している。この記事は、APIを提供する側の視点から、Cloudflareのデフォルト設定がもたらす問題を強調している。

## 深掘り調査で得られた知見

深掘り調査により、Cloudflareの2019年の障害は、誤った正規表現の設計とCPU制限の欠如が原因で発生したことが明確に確認されました。特に、「.*(?:.*=.*)」という正規表現がバックトラックを引き起こし、HTTP処理用のCPUコアを100%にまで押し付け、結果として27分間の502エラーが発生しました。この問題は、WAFルールがsimulateモードで動作しているにもかかわらず、CPUを大量消費していた点も原因の一つです。また、CloudflareのCTOであるJohn Graham-Cummingがポストモルテムを公開し、技術的な詳細を説明したことが記録されています。この障害はセキュリティ攻撃ではなく、技術的なミスによるものであり、その影響はChatGPT、Spotify、Zoomなどの主要サービスにまで及びました。さらに、Cloudflareはその後、WAF検出失敗時の処理を明示的に選択できるようにする新しいフィールド「cf.appsec.request.failed_detections」を導入し、検出失敗のIDを含む配列として提供しています。このフィールドは、カスタムルールやレート制限ルールで利用可能であり、検出失敗を信号として利用するためのものとして位置付けられています。また、CloudflareのBrowser Integrity Checkという設定は、PythonやPerlライブラリからのリクエストをブロックし、APIが403エラーを返す原因となることが判明しました。この問題は、APIの設定を適切に調整することが重要であることを示しており、特に自動化されたクライアントが利用するAPIには注意が必要です。

## 不確実な点・追加確認が必要な点

記事間での情報の整合性や断定できない点について、以下のようにまとめることができる。

記事1では、2019年7月2日13:42 UTCにCloudflareの全サーバーに同時実行された新しいファイアウォールルールが原因で、27分間の502エラーが発生したと明記されている。このルールには、バックトラックを過度に実行する正規表現が含まれており、HTTP処理用のCPUコアを100%にまで押し付けたとされている。また、この問題は、CPU制限の欠如、正規表現の不適切な設計、および一括展開の実行速度が原因であると指摘されている。

一方で、記事2では、Cloudflareの30分間のオートメーションが原因で、ChatGPT、Spotify、Zoom、および他の多くのサービスが停止したと述べている。この記事では、Cloudflareが25%のトラフィックをルーティングしていると述べており、これは記事1とは異なる記述である。また、記事2では、Cloudflareのオートメーションが原因で発生した問題を指摘しているが、具体的な原因や時間帯については明記されていない。

記事3と記事4は、CloudflareのWAF検出失敗時の処理について述べている。記事3では、CloudflareがWAF検出失敗時の処理を明示的に選択できるようにする新しいフィールドを導入したと述べており、記事4では、このフィールドの詳細な仕様と利用可能なルールについて説明している。ただし、これらの記事は、2019年のCloudflareのオートメーションや正規表現の問題とは直接関係がなく、むしろ、CloudflareのWAFの機能改善についての情報である。

記事5では、Cloudflareの設定がPaid APIクライアントを無視して403エラーを返す問題について述べている。この記事では、CloudflareのBrowser Integrity CheckがPythonやPerlのリクエストをブロックしていると指摘しており、これは2019年の正規表現の問題とは異なる技術的な問題である。

以上のように、各記事は異なるテーマや背景を持つため、記事間での情報の整合性や断定できない点が生じている。特に、記事1と記事2は、Cloudflareのオートメーションや正規表現の問題に関するものであり、それぞれ異なる時間帯や原因を指している。一方で、記事3、4、5は、CloudflareのWAFや設定に関する問題を扱っており、これらは2019年のオートメーションや正規表現の問題とは関係が薄い。したがって、記事間での情報の整合性や断定できない点が生じている。

## 元記事一覧

- [Cloudflareoutage2019: how oneregexcaused27 minutes of502s](https://dev.to/axrisi/cloudflare-outage-2019-how-one-regex-caused-27-minutes-of-502s-1nla)
- ["Cloudflarefixes issuecausingglobaloutagesfor..." | LinkedIn](https://www.linkedin.com/posts/garyhoke_cloudflare-outage-disrupts-chatgpt-x-other-activity-7396556671210201088-8Kho)
- [When Cloudflare WAF detections fail, choose a rule response ...](https://otf-kit.dev/blog/cloudflare-waf-failed-detections-fail-open-or-closed)
- [cf.appsec.request.failed_detections·CloudflareRuleset Engine docs](https://developers.cloudflare.com/ruleset-engine/rules-language/fields/reference/cf.appsec.request.failed_detections/)
- [CloudflareSettingsThatBlockPaidAPI Clients | ForgeMesh](https://forgemesh.io/blog/cloudflare-config-gotchas-paid-apis)
