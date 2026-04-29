from __future__ import annotations

import argparse
from pathlib import Path

from src.io_loader import load_cp_archive
from src.pipeline import run_pipeline
from src.report import generate_outputs


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Supplier selection AI pipeline")
    parser.add_argument("--input", required=True, help="Path to cp archive csv")
    parser.add_argument("--query", required=True, help="Procurement request text")
    parser.add_argument("--out", required=True, help="Output directory")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    input_path = Path(args.input)
    output_dir = Path(args.out)
    cp_database = load_cp_archive(str(input_path))
    ranked_suppliers, metrics = run_pipeline(request_text=args.query, cp_database=cp_database)
    generate_outputs(ranked_suppliers=ranked_suppliers, metrics=metrics, output_dir=output_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
