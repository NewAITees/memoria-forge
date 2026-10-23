---
title: YouTubeタイムスタンプを活用したクロスデバイスワークアウト設計
type: knowledge
status: draft
created: 2026-10-24
updated: 2026-10-24
confidence: medium
---

# YouTubeタイムスタンプを活用したクロスデバイスワークアウト設計

## 何が分かったか

このページでは、調査資料から直接確認できた10件の事実を整理する。

## 確認できた事実

- TrainFlow treats timestamped video moments as reusable domain objects. [^fact-bac6be57527dad7b]

- A YouTube URL is a source reference, not an exercise definition. [^fact-1318d211f4af3e1a]

- The timestamp is stored as a number rather than as part of a formatted string. [^fact-ff067e80287a3be9]

- TrainFlow uses a Next.js App Router application with two distinct surfaces. [^fact-29d4024c14955f40]

- Desktop authoring benefits from density, while mobile execution benefits from focus. [^fact-8c92ced348f1e163]

- A routine becomes an ordered composition rather than a copied block of video metadata. [^fact-5458955e3aae6a9a]

- Referencing an action avoids duplicating the source URL and timestamp every time it appears. [^fact-b8f821e7ee1b6c9d]

- Ordering should be explicit to avoid surprising sessions. [^fact-9e31dd527c47dd19]

- A session is easier to reason about when it has explicit states. [^fact-1502bc3c18c403e9]

- TrainFlow separates desktop planning from mobile execution. [^fact-f78aadd79f277588]

## それが意味すること

これらの事実は、YouTubeのタイムスタンプを再利用可能なドメインオブジェクトとして扱い、URLを直接的な運動定義としてではなく参照として扱う設計思想を反映しています。また、タイムスタンプは数値として保存され、Next.jsのアプリケーション構造を用いてデスクトップとモバイルで異なるインターフェースを実装しています。この設計により、デスクトップでの作業効率とモバイルでの実行の集中を両立させ、セッションの順序を明示的に管理することで、ユーザーが予期せぬ動作を避けるようにしています。

## まだ分からないこと

これらの事実は、具体的な実装や技術的詳細については述べていません。また、システムの全体的な目的やユーザーのニーズに応じた設計選択については説明されていません。

## 出典

[^fact-bac6be57527dad7b]: [Designinga Cross-Device Workout WorkflowAroundYouTube...](https://dev.to/fenglq02/designing-a-cross-device-workout-workflow-around-youtube-timestamps-51f)
  - 根拠引用: 「While building TrainFlow , I have been exploring an architecture that treats timestamped video moments as reusable domain objects and separates desktop planning from mobile execution.」
[^fact-1318d211f4af3e1a]: [Designinga Cross-Device Workout WorkflowAroundYouTube...](https://dev.to/fenglq02/designing-a-cross-device-workout-workflow-around-youtube-timestamps-51f)
  - 根拠引用: 「A YouTube URL is a source reference, not an exercise definition. One video may contain a warm-up, three demonstrations, a progression, and a cooldown. The reusable unit is usually a moment inside the video.」
[^fact-ff067e80287a3be9]: [Designinga Cross-Device Workout WorkflowAroundYouTube...](https://dev.to/fenglq02/designing-a-cross-device-workout-workflow-around-youtube-timestamps-51f)
  - 根拠引用: 「A conceptual model can stay small: The timestamp is stored as a number rather than as part of a formatted string. That makes validation, sorting, duration calculations, and player integration easier.」
[^fact-29d4024c14955f40]: [Designinga Cross-Device Workout WorkflowAroundYouTube...](https://dev.to/fenglq02/designing-a-cross-device-workout-workflow-around-youtube-timestamps-51f)
  - 根拠引用: 「TrainFlow uses a Next.js App Router application with two distinct surfaces: This separation is more than responsive CSS. The two contexts have different jobs.」
[^fact-8c92ced348f1e163]: [Designinga Cross-Device Workout WorkflowAroundYouTube...](https://dev.to/fenglq02/designing-a-cross-device-workout-workflow-around-youtube-timestamps-51f)
  - 根拠引用: 「Desktop authoring benefits from density. Users compare sources, edit notes, reorder actions, and see the whole routine. Mobile execution benefits from focus. It should show the current action, the relevant video moment, a small number of controls, and a clear next step.」
[^fact-5458955e3aae6a9a]: [Designinga Cross-Device Workout WorkflowAroundYouTube...](https://dev.to/fenglq02/designing-a-cross-device-workout-workflow-around-youtube-timestamps-51f)
  - 根拠引用: 「Once actions are reusable, a routine becomes an ordered composition rather than a copied block of video metadata.」
[^fact-b8f821e7ee1b6c9d]: [Designinga Cross-Device Workout WorkflowAroundYouTube...](https://dev.to/fenglq02/designing-a-cross-device-workout-workflow-around-youtube-timestamps-51f)
  - 根拠引用: 「Referencing an action avoids duplicating the source URL and timestamp every time it appears. A routine item can carry a small override when the session context differs, while the core action remains reusable.」
[^fact-9e31dd527c47dd19]: [Designinga Cross-Device Workout WorkflowAroundYouTube...](https://dev.to/fenglq02/designing-a-cross-device-workout-workflow-around-youtube-timestamps-51f)
  - 根拠引用: 「Ordering should be explicit. Relying on creation time or database return order will eventually produce surprising sessions.」
[^fact-1502bc3c18c403e9]: [Designinga Cross-Device Workout WorkflowAroundYouTube...](https://dev.to/fenglq02/designing-a-cross-device-workout-workflow-around-youtube-timestamps-51f)
  - 根拠引用: 「A session is easier to reason about when it has explicit states. Even a small state machine is better than a collection of unrelated booleans.」
[^fact-f78aadd79f277588]: [DesigningaCross-DeviceWorkoutWorkflowAroundYouTube...](https://www.jobnewsfeed.site/2026/08/designing-cross-device-workout-workflow.html)
  - 根拠引用: 「While building TrainFlow , I have been exploring an architecture that treats timestamped video moments as reusable domain objects and separates desktop planning from mobile execution.」
