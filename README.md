# Daejeon: ZEV purchase subsidies, bus service and public bus operation

A cost-effectiveness model of Daejeon's transport climate spending. It compares zero-emission vehicle purchase subsidies, more bus service under the current semi-public bus system, full public operation of buses, a route redesign, a monthly transit pass and the hydrogen tram. I built it for the KAIST course GGS50014 "Project for Carbon Neutrality Assessments" (evaluation plan and expected results, November 2026).

Every input has a low, central and high value with its source in `params.csv`. Values with no data behind them are flagged ASSUMPTION and given a range. The results are expected results from an evaluation plan, so read them with those ranges in mind.

## Run it

Python 3.10 or later.

```
pip install -r requirements.txt
python run.py          # about 10 s: central case, 10,000 Monte Carlo draws (seed 2026), tornado, break-even, figures
python make_readme.py  # fills the results and parameter tables in this README from results/
```

The figures use the Inter font if it is installed and fall back to DejaVu Sans otherwise.

| File | Contents |
|---|---|
| `params.csv` | every number with low, central and high values, unit, source and a confidence flag |
| `model.py` | all equations, one function per scenario |
| `run.py` | central run, budget-scale run, Monte Carlo, tornado, break-even |
| `figures.py` | figures drawn at slide size (about 15 pt text), one shared color per item |
| `colors.py` | one color per item, shared by every figure (ColorBrewer hues, rules from Plante and Cushman 2020) |
| `data_fiscal_series.csv` | city money and operating cost for buses, 2015 to 2025 |
| `data_context.csv` | Daejeon transport emissions and targets, and transit share in seven metro cities |
| `results/` | all outputs as CSV, plus `console_output.txt` (the printout of `python run.py`) |
| `figures/` | every figure in the talk that the model draws |
| `README_template.md` | the text of this README before `make_readme.py` fills in the tables |

Confidence flags in `params.csv`: OFFICIAL is city or national government data. NEWS and LITERATURE are what they say. DERIVED is my arithmetic on sourced numbers. ASSUMPTION means no data was found, so the value is a bounded range explained in the note column.

## 1. Results (median and 90% interval, 10,000 draws)

| metric | 5% | median | 95% |
|---|---|---|---|
| A_t_per_bn_all | 341.99 | 687.81 | 1,273.82 |
| A_t_per_bn_city | 1,475.64 | 2,974.88 | 5,555.62 |
| A_krw_per_t_all | 785,041.21 | 1,453,881.36 | 2,924,085.10 |
| A_krw_per_t_city | 179,998.01 | 336,148.06 | 677,671.86 |
| B_t_per_bn_all | 87.18 | 186.45 | 329.38 |
| B_t_per_bn_city | 281.51 | 601.60 | 1,062.90 |
| B_krw_per_t_all | 3,035,807.87 | 5,361,711.13 | 11,461,042.55 |
| B_krw_per_t_city | 940,742.17 | 1,661,961.52 | 3,551,454.53 |
| C_t_per_bn | -673.72 | -470.31 | -308.65 |
| C_krw_per_t | nan | nan | nan |
| D_t_per_bn | -692.97 | -477.50 | -311.22 |
| D_krw_per_t | nan | nan | nan |
| E_t_per_bn | 109.21 | 341.80 | 793.63 |
| E_krw_per_t | 1,260,035.73 | 2,925,644.83 | 9,156,288.74 |
| D_unit_cost_change_pct | -6.48 | -0.97 | 4.53 |
| D_system_saving_bn | -11.60 | 2.47 | 16.60 |
| C_minus_A_t_per_bn | -1,777.29 | -1,171.48 | -777.99 |
| A_jobs_local | 0.14 | 0.36 | 0.79 |
| A_jobs_national | 5.23 | 9.37 | 16.15 |
| C_jobs | 9.88 | 10.94 | 12.35 |
| D_jobs | 9.85 | 11.06 | 12.62 |
| T1_g_pkm_smr | 67.12 | 97.95 | 151.59 |
| T1_g_pkm_mix | 37.72 | 60.25 | 100.88 |
| T1_g_pkm_biogas | 32.39 | 52.52 | 85.41 |
| T1_g_pkm_green | 6.17 | 12.78 | 23.67 |
| T1_g_pkm_battery | 12.96 | 21.47 | 36.38 |
| T1_g_pkm_e_bus | 24.73 | 37.47 | 56.72 |
| T1_g_pkm_cng_bus | 139.02 | 193.50 | 269.01 |
| T1_g_pkm_car | 140.74 | 165.97 | 193.56 |
| T1_t_smr | 12,287.30 | 14,200.98 | 16,330.25 |
| T1_t_mix | 6,356.45 | 8,750.55 | 11,801.50 |
| T1_t_battery | 2,160.26 | 3,089.84 | 4,379.23 |
| T1_t_biogas | 5,539.45 | 7,580.14 | 9,974.72 |
| T1_t_green | 960.17 | 1,853.05 | 2,938.10 |
| T1_t_replaced_buses | 7,201.51 | 12,133.08 | 19,329.87 |
| T1_h2_extra_cost_bn | 10.16 | 11.22 | 12.28 |
| T1_h2_extra_t_mix | 2,957.31 | 5,610.82 | 8,809.46 |
| R_C_t | -635.29 | 693.74 | 2,450.53 |
| R_D_t | -221.46 | 1,288.50 | 3,583.16 |
| R_C_net_cost_bn | -8.38 | -3.53 | 0.12 |
| R_D_net_cost_bn | -11.95 | -6.07 | -1.62 |
| R_D_minus_C_t | 66.64 | 553.79 | 1,586.82 |
| C_after_redesign_t_per_bn | -706.28 | -483.48 | -311.06 |
| D_package_net_bn | -9.30 | 5.09 | 19.56 |
| D_package_with_tram_bn | -0.39 | 14.70 | 30.71 |
| W_t_yr | 500.30 | 1,086.63 | 2,207.36 |
| W_time_cost_bn_yr | 4.83 | 10.20 | 20.37 |
| W_t_total | 1,381.09 | 3,061.20 | 6,501.72 |
| W_time_cost_total_bn | 13.26 | 28.82 | 59.68 |
| W_t_h2_delay | 134.24 | 516.40 | 1,354.63 |
| W_cost_h2_delay_bn | 1.29 | 4.86 | 12.39 |
| W_extra_min | 1.46 | 2.44 | 3.83 |
| W_bus_share_cost | 0.09 | 0.16 | 0.26 |
| W_offpeak_share | 0.05 | 0.16 | 0.30 |
| tram_extra_cost_bn_yr_ops | 10.16 | 11.22 | 12.28 |
| pkg_covers_pass_share | -0.00 | 0.13 | 0.28 |
| gap_pct_W | -0.25 | -0.12 | -0.06 |
| M_cut_kt | 342.96 | 393.28 | 447.47 |
| M_cut_pct_city | 4.01 | 4.59 | 5.23 |
| E_t_per_year | 11,870.78 | 37,198.24 | 84,794.13 |
| gap_pct_R_C | -0.07 | 0.08 | 0.28 |
| gap_pct_R_D | -0.03 | 0.15 | 0.41 |
| gap_pct_T2_retire | 0.21 | 0.43 | 0.81 |
| gap_pct_E | 1.36 | 4.26 | 9.71 |
| gap_pct_C_10bn | -0.52 | -0.38 | -0.24 |
| gap_pct_H2_vs_electric_tram | -1.01 | -0.64 | -0.34 |
| gap_pct_EV_2026_cohort | 0.04 | 0.08 | 0.15 |
| T2_t_redeploy | 260.23 | 670.81 | 1,531.36 |
| T2_saving_retire_bn | 4.65 | 9.32 | 16.46 |
| T2_t_retire | 1,808.40 | 3,738.23 | 7,038.34 |

