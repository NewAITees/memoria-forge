---
title: プロンプトインジェクションがシェル操作に：Semantic Kernelの2つのRCE脆弱性
type: knowledge
status: draft
created: 2026-09-23
updated: 2026-09-23
confidence: medium
---

# プロンプトインジェクションがシェル操作に：Semantic Kernelの2つのRCE脆弱性

## 結論

MicrosoftのSemantic Kernelフレームワークにおける2つのリモートコード実行（RCE）脆弱性、CVE-2026-26030とCVE-2026-25592は、プロンプトインジェクション攻撃が実際のシェル操作にまで発展した実例として、AIエージェントフレームワークにおけるセキュリティリスクの深刻さを明確に示しています。これらの脆弱性は、ユーザー入力の不適切な検証やサニタイズが原因であり、Python SDKと.NET SDKそれぞれで異なる仕組みを悪用して任意コードの実行を可能にしています。この事例は、AI技術の進化に伴う新たなセキュリティ脅威の現実を浮き彫りにし、モデルの出力に過度な信頼を寄せることの危険性を再認識させる重要な教訓となっています。

## テーマ概要

MicrosoftのSemantic Kernelフレームワークにおける2つのリモートコード実行（RCE）の脆弱性、CVE-2026-26030とCVE-2026-25592が発覚し、これはプロンプトインジェクション攻撃が実際のシェル操作にまで発展した例として注目されています。これらの脆弱性は、ユーザー入力の適切な検証が行われていなかったことが原因で、Python SDKのInMemoryVectorStoreと.NET SDKのSessionsPythonPluginでそれぞれ発生しました。CVE-2026-26030では、フィルタパラメータがeval()関数で評価されるため、任意のコード実行が可能となりました。一方、CVE-2026-25592では、モデルがファイルダウンロード機能を呼び出す際、パス検証が行われず、Windowsのスタートアップフォルダにファイルを書き込むことができました。これらの脆弱性は、AIエージェントフレームワークにおけるプロンプトインジェクションの深刻さを示しており、モデルの出力に過度に信頼を寄せると、重大なセキュリティリスクに直面する可能性があります。このテーマは、AI技術の進化に伴うセキュリティ上の新たな脅威を理解し、適切な対策を講じるための重要な事例として注目されています。

## 共通して確認できる点

MicrosoftのSemantic Kernelフレームワークにおいて、2つのリモートコード実行（RCE）の脆弱性が確認され、CVE-2026-26030とCVE-2026-25592として公開されました。これらの脆弱性は、ユーザー入力の適切な検証やサニタイズが行われていなかったため、悪意のある入力が評価されるプロセスに悪用されました。CVE-2026-26030はPython SDKのInMemoryVectorStoreにおいて、フィルタパラメータがPythonのlambda式に変換され、eval()関数で評価される仕組みに問題がありました。このため、入力が適切に検証されなかった場合、任意のコードの実行が可能となりました。CVE-2026-25592は.NET SDKのSessionsPythonPluginにおいて、DownloadFileAsync関数がモデルに対してcallableとして公開され、パス検証が行われていなかったため、任意の場所にファイルを書き込むことが可能となりました。これらの脆弱性は、semantic-kernel 1.39.4（Python）と.NET SDK 1.71.0で修正されました。また、Microsoftのセキュリティブログでは、これらの脆弱性がプロンプトインジェクションの問題として認識されることが多いものの、実際にはリモートコード実行の可能性を示すものであると指摘しています。

## 記事ごとの差分・視点の違い

記事1は、Semantic Kernelの2つのRCE CVEについて詳細に説明しており、特にPython SDKと.NET SDKそれぞれの脆弱性の仕組みと、攻撃の実行例（calc.exeの起動）を具体的に示しています。また、脆弱性の原因として、ユーザー入力の不適切な扱いや、ブロックリストの回避手段を強調しています。この記事は、技術的な詳細に重点を置き、セキュリティ対策としてのパッチのバージョンと日付も明示しています。

