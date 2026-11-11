"""
Cost-effectiveness model: Daejeon ZEV purchase subsidies vs bus service.

Every function takes `p`, a dict {parameter name: value} loaded from
params.csv, and returns a dict of results.
Units: money in KRW, emissions in tCO2e, distance in km.

Scenarios
  A   battery-EV purchase subsidy (passenger car)
  B   hydrogen FCEV purchase subsidy (passenger car)
  C   more bus service under the current semi-public system (준공영제)
  D   more bus service under full public operation (완전공영제 / 교통공사)
  E   fare reduction (10,000 KRW monthly pass)
  T1  hydrogen tram operating emissions by hydrogen pathway
  T2  bus restructuring when the tram opens (준공영제 vs 교통공사)
"""

import numpy as np

BN = 1e9          # 1 billion KRW
G_PER_T = 1e6     # grams per tonne
SERVICE_YEARS = 15  # horizon used to average the grid factor for buses


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------
def grid_avg(p, start_year, years):
    """Average grid factor (gCO2/kWh) over `years` from `start_year`.
    Linear path between the 2026 and 2040 values, flat after 2040."""
    yrs = np.arange(start_year, start_year + int(round(years)))
    return np.interp(yrs, [2026, 2040], [p["grid_g_2026"], p["grid_g_2040"]]).mean()


def h2_ef(p, pathway):
    """Well-to-nozzle emissions of hydrogen, kgCO2e per kg H2."""
    if pathway == "mix":   # current Korean mobility supply mix
        s_bp, s_gr = p["h2_share_byproduct"], p["h2_share_green"]
        s_smr = max(0.0, 1 - s_bp - s_gr)
        return s_smr * p["h2_ef_smr"] + s_bp * p["h2_ef_byproduct"] + s_gr * p["h2_ef_green"]
    if pathway == "biogas":  # landfill biogas, backed up by the national mix
        cov = p["h2_biogas_coverage"]
        bio = p["h2_ef_biogas_process"] + p["h2_biogas_counterfactual"]
        return cov * bio + (1 - cov) * h2_ef(p, "mix")
    return p[f"h2_ef_{pathway}"]


def bus_g_per_km(p):
    """Well-to-wheel gCO2e per km of an ADDED bus, by the fuel mix of added
    buses; electric buses use the grid averaged over 2026-2040."""
    s_e, s_h = p["addbus_share_electric"], p["addbus_share_hydrogen"]
    s_cng = max(0.0, 1 - s_e - s_h)
    g_e = p["bus_e_kwh_km"] * grid_avg(p, 2026, SERVICE_YEARS)
    g_h = p["bus_h2_kg_km"] * h2_ef(p, "mix") * 1000
    return s_cng * p["bus_cng_g_km"] + s_e * g_e + s_h * g_h


def annuity(rate, years):
    """Capital recovery factor: annual payment per 1 KRW of capital."""
    return rate / (1 - (1 + rate) ** -years)


def per_bn(t, cost):
    """tCO2 per 1 bn KRW and KRW per tCO2 (inf if abatement <= 0)."""
    return t / (cost / BN), (cost / t if t > 0 else np.inf)


# ---------------------------------------------------------------------------
# A. Battery EV purchase subsidy
# ---------------------------------------------------------------------------
def scenario_A(p):
    """Per subsidised car (lifetime):
      saved = VKT * life * displace_share * ICE gCO2/km
      added = VKT * life * kWh/km * grid(avg over life)
              + battery_kWh * battery kgCO2/kWh - ICE powertrain credit
      net   = additionality * (saved - added)
    Non-additional (free-rider) buyers contribute zero abatement."""
    km = p["car_vkt"] * p["car_life"]
    saved = km * p["ev_displace_share"] * p["ice_g_km"] / G_PER_T
    use = km * p["ev_kwh_km"] * grid_avg(p, 2026, p["car_life"]) / G_PER_T
    mfg = p["ev_batt_kwh"] * p["batt_kgco2_kwh"] / 1000 - p["ice_mfg_credit_t"]
    gross = saved - use - mfg
    net_per_car = p["ev_additionality"] * gross

    out = {"gross_t_per_additional_ev": gross, "net_t_per_subsidised_ev": net_per_car}
    for view, cost in [("all", p["ev_sub_nat"] + p["ev_sub_local"]),
                       ("city", p["ev_sub_local"])]:
        t = BN / cost * net_per_car
        out[f"t_per_bn_{view}"], out[f"krw_per_t_{view}"] = per_bn(t, BN)

    # jobs: extra demand for cars created by the subsidy (one-off, national)
    cars = BN / (p["ev_sub_nat"] + p["ev_sub_local"])
    demand_bn = cars * p["ev_additionality"] * p["ev_price"] * p["ev_domestic_share"] / BN
    out["jobs_per_bn_national"] = demand_bn * p["car_jobs_per_bn"]
    out["jobs_per_bn_local"] = out["jobs_per_bn_national"] * p["ev_local_job_share"]
    return out


