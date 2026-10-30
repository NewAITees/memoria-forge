from pathlib import Path
import argparse
import hashlib
import json
import multiprocessing
import os
import tempfile
import time
from dataclasses import asdict

from experiments.visualize_clusters import generate as generate_cluster_visualization
from src.discord_notify import notify_rejection_streak, notify_run, read_webhook_url
from src.moc_builder import build_mocs
from src.wiki_agent import (
    Config,
    StateDB,
    Vault,
    embed_text,
    process_lock,
    push_pending,
    run_once,
)


def scheduled_lock_path(config: Config) -> Path:
    """Return a stable OS-temp lock path so the Vault Git tree stays clean."""
    digest = hashlib.sha256(str(config.vault_path.resolve()).encode("utf-8")).hexdigest()[:16]
    return Path(tempfile.gettempdir()) / f"autonomous-wiki-agent-{digest}.lock"


def _run_once_worker(config: Config, webhook_url: str, result_queue: object) -> None:
    """Execute one agent cycle in a killable child process."""
    try:
        result = run_once(config)
        try:
            result["moc"] = build_mocs(
                config.vault_path,
                config.vault_path / ".agent-state.sqlite3",
                lambda text: embed_text(text, config.embed_url, config.embed_model),
            )
        except Exception as error:  # noqa: BLE001 - MOC refresh must not fail a Wiki run
            result["moc"] = {"status": "failed", "error": repr(error)}
        try:
            report = config.vault_path / "cluster-map.html"
            result["cluster_visualization"] = {
                "status": "updated",
                "path": str(report),
                **generate_cluster_visualization(
                    config.vault_path / ".agent-state.sqlite3", report
                ),
            }
        except Exception as error:  # noqa: BLE001 - report refresh must not fail a Wiki run
            result["cluster_visualization"] = {
                "status": "failed",
                "error": repr(error),
            }
        # Work -> commit -> push must finish before the notice, which links to GitHub.
        try:
            result["git_final"] = push_pending(Vault(config.vault_path), config)
        except Exception as error:  # noqa: BLE001 - a Git failure must not lose the run result
            result["git_final"] = {"status": "failed", "error": repr(error)}
        try:
            result["discord"] = notify_run(result, config.vault_path, webhook_url)
        except Exception as error:  # noqa: BLE001 - notification must not fail a Wiki run
            result["discord"] = {"status": "failed", "error": repr(error)}
        try:
            runs = StateDB(config.vault_path / ".agent-state.sqlite3").recent_runs(100)
            result["discord_streak"] = notify_rejection_streak(runs, webhook_url)
        except Exception as error:  # noqa: BLE001 - notification must not fail a Wiki run
            result["discord_streak"] = {"status": "failed", "error": repr(error)}
        result_queue.put(result)  # type: ignore[attr-defined]
    except BaseException as error:  # noqa: BLE001 - report worker failures as JSON
        result_queue.put({"result": "error", "error_message": repr(error)})  # type: ignore[attr-defined]


def run_once_with_timeout(config: Config, webhook_url: str) -> dict[str, object]:
    """Run one cycle and terminate it when the configured limit is reached."""
    context = multiprocessing.get_context("spawn")
    result_queue = context.Queue()
    worker = context.Process(target=_run_once_worker, args=(config, webhook_url, result_queue))
    worker.start()
    worker.join(config.max_run_minutes * 60)
    if worker.is_alive():
        worker.terminate()
        worker.join(10)
        return {
            "result": "timeout",
            "error_message": f"run exceeded max_run_minutes={config.max_run_minutes}",
        }
    if not result_queue.empty():
        result = result_queue.get()
        if isinstance(result, dict):
            return result
    return {"result": "error", "error_message": "worker exited without a result"}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=Path("config.json"))
    parser.add_argument("--once", action="store_true", help="run one cycle and exit")
    parser.add_argument(
        "--dream-once", action="store_true", help="process one local memory Dreaming job"
    )
    parser.add_argument(
        "--dream-batch", action="store_true", help="process a bounded batch of Dreaming jobs"
    )
    parser.add_argument(
        "--dream-limit",
        type=int,
        default=10,
        help="maximum jobs per --dream-batch run (default: 10)",
    )
    parser.add_argument(
        "--dream-retry-only",
        action="store_true",
        help="claim only ready retry jobs in --dream-batch",
    )
    parser.add_argument("--scheduled", action="store_true", help="use the per-vault process lock")
    parser.add_argument("--interval-hours", type=float, default=24.0)
    parser.add_argument(
        "--status", action="store_true", help="print a health report and exit without running"
    )
    args = parser.parse_args()
    if args.dream_once and args.dream_batch:
        parser.error("--dream-once and --dream-batch are mutually exclusive")
    if args.dream_retry_only and not args.dream_batch:
        parser.error("--dream-retry-only requires --dream-batch")
    if (args.dream_once or args.dream_batch) and (args.once or args.scheduled or args.status):
        parser.error("Dreaming modes cannot be combined with --once, --scheduled, or --status")
    if args.dream_batch and args.dream_limit < 1:
        parser.error("--dream-limit must be positive")
    config = Config.load(args.config)
    if args.dream_once or args.dream_batch:
        from src.dream_worker import run_dream_batch, run_dream_once
        from src.memory_store import MemoryStore
        from src.wiki_agent import create_client, create_reviewer_client

        writer = create_client(config)
        reviewer = create_reviewer_client(config)
        with MemoryStore(config.vault_path / ".memory-engine.sqlite3") as store:
            if args.dream_batch:
                output = asdict(
                    run_dream_batch(
                        store,
                        f"dream-{os.getpid()}",
                        extractor=writer,
                        fact_reviewer=reviewer,
                        translator=writer,
                        localization_reviewer=reviewer,
                        relation_evaluator=reviewer,
                        max_jobs=args.dream_limit,
                        retry_only=args.dream_retry_only,
                    )
                )
            else:
                output = asdict(
                    run_dream_once(
                        store,
                        f"dream-{os.getpid()}",
                        extractor=writer,
                        fact_reviewer=reviewer,
                        translator=writer,
                        localization_reviewer=reviewer,
                        relation_evaluator=reviewer,
                    )
                )
        print(json.dumps(output, ensure_ascii=False, indent=2), flush=True)
        return
    if args.status:
        vault = Vault(config.vault_path)
        db = StateDB(vault.root / ".agent-state.sqlite3")
        print(
            json.dumps(db.status_summary(config.stale_days), ensure_ascii=False, indent=2),
            flush=True,
        )
        return
    webhook_url = read_webhook_url(args.config.parent / "config" / "discord_webhook.txt")
    lock = process_lock(scheduled_lock_path(config)) if args.scheduled else None
    if lock is not None:
        with lock as acquired:
            if not acquired:
                print(json.dumps({"result": "skipped_locked"}), flush=True)
                return
            _run(config, webhook_url, args.once, args.interval_hours)
        return
    _run(config, webhook_url, args.once, args.interval_hours)


def _run(config: Config, webhook_url: str, once: bool, interval_hours: float) -> None:
    while True:
        result = run_once_with_timeout(config, webhook_url)
        print(json.dumps(result, ensure_ascii=False, indent=2), flush=True)
        if once:
            return
        time.sleep(max(interval_hours, 0.01) * 3600)


if __name__ == "__main__":
    main()
