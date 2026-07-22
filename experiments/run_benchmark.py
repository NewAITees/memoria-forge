from pathlib import Path
import argparse
import json

from experiments.retrieval_experiment import propose_next_action, run_live_benchmark, write_report
from src.wiki_agent import Ollama


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--vault", type=Path, required=True)
    parser.add_argument("--ollama-url", default="http://localhost:11434")
    parser.add_argument("--model", default="qwen3:8b")
    args = parser.parse_args()
    client = Ollama(args.ollama_url, args.model)
    result = run_live_benchmark(args.vault, client)
    proposal = propose_next_action(client, args.vault, result)
    write_report(args.vault, result, proposal)
    result["next_action"] = proposal
    print(json.dumps(result, ensure_ascii=False, indent=2))
