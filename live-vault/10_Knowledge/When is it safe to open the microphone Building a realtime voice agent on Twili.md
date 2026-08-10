---
title: When is it safe to open the microphone? Building a realtime voice agent on Twilio
created: 2026-08-10
updated: 2026-08-10
---

## 概要
Twilio を使用したリアルタイムの音声アシスタントを構築する際、マイクを開くタイミングを安全に決定する方法を説明します。このプロセスには、音声の遅延とフィードバックループの回避が含まれます。

## 詳細

### 音声処理の流れ
Twilio Media Streams は WebSocket を使用して音声を提供し、STT（音声認識）に送信します。STT の出力は LLM（大規模言語モデル）に送られ、LLM の出力は TTS（テキスト読み上げ）に送られ、最終的に Twilio に送信されます。

### マイクの制御
マイクは、音声の出力が終了した後でも、ネットワークや電話サービスプロバイダーのバッファの影響で、ユーザーがまだ音声を聞いている可能性があります。このため、マイクを開くタイミングは、TTS の出力が完全に届いたタイミングでなければなりません。

### Twilio の mark frame
Twilio は mark frame を提供し、音声が届いたタイミングを確認できます。この mark frame を使用して、マイクが開くタイミングを決定できます。

### 他の条件
マイクの制御には、以下の条件が追加で必要です：
- 音声の遅延を考慮する
- フィードバックループを回避する
- ユーザーからの明示的な確認を待つ

## ソース
- [Whenisitsafetoopenthemicrophone? Buildingarealtimevoice...](https://dev.to/petersoos/when-is-it-safe-to-open-the-microphone-building-a-realtime-voice-agent-on-twilio-3ddo)
- [How to Build aVoiceAgentwithTwilioand AssemblyAI (2026)](https://www.assemblyai.com/blog/build-voice-agent-twilio-assemblyai)
- [CallAssistant: A PhoneAgentonTwilioandRealtimeVoice](https://agenticschool.dev/builds/callassistant)
- [TwilioSetup Made EASY forVoiceAI (Vapi xTwilio) - YouTube](https://www.youtube.com/watch?v=YS7cYaSHswU)
- [BuildaVoiceand SMS AIAgentwithTwilioAgentConnect... |Twilio](https://www.twilio.com/en-us/blog/developers/tutorials/integrations/voice-sms-ai-twilio-agent-connect-microsoft-azure)

## 注意点
- マイクを開くタイミングは、ネットワークや電話サービスプロバイダーのバッファの影響を考慮する必要があります。
- フィードバックループを回避するため、TTS の出力が完全に届いたタイミングでマイクを開く必要があります。
- ユーザーからの明示的な確認を待つことで、誤った行動を防ぐことができます。

# When is it safe to open the microphone Building a realtime voice agent on Twili


## 出典


## 未解決点

- 追加調査が必要です。