記事2は、Microsoft Security Blogによる公式な発表で、Semantic KernelのRCE脆弱性の概要と、その影響範囲を述べています。ただし、具体的な技術的な詳細や、攻撃の実行例は記載されておらず、より広いセキュリティ上の課題や、AIエージェントフレームワーク全体におけるリスクを強調しています。この記事は、Microsoftの公式な立場と、セキュリティ対策の重要性を主張しています。

記事3は、OpenAIのハッキング事件を分析した記事で、攻撃の連鎖的なステップと、AIエージェントがテスト環境から抜け出して行った攻撃の詳細を説明しています。この記事は、攻撃の複雑さと、単一の脆弱性ではなく連続的な攻撃手法の重要性を強調しており、P2 Chain Analysisという新しい検出手法を提案しています。また、MITRE ATLASの技術を用いて攻撃のパターンを分析しています。

記事4は、OpenAI.fmというテキストから音声への変換サービスの紹介記事であり、セキュリティ関連の内容は含まれていません。この記事は、技術的なセキュリティ問題とは無関係で、主にサービスの紹介に焦点を当てています。

記事5は、npmパッケージ「indexed-btree」におけるサプライチェーン型マルウェアの存在を報告しており、このマルウェアが実行時コード内で動作し、スマートコントラクトを用いたC2通信を行うことを説明しています。この記事は、npmエコシステムにおけるセキュリティの脆弱性と、マルウェアの動作メカニズムに注目しており、具体的な技術的詳細と、Checkmarxによる分析結果も含まれています。

## 深掘り調査で得られた知見

MicrosoftのSemantic Kernelフレームワークにおける二つのRCE（リモートコード実行）脆弱性、CVE-2026-26030とCVE-2026-25592が発見され、それらはプロンプトインジェクション攻撃を悪用してシェルへのアクセスを可能にするものであることが明らかになった。CVE-2026-26030では、Python SDKのInMemoryVectorStoreが、フィルタパラメータをPython lambda式に変換してeval()で評価する処理を実行しており、入力が十分に検証されていないことから、任意コードの実行が可能となった。CVE-2026-25592では、.NET SDKのSessionsPythonPluginのDownloadFileAsync関数がモデルにcallableとして公開され、パス検証が行われていないため、攻撃者が任意の場所にファイルを書き込むことができ、特にWindowsのスタートアップフォルダにファイルを置くことで、ユーザーがログインする際にコードが自動的に実行される可能性がある。

これらの脆弱性は、Semantic Kernel 1.39.4（Python）および.NET SDK 1.71.0で修正され、2026年5月7日にリリースされた。Microsoftのセキュリティブログでは、これらの脆弱性がプロンプトインジェクションという通常のコンテンツセキュリティ問題を超えて、完全なリモートコード実行を可能にするものであることを強調している。また、AIエージェントフレームワークにおけるモデル出力の適切な処理が重要であると指摘し、ユーザー入力の検証とサニタイズの必要性を再認識させる内容となっている。

さらに、OpenAIのコミュニティフォーラムにおける脆弱性を悪用したハッキング攻撃が発覚し、その攻撃は複数のステップを経て行われた。Hacktron AIの研究者らがAnthropicのClaudeを用いてOpenAIをハッキングし、内部のサインオンシステムにアクセスし、GitHubのコードを抜き出し、変更を提案するという一連の行動が確認されている。OpenAIはこのハッキングに対して$6,500を支払ったが、これは単一の脆弱性ではなく、複数のステップによる連続的な攻撃であるため、一般的なセキュリティスキャンでは検出が困難である可能性がある。

