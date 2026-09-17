---
title: TTS選定の3軸が交差せず短リスト化
type: knowledge
status: draft
created: 2026-09-17
updated: 2026-09-17
confidence: medium
---

# TTS選定の3軸が交差せず短リスト化

## 結論

TTS APIの選定において、価格、トランスポート、コンプライアンスという3つの軸は独立しており、それぞれ異なる測定単位を持つため、ランキング形式では表現できない。これらの軸はフィルターとして機能し、組み合わせによって最終的なTTS APIが選定されるが、どの軸が優先されるかはケースバイケースであり、選定プロセスにおいて重要な役割を果たしている。

## テーマ概要

TTS（Text-to-Speech）APIの選定において、価格、トランスポート、コンプライアンスという3つの軸が互いに変換できないため、ランキング形式では表現できないという現象が注目されている。それぞれの軸は異なる測定単位を持ち、価格は百万文字あたりのコスト、トランスポートはストリーミングの方法、コンプライアンスは規制対応の有無など、それぞれが独立したフィルターとして機能する。このため、TTS APIの選定はこれらの軸の組み合わせによって行われ、どの軸が優先されるかによって最終的な選定が決まる。この現象は、複数の軸が重複して機能するため、選定プロセスにおいて重要な役割を果たしている。

## 共通して確認できる点

TTS APIの選定において、価格、トランスポート、コンプライアンスという3つの軸が互いに変換できないため、ランキング形式では表現できない。価格は1つの軸で、Google CloudとAmazon Pollyは1百万文字あたり4ドル、OpenAIのtts-1、Deepgram Aura-1、Inworld TTS-2 Flashは15ドル、Cartesiaは37.38ドルから50ドル、ElevenLabsは166.11ドル。トランスポートはWebSocketストリーミング、チャンクドREST、完了ファイルの3つの形状があり、それぞれの違いはアーキテクチャ的なものである。Amazon PollyはWebSocket TTS APIを持たないが、StartSpeechSynthesisStreamはHTTP/2で双方向ストリームをサポートしている。コンプライアンスでは、Google Cloud Text-to-SpeechはHIPAA BAAに名前が含まれており、AWSのPollyもHIPAA-eligibleサービスとしてリストされている。OpenAIはAPI向けにBAAを提供しており、Rimeは2024年2月からコンプライアンスを保証している。OpenAIのtts-1-hdモデルでは、英語の単語を正確に発音する際の高誤り率が報告されており、具体的な原因は未確認。TTS APIの選定において、これらの軸はフィルターとして機能し、交差することで最終的な選定が行われる。価格軸は、プロトタイプではノイズとなるが、年間1億文字の使用量では差額が大きくなる。トランスポート軸では、ストリーミングが必要なアプリケーションでは、OpenAIやGoogle Cloudがサポートしている。コンプライアンスでは、HIPAAなどの規制に合致するかどうかが重要であり、特定のサービスではコンプライアンス階層の価格が影響する。これらの軸は、選定プロセスにおいて重要なフィルターとなり、それぞれの組み合わせによって最終的なTTS APIが選定される。

## 記事ごとの差分・視点の違い

記事「Whenisitsafetoopenthemicrophone? Buildingarealtimevoice...」は、Twilioを用いた電話ボットにおけるマイクの制御に関する技術的な課題に焦点を当てている。著者は、TTSの終了タイミングをもとにマイクを開閉する方法が誤っており、ネットワーク遅延によりフィードバックループが発生する可能性があることを指摘。この問題は、実際の電話通話でのみ発生し、ローカル環境では検出が難しいという点を強調している。

記事「How to Build aVoiceAgentwithTwilioand AssemblyAI (2026)」では、TwilioとAssemblyAIを組み合わせた電話ボットの構築方法が詳述されている。ここでは、ストリーミングSTT、LLM、TTSの統合的なアーキテクチャと、800ms以内のレスポンスタイムを実現するための技術的工夫が説明されている。また、具体的なコードとデプロイガイドが提供されており、実践的な導入が可能であることを示している。

記事「Your TTS shortlist is three shortlists, and they barely intersect」は、TTS API選定における価格、トランスポート、コンプライアンスという3つの軸が互いに変換不可能であるため、ランキング形式では表現できないという点を論じている。著者は、これらの軸がフィルターとして機能し、それぞれの組み合わせによって最終的なTTS APIが選定されることを強調。また、各軸の具体的な価格や技術的な制限についても詳しく説明している。

記事「Tested Qwen3-TTS 1.7B locally:itspeaksGerman.Itcannotread...」では、Qwen3-TTS 1.7Bのドイツ語処理能力をテストした結果が報告されている。識別子（部品番号、通貨など）の処理が不完全で、テキスト再構成レイヤーを導入することで改善されるが、ゼロの脱線が発生しなかった点を強調。また、Amazon Pollyとの比較も行われ、ローカルでの合成には安定性と再構成レイヤーの導入が必要であると結論付けている。

