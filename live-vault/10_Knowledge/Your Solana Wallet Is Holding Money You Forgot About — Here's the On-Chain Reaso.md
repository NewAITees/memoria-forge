---
title: Solanaウォレットに眠る未利用SOLの原因と対処法
type: knowledge
status: draft
created: 2026-09-20
updated: 2026-09-20
confidence: medium
---

# Solanaウォレットに眠る未利用SOLの原因と対処法

## 結論

Solanaのウォレットは、ユーザーが意識していないトークンアカウントや未claimingの報酬、古いアカウントなどにより、実際には所有しているSOLが無駄に保持されている可能性がある。これは、Solanaのrent-exempt仕組みによりアカウントが空でもSOLがロックされるためであり、特に最近導入されたmulti-phase rent reduction（SIMD-0437）によって古いアカウントが過剰なSOLを保持しているケースが確認されている。ユーザーは、Token Programが提供するWithdrawExcessLamports指令を活用することで、過剰なSOLを回収することができる。

## テーマ概要

Solanaウォレットがユーザーが忘れていたお金を持っているという話題は、Solanaブロックチェーンの仕組みと関連する技術的な背景から注目されている。Solanaでは、アカウントが空でも「rent-exempt」のためのSOLを保持する必要があり、これはアカウントの存在を保証するためのロックされた資金である。ユーザーが過去に触れたトークンアカウントや、未claimingされた報酬、古いアカウントなど、多くの理由でSOLが無駄に保持されている可能性がある。特に、Solanaが最近導入した「multi-phase rent reduction（SIMD-0437）」により、古いアカウントが過剰なSOLを保持していることが判明し、ユーザーがその資金を回収する方法が求められている。また、ポンプ.funなどのプラットフォームでの取引により、報酬が未claiming状態で溜まっているケースも確認されている。この問題は、Solanaの設計上の特徴であり、ユーザーが自覚していない間、資金が無駄に消費されている可能性があるため、技術的な理解と対応策が注目されている。

## 共通して確認できる点

Solanaのウォレットでは、ユーザーが意識していないトークンアカウントや、未 claiming された報酬、過剰なSOLの保持が原因で、実際には所有しているお金が存在していることが確認されている。これは、Solanaの rent-exempt 仕組みにより、アカウントが空でもSOLがロックされ、それが原因で損失につながる可能性があるためである。特に、古いアカウントはセキュリティリスクとして懸念されており、ウォレットが空でも不正なアクセスで資金が抜かれる可能性がある。また、Solanaのトークンプログラムは、過剰なSOLを回収するための指令を提供しており、その中でも「WithdrawExcessLamports」は、過剰なSOLを回収するための機能である。この仕組みにより、ユーザーは無駄にロックされているSOLを回収することが可能となる。

## 記事ごとの差分・視点の違い

記事「Your Solana Wallet Is Holding Money You Forgot About — Here's the On-Chain Reason Why」は、Solanaウォレットがユーザーが意識していない状態でSOLやトークンを保持している理由を、Solanaのrent-exempt仕組みとトークンプログラムの機能をもとに解説している。この記事では、アカウントが空でもSOLがロックされる仕組みや、過剰なSOLを回収するためのWithdrawExcessLamports指令の存在を強調しており、ユーザーがウォレットを整理する必要性を指摘している。一方、記事「r/solana on Reddit: What are these transactions on my wallet if I do nothing?」では、ウォレットに現れる不明なトランザクションの原因として、ボットによる誤送金や特定トークンの報酬が挙げられている。この記事は、ユーザーがセキュリティを意識し、送金先のアドレスを確認する必要性を強調している。また、記事「How to Sync Multiple Xero Organisations into One Database」は、Xeroの複数組織を一つのデータベースに統合する方法とその必要性を説明し、SQLを用いた統合プロセスや、各組織のtenant_idによる識別方法を具体的に述べている。記事「Xero Google Sheets Connector: Sync to Your Own Database」は、XeroデータをSQLデータベースに自動同期し、Google Sheetsでのレポート作成を可能にするツールについて解説しており、手動でのCSVエクスポートを避けるためのソリューションとしての価値を強調している。最後に、「How to Validate FFI Between QM and ASIL-D in Zero-Heap AUTOSAR + HSM」は、AUTOSARシステムにおけるFFI（Freedom from Interference）の検証方法と、ゼロヒープ設計やハードウェアセキュリティモジュール（HSM）の役割を詳細に説明し、安全性を確保するための技術的アプローチを論じている。各記事は、それぞれの分野における技術的課題や解決策に焦点を当て、ユーザーにとって重要な情報を提供している。

