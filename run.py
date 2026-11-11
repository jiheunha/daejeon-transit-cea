"""
Run everything: central case, budget-scale case, Monte Carlo, tornado,
figures. Usage:  python run.py
Outputs go to results/ (CSV, markdown) and figures/ (PNG).
"""
import os
import numpy as np
import pandas as pd

import model as m
from params_io import load_table, central
import figures

N_DRAWS = 10_000
SEED = 2026
os.makedirs("results", exist_ok=True)
os.makedirs("figures", exist_ok=True)

TABLE = load_table()
P0 = central(TABLE)


# ---------------------------------------------------------------------------
# 1. Scalar metrics computed for one parameter set
# ---------------------------------------------------------------------------
def metrics(p):
    A, B = m.scenario_A(p), m.scenario_B(p)
    C, D, E = m.scenario_C(p), m.scenario_D(p), m.scenario_E(p)
    T1, T2 = m.scenario_T1(p), m.scenario_T2(p)
    return {
        "A_t_per_bn_all": A["t_per_bn_all"], "A_t_per_bn_city": A["t_per_bn_city"],
        "A_krw_per_t_all": A["krw_per_t_all"], "A_krw_per_t_city": A["krw_per_t_city"],
        "B_t_per_bn_all": B["t_per_bn_all"], "B_t_per_bn_city": B["t_per_bn_city"],
        "B_krw_per_t_all": B["krw_per_t_all"], "B_krw_per_t_city": B["krw_per_t_city"],
        "C_t_per_bn": C["t_per_bn"], "C_krw_per_t": C["krw_per_t"],
        "D_t_per_bn": D["t_per_bn"], "D_krw_per_t": D["krw_per_t"],
        "E_t_per_bn": E["t_per_bn"], "E_krw_per_t": E["krw_per_t"],
        "D_unit_cost_change_pct": D["unit_cost_change_pct"],
        "D_system_saving_bn": D["system_saving_bn"],
        "C_minus_A_t_per_bn": C["t_per_bn"] - A["t_per_bn_all"],
        "A_jobs_local": A["jobs_per_bn_local"], "A_jobs_national": A["jobs_per_bn_national"],
        "C_jobs": C["jobs_per_bn"], "D_jobs": D["jobs_per_bn"],
        "T1_g_pkm_smr": T1["g_pkm_smr"], "T1_g_pkm_mix": T1["g_pkm_mix"],
        "T1_g_pkm_biogas": T1["g_pkm_biogas"], "T1_g_pkm_green": T1["g_pkm_green"],
        "T1_g_pkm_battery": T1["g_pkm_battery"], "T1_g_pkm_e_bus": T1["g_pkm_e_bus"],
        "T1_g_pkm_cng_bus": T1["g_pkm_cng_bus"], "T1_g_pkm_car": T1["g_pkm_car"],
        "T1_t_smr": T1["t_smr"], "T1_t_mix": T1["t_mix"], "T1_t_battery": T1["t_battery"], "T1_t_biogas": T1["t_biogas"],
        "T1_t_green": T1["t_green"], "T1_t_replaced_buses": T1["t_replaced_buses"],
        "T1_h2_extra_cost_bn": T1["h2_extra_cost_bn"], "T1_h2_extra_t_mix": T1["h2_extra_t_mix"],
        "R_C_t": m.scenario_R(p, "C")["t_net"], "R_D_t": m.scenario_R(p, "D")["t_net"],
        "R_C_net_cost_bn": m.scenario_R(p, "C")["net_cost_bn"],
        "R_D_net_cost_bn": m.scenario_R(p, "D")["net_cost_bn"],
        "R_D_minus_C_t": m.scenario_R(p, "D")["t_net"] - m.scenario_R(p, "C")["t_net"],
        "C_after_redesign_t_per_bn": m.scenario_C_after_redesign(p, "D")["t_per_bn"],
        "D_package_net_bn": m.scenario_D(p)["system_saving_bn"]
            - (m.scenario_R(p, "D")["net_cost_bn"] - m.scenario_R(p, "C")["net_cost_bn"]),
        "D_package_with_tram_bn": m.scenario_D(p)["system_saving_bn"]
            - (m.scenario_R(p, "D")["net_cost_bn"] - m.scenario_R(p, "C")["net_cost_bn"])
            + T2["cost_saving_retire_bn"],
        "W_t_yr": m.scenario_W(p)["t_yr"], "W_time_cost_bn_yr": m.scenario_W(p)["time_cost_bn_yr"],
        "W_t_total": m.scenario_W(p)["t_total"], "W_time_cost_total_bn": m.scenario_W(p)["time_cost_total_bn"],
        "W_t_h2_delay": m.scenario_W(p)["t_h2_delay"], "W_cost_h2_delay_bn": m.scenario_W(p)["time_cost_h2_delay_bn"],
        "W_extra_min": m.scenario_W(p)["extra_min_per_vehicle"],
        "W_bus_share_cost": m.scenario_W(p)["bus_share_of_time_cost"],
        "W_offpeak_share": m.scenario_W(p)["offpeak_share_of_car_hours"],
        "tram_extra_cost_bn_yr_ops": T1["h2_extra_cost_bn"],
        "pkg_covers_pass_share": (m.scenario_D(p)["system_saving_bn"]
            - (m.scenario_R(p, "D")["net_cost_bn"] - m.scenario_R(p, "C")["net_cost_bn"])
            + T2["cost_saving_retire_bn"]) / (p["fare_pass_cost"] / 1e9),
        "gap_pct_W": -m.pct_of_transport_gap(p, m.scenario_W(p)["t_yr"]),
        "M_cut_kt": m.scenario_M(p)["cut_kt"], "M_cut_pct_city": m.scenario_M(p)["cut_pct_of_city"],
        "E_t_per_year": E["t_net"],
        "gap_pct_R_C": m.pct_of_transport_gap(p, m.scenario_R(p, "C")["t_net"]),
        "gap_pct_R_D": m.pct_of_transport_gap(p, m.scenario_R(p, "D")["t_net"]),
        "gap_pct_T2_retire": m.pct_of_transport_gap(p, T2["t_diff_retire"]),
        "gap_pct_E": m.pct_of_transport_gap(p, E["t_net"]),
        "gap_pct_C_10bn": m.pct_of_transport_gap(p, m.scenario_C(p, 10e9)["t_net"]),
        "gap_pct_H2_vs_electric_tram": -m.pct_of_transport_gap(p, T1["h2_extra_t_mix"]),
        "gap_pct_EV_2026_cohort": m.pct_of_transport_gap(
            p, p["ev_cars_2026"] * A["net_t_per_subsidised_ev"] / p["car_life"]),
        "T2_t_redeploy": T2["t_diff_redeploy"], "T2_saving_retire_bn": T2["cost_saving_retire_bn"],
        "T2_t_retire": T2["t_diff_retire"],
    }


