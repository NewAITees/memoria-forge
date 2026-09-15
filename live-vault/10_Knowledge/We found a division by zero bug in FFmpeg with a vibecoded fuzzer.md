---
title: FFmpegにおける割り算ゼロエラーのバグ発見
type: knowledge
status: draft
created: 2026-09-15
updated: 2026-09-15
confidence: medium
---

# FFmpegにおける割り算ゼロエラーのバグ発見

## 結論

FFmpegにおける割り算ゼロエラーのバグは、vibecodedというファジングツールを用いて発見され、libavformat/vpk.c内のvpk_read_packet関数でnb_channelsがゼロになる可能性があることからSIGFPEが発生する可能性があることが確認されました。このバグは、フォーマットプローブの誤検出やコードックパラメータのリセットによって生じる可能性があり、FFmpegのissue #24290で報告されています。修正案として、nb_channelsがゼロでないことを事前に確認するなどの対策が提案されており、libFuzzerとAddressSanitizerを用いたファジングによって複数の入力で再現可能です。

## テーマ概要

FFmpegに割り算ゼロ（division by zero）のバグが発見され、vibecodedという名前のファジングツールによって同定されたことが注目されている。このバグは、libavformat/vpk.cのvpk_read_packet関数内で、nb_channelsがゼロになる可能性があるため、割り算時にSIGFPEが発生する可能性がある。このバグは、フォーマットプローブの誤検出やコードックパラメータのリセットによって、nb_channelsがゼロになる可能性があるため、特定の条件下で発生する。このバグは、libFuzzerとAddressSanitizerを使用したファジングによって発見され、複数の入力で再現可能である。このバグの修正案には、nb_channelsがゼロでないことを確認した上で割り算を行うこと、空の最後ブロックをEOFとして返す、block_countがゼロでないことを確認することなどが含まれる。また、このバグはFFmpegのissue #24290で報告されており、修正案が提示されている。このバグの発見方法については、一部の資料ではAIを活用したファジングツールによるものと、手動によるものとが示唆されている。このバグの影響範囲や深刻度については、一部の資料では低から中程度の深刻度と評価されているが、他の資料では詳細な評価が示されていない。

## 共通して確認できる点

FFmpegにおいて、割り算ゼロのバグが発見されたことが複数の記事で確認されています。このバグは、libavformat/vpk.cのvpk_read_packet関数内で、par->ch_layout.nb_channelsで割り算を行う際に、nb_channelsがゼロである可能性があるため、SIGFPEが発生する可能性があるとされています。この問題は、format probingの誤検出やcodec parameter resetによって、nb_channelsがゼロになる可能性があるため、特定の条件下で発生します。また、このバグは、libFuzzerとAddressSanitizerを用いたfuzzingによって発見され、複数の入力で再現可能です。修正案として、nb_channelsがゼロでないことを確認した上で割り算を行うこと、空の最後ブロックをEOFとして返す、block_countがゼロでないことを確認することなどが提案されています。このバグは、FFmpegのissue #24290で報告されており、修正案が提示されています。また、このバグの発見には、AIを活用したfuzzerが使用された可能性があるとされています。

## 記事ごとの差分・視点の違い

記事「WefoundadivisionbyzerobuginFFmpegwithavibecodedfuzzer」は、FFmpegにおける割り算ゼロエラーのバグの存在を指摘し、その発見方法としてvibecoded fuzzingを強調しています。この記事は、技術的な詳細や修正案の提案に焦点を当てており、バグの影響範囲や深刻度については一部の資料で低から中程度と評価されていますが、他の資料では詳細が欠如しています。一方、「21 Bytes Can CrashFFmpeg: Inside theVibecodedFuzzerThat...」は、AIを活用したfuzzerの開発過程を強調し、その結果として得られたFFmpegのクラッシュケースを具体的に説明しています。この記事は、AIによるセキュリティ研究の進化と、その経済的な影響についても論じており、技術的な背景と社会的な影響を幅広く扱っています。また、「Community Feedback: GUI-based PQC file encryption & physical duress models · Issue #9 · bro256/Awesome-PQC-Resources」は、PQC（Post-Quantum Cryptography）関連のツール開発におけるコミュニティフィードバックや、物理的な脅威モデルへの対応を強調しています。この記事は、技術的な実装とセキュリティ設計の観点から、開発者向けの意見交換を促進しています。「GitHub - ForkbombEu/pqspread: Simple Post Quantum File Encryption · GitHub」は、具体的なツールの実装とその利用方法に焦点を当てており、ML-KEM-512やAES-GCMといったアルゴリズムの実装例を提供しています。この記事は、技術的な実装と利用方法を明確に説明し、ユーザーにとっての使いやすさを重視しています。最後に、「TheGTAVIleakisn't really aboutGTAVI— it's anextortionplaybook」は、GTA VIのリークが単なる情報漏洩ではなく、拠出行為（extortion）の一形態であることを指摘し、その背景にあるゲーム業界のデジタル化への批判や、セキュリティ研究者による類似事例の指摘を強調しています。この記事は、技術的な内容よりも社会的・経済的な側面に焦点を当てています。

