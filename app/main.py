"""CLI entrypoint for Marketplace data extraction."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys
from typing import Sequence

from .exporters import export_csv, export_excel, export_json
from .providers import FacebookMarketplaceProvider, Listing, MockProvider

SUPPORTED_OUTPUTS = {".csv", ".json", ".xlsx"}


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Extract Marketplace listings for a given region and query and export to "
            "CSV/JSON/Excel."
        )
    )
    parser.add_argument("--region", required=True, help="Region or city (e.g., Dallas, TX)")
    parser.add_argument("--query", required=True, help="Search query (e.g., Lexus RX350 2013)")
    parser.add_argument(
        "--output",
        required=True,
        help="Output file path (.csv, .json, or .xlsx)",
    )
    parser.add_argument(
        "--provider",
        choices=["mock", "facebook"],
        default="mock",
        help="Data provider to use. 'facebook' is a placeholder for compliant access.",
    )
    parser.add_argument(
        "--mock-data",
        default=Path(__file__).with_name("sample_data.json"),
        type=Path,
        help="Path to mock data JSON file.",
    )
    return parser.parse_args(argv)


def pick_provider(provider: str, mock_data: Path):
    if provider == "mock":
        return MockProvider(mock_data)
    return FacebookMarketplaceProvider()


def export_listings(listings: Sequence[Listing], output_path: Path) -> None:
    suffix = output_path.suffix.lower()
    if suffix not in SUPPORTED_OUTPUTS:
        raise ValueError(f"Unsupported output format: {suffix}")
    if not listings:
        raise ValueError("No listings found for the specified query/region.")

    if suffix == ".csv":
        export_csv(listings, output_path)
    elif suffix == ".json":
        export_json(listings, output_path)
    else:
        export_excel(listings, output_path)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    provider = pick_provider(args.provider, args.mock_data)
    listings = list(provider.fetch(args.region, args.query))
    export_listings(listings, Path(args.output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
