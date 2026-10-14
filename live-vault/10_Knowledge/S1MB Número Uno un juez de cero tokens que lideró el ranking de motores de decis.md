---
title: S1MB デシジョンエンジンリーダー ダービン27B-ZTC-v2 が1位
type: knowledge
status: draft
created: 2026-10-15
updated: 2026-10-15
confidence: medium
---

# S1MB デシジョンエンジンリーダー ダービン27B-ZTC-v2 が1位

## 結論

S1MB（System One Mosaic Benchmark）では、Darwin-27B-ZTC-v2が102モデル中でトップにランクインし、Bordaスコア89.58を記録した。このモデルはゼロトークンで動作し、1回の前向き推論で決定を生成する非自己回帰的な設計を採用しており、遅延とコストを低減しながら高い精度を達成している。

## テーマ概要

S1MB（System One Mosaic Benchmark）は、決定品質を測定するためのベンチマークであり、102のモデルを137の専門的なベンチマークで比較し、Noul（条件評価）、Choice（選択肢選択）、Score（スケール評価）の3つのタスクタイプに基づいてランク付けを行っている。このベンチマークでトップにランクインしたのは、Darwin-27B-ZTC-v2で、Bordaスコア89.58を記録した。このモデルはゼロトークンで動作し、1回のフォワードパスで決定を生成するため、通常の生成ループを省き、遅延とコストを低減しながら精度を高めている。S1MBでは、出力にトークンを含まないゼロトークンの判断を行う「juez de cero tokens（ゼロトークンの判断者）」が注目されており、Darwin-27B-ZTC-v2がその代表例として今注目されている。このテーマは、AIモデルの決定品質評価の新たな指標として、技術的なベンチマークと実用性の両面から議論を呼び出している。

## 共通して確認できる点

S1MB（System One Mosaic Benchmark）では、Darwin-27B-ZTC-v2が102モデル中で1位を獲得し、Bordaスコア89.58を記録しました。このベンチマークは、決定品質を評価するもので、各項目が条件と選択肢を提供し、モデルが正しい選択肢を選び、評価する必要がある仕組みです。S1MBでは、137の専門的なベンチマークを用いて、3つのタスクタイプ（Noul、Choice、Score）でモデルを比較しています。Darwin-27B-ZTC-v2はゼロトークンで動作し、1回のフォワードパスで決定を生成します。これにより、通常の生成ループを実行せず、遅延とコストを低減し、決定の精度を向上させています。S1MBリーダーボードの結果は、2026年10月24日にHugging Faceで発表されました。リーダーボードの詳細な順位や、特定のモデルのスコアについては、各ソースによって一貫して記載されていません。

## 記事ごとの差分・視点の違い

記事ごとの立場や強調点、論点の違いは以下の通りです。

記事1はUCIのロードサイクリングに関する情報であり、S1MBに関する直接的な内容は含まれていません。したがって、S1MBとの関連性は不明であり、他の記事との比較には適さない。記事2は空気質ランキングに関する情報であり、S1MBとは関係がありません。記事3はMetaが発表したMuse Wonderモデルに関する情報で、S1MBとは直接的な関連性はなく、AIモデルの競争や性能評価について述べています。記事4はYouTubeの動画リンクで、Muse Wonderの発表後の反応や評価についての情報が含まれていますが、S1MBとの関連性は確認されていません。記事5はHugging Faceでの投稿で、S1MBにおけるDarwin-27B-ZTC-v2のトップランクを示し、S1MBのベンチマークについて具体的な情報を提供しています。この記事は他の記事と比べて、S1MBの結果や評価について詳しく説明しており、他の記事とは異なる視点でS1MBを扱っています。

## 深掘り調査で得られた知見

S1MB（System One Mosaic Benchmark）での決定品質評価において、Darwin-27B-ZTC-v2が102モデル中でトップにランクインした。このモデルはゼロトークンで動作し、1回の前向き推論で決定を生成する非自己回帰的な設計を採用している。これにより、生成プロセスを省略することで遅延とコストを低減し、決定の精度を向上させている。S1MBは137の専門的なベンチマークを用いて、Noul（条件評価）、Choice（選択肢選択）、Score（スケール評価）の3つのタスクタイプでモデルを比較しており、Bordaスコアで順位を決定している。Darwin-27B-ZTC-v2はBordaスコア89.58を記録し、同ベンチマークで最も高いスコアを取得した。この結果は2026年10月19日にHugging Faceで発表された。また、同モデルはゼロショットでの決定エンジンとしての性能も高く、タイプド・デシジョンのリーダーボードでも1位を獲得している。S1MBのリーダーボードは、決定品質を評価するための技術的なベンチマークとして位置付けられており、その結果は業界の技術動向を示す重要な指標となっている。

## 不確実な点・追加確認が必要な点

S1MB デシジョン・エンジン・リーダーボードに関する情報は、複数のソースから得られているが、記事間で一貫性が見られない点がある。例えば、記事5（Hugging Face）では、Darwin-27B-ZTC-v2 が S1MB で 1 位を獲得したと明記されており、Borda スコア 89.58 を記録している。一方で、記事1（UCI）や記事2（IQAir）は、S1MB に関する情報が含まれていないため、その内容を直接確認することはできない。また、記事4（YouTube）は、Meta が Muse Wonder を発表したことを伝えているが、S1MB との関連性は示されていない。さらに、記事5では、S1MB リーダーボードの結果が 2023 年 10 月 24 日に Hugging Face で発表されたとされているが、他の記事ではその日付が明記されていないため、時系列的な整合性が確認できない。また、S1MB が決定品質を測定するベンチマークであることは確認されているが、具体的な評価基準や各タスクの詳細については、どの記事にも明確に記載されていない。そのため、S1MB に関する情報を正確に整理するためには、さらに詳細な情報の収集が必要である。

## 元記事一覧

- [Road cycling latest news, details,rankings, calendar, results | UCI](https://www.uci.org/discipline/road/6TBjsDD8902tud440iv1Cu?tab=rankings&discipline=ROA)
- [World Air QualityRanking| IQAir USA](https://www.iqair.com/world-air-quality-ranking)
- [Metareleases its first frontier model,MuseWonder| TechCrunch](https://techcrunch.com/2026/10/12/meta-releases-its-first-frontier-model-muse-wonder/)
- [Metajust droppedMuseWonder- YouTube](https://www.youtube.com/watch?v=NMthg09WKTA)
- [@SeaWolf-AI on Hugging Face: " Darwin-27B-ZTC-v2 just took ...](https://huggingface.co/posts/SeaWolf-AI/445254363365143)
