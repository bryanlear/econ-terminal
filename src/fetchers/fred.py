import pandas as pd
import requests
import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass 

FRED_BASE_URL = "https://api.stlouisfed.org/fred"

#Get API key from .env, initiate session and keep reusing it for all requests 🥹
class FREDClient:
    def __init__(self) -> None:
        self.api_key = os.getenv("FRED_API")
        if not self.api_key:
            raise ValueError(
                "FRED_API NOT FOUND, HOMIE. GET AN API KEY FROM https://fred.stlouisfed.org and add it to .env file:\n"
                "  FRED_API=your_key_here"
            )
        self._session = requests.Session() # keep reusing initial TCP and TLS handshake

# send GET request to API --> return JSON
    def _get(self, endpoint: str, params: dict) -> dict:        
        full_params = {"api_key": self.api_key, "file_type": "json", **params} # this is from FRED API docs
        # e.g., https://api.stlouisfed.org/fred/release/series?release_id=51&api_key=[your_key_here_homeboy]&file_type=json
        url = f"{FRED_BASE_URL}/{endpoint}" ##..fred/release/series
        response = self._session.get(url, params=full_params, timeout=10)
        response.raise_for_status()
        return response.json() #json --> DataFrame 
    
###############################################################
###############GET and PROCESS DATA############################
###############################################################

# Fetches actual data points for series --> return pandas DataFrame
    def get_series_observations(
        self,
        series_id: str,
        observation_start: str | None = None,
        observation_end: str | None = None,
        frequency: str | None = None, #m, q, a, ... dont know what other options are tbh
        aggregation_method: str | None = None, #avg,sum, eop,...
    ) -> pd.DataFrame: # all nones are optional. if not provided, FRED uses defaults (I don't really know what the defaults are)
        
        params: dict = {"series_id": series_id} #builds dict
        if observation_start:
            params["observation_start"] = observation_start
        if observation_end:
            params["observation_end"] = observation_end
        if frequency:
            params["frequency"] = frequency
        if aggregation_method:
            params["aggregation_method"] = aggregation_method
 
        data = self._get("series/observations", params) #calls _get funtion to fetch data using params dict
        df = pd.DataFrame(data["observations"])[["date", "value"]] #converts JSON to DataFrame 🤫
        df["date"] = pd.to_datetime(df["date"])
        df["value"] = pd.to_numeric(df["value"], errors="coerce")  # '.' → NaN
        df = df.set_index("date").rename(columns={"value": series_id})
        return df #Final product🤭

    #############################################################
    #################### DataFrame ##############################
    #############################################################

    def get_series_info(self, series_id: str) -> dict: #metadata for series. Hits https://api.stlouisfed.org/fred/series?series_id=UNRATE 
        data = self._get("series", {"series_id": series_id})
        return data["seriess"][0]

    def get_release_series(self, release_id: int) -> pd.DataFrame: # series for each release. Hits https://api.stlouisfed.org/fred/release/series?release_id=51
        data = self._get("release/series", {"release_id": release_id}) #as long as release ID is provided
        return pd.DataFrame(data["seriess"])

#same but for multiple series IDs. returned in wide format.
    def get_multiple_series(
        self,
        series_ids: list[str],
        observation_start: str | None = None,
        observation_end: str | None = None,
        frequency: str | None = None,
    ) -> pd.DataFrame: 
        frames = [
            self.get_series_observations(
                sid,
                observation_start=observation_start,
                observation_end=observation_end,
                frequency=frequency,
            )
            for sid in series_ids
        ]
        return pd.concat(frames, axis=1, join="outer").sort_index()