# ---------------------------------------------------------------------------
# 2. Monte Carlo: independent triangular draws (low, central, high)
# ---------------------------------------------------------------------------
def draw(table, n, rng):
    cols = {}
    for name, r in table.iterrows():
        if r.low == r.high:
            cols[name] = np.full(n, r.central)
        else:
            cols[name] = rng.triangular(r.low, r.central, r.high, n)
    return pd.DataFrame(cols)


def monte_carlo():
    rng = np.random.default_rng(SEED)
    draws = draw(TABLE, N_DRAWS, rng)
    rows = [metrics(r.to_dict()) for _, r in draws.iterrows()]
    return draws, pd.DataFrame(rows)


def summarise(mc):
    s = pd.DataFrame({
        "p05": mc.quantile(0.05), "median": mc.median(), "p95": mc.quantile(0.95),
        "central_run": pd.Series(metrics(P0)),
    })
    return s


# ---------------------------------------------------------------------------
# 3. Tornado: one parameter at a time to low / high, others central
# ---------------------------------------------------------------------------
def tornado(metric, top=12):
    base = metrics(P0)[metric]
    rows = []
    for name, r in TABLE.iterrows():
        if r.low == r.high:
            continue
        vals = []
        for v in (r.low, r.high):
            q = dict(P0)
            q[name] = v
            vals.append(metrics(q)[metric])
        rows.append({"param": name, "at_low": vals[0], "at_high": vals[1],
                     "swing": abs(vals[1] - vals[0])})
    df = pd.DataFrame(rows).sort_values("swing", ascending=False).head(top)
    return base, df


# ---------------------------------------------------------------------------
# 4. Actual budget scale (central values)
# ---------------------------------------------------------------------------
def budget_scale(p):
    A, B = m.scenario_A(p), m.scenario_B(p)
    ev_total = p["ev_cars_2026"] * (p["ev_sub_nat"] + p["ev_sub_local"])
    ev_city = p["ev_cars_2026"] * p["ev_sub_local"]
    fc_total = p["fcev_cars_2026"] * (p["fcev_sub_nat"] + p["fcev_sub_local"])
    fc_city = p["fcev_cars_2026"] * p["fcev_sub_local"]
    city_zev = ev_city + fc_city
    rows = [
        ("A  EV subsidy 2026 (passenger)", ev_total / 1e9, ev_city / 1e9,
         p["ev_cars_2026"] * A["net_t_per_subsidised_ev"], "lifetime"),
        ("B  FCEV subsidy 2026", fc_total / 1e9, fc_city / 1e9,
         p["fcev_cars_2026"] * B["net_t_per_subsidised_fcev"], "lifetime"),
    ]
    C1 = m.scenario_C(p, city_zev)
    rows.append(("C  city's ZEV money moved to buses", city_zev / 1e9, city_zev / 1e9,
                 C1["t_net"], "per year"))
    C2 = m.scenario_C(p, 10e9)
    rows.append(("C  +10 bn KRW/yr bus service", 10, 10, C2["t_net"], "per year"))
    D = m.scenario_D(p)
    rows.append(("D  convert all 1,044 buses (saving if >0)", -D["system_saving_bn"],
                 -D["system_saving_bn"], 0.0, "per year"))
    E = m.scenario_E(p)
    rows.append(("E  10,000 KRW monthly pass", p["fare_pass_cost"] / 1e9,
                 p["fare_pass_cost"] / 1e9, E["t_net"], "per year"))
    df = pd.DataFrame(rows, columns=["scenario", "public_cost_bn", "city_cost_bn",
                                     "tCO2", "tCO2_basis"])
    # mode share for the two bus cases
    ms = []
    for label, r, budget in [("city ZEV money to buses", C1, city_zev),
                             ("+10 bn KRW/yr", C2, 10e9)]:
        d_tr, d_car = m.mode_share_change(p, r["new_trips"], p["car_diversion"])
        ms.append({"case": label, "added_buses": r["buses"],
                   "transit_share_pp": d_tr, "car_share_pp": d_car})
    dE_car = -E["switched_trips_day"] / p["total_trips_day"] * 100
    ms.append({"case": "10,000 KRW pass", "added_buses": 0,
               "transit_share_pp": -dE_car, "car_share_pp": dE_car})
    return df, pd.DataFrame(ms)


