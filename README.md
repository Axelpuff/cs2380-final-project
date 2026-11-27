# Delimitation Stress Test

## Start here: reading order

The docs in `docs/` are numbered in the order they were written. Each one answers the question the one before it raises, so read them in that order.

1. [01_project_origin.md](docs/01_project_origin.md): what was asked, what was built, and which seat formulas had to be filled in. **Leads to** the six rules to analyse.
2. [02_theory_state_apportionment.md](docs/02_theory_state_apportionment.md): Module 1, lever 1. Covers the apportionment axioms (Lectures 15–17), each rule's properties with proofs, and the trilemma. **Leads to** the question of whether each rule gives every state its lower quota.
3. [03_committee_bridge.md](docs/03_committee_bridge.md): apportionment as a party-list committee election (Lecture 12): Thiele ↔ divisor, and EJR = lower quota. **Leads to** the vocabulary for the reservation layer.
4. [04_reserved_seats.md](docs/04_reserved_seats.md): Module 2. Covers the law of SC, ST and women's reservations, rounding model M, theory directives T1–T7, and the House as a constrained committee. **Leads to** the paper.
5. [05_report_outline.md](docs/05_report_outline.md): the 8-page report, section by section, with the claims ledger and the work still needed. **This is the map of the final paper.**
6. [06_status_and_open_work.md](docs/06_status_and_open_work.md): what is done, what is missing, and which numbers have no code behind them yet.

The simulation (Module 1, lever 2: line-drawing) is described below, under Method.

How much partisan power moves when the Lok Sabha is reapportioned, and how much moves when the lines inside each state are redrawn. Built as a starting point for a CS 2380 (Optimized Democracy) final project.

Seven seat formulas are combined with five ways of drawing constituencies. The 2024 Lok Sabha votes are recounted in each simulated map.

Run date: 25 November 2026. Published page (private until shared): https://claude.ai/artifact/WzDrwHdZBwf81XFgEpqhKJ

## Headline numbers

NDA seats in an 816-seat House on the 2011 census. Two-thirds is 544 and a majority is 409.

| Formula | Optimised against NDA | Neutral | Tilted toward NDA | Optimised for NDA |
|---|---|---|---|---|
| Freeze at 543 (two-thirds is 362) | 226 | 301 | 328 | 379 |
| Flat scale-up | 356 | 454 | 483 | 554 |
| Bill as drafted (by population) | 367 | 467 | 497 | 565 |
| Reddy 50/50 | 360 | 457 | 485 | 556 |
| Tharoor degressive | 375 | 470 | 498 | 560 |
| Fertility-window discount (weight 0.5) | 364 | 463 | 492 | 562 |

- The formulas differ by about two points with neutral lines. The lines move the result about twelve points in either direction.
- The actual 2024 House was NDA 293 of 543. A neutral redraw of those 543 seats gives 301, so compare formulas with the "Freeze at 543" row, not with 293.
- A one-point adverse shift in margins takes the optimised map under the bill from 563 to 513 seats. At four points it equals a neutral map.

`analysis/summary.py` prints these tables. The swing figures come from the seats-votes chart on the page.

## Layout

```
page/                 the interactive page and the three data files it fetches
analysis/             scripts, run from inside this folder
analysis/out/         raw simulation output, one JSON per state
analysis/run_log_*.txt  console logs of the simulation run
data/                 source data goes here (not committed; see data/README.md)
docs/                 project write-ups, numbered in reading order (see "Start here")
docs/screenshots/     the page in light, dark and phone layouts
scratch/              the first-pass apportionment script behind the earlier pitch
```

## View the page

```
python3 -m http.server --directory page 8000
```

Then open http://localhost:8000. It needs to be served, not opened as a file, because it fetches `sim.json` and the two map files. `index.html` is a fragment without `<html>` or `<body>` tags (the publishing tool adds them); browsers render it as is.

## Reproduce

```
pip install -r requirements.txt
# fetch the data as described in data/README.md, then:
cd analysis
python3 build_graph.py        # cleans the constituency map, matches it to 2024 results, builds adjacency graphs -> stage1.pkl
python3 apportion.py          # seat formulas; writes krange.json (range of seat counts per state)
NCH=4 LEN=2000 NB=500 python3 run_state.py "Uttar Pradesh" "Maharashtra" ...   # ensembles and short bursts -> out/<code>.json
python3 build_topo.py         # simplified constituency shapes for the page
python3 build_states.py       # national map, and fixed.json for units that are not redrawn
python3 pack.py               # writes ../page/sim.json and copies the map files
python3 summary.py            # tables and cross-checks
```

State names for `run_state.py` are the keys of `CODE` in that file. The full run took about 40 minutes on two cores, split into two processes.