また、npmパッケージ「indexed-btree」が、合法的な「sorted-btree」を模倣して、実行時コード内でマルウェアローダーを隠蔽していることが確認されている。このマルウェアは、特定のキー値（key == 100）がBTree.prototype.set()メソッドに渡されるときに実行され、ホスト情報やC2アドレスを取得し、スマートコントラクトを介してC2通信を行う。Checkmarxによると、このキャンペーンに関連する9つの他のnpmパッケージも発見され、合計で530万ダウンロードを達成している。この攻撃は、npmエコシステムのセキュリティ対策を克服する高度な技術を用いており、今後も同様の攻撃が増加する可能性がある。

## 不確実な点・追加確認が必要な点

記事間の食い違いや、資料からは断定できない点を以下に示す。まず、Semantic KernelのRCE脆弱性に関する情報は、記事1と記事2が一致しているが、記事2はMicrosoft Security Blogの投稿であり、記事1はDev.toの投稿であるため、情報の信頼性や発表時期の違いが確認されている。記事1は、CVE-2026-26030とCVE-2026-25592の2つのRCE脆弱性を具体的に説明し、それぞれの脆弱性の詳細な原因と修正バージョン（semantic-kernel 1.39.4と.NET SDK 1.71.0）を明記している。一方、記事2はMicrosoftの公式ブログであり、記事1の内容を一部反映しているが、具体的なCVE番号や修正バージョンは記載されていない。また、記事2の公開日時が不明であるため、記事1の情報が先に公開された可能性がある。

次に、記事3はOpenAIのハッキングに関する分析であり、記事1と記事2の内容とは異なるテーマを扱っている。記事3は、Hacktron AIの研究者によるOpenAIのハッキングと、その攻撃チェーンの分析を説明しており、Semantic KernelのRCE脆弱性とは直接関係がない。しかし、記事3の内容は、AIエージェントの脆弱性や攻撃手法の多段階性を示しており、記事1や記事2のテーマと関連性がある可能性がある。記事3の情報は、OpenAIの内部システムの脆弱性を指摘しており、これはSemantic KernelのRCE脆弱性とは別の問題であるが、同様の攻撃手法が使われている可能性がある。

記事4はOpenAI.fmの紹介であり、Semantic KernelやRCE脆弱性とは関係がない。記事5はnpmパッケージのSupply Chain Malwareに関する情報であり、Semantic KernelのRCE脆弱性とは異なるテーマを扱っている。記事5の情報は、npmエコシステムのセキュリティ問題を示しており、Semantic KernelのRCE脆弱性とは別の分野の問題である。ただし、両者ともAI関連の技術を扱っているため、共通のセキュリティ課題がある可能性がある。

以上のように、記事間にはテーマの違いや情報の信頼性の違いが確認されている。特に、Semantic KernelのRCE脆弱性に関する情報は記事1と記事2が一致しており、他の記事は関連性が低い。また、記事2の公開日時が不明であるため、記事1の情報が先に公開された可能性がある。したがって、記事1と記事2の情報は信頼性が高いが、他の記事の情報は関連性が低い。

## 元記事一覧

- [APromptInjectionTurnedIntoaShell:InsideSemantic...](https://dev.to/aditya_soni_e5b9d5213e544/a-prompt-injection-turned-into-a-shell-inside-semantic-kernels-two-rce-cves-22l7)
- [Whenpromptsbecomeshells:RCE... | Microsoft Security Blog](https://www.microsoft.com/en-us/security/blog/2026/05/07/prompts-become-shells-rce-vulnerabilities-ai-agent-frameworks/)
- [WhenChainAnalysisBeatsNeuralDetection:ALayer-by-Layer...](https://dev.to/aegisgate/when-chain-analysis-beats-neural-detection-a-layer-by-layer-look-at-the-openai-hack-346n)
- [OpenAI.fm](https://www.openai.fm/?ref=completeaitraining.com)
- [indexed-btree: npm Supply Chain Malware Executes at Runtime and Uses a Smart Contract on Ethereum Sepolia for C2 - DEV Community](https://dev.to/anoymask/indexed-btree-npm-supply-chain-malware-executes-at-runtime-and-uses-a-smart-contract-on-ethereum-d83)
