# 記憶エンジン Stage 7 受け入れ評価（2026-10-28）

## 評価の目的と範囲

この評価は、新しいローカル記憶エンジンの保存・状態遷移・検索・再実行の決定的な契約を確認する。LLM応答は固定fixtureに差し替えるため、モデル自体の意味品質を測る評価とは分ける。実モデルを用いた品質評価と本番Vaultへの切替判定は未実施。

## 固定シナリオと合格条件

| ID | シナリオ | 合格条件 | pytestケース |
|---|---|---|---|
| E1 | ソース取り込み・改訂・検索 | 同一ソース再投入が冪等で、改訂版が保持され、Dream完了前に原文検索が可能 | `test_source_ingestion_is_idempotent_and_retrievable_before_dreaming`, `test_source_revision_is_stored_as_a_new_immutable_version` |
| E2 | 根拠付きFactとレビュー | 引用が原文内に存在し、Factは独立レビューまでRecallに出ず、日本語表示は承認後のみ使われる | `test_fact_candidate_requires_verbatim_evidence_and_stays_pending`, `test_fact_candidate_rejects_quote_not_in_source`, `test_pipeline_persists_only_reviewed_facts_and_approved_localization`, `test_pipeline_rejects_fact_when_independent_review_rejects_it` |
| E3 | 関係候補 | active Fact間の関係だけを作成し、候補は`proposed`のまま。明示的レビューなしにactive化しない | `test_fact_relations_are_proposed_and_require_review`, `test_relations_cannot_be_proposed_for_unreviewed_facts`, `test_dream_once_reviews_facts_and_only_proposes_clear_relations` |
| E4 | 更新と時点検索 | 更新後の通常Recallは新Factを返し、`as_of`は指定時点に有効な旧Fact/新Factを返す | `test_superseding_fact_preserves_history_and_recalls_by_valid_time` |
| E5 | Forget | Forget済みFactを現在検索・時点検索の両方から返さない | `test_forgotten_fact_is_removed_from_current_and_historical_recall`, `test_recalls_only_current_approved_facts_from_matching_sources` |
| E6 | 完全消去 | 同一URIの版、派生Fact/Relation、Dream job、識別可能なイベントを消し、識別子のないtombstoneだけを残す | `test_source_erase_removes_all_versions_derived_data_and_linked_events` |
| E7 | Dream jobの障害回復 | lease中の二重claimを防ぎ、期限切れleaseを再取得し、指数retry・最大試行数・完了冪等性を守る | `test_dream_job_claim_retry_and_completion_are_leased_and_idempotent`, `test_expired_dream_lease_can_be_reclaimed_by_another_worker`, `test_dream_job_final_failure_stops_after_max_attempts`, `test_dream_once_records_transient_error_for_retry`, `test_dream_once_is_idle_without_pending_job` |

## 実行結果

2026-10-28に次の固定範囲を実行した。

```powershell
uv run --no-sync pytest -q -p no:cacheprovider tests/test_memory_store.py tests/test_memory_pipeline.py tests/test_dream_worker.py
```

**結果: 30 passed, 0 failed。** E1〜E7の決定的な受け入れ条件は通過した。評価はSQLite・パイプライン・workerの契約を検証し、実際のLLMに対する真偽精度を主張しない。

## 未測定と切替判定

- 主張と引用の意味的含意、日本語翻訳の忠実度、relationのprecision/recallは実モデルによる固定gold set評価が必要。
- 複数文書にまたがる更新・矛盾・同一性のモデル判定品質と、誤ったRecall率は未測定。
- 実際のTask Scheduler上の停止・再起動・遅延と、Dream所要時間/ retry率は未測定。タスク登録は行っていない。
- RSS本文全文、Deep Research全文、Markdown/Vault直接取り込みは未接続。
- 旧運用DBの監査、shadow run、切替・復旧手順は未実施。

したがって、この評価だけでは通常運用DBの切替を承認できない。実モデルのgold set評価と残るソースアダプター・運用項目をStage 7の次のゲートとする。
