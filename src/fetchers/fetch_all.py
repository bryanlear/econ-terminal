import pandas as pd
from pathlib import Path
from src.fetchers.fred import FREDClient
from src.indicators.catalog import DAILY, WEEKLY, MONTHLY, SERIES

### Run from the project root:
###   python -m src.fetchers.fetch_all

OUTPUT_DIR = Path(__file__).resolve().parents[2] / "data" / "processed"
START_DATE = "2000-01-01"  # baseline for all

def fetch_group(client: FREDClient, group: list[dict], label: str):
    print(f"\nFetching {len(group)} {label} series")

    frames = []
    failed = []

    for s in group:
        try:
            df = client.get_series_observations(s["id"], observation_start=START_DATE)
            frames.append(df)
            print(f"  OK  {s['id']:35s} {s['name']}")
        except Exception as e:
            failed.append(s["id"])
            print(f"  FAIL {s['id']:34s} {e}")

    if not frames:
        print(f"  No data fetched for {label}")
        return None

    combined = pd.concat(frames, axis=1, join="outer", sort=False).sort_index()
    combined = combined.dropna(how="all")  #remove NaN rows

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUT_DIR / f"{label}.csv"
    combined.to_csv(out_path)
    print(f"\n  Saved {combined.shape[0]} rows x {combined.shape[1]} cols → {out_path}")

#report
    empty_cols = [col for col in combined.columns if combined[col].isna().all()]
    if empty_cols:
        print(f"  !!!! — all-NaN columns ({len(empty_cols)}): {', '.join(empty_cols)}")
        print(f"  Series returned no numeric data from FRED. Check IDs in catalog.py")

    if failed:
        print(f"  FAILED to fetch ({len(failed)}): {', '.join(failed)}")

    return combined

def main():
    client = FREDClient()
    QUARTERLY   = [s for s in SERIES if s["frequency"] == "q"]
    SEMIANNUAL  = [s for s in SERIES if s["frequency"] == "sa"]
    fetch_group(client, DAILY,      "daily")
    fetch_group(client, WEEKLY,     "weekly")
    fetch_group(client, MONTHLY,    "monthly")
    fetch_group(client, QUARTERLY,  "quarterly")
    fetch_group(client, SEMIANNUAL, "semiannual")
    print("\nAll saved to data/processed/")

if __name__ == "__main__":
    main()