The run is not seeded reproducibly. `run_state.py` seeds from Python's string hash, which changes between processes, so a rerun gives slightly different numbers. Set `PYTHONHASHSEED=0` before a rerun to make later runs repeatable.

## Method

- **Seats.** Each formula is rounded with the Webster (Sainte-Laguë) method. States under six million people keep at least their current seats. Code in `apportion.py`, mirrored in JavaScript in the page.
- **Votes.** 2024 results for all 543 seats, pooled into the alliances that shared seats in each state. Each constituency's vote is spread evenly over its assembly segments. In eleven states the latest assembly election supplies each segment's NDA lean relative to its constituency, with constituency totals kept exact.
- **Neutral maps.** GerryChain ReCom on the graph of assembly segments: four chains, 500 burn-in and 2,000 recorded plans each, for every seat count tested (130 state and seat-count combinations, about 2.3 million plans scored).
- **Drawn maps.** Short-burst optimisation (500 bursts of 10 steps) for the most NDA seats, and separately the fewest. "Tilted" is the 5th or 95th percentile of the neutral ensemble.
- **Scoring.** Ordered-margin plots, efficiency gap and mean-median difference.
- **Between seat counts.** The page interpolates seat shares linearly between the counts that were simulated.

## Formula definitions used

| Formula | Rule in this code | Status |
|---|---|---|
| Bill as drafted | Seats proportional to population | April 2026 bill text |
| Flat scale-up | Seats proportional to current seats | Verbal assurance |
| Reddy 50/50 | Current seats kept; half of new seats pro rata to current seats, half by state GDP share (2022-23) | My reading of press reports |
| Tharoor degressive | Seats proportional to population to the power 0.517 | Fitted to his two examples (30m people at 1m per MP, 200m at 2.5m) |
| Rajagopalan | Lok Sabha by population; Revenue Sabha weights use state GDP as a stand-in for own revenue | Party make-up of the upper house is not modelled |
| Fertility-window discount | 1971 population, plus growth from 1971 to 2021 at weight λ, plus later growth in full | New here |

## Limits

- One election. Alliances have shifted since 2024.
- Building blocks are whole assembly segments, with constituencies allowed to differ by about 20% in size (more where a constituency is only three segments). A real commission can cut finer.
- Nine states have no segment-level lean in the data (Tamil Nadu, Madhya Pradesh, Rajasthan, Gujarat, Odisha, Andhra Pradesh, Telangana, Chhattisgarh, Himachal Pradesh). Where one side swept such a state, no simulated map changes the result.
- Assam, Jammu and Kashmir and sixteen small states and territories (39 seats) are not redrawn and keep their 2024 split.
- Reserved seats (Scheduled Castes, Scheduled Tribes, women) are ignored.
- Gujarat's map has twenty urban segments without labels. They are modelled as blocks of the right weight inside their constituencies.
- "Optimised" is the best plan a heuristic found in every state at once. It is a bound on what the method can reach, not a forecast.
- The 1971 populations for the five territories without legislatures are approximate; they sit on the one-seat floor and do not affect results.

## Sources

- Election Commission of India 2024 results: https://github.com/thecont1/india-votes-data
- Constituency boundaries, DataMeet: https://github.com/datameet/maps
- Population projections 2011-2036: https://files.givewell.org//files/DWDA%202009/Interventions/KMC/India-gov_MoH-Population-Projections_2011-2036.pdf
- PRS on the Delimitation Bill, 2026: https://prsindia.org/billtrack/the-delimitation-bill-2026
- Carnegie, Delimitation After Defeat: https://carnegieendowment.org/research/2026/05/india-parliament-lok-sabha-representation-reapportionment-vote-women-elections
- Rajagopalan, Demography, Delimitation, and Democracy: https://srajagopalan.substack.com/p/demography-delimitation-and-democracy
- Reddy's hybrid model: https://www.deccanchronicle.com/southern-states/telangana/revanth-reddy-seeks-delimitation-based-on-2026-census-1950191
- Tharoor on degressive proportionality: https://telanganatoday.com/shashi-tharoor-suggests-degressive-proportionality-for-lok-sabha-delimitation
- Iyer, Weir and Ostermann on the 2008 delimitation: https://sites.nd.edu/lakshmi-iyer/files/2026/03/IWO_Political-Influence_Feb2026_Full.pdf
- State GDP: https://en.wikipedia.org/wiki/List_of_Indian_states_and_union_territories_by_GDP
- DeFord, Duchin and Solomon, Recombination: https://arxiv.org/abs/1911.05725
- Cannon et al., Optimization by Short Bursts: https://arxiv.org/abs/2011.02288
