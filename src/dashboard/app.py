import argparse
import math
import webbrowser
from threading import Timer
from urllib.parse import quote
from __future__ import annotations
from dash import Dash, Input, Output, State, callback_context, dcc, html
import plotly.graph_objects as go
from src.dashboard.layout import DataStore, PANEL_ORDER, PANELS
from src.plots.style import BG, BORDER, DIM, DOWN, HEADER, HEADER_BG, LABEL, NEUTRAL, UP, VALUE

DEFAULT_PANEL = None
PANEL_BUTTON_IDS = {panel_key: f"panel-{panel_key.lower()}" for panel_key in PANEL_ORDER}
BUTTON_TO_PANEL = {button_id: panel_key for panel_key, button_id in PANEL_BUTTON_IDS.items()}
_STORE = DataStore()
RETRO_DISPLAY_FONT = '"VT323", "Courier New", monospace'
RETRO_BODY_FONT = '"IBM Plex Mono", "Courier New", monospace' 
RETRO_FONT_STYLESHEET = "https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;700&family=VT323&display=swap" # retro font


def _store(refresh: bool = False) -> DataStore:
    global _STORE
    if refresh:
        _STORE = DataStore()
    return _STORE

def _format_value(value: float, unit: str = "") -> str:
    if math.isnan(value):
        return "N/A"

    if unit == "%":
        return f"{value:,.2f}%"

    suffix = f" {unit}" if unit else ""
    if abs(value) >= 1_000:
        return f"{value:,.0f}{suffix}"
    return f"{value:,.2f}{suffix}"

def _format_change(change: float, pct_change: float, unit: str = "") -> tuple[str, str]:
    if math.isnan(change):
        return "No prior point", NEUTRAL
    magnitude = _format_value(abs(change), unit)
    prefix = "+" if change > 0 else "-" if change < 0 else "="
    pct_text = f" ({abs(pct_change):,.2f}%)" if not math.isnan(pct_change) else ""
    color = UP if change > 0 else DOWN if change < 0 else NEUTRAL
    return f"{prefix} {magnitude}{pct_text}", color

def _sparkline_data_uri(series, stroke_color: str) -> str:
    sample = series.dropna().tail(28)
    width = 82
    height = 24

    if sample.empty:
        svg = (
            f"<svg xmlns='http://www.w3.org/2000/svg' width='{width}' height='{height}' viewBox='0 0 {width} {height}'>"
            f"<line x1='2' y1='{height - 4}' x2='{width - 2}' y2='{height - 4}' stroke='{DIM}' stroke-width='1.2' />"
            "</svg>"
        )
        return f"data:image/svg+xml;utf8,{quote(svg)}"

    values = [float(value) for value in sample.tolist()]
    min_value = min(values)
    max_value = max(values)
    span = max_value - min_value or 1.0
    points = []
    for index, value in enumerate(values):
        x = 2 + (index * (width - 4) / max(len(values) - 1, 1))
        y = height - 3 - ((value - min_value) / span) * (height - 8)
        points.append(f"{x:.2f},{y:.2f}")
    svg = (
        f"<svg xmlns='http://www.w3.org/2000/svg' width='{width}' height='{height}' viewBox='0 0 {width} {height}'>"
        f"<rect x='0' y='0' width='{width}' height='{height}' rx='6' fill='rgba(255,102,0,0.04)' />"
        f"<line x1='2' y1='{height - 4}' x2='{width - 2}' y2='{height - 4}' stroke='{DIM}' stroke-width='1.1' />"
        f"<polyline points='{' '.join(points)}' fill='none' stroke='{stroke_color}' stroke-width='2' stroke-linecap='round' stroke-linejoin='round' />"
        "</svg>"
    )
    return f"data:image/svg+xml;utf8,{quote(svg)}"

def _modal_style(is_open: bool) -> dict[str, str]:
    return {
        "display": "flex" if is_open else "none",
        "position": "fixed",
        "inset": "0",
        "zIndex": "1000",
        "padding": "3vh 20px",
        "justifyContent": "center",
        "alignItems": "flex-start",
        "background": "rgba(0, 0, 0, 0.82)",
        "backdropFilter": "blur(4px)",
        "overflowY": "auto",
    }

