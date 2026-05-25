from .catalog import SERIES, DAILY, WEEKLY, MONTHLY, ID_TO_NAME

QUARTERLY = [s for s in SERIES if s["frequency"] == "q"]

__all__ = ["SERIES", "DAILY", "WEEKLY", "MONTHLY", "QUARTERLY", "ID_TO_NAME"]
