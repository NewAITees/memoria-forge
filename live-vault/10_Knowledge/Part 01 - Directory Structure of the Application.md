---
title: PHPベースのアプリケーションのディレクトリ構造とFront Controllerの役割
type: knowledge
status: draft
created: 2026-10-21
updated: 2026-10-21
confidence: medium
---

# PHPベースのアプリケーションのディレクトリ構造とFront Controllerの役割

## 結論

PHPベースのアプリケーションにおいて、ディレクトリ構造の設計はコードの整理と保守性向上に直結しており、特に`public`ディレクトリに`index.php`を配置するFront Controllerパターンの導入は、リクエスト処理の集中管理とセキュリティ確保に不可欠です。また、`app`ディレクトリ内での機能別ディレクトリ分割（`Controllers`、`Core`、`Models`など）は、開発効率と拡張性を高めるための標準的な設計思想として根付いています。

## テーマ概要

アプリケーションのディレクトリ構造は、ソフトウェア開発においてコードの整理や保守性を高めるために重要な要素です。特にPHPベースのアプリケーションでは、プロジェクトルートディレクトリにコントローラー、モデル、コアファイル、データベース関連ファイルなどを分離して配置することで、コードの可読性と管理性が向上します。このテーマでは、具体的なディレクトリ構造の例として、`app`ディレクトリ内に`Controllers`、`Core`、`Models`、`Queue`、`Services`などのサブディレクトリが存在し、それぞれが特定の機能を担っています。また、`public`ディレクトリには`index.php`などのエントリポイントファイルが配置され、Front Controllerパターンを実装するための中心的な役割を果たしています。このような構造は、アプリケーション全体のリクエスト処理を一貫して管理し、保守性を高めるための設計思想に基づいています。近年では、フレームワークの導入によりこのようなディレクトリ構造が標準化され、開発効率の向上やコードの再利用性の向上に貢献しています。

## 共通して確認できる点

複数の記事で共通して確認できた事実として、アプリケーションのディレクトリ構造において、`public`ディレクトリに`index.php`ファイルが配置されることが挙げられます。この`index.php`ファイルは、Front Controllerとして機能し、アプリケーションのすべてのリクエストを処理するエントリポイントとして使用されています。また、`index.php`ファイルは`declare(strict_types=1)`を含むことで、関数引数と戻り値の厳格な型チェックを強制しています。この構造は、PHPベースのアプリケーションにおいて機密情報の保護とリクエスト処理の効率化を目的としています。さらに、`public`ディレクトリには、`adminer.php`や`css`、`images`、`scripts`などの公開リソースが配置されており、これらはユーザーがアクセス可能な範囲に含まれます。また、`routes`ディレクトリには`api.php`や`web.php`などのルーティング設定ファイルが配置されており、リクエストの処理を制御するための重要な役割を果たしています。

## 記事ごとの差分・視点の違い

記事「Part 01 - Directory Structure of the Application」は、PHPベースのアプリケーションのディレクトリ構造を詳細に説明しており、コントローラー、コア、モデル、キュー、サービスなどのディレクトリとファイルの配置を具体的に示しています。また、データベースのマイグレーションやシーダーに関するファイルも含まれており、開発の際の構造的な設計を重視しています。一方で、「Android Project folder Structure」は、Androidアプリケーションにおけるフォルダ構造について説明しており、JavaやKotlinのソースコード、リソースファイル、マニフェストファイルなどの配置について述べています。この記事は、Android開発における一般的なフォルダ構造を説明しており、PHPアプリケーションとは異なる技術スタックに焦点を当てています。

「Part 02 - Front Controller (index.php) File」は、Front Controllerデザインパターンの実装について説明しており、index.phpファイルがエントリポイントとして機能することを強調しています。この記事では、セキュリティ上の理由からindex.phpをpublicディレクトリに配置する必要性についても触れています。一方、「Symfony versus FlatPHP (Symfony Docs)」は、Symfonyフレームワークの特徴と、フラットなPHPでの開発との比較を説明しており、Front Controllerの概念をフレームワークの文脈で説明しています。この記事では、Symfonyにおけるコントローラーの役割や、アプリケーションロジックとプレゼンテーションの分離についても述べています。

「Bootstrap for Beginners - Part Three (Bootstrap Grids)」は、Bootstrapフレームワークにおけるグリッドシステムについて説明しており、レスポンシブデザインの実装方法について述べています。この記事は、フロントエンド開発におけるUIレイアウトの設計に焦点を当てており、PHPやAndroid開発とは異なる技術領域に属しています。

## 深掘り調査で得られた知見