# ---------------------------------------------------------------------------
# B. Hydrogen FCEV purchase subsidy
# ---------------------------------------------------------------------------
def scenario_B(p, pathway="mix"):
    """Same structure as A. Fuel emissions = kg H2/km * kgCO2e/kg H2.
    The public share of a refuelling station is spread over the cars it serves."""
    km = p["car_vkt"] * p["car_life"]
    saved = km * p["fcev_displace_share"] * p["ice_g_km"] / G_PER_T
    fuel = km * p["fcev_kg_km"] * h2_ef(p, pathway) / 1000
    net_per_car = p["fcev_additionality"] * (saved - fuel - p["fcev_extra_mfg_t"])

    station = p["h2_station_subsidy"] / p["h2_station_cars_served"]
    views = {"all": p["fcev_sub_nat"] + p["fcev_sub_local"] + station,
             "city": p["fcev_sub_local"] + station * p["h2_station_local_share"]}
    out = {"net_t_per_subsidised_fcev": net_per_car}
    for view, cost in views.items():
        t = BN / cost * net_per_car
        out[f"t_per_bn_{view}"], out[f"krw_per_t_{view}"] = per_bn(t, BN)
    return out


# ---------------------------------------------------------------------------
# C / D. Bus service improvement
# ---------------------------------------------------------------------------
def cost_C(p):
    """Daily cost of one bus under 준공영제 (KRW per vehicle-day)."""
    return p["std_cost_veh_day"]


def cost_components_D(p):
    """Daily cost of one bus under full public operation, built up from the
    준공영제 cost item by item (KRW per vehicle-day).

    Vehicles are NOT in the buyout: their depreciation is already inside the
    standard cost, so buying them at book value only swaps one payment stream
    for another. Depots: if bought, the depot rent item is no longer paid."""
    base = p["std_cost_veh_day"]
    crf = annuity(p["discount_rate"], p["buyout_years"])
    licence = p["licence_value_per_bus"] * crf / 365
    depot = p["depot_value_per_bus"] * crf / 365 - (p["depot_rent_day"] if p["depot_value_per_bus"] > 0 else 0)
    transition = p["transition_cost_total"] * crf / (p["fleet"] * 365)
    return {
        "Semi-public standard cost": base,
        "Guaranteed profit + bonus": -base * p["profit_share"],
        "Duplicated executives/admin": -base * p["overhead_dup_share"],
        "Leakage (overpayment, fraud)": -base * p["leakage_share"],
        "Pay change per driver vs today": base * p["labour_share_of_cost"] * p["pay_change_per_driver"],
        "Public-operator efficiency": base * p["public_eff_penalty_share"],
        "Route-licence buyout": licence,
        "Depots (net of rent)": depot,
        "Transition cost": transition,
    }


def cost_D(p):
    return sum(cost_components_D(p).values())