| probability | value |
|---|---|
| P(C abatement > 0) | 0% |
| P(D abatement > 0) | 0% |
| P(C beats A per bn, all public money) | 0% |
| P(D cheaper than C per bus-day) | 61% |
| P(E beats A per bn, all public money) | 16% |
| P(grey-H2 tram > CNG bus per pkm) | 2% |
| P(restructuring under C cuts CO2) | 81% |
| P(restructuring under C pays for itself) | 94% |
| P(D package (unit cost + better redesign) beats C, before tram) | 71% |
| P(D package + tram restructuring beats C, after 2030) | 94% |
| P(added service after redesign cuts CO2) | 0% |
| P(mix-H2 tram > battery tram per pkm) | 100% |

Actual budget scale (central values):

| scenario                                  |   public_cost_bn |   city_cost_bn |     tCO2 | tCO2_basis   |
|:------------------------------------------|-----------------:|---------------:|---------:|:-------------|
| A  EV subsidy 2026 (passenger)            |             17.1 |            4.0 | 11,203.9 | lifetime     |
| B  FCEV subsidy 2026                      |              4.9 |            1.5 |  1,262.5 | lifetime     |
| C  city's ZEV money moved to buses        |              5.5 |            5.5 | -1,769.0 | per year     |
| C  +10 bn KRW/yr bus service              |             10.0 |           10.0 | -3,235.8 | per year     |
| D  convert all 1,044 buses (saving if >0) |             -3.6 |           -3.6 |      0.0 | per year     |
| E  10,000 KRW monthly pass                |            107.2 |          107.2 | 15,211.2 | per year     |

### What the numbers say

Adding buses to today's network and making the network work better behave very differently.

1. Adding bus-km to today's network raises CO2 in all 10,000 draws.
   - Daejeon carries about 1.08 boardings per bus-km, and an added bus-km attracts about 0.54 new boardings.
   - About 25% of new riders come from cars, so each new boarding avoids about 250 g of car CO2.
   - An added bus emits about 360 g/km if electric and about 1,250 g/km if CNG.
   - Break-even would need more than 100% of new riders to come from cars. Adding buses after a route redesign still raises CO2 in every draw.
   - This result assumes no car restraint. Higher parking charges or a congestion charge would raise the share of riders who leave their cars.
2. Route redesign with the same buses (R) cuts CO2 in about 81% of draws and pays for itself through extra fares in about 94%.
   - Under the semi-public system the median is about 700 tCO2 and +3.5 bn KRW a year. With a public operator that carries out more of the redesign it is about 1,300 t and +6.0 bn KRW.
   - The calibration comes from Daejeon's own reform of 2008-12-30, made under the semi-public system. Boardings rose 13.9% after three weeks, while trips excluding transfers rose 3.9%.
   - The idea that the semi-public system carries out less of a redesign is an ASSUMPTION. Daejeon did restructure under that system in 2008. The likely obstacle is operators resisting cuts to vehicles and profitable routes, because pay is per vehicle.
   - The tonnes are small next to Daejeon's transport emissions. The case for redesign rests on better service at no extra cost.
3. EV purchase subsidies buy the cheapest tonne per KRW in this comparison.
   - The cost is about 1.5 M KRW/tCO2e with national and city money combined, and about 0.34 M with city money alone, because the national government pays about 77% of each subsidy.
   - KDI (2024) finds about 73% of buyers would have bought an EV anyway; a 2026 KIPF stated-choice survey suggests fewer, so the additionality range runs from 15% to 60%. Hong, Kim and Verboven (2026) estimate 0.7 to 1.1 M KRW/t.
4. FCEV subsidies cost about three times as much per tonne, about 5.4 M KRW/t.
5. The 10,000 KRW monthly pass (E) beats EV subsidies in about 16% of draws, mostly when the optimistic 18% car-switching figure holds. Its median is about 2.9 M KRW/t, and about 4.8 M with a 9% upper bound.
6. Full public operation (D) on its own. The pay change per driver compared with today and public-operator efficiency are centred on 0% with symmetric ranges (pay per driver -5% to +5%, efficiency -6.5% to +6.5% of total cost), because the evidence points both ways. The pay change applies to the driver-labour share of cost, 65.6% in 2025.
   - At central values D is about 1.4% cheaper per bus-day, a saving of about 3.6 bn KRW a year. The Monte Carlo median is about +2.5 bn KRW a year (90% interval -11.6 to +16.6), and D is cheaper in about 61% of draws.
   - Narrower ranges (±2% and ±3%) give 69% and wider ones (±8% and ±10%) give 58%, with the same median.
   - Profit and bonus, duplicated executives and admin, and leakage add up to at most about 11.7 bn KRW a year. The licence buyout and depot purchase use most of it.
   - The saving disappears if pay per driver rises by more than about 2.1%, if public operation is more than about 1.4% less efficient, or if licences cost more than about 157 M KRW per bus.
   - The pay parameter is the change in pay per driver compared with today, plus any extra hiring to cut overtime. Today's driver pay (about 171.6 bn KRW a year) is already inside the semi-public cost, so a 0% change leaves it as it is, and +1% adds about 1.7 bn KRW a year. It does not assume more buses. Merging 13 companies with different pay scales tends to level pay up, while the KCTU report (p. 268) says semi-public drivers already earn more than drivers at public bus operators. A wage rise costs the city money and goes to drivers, so it counts as a cost here and as a gain in the labour metrics.
   - Without buying licences and depots, for example through gradual take-over, D saves about 11.7 bn KRW a year when wages and efficiency stay level.
7. Public operation combined with better redesign and tram-era restructuring.
   - Before the tram opens, the package has a median gain of about 5.1 bn KRW a year and is ahead of C in about 71% of draws.
   - After the tram opens in 2030 or later, a single operator can retire buses that duplicate it. That is worth about 9 bn KRW and 3,700 t a year.
   - With that step the median gain is about 14.7 bn KRW a year, ahead of C in about 94% of draws.
   - The case for 공영제 is about planning the network, and it is strongest when the tram opens.
8. Choosing hydrogen for the tram costs about as much as public operation would.
   - Operating CO2 is about 98 g/pkm with grey hydrogen and about 60 g/pkm with the Korean mobility mix. A battery or catenary tram is about 21 g/pkm.
   - Compared with an electric tram, hydrogen costs about 11 bn KRW a year more in energy and emits about 5,600 t a year more CO2.
   - The supply plan at 4,344 KRW/kg was scrapped in May 2025.
