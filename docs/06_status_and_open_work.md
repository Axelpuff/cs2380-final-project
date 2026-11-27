# Summary of the codebase

*Read after: [05 report outline](05_report_outline.md). Last in the chain.*

Written 27 November 2026. The numbers checked below were run against `analysis/apportion.py` on that date.

The project asks how much partisan power shifts when India reapportions the Lok Sabha, and how that compares with redrawing the lines inside each state. It has three parts:

- **Theory:** `02_theory_state_apportionment.md` analyses each proposed seat formula using the axioms from Lectures 15–17.
- **Application:** a GerryChain simulation re-scores the 2024 vote under every combination of seat formula and kind of map.
- **Page:** an interactive page at `page/index.html`.

The headline finding: with neutral maps, the seat formulas differ by about 2 points of NDA seat share, while the choice of map moves it about 12 points either way.

## Done: theory

**Part A** restates the course framework: the apportionment model, Hamilton's method, divisor methods, the monotonicity and quota properties, Theorems A1–A5 and Banzhaf power. It then adds three results of its own:

- **Weight rules and Lemma A6:** any divisor method run on weights that rise with population and don't depend on House size is monotone in both House size and population.
- **Region share and restoration:** a formal way to ask whether a group of states keeps its current share of seats.
- **Observation A7:** under any population-monotone rule, a state can never gain seats by growing more slowly. This is the formal version of the southern states' complaint.

**Part B** analyses each rule, with proofs:

| Rule | Main result |
|---|---|
| Fertility window | Prop B1: each region's share moves in only one direction as the weight λ changes |
| Tharoor (degressive) | Prop B3: each state's share rises then falls as the exponent α grows; derives α = ½ from Penrose's square-root law, then explains why bloc voting by state doesn't hold in India |
| Floor plus proportional | Prop B4: no floor restores the south, and every floor lowers its share |
| Reddy hybrid | Prop B5 and Cor B6: breaks both monotonicity properties, with a 3-state counterexample. Prop B8: rounding only the new seats fixes house monotonicity |

The conclusion is a trilemma. Population-based rules can't restore the south. The rules that do restore it ignore population. Reddy's hybrid, as he proposed it, has the Alabama paradox (a state loses a seat when the House grows).

**Numbers checked against `analysis/apportion.py`:**

- The Bihar paradox reproduces exactly: 44 seats at a House of 607, then 43 at 608.
- The south's unrounded quota share under the population rule is 19.45%, as stated.
- Reddy's rule gives the south about 25%, as stated.

## Done: application

- **Data pipeline:** the 2024 constituency results, matched to assembly-segment maps. In 11 states, each segment is shifted by its lean in the latest state election, with constituency totals kept exact.
- **Seat formulas:** all six are coded in `analysis/apportion.py`, using Webster's method with the small-state floors.
- **Neutral maps:** a ReCom ensemble (GerryChain's random map generator) in 20 states, with 4 chains each. That covers 130 combinations of state and seat count and about 2.3 million maps. Both run logs are clean: 65 + 65 runs, and the only warnings are harmless unclosed-file notices.
- **Drawn maps:** short-burst optimisation finds maps that maximise and minimise NDA seats. "Tilted" maps take the 5th or 95th percentile of the neutral ensemble.
- **Scoring:** efficiency gap (adapted for many parties by comparing the NDA with its strongest rival), mean–median difference, and ordered-margin plots.
- **Outputs:** the headline table, a swing-sensitivity result (the optimised map's advantage is gone after an adverse shift of about 4 points), and the published page with maps and a seats–votes chart.

## Missing: next steps, in priority order

1. **Several theory numbers have no code behind them.** The floor rule (B.5), the fixed hybrid R′, the α ≈ 0.558 peak and the counts of states outside quota are not in `analysis/apportion.py`. Add them so every "Computed" figure can be reproduced.
2. **The two halves use different census years.** `02_theory_state_apportionment.md` uses 2026 projections, but the simulation headline uses the 2011 census. Pick one baseline, or label both clearly. The rounded southern seat share under the population rule is 20.6% with 2011 figures and 19.4% with 2026 projections.
3. **The four open TODOs in `02_theory_state_apportionment.md`:**
   - the end year of the fertility window and the default λ (`02_theory_state_apportionment.md`, TODO in B.3)
   - whether to compute Banzhaf power (TODO in B.4)
   - which reading of "pro rata" to use for Reddy's rule (TODO in B.6)
   - the link from theory to simulation (TODO after the Summary table), which is the project's central argument and hasn't been written yet
4. **Rajagopalan's proposal isn't in `02_theory_state_apportionment.md` at all.** It also has no row in the README's headline table.
5. **Reproducibility.** `analysis/run_state.py:23` seeds from `hash()`, which changes between runs. `CUR` and `CODE` are also duplicated across four scripts rather than imported from one place.
6. **Gaps listed in `01_project_origin.md`:**
   - "tilted" is a stand-in, not calibrated against real gerrymandering trends
   - 9 states have no segment-level lean
   - Assam, Jammu and Kashmir and the small states and territories (39 seats in all) are not redrawn
   - reserved seats are ignored
   - only one election is used
7. **No paper.** There's a README, a summary and the theory section, but no single write-up with motivation, results and limits.

## Extensions that would raise the project

The first two are the recommended ones. Both are cheap, build on what exists, and fit the course's theme.

1. **Treat the 2008 map as an outlier test.** `analysis/run_state.py` already computes where the actual map falls within the neutral ensemble (`actual_pct`), and `analysis/summary.py` prints it, but nothing reports the result. A result like "the 2008 delimitation sits at the Xth percentile in states A, B and C" would be a real empirical contribution, and it could be checked against Iyer, Weir and Ostermann's paper on the 2008 delimitation.
2. **Measure power, not seats.** Compute Banzhaf indices for the party blocs at the majority and two-thirds thresholds. The two-thirds line matters because constitutional amendments need it. This closes the TODO in `02_theory_state_apportionment.md` and replaces seat counts with the power measure from Lecture 15.
3. **Turn rule design into an optimisation problem.** Find the allocation closest to proportional, subject to no state losing seats and the south keeping its current share, and the smallest House where that's possible. `scratch/first_pass_apportionment.py` already searches for the smallest House with no losses. Proving when the problem has no solution would extend the trilemma from three examples to a theorem.
4. **Formally split the effect of formula versus lines.** For example, a variance or Shapley decomposition of NDA seats across the 6 × 5 grid. This would turn "2 points versus 12" from an observation into a measured result.
5. **Robustness checks:**
   - a second election (2019), or a uniform swing
   - convergence diagnostics across the 4 chains
   - reserved-seat constraints in ReCom
