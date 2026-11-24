# Daejeon's transport climate policies: a cost-effectiveness model

This model estimates the emissions reductions and costs of Daejeon's transport climate policies. The Scenarios table below lists what it compares. I built it for the KAIST course GGS50014 "Project for Carbon Neutrality Assessments" in November 2026.

These are modeled estimates based on an evaluation plan. Every input in `params.csv` has a low, central and high value, and inputs without sufficient evidence are marked ASSUMPTION. The simulations sample these input ranges.

## Run it

Python 3.10 or later.

```
pip install -r requirements.txt
python run.py          # about 10 s: central case, 10,000 Monte Carlo draws (seed 2026), figures
python make_readme.py  # refreshes the results table in this README
```

The figures use the Inter font if it is installed and DejaVu Sans if it is not.

## Files

| File | Contents |
|---|---|
| `params.csv` | every input with low, central and high values, unit, source and a confidence flag |
| `model.py` | the equations, one function per scenario |
| `run.py` | central run, Monte Carlo, tornado and break-even analysis |
| `figures.py`, `colors.py` | figure generation and consistent scenario colors |
| `data_fiscal_series.csv` | city bus funding and operating costs, 2015 to 2025 |
| `data_context.csv` | Daejeon transport emissions and targets, transit share in seven cities |
| `results/` | all outputs as CSV; `montecarlo_summary.csv` has every metric |
| `figures/` | the figures used in the talk |

Confidence flags in `params.csv`:

| Flag | Meaning |
|---|---|
| OFFICIAL | city or national government data |
| NEWS | news reports |
| LITERATURE | published research |
| DERIVED | calculated from sourced inputs |
| ASSUMPTION | no data found; the value is a bounded range explained in the source column |

## Scenarios

| Code | Scenario | In the class presentation |
|---|---|---|
| A | battery electric vehicle purchase subsidy | no |
| B | fuel-cell electric vehicle purchase subsidy | no |
| C | more bus service on today's routes, semi-public operation | yes, as a comparison point |
| D | existing bus service under full public operation | yes |
| E | 10,000 KRW monthly transit pass | no |
| R | route redesign with the same buses | yes |
| T1 | hydrogen tram compared with a battery or catenary tram | yes |
| T2 | removing buses that overlap the tram after 2030 | yes |
| W | traffic delay during tram construction | yes |

A, B and E are additional model scenarios. The class presentation does not cover them, but their results are reported here and in `results/`.

## How to read the numbers

- Central case: one run with every input at its central value.
- Monte Carlo median: the median of 10,000 runs. Each run draws every input independently from a triangular distribution with the low and high values as bounds and the central value as the mode. Inputs with no range, such as the number of buses, stay fixed. Shares such as "cheaper in 61% of runs" are shares of model runs, not observed outcomes.
- Break-even threshold: the value of one input at which a central-case result reaches zero, with every other input at its central value.
- Each scenario is a separate comparison. Their emissions changes are not additive and should not be read as a combined policy outcome. The public operation package in D is the only combination the model builds.

## Main results

Median and 90% interval over 10,000 runs. Cost per ton (M KRW per tCO2) is reported only for scenarios that reduce emissions; lower is better. Tons per bn KRW are reported for scenarios that can raise emissions; higher is better, and a negative value means emissions rise.

| Result | Median | 90% interval |
|---|---|---|
| A. EV subsidy, M KRW per tCO2 avoided (national and city funding) | 1.45 | 0.79 to 2.92 |
| B. Fuel-cell car subsidy, M KRW per tCO2 avoided (national and city funding) | 5.36 | 3.04 to 11.46 |
| C. More buses, tCO2 avoided per bn KRW a year (negative: emissions rise) | -470 | -674 to -309 |
| E. Monthly pass, M KRW per tCO2 avoided | 2.93 | 1.26 to 9.16 |
| R. Redesign, semi-public, tCO2 avoided a year | 694 | -635 to 2,451 |
| R. Redesign, semi-public, annual city savings, bn KRW | 3.5 | -0.1 to 8.4 |
| R. Redesign, public operator, tCO2 avoided a year | 1,288 | -221 to 3,583 |
| D. Public operation alone (ownership change only), annual savings, bn KRW | 2.5 | -11.6 to 16.6 |
| D. Annual savings from the public operation package before tram opening, bn KRW | 5.1 | -9.3 to 19.6 |
| D. Annual package savings after removing overlapping buses, bn KRW | 14.7 | -0.4 to 30.7 |
| T1. Hydrogen tram on gray hydrogen, gCO2e per passenger-km | 98 | 67 to 152 |
| T1. Hydrogen tram on Korea's transport hydrogen mix, gCO2e per passenger-km | 60 | 38 to 101 |
| T1. Battery or catenary tram, gCO2e per passenger-km | 21 | 13 to 36 |
| T1. Extra energy cost of hydrogen over an electric tram, bn KRW a year | 11.2 | 10.2 to 12.3 |
| W. Additional annual CO2 from construction congestion, t | 1,087 | 500 to 2,207 |
| W. Estimated value of travel time lost, bn KRW a year (social cost) | 10.2 | 4.8 to 20.4 |

| Share of runs in which | Percentage |
|---|---|
| Public operation alone is cheaper than semi-public operation | 61% |
| Redesign under semi-public operation cuts CO2 | 81% |
| Additional fares cover redesign costs | 94% |
| Package is cheaper than semi-public operation, before tram opening | 71% |
| Package is cheaper than semi-public operation, after removing overlapping buses | 94% |
| Monthly pass avoids more CO2 per KRW than the EV subsidy | 16% |

## What the numbers say

