---
title: SQL実行順序の違いがWHEREとORDER BYのalias扱いに影響する理由
type: knowledge
status: draft
created: 2026-10-01
updated: 2026-10-01
confidence: medium
---

# SQL実行順序の違いがWHEREとORDER BYのalias扱いに影響する理由

## 結論

SQLクエリにおいて、WHERE句ではSELECT句で定義されたaliasを参照できないのは、実行順序の仕組みによるものであり、ORDER BY句ではSELECT句の後に実行されるためaliasを参照できる。この違いは、SQLが宣言型の言語であり、ユーザーが書いた順序とは異なる順序でクエリを実行するための仕組みに基づいている。この理解は、クエリのデバッグやパフォーマンスの向上に不可欠である。

## テーマ概要

SQL Execution Order Internals: Why WHERE Fails on Aliases but ORDER BY Succeeds は、SQLクエリにおける実行順序に関する深い理解を求めるテーマです。このテーマでは、WHERE句とORDER BY句がなぜ異なる挙動を示すのかを説明しています。具体的には、WHERE句はFROM/JOIN、GROUP BY、HAVINGの前に実行されるため、SELECT句で生成されたalias（例えばemp_count）は利用できません。一方、ORDER BY句はSELECT句の後に実行されるため、SELECT句で定義されたaliasを参照することが可能です。このような実行順序の違いは、SQLクエリの動作を理解し、デバッグやパフォーマンスの向上に重要です。このテーマは、SQLの動作を正確に把握し、エラーを回避するための知識として注目されています。

## 共通して確認できる点

SQLクエリにおけるWHERE句とORDER BY句の動作の違いは、実行順序に起因している。WHERE句はFROM/JOIN、GROUP BY、HAVINGの前に実行されるため、SELECT句で生成されたalias（例えばemp_count）は利用できない。一方、ORDER BY句はSELECT句の後に実行されるため、SELECT句で定義されたaliasを参照することが可能である。SQLクエリはユーザーが書いた順序とは異なり、FROM/JOIN → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT/OFFSETの順序で実行される。WHERE句ではグループ化や集約処理が行われる前の段階で実行されるため、集計関数（COUNT、SUMなど）の結果は利用できない。HAVING句はGROUP BYの後に実行されるため、集計結果に基づいたフィルタリングが可能である。SELECT句では列の計算やaliasの定義が行われるため、ORDER BY句ではこれらのaliasが利用できる。SQLは宣言型の言語であり、ユーザーが書いた順序とは異なる順序でクエリを実行する。実行順序の理解はクエリのデバッグやパフォーマンスの向上に重要であり、WHERE句でaliasが利用できない理由やORDER BY句でaliasが利用できる理由を理解することで、SQLの動作をより正確に把握できる。

## 記事ごとの差分・視点の違い

記事1では、SQL実行順序の内部仕組みを解説し、WHERE句がSELECT句のaliasを参照できない理由をステージごとの実行順序で説明しています。特に、WHERE句がSELECT句よりも前に実行されるため、aliasが存在しない状態で参照しようとするためエラーになる点を強調しています。一方で、ORDER BY句はSELECT句の後に実行されるため、aliasを参照することが可能であり、これがORDER BYでaliasが使える理由を説明しています。この記事では、SQLクエリの実行順序がユーザーが書いた順序とは異なる点を明確にし、実行順序の理解がクエリのデバッグやパフォーマンス向上に重要であると述べています。

記事2では、SQL実行順序の論理的な処理順序を段階的に説明し、FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT/OFFSETの順序で実行される点を強調しています。この記事では、論理的な順序と物理的な順序の違いを説明し、論理的な順序がクエリの理解やデバッグに重要であると述べています。また、実際のクエリでは、クエリオプティマイザが物理的な実行順序を最適化することがあり、これにより実行効率が向上する可能性があると説明しています。

記事3では、SQLインタビューが「翻訳テスト」であり、ビジネスの質問をSQLクエリに変換する能力が問われる点を強調しています。この記事では、インタビューでは単なる構文の確認ではなく、問題の明確化、エッジケースの考慮、理由の説明が求められることを述べています。また、インタビューでは最初の60秒が非常に重要で、問題を理解する時間を確保することが求められると説明しています。

