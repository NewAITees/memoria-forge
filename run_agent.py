from pathlib import Path
import argparse
import json
import time
from src.wiki_agent import Config, process_lock, run_once


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=Path("config.json"))
    parser.add_argument("--once", action="store_true", help="run one cycle and exit")
    parser.add_argument("--scheduled", action="store_true", help="use the per-vault process lock")
    parser.add_argument("--interval-hours", type=float, default=24.0)
    args = parser.parse_args()
    config = Config.load(args.config)
    lock = process_lock(config.vault_path / ".agent-run.lock") if args.scheduled else None
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
        result = run_once(config)
        print(json.dumps(result, ensure_ascii=False, indent=2), flush=True)
        if once:
            return
        time.sleep(max(interval_hours, 0.01) * 3600)


if __name__ == "__main__":
    main()
