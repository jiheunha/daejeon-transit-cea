"""Figures (PNG) drawn at the size they appear on a slide, so the text reads at
about the size of slide body text. Style follows the IAMC handout: Inter
font, light horizontal grid, no top/right frame, values written on the plot,
bold panel labels. One shared color per item (colors.py). No notes under the
plots: captions live in the slides. Called from run.py."""
import os
import glob
import textwrap
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

from colors import COLORS as K, WATERFALL, TORNADO_LOW, TORNADO_HIGH

# register Inter / Pretendard from the user font folder if matplotlib missed them
for d in (os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Windows\Fonts"), r"C:\Windows\Fonts"):
    for f in glob.glob(os.path.join(d, "Inter*.ttf")) + glob.glob(os.path.join(d, "Pretendard*.otf")):
        try:
            fm.fontManager.addfont(f)
        except Exception:
            pass

FS = 15          # base font size at slide scale
SLOT = (7.6, 4.8)    # figure slot of the "Text + Figure" layout, inches
WIDE = (12.3, 5.3)   # full-width slot of the "Appendix" layout

plt.rcParams.update({
    "font.family": ["Inter", "Pretendard", "DejaVu Sans"],
    "font.size": FS, "axes.titlesize": FS + 1, "axes.titleweight": "bold",
    "axes.titlelocation": "left", "axes.labelsize": FS,
    "xtick.labelsize": FS - 1, "ytick.labelsize": FS - 1, "legend.fontsize": FS - 1,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.edgecolor": "#6b6b6b", "xtick.color": "#333333", "ytick.color": "#333333",
    "axes.axisbelow": True, "grid.color": "#e3e3e3", "grid.linewidth": 0.9,
    "legend.frameon": False,
    "figure.facecolor": "white", "savefig.facecolor": "white",
})

PARAM_LABEL = {
    "ev_additionality": "EV additionality",
    "ice_g_km": "Petrol car g/km",
    "ev_displace_share": "EV km replacing petrol km",
    "car_life": "Car lifetime",
    "addbus_share_electric": "Electric share of added buses",
    "car_vkt": "Car km per year",
    "ev_sub_nat": "National EV subsidy",
    "bus_km_per_day": "Bus km per day",
    "std_cost_veh_day": "Cost per bus-day",
    "bus_cng_g_km": "CNG bus g/km",
    "car_diversion": "New riders who left a car",
    "ev_kwh_km": "EV kWh/km",
    "public_eff_penalty_share": "Public-operator efficiency",
    "pay_change_per_driver": "Pay change per driver",
    "licence_value_per_bus": "Route-licence value",
    "depot_value_per_bus": "Depot value",
    "leakage_share": "Leakage",
    "overhead_dup_share": "Duplicated overhead",
    "profit_share": "Profit + bonus",
    "discount_rate": "Discount rate",
    "transition_cost_total": "Transition cost",
}


def _q(s):
    s = s.dropna()
    return s.quantile(0.05), s.median(), s.quantile(0.95)


def _save(fig, name, rect=(0, 0, 1, 1)):
    """Save via a temporary file and retry: on this Windows machine another
    process sometimes holds the PNG for a moment."""
    import time
    fig.tight_layout(rect=rect)
    tmp, out = f"figures/_{name}.tmp.png", f"figures/{name}.png"
    for _ in range(10):
        try:
            fig.savefig(tmp, dpi=220)
            os.replace(tmp, out)
            break
        except OSError:
            time.sleep(0.5)
    else:
        raise OSError(f"could not write {out}")
    plt.close(fig)


def _fmt(v, nd=0):
    return f"{v:,.{nd}f}"


def _hbars(ax, rows, mc, fmt=_fmt, suffix="", whisker=True):
    """Horizontal median bars with 90% whiskers; value written past the whisker."""
    y = np.arange(len(rows))[::-1]
    his = [_q(mc[r[1]])[2] for r in rows]
    los = [_q(mc[r[1]])[0] for r in rows]
    span = max(max(his), 0) - min(min(los), 0)
    for yi, (label, col, c) in zip(y, rows):
        lo, md, hi = _q(mc[col])
        ax.barh(yi, md, color=c, height=0.66, edgecolor="none")
        if whisker:
            ax.plot([lo, hi], [yi, yi], color="#222222", lw=1.4)
        x = max(hi, 0) + 0.02 * span
        ax.text(x, yi, fmt(md) + suffix, va="center", fontsize=FS - 1, fontweight="bold", color="#222222")
    ax.set_yticks(y, [r[0] for r in rows])
    ax.tick_params(axis="y", length=0)
    ax.grid(axis="x")
    ax.spines["left"].set_visible(False)
    return y


# (bg) context -----------------------------------------------------------------
def fig_bg():
    d = pd.read_csv("data_context.csv").set_index("item")["value"]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=SLOT, gridspec_kw={"width_ratios": [1, 1.25]})
    yrs = ["2018", "2030\ntarget", "2033\ntarget"]
    vals = [d["transport_ghg_2018"], d["transport_ghg_2030_target"], d["transport_ghg_2033_target"]]
    ax1.bar(yrs, vals, color=[K["car"], "#9e9e9e", "#c4c4c4"], width=0.62)
    for i, v in enumerate(vals):
        ax1.text(i, v + 40, f"{v:,.0f}", ha="center", fontsize=FS - 1, fontweight="bold")
    ax1.set_ylim(0, 3100)
    ax1.set_ylabel("kt CO$_2$e")
    ax1.grid(axis="y")
    ax1.set_title("(a) Daejeon transport GHG")
    cities = ["Seoul", "Busan", "Gwangju", "Incheon", "Daegu", "Daejeon", "Ulsan"]
    sh = [d[f"transit_share_{c}"] for c in cities]
    y = np.arange(len(cities))[::-1]
    cols = ["#c4c4c4" if c != "Daejeon" else K["C"] for c in cities]
    ax2.barh(y, sh, color=cols, height=0.66)
    for yi, v, c in zip(y, sh, cities):
        ax2.text(v + 1, yi, f"{v:.1f}", va="center", fontsize=FS - 1,
                 fontweight="bold", color=K["C"] if c == "Daejeon" else "#333333")
    ax2.set_yticks(y, cities)
    ax2.tick_params(axis="y", length=0)
    ax2.spines["left"].set_visible(False)
    ax2.set_xlim(0, 66)
    ax2.set_xlabel("%")
    ax2.grid(axis="x")
    ax2.set_title("(b) Transit share, 2022")
    _save(fig, "bg_context")