def _cards_grid_style(modal_open: bool) -> dict[str, str]:
    return {
        "display": "grid",
        "gridTemplateColumns": "repeat(auto-fit, minmax(320px, 1fr))",
        "gap": "18px",
        "marginTop": "26px",
        "pointerEvents": "none" if modal_open else "auto",
        "filter": "blur(3px)" if modal_open else "none",
        "opacity": "0.55" if modal_open else "1",
        "transition": "filter 140ms ease, opacity 140ms ease",
    }

def _build_panel_button(panel_key: str, store: DataStore, active: bool):
    config = PANELS[panel_key]
    tickers = store.build_panel(config["entries"])
    border_color = HEADER if active else BORDER
    shadow = f"0 0 0 1px {HEADER}" if active else "0 18px 38px rgba(0, 0, 0, 0.35)"
    rows = []
    for index, ticker in enumerate(tickers):
        change_text, change_color = _format_change(ticker.change, ticker.pct_change, ticker.unit)
        sparkline = _sparkline_data_uri(store.series(ticker.series_id), change_color)
        rows.append(
            html.Div(
                [
                    html.Div(
                        [
                            html.Span(
                                ticker.label,
                                style={
                                    "color": LABEL,
                                    "fontWeight": "400",
                                    "fontFamily": RETRO_DISPLAY_FONT,
                                    "fontSize": "1.05rem",
                                    "lineHeight": "1",
                                    "flex": "1 1 auto",
                                    "minWidth": "0",
                                },
                            ),
                            html.Img(
                                src=sparkline,
                                alt="",
                                style={"width": "82px", "height": "24px", "display": "block", "opacity": "0.94"},
                            ),
                        ],
                        style={"display": "flex", "alignItems": "center", "gap": "10px", "minWidth": "0"},
                    ),
                    html.Span(
                        _format_value(ticker.value, ticker.unit),
                        style={"color": VALUE, "fontWeight": "700", "textAlign": "right", "fontFamily": RETRO_BODY_FONT},
                    ),
                    html.Span(
                        change_text,
                        style={"color": change_color, "fontWeight": "700", "textAlign": "right", "fontFamily": RETRO_BODY_FONT},
                    ),
                ],
                style={
                    "display": "grid",
                    "gridTemplateColumns": "minmax(0, 1.7fr) 0.9fr 0.95fr",
                    "gap": "12px",
                    "alignItems": "center",
                    "padding": "10px 0",
                    "borderTop": "none" if index == 0 else f"1px solid {DIM}",
                },
            )
        )

    return html.Button(
        [
            html.Div(
                config["title"],
                style={
                    "color": HEADER,
                    "fontSize": "1.42rem",
                    "fontWeight": "400",
                    "letterSpacing": "0.12em",
                    "fontFamily": RETRO_DISPLAY_FONT,
                    "textShadow": "0 0 10px rgba(255, 140, 0, 0.22)",
                },
            ),
            html.Div(
                "Click to open a larger chart",
                style={"color": VALUE, "fontSize": "0.82rem", "opacity": "0.74", "marginTop": "6px", "marginBottom": "12px", "fontFamily": RETRO_BODY_FONT},
            ),
            html.Div(rows, style={"display": "grid"}),
        ],
        id=PANEL_BUTTON_IDS[panel_key],
        n_clicks=0,
        title=f"Open the {config['title']} panel",
        style={
            "background": f"linear-gradient(180deg, {HEADER_BG} 0%, {BG} 100%)",
            "border": f"1px solid {border_color}",
            "borderRadius": "18px",
            "padding": "18px 20px",
            "textAlign": "left",
            "cursor": "pointer",
            "boxShadow": shadow,
            "transition": "transform 160ms ease, box-shadow 160ms ease, border-color 160ms ease",
            "fontFamily": RETRO_BODY_FONT,
        },
    )