9. Jobs: 1 bn KRW a year of bus service keeps about 11 people employed in Daejeon. 1 bn KRW of EV subsidy creates about 9 job-years once across Korea, and about 0.4 in Daejeon.
10. Tram construction congestion (W). Closing 5 of 10 lanes on 대덕대교 adds about 2.4 minutes per peak car trip. Counting peak and off-peak cars and bus passengers at two bottlenecks of that size, the lost time burns about 1,090 tCO2 a year at idling rates (500 to 2,200) and costs about 10.2 bn KRW a year in travellers' time, about 16% of it bus passengers'. Over the works that is about 3,100 t and 29 bn KRW. If the hydrogen choice delays opening by six months, about 520 t and 4.9 bn KRW belong to that choice. Off-peak slowdown and bus counts are assumptions.
    - Can public operation pay for the 10,000 KRW pass? The package saving with tram restructuring (median 14.7 bn KRW a year) covers about 14% of the pass's 107.2 bn KRW cost.
11. Scale. Daejeon's plan cuts transport emissions from 2,701 kt (2018) to 1,828 kt by 2030, so the city needs about 873 kt a year less.
    - Route redesign covers about 0.1 to 0.15% of that cut, retiring tram-duplicating buses about 0.4%, and the 2026 EV subsidy cohort about 0.07%. The fare pass covers about 4% at the median, with a wide range.
    - Choosing hydrogen over an electric tram moves the city about 0.6% further from the target.
    - Kim Yun-gi (2026, p. 42) writes that raising transit's share from the 20% range to 40% would cut about 10% of city emissions. A rough check gives about 4.6% (4.0 to 5.2%), even if every new transit trip replaces a car trip and extra bus and tram emissions are ignored.
12. City spending on buses grew mostly because costs grew faster than fares.
    - Operating cost rose 47% from 2015 to 2025 (177.6 to 261.6 bn KRW). Fare and other revenue rose about 14%, so city money went from 38.3 to 102.4 bn KRW.
    - Bonus fraud of about 8.1 bn KRW over 2019 to 2023 is about 1.6 bn a year, about 1.6% of city money. Fraud is a real governance problem, and the budget growth comes mainly from labour cost and frozen fares.

## 2. Equations

Symbols match the names in `params.csv`. Outputs for A and B are lifetime tonnes per one-off subsidy. Outputs for C, D and E are tonnes per year per KRW per year. Both measure tonnes bought per KRW spent.

Grid factor, linear between 2026 and 2040 and flat after:
g(t) = interp(t; 2026 → `grid_g_2026`, 2040 → `grid_g_2040`); ḡ(start, n) = mean of g over n years.

Hydrogen, kgCO2e per kg H2 at the nozzle:
EF_mix = (1 − s_bp − s_green)·EF_smr + s_bp·EF_byproduct + s_green·EF_green
EF_biogas,tram = cov·(EF_process + EF_counterfactual) + (1 − cov)·EF_mix

### A. Battery EV subsidy (per subsidised car, lifetime)
km = VKT · life
saved = km · displace · g_ICE
added = km · kWh/km · ḡ(2026, life) + kWh_batt · EF_batt − credit_ICE_powertrain
net_t = additionality · (saved − added)
t per bn KRW = (10⁹ / subsidy) · net_t, with subsidy = national + city ("all") or city only ("city")
Jobs = (10⁹/subsidy) · additionality · price · domestic_share · jobs_per_bn_demand (× local share for Daejeon)

### B. FCEV subsidy
net_t = additionality · (km·displace·g_ICE − km·kgH2/km·EF_H2 − extra_mfg)
cost per car = national + city + station_subsidy / cars_served (city view: city share only)

### C. More bus service under the semi-public system (budget X KRW a year)
buses = X / (c_day · 365), with c_day = 2025 cost per licensed bus-day
ΔK = buses · km_day · 365
ΔB = B₀ · ((N₀ + buses)/N₀)^ε − B₀ (constant elasticity; B₀ boardings a year, N₀ = 1,044 buses)
new trips = ΔB · trips_per_boarding
net cost = X − ΔB · fare_per_boarding
avoided car-km = new trips · diversion · trip_km / occupancy
net t = avoided car-km · g_car − ΔK · g_bus
g_bus = s_CNG·g_CNG + s_e·kWh/km·ḡ(2026,15) + s_H2·kgH2/km·EF_mix·1000
jobs = buses · (drivers_per_bus + other_staff_per_bus)

### D. Same service under full public operation
c_D = c_C · (1 − profit − overhead − leakage + wage + efficiency)
  + (licence + depot) · CRF(r, 30)/365 − depot_rent (if depots are bought) + transition · CRF/(N₀·365)
CRF(r, n) = r / (1 − (1 + r)^−n), r = 4.5% (KDI social discount rate)
System saving (bn KRW a year) = (c_C − c_D) · N₀ · 365 / 10⁹
Vehicles are left out of the buyout. Their depreciation is already in c_C, so buying them at book value replaces one payment stream with another.

### E. 10,000 KRW monthly pass
switched trips/day = total_trips · car_share · switch_share
net t = switched · 365 · trip_km / occupancy · g_car; cost = 107.2 bn KRW a year in lost fares
No extra bus-km is charged, which is optimistic.

### Mode share (percentage points of all person-trips)
Δtransit = new trips / total trips; Δcar = −new trips · diversion / total trips

### R. Route redesign with the same buses
new trips = B₀ · trips_per_boarding · gain · impl_g (g is the governance model, C or D)
avoided car-km = new trips · diversion · trip_km / occupancy
net t = avoided car-km · g_car − N₀ · added_share · km_day · 365 · g_bus
net cost = one-off · CRF(r,10) + N₀ · added_share · c_g · 365 − new boardings · fare
Package (D against C) = system saving_D − (net cost R_D − net cost R_C), plus the T2 retirement saving after 2030

### T1. Hydrogen tram
H2 a year = train-km/day · kgH2/train-km · 365
t(pathway) = H2 · EF_pathway; g/pkm = t / (riders · trip_km · 365)
Battery or catenary tram: t = train-km · kWh/train-km · ḡ(2030, 30)
Replaced buses: t = R · km_day · 365 · g_CNG, with R = overlap · (1 − keep)
Extra cost of hydrogen over an electric tram = hydrogen energy cost − electricity cost; extra t = t(mix) − t(battery)

### T2. Bus restructuring when the tram opens
R = overlap · (1 − keep); stuck = R · resistance (semi-public case)
Redeploy the stuck buses: Δt = ΔB(stuck) · trips/boarding · diversion · trip_km / occupancy · g_car. Bus-km do not change, so bus emissions cancel.
Retire them: saving = stuck · c_C · 365; Δt = stuck · km_day · 365 · g_bus

