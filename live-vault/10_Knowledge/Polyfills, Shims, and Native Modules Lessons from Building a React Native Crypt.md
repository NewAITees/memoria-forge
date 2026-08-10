---
title: ポリフィル、シム、ネイティブモジュールの導入経験から学んだReact Nativeの暗号通貨ウォレット構築
created: 2026-08-11
updated: 2026-08-11
---

## 概要
React Nativeで暗号通貨ウォレットを構築する際、メタマスクコンネクトなどのネイティブモジュールやポリフィルの導入が不可欠である。特に、React NativeのメトロバンドラーがNode.jsのビルトインモジュールを解決できないため、カスタムポリフィルやシムの導入が必要となる。また、セキュリティ機能やマルチチェーンサポートの実装にも多くの課題が伴う。

## 詳細

### ポリフィルとシムの導入
React Nativeはメトロバンドラーを使用し、Node.jsのビルトインモジュールを解決できないため、以下のようなポリフィルやシムが必要となる。
- `react-native-get-random-values`：`crypto.getRandomValues`を提供し、メタマスクコンネクトなどの要件を満たす。
- `buffer`：`Buffer`グローバルを提供。
- `readable-stream`：ストリームシムを提供。
- `@peculiar/webcrypto`：Web Crypto APIの実装。
- `text-encoding`：`TextEncoder`と`TextDecoder`を提供。

### メタマスクコンネクトとの互換性
メタマスクコンネクトは`eventemitter3`を内部で使用し、DOMイベントや`CustomEvent`を必要としないが、Wagmiなどのライブラリを使用する場合、これらのイベントをポリフィルする必要がある。

### メトロバンドラーの設定
メトロバンドラーの設定でNode.jsモジュールをReact Nativeに適したシムや空のモジュールにマッピングする必要がある。具体的には以下のような手順が推奨される。
1. 空のモジュールファイルを作成。
2. メトロの設定ファイルを更新し、Node.jsモジュールをReact Native互換のシムにマッピング。
3. `polyfills.ts`を作成し、`Buffer`、`crypto.getRandomValues`、`window`シムなどをグローバルに定義。
4. `react-native-get-random-values`は最初にインポートする必要がある。

### ポリフィルの導入順序
インポート順序は非常に重要で、`react-native-get-random-values`は他のモジュールよりも最初にインポートする必要がある。また、`polyfills.ts`はその次にインポートし、その後にアプリケーションコードをインポートする。

### マルチチェーンサポート
複数のEVMチェーンをサポートする際には、各チェーンに固有のRPCエンドポイント、チェーンID、ブロックエクスプローラー、ネイティブトークンの設定が必要となる。Alchemy SDKなどのサービスを活用することで、ロードバランシングやフェールオーバー、レート制限などの問題を解決できる。

### セキュリティとプライベートキー管理
セキュリティ機能はウォレットの中心であり、プライベートキーの管理が特に重要である。BIP-39を使用して復元フレーズを生成し、AES-256-GCMで暗号化してExpoのSecureStoreに保存する。`WHEN_UNLOCKED_THIS_DEVICE_ONLY`フラグはデータのバックアップや他のデバイスへの転送を防ぐ。

### ポリフィルとネイティブモジュールの選択
`react-native-quick-crypto`はC/C++で実装され、JavaScriptのポリフィルに依存しない高速な暗号化機能を提供する。これにより、ランタイムのパフォーマンスが向上する。

### ポリフィルの導入時の注意点
ポリフィルは別ファイルで読み込む必要があり、1つのファイルにまとめるとランタイム初期化エラーが発生する可能性がある。また、`global.js`や`rn-cli.config.js`などのファイルにポリフィルのインポートを追加する必要がある。

### デザインシステムとAPIの整合性
設計システムではAPIデータの変動を考慮し、コンポーネントが実際のデータに柔軟に対応できるように設計する必要がある。APIの制約を設計の創造的な制約として捉え、柔軟な設計を実現する。

### 再利用可能なReactコンポーネント
再利用可能なReactコンポーネントは現代のReactアプリの骨格であり、設計の再利用性と保守性を高める。

## 未解決の課題
- ポリフィルの導入時のランタイムエラーの回避。
- ネイティブモジュールとポリフィルの互換性の確保。
- マルチチェーンサポートの拡張性。
- デザインシステムとAPIデータの整合性。

## 参考
- [react-native-quick-crypto](https://www.npmjs.com/package/react-native-quick-crypto)
- [Using crypto NodeJS module polyfill in React-Native](https://gist.github.com/pedrouid/629367f8d1b69bf1f93992b2be87bab1)
- [Reusable React Components: Best Practices Guide](https://nareshit.com/blogs/reusable-react-components-best-practices-guide-nareshit)

---

# Polyfills, Shims, and Native Modules Lessons from Building a React Native Crypt


## 出典

- [React Native Metro Polyfill Issues - MetaMask Connect ...](https://docs.metamask.io/metamask-connect/troubleshooting/metro-polyfill-issues/)
- [Building a Self-Custodial Crypto Wallet with React Native](https://kibria.me/blog/building-crypto-wallet-react-native)
- [React Native Integration | Stacks Documentation](https://docs.stacks.co/stacks.js/react-native-integration)

## 未解決点

- 追加調査が必要です。
