---
title: 10年経ったGalaxy Note4を1.2WでLinuxサーバーに変換
type: knowledge
status: draft
created: 2026-10-22
updated: 2026-10-22
confidence: medium
---

# 10年経ったGalaxy Note4を1.2WでLinuxサーバーに変換

## 結論

Samsung Galaxy Note 4 を 1.2 ワットという極めて低消費電力で Linux サーバーとして運用し、海洋安全アプリケーション「Maritime Watch」を動かした実績は、退役スマートフォンの再利用可能性を示す明確な例である。このプロジェクトでは、Android の電力管理を制御し、Termux と headless Linux を組み合わせることで、表示を必要としないバックグラウンド処理を実現した点が、技術的な特徴として重要である。

## テーマ概要

古いスマートフォンを再利用して、低消費電力のLinuxサーバーとして運用するというアイデアが注目されている。特に、2014年に発売されたSamsung Galaxy Note 4を1.2ワットという極めて低消費電力で動作させる技術が紹介されており、海洋安全を目的としたアプリケーション「Maritime Watch」を動かしている。このプロジェクトでは、Androidの電力管理を制御し、バックグラウンドでの処理を可能にするための工夫が行われており、Termuxとheadless Linuxを組み合わせることで、表示を必要としない環境での運用が実現されている。また、この技術は、Raspberry Piなどの他のオプションよりも高性能なプロセッサとRAMを備えた退役スマートフォンが適しているという主張を含んでいる。このような再利用技術は、電子廃棄物の削減やコスト削減を目的とした持続可能な技術革新として注目されている。

## 共通して確認できる点

Samsung Galaxy Note 4は2014年に発売され、Octa-core Exynosプロセッサと3GB RAMを搭載していた。このデバイスは、廃棄処分やクラウドVPSの利用よりも、再利用可能なLinuxサーバーとして活用されることが検討された。1.2ワットの消費電力で運用可能な状態にまで到達し、Maritime Watchというオープンソースの海洋安全エンジンを動かしている。Maritime Watchは、気象情報とAIS船舶トラフィックを組み合わせて漁船の出港タイミングを計算する。Androidの電力管理を克服し、HTTP Keep-Alive Long Pollingを導入したり、Termuxを電池最適化の除外リストに追加することで電力消費を削減した。また、tmuxを使用してセッションを維持し、表示を必要としないバックグラウンド処理を実現している。このプロジェクトでは、Raspberry Piなどの他のオプションよりも、高性能なプロセッサとRAMを備えた退役スマートフォンが適しているという主張が含まれている。

## 記事ごとの差分・視点の違い

記事「How I Turned a 10-Year-Old Galaxy Note 4 into a 1.2W Linux Server for Marine Safety」は、退役スマートフォンを海洋安全のための低消費電力サーバーとして再利用した実績を紹介しており、電力管理の工夫や具体的な用途（漁船の出港タイミング計算）に焦点を当てている。一方、「I turned my old Galaxy phone into a pocket Linux server with Termux」は、個人的な用途（Syncthingのホストとしての利用）に特化し、Termuxを活用したLinux環境の構築方法を解説している。また、「How to Run Docker/Containers With Termux」は、Termux内でDockerやコンテナ技術を活用する際の制限と代替手段について議論しており、実行可能な方法やツールの選択肢を提示している。さらに、「Running and managing Docker containers - Termux」は、YouTube動画を通じてDockerの実行例を示しているが、具体的な手順や検証情報は限られている。最後に、「GitHub - eyalgi11/screenshot-text-to-speech」は、スクリーンキャプチャからテキストを抽出し音声合成するOCRツールの実装例を紹介しており、TesseractやPaddleOCRといったOCR技術の応用例を示している。各記事は、目的や技術的アプローチ、利用シーンに応じて異なる視点でTermuxやLinux環境の活用法を提示している。

## 深掘り調査で得られた知見

Samsung Galaxy Note 4 は 2014 年に発売され、Octa-core Exynos プロセッサと 3GB RAM を搭載しており、10 年後も再利用可能な性能を備えていた。このデバイスは、1.2 ワットの消費電力で運用可能な Linux サーバーとして改造され、Maritime Watch という海洋安全エンジンを動かしている。Maritime Watch は気象情報と AIS 船舶トラフィックを組み合わせ、漁船の出港タイミングを計算する。このプロジェクトでは、Android の電力管理を制御し、電力消費を極力抑える工夫が行われた。Termux と headless Linux を組み合わせることで、表示を必要としないバックグラウンド処理を実現している。Telegram ボットリスナーでは、HTTP Keep-Alive Long Polling を導入し、電力消費を削減した。また、Termux を電池最適化の除外リストに追加し、tmux を使ってセッションを維持している。Raspberry Pi などの他のオプションと比較して、退役スマートフォンが高性能なプロセッサと RAM を備えており、適していると主張している。

## 不確実な点・追加確認が必要な点

記事間の食い違いや資料からは断定できない点を以下に示す。まず、Galaxy Note 4 を Linux サーバーとして再利用する取り組みについては、記事 1 で 2014 年モデルの Galaxy Note 4 を使用し、1.2W の消費電力で運用していることが明記されている。一方、記事 2 では、2026 年に公開された記事で、同様の手法を用いて Syncthing の利用を目的としたが、具体的な電力消費量は記載されていない。また、記事 1 は Marine Watch という特定のアプリケーションを動かしており、その背景にある問題（気象情報の誤解釈など）や、Telegram ボットリスナーの電力消費削減策（HTTP Keep-Alive Long Polling の導入）が詳細に記載されている。一方、記事 2 は Syncthing を中心にした用途で、Termux を使用した Linux 環境の構築方法や、Ubuntu と RVNC との併用について記載しているが、電力管理や具体的な電力消費量には触れていない。このため、両記事は目的や実装の詳細に違いがある。また、記事 3 と 4 では、Termux と Docker の関連性について論じているが、Docker の実行環境が Android では制限があり、Proot-Distro や rootless ツールの利用が推奨されている点が一致している。ただし、記事 4 の YouTube ビデオでは具体的な手順が示されていないため、Docker の実行可能性に関する断定は避けている。また、記事 5 は OCR と Tesseract に関する情報だが、他の記事と直接的な関連性は見られず、独立した技術の利用が記載されている。これらの点から、各記事は異なる目的や技術的背景に基づいており、特定の実装や結果については断定できない部分が含まれている。

## 元記事一覧

- [HowI Turned a 10-Year-OldGalaxyNote4intoa1.2WLinuxServer...](https://dev.to/keremkalyoncu/how-i-turned-a-10-year-old-galaxy-note-4-into-a-12w-linux-server-for-marine-safety-1lb5)
- [I turned my old Galaxy phone into a pocket Linux server with ...](https://www.howtogeek.com/old-galaxy-phone-into-a-pocket-linux-server-with-termux/)
- [HowtoRunDocker/ContainersWithTermux- DEV Community](https://dev.to/terminaltools/how-to-run-dockercontainers-with-termux-52g5)
- [Runningand managingDockercontainers-Termux- YouTube](https://www.youtube.com/watch?v=3RVyCdcRi74)
- [GitHub - eyalgi11/screenshot-text-to-speech: KDE screenshot OCR to...](https://github.com/eyalgi11/screenshot-text-to-speech)
