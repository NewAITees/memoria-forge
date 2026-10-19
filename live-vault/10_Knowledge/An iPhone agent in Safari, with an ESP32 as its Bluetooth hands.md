---
title: iPhoneをAIで操作する技術とESP32の活用
type: knowledge
status: draft
created: 2026-10-20
updated: 2026-10-20
confidence: medium
---

# iPhoneをAIで操作する技術とESP32の活用

## 結論

iPhoneをAIモデルで制御する技術として、ESP32をBluetooth Low Energyで接続し、タップやキーボード入力を行う仕組みが実現されており、特にSafariを介したウェブインターフェースとESP32の組み合わせが注目されている。また、ESP32-S3を用いた直接の画面操作や音声認識エンジンの導入も進んでおり、AIとIoTの融合を加速させる重要な技術としての位置づけが明確になっている。

## テーマ概要

iPhoneの操作をAIモデルで行うための技術的アプローチとして、Safariを介したウェブインターフェースとESP32を組み合わせた「iPhone Agent Harness」というプロジェクトが注目されています。このプロジェクトでは、iPhoneの画面をSafariでキャプチャし、ビジョンモデルが画面を解析してタスクを実行し、ESP32を介してタップやキーボード入力などの操作を提供します。ESP32はBluetooth Low Energyを介してiPhoneと通信し、USB HIDとして認識されるため、AssistiveTouchを有効にすることでマウス操作をタップやスワイプとして再現します。この技術は、iPhoneの操作を自動化し、AIモデルが物理デバイスと直接対話する可能性を示しており、特にiOS18以降の環境で動作可能であることから、今注目されています。また、同様のコンセプトを実現する「esp32-iphone-agent」というオープンソースプロジェクトも存在し、ESP32-S3ボードを用いてiPhoneの画面を鏡のように表示し、AIモデルにアクションを送信する仕組みを提供しています。このような技術は、スマートデバイスとAIの連携を進める上で重要な役割を果たしており、今後の開発に期待が寄せられています。

## 共通して確認できる点

複数の記事から共通して確認できる事実として、iPhoneをAIモデルで制御するための実装が進められていることが明確です。具体的には、ESP32を Bluetooth Low Energy で iPhone と接続し、タップやキーボード入力などの操作を提供する仕組みが紹介されています。また、iPhone Agent Harness と ESP32-iPhone-Agent は、それぞれ異なるアプローチを採用しており、前者は Safari を介して画面を検出し、後者は AirPlay を用いて画面を鏡のように表示して操作を行います。これらのプロジェクトは、iPhone の自動ロックを無効にしないと画面の表示が停止するなどの制限も存在しており、特定の敏感なコンテンツ（パスコード入力、Apple Pay、DRM保護された動画など）の操作には制限があります。さらに、ESP32-iPhone-Agent は、USB HID で iPhone にマウスとキーボードとして認識され、AssistiveTouch を有効にすることで、マウスクリックがタップ、ドラッグがスワイプとして動作します。また、Oído という ESP32-S3 用の音声認識エンジンも、オープンソースで動作し、英語のオープンボキャブラリ音声をテキストに変換する機能を持っています。これらの技術は、AI と IoT の融合を進めるための重要な一環として注目されています。

## 記事ごとの差分・視点の違い

記事「An iPhone agent in Safari, with an ESP32 as its Bluetooth hands」は、Safariを介したウェブインターフェースでiPhoneのタスクを制御する仕組みを実装しており、ESP32を入力橋として利用する点が特徴的です。このアプローチでは、iPhone自身が画面キャプチャやモデルとのやり取りを担い、ESP32はBluetooth HIDを通じてタップやキーボード入力を提供します。一方、「GitHub - onehumanbeing/esp32-iphone-agent」は、ESP32-S3を直接iPhoneの画面を鏡のように表示し、AIモデルにアクションを送信する仕組みを採用しており、AirPlayやUSB HIDを活用した制御が可能となっています。また、「LLMsConfidentlyLieAboutYourMicrocontroller- DEV Community」では、LLMがマイクロコントローラーの詳細なボード固有情報について誤って説明する問題点を指摘し、これを解決するための「スキル」の収集と整理が提案されています。「AI Hallucination: WhyLLMsConfidentlyLie| by Anushka... | Medium」は、LLMがパターン認識と統計を基に次元を予測する仕組みのため、事実とは異なる情報を生成する傾向があることを説明しています。最後に、「Oído: open-source speech recognition for the ESP32-S3, without a command list」は、ESP32-S3上で動作する音声認識エンジンであり、命令リストを必要とせず、オープンボキャブラリの英語音声をテキストに変換する点が特徴的です。各記事は、それぞれ異なる技術的アプローチや課題に焦点を当て、LLMの限界や、ESP32を活用した制御方法、音声認識技術の進展といった視点から情報を提供しています。

## 深掘り調査で得られた知見

