---
title: HTMLキャンバスが画像メタデータを削除する仕組み
type: knowledge
status: draft
created: 2026-10-26
updated: 2026-10-26
confidence: medium
---

# HTMLキャンバスが画像メタデータを削除する仕組み

## 何が分かったか

iPhoneやカメラデバイスは通常、画像の向きをEXIF方向フラグで記録します[^fact-3a6176af0d04030a]。HTMLキャンバス処理ではこの方向フラグが削除され、画像が永久的に回転エラーになる可能性があります[^fact-56f27325d66a477a]。ブラウザは<img>プレビューで方向フラグを自動適用するため、問題が見えず、キャンバス処理後に初めて影響が現れます[^fact-d814c367d46c78e1]。

## 確認できた事実

- iPhone和其他相机设备通常不会旋转像素，而是存储图像的原生方向并设置EXIF方向标志。 [^fact-3a6176af0d04030a]

- 当图像通过canvas处理时，方向标志会被删除，导致图像永久旋转错误。 [^fact-56f27325d66a477a]

- 問題なのは、<img>プレビューでは問題ないため、ブラウザが表示する際に入力時にオリエンテーションフラグを適用しているからです。キャンバスのリンドラップ後になって初めて問題が発生します。 [^fact-d814c367d46c78e1]

- あるいは、<img>要素を描画する場合、CSS image-orientation: from-image（現代のブラウザでのデフォルト）で表示を修正できますが、drawImageが読み取る内容は変わりません。drawImageは依然としてraw pixelsを読み取ります。そのため、キャンバス作業ではcreateImageBitmapを使用し、imageOrientation: "from-image"を指定するのが信頼できる方法です。 [^fact-740bbddda3bfc11e]

## それが意味すること

画像の向きが正しく表示されない可能性があるため、特に印刷やその他の用途で問題になる場合があります。drawImageは依然としてraw pixelsを読み取り、createImageBitmapを使用してimageOrientation: "from-image"を指定することが信頼できる方法とされています。 [^fact-740bbddda3bfc11e]

## まだ分からないこと

具体的な回転エラーの条件や、問題が発生する際の詳細なシナリオについては明確ではありません。

## 出典

[^fact-3a6176af0d04030a]: [TheHTMLcanvasquietlydeletesyourphoto'smetadata—and...](https://dev.to/bellsal_b44bf6d/the-html-canvas-quietly-deletes-your-photos-metadata-and-one-day-that-bites-you-2h68)
  - 根拠引用: 「Here's the one that generates the confused bug reports. iPhones (and many other cameras) don't rotate the pixels when you turn the phone. They store the image in the sensor's native orientation and set an EXIF Orientation flag — "display this rotated 90°." Your photo viewer reads that flag and rotates on display. The pixels themselves are sideways.」
[^fact-56f27325d66a477a]: [TheHTMLcanvasquietlydeletesyourphoto'smetadata—and...](https://dev.to/bellsal_b44bf6d/the-html-canvas-quietly-deletes-your-photos-metadata-and-one-day-that-bites-you-2h68)
  - 根拠引用: 「Now send that image through a canvas. The canvas draws the raw pixels — sideways — and the orientation flag, like all metadata, is dropped. Your output is a photo that is now permanently rotated the wrong way, with no flag left to correct it.」
[^fact-d814c367d46c78e1]: [TheHTMLcanvasquietlydeletesyourphoto'smetadata—and...](https://dev.to/bellsal_b44bf6d/the-html-canvas-quietly-deletes-your-photos-metadata-and-one-day-that-bites-you-2h68)
  - 根拠引用: 「The infuriating part is that it looks fine in your <img> preview, because the browser applied the orientation flag when it displayed the original. It only breaks after the canvas round-trip. So the user sees a correct preview, downloads the result, and it's rotated. Classic "works on my screen."」
[^fact-740bbddda3bfc11e]: [TheHTMLcanvasquietlydeletesyourphoto'smetadata—and...](https://dev.to/bellsal_b44bf6d/the-html-canvas-quietly-deletes-your-photos-metadata-and-one-day-that-bites-you-2h68)
  - 根拠引用: 「Or, if you draw an <img> element instead, CSS image-orientation: from-image (the default in modern browsers) fixes the display — but not what drawImage reads. drawImage still takes the raw pixels. So for canvas work, createImageBitmap with imageOrientation: "from-image" is the reliable route.」
