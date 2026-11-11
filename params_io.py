"""Load params.csv into dicts of low / central / high values."""
import pandas as pd

def load_table(path="params.csv"):
    df = pd.read_csv(path, comment=None)
    df = df[~df["name"].astype(str).str.startswith("#")].copy()
    for c in ["low", "central", "high"]:
        df[c] = df[c].astype(float)
    bad = df[(df.low > df.central) | (df.central > df.high)]
    if len(bad):
        raise ValueError(f"low <= central <= high violated:\n{bad[['name','low','central','high']]}")
    return df.set_index("name")

def central(df):
    return df["central"].to_dict()
