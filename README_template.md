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

<!--RESULTS-->

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

<!--PARAMS-->

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