# (a) abatement per bn KRW --------------------------------------------------------
def fig_a(mc):
    rows = [("EV subsidy, all money", "A_t_per_bn_all", K["A_all"]),
            ("EV subsidy, city money", "A_t_per_bn_city", K["A_city"]),
            ("FCEV subsidy, all money", "B_t_per_bn_all", K["B_all"]),
            ("FCEV subsidy, city money", "B_t_per_bn_city", K["B_city"]),
            ("More buses, semi-public", "C_t_per_bn", K["C"]),
            ("More buses, public operator", "D_t_per_bn", K["D"]),
            ("10,000 KRW monthly pass", "E_t_per_bn", K["E"])]
    fig, ax = plt.subplots(figsize=SLOT)
    _hbars(ax, rows, mc)
    ax.axvline(0, color="#222222", lw=1)
    ax.set_xlabel("tCO$_2$e per 1 bn KRW (median, 90% interval)")
    _save(fig, "a_cost_effectiveness")


# (b) tornados, one per figure ------------------------------------------------------
def _tornado(base, df, name, xlabel, top=8):
    df = df[df.swing > 1e-9].head(top).iloc[::-1]
    fig, ax = plt.subplots(figsize=SLOT)
    y = np.arange(len(df))
    ax.barh(y, df.at_low - base, left=base, color=TORNADO_LOW, height=0.68, label="low value")
    ax.barh(y, df.at_high - base, left=base, color=TORNADO_HIGH, height=0.68, label="high value")
    ax.axvline(base, color="#222222", lw=1.3)
    ax.axvline(0, color="#888888", lw=1, ls="--")
    ax.set_yticks(y, [PARAM_LABEL.get(p, p) for p in df.param])
    ax.tick_params(axis="y", length=0)
    ax.spines["left"].set_visible(False)
    ax.grid(axis="x")
    ax.set_xlabel(xlabel)
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=2)
    _save(fig, name)