### W. Tram construction congestion
peak vehicles = daily traffic · peak share · bottlenecks
extra hours per vehicle = L / (v0 · (1 − drop)) − L / v0
vehicle-hours a year = peak vehicles · extra hours · 250
CO2 = vehicle-hours · idling CO2 rate; time cost = vehicle-hours · occupancy · value of time
hydrogen share = annual values · delay months / 12

### M. Check of the 40% transit-share claim and scale against the target
car trip cut = (0.40 − transit share 2022) / car share 2022, all on a motorized-trip basis
cut (kt) = car trip cut · car share of transport emissions · transport emissions 2018
% of target gap = annual t / (transport 2018 − transport 2030 target)

## 3. Parameters (all of `params.csv`)

| name | low | central | high | unit | confidence | source |
|---|---|---|---|---|---|---|
| grid_g_2026 | 370 | 400 | 420 | gCO2/kWh | DERIVED | Official 2023 consumption-side factor 0.4173 t/MWh (국가온실가스통계관리위원회 2025-12-17; korea.kr newsId=156735726); 2026 assumed slightly lower |
| grid_g_2040 | 80 | 150 | 250 | gCO2/kWh | DERIVED | Derived: 11th 전력수급기본계획 2030 target 145.9 Mt / 642.6 TWh = ~227 g/kWh; 2035 NDC power -68.8~-75.3% vs 2018 = ~100-130 g/kWh (newsis NISX20251110_0003397077) |
| car_vkt | 9500 | 11200 | 13500 | km/yr | OFFICIAL | TS 2025 driving stats: non-commercial cars 30.8 km/day (fnnews 2026-06-29 202606291005221113) |
| car_life | 12 | 15 | 18 | yr | LITERATURE | Literature standard 15 yr (Hong Kim Verboven 2026 arXiv 2607.14446); scrapped cars average 213858 km (ddaily 2026-08-04) |
| ice_g_km | 160 | 200 | 230 | gCO2e/km | LITERATURE | Fuel-cycle WTW of new gasoline car 199.9 g/km sales-weighted (Hong et al. 2026 Table 3); low = hybrid counterfactual |
| car_fleet_g_km | 170 | 210 | 250 | gCO2e/km | LITERATURE | Gasoline WTW 225 g/km national avg 2017 (Choi et al. 2020 Applied Energy 265:114754) adjusted for hybrids/EVs in fleet |
| car_occupancy | 1.1 | 1.25 | 1.45 | persons/car | LITERATURE | Seoul region household travel survey 2010: 1.23-1.40 (80.5% driver only) |
| car_trip_km | 5 | 7.5 | 11 | km/trip | ASSUMPTION | No Daejeon value found; bounded by typical intra-city trip length |
| ev_sub_nat | 4.5e+06 | 5.6e+06 | 6.8e+06 | KRW/car | OFFICIAL | 2026 national cap 5.80M (zdnet 20251231124742); Ioniq 5 gets 5.64M; high adds national 전환지원금 1.0M |
| ev_sub_local | 1.35e+06 | 1.69e+06 | 2.04e+06 | KRW/car | OFFICIAL | Daejeon 2026 시비 1.74M max = 30% of national; Ioniq 5 1.69M; +0.3M local 전환지원금 (Seoul Shinmun 2026-07-23; city notice via blog) |
| ev_kwh_km | 0.17 | 0.2 | 0.24 | kWh/km | LITERATURE | Ioniq 5 LR 5.1-5.2 km/kWh label (carnoon) + ~5-15% charging loss |
| ev_batt_kwh | 58 | 70 | 84 | kWh | LITERATURE | Ioniq 5 LR 84 kWh; EV3/Model Y 58-81 kWh |
| batt_kgco2_kwh | 61 | 80 | 106 | kgCO2e/kWh | LITERATURE | IVL report C444 (2019): 61-106 kg/kWh |
| ice_mfg_credit_t | 1 | 2 | 3 | tCO2e/car | DERIVED | Engine/drivetrain manufacturing avoided; calibrated so central EV-minus-ICE vehicle-cycle = 3.6 t (Hong et al. 2026: 10.61 vs 6.99 t) |
| ev_additionality | 0.15 | 0.274 | 0.6 | share | LITERATURE | KDI FOCUS 135 (김현석 2024): 27.4% of 2019-22 subsidised EVs were caused by the subsidy (central, revealed preference). High: KIPF 2026 조세특례 심층평가(8) p.116, stated choice: cutting EV support by 4 M KRW drops the share staying with an EV from 80.1% to 33.4%; discounted for stated-preference bias |
| ev_displace_share | 0.7 | 0.9 | 1 | share | ASSUMPTION | No Korean data on second-car purchases; KCTU report pp.255-256 (ICE fleet stays ~23 million to 2030) suggests EVs partly add to the fleet |
| ev_cars_2026 | 1800 | 2350 | 2350 | cars/yr | NEWS | Daejeon 2026: 924 passenger EVs in H1 (newspim 20260129000509) + 1428 H2 applicants all funded (Seoul Shinmun 2026-07-23) |
| fcev_sub_nat | 2.25e+07 | 2.25e+07 | 2.25e+07 | KRW/car | OFFICIAL | National 22.5M fixed (newsis NISX20260105_0003465353) |
| fcev_sub_local | 1e+07 | 1e+07 | 1e+07 | KRW/car | DERIVED | Daejeon total 32.5M per car (asiae 2026012809452885014) minus national |
| fcev_kg_km | 0.0093 | 0.01 | 0.0115 | kgH2/km | LITERATURE | Nexo 2nd gen 107.6 km/kg; 1st gen 96.2 km/kg; WLTP 0.95 kg/100km |
| fcev_additionality | 0.3 | 0.5 | 0.8 | share | ASSUMPTION | KDI 2024: FCEV price elasticity -2.90 (vs -1.58 for EV) implies higher additionality; no direct estimate |
| fcev_displace_share | 0.7 | 0.9 | 1 | share | ASSUMPTION | same as EV |
| fcev_extra_mfg_t | 1 | 2 | 4 | tCO2e/car | ASSUMPTION | Fuel-cell stack + carbon-fibre tanks vs ICE; literature range |
| h2_station_subsidy | 1.5e+09 | 2.25e+09 | 3e+09 | KRW/station | NEWS | Passenger station ~3.0bn; national 50% + local 25% public (전북일보 2021); cap 3.0bn (asiae 2024) |
| h2_station_local_share | 0.33 | 0.33 | 0.33 | share | DERIVED | Local 25% of 75% public |
| h2_station_cars_served | 300 | 600 | 1200 | cars per station life | ASSUMPTION | No data; ~250 kg/day station / ~1 kg per car-day, partly used |
| fcev_cars_2026 | 150 | 150 | 150 | cars/yr | OFFICIAL | Daejeon 2026 150 FCEVs (asiae 2026012809452885014) |
| h2_ef_smr | 10.5 | 12.5 | 14.5 | kgCO2e/kgH2 | LITERATURE | Korean LCA: reforming 11.2 (Sustainability 2025 17(22):9944) + compression/delivery ~1.3 |
| h2_ef_byproduct | 1.5 | 4.5 | 11 | kgCO2e/kgH2 | LITERATURE | Korean LCA 2.63 + compression (allocation); system expansion 8.5-9.3 (Frontiers Energy Res. 2024) |
| h2_ef_green | 0.5 | 1.5 | 3 | kgCO2e/kgH2 | LITERATURE | Renewable electrolysis; 청정수소 grades 1-3; compression on grid |
| h2_share_byproduct | 0.55 | 0.7 | 0.75 | share | OFFICIAL | Mobility supply Sept 2025: by-product 35% + liquefied 39% (SK Incheon, by-product feed) + reforming 25% + electrolysis 1% (구준모 2025, h2hub.or.kr) |
| h2_share_green | 0 | 0.01 | 0.03 | share | OFFICIAL | same source |
| h2_ef_biogas_process | 1 | 2.5 | 4 | kgCO2e/kgH2 | ASSUMPTION | Landfill-gas upgrading + reforming energy + compression; biogenic CO2 counted as 0; no land-use change (waste feedstock) |
| h2_biogas_counterfactual | 0 | 2 | 7 | kgCO2e/kgH2 | ASSUMPTION | Displaced use of landfill gas: 0 if now flared; ~5-8 if now generating grid power (~4 kg CH4/kg H2 at 35% power efficiency on ~400 g/kWh grid) |
| h2_biogas_coverage | 0.2 | 0.4 | 0.8 | share | ASSUMPTION | Share of tram demand (3.25 t/day) biogas could supply; Hyundai Rotem proposal claimed 3.1 t/day; landfill gas declines after closure |
| std_cost_veh_day | 600000 | 686571 | 740000 | KRW/vehicle-day | OFFICIAL | Daejeon 준공영제 운영현황 2025: total cost per licensed bus-day 686571 (daejeon.go.kr FileUpload/DRH/202607/20260713103643109.pdf) |
| fleet | 1044 | 1044 | 1044 | buses | OFFICIAL | Daejeon licensed buses 2024-2025 (same source) |
| bus_km_per_day | 280 | 340 | 405 | km/licensed bus-day | DERIVED | CCEJ 2026-04-13: 154.25M bus-km in 2024 = 405; fuel-cost check (91553 KRW/day) suggests lower |
| ridership_day | 384624 | 384624 | 384624 | boardings/day | OFFICIAL | Daejeon 2025: 140.39M boardings (official 운영현황) |
| trip_per_boarding | 0.75 | 0.79 | 0.85 | linked trips/boarding | OFFICIAL | Transfer share ~21% of boardings (official 운영현황) |
| fare_per_boarding | 950 | 1111 | 1200 | KRW/boarding | DERIVED | Fare revenue 1560억 / 140.39M boardings (2025) |
| service_elasticity | 0.3 | 0.5 | 0.75 | - | LITERATURE | Paulley et al. 2006 / TRL593: bus vehicle-km elasticity +0.38 short run, +0.66 long run |
| car_diversion | 0.1 | 0.25 | 0.45 | share | LITERATURE | CARB 2013 review: 10-50% of new transit trips replace car trips; IPPR uses 24% (Dunkerley et al. 2018) |
| addbus_share_electric | 0.13 | 0.4 | 0.7 | share | ASSUMPTION | Fleet ~137 electric of 1044 (namu.wiki 2024-06, unofficial); new buses are mostly zero-emission |
| addbus_share_hydrogen | 0.04 | 0.15 | 0.25 | share | ASSUMPTION | ~43 hydrogen buses 2024 (namu.wiki); city plan ~20/yr (dailycc 664571) |
| bus_cng_g_km | 1050 | 1250 | 1500 | gCO2e/km | LITERATURE | CNG city bus ~0.45-0.55 Nm3/km x ~2.2 kgCO2/Nm3 + upstream and methane slip |
| bus_e_kwh_km | 1.1 | 1.3 | 1.5 | kWh/km | LITERATURE | Korean 11-12 m electric bus, incl. charging loss |
| bus_h2_kg_km | 0.07 | 0.08 | 0.1 | kgH2/km | LITERATURE | Hyundai Elec City FCEV / Universe FCEV |
| drivers_per_bus | 2.2 | 2.37 | 2.87 | drivers/bus | OFFICIAL | Daejeon 2025: 2473 drivers / 1044 buses (official); 2.87 = standard-cost norm (KCTU report p.265) |
| other_staff_per_bus | 0.23 | 0.23 | 0.23 | staff/bus | OFFICIAL | Daejeon 2025: 119 maintenance + 102 admin + 19 executives / 1044 |
| profit_share | 0.015 | 0.025 | 0.029 | share | OFFICIAL | 2025 standard cost: profit 10283 + performance bonus 9477 KRW/day = 2.9% of 686571; low = profit only |
| overhead_dup_share | 0.004 | 0.012 | 0.025 | share | DERIVED | Executives 4624 (0.67%) + admin 19124 (2.8%) KRW/day; merging 13 firms removes executives and part of admin |
| leakage_share | 0.002 | 0.008 | 0.025 | share | DERIVED | 감사원 2021: Seoul overpaid maintenance/insurance/tires ~0.3%/yr; Busan undeducted missed runs ~2.5%/yr; Pohang double depreciation |
| pay_change_per_driver | -0.05 | 0 | 0.05 | share of pay per driver | ASSUMPTION | Change in pay per driver under public operation compared with today. KCTU p.268: semi-public pay already above public bus workplaces (<0); KRITI 2023: public operation may raise pay and staffing (>0) |
| labour_share_of_cost | 0.656 | 0.656 | 0.656 | share | OFFICIAL | Daejeon 2025 운영현황: driver labour 450,358 of 686,571 KRW per bus-day |
| public_eff_penalty_share | -0.065 | 0 | 0.065 | share | ASSUMPTION | London tendering: no public/private cost difference; Barcelona: public cheaper incl. transaction costs; Korean public corps often costly |
| licence_value_per_bus | 3e+07 | 1e+08 | 2e+08 | KRW/bus | DERIVED | Seoul 2008 fleet-cut compensation 30M/bus (KRITI 2023); PE fund size 1.7-3.1억/bus incl. vehicles and depots (dealsite 118784) |
| depot_value_per_bus | 0 | 5e+07 | 1.5e+08 | KRW/bus | ASSUMPTION | No data on Daejeon depot ownership |
| depot_rent_day | 4149 | 4149 | 4149 | KRW/vehicle-day | OFFICIAL | 2025 standard cost depot item (official) |
| transition_cost_total | 5e+08 | 2e+09 | 5e+09 | KRW one-off | ASSUMPTION | No Korean estimate; IT, legal, set-up |
| discount_rate | 0.035 | 0.045 | 0.055 | - | OFFICIAL | KDI 예비타당성 social discount rate 4.5% |
| buyout_years | 30 | 30 | 30 | yr | ASSUMPTION | annualisation period |
| fare_pass_cost | 9e+10 | 1.072e+11 | 1.3e+11 | KRW/yr | NEWS | 정의당 대전시당 proposal (OhmyNews 2023-06-14): 10000 KRW monthly pass = 107.2bn/yr |
| total_trips_day | 2.2e+06 | 2.45e+06 | 2.9e+06 | person-trips/day | DERIVED | Derived: transit ~420k trips/day = 17.3% share in 2017 (booklet p.16) |
| car_mode_share | 0.425 | 0.45 | 0.53 | share | OFFICIAL | 2017 O/D: 42.5% (booklet p.16); 2024 survey 53% (different definition) |
| fare_switch_share | 0.01 | 0.03 | 0.18 | share of car trips | LITERATURE | Seoul 기후동행카드 4-9% of users came from car (dailian 1350937); 18% KOTI figure (user-supplied, not located) used as upper bound only |
| tram_trainkm_day | 8000 | 8860 | 9500 | train-km/day | DERIVED | Official timetable (daejeon.go.kr/djTram menuSeq=7704): 05:30-00:30, main 8 min peak (07-09, 18-20) / 10.67 min off-peak, branches 10.67 min; main loop 33.819 km both directions, branch round trips 7.26 + 3.27 km (KDI 2024 p.317); fleet 34 sets = 30 operating + 4 spare (KDI p.259) |
| tram_h2_kg_km | 0.32 | 0.346 | 0.4 | kgH2/train-km | OFFICIAL | KDI 2024 사업계획적정성재검토 appendix p.317: 12 tanks x 6.54 kg = 78.48 kg; 2.89 km/kg (0.346 kg/km); range 227 km. Real-world range +-15%. Cross-check: city 3.25 t/day (Segye 2026-06-24) |
| tram_riders_day | 40000 | 70000 | 110000 | boardings/day | ASSUMPTION | No tram forecast published (예타 exempt 2019; KDI 2024 re-review did not re-estimate daily demand). Anchor: design peak max load 1668 pax/h/direction in 2030 (KDI 2024 p.151) = 8.38 min headway; 2012 plan: rail 461k/day citywide in 2030 |
| tram_trip_km | 4 | 5.5 | 7 | km/trip | ASSUMPTION | No data |
| tram_batt_kwh_km | 3.5 | 5 | 7 | kWh/train-km | ASSUMPTION | Lille Citadis simulation ~3.1 kWh/vehicle-km; 35 m 81 t unit; fuel-cell equivalent ~6 kWh |
| bus_avg_load | 4 | 6 | 10 | passengers/bus | ASSUMPTION | Derived: 140M boardings x ~5 km / ~125-154M bus-km |
| t2_overlap_buses | 80 | 150 | 250 | buses | ASSUMPTION | No route data published; 13 routes in sections 1-2 (cctoday 2212021); ~10 buses/route |
| t2_keep_share | 0.3 | 0.5 | 0.7 | share | ASSUMPTION | Share kept for local access |
| t2_resistance | 0.2 | 0.5 | 0.8 | share | ASSUMPTION | Share of removable buses operators keep on the corridor under 준공영제 |
| ev_price | 4e+07 | 5e+07 | 6e+07 | KRW/car | ASSUMPTION | Typical subsidy-eligible EV <53M |
| ev_domestic_share | 0.55 | 0.7 | 0.85 | share | ASSUMPTION | Imported EVs (Tesla, BYD etc.) take a large share |
| car_jobs_per_bn | 4 | 6 | 8 | job-years per bn KRW final demand | ASSUMPTION | Bank of Korea input-output employment inducement range for motor vehicles |
| ev_local_job_share | 0.01 | 0.03 | 0.08 | share | ASSUMPTION | No car assembly in Daejeon (tyre plant only) |
| redesign_trip_gain | 0.02 | 0.05 | 0.12 | share of linked trips | LITERATURE | Daejeon 2008-12-30 reform: boardings +13.9% but trips excl. transfers +3.9% after 3 weeks (daejeon.go.kr press release 2009-01-18); Houston 2015: bus +1.2% yr 1 (Streetsblog 2016); Seoul 2004: bus +9.9% (with fare integration and median bus lanes; mediahub.seoul.go.kr 145901) |
| redesign_impl_C | 0.3 | 0.6 | 0.9 | share | ASSUMPTION | Share of the redesign actually implemented under 준공영제 (operators negotiate routes; compensation per vehicle). Daejeon 2008 reform WAS done under 준공영제 |
| redesign_impl_D | 0.7 | 0.9 | 1 | share | ASSUMPTION | Share implemented by a single public operator that owns routes |
| redesign_added_bus_share | 0 | 0 | 0.02 | share of fleet | NEWS | Daejeon 2008 added 21 buses (~2% of fleet) to fix overloads |
| redesign_oneoff_cost | 5e+08 | 2e+09 | 5e+09 | KRW one-off | ASSUMPTION | Planning study, stop relocation (80 moved + 30 new in 2008), information; no cost figure found |
| tram_h2_energy_cost_yr | 1.19e+10 | 1.35e+10 | 1.5e+10 | KRW/yr | NEWS | Hyundai Rotem 30-yr traction energy cost 358.2bn (2025-07; was 147bn in 2023-11) = 11.9bn/yr (대전참여자치시민연대 newsletter 2026-10-14); council forum 2026-09-22: ~15bn/yr at market H2 price 11000-13000 KRW/kg |
| tram_elec_energy_cost_yr | 2e+09 | 2.25e+09 | 2.5e+09 | KRW/yr | NEWS | Council forum 2026-09-22: catenary tram electricity 2.0-2.5bn/yr (news.tf.co.kr 2368939) |
| daejeon_ghg_2018_kt | 8559.3 | 8559.3 | 8559.3 | ktCO2e | OFFICIAL | 대전시 탄소중립녹색성장 기본계획 via 버스공영제.pdf p.42 Table 14 |
| transport_ghg_2018_kt | 2701.2 | 2701.2 | 2701.2 | ktCO2e | OFFICIAL | same Table 14 (수송) |
| transport_ghg_2030_target_kt | 1828 | 1828 | 1828 | ktCO2e | OFFICIAL | same Table 14: -32% by 2030 (2033: 1719.1 kt, -36%) |
| transit_share_motorized_2022 | 0.227 | 0.227 | 0.227 | share | OFFICIAL | KTDB 2022 national transport survey via 버스공영제.pdf p.41 Figure 6 (car/transit/taxi basis) |
| car_share_motorized_2022 | 0.6 | 0.66 | 0.7 | share | ASSUMPTION | Read off Figure 6 (taxi ~10%); not printed in the book |
| car_share_of_transport_ghg | 0.45 | 0.55 | 0.65 | share | ASSUMPTION | Passenger cars' share of Daejeon transport emissions; not published |
| w_daily_traffic | 50000 | 60000 | 70000 | vehicles/day | NEWS | 대덕대교: close to 60,000 vehicles a day (경향신문 2026-10-28, khan.co.kr/article/202610281625001) |
| w_peak_share | 0.2 | 0.28 | 0.35 | share of daily traffic | ASSUMPTION | Share of daily traffic in the congested morning and evening peaks; no Daejeon count found |
| w_corridors | 1 | 2 | 4 | bottlenecks | ASSUMPTION | Number of 대덕대교-sized bottlenecks: 대덕대교 and 한밭대로 중리 are measured; 14 work sections in total |
| w_segment_km | 0.8 | 1.5 | 2.5 | km | ASSUMPTION | Length of road slowed at each bottleneck; not published |
| w_speed_before_kmh | 15 | 20 | 25 | km/h | DERIVED | Peak speed before closure; after closure 8-13 km/h on 둔산→연구단지 evening after a 37-42% drop implies roughly 13-22 km/h before (대전참여자치시민연대 2026-11-05) |
| w_speed_drop | 0.25 | 0.35 | 0.42 | share | NEWS | Measured: car speed -19 to -30% morning, -37 to -42% evening at 대덕대교; -44% evening at 한밭대로 중리 (대전참여자치시민연대 2026-11-05) |
| w_years | 2 | 2.6 | 4 | years | NEWS | 대덕대교 closure 2026-10-19 to 2029-05-12 = 2.6 years; tram works run to 2030 H2 |
| w_idle_co2_kg_h | 1.4 | 2.3 | 3.5 | kgCO2 per vehicle-hour | LITERATURE | Extra time in congestion burns fuel at about the idling rate: 0.6-1.5 L/h petrol x 2.3 kg CO2/L (US DOE idling estimates) |
| w_vot_krw_h | 10000 | 15000 | 20000 | KRW per person-hour | ASSUMPTION | Value of travel time; KDI preliminary feasibility guideline value not retrieved |
| w_h2_delay_months | 0 | 6 | 12 | months | ASSUMPTION | Opening slip attributable to the hydrogen choice: test running extended 6 months, no technical standard yet (Segye 2026-06-24; 띠모크라시 2026-10-14) |
| w_offpeak_speed_kmh | 30 | 35 | 45 | km/h | ASSUMPTION | Off-peak speed through the bottleneck before closure; not measured |
| w_offpeak_drop | 0 | 0.05 | 0.15 | share | ASSUMPTION | Off-peak slowdown; the NGO measured peaks only and the city reports 24-hour averages |
| w_bus_drop | 0.2 | 0.27 | 0.34 | share | NEWS | Measured evening bus speed change at 대덕대교: -27% (-34% toward 둔산) (대전참여자치시민연대 2026-11-05) |
| w_buses_per_peak_hour | 30 | 50 | 80 | buses/hour | ASSUMPTION | City buses crossing a bottleneck per peak hour, both directions; route-level counts not published |
| w_bus_load | 20 | 30 | 45 | passengers/bus | ASSUMPTION | Average peak load on buses crossing the bottleneck |
| w_peak_hours | 3 | 4 | 5 | hours/day | ASSUMPTION | Congested hours per weekday (morning + evening) |
| w_bus_idle_co2_kg_h | 3 | 5 | 7 | kgCO2 per bus-hour | LITERATURE | CNG city bus idling; literature range |

