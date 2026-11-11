"""Fill README_template.md with the parameter table and Monte Carlo results -> README.md.
Run after run.py."""
import pandas as pd
from params_io import load_table

t = load_table()
rows = ["| name | low | central | high | unit | confidence | source |", "|---|---|---|---|---|---|---|"]
for n, r in t.iterrows():
    rows.append(f"| {n} | {r.low:g} | {r.central:g} | {r.high:g} | {r.unit} | {r.confidence} | {str(r.source).replace('|', '/')} |")

s = pd.read_csv("results/montecarlo_summary.csv", index_col=0)
res = ["| metric | 5% | median | 95% |", "|---|---|---|---|"]
for n, r in s.iterrows():
    res.append(f"| {n} | {r.p05:,.2f} | {r['median']:,.2f} | {r.p95:,.2f} |")
pr = pd.read_csv("results/probabilities.csv", index_col=0)
res += ["", "| probability | value |", "|---|---|"] + [f"| {n} | {v:.0%} |" for n, v in pr.probability.items()]
b = pd.read_csv("results/budget_scale.csv")
res += ["", "Actual budget scale (central values):", "", b.to_markdown(index=False, floatfmt=",.1f")]

tmp = open("README_template.md", encoding="utf-8").read()
out = tmp.replace("<!--PARAMS-->", "\n".join(rows)).replace("<!--RESULTS-->", "\n".join(res))
open("README.md", "w", encoding="utf-8").write(out)
print("README.md written")