def _build_series_figure(series, entry: dict) -> go.Figure:
    figure = go.Figure()
    hover_template = "%{x|%Y-%m-%d}<br>%{y:,.2f}"
    if entry.get("unit"):
        hover_template += f" {entry['unit']}"
    hover_template += "<extra></extra>"

    figure.add_trace(
        go.Scatter(
            x=series.index,
            y=series.values,
            mode="lines",
            line={"color": BORDER, "width": 2.5},
            hovertemplate=hover_template,
        )
    )
    figure.update_layout(
        paper_bgcolor=HEADER_BG,
        plot_bgcolor=BG,
        font={"color": VALUE, "family": RETRO_BODY_FONT},
        margin={"l": 56, "r": 20, "t": 20, "b": 44},
        height=420,
        hovermode="x unified",
    )
    figure.update_xaxes(
        showgrid=True,
        gridcolor="rgba(255, 140, 0, 0.10)",
        linecolor="rgba(255, 140, 0, 0.25)",
        tickfont={"color": VALUE},
        rangeslider_visible=True,
        rangeslider_thickness=0.08,
    )
    figure.update_yaxes(
        showgrid=True,
        gridcolor="rgba(255, 140, 0, 0.10)",
        zerolinecolor="rgba(255, 140, 0, 0.18)",
        tickfont={"color": VALUE},
        title=entry.get("unit", ""),
    )
    return figure

def _build_detail_panel(panel_key: str, store: DataStore):
    config = PANELS[panel_key]
    charts = []

    for entry in config["entries"]:
        series = store.series(entry["id"])
        if series.empty:
            charts.append(
                html.Div(
                    [
                        html.Div(entry["label"], style={"color": HEADER, "fontWeight": "400", "fontSize": "1.2rem", "fontFamily": RETRO_DISPLAY_FONT}),
                        html.Div(entry["id"], style={"color": VALUE, "opacity": "0.72", "marginTop": "6px", "fontFamily": RETRO_BODY_FONT}),
                        html.Div("No data is available for this series.", style={"color": VALUE, "marginTop": "18px", "fontFamily": RETRO_BODY_FONT}),
                    ],
                    style={
                        "background": HEADER_BG,
                        "border": f"1px solid {BORDER}",
                        "borderRadius": "18px",
                        "padding": "18px 20px",
                    },
                )
            )
            continue

        latest_value = float(series.iloc[-1])
        previous_value = float(series.iloc[-2]) if len(series) > 1 else float("nan")
        change = latest_value - previous_value if len(series) > 1 else float("nan")
        pct_change = (change / abs(previous_value) * 100) if len(series) > 1 and previous_value != 0 else float("nan")
        change_text, change_color = _format_change(change, pct_change, entry.get("unit", ""))
        sparkline = _sparkline_data_uri(series, change_color)
        start = series.index[0].strftime("%Y-%m-%d")
        end = series.index[-1].strftime("%Y-%m-%d")

        charts.append(
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Div(
                                        entry["label"],
                                        style={
                                            "color": HEADER,
                                            "fontSize": "1.25rem",
                                            "fontWeight": "400",
                                            "fontFamily": RETRO_DISPLAY_FONT,
                                            "letterSpacing": "0.04em",
                                        },
                                    ),
                                    html.Img(src=sparkline, alt="", style={"width": "104px", "height": "28px", "display": "block"}),
                                ],
                                style={"display": "flex", "alignItems": "center", "gap": "12px", "flexWrap": "wrap"},
                            ),
                            html.Div(entry["id"], style={"color": VALUE, "opacity": "0.72", "fontSize": "0.85rem", "fontFamily": RETRO_BODY_FONT}),
                        ],
                        style={"display": "flex", "justifyContent": "space-between", "gap": "16px", "alignItems": "baseline", "flexWrap": "wrap"},
                    ),
                    html.Div(
                        [
                            html.Div(f"Latest: {_format_value(latest_value, entry.get('unit', ''))}", style={"color": VALUE, "fontWeight": "700", "fontFamily": RETRO_BODY_FONT}),
                            html.Div(change_text, style={"color": change_color, "fontWeight": "700", "fontFamily": RETRO_BODY_FONT}),
                            html.Div(f"Range: {start} to {end}", style={"color": VALUE, "opacity": "0.72", "fontFamily": RETRO_BODY_FONT}),
                        ],
                        style={
                            "display": "flex",
                            "flexWrap": "wrap",
                            "gap": "16px",
                            "marginTop": "12px",
                            "fontSize": "0.86rem",
                        },
                    ),
                    dcc.Graph(
                        figure=_build_series_figure(series, entry),
                        config={"displaylogo": False, "responsive": True},
                        style={"marginTop": "12px", "height": "420px"},
                    ),
                ],
                style={
                    "background": HEADER_BG,
                    "border": f"1px solid {BORDER}",
                    "borderRadius": "18px",
                    "padding": "22px 24px 12px",
                    "boxShadow": "0 18px 38px rgba(0, 0, 0, 0.35)",
                },
            )
        )

    return html.Div(
        [
            html.Div(
                [
                    html.Div(
                        config["title"],
                        style={
                            "color": HEADER,
                            "fontSize": "1.9rem",
                            "fontWeight": "400",
                            "letterSpacing": "0.10em",
                            "fontFamily": RETRO_DISPLAY_FONT,
                            "textShadow": "0 0 10px rgba(255, 140, 0, 0.20)",
                        },
                    ),
                    html.Div(
                        "Large chart view.",
                        style={"color": VALUE, "opacity": "0.76", "marginTop": "6px", "fontFamily": RETRO_BODY_FONT},
                    ),
                ],
                style={"marginBottom": "24px"},
            ),
            html.Div(
                charts,
                style={
                    "display": "flex",
                    "flexDirection": "column",
                    "gap": "20px",
                },
            ),
        ]
    )