Adding buses (C). In the model, adding buses to existing routes increases CO2 emissions in every run. An added electric bus emits about 360 g of CO2 per km. Each added bus-km attracts about 0.54 new boardings, and reduced car travel avoids only about 135 g of car CO2 per bus-km, so it offsets only part of the additional bus emissions. Daejeon's buses carry about 1.08 boardings per bus-km (2025 boardings over central bus-km).

Route redesign (R). Redesign under semi-public operation cuts CO2 in about 81% of runs, and additional fares cover its costs in about 94%. The ridership assumptions draw on Daejeon's 2008 route redesign, after which trips excluding transfers rose 3.9% in three weeks. "The same buses" allows up to 2% added buses (central value 0); Daejeon added about 2% in 2008 to relieve overloads. The share of a planned redesign that is actually carried out (about 60% under semi-public operation, about 90% under a public operator) is an assumption. The modeled emissions reductions are small. The model suggests that redesign could improve service while reducing city costs.

Vehicle subsidies and the monthly pass (A, B, E). EV subsidies have the lowest estimated cost per ton of CO2 avoided in this comparison, about 1.5 M KRW per ton with national and city funding combined. The model accounts for buyers who would have purchased an EV without the subsidy. The additionality rate, the share of subsidized purchases attributable to the subsidy, runs from 15% to 60%. Fuel-cell cars cost about 5.4 M KRW per ton. The monthly pass costs about 2.9 M KRW per ton and avoids more CO2 per KRW than the EV subsidy in about 16% of runs.

Full public operation (D). The results for public operation differ by what is counted:

- Ownership change only, central case: the cost per bus-day falls from about 687,000 to 677,000 KRW, an annual saving of about 3.6 bn KRW.
- Ownership change only, Monte Carlo: median annual savings of 2.5 bn KRW (90% interval -11.6 to +16.6). Public operation is cheaper in 61% of runs.
- Break-even thresholds (central case): the saving disappears if pay per driver rises by more than about 2.1%, if a public operator is more than about 1.4% less efficient, or if route licences cost more than about 157 M KRW per bus (central value 100 M).
- Package: the ownership change plus more extensive route redesign and, after the tram opens, removing buses that overlap it. Median annual savings are 14.7 bn KRW, and the package is cheaper than semi-public operation in 94% of runs. Before the tram opens, the median is 5.1 bn KRW and the share is 71%.
- The package result assumes that semi-public operation carries out less redesign and removes fewer overlapping buses. If that assumed redesign advantage disappears, the share of runs in which the package is cheaper falls to 61%. If the advantage is halved, it falls to 79%.

Hydrogen tram (T1). The hydrogen tram emits about 98 gCO2e per passenger-km on gray hydrogen (made from natural gas) and about 60 g on Korea's current mix of transport hydrogen. A battery or catenary tram emits about 21 g. Compared with an electric tram, hydrogen costs about 11.2 bn KRW a year more in energy and emits about 5,600 t a year more CO2.

The tram's hydrogen supply has gone through two plans:

| Date | Event |
|---|---|
| 2023-10 | Hyundai Rotem offers to invest 90 bn KRW and supply hydrogen at 4,344 KRW/kg for 30 years |
| 2025-02 | Separately, the city plans its own production from Geumgo-dong landfill biogas, whose output drops in cold weather |
| 2025-05 | The Hyundai Rotem offer is dropped; the investment pledge was never signed |
| 2026-11 | The fallback for the city's plan is hydrogen from city gas. A news report says the criteria for a production site include proximity to city-gas pipes, which points to gray hydrogen |
| 2026-11-16 | At the council audit the city puts the hydrogen price at about 10,400 KRW/kg, which raises the 30-year fuel cost from about 147 bn to 355 bn KRW |

Tram construction traffic (W). Tram construction closed 5 of 10 lanes on Daedeok Bridge on 2026-10-19, and evening car speeds there fell by 37% to 42%. The construction model extrapolates the observed slowdowns at Daedeok Bridge to 1 to 4 comparable bottlenecks (central value 2). At the Monte Carlo median, extra idling produces about 1,090 tCO2 a year, and the estimated value of travel time lost is about 10.2 bn KRW a year. The time cost is a social cost borne by drivers and bus riders, not a cost to the city budget. The value of time (15,000 KRW per hour), off-peak slowdown and bus counts are assumptions.

Scale (M). Daejeon's plan cuts annual transport emissions from 2,701 kt (2018) to 1,828 kt by 2030, a reduction of about 873 kt a year. Removing buses that overlap the tram covers about 0.4% of that reduction and route redesign 0.1% to 0.15%. Choosing hydrogen over an electric tram adds emissions equal to about 0.6% of the required reduction.

City bus funding. City funding for buses rose from 38.3 bn KRW in 2015 to 102.4 bn in 2025, because annual operating costs rose 47% while fare and other revenue rose about 14%. A 2025 union complaint alleged improper claims involving 8.1 bn KRW in service bonuses (Kim Yun-gi 2026, p. 43). Each 1 bn KRW a year of bus service keeps about 11 people employed in Daejeon.

## Data that would change the results

| Data to request | Assumption it tests |
|---|---|
| Hydrogen source, production method, and contract price for the tram | tram operating CO2 and energy cost |
| Tram ridership forecast and service plan | emissions per passenger-km |
| Route-level ridership and bus-km, including before and after the 2008 reform | how much redesign semi-public operation carries out |
| Audited accounts of the 13 bus companies | public operation savings |
| Traffic volumes and peak speeds by tram work zone | construction delay cost |
| Previous travel modes and travel behavior of new bus riders | share of new riders switching from cars |
| Legal status and price of route licences | licence buyout cost in D |

The city, bus companies, and tram contractor hold most of these records.