PHPベースのアプリケーションにおけるディレクトリ構造は、プロジェクトの規模に応じて複雑さを増す傾向にあり、特に開発の初期段階では明確なルールやガイドラインが求められます。記事1では、プロジェクトルートディレクトリに「app」フォルダが配置され、その下に「Controllers」「Core」「Models」「Queue」「Services」などの主要なディレクトリが存在することが示されています。これにより、各機能やロジックが分離され、保守性が向上しています。例えば、「Controllers」フォルダには「UserController.php」「AuthController.php」などのファイルが配置され、それぞれのコントローラーが特定のリクエストを処理する役割を担っています。また、「Core」フォルダにはアプリケーションの基盤となるファイルが配置されており、「Bootstrap.php」「Config.php」「Database.php」などは、アプリケーションの初期化や設定、データベース接続に必要な処理を担っています。さらに、「database」フォルダには「Migrations」および「Seeders」が配置されており、データベースの構造変更や初期データの挿入に使用されるため、データベース管理の柔軟性が確保されています。このような構造は、開発の効率化と保守性の向上を目的としており、特に大規模なアプリケーションでは必須の設計です。一方で、Androidアプリケーションのディレクトリ構造は、プロジェクトの種類に応じて異なるため、PHPとAndroidの構造は直接的な比較が難しいです。また、Front Controllerパターンの導入により、すべてのリクエストが「public」ディレクトリ内の「index.php」ファイルを通じて処理されるため、セキュリティ面での制御が可能になります。この設計は、アプリケーション全体のリクエスト処理を一貫して管理し、保守性を高めるための重要な要素です。さらに、Symfonyなどのフレームワークでは、Front Controllerパターンを採用しており、すべてのリクエストを「index.php」ファイルで処理するため、フレームワークの汎用性と柔軟性が確保されています。このような設計は、現代のWebアプリケーション開発において広く採用されており、開発者にとって重要な知識となっています。

## 不確実な点・追加確認が必要な点

記事間の食い違いや資料からは断定できない点を以下に示します。  

記事1では、PHPベースのアプリケーションのディレクトリ構造が詳細に記述されており、`app`ディレクトリ下に`Controllers`、`Core`、`Models`、`Queue`、`Services`などのサブディレクトリが存在する様子が確認できます。また、`public`ディレクトリには`index.php`や`adminer.php`などのファイルが配置されており、`public`ディレクトリがエントリポイントとなる設計が述べられています。さらに、`database`ディレクトリには`Migrations`と`Seeders`が含まれており、データベースの初期化やテーブル構造の管理が行われていることが示されています。  

一方で、記事2ではAndroidアプリケーションのディレクトリ構造について説明されており、`src`、`res`、`AndroidManifest.xml`などのフォルダが含まれているとされています。この記事はPHPのディレクトリ構造とは全く異なる分野であり、比較対象として扱うことはできません。  

記事3と記事4は、`index.php`ファイルがFront Controllerとして機能することを説明していますが、記事3では`public`ディレクトリに`index.php`が配置され、機密情報を保護する目的でそのような配置が選ばれた理由が述べられています。一方で、記事4ではSymfonyフレームワークにおいて`index.php`がFront Controllerとして使用され、リクエストを処理する中心的な役割を果たすことが説明されています。ただし、記事4の内容はSymfonyフレームワークに特化しており、記事1のPHPベースのアプリケーションとは直接的な関連性は確認できません。  

また、記事5はBootstrapのグリッドシステムについて説明しており、PHPやAndroidアプリケーションのディレクトリ構造とは関係がありません。  

以上の通り、各記事は異なる技術分野を扱っており、直接的な比較や統合は困難です。特に、記事1のPHPベースのディレクトリ構造は詳細に記述されていますが、他の記事ではその構造に関する情報は提供されていません。したがって、記事1の内容は独自の技術的背景を持つものであり、他の記事との関連性は限定的です。

## 元記事一覧

- [Part 01 - Directory Structure of the Application - DEV Community](https://dev.to/johirpro/part-01-directory-structure-of-the-application-44hb)
- [Android Project folder Structure - GeeksforGeeks](https://www.geeksforgeeks.org/android/android-project-folder-structure/)
- [Part 02 -FrontController(index.php) File - DEV Community](https://dev.to/johirpro/part-02-front-controller-indexphp-file-5cjf)
- [Symfony versus FlatPHP(Symfony Docs)](https://symfony.com/doc/current/introduction/from_flat_php_to_symfony.html)
- [BootstrapFor Beginners -PartThree(BootstrapGrids)](https://www.c-sharpcorner.com/article/bootstrap-for-beginners-part-threebootstrap-grids/)
