# Marketplace Data Exporter (Scaffold)

This repository provides a **safe, compliant scaffold** for exporting Marketplace-style listings
based on a region + search query and saving results to CSV, JSON, or Excel. It intentionally ships
with a **mock provider** to avoid unauthorized scraping; you can swap in a compliant data provider
when you have approved access to Marketplace data.

## Why a mock provider?
Facebook Marketplace does not provide a public scraping API. Any production integration must comply
with Facebook's Terms of Service and use approved access (e.g., a partner data feed, licensed data
provider, or user-authorized export).

## Quick start

```bash
python -m app.main \
  --region "Dallas, TX" \
  --query "Lexus RX350 2013" \
  --output out/listings.csv
```

To export to Excel:

```bash
pip install pandas openpyxl
python -m app.main --region "Dallas, TX" --query "Lexus RX350 2013" --output out/listings.xlsx
```

## Providers

- `mock` (default): Loads `app/sample_data.json` and filters by region + query.
- `facebook`: Placeholder for **compliant** Marketplace data access. You must implement this with
  an approved data source.

## Output formats

- `.csv`
- `.json`
- `.xlsx` (requires `pandas` + `openpyxl`)

## Next steps (suggested)

- Replace `FacebookMarketplaceProvider` with a compliant data source.
- Add deduplication, pagination, and error handling.
- Store results in a database (Postgres, SQLite, etc.).

## Disclaimer
This scaffold does **not** scrape Marketplace. It is meant to help you structure the app and exports
so you can plug in a compliant data source later.