## 深掘り調査で得られた知見

Solanaのウォレットでは、ユーザーが意識していないトークンアカウントや、未 claiming された報酬、過剰なSOLの保持が原因で、実際には所有しているお金が存在していることが明らかになった。これは、Solanaの rent-exempt 仕組みにより、アカウントが空でもSOLがロックされ、それが原因で損失につながる可能性があるためである。Solanaのトークンプログラムは、過剰なSOLを回収するための指令を提供しており、その指令は「WithdrawExcessLamports」として実装されている。この指令は、rent-exempt 最低額を超えた分だけSOLを回収し、アカウントを閉じることをせず、トークンの残高に影響を与えない。また、Solanaは最近、multi-phase rent reduction（SIMD-0437）を導入し、オンチェーンストレージのコストを削減したが、これにより古いアカウントが過剰なSOLを保持している可能性が生じた。このような状況に対応するためには、ユーザーが自らアカウントを閉じるか、またはツールを活用して過剰なSOLを回収する必要がある。また、ウォレットUIでは、どのアカウントが安全に閉じられるかを明示する機能が不足しており、ユーザーが手動で確認する必要がある。

## 不確実な点・追加確認が必要な点

Solanaのウォレットがユーザーが意識していない状態で資産を保持している可能性について、複数の記事が触れていますが、それぞれの内容には若干の違いがあります。記事1では、Solanaのrent-exempt仕組みにより、空のアカウントでもSOLがロックされることが原因で、ユーザーが気づかないまま資産が保持されていると説明しています。また、Token Programが提供するWithdrawExcessLamports指令により、過剰なSOLを回収することができるという具体的なメカニズムが述べられています。一方で、記事2では、ウォレットに表示されないトランザクションが原因で、ユーザーが気づかないまま資産が保持されている可能性があると指摘していますが、具体的なメカニズムや解決策については触れていません。このため、記事間では、原因や解決策の詳細について一致していない点があります。また、記事1では、Solanaが最近導入したrent reduction（SIMD-0437）により、古いアカウントが過剰にSOLを保持している可能性があると説明していますが、その影響範囲や具体的な対応策については、他の記事には記載されていません。そのため、これらの情報は独立した背景を持つため、統合的な理解には注意が必要です。

## 元記事一覧

- [Your Solana Wallet Is Holding Money You Forgot About — Here's the On-Chain Reason Why - DEV Community](https://dev.to/blockexperts/your-solana-wallet-is-holding-money-you-forgot-about-heres-the-on-chain-reason-why-1f1f)
- [r/solana on Reddit: What are these transactions on my wallet if I do nothing?](https://www.reddit.com/r/solana/comments/1elm75e/what_are_these_transactions_on_my_wallet_if_i_do/)
- [How toSyncMultipleXeroOrganisationsinto OneDatabase](https://dev.to/ilshadyx/how-to-sync-multiple-xero-organisations-into-one-database-30pc)
- [XeroGoogle Sheets Connector:Syncto Your OwnDatabase](https://synctools.ai/xero-google-sheets-connector)
- [How to Validate FFI Between QM and ASIL-D in Zero-Heap AUTOSAR + HSM - DEV Community](https://dev.to/kadritalal38/how-to-validate-ffi-between-qm-and-asil-d-in-zero-heap-autosar-hsm-26ln)
