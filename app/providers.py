"""Data provider interfaces for Marketplace extraction."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json
from typing import Iterable, Protocol


@dataclass
class Listing:
    title: str
    price: str
    description: str
    location: str
    url: str


class Provider(Protocol):
    """Protocol for data providers that fetch Marketplace listings."""

    def fetch(self, region: str, query: str) -> Iterable[Listing]:
        """Return listings for a region and query."""


class MockProvider:
    """Local data provider using a bundled JSON file for demos/tests."""

    def __init__(self, data_path: Path) -> None:
        self._data_path = data_path

    def fetch(self, region: str, query: str) -> Iterable[Listing]:
        with self._data_path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
        for entry in payload:
            if region.lower() in entry["location"].lower() and query.lower() in entry[
                "title"
            ].lower():
                yield Listing(**entry)


class FacebookMarketplaceProvider:
    """Placeholder for a compliant Marketplace data provider.

    NOTE: Facebook Marketplace does not provide a public API for scraping listings.
    Any implementation must comply with Facebook's Terms of Service and use only
    permitted data access methods.
    """

    def fetch(self, region: str, query: str) -> Iterable[Listing]:
        raise NotImplementedError(
            "Marketplace data access requires an approved data source. "
            "Integrate a compliant provider before running live." 
        )
