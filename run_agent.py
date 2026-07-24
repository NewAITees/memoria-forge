from pathlib import Path
import argparse
import hashlib
import json
import multiprocessing
import tempfile
import time
from src.wiki_agent import Config, StateDB, Vault, process_lock, run_once


def scheduled_lock_path(config: Config) -> Path:
    """Return a stable OS-temp lock path so the Vault Git tree stays clean."""
    digest = hashlib.sha256(str(config.vault_path.resolve()).encode("utf-8")).hexdigest()[:16]
    return Path(tempfile.gettempdir()) / f"autonomous-wiki-agent-{digest}.lock"


def _run_once_worker(config: Config, result_queue: object) -> None:
    """Execute one agent cycle in a killable child process."""
    try:
        result = run_once(config)
        result_queue.put(result)  # type: ignore[attr-defined]
    except BaseException as error:  # noqa: BLE001 - report worker failures as JSON
        result_queue.put({"result": "error", "error_message": repr(error)})  # type: ignore[attr-defined]


def run_once_with_timeout(config: Config) -> dict[str, object]:
    """Run one cycle and terminate it when the configured limit is reached."""
    context = multiprocessing.get_context("spawn")
    result_queue = context.Queue()
    worker = context.Process(target=_run_once_worker, args=(config, result_queue))
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
    parser.add_argument("--scheduled", action="store_true", help="use the per-vault process lock")
    parser.add_argument("--interval-hours", type=float, default=24.0)
    parser.add_argument(
        "--status", action="store_true", help="print a health report and exit without running"
    )
    args = parser.parse_args()
    config = Config.load(args.config)
    if args.status:
        vault = Vault(config.vault_path)
        db = StateDB(vault.root / ".agent-state.sqlite3")
        print(json.dumps(db.status_summary(config.stale_days), ensure_ascii=False, indent=2), flush=True)
        return
    lock = process_lock(scheduled_lock_path(config)) if args.scheduled else None
    if lock is not None:
        with lock as acquired:
            if not acquired:
                print(json.dumps({"result": "skipped_locked"}), flush=True)
                return
            _run(config, args.once, args.interval_hours)
        return
    _run(config, args.once, args.interval_hours)


def _run(config: Config, once: bool, interval_hours: float) -> None:
    while True:
        result = run_once_with_timeout(config)
        print(json.dumps(result, ensure_ascii=False, indent=2), flush=True)
        if once:
            return
        time.sleep(max(interval_hours, 0.01) * 3600)


if __name__ == "__main__":
    main()
