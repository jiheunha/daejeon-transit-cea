"""Fill the results table in README_template.md -> README.md. Run after run.py."""
import pandas as pd

# (metric in results/montecarlo_summary.csv, label, multiplier, decimals)
ROWS = [
    ("A_krw_per_t_all", "A. EV subsidy, M KRW per tCO2 (national and city money)", 1e-6, 2),
    ("B_krw_per_t_all", "B. Fuel-cell car subsidy, M KRW per tCO2", 1e-6, 2),
    ("C_t_per_bn", "C. More buses, tCO2 per bn KRW a year (negative means more CO2)", 1, 0),
    ("E_krw_per_t", "E. Monthly pass, M KRW per tCO2", 1e-6, 2),
    ("R_C_t", "R. Redesign, semi-public, tCO2 avoided a year", 1, 0),
    ("R_C_net_cost_bn", "R. Redesign, semi-public, city money saved, bn KRW a year", -1, 1),
    ("R_D_t", "R. Redesign, public operator, tCO2 avoided a year", 1, 0),
    ("D_system_saving_bn", "D. Public operation alone, saving, bn KRW a year", 1, 1),
    ("D_package_net_bn", "D. Public operation package before the tram, bn KRW a year", 1, 1),
    ("D_package_with_tram_bn", "D. Package with tram-era bus retirement, bn KRW a year", 1, 1),
    ("T1_g_pkm_smr", "T1. Hydrogen tram on grey hydrogen, gCO2e per passenger-km", 1, 0),
    ("T1_g_pkm_mix", "T1. Hydrogen tram on Korea's mix, gCO2e per passenger-km", 1, 0),
    ("T1_g_pkm_battery", "T1. Battery or catenary tram, gCO2e per passenger-km", 1, 0),
    ("T1_h2_extra_cost_bn", "T1. Extra energy cost of hydrogen, bn KRW a year", 1, 1),
    ("W_t_yr", "W. Construction delay, tCO2 a year", 1, 0),
    ("W_time_cost_bn_yr", "W. Construction delay, time cost, bn KRW a year", 1, 1),
]
PROBS = [
    ("P(D cheaper than C per bus-day)", "Public operation alone is cheaper"),
    ("P(restructuring under C cuts CO2)", "Redesign cuts CO2"),
    ("P(restructuring under C pays for itself)", "Redesign pays for itself"),
    ("P(D package + tram restructuring beats C, after 2030)", "Package with tram-era retirement comes out ahead"),
    ("P(E beats A per bn, all public money)", "Monthly pass beats EV subsidy per KRW"),
]

s = pd.read_csv("results/montecarlo_summary.csv", index_col=0)
out = ["| Result | Median | 90% interval |", "|---|---|---|"]
for key, label, k, d in ROWS:
    lo, mid, hi = (s.loc[key, c] * k for c in ("p05", "median", "p95"))
    lo, hi = min(lo, hi), max(lo, hi)
    out.append(f"| {label} | {mid:,.{d}f} | {lo:,.{d}f} to {hi:,.{d}f} |")

pr = pd.read_csv("results/probabilities.csv", index_col=0).probability
out += ["", "| Share of draws in which | Value |", "|---|---|"]
out += [f"| {label} | {pr[key]:.0%} |" for key, label in PROBS]

tmp = open("README_template.md", encoding="utf-8").read()
open("README.md", "w", encoding="utf-8").write(tmp.replace("<!--RESULTS-->", "\n".join(out)))
print("README.md written")
