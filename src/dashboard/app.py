from __future__ import annotations
import math
from datetime import datetime
import plotext as plt
from rich.text import Text
from textual.app import App, ComposeResult, RenderResult
from textual.binding import Binding
from textual.containers import Container, Horizontal
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Static
from src.plots.style import (
    ACCENT, ARROW_DOWN, ARROW_FLAT, ARROW_UP,
    BORDER, DIM, DOWN, HEADER, LABEL, NEUTRAL, UP, VALUE,
)
from src.dashboard.layout import (
    DataStore, PANEL_ORDER, PANELS, Ticker,
)

################################################
######### python -m src.dashboard.app ##########
################################################

### allows large number to fit with M and K
def _fmt_val(val: float, unit: str = "") -> str:
    if math.isnan(val):
        return "  N/A"
    if abs(val) >= 1_000_000: #divide by 1M and add M
        return f"{val / 1_000_000:.2f}M{unit}"
    if abs(val) >= 1_000: #divide by 1K and add K
        return f"{val / 1_000:.1f}K{unit}"
    return f"{val:.2f}{unit}"

### assign color based on direction of change`` 
def _fmt_chg(chg: float, pct: float) -> tuple[str, str]:
    if math.isnan(chg):
        return "  ---     ", "dim"
    sym   = ARROW_UP if chg > 0 else (ARROW_DOWN if chg < 0 else ARROW_FLAT)
    color = "green"   if chg > 0 else ("red"       if chg < 0 else "dim")
    pct_s = f"({abs(pct):.2f}%)" if not math.isnan(pct) else ""
    return f"{sym}{_fmt_val(abs(chg))} {pct_s}", color

###official label/description using FRED ID
def _series_label(series_id: str) -> str:
    for panel in PANELS.values():
        for e in panel["entries"]:
            if e["id"] == series_id:
                return e["label"]
    return series_id

###############################################
###############################################

class TickerPanel(Widget):

    DEFAULT_CSS = """
    TickerPanel {
        border: solid #FF6600;
        background: #000000;
        padding: 0 1;
        height: 100%;
    }
    """

    def __init__(self, panel_key: str, store: DataStore, **kw) -> None:
        super().__init__(**kw)
        self._key   = panel_key
        self._store = store

    def render(self) -> RenderResult:
        cfg     = PANELS[self._key]
        tickers = self._store.build_panel(cfg["entries"])
        t       = Text()
        t.append(f" {cfg['title']}\n", style=f"bold {HEADER}")
        t.append("─" * 30 + "\n",      style=HEADER)

        for tk in tickers:
            lbl = tk.label[:15].ljust(15)
            val = _fmt_val(tk.value, tk.unit).rjust(9)
            chg_str, color = _fmt_chg(tk.change, tk.pct_change)
            t.append(f" {lbl}", style=LABEL)
            t.append(f"{val}  ", style=f"bold {VALUE}")
            t.append(f"{chg_str}\n", style=color)
        return t

