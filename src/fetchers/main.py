import argparse
from src.fetchers.fred import FREDClient

###############################################################
##################### CLI INTERFACE 🥵 ########################
###############################################################

def main():
    parser = argparse.ArgumentParser(description="FRED API CLI")
    sub = parser.add_subparsers(dest="command", required=True)

### For a single series and start,end,freq parameters
    p_obs = sub.add_parser("observations", help="Fetch time-series data for a series")
    p_obs.add_argument("series_id", type=str, help="e.g. UNRATE, CPIAUCSL, DGS10")
    p_obs.add_argument("--start", dest="observation_start", default=None, help="YYYY-MM-DD")
    p_obs.add_argument("--end",   dest="observation_end",   default=None, help="YYYY-MM-DD")
    p_obs.add_argument("--freq",  dest="frequency",         default=None, help="d,w,m,q,a")

###metadata method
    p_info = sub.add_parser("info", help="Fetch metadata for a series")
    p_info.add_argument("series_id", type=str)

    p_rel = sub.add_parser("release", help="List all series in a FRED release")
    p_rel.add_argument("release_id", type=int, help="e.g. 51 for H.15 Interest Rates")

### For calling multiple series and same parameters as single methods
    p_multi = sub.add_parser("multi", help="Fetch multiple series into a wide DataFrame")
    p_multi.add_argument("series_ids", nargs="+", help="Space-separated series IDs")
    p_multi.add_argument("--start", dest="observation_start", default=None, help="YYYY-MM-DD")
    p_multi.add_argument("--end",   dest="observation_end",   default=None, help="YYYY-MM-DD")
    p_multi.add_argument("--freq",  dest="frequency",         default=None, help="d,w,m,q,a")


##################################################
##################################################

    args = parser.parse_args() #terminal input --> python object
    client = FREDClient() #calls class

    if args.command == "observations": #router
        df = client.get_series_observations(
            args.series_id,
            observation_start=args.observation_start,
            observation_end=args.observation_end,
            frequency=args.frequency,
        )
        print(df.to_string())

    elif args.command == "info":
        info = client.get_series_info(args.series_id)
        for k, v in info.items():
            print(f"{k:30s} {v}")

    elif args.command == "release":
        df = client.get_release_series(args.release_id)
        print(df[["id", "title", "frequency", "units"]].to_string())

    elif args.command == "multi":
        df = client.get_multiple_series(
            args.series_ids,
            observation_start=args.observation_start,
            observation_end=args.observation_end,
            frequency=args.frequency,
        )
        print(df.to_string())

if __name__ == "__main__":
    main()


