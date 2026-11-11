# Daejeon transport climate spending: a cost-effectiveness model

This model estimates how much CO2 Daejeon gets for its transport climate money. It compares zero-emission vehicle subsidies, more buses under the current semi-public bus system, full public operation of the buses, a route redesign, a 10,000 KRW monthly pass and the hydrogen tram. I built it for the KAIST course GGS50014 "Project for Carbon Neutrality Assessments" in November 2026.

The results are the expected results of an evaluation plan. Many inputs have no data behind them yet. Those are flagged ASSUMPTION in `params.csv` and given a range, and the Monte Carlo runs carry that uncertainty into every result.

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
| `figures.py`, `colors.py` | the figures, with one fixed color per item |
| `data_fiscal_series.csv` | city money and operating cost for buses, 2015 to 2025 |
| `data_context.csv` | Daejeon transport emissions and targets, transit share in seven cities |
| `results/` | all outputs as CSV; `montecarlo_summary.csv` has every metric |
| `figures/` | the figures used in the talk |

Confidence flags in `params.csv`: OFFICIAL is government data, NEWS and LITERATURE are what they say, DERIVED is my arithmetic on sourced numbers, and ASSUMPTION means no data was found.

## Scenarios

| Code | Scenario |
|---|---|
| A | battery EV purchase subsidy |
| B | fuel-cell EV purchase subsidy |
| C | more bus service on today's routes, semi-public operation |
| D | the same service under full public operation |
| E | 10,000 KRW monthly transit pass |
| R | route redesign with the same buses |
| T1 | hydrogen tram against a battery or catenary tram |
| T2 | retiring buses that duplicate the tram after 2030 |
| W | traffic delay during tram construction |

## Main results

Median and 90% interval over 10,000 draws.

<!--RESULTS-->

## What the numbers say

Adding buses to today's routes raises CO2 in every draw. An added electric bus emits about 360 g per km, and the new riders it attracts avoid only about 135 g of car CO2 per bus-km. Daejeon's buses already run fairly empty, at about 1.08 boardings per bus-km.

Redesigning routes with the same buses cuts CO2 in about 81% of draws and pays for itself through fares in about 94%. The gain is calibrated on Daejeon's own 2008 reform, when trips excluding transfers rose 3.9%. The tonnes are small, so the case for redesign is better service at no extra cost.

EV subsidies buy the cheapest tonne in this comparison, about 1.5 M KRW per tonne with national and city money combined. Many buyers would have bought an EV anyway, so the share of subsidized cars that are additional runs from 15% to 60%. Fuel-cell cars cost about 5.4 M KRW per tonne. The monthly pass costs about 2.9 M KRW per tonne and beats EV subsidies in about 16% of draws.

Full public operation on its own saves a median 2.5 bn KRW a year and is cheaper in about 61% of draws. A 2.1% rise in pay per driver or a 1.4% loss of efficiency wipes that saving out.

With fuller redesign and, after 2030, retirement of buses that duplicate the tram, public operation saves a median 14.7 bn KRW a year and comes out ahead in about 94% of draws. This assumes the semi-public system would carry out less redesign and retire fewer buses. If the assumption is wrong the figure falls to 61%, and if it is half right, to 79%.

The hydrogen tram emits about 98 g per passenger-km on grey hydrogen and about 60 g on Korea's current mix, against about 21 g for a battery or catenary tram. Compared with an electric tram it costs about 11 bn KRW a year more in energy. The city's hydrogen supply plan was scrapped in May 2025.

Closing 5 of 10 lanes on Daedeok Bridge for tram works burns about 1,090 tCO2 a year in extra idling and costs travelers about 10.2 bn KRW a year in time.

All of these are small next to the 873 kt a year Daejeon must cut from transport by 2030. Retiring tram-duplicating buses covers about 0.4% of that cut and route redesign 0.1 to 0.15%. Choosing hydrogen over an electric tram moves the city about 0.6% further away.

City money for buses rose from 38.3 bn KRW in 2015 to 102.4 bn in 2025, because operating cost rose 47% while fares and other revenue rose 14%. Bonus fraud, about 1.6 bn KRW a year, is about 1.6% of that money. Each 1 bn KRW a year of bus service keeps about 11 people employed in Daejeon.

## Data that would change the results

- The tram's hydrogen source, pathway and contract price
- The tram ridership forecast
- Route-level ridership and bus-km, including before and after the 2008 reform
- Audited accounts of the 13 bus companies
- What new bus riders did before: drive, walk or not travel
- The legal status and price of route licences

Most of this data sits with the city, the bus companies and the tram contractor.