class SparkWidget(Widget):

    DEFAULT_CSS = """
    SparkWidget {
        border: solid #FF6600;
        background: #000000;
        padding: 0 1;
        height: 100%;
    }
    """

    series_id: reactive[str] = reactive("VIXCLS")

    def watch_series_id(self, _: str) -> None:
        self.refresh()

    def __init__(self, store: DataStore, **kw) -> None:
        super().__init__(**kw)
        self._store = store

    def render(self) -> RenderResult:
        sid    = self.series_id
        series = self._store.series(sid)

        if series.empty:
            return Text(f"  No data available for {sid}", style="dim")

        w = max(self.size.width  - 4, 40) if self.size.width  > 4 else 80
        h = max(self.size.height - 2, 5)  if self.size.height > 2 else 8
        step    = max(1, len(series) // w)
        sampled = series.iloc[::step]
        label = _series_label(sid)
        start = series.index[0].strftime("%Y-%m-%d")
        end   = series.index[-1].strftime("%Y-%m-%d")
        dates = [d.strftime("%Y-%m-%d") for d in sampled.index]

        plt.clf()
        plt.plotsize(w, h)
        plt.theme("dark")
        plt.date_form("Y-m-d")
        plt.plot(dates, sampled.values.tolist(), color="orange")
        plt.title(f" {label}  ({sid})   {start} → {end} ")
        plt.ticks_color("orange")
        plt.axes_color("black")
        plt.frame(False)
        return Text.from_ansi(plt.build())

class HeaderBar(Widget):
    def compose(self) -> ComposeResult:
        yield Static("◆ ECON TERMINAL ◆   FRED MACRO DATA", id="title")
        yield Static("", id="clock")

    def on_mount(self) -> None:
        self.set_interval(1, self._tick)

    def _tick(self) -> None:
        self.query_one("#clock", Static).update(
            datetime.now().strftime("  %Y-%m-%d  %H:%M:%S  ")
        )

########### APP CLASS ###########
class EconTerminal(App):

    CSS = """
    Screen {
        background: #000000;
        layout: vertical;
    }
    HeaderBar {
        height: 3;
        background: #0D0600;
        border: solid #FF6600;
        layout: horizontal;
        padding: 0 2;
    }
    HeaderBar #title {
        content-align: left middle;
        color: #FF8C00;
        text-style: bold;
        width: 1fr;
    }
    HeaderBar #clock {
        content-align: right middle;
        color: #FF6600;
        width: 28;
    }
    #main-grid {
        layout: grid;
        grid-size: 3 2;
        grid-gutter: 1 1;
        height: 1fr;
        padding: 0 1;
    }
    #spark {
        height: 16;
        border: solid #FF6600;
        background: #000000;
        padding: 0 1;
        margin: 0 1;
    }
    #footer-bar {
        height: 1;
        background: #0D0600;
        color: #FF6600;
        content-align: left middle;
        padding: 0 2;
    }
    """

    BINDINGS = [
        Binding("1", "spark('RATES')",      "Rates",    show=True),
        Binding("2", "spark('VOLATILITY')", "Vol",      show=True),
        Binding("3", "spark('FX')",         "FX",       show=True),
        Binding("4", "spark('LABOR')",      "Labor",    show=True),
        Binding("5", "spark('ACTIVITY')",   "Activity", show=True),
        Binding("6", "spark('MACRO')",      "Macro",    show=True),
        Binding("r", "reload",              "Refresh",  show=True),
        Binding("q", "quit",                "Quit",     show=True),
    ]

    def __init__(self, **kw) -> None:
        super().__init__(**kw)
        self._store = DataStore()

    def compose(self) -> ComposeResult:
        yield HeaderBar()

        with Container(id="main-grid"):
            for key in PANEL_ORDER:
                yield TickerPanel(key, self._store, id=f"p-{key.lower()}")

        yield SparkWidget(self._store, id="spark")

        yield Static(
            "[1] RATES  [2] VOL  [3] FX  [4] LABOR  [5] ACTIVITY  [6] MACRO"
            "   [R] REFRESH   [Q] QUIT",
            id="footer-bar",
        )

########## ACTIONS ##########

    def action_spark(self, panel_key: str) -> None:
        first_id = PANELS[panel_key]["entries"][0]["id"]
        self.query_one("#spark", SparkWidget).series_id = first_id

    def action_reload(self) -> None:
        self._store = DataStore()
        for key in PANEL_ORDER:
            panel = self.query_one(f"#p-{key.lower()}", TickerPanel)
            panel._store = self._store
            panel.refresh()
        spark = self.query_one("#spark", SparkWidget)
        spark._store = self._store
        spark.refresh()
        self.notify("Data refreshed from disk.", severity="information")

if __name__ == "__main__":
    EconTerminal().run()