## 4. Data I still need from the city (data-collection plan)

| # | Data | From whom | Why it matters |
|---|---|---|---|
| 1 | Hydrogen sourcing plan for Line 2: supplier, pathway (SMR, by-product, biogas, electrolysis), volume and contract price | 대전시 트램건설본부, 대전교통공사, 현대로템 | Tram CO2 varies about eight times by pathway (13 to 98 g/pkm) |
| 2 | Current use of Daejeon landfill gas (flared or used for power), volume and decline curve | 대전시 자원순환과 | Decides whether biogas hydrogen is low carbon |
| 3 | Line 2 daily ridership forecast | 대전시 기본계획 변경 용역 | Only the design peak load (1,668 passengers an hour per direction, KDI 2024) is public |
| 4 | Bus routes and vehicles that overlap the Line 2 corridor, and the network plan for opening day | 대전시 버스정책과 | Sets the size of T2, now an ASSUMPTION |
| 5 | Annual bus-km by route (운행실적) | 버스정책과, 운송사업조합 | The NGO figure of 405 km per bus-day conflicts with a fuel-cost check |
| 6 | Official fleet by fuel (CNG, electric, hydrogen) | 버스정책과 | Only unofficial counts found |
| 7 | Audited accounts by company: dividends, executive pay, related-party deals, actual against standard cost by item | 운영현황 공시, 회계감사 | Leakage is calibrated on other cities' audits |
| 8 | Final report of the 2021 공영제 feasibility study (225 M KRW) | 대전시 | Only press summaries found; it may contain buyout estimates |
| 9 | Legal status of route licences and compensation precedent | 법무, 국토부 | The licence buyout is the largest new cost in D |
| 10 | Driver wages, hours, overtime and shifts by company | 노조, 운송사업조합 | The pay change per driver is the second-largest driver of D |
| 11 | Income profile of bus riders and of EV subsidy recipients (가구통행실태조사 microdata, 무공해차 통합누리집 recipient data) | KOTI, 환경부 | Partial data only. Transport takes 11.9% of spending in the lowest income quintile and 7.0% in the highest (2025 Q3 household survey, via Kim 2026, p. 40). A Jeju 2021 survey found the largest EV-owner group (35%) had household income of 5 M KRW a month or more |
| 12 | Car trip length and occupancy in Daejeon | KOTI 전국여객O/D | Both are bounded assumptions |
| 13 | Rider survey: what new riders did before (car, walk, no trip) | own survey or the city | The car-diversion share is the main lever for C |
| 14 | 2026 EV and FCEV budget split between national and city money, and the average subsidy actually paid | 대전시 기후환경정책과 | Only caps and car counts found |
| 15 | Tram decision record: technical-proposal score sheets, evaluator list, operating-cost scores, 2023-12 committee papers | 대전시 (정보공개청구) | Process evaluation of the fuel choice |
| 16 | Same-basis 30-year life-cycle cost and CO2 for hydrogen, battery and catenary trams | 대전시 기본계획 변경 용역 | The T1 cost line relies on NGO and forum figures |
| 17 | Route-level ridership before and after the 2008 reform and later changes; route duplication and detour indices | 버스정책과 | Calibrates the redesign gain and the implementation share |
| 18 | Car share of motorized trips and passenger cars' share of transport emissions in Daejeon | KTDB, 대전시 온실가스 인벤토리 | Needed to test the 40% transit-share claim properly |