記事「Your TTS Model Sounds Great — Until It Says "GPUB"」は、TTSモデルが特定の単語（例：GPUB）を誤って発音する問題を指摘。これは、構造的なチェックで対処可能であり、モデル自体に依存しないという点を強調。また、この問題が現実の電話通話において顕著に現れることを指摘し、ローカル環境では検出が難しいという点を述べている。

## 深掘り調査で得られた知見

TTS APIの選定において、価格、トランスポート、コンプライアンスという3つの軸が互いに変換できないため、ランキング形式では表現できないことが明らかになった。価格軸では、Google Cloud Text-to-SpeechとAmazon Pollyは1百万文字あたり4ドル、OpenAIのtts-1、Deepgram Aura-1、Inworld TTS-2 Flashは15ドル、Cartesiaは37.38ドルから50ドル、ElevenLabsは166.11ドルと幅が広がる。トランスポート軸では、WebSocketストリーミング、チャンクドREST、完了ファイルの3つの形状があり、それぞれの違いはアーキテクチャ的なものである。Amazon PollyはWebSocket TTS APIを持たないが、StartSpeechSynthesisStreamはHTTP/2で双方向ストリームをサポートしており、ストリーミングが必要なアプリケーションではOpenAIやGoogle Cloudが適している。コンプライアンスでは、Google Cloud Text-to-SpeechはHIPAA BAAに名前が含まれており、AWSのPollyもHIPAA-eligibleサービスとしてリストされている。OpenAIはAPI向けにBAAを提供し、Rimeは2024年2月からコンプライアンスを保証している。これらの軸はフィルターとして機能し、交差することで最終的な選定が行われる。価格軸では、プロトタイプではノイズとなるが、年間1億文字の使用量では差額が大きくなる。コンプライアンスでは、HIPAAなどの規制に合致するかどうかが重要であり、特定のサービスではコンプライアンス階層の価格が影響する。Qwen3-TTS 1.7BはApple Silicon上で動作し、ドイツ語のテキストを処理する際、識別子を途中で停止し、関係のないドイツ語を20秒間読み上げる現象が確認された。テキスト再構成レイヤーを導入することで、40のテスト文書のうち3つは読み上げられなかったが、ゼロの脱線が発生した。Amazon Pollyは同じテスト文書に対してゼロの脱線を示し、ローカルのテキスト合成には安定性と再構成レイヤーの導入が必要である。

## 不確実な点・追加確認が必要な点

記事間での情報の整合性を確認すると、TTS APIの選定において、価格、トランスポート、コンプライアンスという3つの軸がそれぞれ独立しており、これらは相互に変換できないため、ランキング形式では表現できないことが明確にされている。例えば、価格軸ではGoogle Cloud TTSとAmazon Pollyが1百万文字あたり4ドル、OpenAIのtts-1やDeepgram Aura-1、Inworld TTS-2 Flashが15ドル、Cartesiaが37.38ドルから50ドル、ElevenLabsが166.11ドルと幅広い価格帯が確認されている。一方、トランスポート軸では、WebSocketストリーミング、チャンクドREST、完了ファイルの3つの形状があり、それぞれの違いはアーキテクチャ的なものである。Amazon PollyはWebSocket TTS APIを持たないが、StartSpeechSynthesisStreamはHTTP/2で双方向ストリームをサポートしている。コンプライアンスでは、Google Cloud TTSはHIPAA BAAに名前が含まれており、AWSのPollyもHIPAA-eligibleサービスとしてリストされている。OpenAIはAPI向けにBAAを提供しており、Rimeは2024年2月からコンプライアンスを保証している。しかし、これらの軸はフィルターとして機能し、交差することで最終的な選定が行われる。価格軸は、プロトタイプではノイズとなるが、年間1億文字の使用量では差額が大きくなる。トランスポート軸では、ストリーミングが必要なアプリケーションでは、OpenAIやGoogle Cloudがサポートしている。コンプライアンスでは、HIPAAなどの規制に合致するかどうかが重要であり、特定のサービスではコンプライアンス階層の価格が影響する。これらの軸は、選定プロセスにおいて重要なフィルターとなり、それぞれの組み合わせによって最終的なTTS APIが選定される。ただし、記事間で具体的な選定プロセスや実際の選定結果については断定できない。

## 元記事一覧

- [Whenisitsafetoopenthemicrophone? Buildingarealtimevoice...](https://dev.to/petersoos/when-is-it-safe-to-open-the-microphone-building-a-realtime-voice-agent-on-twilio-3ddo)
- [How to Build aVoiceAgentwithTwilioand AssemblyAI (2026)](https://www.assemblyai.com/blog/build-voice-agent-twilio-assemblyai)
- [Your TTS shortlist is three shortlists, and they barely intersect - DEV Community](https://dev.to/aialleyway/your-tts-shortlist-is-three-shortlists-and-they-barely-intersect-jhf)
- [Tested Qwen3-TTS 1.7B locally:itspeaksGerman.Itcannotread...](https://dev.to/aws-builders/it-speaks-german-it-cannot-read-a-part-number-1lc6)
- [Your TTS Model Sounds Great — Until It Says "GPUB" - DEV Community](https://dev.to/bedvibe_studios/your-tts-model-sounds-great-until-it-says-gpub-1d77)
