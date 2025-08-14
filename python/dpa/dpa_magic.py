import shlex, subprocess, tempfile, importlib.util
from IPython.core.magic import Magics, magics_class, line_magic, cell_magic
from IPython.display import display

def _have_polars():
    return importlib.util.find_spec("polars") is not None

def _read_df(path):
    if _have_polars():
        import polars as pl
        return pl.read_parquet(path) if path.endswith(".parquet") else pl.read_csv(path)
    else:
        import pandas as pd
        return pd.read_parquet(path) if path.endswith(".parquet") else pd.read_csv(path)

@magics_class
class DPAMagics(Magics):
    @line_magic
    def dpa(self, line):
        args = shlex.split(line)
        into_var = None
        if "--into" in args:
            i = args.index("--into")
            into_var = args[i+1]
            del args[i:i+2]
        tmp = None
        if into_var and ("-o" not in args and "--output" not in args):
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".parquet").name
            args += ["-o", tmp]
        cmd = ["dpa"] + args
        cp = subprocess.run(cmd, capture_output=True, text=True)
        print(cp.stdout, end="")
        if cp.returncode != 0:
            print(cp.stderr)
            raise SystemExit(cp.returncode)
        if into_var:
            out = tmp
            if not out:
                for flag in ("-o","--output"):
                    if flag in args:
                        out = args[args.index(flag)+1]
                        break
            df = _read_df(out)
            self.shell.user_ns[into_var] = df
            try:
                display(df.head(10) if hasattr(df,"head") else df.limit(10))
            except Exception:
                pass

def load_ipython_extension(ip):
    ip.register_magics(DPAMagics)
