---
title: ESP32におけるパルス幅変調の実装と応用
type: knowledge
status: draft
created: 2026-10-04
updated: 2026-10-04
confidence: medium
---

# ESP32におけるパルス幅変調の実装と応用

## 結論

ESP32におけるPWM（パルス幅変調）の実装は、LEDC（LED Control）パーセリカルを介して行われており、最大4つのタイマと16チャネルを備えることで柔軟なPWM信号生成が可能である。PWMはデューティーサイクルと周波数を調整することで、平均電圧を制御し、デジタル信号を用いた擬似アナログ出力を作成する技術であり、LEDの明るさ制御やモータの速度制御など、幅広い用途に応用されている。また、MicroPythonを用いたPWMの実装も確認されており、パラメータの変更は次のPWMサイクルから有効となる点も明確である。

## テーマ概要

Pulse Width Modulation (PWM) は、デジタル信号を用いて擬似アナログ出力を作成する技術であり、ESP32ではLEDの明るさ制御やモータの速度制御など幅広い用途に利用されている。ESP32はLED Control（LEDC）パーセリカルを備えており、最大4つのタイマと16チャネルを提供し、柔軟なPWM信号生成が可能である。PWMは、デューティーサイクルと周波数を調整することで、平均電圧を制御し、電力の供給量を変えることが可能である。LEDCは、CPUレジスタではなくパーセリカルレジスタを介して制御され、`ledcSetup`、`ledcAttachPin`、`ledcWrite`などの関数を用いて設定と制御が行われる。また、MicroPythonでのPWM実装も確認されており、デューティーサイクルや周波数の変更が可能である。このようなPWM技術は、ESP32の多様な応用を支える重要な機能であり、今後も注目されている。

## 共通して確認できる点

ESP32はPWM（パルス幅変調）を実装するためにLEDC（LED制御）パーセリカルを採用しており、これは4つのタイマと16チャネルを備え、柔軟なPWM信号生成が可能である。LEDCは、タイマの設定、周波数と解像度の設定、デューティサイクルの定義を通じてPWM信号を生成する。PWM信号の基本的な特性は、デューティサイクル（ON時間の割合）と周波数（パルスの周期）であり、これらを変更することで平均電圧を制御し、アナログ出力を模倣する。ESP32のLEDCは、LEDの明るさ制御やモータ制御など、幅広い用途に利用可能であり、最大で28チャネルのPWMがサポートされている。また、特定のピン（~記号付き）はPWMをサポートしており、`ledcSetup`、`ledcAttachPin`、`ledcWrite`などの関数を用いて設定や制御が可能である。MicroPythonのドキュメンテーションでは、PWM信号の生成において、デューティサイクルと周波数が重要なパラメータとして扱われており、`PWM`オブジェクトを通じてピンにPWMを適用する方法が示されている。また、PWMパラメータの変更は次のPWMサイクルから有効となる点も確認されている。

## 記事ごとの差分・視点の違い

記事ごとの立場や強調点、論点の違いは以下の通りです。

記事「Esp32PwmOfEsp32|Esp32」は、ESP32のPWM実装に焦点を当て、LEDの明るさ制御やモーター制御など、PWMの応用例を具体的に説明しています。この記事では、ESP32のLEDC（LED Control）パーセリカルの仕様や、`ledcSetup`や`ledcAttachPin`などの関数の使用方法を詳しく解説しており、実践的なコード例も提供しています。また、PWMの基本的な概念であるパルス幅と周波数の関係についても説明しています。

記事「2.PulseWidthModulation— MicroPython latest documentation」は、MicroPython環境でのPWMの実装方法を説明しており、PWMの基本的な概念とそのパラメータ（周波数とデューティー比）について解説しています。この記事では、MicroPythonを用いたPWMの実行例を提供し、パラメータ変更後の効果を示すコード例も紹介しています。また、MicroPythonの最新開発版に関する注意点も記載されており、特定のバージョンのドキュメントへのアクセス方法も説明しています。

記事「GitHub - TidalImpact/LighthouseReckoning: AlightweightLoRamesh...」は、LoRaメッシュネットワークにおける通信ライブラリの実装について説明しており、PWMとは直接関係ありません。この記事では、ネットワーク内のノードが自動的にルートを決定し、パケットの信頼性を確保する仕組みについて説明しています。また、LighthouseReckoningライブラリがESP32とRP2040で動作することも記載されていますが、PWMの話題には触れていないため、テーマと関係が薄いです。

記事「LighthouseReckoning: ALightweightLoRaMeshNetworkfor...」も、LoRaメッシュネットワークに関する技術的な説明が中心で、PWMとは直接関係がありません。この記事では、ネットワークの構築方法や、パケットのルーティング、リトライ、ループ回避などの問題解決策について説明しています。また、LighthouseReckoningライブラリがArduino互換マイクロコントローラーで動作することを強調しており、PWMの話題には触れていません。

