---
title: Windows 11 25H2以降、HEICはWICコデックでデコード可能
type: knowledge
status: draft
created: 2026-10-13
updated: 2026-10-13
confidence: medium
---

# Windows 11 25H2以降、HEICはWICコデックでデコード可能

## 結論

Windows 11 25H2以降は、HEICファイルのデコードおよびエンコードに必要なWICコデックが標準搭載され、ImageMagickのインストールは不要となった。しかし、ブラウザではHEICのデコードがサポートされておらず、libheifライブラリやWebAssemblyを用いたデコードが必要であり、すべてのブラウザが対応しているわけではない。また、HEICファイルをJPEGに変換する場合、WICコデックを使用することができるが、通常JPEGファイルはHEICよりもサイズが大きい。これらの事実は、HEICファイルの利用や共有において、プラットフォームごとのサポート状況や技術的制約を理解する上で重要である。

## テーマ概要

WindowsがHEIC形式の画像をデコードおよびエンコードできるが、ブラウザではデコードができないという現象が注目されている。HEICはAppleのiPhoneで使用される高効率画像ファイル形式であり、JPEGよりも少ないストレージで高品質な画像を保存できる。しかし、HEICファイルをブラウザで表示するには、WebAssemblyを用いたlibheifライブラリが必要であり、すべてのブラウザがサポートしているわけではない。また、HEICファイルをJPEGに変換する際には、WindowsのWICコデックを使用できるが、通常JPEGはHEICよりも大きい。このため、HEICファイルの扱いやブラウザとの互換性が議論されている。

## 共通して確認できる点

Windows 11 25H2以降は、HEICファイルをデコードおよびエンコードするためのWICコデックが提供されており、ImageMagickのインストールは不要である。HEICはAppleのiPhoneで使用される高効率画像ファイル形式であり、JPEGよりも少ないストレージで高品質な画像を保存する。ただし、HEICファイルをブラウザで表示するには、WebAssemblyを用いたlibheifライブラリが必要である。また、WindowsではHEIF/HEVCメディア拡張機能をインストールすることで、ファイルエクスプローラーでHEICファイルのサムネイルを表示できるようになる。一方で、ブラウザではHEICのデコードがサポートされていないため、HEICファイルを表示するには、外部のライブラリやサーバーにアップロードする必要がある。ICCプロファイルの喪失がサムネイルの色合いの変化を引き起こす可能性があり、JPEGの品質設定を変更しても色合いが改善されない場合がある。1ビットの誤りが発生した画像ファイルでは、PNGは完全に破損し、JPEGは誤りが隠蔽される一方で、BMPは誤りが検出されない。これらの事実は、HEIC、JPEG、PNGなどの画像形式の違いや、各プラットフォームでのサポート状況を理解する上で重要である。

## 記事ごとの差分・視点の違い

記事「Windows can decode (and encode) HEIC without ImageMagick - but your browser can't decode it at all」は、Windows環境でのHEICファイルのデコード・エンコード機能と、ブラウザでの制限について詳述しており、特にWindows 11 25H2以降のWICコデックの導入を強調している。一方、記事「What is HEIC? iPhone Photos, Windows, and Alternatives」は、HEICの概要とWindowsでの対応状況を解説し、HEICがiPhoneで広く使用されている理由や、Windowsでのサポート状況について説明している。記事「Your thumbnails look washed out: it's the ICC profile, not JPEG quality」は、サムネイルの色合いの問題がICCプロファイルの喪失によるものであることを指摘し、JPEGの品質設定ではなく、プロファイルの保持が重要であると主張している。記事「PNG admits when it is damaged and JPEG does not」は、1ビットの誤りが画像ファイルに与える影響を形式ごとに検証し、PNGが誤りを検出する一方でJPEGは誤りを隠蔽するという違いを強調している。これらの記事は、それぞれ異なる視点から画像ファイル形式の特徴や、Windowsとの互換性、ブラウザの制限、色再現性の問題などについて論じており、HEICやJPEG、PNGなどの形式の違いや、それぞれの利点・欠点を比較・検討している。

## 深掘り調査で得られた知見

Windows 11 25H2以降は、HEICファイルのデコードおよびエンコードに必要なWICコデックが標準で提供されるようになった。これにより、ImageMagickのインストールが不要となり、HEICファイルをローカルで処理することが可能となった。ただし、ブラウザでのHEICファイルのデコードには、WebAssemblyを用いたlibheifライブラリが必要であり、すべてのブラウザがサポートしているわけではない。また、HEICファイルをJPEGに変換する際には、WICコデックを使用することができるが、通常JPEGファイルはHEICよりもサイズが大きい。HEICファイルをブラウザで表示するには、libheifライブラリやWebAssemblyを用いたデコードが必須であり、特定のブラウザではサポートされていない場合がある。一方、HEICファイルのエンコードはHEVCのライセンス問題を考慮した上で、無料ツールでの実装は困難である。また、HEICファイルをJPEGに変換する際のファイルサイズに関する情報は、HEICが通常JPEGよりも小さいとされているが、実際の変換結果はデバイスや設定に依存する。これらの情報は、Windows環境でのHEICファイル処理に必要な技術的背景を示しており、HEICファイルの利用や共有において重要な考慮点となる。

## 不確実な点・追加確認が必要な点

記事間では、HEICファイルのデコードやエンコードに関する情報が一致していない点が確認できた。記事1では、Windows 11 25H2以降はWICコデックを搭載しており、ImageMagickを必要としないとされている。一方で、記事2では、WindowsがHEICデコード機能を標準搭載していないことや、Storeからオプションでインストールする必要があるとされている。このため、HEICファイルのデコードやエンコードが可能かどうかは、Windowsのバージョンや設定によって異なる可能性がある。また、記事1では、ブラウザがHEICをデコードできない理由として、WebAssemblyを用いたlibheifライブラリの必要性が挙げられているが、記事2では、ブラウザがHEICをサポートしている例も示されている。このため、HEICファイルのブラウザでの表示には、ブラウザのサポート状況や設定に依存する可能性がある。さらに、記事1と記事2では、HEICファイルの変換時に生じるファイルサイズの違いについても異なった記述があるため、HEICからJPEGへの変換時のファイルサイズの変化は、デバイスや設定により異なる可能性がある。

## 元記事一覧

- [Windowscandecode(andencode)HEICwithoutImageMagick...](https://dev.to/_8729c5bde46be2/windows-can-decode-and-encode-heic-without-imagemagick-but-your-browser-cant-decode-it-at-all-51ca)
- [What isHEIC? iPhone Photos,Windows, and Alternatives — Labmorf](https://labmorf.com/heic/)
- [Your thumbnails look washed out: it's the ICC profile, not ...](https://dev.to/iterandum/your-thumbnails-look-washed-out-its-the-icc-profile-not-jpeg-quality-4mh7)
- [Your thumbnails look washed out: it's the ICC profile, not ...](https://thenote.app/post/en/your-thumbnails-look-washed-out-its-the-icc-profile-not-jpeg-quality-4rnx9fld70)
- [PNGadmits when it is damaged andJPEGdoes not - DEV Community](https://dev.to/remdore/i-flipped-one-bit-in-an-image-file-png-died-jpeg-lied-35b3)
