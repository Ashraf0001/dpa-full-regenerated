
from __future__ import annotations
import pandas as pd
import dpa as _dpa

_ORIG_READ_PARQUET = pd.read_parquet

def _read_parquet_dpa(path, *, engine=None, columns=None, filters=None, **kwargs):
    # Only intercept when engine == "dpa"
    if engine != "dpa":
        return _ORIG_READ_PARQUET(path, engine=engine, columns=columns, **kwargs)
    # Build a where expression from simple filters [(col, op, value), ...]
    where = None
    if filters:
        parts = []
        for (col, op, val) in filters:
            if isinstance(val, str):
                parts.append(f"{col} {op} '{val}'")
            else:
                parts.append(f"{col} {op} {val}")
        where = " and ".join(parts)
    out = _dpa.filter(str(path), where=where or "True",
                      select=columns, output=None, as_pandas=False)
    return pd.read_parquet(out, columns=columns, **kwargs)

def enable() -> None:
    """Enable pandas engine='dpa' monkeypatch."""
    pd.read_parquet = _read_parquet_dpa  # type: ignore[assignment]
