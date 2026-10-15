---
title: macOSでシステム音声を仮想ドライバなしで録音する方法
type: knowledge
status: draft
created: 2026-10-15
updated: 2026-10-15
confidence: medium
---

# macOSでシステム音声を仮想ドライバなしで録音する方法

## 結論

macOS 13（Ventura）以降、Apple は ScreenCaptureKit を導入し、システム音声を直接録音する機能を提供するようになり、仮想ドライバやループバックルーティングの必要性が大幅に低下しました。これにより、ユーザーは設定を簡素化し、より効率的にシステム音声を録音できるようになりました。特に、MeetingRecorder や ReScreen、OBS Studio といったツールが ScreenCaptureKit を活用して実用的な録音を実現しており、プライバシー保護とローカルでの処理が重視される傾向が見られます。

## テーマ概要

macOSでシステム音声を録音する方法についての話題は、仮想ドライバを使わずに直接録音できるようになったことにより注目を集めています。AppleはmacOS 13（Ventura）以降、ScreenCaptureKitという開発者向けフレームワークを導入し、システム音声を直接キャプチャする機能を提供するようになりました。これにより、BlackHoleやSoundflowerなどの仮想ドライバの使用が不要となり、ユーザーはより簡単で効率的な方法で録音を行うことが可能となりました。また、プライバシーや著作権保護の観点から、システム音声の録音は制限されていましたが、ScreenCaptureKitの導入によりその制限が緩和されました。このような技術的な進化により、ユーザーがシステム音声を録音する際の手間や複雑さが減り、関心が高まっています。

## 共通して確認できる点

macOS 13（Ventura）以降、AppleはScreenCaptureKitという開発者向けフレームワークを導入し、システム音声を直接キャプチャする機能を提供しています。これにより、BlackHoleやSoundflowerなどの仮想ドライバの使用が不要となりました。MeetingRecorderというアプリでは、636回の会議（284時間）を録音し、システム音声を正確にキャプチャするための実用的なソリューションとして構築されました。ReScreenは、仮想ドライバやループバックルーティングを必要とせず、macOS自体を介して録音する方法を提供しています。OBS StudioもScreenCaptureKitを活用し、macOSのシステム音声を録音できるようになりました。macos-screen-recorder（sck-record）は、CLIからスクリーンとシステム音声を録音できるツールで、仮想ドライバやsudoの使用を必要としません。Appleはプライバシーや著作権保護のため、ユーザーがシステム音声を直接録音するのを制限していましたが、ScreenCaptureKitの導入によりその制限が緩和されました。これらのツールは、ユーザーがシステム音声を録音する際に、仮想ドライバやループバックルーティングの複雑な設定を必要としなくなり、より簡単で効率的な方法を提供しています。

## 記事ごとの差分・視点の違い

記事「How to Capture System Audio on Mac (No Drivers) | Cubix」は、macOS 13（Ventura）以降導入されたScreenCaptureKitフレームワークを活用したシステム音声の録音方法を解説しており、仮想ドライバやループバック設定を必要としない点を強調しています。また、ReScreenやOBS StudioなどのツールがScreenCaptureKitを用いてシステム音声を録音できるようになった点を挙げ、ユーザーが設定を簡素化できるようになった実用性を説明しています。

記事「How I record system audio on macOS without a virtual driver」は、macOSがシステム音声を録音するのを制限している現状を背景に、MeetingRecorderという自前のアプリケーションを開発した経緯を述べています。この記事では、仮想ドライバの使用が面倒で、ユーザーが録音の設定を忘れがちであるという課題を強調し、ScreenCaptureKitの導入によって解決された点を具体的に示しています。

記事「HowWeSolved360VideoStreaming&Real-TimeUploadingfor...」は、iOSデバイスにおけるビデオストリームとリアルタイムアップロードの技術的課題を扱っており、macOSのシステム音声録音とは直接関係ありません。この記事は、WebSocket接続のドメインマッチングやメモリ管理の問題を解決した実装例として、iOSデバイスの制限を克服した技術的なアプローチを説明しています。

記事「Howto Reframe360Videosin DavinciResolve- YouTube」は、360度動画の編集方法を紹介した動画の概要であり、macOSのシステム音声録音とは関連性がありません。この記事では、Davinci Resolveを用いた360度動画の編集プロセスを説明しており、音声録音の技術的側面には触れていないため、今回のテーマとは異なります。