def bus_service(p, cost_per_bus_day, budget=BN):
    """Spend `budget` per year (gross) on extra bus service.

    added buses    = budget / (cost per bus-day * 365)
    added bus-km   = buses * km per bus-day * 365
    new boardings  = B0 * ((N0 + buses)/N0)^elasticity - B0
    new trips      = new boardings * linked trips per boarding
    fare revenue   = new boardings * fare per boarding   -> net public cost
    avoided car-km = new trips * car diversion * car trip km / occupancy
    net tCO2       = avoided car-km * car g/km - added bus-km * bus g/km
    """
    buses = budget / (cost_per_bus_day * 365)
    bus_km = buses * p["bus_km_per_day"] * 365
    B0 = p["ridership_day"] * 365
    new_board = B0 * ((p["fleet"] + buses) / p["fleet"]) ** p["service_elasticity"] - B0
    new_trips = new_board * p["trip_per_boarding"]
    net_cost = budget - new_board * p["fare_per_boarding"]
    car_km = new_trips * p["car_diversion"] * p["car_trip_km"] / p["car_occupancy"]
    t_saved = car_km * p["car_fleet_g_km"] / G_PER_T
    t_bus = bus_km * bus_g_per_km(p) / G_PER_T
    t_net = t_saved - t_bus
    t_bn, krw_t = per_bn(t_net, net_cost)
    jobs = buses * (p["drivers_per_bus"] + p["other_staff_per_bus"])
    return {"buses": buses, "bus_km": bus_km, "new_trips": new_trips,
            "net_cost": net_cost, "car_km_avoided": car_km,
            "t_saved": t_saved, "t_bus": t_bus, "t_net": t_net,
            "t_per_bn": t_bn, "krw_per_t": krw_t,
            "jobs": jobs, "jobs_per_bn": jobs / (budget / BN)}


def scenario_C(p, budget=BN):
    return bus_service(p, cost_C(p), budget)


def scenario_D(p, budget=BN):
    """Marginal service bought at the public-operator unit cost, plus the
    system-wide annual saving (+) or extra cost (-) of converting all buses."""
    r = bus_service(p, cost_D(p), budget)
    r["unit_cost_change_pct"] = (cost_D(p) / cost_C(p) - 1) * 100
    r["system_saving_bn"] = (cost_C(p) - cost_D(p)) * p["fleet"] * 365 / BN
    return r


# ---------------------------------------------------------------------------
# R. Route restructuring (same buses, better network)
# ---------------------------------------------------------------------------
def scenario_R(p, governance="C"):
    """Redesign the network with (almost) the same buses.

    new trips     = base linked trips * trip_gain * implementation share
                    (implementation share differs by governance: 준공영제 vs 교통공사)
    avoided car-km= new trips * diversion * car trip km / occupancy
    added buses   = fleet * added_bus_share (cost and emissions charged)
    annual cost   = one-off cost * CRF(r, 10) + added buses * cost/day * 365
                    - new boardings * fare per boarding
    """
    impl = p["redesign_impl_" + governance]
    base_trips = p["ridership_day"] * 365 * p["trip_per_boarding"]
    new_trips = base_trips * p["redesign_trip_gain"] * impl
    new_board = new_trips / p["trip_per_boarding"]
    car_km = new_trips * p["car_diversion"] * p["car_trip_km"] / p["car_occupancy"]
    added = p["fleet"] * p["redesign_added_bus_share"]
    unit = cost_C(p) if governance == "C" else cost_D(p)
    t_bus = added * p["bus_km_per_day"] * 365 * bus_g_per_km(p) / G_PER_T
    t_net = car_km * p["car_fleet_g_km"] / G_PER_T - t_bus
    cost = (p["redesign_oneoff_cost"] * annuity(p["discount_rate"], 10)
            + added * unit * 365 - new_board * p["fare_per_boarding"])
    return {"new_trips": new_trips, "t_net": t_net, "net_cost_bn": cost / BN,
            "new_board": new_board}


def scenario_C_after_redesign(p, governance="C", budget=BN):
    """Marginal added service (as in C) on the redesigned, busier network."""
    q = dict(p)
    q["ridership_day"] = p["ridership_day"] * (1 + p["redesign_trip_gain"] * p["redesign_impl_" + governance])
    return bus_service(q, cost_C(p) if governance == "C" else cost_D(p), budget)


# ---------------------------------------------------------------------------
# E. Fare reduction
# ---------------------------------------------------------------------------
def scenario_E(p):
    """Cost = city's estimate of lost fare revenue. Car person-trips switching
    = switch share * daily car trips. No extra bus-km is added (assumes spare
    capacity), which is optimistic."""
    car_trips = p["total_trips_day"] * p["car_mode_share"]
    switched = car_trips * p["fare_switch_share"] * 365
    car_km = switched * p["car_trip_km"] / p["car_occupancy"]
    t = car_km * p["car_fleet_g_km"] / G_PER_T
    t_bn, krw_t = per_bn(t, p["fare_pass_cost"])
    return {"t_net": t, "net_cost": p["fare_pass_cost"], "t_per_bn": t_bn,
            "krw_per_t": krw_t, "switched_trips_day": switched / 365}


