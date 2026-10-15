---
title: Google ChromeでuBlock Originをインストールする方法と制限
type: knowledge
status: draft
created: 2026-10-16
updated: 2026-10-16
confidence: medium
---

# Google ChromeでuBlock Originをインストールする方法と制限

## 結論

Google Chrome 151 以降、Manifest V2 を使用する拡張機能のサポートが完全に終了したため、uBlock Origin のフル版をインストールするには、旧バージョンの Chrome（150.0.7871.187）を手動でインストールする必要がある。この方法はセキュリティリスクを伴うが、現時点での唯一のワークアラウンドであり、macOS においても同様の対応が求められている。

## テーマ概要

Google Chrome 151 以降、拡張機能が Manifest V2 を使用するサポートが完全に終了したため、uBlock Origin のフル版をインストールすることが困難となった。この変更により、ユーザーは古いバージョンの Chrome（150.0.7871.187）を手動でインストールする必要があり、更新を防ぐための手順が求められる。この問題は macOS において特に注目されており、ユーザーが Chrome に依存するアドブロッカーを維持するためのワークアラウンドや制限についての情報が求められている。また、このテーマは、ブラウザ拡張機能の技術的変化とその影響、そしてユーザーがどのように対応しているかを理解する上で重要な背景を提供している。

## 共通して確認できる点

Google Chrome version 151 以降、Manifest V2 を使用する拡張機能のサポートが完全に削除され、uBlock Origin のフルバージョンのインストールが困難となった。この問題に対処するためには、Manifest V2 をサポートする Chrome の旧バージョン（150.0.7871.187）を使用する必要がある。ただし、Chrome の更新を防ぐためには、特定のディレクトリのパーミッションを 000 に設定するなど、手動での対応が必要となる。また、アプリケーションの正当性を確認するためには、`spctl` コマンドを使用して Apple による認証を確認する必要がある。uBlock Origin Lite は Chrome で Manifest V3 をサポートしているが、フルバージョンは Firefox でより適切に動作する。uBlock Origin は、他のアプリケーションやデバイスでの広告ブロックができないなどの制限があり、ウェブサイトのレイアウトを破壊する可能性もある。

## 記事ごとの差分・視点の違い

記事「InstallinguBlockOrigininGoogleChrome:workaroundsand...」は、Chromeバージョン151でのManifest V2の非対応により、uBlock Originのフル版をインストールする方法を主に扱っており、特にmacOS環境での対処法に焦点を当てている。一方、「How ToInstalluBlockOriginExtensionInGoogleChromeIn 2025」はYouTube動画として提供されており、視覚的な説明を通じて、Chromeバージョンの変更やuBlock Originのインストール手順を解説している。また、「HowtoDebugAndroidChromeBrowserLogsfromaWindows...」はAndroidデバイスのChromeブラウザをWindowsからのリモートデバッグする方法を詳細に説明し、特にUSBデバッグの設定やadbコマンドの使用に注力している。一方、「RemotedebugAndroiddevices |ChromeDevTools |Chromefor...」はChrome DevToolsのリモートデバッグ機能の公式ドキュメントであり、一般的な手順とトラブルシューティング方法を網羅的に解説している。最後に、「AWindowsDesktopAppIs“NotResponding”:DiagnosetheWait...」はWindowsアプリケーションの「Not Responding」状態の診断方法を説明し、uBlock Originとは直接関係がないが、Windows環境でのアプリケーショントラブルシューティングの視点を提供している。各記事は対象のテーマに応じて、技術的な深さや対象読者層、情報の形式（テキスト vs 動画）が異なっている。

## 深掘り調査で得られた知見

