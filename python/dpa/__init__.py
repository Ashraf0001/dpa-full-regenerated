from __future__ import annotations
from typing import Iterable, Optional

from dpa_core import filter_py, select_py, convert_py, profile_py

def _maybe_load(path: str, as_pandas: bool = False, as_polars: bool = False):
    if as_pandas:
        import pandas as pd
        return pd.read_parquet(path) if path.endswith(".parquet") else pd.read_csv(path)
    if as_polars:
        import polars as pl
        return pl.read_parquet(path) if path.endswith(".parquet") else pl.read_csv(path)
    return path

def filter(input: str, where: str, select: Optional[Iterable[str]] = None,
           output: Optional[str] = None, *, as_pandas=False, as_polars=False):
    out = filter_py(str(input), str(where), list(select) if select else None, output)
    return _maybe_load(out, as_pandas=as_pandas, as_polars=as_polars)

def select(input: str, columns: Iterable[str], output: Optional[str] = None, *,
           as_pandas=False, as_polars=False):
    out = select_py(str(input), list(columns), output)
    return _maybe_load(out, as_pandas=as_pandas, as_polars=as_polars)

def convert(input: str, output: str):
    return convert_py(str(input), str(output))

def profile(input: str) -> dict:
    return dict(profile_py(str(input)))