def _initial_layout():
    store = _store()
    return html.Div(
        [
            dcc.Store(id="selected-panel", data=DEFAULT_PANEL),
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                "ECON DASHBOARD",
                                style={
                                    "color": HEADER,
                                    "fontSize": "4.1rem",
                                    "fontWeight": "400",
                                    "letterSpacing": "0.12em",
                                    "fontFamily": RETRO_DISPLAY_FONT,
                                    "textShadow": "0 0 18px rgba(255, 140, 0, 0.26)",
                                    "lineHeight": "0.95",
                                },
                            ),
                            html.Div(
                                "Click a card to expand its data over time.",
                                style={"color": VALUE, "opacity": "0.78", "marginTop": "12px", "maxWidth": "860px", "lineHeight": "1.6", "fontFamily": RETRO_BODY_FONT},
                            ),
                        ]
                    ),
                    html.Button(
                        "Refresh data",
                        id="refresh-button",
                        n_clicks=0,
                        style={
                            "border": f"1px solid {BORDER}",
                            "background": HEADER_BG,
                            "color": VALUE,
                            "borderRadius": "999px",
                            "padding": "12px 18px",
                            "fontWeight": "700",
                            "cursor": "pointer",
                            "height": "fit-content",
                            "fontFamily": RETRO_BODY_FONT,
                            "letterSpacing": "0.04em",
                        },
                    ),
                ],
                style={
                    "display": "flex",
                    "justifyContent": "space-between",
                    "alignItems": "flex-start",
                    "gap": "18px",
                    "flexWrap": "wrap",
                },
            ),
            html.Div(
                id="cards-grid",
                children=[_build_panel_button(panel_key, store, False) for panel_key in PANEL_ORDER],
                style=_cards_grid_style(False),
            ),
            html.Div(
                id="panel-modal",
                style=_modal_style(False),
                children=[
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Div(
                                        "Expanded view",
                                        style={"color": VALUE, "opacity": "0.68", "fontSize": "0.9rem", "letterSpacing": "0.05em", "textTransform": "uppercase"},
                                    ),
                                    html.Button(
                                        "Close",
                                        id="close-panel-modal",
                                        n_clicks=0,
                                        style={
                                            "border": f"1px solid {BORDER}",
                                            "background": BG,
                                            "color": VALUE,
                                            "borderRadius": "999px",
                                            "padding": "10px 16px",
                                            "fontWeight": "700",
                                            "cursor": "pointer",
                                            "fontFamily": RETRO_BODY_FONT,
                                        },
                                    ),
                                ],
                                style={
                                    "display": "flex",
                                    "justifyContent": "space-between",
                                    "alignItems": "center",
                                    "gap": "18px",
                                    "marginBottom": "20px",
                                    "position": "sticky",
                                    "top": "0",
                                    "paddingBottom": "12px",
                                    "background": "linear-gradient(180deg, rgba(13, 6, 0, 0.98) 0%, rgba(13, 6, 0, 0.88) 100%)",
                                    "backdropFilter": "blur(4px)",
                                    "zIndex": "2",
                                },
                            ),
                            html.Div(id="panel-modal-body"),
                        ],
                        style={
                            "width": "min(1480px, 100%)",
                            "background": "linear-gradient(180deg, rgba(18, 7, 0, 0.98) 0%, rgba(0, 0, 0, 0.98) 100%)",
                            "border": f"1px solid {BORDER}",
                            "borderRadius": "24px",
                            "padding": "24px",
                            "boxShadow": "0 32px 80px rgba(0, 0, 0, 0.55)",
                        },
                    )
                ],
            ),
        ],
        style={
            "minHeight": "100vh",
            "padding": "28px",
            "background": f"repeating-linear-gradient(180deg, rgba(255, 140, 0, 0.03) 0px, rgba(255, 140, 0, 0.03) 1px, transparent 1px, transparent 4px), radial-gradient(circle at top left, rgba(255, 140, 0, 0.12), transparent 26%), linear-gradient(180deg, #120700 0%, {BG} 42%)",
            "fontFamily": RETRO_BODY_FONT,
        },
    )