## 深掘り調査で得られた知見

FFmpegにおける割り算ゼロエラーのバグは、vibecoded fuzzingによって発見され、特定の条件下でSIGFPEを引き起こす可能性があることが確認されました。このバグは、libavformat/vpk.c内のvpk_read_packet関数で、nb_channelsがゼロになる可能性があるため、割り算時に例外が発生する可能性があります。この問題は、フォーマットプロービングの誤検出やコーデックパラメータのリセットによって生じる可能性があり、FFmpegのissue #24290で報告されています。修正案としては、nb_channelsがゼロでないことを事前に確認し、空の最後ブロックをEOFとして返す、block_countがゼロでないことを検証するなどの対策が提案されています。このバグは、libFuzzerとAddressSanitizerを用いたファジングによって発見され、10種類の入力で再現可能です。また、AIを活用したファジングツールによって発見されたとされる情報もあり、セキュリティ研究におけるAIの活用が注目されています。

## 不確実な点・追加確認が必要な点

記事間の食い違いや資料からは断定できない点について、以下のようにまとめられます。

記事1と記事2は同一体の問題である「FFmpegにおける割り算ゼロエラーのバグ」を扱っており、両方とも同様の技術的背景と修正案を示しています。記事2では、AIを活用したfuzzerによるバグの発見が明記されており、記事1ではその点については言及されていません。このため、AIを活用したfuzzerによる発見がどの程度一般的か、あるいはこのバグの発見は単発的なものか、といった点は明確ではありません。

また、記事1と記事2が示す情報は、FFmpegのissue #24290に記載されている修正案や再現方法と一致しており、その信頼性は高いと考えられます。しかし、記事1では「2024年にもこの問題についての議論があった」という記述があり、記事2では「2024年11月に同様のガードがffmpeg-develメーリングリストで提案されていた」という情報が示されています。このため、このバグの存在は以前から認識されていた可能性があり、なぜ修正が行われなかったのか、あるいは修正が行われなかった理由についての詳細は不明です。

さらに、記事1と記事2の両方で同様のバグが報告されているにもかかわらず、記事3や記事4、記事5はこのバグとは関連性がなく、PQC（Post-Quantum Cryptography）やGTA VIのリークに関する情報となっています。このため、これらの記事はテーマと関係が薄く、本テーマの分析には関与していません。

## 元記事一覧

- [WefoundadivisionbyzerobuginFFmpegwithavibecodedfuzzer](https://news.ycombinator.com/item?id=49468642)
- [21 Bytes Can CrashFFmpeg: Inside theVibecodedFuzzerThat...](https://dev.to/jamilxt/21-bytes-can-crash-ffmpeg-inside-the-vibecoded-fuzzer-that-found-what-years-of-audits-missed-fpe)
- [Community Feedback: GUI-based PQC file encryption & physical duress models · Issue #9 · bro256/Awesome-PQC-Resources](https://github.com/bro256/Awesome-PQC-Resources/issues/9)
- [GitHub - ForkbombEu/pqspread: Simple Post Quantum File Encryption · GitHub](https://github.com/ForkbombEu/pqspread)
- [TheGTAVIleakisn't really aboutGTAVI— it's anextortionplaybook](https://dev.to/alvarito1983/the-gta-vi-leak-isnt-really-about-gta-vi-its-an-extortion-playbook-o1a)