記事4では、SQLインタビューの実際の構造と対策を解説し、インタビューでは構文だけでなく、論理的思考や問題解決能力が問われることを強調しています。この記事では、インタビューでは最初に問題を理解し、正しいクエリを書くことが重要であり、その過程で説明能力も求められることを述べています。また、インタビューでは、クエリの可読性や保守性にも注目される点を強調しています。

記事5では、テーブルコメントの活用方法とその重要性を説明しています。この記事では、PostgreSQLやOracleでは`COMMENT ON TABLE`文を使用してテーブルに説明を保存でき、MySQLやSQL Serverでは異なる文が必要である点を述べています。また、コメントはバックアップとともに保存され、BIツールやデータカタログで自動的に表示されるため、知識の継続的な保存と共有に役立つと説明しています。この記事では、コメントの追加作業が簡単で、知識の継続的な保存手段として推奨されている点を強調しています。

## 深掘り調査で得られた知見

SQLクエリにおけるWHERE句とORDER BY句の動作の違いは、実行順序に起因している。WHERE句はFROM/JOIN、GROUP BY、HAVINGの前に実行されるため、SELECT句で生成されたalias（例えばemp_count）は利用できない。一方、ORDER BY句はSELECT句の後に実行されるため、SELECT句で定義されたaliasを参照することが可能である。SQLクエリはユーザーが書いた順序とは異なり、FROM/JOIN → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT/OFFSETの順序で実行される。WHERE句ではグループ化や集約処理が行われる前の段階で実行されるため、集計関数（COUNT、SUMなど）の結果は利用できない。HAVING句はGROUP BYの後に実行されるため、集計結果に基づいたフィルタリングが可能である。SELECT句では列の計算やaliasの定義が行われるため、ORDER BY句ではこれらのaliasが利用できる。SQLは宣言型の言語であり、ユーザーが書いた順序とは異なる順序でクエリを実行する。実行順序の理解はクエリのデバッグやパフォーマンスの向上に重要であり、WHERE句でaliasが利用できない理由やORDER BY句でaliasが利用できる理由を理解することで、SQLの動作をより正確に把握できる。また、一部の資料ではSQL実行順序のステップ数が異なり、9段階と6段階の記述が見られる。さらに、論理的な順序と物理的な順序の違いについても強調されている。

## 不確実な点・追加確認が必要な点

SQL Execution Order Internals: Why WHERE Fails on Aliases but ORDER BY Succeeds に関する調査では、WHERE句とORDER BY句の動作の違いがSQLの実行順序に起因していることが確認されました。具体的には、WHERE句はFROM/JOIN、GROUP BY、HAVINGの前に実行されるため、SELECT句で生成されたalias（例えばemp_count）は利用できません。一方、ORDER BY句はSELECT句の後に実行されるため、SELECT句で定義されたaliasを参照することが可能です。この違いは、SQLが宣言型の言語であり、ユーザーが書いた順序とは異なる順序でクエリを実行するためです。

ただし、記事間で実行順序のステップ数が異なり、9段階と6段階の記述が見られるため、一概に断定することはできません。また、論理的な順序と物理的な順序の違いについても強調されており、論理的な順序はSQLクエリのデバッグやパフォーマンスの向上に重要ですが、物理的な順序はクエリオプティマイザが実行時に変更する可能性があります。このため、実行順序に関する情報は、特定のデータベースシステムやクエリオプティマイザの動作に依存する可能性があります。

## 元記事一覧

- [SQLExecutionOrderInternals:WhyWHEREFailsonAliasesbut...](https://dev.to/arpitmbangre/sql-execution-order-internals-why-where-fails-on-aliases-but-order-by-succeeds-1774)
- [SQLExecutionOrderExplained With RealQuery... - StrataScratch](https://www.stratascratch.com/blog/sql-execution-order-explained)
- [ASQLinterviewisatranslationtest,notasyntax... - DEV Community](https://dev.to/fourleaf/a-sql-interview-is-a-translation-test-not-a-syntax-test-4a9p)
- [How to Ace Your Next SQL Interview! - by Sai Kumar Bysani](https://thedatahustle.substack.com/p/how-to-pass-sql-interviews)
- [When to IndexaTable: A Practical Guide for Analysts - DEV Community](https://dev.to/michaelnocito/when-to-index-a-table-a-practical-guide-for-analysts-2dg8)
