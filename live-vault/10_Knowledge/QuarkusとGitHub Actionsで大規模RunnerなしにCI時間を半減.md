---
type: knowledge
status: draft
created: 2026-08-09
updated: 2026-08-09
confidence: medium
---

# Quarkus + GitHub Actions Reducing CI Time by Half Without Larger Runners

## 概要
Quarkus と GitHub Actions を組み合わせることで、CI（継続的インテグレーション）の時間を半分に削減する方法が導入されています。このアプローチは、大規模なランナーや複雑な設定を必要とせずに、効率的なCI/CDパイプラインを構築することを可能にします。

## 詳細
Quarkus は Java で GitHub Actions を開発するための拡張機能を提供しており、コードの共有やテストの効率化を促進します。GitHub Actions は、Quarkus の CI/CD パイプラインにおいて、JVM バージョン、OS、テストカテゴリ、コンパイルターゲット（JVM vs. ネイティブ）を複数次元で管理します。

Quarkus は Gitflow Incremental Builder (GIB) を使用して、コード変更に影響を与えるテストをのみ実行することで、CI 時間を大幅に短縮します。これは、特に pull request において、変更がなかったモジュールをスキップすることを可能にします。

また、ネイティブイメージテストはリソースを多く消費するため、Quarkus は `.github/native-tests.json` でテストをカテゴリに分類し、時間とメモリのバランスを取るよう設計されています。テストは、それぞれのカテゴリに特定のタイムアウトとテストモジュールが割り当てられています。

## ソース
- [GitHub - quarkiverse/quarkus-github-action](https://github.com/quarkiverse/quarkus-github-action)
- [GitHub Action | Extensions - Quarkus](https://quarkus.io/extensions/io.quarkiverse.githubaction/quarkus-github-action/)
- [Quarkus GitHub Action :: Quarkiverse Documentation](https://docs.quarkiverse.io/quarkus-github-action/dev/index.html)
- [CI/CD Automation - Quarkus Super Heroes](https://quarkus.io/quarkus-super-heroes/automation/)
- [CI/CD Pipeline and Integration Testing | quarkusio/quarkus](https://deepwiki.com/quarkusio/quarkus/2.3-cicd-pipeline-and-integration-testing)

## 解決されていない点
- Quarkus と GitHub Actions の組み合わせによる CI 時間削減の具体的なメトリクスや、他の CI ツールとの比較情報は未確認です。
- ネイティブイメージテストのカテゴリ分類やタイムアウトの設定についての詳細な情報は、現時点では確認されていません。

## 作成日
2026-08-09

## 更新日
2026-08-09

## 出典


## 未解決点