## 5. Mapping to the course frameworks

Six-step assessment process. Section 1 sets the purpose and scope. Scenarios A to E, R, T1, T2 and M specify the process. This model and section 4 are the design and data plan. `run.py` does the analysis, and the figures are the report.

Outcome and impact evaluation, with CEA.
- Outcome: mode share, riders, bus-km. Daejeon's 2025 targets were a 40% transit share and 10% for bicycles (green-transition booklet, p. 16). KTDB 2022 puts transit at 22.7% of motorized trips, second lowest among seven metro cities.
- Impact: tCO2 and jobs. The city's plan sets transport at 1,828 kt by 2030 (-32% from 2018).
- CEA: KRW per tCO2 and tCO2 per bn KRW. This is a cost-effectiveness study, so health, time savings, access and congestion are not monetised. Adding them would favour buses.
- Fiscal outcome: city money for buses rose from 38.3 bn KRW (2015) to 102.4 bn (2025) while ridership has not returned to its 2019 level.

Process evaluation, governance and the 5C variables.
- Capability: Daejeon has no experience running buses and owns no depots or buses. The KCTU report (p. 264) argues this is why cities cannot discipline operators. The 2021 feasibility study concluded that the semi-public system was "appropriate for now".
- Content: the standard-cost contract pays per licensed vehicle, plus profit, so removing buses removes revenue (T2). For the tram, the policy names hydrogen without naming a hydrogen source (section 6).
- Context: the 2026 change of mayor, the tram delay to 2030, national EV subsidy design and fuel-tax cuts.
- Commitment: repeated feasibility studies without a decision. The new mayor calls 공영제 premature until the tram opens.
- Client and coalition: 13 operators, about one sixth of the fleet owned by the private-equity firm 차파트너스 (대전승합, 동인여객), and a union in a "status-quo bargain" (KCTU pp. 264 to 269). Both sides gain from the standard-cost structure, while riders and people who do not drive are unorganised. The 2026 proposal from 대전체제전환운동모임 is a three-stage path: reform the semi-public system, then run core routes directly when the tram opens, then buy buses and depots.