# ---------------------------------------------------------------------------
# W. Tram construction congestion: lost time and idling CO2
# ---------------------------------------------------------------------------
def scenario_W(p):
    """Extra hours at the bottlenecks during the works, for cars in the peak,
    cars off-peak, and bus passengers.

    cars, peak:     daily traffic * peak share * bottlenecks, slowed by `drop`
    cars, off-peak: daily traffic * (1 - peak share) * bottlenecks, slowed by `offpeak_drop`
    bus passengers: buses per peak hour * peak hours * load * bottlenecks, slowed by `bus_drop`
    extra hours per trip = L / (v * (1 - drop)) - L / v
    CO2 = car vehicle-hours * car idling rate + bus-hours * bus idling rate
    time cost = (car vehicle-hours * occupancy + bus passenger-hours) * value of time
    The part caused by the hydrogen choice = annual values * delay months / 12."""
    L, n = p["w_segment_km"], p["w_corridors"]
    def extra(v, drop):
        return L / (v * (1 - drop)) - L / v
    car_peak = p["w_daily_traffic"] * p["w_peak_share"] * n * extra(p["w_speed_before_kmh"], p["w_speed_drop"])
    car_off = p["w_daily_traffic"] * (1 - p["w_peak_share"]) * n * extra(p["w_offpeak_speed_kmh"], p["w_offpeak_drop"])
    buses = p["w_buses_per_peak_hour"] * p["w_peak_hours"] * n
    bus_h = buses * extra(p["w_speed_before_kmh"], p["w_bus_drop"])
    car_vh = (car_peak + car_off) * 250
    bus_vh = bus_h * 250
    bus_ph = bus_vh * p["w_bus_load"]
    t_yr = (car_vh * p["w_idle_co2_kg_h"] + bus_vh * p["w_bus_idle_co2_kg_h"]) / 1000
    cost_yr = (car_vh * p["car_occupancy"] + bus_ph) * p["w_vot_krw_h"] / BN
    f = p["w_h2_delay_months"] / 12
    return {"veh_hours_yr": car_vh, "bus_passenger_hours_yr": bus_ph,
            "t_yr": t_yr, "time_cost_bn_yr": cost_yr,
            "bus_share_of_time_cost": bus_ph / (car_vh * p["car_occupancy"] + bus_ph),
            "offpeak_share_of_car_hours": car_off * 250 / car_vh,
            "t_total": t_yr * p["w_years"], "time_cost_total_bn": cost_yr * p["w_years"],
            "t_h2_delay": t_yr * f, "time_cost_h2_delay_bn": cost_yr * f,
            "extra_min_per_vehicle": extra(p["w_speed_before_kmh"], p["w_speed_drop"]) * 60}


# ---------------------------------------------------------------------------
# M. Check of the claim "transit share 20% -> 40% cuts ~10% of city emissions"
# ---------------------------------------------------------------------------
def scenario_M(p, target_share=0.40):
    """Car trips fall by (target - current transit share) / car share (all of
    the shift comes from cars; optimistic). Car emissions fall in proportion.
    Extra bus/tram emissions are ignored (optimistic)."""
    shift = target_share - p["transit_share_motorized_2022"]
    car_cut = shift / p["car_share_motorized_2022"]
    t_cut_kt = car_cut * p["car_share_of_transport_ghg"] * p["transport_ghg_2018_kt"]
    return {"car_trip_cut_share": car_cut, "cut_kt": t_cut_kt,
            "cut_pct_of_city": t_cut_kt / p["daejeon_ghg_2018_kt"] * 100,
            "cut_pct_of_transport_gap": t_cut_kt / (p["transport_ghg_2018_kt"] - p["transport_ghg_2030_target_kt"]) * 100}


def pct_of_transport_gap(p, t_per_year):
    """Annual tonnes as % of the cut Daejeon needs in transport, 2018 -> 2030."""
    return t_per_year / ((p["transport_ghg_2018_kt"] - p["transport_ghg_2030_target_kt"]) * 1000) * 100


