from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import pandas as pd
import math

DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "processed"

@dataclass
class Ticker:
    series_id:  str
    label:      str
    value:      float
    change:     float
    pct_change: float
    unit:       str = ""

    @property
    def is_valid(self) -> bool:
        return not math.isnan(self.value)
    
#####################################################################
#####################################################################

class DataStore: ###uses csv files data/processed/
    _FREQ_FILES = ("daily", "weekly", "monthly", "quarterly", "semiannual")

    def __init__(self, data_dir: Path = DATA_DIR) -> None:
        self._frames: dict[str, pd.DataFrame] = {}
        self._load(data_dir)

    def _load(self, data_dir: Path) -> None:
        for name in self._FREQ_FILES:
            path = data_dir / f"{name}.csv"
            if path.exists():
                try:
                    df = pd.read_csv(path, index_col=0, parse_dates=True)
                    self._frames[name] = df
                except Exception:
                    pass

###----------------------------------------------------------------------###

    def latest(self, series_id: str) -> tuple[float, float, float]:
        for df in self._frames.values():
            if series_id not in df.columns:
                continue
            s = df[series_id].dropna()
            if s.empty:
                break
            val = float(s.iloc[-1])
            if len(s) >= 2:
                prev = float(s.iloc[-2])
                chg  = val - prev
                pct  = (chg / abs(prev) * 100) if prev != 0 else 0.0
            else:
                chg = pct = float("nan")
            return val, chg, pct
        return float("nan"), float("nan"), float("nan")

    def series(self, series_id: str) -> pd.Series:
        for df in self._frames.values():
            if series_id in df.columns:
                return df[series_id].dropna()
        return pd.Series(dtype=float)

    def build_panel(self, entries: list[dict]) -> list[Ticker]:
        tickers = []
        for e in entries:
            val, chg, pct = self.latest(e["id"])
            tickers.append(
                Ticker(
                    series_id=e["id"],
                    label=e["label"],
                    value=val,
                    change=chg,
                    pct_change=pct,
                    unit=e.get("unit", ""),
                )
            )
        return tickers

#####################################################################
#####################################################################

PANELS: dict[str, dict] = {
    "RATES": {
        "title": "INTEREST RATES",
        "entries": [
            {"id": "T10Y2Y",   "label": "10Y–2Y Spread",  "unit": "%"},
            {"id": "T10Y3M",   "label": "10Y–3M Spread",  "unit": "%"},
            {"id": "T10YIE",   "label": "10Y Breakeven",  "unit": "%"},
            {"id": "T5YIE",    "label": "5Y Breakeven",   "unit": "%"},
            {"id": "T10YFF",   "label": "10Y–FF Spread",  "unit": "%"},
            {"id": "T1YFF",    "label": "1Y–FF Spread",   "unit": "%"},
            {"id": "DAAA",     "label": "Moody's Aaa",    "unit": "%"},
            {"id": "DBAA",     "label": "Moody's Baa",    "unit": "%"},
            {"id": "DPRIME",   "label": "Prime Rate",     "unit": "%"},
        ],
    },
    "VOLATILITY": {
        "title": "VOLATILITY",
        "entries": [
            {"id": "VIXCLS",   "label": "VIX",            "unit": ""},
            {"id": "RVXCLS",   "label": "RVX (Russell)",  "unit": ""},
            {"id": "OVXCLS",   "label": "OVX (Crude)",    "unit": ""},
            {"id": "GVZCLS",   "label": "GVZ (Gold)",     "unit": ""},
            {"id": "VXVCLS",   "label": "VXV (S&P 3M)",   "unit": ""},
            {"id": "VXEEMCLS", "label": "VXEEM (EM)",     "unit": ""},
        ],
    },
    "FX": {
        "title": "FX & CREDIT SPREADS",
        "entries": [
            {"id": "DTWEXBGS", "label": "USD Index",      "unit": ""},
            {"id": "DEXUSEU",  "label": "USD/EUR",        "unit": ""},
            {"id": "DEXJPUS",  "label": "JPY/USD",        "unit": ""},
            {"id": "DEXCHUS",  "label": "CNY/USD",        "unit": ""},
            {"id": "DEXUSUK",  "label": "USD/GBP",        "unit": ""},
            {"id": "BAA10Y",   "label": "Baa–10Y Sprd",   "unit": "%"},
            {"id": "AAA10Y",   "label": "Aaa–10Y Sprd",   "unit": "%"},
        ],
    },
    "LABOR": {
        "title": "LABOR MARKET",
        "entries": [
            {"id": "U6RATE",           "label": "U-6 Rate",       "unit": "%"},
            {"id": "LNS14027660",      "label": "Unemp HS+ 25+",  "unit": "%"},
            {"id": "UEMP27OV",         "label": "LT Unemployed",  "unit": "K"},
            {"id": "PAYEMS",           "label": "Nonfarm Pay",    "unit": "K"},
            {"id": "JTSJOL",           "label": "JOLTS Openings", "unit": "K"},
            {"id": "JTSLDL",           "label": "JOLTS Layoffs",  "unit": "K"},
            {"id": "IHLIDXUS",         "label": "Indeed Postings","unit": ""},
        ],
    },
    "ACTIVITY": {
        "title": "PRODUCTION & TRADE",
        "entries": [
            {"id": "RSXFS",            "label": "Retail Sales",   "unit": "M"},
            {"id": "MNFCTRIRSA",       "label": "Mfg Inv/Sales",  "unit": ""},
            {"id": "WHLSLRIRSA",       "label": "Whsl Inv/Sales", "unit": ""},
            {"id": "FRGSHPUSM649NCIS", "label": "Cass Freight",   "unit": ""},
            {"id": "BOPGSTB",          "label": "Trade Balance",  "unit": "M"},
            {"id": "IMPCH",            "label": "China Imports",  "unit": "M"},
            {"id": "FORTREASPOS41408", "label": "China Tsy Hold", "unit": "B"},
        ],
    },
    "MACRO": {
        "title": "SENTIMENT & MACRO",
        "entries": [
            {"id": "UMCSENT",          "label": "UMich Sentiment","unit": ""},
            {"id": "MICH",             "label": "UMich Infl Exp", "unit": "%"},
            {"id": "NFCI",             "label": "Chicago NFCI",   "unit": ""},
            {"id": "STLFSI4",          "label": "St. Louis FSI",  "unit": ""},
            {"id": "SAHMREALTIME",     "label": "Sahm Indicator", "unit": "%"},
            {"id": "PPIACO",           "label": "PPI All Commod", "unit": ""},
            {"id": "ATLSBUSRGEP",      "label": "Biz Sales Exp",  "unit": "%"},
        ],
    },
}

PANEL_ORDER = ["RATES", "VOLATILITY", "FX", "LABOR", "ACTIVITY", "MACRO"]