Barriers to evaluation.
- Goal ambiguity: the 40% transit target has no budget attached, and the hydrogen tram has no emission target.
- Measurement: bus-km, fleet mix, company accounts and tram demand are unpublished.
- Politics: each option has an advocacy coalition. I favour 완전공영제, and the results do not support the climate argument for it.
- Bureaucratic resistance: operators hold the data needed to evaluate them.

Attribution.
- After 2030 the tram, the bus-network overhaul, fare changes (K-패스, the 2024 fare rise) and the recovery from COVID will all move bus ridership at the same time.
- An ex-post evaluation of a bus reform needs to separate these effects. Options are a difference-in-differences design against a comparison city, route-level data and a rider survey on previous mode.
- For EV subsidies the attribution problem is the free-rider problem. The KDI estimate that 27% of subsidised EVs were additional is national, so it may differ for Daejeon.

## 6. The hydrogen tram and the missing hydrogen plan

Sources are the city, the press, KDI (2024) and the 대전참여자치시민연대 newsletter of 2026-10-14, which is built from information-disclosure requests.

| Date | Event |
|---|---|
| 2022-02 | City advisory committee calls hydrogen "unverified technology". Battery with 10.5 km of catenary is chosen |
| 2022-12 | 철도정책위원회 agrees to pick the power supply by competition in the formal tender, with operating cost in the scoring |
| 2023-07 to 10 | A "technical proposal" call, separate from the formal tender. On 2023-10-19 seven evaluators pick hydrogen |
| 2023-11-07 | The city confirms the hydrogen tram |
| 2023-12 | 철도정책위원회 receives a written report a month later without deliberating, although the call said a rejection at policy review could cancel the selection |
| 2024 | KDI re-review lists hydrogen production and refuelling as private investment (p. 154). KDI notes that the basic design report gave no traction energy cost or basis, and builds its own estimate from the city's answers (p. 258). Official specification: 78.48 kg tank, 2.89 km/kg, 227 km range (p. 317) |
| 2024 | Formal tender with hydrogen as a condition draws one bidder, 현대로템: 34 sets for 293.4 bn KRW |
| 2025-05 | 현대로템's plan to build hydrogen production (90 bn KRW, 4,344 KRW/kg for 30 years) is scrapped |
| 2025-07 | Proposed 30-year traction energy cost rises from 147 bn to 358.2 bn KRW |
| 2026 | No technical standard for hydrogen trams yet (10 items to add to 140). Vehicle production starts in 2027 Q3 at the earliest, and opening slips to late 2030. Project cost rises from about 0.74 tn KRW (2019) to about 1.63 tn |
| 2026-10 | The new mayor says the hydrogen decision will follow an audit this year. The city is studying whether to build its own hydrogen production |

