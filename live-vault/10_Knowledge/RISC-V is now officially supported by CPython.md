---
title: RISC-VがCPythonで公式サポートへ
type: knowledge
status: draft
created: 2026-10-03
updated: 2026-10-03
confidence: medium
---

# RISC-VがCPythonで公式サポートへ

## 結論

CPythonは2026年8月24日にRISC-Vアーキテクチャを公式サポートとして追加し、同年9月10日にInfoQを通じてその発表が確認されました。このサポートはPEP 11において「tier 3プラットフォーム」として正式に採用され、RISC-Vの実際のハードウェアでのテストとデバッグが可能になったことが背景にあります。RISEプロジェクトが提供したRISC-Vマシンは、CPythonのビルドボットとしての役割を果たし、アーキテクチャ固有の問題の修正にも貢献しました。

## テーマ概要

CPythonがRISC-Vを公式サポートとして導入したことで、Pythonのクロスプラットフォーム開発における重要な進展が実現しました。このサポートは、RISC-Vアーキテクチャを「ティア3プラットフォーム」としてPEP 11に正式に記載し、開発コミュニティによる協力とテストを通じて実現されました。RISC-Vはオープンな指令セットアーキテクチャ（ISA）であり、x86やARMなどの特許を持つアーキテクチャとは異なり、誰でも実装可能という特徴があります。これにより、RISC-Vは近年急速に成長しており、2032年までに4倍に成長すると予測されています。PythonがRISC-V上で安定して動作することにより、この成長に伴う開発環境の整備が進むことが期待されています。また、CPythonのCIパイプラインにRISC-Vを統合する取り組みも進められており、今後のさらなる改善が見込まれています。

## 共通して確認できる点

CPythonは2026年8月24日にRISC-Vアーキテクチャを公式サポートとして追加し、同年9月10日にInfoQを通じてその発表が確認されました。このサポートはPEP 11において「tier 3プラットフォーム」として公式に採用され、RISC-Vの実際のハードウェアでのテストとデバッグが可能になったことが背景にあります。RISEプロジェクトが提供したRISC-Vマシンは、CPythonのビルドボットとしての役割を果たし、アーキテクチャ固有の問題の修正にも貢献しました。サポート内容にはriscv64-unknown-linux-gnuというターゲットトリプルが含まれており、glibc/gccおよびglibc/clangのビルドが可能となっています。今後は、CPythonのCIパイプラインにRISC-Vを直接統合し、開発者に即時フィードバックを提供するためのRISE RISC-V Runnersの導入が計画されています。また、tier 3からtier 2への移行を目指すとともに、RISC-Vの特長を活かしたパフォーマンス最適化の検討も進められています。コミュニティからのフィードバックを求められ、RISC-Vハードウェアを持つ開発者にCPythonのビルドとテストを呼びかける動きも見られます。

## 記事ごとの差分・視点の違い

記事1は、CPythonがRISC-Vをtier 3プラットフォームとして公式サポートを開始したことを発表したブログ記事であり、主に開発過程やコミュニティの貢献、RISEプロジェクトの支援について強調しています。また、今後の改善計画やCIパイプラインへの統合も触れています。  
記事2は、InfoQが掲載したニュース記事で、CPythonのRISC-Vサポートが公式に承認されたことを報じています。この記事では、コミュニティによるテストと修正の成果、RISEプロジェクトの支援、今後のTier 2への進展を目指す計画が強調されています。  
記事3は、STM32F446RE向けのRTOSカーネルプロジェクトの構造と実装について説明した記事で、カーネルの設計やディレクトリ構造、ビルドシステム、シミュレーション環境について詳しく紹介しています。  
記事4は、FreeRTOSのクイックスタートガイドで、RTOSの基礎知識やFreeRTOSのライブラリ、ツール、AWSとの統合について説明しています。  
記事5は、8051マイクロコントローラー向けのSDCCコンパイラの動作について解説した記事で、コンパイルプロセスやバイナリ生成、ハードウェアの特性について詳しく説明しています。

## 深掘り調査で得られた知見

CPythonは2026年8月24日にRISC-Vアーキテクチャをティア3プラットフォームとして公式にサポートすることを発表しました。この実現には、コミュニティの協力とテスト環境の整備が不可欠でした。特にRISEプロジェクトが提供したRISC-Vマシンは、ビルドボットとしての役割を果たし、アーキテクチャ固有の問題のデバッグにも貢献しました。また、CPythonのCIパイプラインにRISC-Vを直接統合するためのRISE RISC-V Runnersイニシアチブも進行中で、開発者に即時のフィードバックを提供する予定です。ティア3サポートは重要な進展ですが、今後はティア2への昇格を目指す計画が進められています。さらに、CPythonがRISC-Vプラットフォームでより効率的に動作するためのアーキテクチャ固有の最適化も検討されています。コミュニティからのフィードバックは、CPythonのRISC-Vサポートのさらなる改善に不可欠であり、RISC-Vハードウェアを持つ開発者にはテストと報告を呼びかけられています。この動きは、PythonがオープンなISAであるRISC-V上で安定して動作するための重要な一歩として注目されています。

## 不確実な点・追加確認が必要な点

記事間の比較から明らかなのは、RISC-VがCPythonで公式サポートされたという情報は、2026年8月24日にPython Insiderのブログで最初に発表され、その後、2026年9月10日にInfoQが同内容を確認した点です。この時点での情報は、CPythonの公式ドキュメントであるPEP 11にRISC-Vのサポートが正式に追加されたことを示しており、これはコミュニティによる協力とテストの結果としての成果です。一方で、他の記事（記事3〜5）は、RISC-Vとは無関係なRTOSやマイクロコントローラー関連の技術情報であり、テーマの中心であるCPythonのRISC-Vサポートとは直接的な関連性がありません。したがって、テーマ「RISC-V is now officially supported by CPython」に関する情報は、記事1と記事2の内容に限定されるため、他の記事はこのセクションの対象外です。また、記事1と記事2の記述は一致しており、CPythonのRISC-VサポートがTier 3プラットフォームとして正式に追加されたという事実を共有しています。ただし、具体的な公開日時や取得日時については、各記事の情報が不明であるため、時系列的な優先順位を明確に断定することはできません。

## 元記事一覧

- [RISC-V is now officially supported by CPython! | Python Insider](https://blog.python.org/2026/08/riscv-now-officially-supported/)
- [CPython Officially Adds RISC-V Support as a Tier 3 Platform](https://www.infoq.com/news/2026/09/riscv-cpython/)
- [Overview of theRTOSKernelProject - DEV Community](https://dev.to/cangulmez/overview-of-the-rtos-kernel-project-lca)
- [FreeRTOSKernelQuick Start Guide - FreeRTOS](https://freertos.org/Documentation/01-FreeRTOS-quick-start/01-Beginners-guide/02-Quick-start-guide)
- [8051WhatdoesSDCCdopart1? - DEV Community](https://dev.to/ddupard/8051-what-does-sdcc-do-part-1--2d1d)