# ---------------------------------------------------------------------------
# Mode share
# ---------------------------------------------------------------------------
def mode_share_change(p, new_trips_year, car_diversion):
    """Percentage-point change in transit and car mode share (person-trips)."""
    tot = p["total_trips_day"] * 365
    return new_trips_year / tot * 100, -new_trips_year * car_diversion / tot * 100


# ---------------------------------------------------------------------------
# T1. Hydrogen tram: operating emissions per passenger-km
# ---------------------------------------------------------------------------
def scenario_T1(p):
    """Annual H2 = train-km/day * kg H2/train-km * 365.
    gCO2/pkm = H2 * EF(pathway) / passenger-km. Grid uses 2030-2059 average."""
    train_km = p["tram_trainkm_day"] * 365
    h2_kg = train_km * p["tram_h2_kg_km"]
    pkm = p["tram_riders_day"] * p["tram_trip_km"] * 365
    grid = grid_avg(p, 2030, 30)
    out = {"h2_t_day": h2_kg / 365 / 1000, "pkm_per_year": pkm}
    for path in ["smr", "byproduct", "mix", "biogas", "green"]:
        t = h2_kg * h2_ef(p, path) / 1000
        out[f"t_{path}"] = t
        out[f"g_pkm_{path}"] = t * G_PER_T / pkm
    t_batt = train_km * p["tram_batt_kwh_km"] * grid / G_PER_T
    out["t_battery"] = t_batt
    out["g_pkm_battery"] = t_batt * G_PER_T / pkm
    out["g_pkm_cng_bus"] = p["bus_cng_g_km"] / p["bus_avg_load"]
    out["g_pkm_e_bus"] = p["bus_e_kwh_km"] * grid / p["bus_avg_load"]
    out["g_pkm_car"] = p["car_fleet_g_km"] / p["car_occupancy"]
    # (a) the bus-km the tram replaces: removable overlapping buses (see T2),
    # assumed CNG (the current corridor fleet)
    removable = p["t2_overlap_buses"] * (1 - p["t2_keep_share"])
    out["t_replaced_buses"] = removable * p["bus_km_per_day"] * 365 * p["bus_cng_g_km"] / G_PER_T
    # fiscal side of the fuel choice: extra energy cost and extra CO2 vs an
    # electric (battery/catenary) tram, current hydrogen mix
    out["h2_extra_cost_bn"] = (p["tram_h2_energy_cost_yr"] - p["tram_elec_energy_cost_yr"]) / BN
    out["h2_extra_t_mix"] = out["t_mix"] - t_batt
    return out


# ---------------------------------------------------------------------------
# T2. Bus restructuring when the tram opens
# ---------------------------------------------------------------------------
def scenario_T2(p):
    """R = overlapping buses that could leave the tram corridor
         = overlap * (1 - keep_share).
    (i)  준공영제: a share `resistance` of R stays on the corridor carrying
         almost no new riders; the rest is redeployed.
    (ii) 교통공사: all of R is redeployed as feeders / higher frequency.
    Both cases pay for the same buses and run the same bus-km, so the bus
    emissions cancel; the difference is the riders the stuck buses would
    have attracted elsewhere (ii-a). Alternative (ii-b): retire the stuck
    buses instead -> saves their cost and their emissions."""
    R = p["t2_overlap_buses"] * (1 - p["t2_keep_share"])
    stuck = R * p["t2_resistance"]
    # riders gained by redeploying `stuck` buses (same formula as bus_service)
    B0 = p["ridership_day"] * 365
    new_board = B0 * ((p["fleet"] + stuck) / p["fleet"]) ** p["service_elasticity"] - B0
    car_km = new_board * p["trip_per_boarding"] * p["car_diversion"] \
        * p["car_trip_km"] / p["car_occupancy"]
    t_redeploy = car_km * p["car_fleet_g_km"] / G_PER_T
    cost_stuck_bn = stuck * p["std_cost_veh_day"] * 365 / BN
    t_retire = stuck * p["bus_km_per_day"] * 365 * bus_g_per_km(p) / G_PER_T
    return {"removable_buses": R, "stuck_buses": stuck,
            "t_diff_redeploy": t_redeploy, "fare_gain_bn": new_board * p["fare_per_boarding"] / BN,
            "cost_saving_retire_bn": cost_stuck_bn, "t_diff_retire": t_retire}