How this maps to the course.
- Goal specification and ambiguity. "Zero-emission tram" is defined at the tailpipe. The tram needs about 3.25 t of hydrogen a day and has no secured source. With grey hydrogen its operating CO2 is about 4.6 times an electric tram's, and higher than the CNG buses it replaces in about 69% of draws.
- 5C content. The vehicle technology was fixed before its main input (hydrogen source, price and CO2 intensity), and by a different body from the one the ordinance names.
- 5C capability and commitment. There is no technical standard, the tender had one bidder, and the supply plan was dropped. The current plan-revision study reportedly leaves out both the power supply and type approval.
- What gets measured gets done. Hydrogen vehicles count as zero emission in national targets, so upstream CO2 never appears in city indicators. The evaluation plan should require well-to-wheel gCO2e per passenger-km and disclosure of hydrogen origin (청정수소 인증 grade).
- Politics. Some call the audit retaliation against the previous administration. The evaluation should rest on disclosed, same-basis life-cycle cost and CO2 for hydrogen, battery and catenary trams.
- Attribution. Mode-share changes after 2030 will mix tram, bus redesign and fare effects (section 5).

## 7. Plain-language summary of the expected results

Putting more buses on Daejeon's current routes would raise CO2, because the buses are lightly used and most new riders were not driving. Redesigning routes with the same buses helps a little and pays for itself through fares, so it is worth doing under either governance model. EV subsidies remain the cheapest tonne per KRW at about 1.5 M KRW/t, which is still expensive by carbon-price standards.

Full public operation saves the guaranteed profit, duplicated management and some leakage, worth at most about 12 bn KRW a year. With wages and efficiency held level, it saves about 3.6 bn KRW a year after paying for licences and depots, and it is cheaper in about 61% of draws. The saving is thin: a rise of about 2.1% in pay per driver, or a 1.4% loss of efficiency, wipes it out. A pay rise is also money that reaches drivers, so the fiscal cost and the labour gain are the same money. Public operation helps most through control of the network: carrying out redesigns fully and retiring buses that duplicate the tram in 2030. With those steps it comes out ahead in about 94% of draws. Bus spending also keeps about 11 people employed in Daejeon per bn KRW each year, against almost none from car subsidies.

The hydrogen choice for the tram is the largest number in the comparison. It costs about 11 bn KRW a year more in energy than an electric tram and emits about 5,600 t a year more CO2. The city still has no hydrogen supply plan, and the choice was made outside the committee its own ordinance set up.

All of these measures are small next to the 873 kt a year cut the city's own plan needs in transport by 2030. The fare pass is the largest at about 4%, and its range is wide.

Weak points: how much of a redesign each governance model carries out is an assumption, and Daejeon restructured under the semi-public system in 2008. Car-trip length, the car-diversion share, bus-km, tram ridership, licence value and wage effects are bounded assumptions. The tram cost figures come from an NGO and a council forum. Health, access and congestion benefits are left out, and they would favour buses.

I started out in favour of 완전공영제. The numbers support it on network planning, the tram transition, transparency and jobs. They do not show it to be a cheaper climate policy per KRW.