def main():
    pd.options.display.float_format = "{:,.3f}".format
    c = metrics(P0)
    pd.Series(c).to_csv("results/central.csv", header=["value"])

    scale, modes = budget_scale(P0)
    scale.to_csv("results/budget_scale.csv", index=False)
    modes.to_csv("results/mode_share.csv", index=False)

    comp = pd.Series(m.cost_components_D(P0))
    comp.to_csv("results/cost_components_D.csv", header=["KRW_per_vehicle_day"])

    draws, mc = monte_carlo()
    mc_clean = mc.replace([np.inf, -np.inf], np.nan)
    summ = summarise(mc_clean)
    summ.to_csv("results/montecarlo_summary.csv")

    probs = {
        "P(C abatement > 0)": (mc["C_t_per_bn"] > 0).mean(),
        "P(D abatement > 0)": (mc["D_t_per_bn"] > 0).mean(),
        "P(C beats A per bn, all public money)": (mc["C_minus_A_t_per_bn"] > 0).mean(),
        "P(D cheaper than C per bus-day)": (mc["D_system_saving_bn"] > 0).mean(),
        "P(E beats A per bn, all public money)": (mc["E_t_per_bn"] > mc["A_t_per_bn_all"]).mean(),
        "P(grey-H2 tram > CNG bus per pkm)": (mc["T1_g_pkm_smr"] > mc["T1_g_pkm_cng_bus"]).mean(),
        "P(restructuring under C cuts CO2)": (mc["R_C_t"] > 0).mean(),
        "P(restructuring under C pays for itself)": (mc["R_C_net_cost_bn"] < 0).mean(),
        "P(D package (unit cost + better redesign) beats C, before tram)": (mc["D_package_net_bn"] > 0).mean(),
        "P(D package + tram restructuring beats C, after 2030)": (mc["D_package_with_tram_bn"] > 0).mean(),
        "P(added service after redesign cuts CO2)": (mc["C_after_redesign_t_per_bn"] > 0).mean(),
        "P(mix-H2 tram > battery tram per pkm)": (mc["T1_g_pkm_mix"] > mc["T1_g_pkm_battery"]).mean(),
    }
    pd.Series(probs).to_csv("results/probabilities.csv", header=["probability"])

    torn = {}
    for metric in ["C_minus_A_t_per_bn", "D_system_saving_bn", "D_package_net_bn"]:
        base, df = tornado(metric)
        df.to_csv(f"results/tornado_{metric}.csv", index=False)
        torn[metric] = (base, df)

    # break-even for D: which single changes flip the sign of the saving?
    be = []
    for name in ["licence_value_per_bus", "pay_change_per_driver",
                 "public_eff_penalty_share", "leakage_share", "depot_value_per_bus"]:
        lo, hi = TABLE.loc[name, "low"], TABLE.loc[name, "high"]
        grid = np.linspace(lo, hi, 401)
        vals = []
        for v in grid:
            q = dict(P0); q[name] = v
            vals.append(m.scenario_D(q)["system_saving_bn"])
        vals = np.array(vals)
        flip = grid[np.argmin(np.abs(vals))] if (vals.min() < 0 < vals.max()) else np.nan
        be.append({"param": name, "central": P0[name], "saving_at_low": vals[0],
                   "saving_at_high": vals[-1], "break_even_value": flip})
    pd.DataFrame(be).to_csv("results/break_even_D.csv", index=False)

    figures.all_figures(P0, mc_clean, torn, comp, TABLE)

    print("== central run"); print(pd.Series(c).round(3).to_string())
    print("\n== budget scale"); print(scale.to_string(index=False))
    print("\n== mode share"); print(modes.to_string(index=False))
    print("\n== Monte Carlo (5% / median / 95%)"); print(summ.round(3).to_string())
    print("\n== probabilities"); print(pd.Series(probs).round(3).to_string())
    print("\n== break-even D"); print(pd.DataFrame(be).round(4).to_string(index=False))
    for k, (b, df) in torn.items():
        print(f"\n== tornado {k} (base {b:,.2f})"); print(df.round(2).to_string(index=False))


if __name__ == "__main__":
    main()