def fig_b(torn):
    base, df = torn["C_minus_A_t_per_bn"]
    _tornado(base, df, "b1_tornado_bus_vs_ev", "Bus minus EV subsidy, tCO$_2$e per bn KRW")
    base, df = torn["D_system_saving_bn"]
    _tornado(base, df, "b2_tornado_public_operation", "Saving from public operation, bn KRW/yr")


# (c) waterfall, horizontal ---------------------------------------------------------
def fig_c(comp):
    labels = list(comp.index) + ["Public operator unit cost"]
    show = {"Semi-public standard cost": "Semi-public cost",
            "Guaranteed profit + bonus": "Profit + bonus",
            "Duplicated executives/admin": "Duplicated overhead",
            "Leakage (overpayment, fraud)": "Leakage",
            "Pay change per driver vs today": "Pay change per driver",
            "Public-operator efficiency": "Operator efficiency",
            "Route-licence buyout": "Route-licence buyout",
            "Depots (net of rent)": "Depots (net of rent)",
            "Transition cost": "Transition cost",
            "Public operator unit cost": "Public operator cost"}
    vals = list(comp.values / 1000)
    fig, ax = plt.subplots(figsize=SLOT)
    n = len(labels)
    y = np.arange(n)[::-1]
    run = vals[0]
    lo_lim = vals[0] * 0.93
    ax.barh(y[0], vals[0] - lo_lim, left=lo_lim, color=WATERFALL[labels[0]], height=0.66)
    ax.text(vals[0] + 0.6, y[0], f"{vals[0]:,.0f}", va="center", fontweight="bold", fontsize=FS - 1)
    for i in range(1, n - 1):
        v = vals[i]
        ax.barh(y[i], v, left=run, color=WATERFALL[labels[i]], height=0.66,
                edgecolor="#555555", linewidth=0.6)
        ax.text(max(run, run + v) + 0.6, y[i], f"{v:+.1f}", va="center", fontsize=FS - 1)
        run += v
    ax.barh(y[-1], run - lo_lim, left=lo_lim, color=WATERFALL[labels[-1]], height=0.66)
    ax.text(run + 0.6, y[-1], f"{run:,.0f}", va="center", fontweight="bold", fontsize=FS - 1)
    ax.set_yticks(y, [show[l] for l in labels])
    ax.tick_params(axis="y", length=0)
    ax.spines["left"].set_visible(False)
    ax.set_xlim(lo_lim, vals[0] * 1.06)
    ax.grid(axis="x")
    ax.set_xlabel("Thousand KRW per bus per day (axis starts at %d)" % lo_lim)
    _save(fig, "c_waterfall_semi_public_vs_public")


# (d) jobs ----------------------------------------------------------------------------
def fig_d(mc):
    rows = [("Bus service,\nsemi-public", "C_jobs", K["C"]),
            ("Bus service,\npublic operator", "D_jobs", K["D"]),
            ("EV subsidy,\nKorea (once)", "A_jobs_national", K["A_all"]),
            ("EV subsidy,\nDaejeon (once)", "A_jobs_local", K["A_city"])]
    fig, ax = plt.subplots(figsize=SLOT)
    for i, (label, col, c) in enumerate(rows):
        lo, md, hi = _q(mc[col])
        ax.bar(i, md, color=c, width=0.62)
        ax.plot([i, i], [lo, hi], color="#222222", lw=1.4)
        ax.text(i + 0.33, md, f"{md:,.1f}", va="center", fontsize=FS, fontweight="bold")
    ax.set_xticks(range(len(rows)), [r[0] for r in rows])
    ax.tick_params(axis="x", length=0)
    ax.set_ylabel("Jobs per 1 bn KRW")
    ax.grid(axis="y")
    _save(fig, "d_jobs_per_bn")