記事「Pi4JLEDPlayground: A Community Resource for...」は、Javaを用いたハードウェアプログラミングに関するリソースであり、PWMとは直接関係がありません。この記事では、LEDのアニメーションや色、明るさの調整など、GPIOの操作に関する情報が提供されていますが、ESP32のPWMについての説明は含まれていません。

## 深掘り調査で得られた知見

ESP32はPWM（パルス幅変調）を実装するためにLEDコントロール（LEDC）パーセリカルを採用しており、これにより柔軟なPWM信号生成が可能である。LEDCは4つのタイマと16チャネルを備え、PWM周波数は1Hzから40MHzまで設定可能で、解像度は1〜16ビットの範囲で調整できる。デューティサイクルはON時間と周期の比率であり、これにより平均電圧を制御し、アナログ出力の擬似を実現する。LEDCはLEDの明るさ制御やモーター制御など、幅広い用途に利用される。また、ESP32では28チャネルのPWMがサポートされており、ピンの記号「~」がPWMをサポートしていることを示している。  

PWMの実装には、`ledcSetup`、`ledcAttachPin`、`ledcWrite`などの関数がよく使用される。これらの関数を用いることで、PWMの設定や制御が簡潔かつ柔軟に行える。MicroPythonでは、`PWM`クラスを用いてPWM信号を生成し、デューティサイクルや周波数を調整することができる。また、新しいPWMパラメータは次のPWMサイクルから有効となる点に注意が必要である。  

さらに、ESP32ではPWMを用いたLEDのフェードイン・フェードアウトや、ポテンショメータによるLED明るさ制御などの応用例が記載されている。これらの例は、PWMの基本的な動作を理解し、実際の応用に移行するための参考となる。また、LEDCは高度な機能を備えており、自動的に暗めたりするなどの機能が可能である。これにより、ESP32のPWMは単なるLED制御にとどまらず、さまざまな用途に応じた柔軟な制御が可能である。

## 不確実な点・追加確認が必要な点

記事間の食い違いや、資料からは断定できない点を以下のように具体的に述べます。

まず、ESP32におけるPWMの実装について、記事1と記事2の内容は一致しています。両記事ともPWMの基本概念を説明し、ESP32のPWM機能に関する具体的な説明を含んでいます。特に記事1では、LEDの明るさ制御やモータ制御など、PWMが使われる用途についても触れています。一方、記事2はMicroPythonを用いたPWMの実装方法を説明しており、PWMのパラメータ（周波数、デューティー比）の設定や、PWM波形の観測方法についても具体的に記載しています。ただし、記事2ではESP32のPWMに関する詳細な設定や、具体的なコード例は含まれていません。

一方、記事3と記事4はPWMとは関係のないLoRaメッシュネットワークに関する内容であり、PWMの話題とは直接関係がありません。記事5はJavaを用いたハードウェアプログラミングに関する内容であり、PWMとは関係がありません。したがって、PWMに関する情報を得るためには、記事1と記事2に焦点を当てることが必要です。

また、記事1と記事2の内容を比較すると、PWMの設定方法や、デューティー比の変化に関する説明は一致していますが、記事1ではESP32のPWMチャンネル数やピンのサポート状況についても記載されており、記事2にはそのような情報は含まれていません。したがって、PWMの実装に関する詳細な情報は、記事1に含まれている可能性があります。一方、MicroPythonを用いたPWMの実装方法については、記事2が詳細に説明しています。

さらに、記事1と記事2の情報は、PWMの基本的な概念や実装方法についての説明にとどまり、ESP32のPWM機能に関する最新の情報を含んでいるかは不明です。したがって、PWMに関する最新の情報や、具体的な実装例については、さらなる調査が必要です。

## 元記事一覧

- [Esp32PwmOfEsp32|Esp32](https://www.electronicwings.com/esp32/pwm-of-esp32)
- [2.PulseWidthModulation— MicroPython latest documentation](https://docs.micropython.org/en/latest/esp32/tutorial/pwm.html)
- [GitHub - TidalImpact/LighthouseReckoning: AlightweightLoRamesh...](https://github.com/TidalImpact/LighthouseReckoning)
- [LighthouseReckoning: ALightweightLoRaMeshNetworkfor...](https://dev.to/fynn_schulz_8dad41ee4e7b/lighthousereckoning-a-lightweight-lora-mesh-network-for-arduino-esp32-and-rp2040-50oh)
- [Pi4JLEDPlayground: A Community Resource for... - DEV Community](https://dev.to/igoriot/pi4j-led-playground-a-community-resource-for-learning-hardware-programming-with-java-2ip3)