iPhone Agent HarnessとESP32-iPhone-Agentは、iPhoneをAIモデルで制御するための異なるアプローチを採用しています。iPhone Agent Harnessは、Safariを介してiPhoneのタスクを記述し、ビジョンモデルが画面を検査し、ESP32を介してタップやキーボード入力を提供する仕組みを実装しています。一方、ESP32-iPhone-Agentは、iPhoneをAIモデルで直接制御するための低コストソリューションであり、ESP32-S3ボードを使用して、iPhoneの画面を確認してタップやスワイプ、タイピングを行います。ESP32-iPhone-Agentは、jailbreakやApple開発者アカウントを必要とせず、OpenAI互換のビジョンモデルをサポートしています。また、AirPlayで画面を鏡のように表示し、Bluetooth Low EnergyでiPhoneアプリにH.264ストリームを送信する仕組みも備えています。さらに、USB HIDでiPhoneにマウスとキーボードとして認識され、AssistiveTouchを有効にすることで、マウスクリックがタップ、ドラッグがスワイプとして動作します。ただし、iPhoneの特定の敏感なコンテンツ（パスコード入力、Apple Pay、DRM保護された動画など）の画面を鏡のように表示することはできません。また、iPhoneの自動ロックを無効にしないと、画面の鏡のように表示が停止します。ESP32-iPhone-Agentは、ASCII文字に限定され、ランドスケープアプリケーションはサポートされていません。一方、iPhone Agent Harnessは、Safariを介したウェブインターフェースで設定を行い、ESP32のファームウェアはChromeやEdgeからインストールできます。両者の違いは、iPhone Agent HarnessがSafariでスクリーンキャプチャを取得し、選択したコンテキストをAIプロバイダーに送信するのに対し、ESP32-iPhone-AgentはiPhoneアプリで画面ストリームをデコードし、AIモデルにアクションを送信する点にあります。また、ESP32-iPhone-Agentは、iPhoneアプリで画面ストリームをデコードし、AIモデルにアクションを送信する仕組みを採用しており、iPhone Agent Harnessとは異なるアプローチを取っています。さらに、ESP32-iPhone-Agentは、iPhoneアプリで画面ストリームをデコードし、AIモデルにアクションを送信する仕組みを採用しており、iPhone Agent Harnessとは異なるアプローチを取っています。

## 不確実な点・追加確認が必要な点

記事間では、iPhoneをAIモデルで制御するためのアプローチや技術的実装にいくつかの違いが見られます。記事1と記事2は、どちらもESP32をiPhoneと連携させる技術を紹介していますが、実装方法や使用するインターフェースが異なっています。記事1では、Safariを介してiPhoneのタスクを記述し、ビジョンモデルが画面を検査し、ESP32を介して入力を行う仕組みが説明されています。一方、記事2では、ESP32-S3ボードをAirPlay受信機およびマウスとして動作させ、iPhoneアプリ内で画面ストリームをデコードし、AIモデルにアクションを送信する方法が示されています。また、記事2では、iPhoneアプリを介した操作が可能であり、ESP32はiPhoneのWi-Fiネットワークに接続される必要があります。一方で、記事1では、ESP32がBluetoothでiPhoneに接続され、Wi-Fiネットワークを共有する必要があるとされています。さらに、記事1では、iPhone Agent Harnessはブラウザベースのインターフェースで設定が行われる一方、記事2では、ESP32 AgentはiPhoneアプリ内で動作し、設定プロセスがアプリ内に統合されています。また、記事3では、LLMsがマイクロコントローラーに関する知識をもつものの、特定のボードに関する詳細な情報は持たず、これはAIのhallucinationのリスクとして指摘されています。記事4では、LLMsがパターン認識と統計を基に次に来る単語を予測する仕組みであり、これはAIのhallucinationの原因となるとされています。記事5では、OídoというESP32-S3用の音声認識エンジンが紹介されており、英語のオープンボキャブラリ音声をテキストに変換する機能を持ち、PSRAMを必要とするなど、特定のハードウェア要件が明記されています。これらの記事は、それぞれ異なる観点から、ESP32とiPhoneの連携技術やAIモデルの活用方法について述べていますが、技術的な実装や使用条件にはいくつかの違いがあります。

## 元記事一覧

- [An iPhone agent in Safari, with an ESP32 as its Bluetooth hands](https://dev.to/_14956125ac497ae131f60/an-iphone-agent-in-safari-with-an-esp32-as-its-bluetooth-hands-a8d)
- [GitHub - onehumanbeing/esp32-iphone-agent: Let an AI model ...](https://github.com/onehumanbeing/esp32-iphone-agent)
- [LLMsConfidentlyLieAboutYourMicrocontroller- DEV Community](https://dev.to/__3ed627f/llms-confidently-lie-about-your-microcontroller-17ap)
- [AI Hallucination: WhyLLMsConfidentlyLie| by Anushka... | Medium](https://medium.com/@anushka.sonawane/ai-hallucination-why-llms-confidently-lie-0d48fcee8fb8)
- [Oído:open-sourcespeechrecognition for theESP32-S3, without...](https://dev.to/danivs10/oido-open-source-speech-recognition-for-the-esp32-s3-without-a-command-list-2n48)