# (e) tram ----------------------------------------------------------------------------
def fig_e(mc):
    rows = [("Tram, grey H$_2$", "T1_g_pkm_smr", K["H2_smr"]),
            ("Tram, Korean H$_2$ mix", "T1_g_pkm_mix", K["H2_mix"]),
            ("Tram, biogas H$_2$ (part)", "T1_g_pkm_biogas", K["H2_biogas"]),
            ("Tram, green H$_2$", "T1_g_pkm_green", K["H2_green"]),
            ("Battery or catenary tram", "T1_g_pkm_battery", K["tram_battery"]),
            ("Electric bus", "T1_g_pkm_e_bus", K["bus_electric"]),
            ("CNG bus", "T1_g_pkm_cng_bus", K["bus_cng"]),
            ("Car", "T1_g_pkm_car", K["car"])]
    fig, ax = plt.subplots(figsize=SLOT)
    _hbars(ax, rows, mc)
    ax.set_xlabel("gCO$_2$e per passenger-km (median, 90% interval)")
    _save(fig, "e_tram_g_per_pkm")


# (f) restructuring, two stacked panels -------------------------------------------------
def fig_f(mc):
    mc = mc.copy()
    mc["R_C_gain"] = -mc["R_C_net_cost_bn"]
    mc["R_D_gain"] = -mc["R_D_net_cost_bn"]
    names = ["Redesign, semi-public", "Redesign, public operator", "Retire tram-duplicating buses"]
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=SLOT, sharey=False)
    _hbars(ax1, list(zip(names, ["R_C_t", "R_D_t", "T2_t_retire"], [K["R_C"], K["R_D"], K["T2"]])), mc)
    ax1.axvline(0, color="#222222", lw=1)
    ax1.set_title("(a) CO$_2$ avoided, t per year")
    _hbars(ax2, list(zip(names, ["R_C_gain", "R_D_gain", "T2_saving_retire_bn"], [K["R_C"], K["R_D"], K["T2"]])),
           mc, fmt=lambda v: f"{v:.1f}")
    ax2.axvline(0, color="#222222", lw=1)
    ax2.set_title("(b) City budget saving, bn KRW per year")
    _save(fig, "f_restructuring")


# (g) fiscal trend ----------------------------------------------------------------------
def fig_g():
    d = pd.read_csv("data_fiscal_series.csv")
    fig, ax = plt.subplots(figsize=SLOT)
    oc, cm = d.operating_cost_100m_krw / 10, d.city_input_100m_krw / 10
    ax.plot(d.year, oc, "o-", lw=2.6, ms=7, color=K["operating_cost"])
    ax.plot(d.year, cm, "s-", lw=2.6, ms=7, color=K["C"])
    for s, c, lab in ((oc, K["operating_cost"], "Operating cost"), (cm, K["C"], "City money")):
        ax.text(d.year.iloc[0] - 0.3, s.iloc[0], f"{s.iloc[0]:.0f}", ha="right", va="center", fontsize=FS - 1, color=c)
        ax.text(d.year.iloc[-1] + 0.3, s.iloc[-1], f"{s.iloc[-1]:.0f}", va="center", fontsize=FS, fontweight="bold", color=c)
        dy = 22 if lab == "Operating cost" else -26
        ax.text(d.year.iloc[-1], s.iloc[-1] + dy, lab, ha="right", fontsize=FS - 1, color=c, fontweight="bold")
    ax.set_xlim(d.year.iloc[0] - 1.2, d.year.iloc[-1] + 1.3)
    ax.set_ylim(0, 300)
    ax.set_ylabel("bn KRW per year")
    ax.grid(axis="y")
    _save(fig, "g_fiscal_trend")