記事「I built a $5 meeting recorder for Mac that never leaves your ...」は、macOSで録音する際のプライバシー保護と、ローカルでの音声認識機能を活用したアプリケーション「Listener」の開発経緯を述べています。この記事では、ユーザーがクラウドに音声をアップロードせず、すべての処理をローカルで行うという点を強調し、macOSの音声録音機能とプライバシー保護の関係性を論じています。

## 深掘り調査で得られた知見

macOS 13（Ventura）以降、Apple は ScreenCaptureKit という開発者向けフレームワークを導入し、システム音声を直接録音する機能を提供するようになり、BlackHole や Soundflower などの仮想ドライバの使用が不要となりました。この機能は、スクリーンキャプチャのAPIを拡張したもので、音声録音にはスクリーンストリームを設定し、その後ビデオを無視する形で利用します。MeetingRecorder というアプリでは、この ScreenCaptureKit を活用し、636回の会議（284時間）を録音し、システム音声を正確にキャプチャする実用的なソリューションとして構築されました。また、ReScreen や OBS Studio も ScreenCaptureKit を利用してシステム音声を録音できるようになりました。macos-screen-recorder（sck-record）という CLI ツールも、仮想ドライバや sudo の使用を必要とせず、スクリーンとシステム音声を録音できます。Apple はプライバシーや著作権保護のため、ユーザーがシステム音声を直接録音するのを制限していましたが、ScreenCaptureKit の導入によりその制限が緩和されました。これらのツールは、ユーザーがシステム音声を録音する際に、仮想ドライバやループバックルーティングの複雑な設定を必要としなくなり、より簡単で効率的な方法を提供しています。

## 不確実な点・追加確認が必要な点

macOSでシステム音声を録音する方法について、複数の記事が異なる角度から情報を提供していますが、それらの間にはいくつかの不一致や不明点が確認されています。まず、記事1と記事2は、macOS 13（Ventura）以降に導入されたScreenCaptureKitというフレームワークを前提としており、これにより仮想ドライバの使用が不要となることを述べています。ただし、記事2では、ScreenCaptureKitが音声録音に特化したAPIを備えていることを強調しており、録音用のスクリーンキャプチャストリームを設定する必要があると説明しています。一方で、記事1は、macOSのプライバシーコントロールの制限を解除するための設定や、ツールの使用方法に焦点を当てています。

また、記事5では、macOSでシステム音声を録音する際のユーザー体験を重視したアプリ「Listener」が紹介されており、音声認識や要約機能をローカルで実行できる点を強調しています。ただし、記事1や記事2では、macOSのシステム音声録音に特化したツールや方法が詳細に説明されている一方で、記事5の内容は、録音機能に加えて音声認識や要約機能を含むアプリケーションの実装に注力しており、システム音声録音の技術的なプロセスには深く触れていない点が見られます。さらに、記事3や記事4は、システム音声録音とは直接関係のない内容を扱っており、テーマの範囲外となるため、本セクションでは対象外とします。

以上の通り、各記事は異なる視点から情報を提供しており、技術的な詳細や実装方法については一貫性がなく、特定の情報が断定的に述べられているわけではありません。そのため、システム音声録音の具体的な方法やツールの使用について、正確な情報を得るためには、各記事の内容を総合的に検討する必要があります。

## 元記事一覧

- [How to Capture System Audio on Mac (No Drivers) | Cubix](https://cubix.design/resources/how-to-capture-system-audio-on-mac-without-installing-drivers)
- [How I record system audio on macOS without a virtual driver](https://meetingsrecorder.com/blog/system-audio-macos-build-log/)
- [HowWeSolved360VideoStreaming&Real-TimeUploadingfor...](https://www.scien.cx/2026/08/08/how-we-solved-360-video-streaming-real-time-uploading-for-ios-devices/)
- [Howto Reframe360Videosin DavinciResolve- YouTube](https://www.youtube.com/watch?v=crzUGxkAYMk)
- [I built a $5 meeting recorder for Mac that never leaves your ...](https://dev.to/luizhcrs_47/i-built-a-5-meeting-recorder-for-mac-that-never-leaves-your-machine-4p4a)
