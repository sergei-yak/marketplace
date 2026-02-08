"""Export listings to supported formats."""

from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
import csv
from typing import Iterable, Sequence

from .providers import Listing


def export_csv(listings: Sequence[Listing], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=asdict(listings[0]).keys())
        writer.writeheader()
        writer.writerows(asdict(listing) for listing in listings)


def export_json(listings: Iterable[Listing], output_path: Path) -> None:
    import json

    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = [asdict(listing) for listing in listings]
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def export_excel(listings: Sequence[Listing], output_path: Path) -> None:
    try:
        import pandas as pd
    except ImportError as exc:  # pragma: no cover - optional dependency
        raise RuntimeError(
            "Excel export requires pandas and openpyxl. "
            "Install with `pip install pandas openpyxl`."
        ) from exc

    output_path.parent.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame([asdict(listing) for listing in listings])
    df.to_excel(output_path, index=False)