# (h) scale ---------------------------------------------------------------------------------
def fig_h(mc):
    rows = [("10,000 KRW monthly pass", "gap_pct_E", K["E"]),
            ("Retire tram-duplicating buses", "gap_pct_T2_retire", K["T2"]),
            ("Redesign, public operator", "gap_pct_R_D", K["R_D"]),
            ("Redesign, semi-public", "gap_pct_R_C", K["R_C"]),
            ("2026 EV subsidy cohort", "gap_pct_EV_2026_cohort", K["A_all"]),
            ("+10 bn KRW/yr more buses", "gap_pct_C_10bn", K["C"]),
            ("Tram works congestion", "gap_pct_W", K["W"]),
            ("H$_2$ tram, not electric", "gap_pct_H2_vs_electric_tram", K["H2_mix"])]
    fig, ax = plt.subplots(figsize=SLOT)
    _hbars(ax, rows, mc, fmt=lambda v: f"{v:.2f}", suffix="%")
    ax.axvline(0, color="#222222", lw=1)
    ax.set_xlabel("% of the cut Daejeon needs in transport by 2030")
    _save(fig, "h_scale_vs_target")


# (i) construction congestion ------------------------------------------------------------------
def fig_i():
    d = pd.read_csv("data_context.csv").set_index("item")["value"]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=SLOT, gridspec_kw={"width_ratios": [1.5, 1]})
    rows = [("Car, morning", (d["speed_car_morning_low"] + d["speed_car_morning_high"]) / 2,
             f'{d["speed_car_morning_low"]:.0f} to {d["speed_car_morning_high"]:.0f}', K["car"]),
            ("Car, evening", (d["speed_car_evening_low"] + d["speed_car_evening_high"]) / 2,
             f'{d["speed_car_evening_low"]:.0f} to {d["speed_car_evening_high"]:.0f}', K["car"]),
            ("Bus, evening", d["speed_bus_evening"], f'{d["speed_bus_evening"]:.0f}', K["C"]),
            ("Bus, to Dunsan", d["speed_bus_evening_dunsan"], f'{d["speed_bus_evening_dunsan"]:.0f}', K["C"])]
    y = np.arange(len(rows))[::-1]
    for yi, (lab, v, txt, c) in zip(y, rows):
        ax1.barh(yi, v, color=c, height=0.62)
        ax1.text(v + 1.5, yi, txt + "%", va="center", ha="left", fontsize=FS - 1, fontweight="bold", color="white")
    ax1.set_yticks(y, [r[0] for r in rows])
    ax1.tick_params(axis="y", length=0)
    ax1.spines["left"].set_visible(False)
    ax1.set_xlim(-60, 0)
    ax1.grid(axis="x")
    ax1.set_title("(a) Speed change, %")
    for i, (route, b, a) in enumerate((("201", d["runs_201_before"], d["runs_201_after"]),
                                       ("211", d["runs_211_before"], d["runs_211_after"]))):
        ax2.bar(i - 0.2, b, width=0.38, color="#c4c4c4")
        ax2.bar(i + 0.2, a, width=0.38, color=K["C"])
        ax2.text(i - 0.2, b + 4, f"{b:.0f}", ha="center", fontsize=FS - 2)
        ax2.text(i + 0.2, a + 4, f"{a:.0f}", ha="center", fontsize=FS - 2, fontweight="bold", color=K["C"])
    ax2.set_xticks([0, 1], ["Route 201", "Route 211"])
    ax2.tick_params(axis="x", length=0)
    ax2.grid(axis="y")
    ax2.set_title("(b) Bus runs per day")
    from matplotlib.patches import Patch
    ax2.set_ylim(0, 340)
    ax2.legend(handles=[Patch(color="#c4c4c4", label="before"), Patch(color=K["C"], label="after")],
               loc="upper center", ncol=2, handlelength=1.0, columnspacing=0.8)
    _save(fig, "i_construction_congestion")


# (j) 특구1 loop bus against ordinary routes -----------------------------------------
def fig_j():
    d = pd.read_csv("data_context.csv").set_index("item")["value"]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=SLOT)
    for ax, vals, title, unit in (
            (ax1, [d["tukgu_riders_per_trip"], d["bus104_riders_per_trip"]], "(a) Riders per trip", ""),
            (ax2, [d["tukgu_headway_min"], d["bus604_headway_min"]], "(b) Minutes between buses", " min")):
        labels = ["Teukgu 1", "Route 104" if ax is ax1 else "Route 604"]
        ax.bar(labels, vals, color=[K["tukgu"], "#c4c4c4"], width=0.58)
        for i, v in enumerate(vals):
            ax.text(i, v + max(vals) * 0.02, f"{v:.0f}{unit}", ha="center", fontsize=FS + 1, fontweight="bold",
                    color=K["tukgu"] if i == 0 else "#333333")
        ax.set_ylim(0, max(vals) * 1.18)
        ax.tick_params(axis="x", length=0)
        ax.grid(axis="y")
        ax.set_title(title)
    _save(fig, "j_tukgu_bus")


