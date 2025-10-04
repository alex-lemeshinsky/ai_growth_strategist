import argparse
import json
from typing import Tuple

from src.analysis.mvp_pipeline import run_mvp


def parse_window(window: str) -> Tuple[int, int]:
    try:
        a, b = window.split(":")
        return int(a), int(b)
    except Exception:
        return 3, 14


def main():
    parser = argparse.ArgumentParser(description="Analyze creatives from local JSON and rank top ones")
    parser.add_argument("--input", required=True, help="Path to creatives JSON file")
    parser.add_argument("--window", default="3:14", help="Active days window, e.g., 3:14")
    parser.add_argument("--top", type=int, default=3, help="Number of top creatives to return")
    parser.add_argument("--mode", choices=["simple", "gemini"], default="simple", help="Analysis mode")
    parser.add_argument("--schema", action="store_true", help="Enable response schema enforcement (Gemini mode only)")
    args = parser.parse_args()

    window = parse_window(args.window)

    results = run_mvp(args.input, top_k=args.top, window=window, use_schema=args.schema, mode=args.mode)

    print(json.dumps([r.model_dump() for r in results], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