app = Dash(
    __name__,
    external_stylesheets=[RETRO_FONT_STYLESHEET],
    title="Econ Dashboard",
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
server = app.server
app.layout = _initial_layout

@app.callback(
    Output("selected-panel", "data"),
    Output("cards-grid", "children"),
    Output("cards-grid", "style"),
    Output("panel-modal", "style"),
    Output("panel-modal-body", "children"),
    [Input(PANEL_BUTTON_IDS[panel_key], "n_clicks") for panel_key in PANEL_ORDER] + [Input("refresh-button", "n_clicks"), Input("close-panel-modal", "n_clicks")],
    State("selected-panel", "data"),
)
def _update_dashboard(*callback_args):
    selected_panel = callback_args[-1] or DEFAULT_PANEL
    triggered_id = getattr(callback_context, "triggered_id", None)
    if triggered_id is None and callback_context.triggered:
        prop_id = callback_context.triggered[0]["prop_id"]
        triggered_id = None if prop_id == "." else prop_id.split(".", 1)[0]
    if triggered_id in BUTTON_TO_PANEL:
        selected_panel = BUTTON_TO_PANEL[triggered_id]
    elif triggered_id == "close-panel-modal":
        selected_panel = None
    store = _store(refresh=triggered_id == "refresh-button")
    cards = [_build_panel_button(panel_key, store, panel_key == selected_panel) for panel_key in PANEL_ORDER]
    modal_body = _build_detail_panel(selected_panel, store) if selected_panel else []
    modal_open = selected_panel is not None
    return selected_panel, cards, _cards_grid_style(modal_open), _modal_style(modal_open), modal_body

def main() -> None:
    parser = argparse.ArgumentParser(description="Run dashboard.")
    parser.add_argument("--host", default="127.0.0.1", help="Host interface for dashboard server.")
    parser.add_argument("--port", type=int, default=8050, help="Port for dashboard server.")
    parser.add_argument("--no-browser", action="store_true", help="Start dashboard with no browser tab.")
    args = parser.parse_args()

    browser_host = "127.0.0.1" if args.host in {"0.0.0.0", "::"} else args.host
    url = f"http://{browser_host}:{args.port}"
    if not args.no_browser:
        Timer(1.0, lambda: webbrowser.open_new(url)).start()
    app.run(host=args.host, port=args.port, debug=False)

if __name__ == "__main__":
    main()
