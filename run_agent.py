from pathlib import Path
import argparse
import json
import time
from src.wiki_agent import Config, run_once


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=Path("config.json"))
    parser.add_argument("--once", action="store_true", help="run one cycle and exit")
    parser.add_argument("--interval-hours", type=float, default=24.0)
    args = parser.parse_args()
    config = Config.load(args.config)
    while True:
        result = run_once(config)
        print(json.dumps(result, ensure_ascii=False, indent=2), flush=True)
        if args.once:
            return
        time.sleep(max(args.interval_hours, 0.01) * 3600)


if __name__ == "__main__":
    main()