Google Chromeのバージョン151以降では、Manifest V2をサポートしなくなったため、uBlock Originのフル版をインストールすることが困難となった。この問題に対処するためには、バージョン150.0.7871.187の古いChromeを手動でインストールする必要があり、更新を防ぐための手順が示されている。ただし、この方法はセキュリティアップデートの欠如や新しいウェブ技術への対応ができないなどのリスクを伴う。uBlock Origin LiteはManifest V3に対応しているが、フル版はFirefoxなど他のブラウザで動作が安定している。また、uBlock Originは他のアプリケーションやデバイスでの広告ブロックができないなどの制限がある。一方、AndroidデバイスのChromeブラウザをWindowsのPCからリモートでデバッグする方法も紹介されており、USBデバッグを有効にし、adbコマンドなどを用いることで、JavaScriptコンソールログやネットワークリクエストなどを確認できる。ただし、認証エラーなどのトラブルが発生する可能性がある。Windowsのアプリケーションが「Not Responding」と表示される状態は、UIスレッドが長時間メッセージを処理しなくなったことによるもので、ディスクやネットワークのI/O待機、他プロセスのブロック、モーダルダイアログ、デッドロックなどが原因となる。この状態を正確に診断するには、再現可能なアクションを実行し、システムの活動を記録することが重要である。

## 不確実な点・追加確認が必要な点

記事間の食い違いや、資料からは断定できない点を具体的に記述すると、以下の通りです。  

まず、記事1と記事2は、uBlock OriginをGoogle Chromeでインストールするためのワークアラウンドについて述べていますが、具体的な手順や対応バージョンの情報が異なります。記事1では、Chrome version 150.0.7871.187を用いる必要があると明記されており、そのバージョンはManifest V2をサポートしていると説明されています。一方、記事2はYouTubeの動画形式で提供されており、具体的なバージョン情報や手順が明示されていません。このため、記事2の内容は、記事1に依存した情報として捉える必要があります。  

また、記事3と記事4は、AndroidデバイスのChromeブラウザをWindowsからリモートデバッグする方法について説明していますが、手順や必要なツールの詳細に違いがあります。記事3では、USBデバッグの設定やadbコマンドの使用方法が具体的に記載されており、トラブルシューティングの手順も含まれています。一方で、記事4は公式ドキュメントとして提供されており、一般的なリモートデバッグの手順を説明していますが、特定のデバイスやOSの違いに注意する必要があると述べています。このため、記事3と記事4は補完的な情報として扱う必要があります。  

さらに、記事5は、Windowsアプリケーションが「Not Responding」状態になる原因について述べていますが、具体的なトラブルシューティング手順や原因の特定方法は、他の記事とは異なります。記事5では、UIスレッドが長時間メッセージを処理しないために発生する状態と、その原因となる可能性を列挙していますが、具体的な解決策や再インストール前の検証手順は、他の記事とは異なる内容となっています。このため、記事5の情報は、他の記事とは別個の問題として捉える必要があります。  

以上の通り、各記事はそれぞれ異なる焦点や詳細な情報に基づいており、一貫性や整合性が保証されていない点があります。そのため、情報の信頼性や正確性を確保するためには、各記事の内容を個別に検討し、必要に応じて補完的な情報や追加の確認を行う必要があります。

## 元記事一覧

- [InstallinguBlockOrigininGoogleChrome:workaroundsand...](https://dev.to/itlnx/installing-ublock-origin-in-google-chrome-workarounds-and-limitations-macos-3j93)
- [How ToInstalluBlockOriginExtensionInGoogleChromeIn 2025](https://www.youtube.com/watch?v=he7TQUxzjm0)
- [HowtoDebugAndroidChromeBrowserLogsfromaWindows...](https://dev.to/naimulkarim/how-to-debug-android-chrome-browser-logs-from-a-windows-laptop-1bib)
- [RemotedebugAndroiddevices |ChromeDevTools |Chromefor...](https://developer.chrome.com/docs/devtools/remote-debugging)
- [AWindowsDesktopAppIs“NotResponding”:DiagnosetheWait...](https://dev.to/wangwang_huang/a-windows-desktop-app-is-not-responding-diagnose-the-wait-before-reinstalling-1h7j)