# (k) annual money at stake, one scale ----------------------------------------------
def fig_k(mc):
    d = pd.read_csv("data_context.csv").set_index("item")["value"]
    mc = mc.copy()
    mc["tukgu"] = d["tukgu_cost_bn_yr"]
    rows = [("H$_2$ tram energy,|extra vs electric", "T1_h2_extra_cost_bn", K["H2_mix"]),
            ("Time lost to|tram works", "W_time_cost_bn_yr", K["W"]),
            ("Public-operation|saving", "D_system_saving_bn", K["D"]),
            ("Teukgu 1 bus,|cost of running it", "tukgu", K["tukgu"])]
    fig, ax = plt.subplots(figsize=SLOT)
    y = np.arange(len(rows))[::-1]
    for yi, (label, col, c) in zip(y, rows):
        lo, md, hi = _q(mc[col])
        ax.barh(yi, md, color=c, height=0.62)
        if hi - lo > 1e-9:
            ax.plot([lo, hi], [yi, yi], color="#222222", lw=1.4)
        ax.text(max(hi, md) + 0.5, yi, f"{md:.1f}", va="center", fontsize=FS, fontweight="bold")
    ax.set_yticks(y, [r[0].replace("|", chr(10)) for r in rows])
    ax.tick_params(axis="y", length=0)
    ax.spines["left"].set_visible(False)
    ax.axvline(0, color="#222222", lw=1)
    ax.grid(axis="x")
    ax.set_xlabel("bn KRW per year (median, 90% interval)")
    _save(fig, "k_money_per_year")


# trimmed variants for the shorter deck -------------------------------------------------
def fig_a2(mc):
    rows = [("EV subsidy", "A_t_per_bn_all", K["A_all"]),
            ("More buses, semi-public", "C_t_per_bn", K["C"]),
            ("More buses, public operator", "D_t_per_bn", K["D"])]
    fig, ax = plt.subplots(figsize=SLOT)
    _hbars(ax, rows, mc)
    ax.axvline(0, color="#222222", lw=1)
    ax.set_xlabel("tCO$_2$e per 1 bn KRW (median, 90% interval)")
    _save(fig, "a2_cost_effectiveness_short")


def fig_h2(mc):
    rows = [("Retire tram-duplicating buses", "gap_pct_T2_retire", K["T2"]),
            ("Redesign, public operator", "gap_pct_R_D", K["R_D"]),
            ("Redesign, semi-public", "gap_pct_R_C", K["R_C"]),
            ("2026 EV subsidy cohort", "gap_pct_EV_2026_cohort", K["A_all"]),
            ("Tram works congestion", "gap_pct_W", K["W"]),
            ("+10 bn KRW/yr more buses", "gap_pct_C_10bn", K["C"]),
            ("H$_2$ tram, not electric", "gap_pct_H2_vs_electric_tram", K["H2_mix"])]
    fig, ax = plt.subplots(figsize=SLOT)
    _hbars(ax, rows, mc, fmt=lambda v: f"{v:.2f}", suffix="%")
    ax.axvline(0, color="#222222", lw=1)
    ax.set_xlabel("% of the cut Daejeon needs in transport by 2030")
    _save(fig, "h2_scale_vs_target_short")


def all_figures(p, mc, torn, comp, table):
    fig_a2(mc)
    fig_h2(mc)
    fig_j()
    fig_k(mc)
    fig_bg()
    fig_a(mc)
    fig_b(torn)
    fig_c(comp)
    fig_d(mc)
    fig_e(mc)
    fig_f(mc)
    fig_g()
    fig_h(mc)
    fig_i()
