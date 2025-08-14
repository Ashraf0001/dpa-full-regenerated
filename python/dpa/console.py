import argparse
from . import filter as dpa_filter, select as dpa_select, convert as dpa_convert, profile as dpa_profile

def main(argv=None):
    ap = argparse.ArgumentParser(prog="dpa", description="Data Processing Accelerator (Rust + Polars)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("filter", aliases=["f"], help="Filter rows and optionally select columns")
    p.add_argument("input")
    p.add_argument("-w","--where", required=True)
    p.add_argument("-s","--select")
    p.add_argument("-o","--output", required=True)

    s = sub.add_parser("select", aliases=["s"], help="Select columns")
    s.add_argument("input")
    s.add_argument("-c","--columns", required=True)
    s.add_argument("-o","--output", required=True)

    c = sub.add_parser("convert", aliases=["c"], help="Convert between CSV/Parquet")
    c.add_argument("input")
    c.add_argument("output")

    pr = sub.add_parser("profile", aliases=["p"], help="Simple profile")
    pr.add_argument("input")

    args = ap.parse_args(argv)

    if args.cmd in ("filter","f"):
        cols = args.select.split(",") if args.select else None
        dpa_filter(args.input, args.where, cols, args.output)
    elif args.cmd in ("select","s"):
        cols = args.columns.split(",")
        dpa_select(args.input, cols, args.output)
    elif args.cmd in ("convert","c"):
        dpa_convert(args.input, args.output)
    elif args.cmd in ("profile","p"):
        out = dpa_profile(args.input)
        for k, v in out.items():
            print(f"{k}: {v}")
    return 0
