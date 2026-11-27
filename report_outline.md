# Report outline (8 pages + appendix)

Working title: **Formula or Lines? Apportionment Axioms and Redistricting Ensembles for India's Delimitation**

## How this outline was shaped by the CS 238 examples

| Example | Type | Main body | Appendix | Skeleton |
|---|---|---|---|---|
| Optimal Size of Congress (project 1) | theory + real data | ~8 pp, 3 figures | proofs (A) | Intro (with 1.1 Related Work), Problem Statement, theory, real-world data, extension, Discussion |
| Obvious Independence of Clones (project 2) | theory | ~11 pp | proofs (A), worked examples (B) | Intro (with 1.1 Overview roadmap), definitions, new definition, positive results, impossibility, Conclusion |
| Participatory Budgeting in Cambridge (project 3) | empirical | ~8 pp, 6 figures | tables, extra figure | Intro, Background, Data, Methods, Results and Discussion, Recommendations, Conclusion |

Conventions this outline follows:

- Theorems are stated in the body with short proof sketches. Full proofs go in Appendix A.
- Related work is a subsection of the introduction, not its own section.
- The body has about 3 figures and 2 tables. Everything else goes in the appendix.
- The report ends with discussion and policy recommendations, not only a recap.

Project 1 is the closest model: it combines theorems with real legislature data and is also about House size. References are assumed not to count toward the 8 pages, as in all three examples.

## Page budget

| Section | Pages |
|---|---|
| Abstract + 1 Introduction | 1.25 |
| 2 Setting and model | 1.0 |
| 3 The seat rules: axiomatic analysis | 2.5 |
| 4 Simulation design | 1.0 |
| 5 Results | 1.75 |
| 6 Discussion and limitations | 0.5 |
| **Total** | **8.0** |

§3.7 (reserved seats) takes its quarter page from §5.4 (demographic trends), which moves to Appendix B with one sentence left in the body.

## Novelty relative to the US setting

Both countries solve the same two problems in sequence: apportion seats among states, then draw districts within each state. Almost all apportionment theory (Balinski and Young; Lectures 16–17) and redistricting-ensemble work (the Duchin group) is built on the US. India adds a third layer: which seats are reserved, and for whom.

| | United States (House) | India (Lok Sabha) |
|---|---|---|
| Seats among states | Huntington–Hill method, House fixed at 435 | Frozen at 1971 since 1976; the formula is now contested (§3) |
| Equal population within a state | Strict (*Wesberry v. Sanders*, 1964) | Roughly equal, built from whole assembly segments |
| Contiguity, compactness | Set by state law; not a federal requirement | Practicability and geography, per the Delimitation Act |
| Minority representation | Voting Rights Act §2: districts where a minority group can elect its preferred candidate. Any candidate may run | **Reserved seats** (Art. 330): only Scheduled Caste (SC) or Scheduled Tribe (ST) candidates may stand; everyone votes |
| How many minority seats | Comes out of litigation; no fixed number | **Proportional to the group's share of the state's population** (Art. 330(2)), so it is itself an apportionment |
| Women | None | **One third of seats**, including one third of SC and ST seats (106th Amendment, 2023). Takes effect only after the next delimitation, and rotates at each later one |

Corrections to keep the framing accurate:

- **Castes:** only Scheduled Castes and Scheduled Tribes get reserved Lok Sabha seats. Other Backward Classes do not.
- **Women's quota:** it exists, but it is not yet in force. The 2023 Act ties it to the delimitation this project studies, which makes it more relevant to the project, not less.
- **US geometric rules:** the federal rule is mainly equal population. Compactness and contiguity come from state law.

**Why it is a committee problem.** After the formula fixes $`k_i`$ seats for state $`i`$, two more allocations follow:

1. **Category counts.** These are SC seats $`s_i\approx k_i\cdot \mathrm{SC}_i/p_i`$ and the matching ST seats $`t_i`$. Each is rounded within its state, so the national result is a two-dimensional (state × category) apportionment. That links to biproportional apportionment (Balinski and Demange; Pukelsheim).
2. **Constituency labels.** Some constituencies get labels (SC, ST, women), subject to quotas that overlap, because women's seats must be one third of the SC and ST seats as well. This resembles committee selection with quotas on overlapping groups, as in fair selection of citizens' assemblies.

So a seat formula moves more than state seat counts. Because SC and ST shares vary widely across states, it also changes how many reserved seats exist nationally.

---

## Abstract (~150 words)

The abstract makes four points:

1. The question: when India reapportions the Lok Sabha, which matters more for partisan power, the seat formula or the lines drawn within states?
2. The theory result: a trilemma, plus the Alabama paradox in Reddy's rule and its one-line fix.
3. The simulation: ensembles of about 2.3 million maps across 20 states.
4. The headline: formulas differ by about 2 points of NDA seat share; lines move it about 12 points either way.

## 1 Introduction (1 page)

- **Hook.** The 1976 freeze at the 1971 census, the failed April 2026 bill, and the north–south conflict. Like project 2's Oregon example, open with one concrete number: Bihar has 60 seats under a flat scale-up against a population quota of 75.8.
- **Question.** Public debate focuses on the formula, but the Delimitation Commission also redraws every constituency. The report measures both effects in the same units.
- **Contributions** (bulleted):
  1. An axiomatic analysis of six rules in the lecture framework. It includes the weight-rule lemma and a formal version of the south's complaint (Observation A7).
  2. Proof that Reddy's hybrid is neither house monotonic nor population monotonic, an instance of the paradox in real data, and a fix.
  3. A new fertility-window rule and its monotone comparative statics.
  4. The first ensemble analysis of Indian redistricting that we know of, combining ReCom (GerryChain's random map generator) with short-burst optimisation in 20 states.
  5. The headline finding: line-drawing moves seats about six times as much as the formula does.
  6. **A setting beyond the US model.** India's delimitation is a three-layer problem: seats among states, reserved-seat counts within states, and district lines. We show that the seat formula also changes the national number of SC and ST seats (§3.7).
- **1.1 Related work** (one paragraph):
  - apportionment axioms: Balinski and Young
  - degressive proportionality: Penrose; Grimmett's Cambridge Compromise
  - redistricting ensembles: DeFord, Duchin and Solomon; Cannon et al. on short bursts. Note that this work is almost entirely on US maps
  - India's 2008 delimitation: Iyer, Weir and Ostermann
  - apportionment with categories: biproportional apportionment (Balinski and Demange; Pukelsheim); committee and panel selection with group quotas

## 2 Setting and model (1 page)

- **2.1 Institutional setting** (one paragraph):
  - Article 81 and its proviso exempting states under 6 million
  - the 42nd and 84th Amendments
  - the 2026 bill and its 850-seat cap
  - how delimitation works: seats among states first, then constituency lines within each state
  - **the comparison with the US** (a compressed version of the table under "Novelty relative to the US setting", possibly as Table 0): Art. 330 reserved seats for SC and ST, the women's quota from the 2023 Act, and how reserved seats differ from Voting Rights Act districts
- **2.2 Apportionment model.** Quotas, divisor methods and Webster's method, compressed from theory.md A.1–A.5. Cite Lectures 16–17 rather than reproducing them.
- **2.3 Our extensions:**
  - the definition of a weight rule
  - region share and the definition of restoration (A.7)
  - the region used throughout: the south, defined as AP, KA, KL, TN, TG and PY

Source: `theory.md` Part A.

## 3 The seat rules: axiomatic analysis (2.25 pages)

- **3.1 Baselines and the general lemma.**
  - The freeze, the flat scale-up and the population rule (the 2026 bill).
  - Lemma A6, with a two-line proof.
  - Observation A7, framed as why the south objects: slower growth can never win a state seats.
- **3.2 Fertility window (new rule).** The definition, plus Prop B1: each region's share changes in only one direction as λ varies. Include a one-line proof, since it is a short derivative.
- **3.3 Degressive proportionality (Tharoor).**
  - Prop B3: each state's share rises then falls as α grows. Give a proof sketch.
  - Penrose's square-root law in one paragraph, including why it breaks down under party discipline.
  - α = 0.517 gives the south 21.14%, close to its best case of 21.16% at α ≈ 0.558. No α restores it.
- **3.4 Floors.** Prop B4: each region's share is a mix of its population share and its share of states. So no floor restores the south.
- **3.5 Reddy's hybrid.**
  - Prop B5, with the three-state counterexample inline. It is short, and the most memorable result in this section.
  - The real-data instance: Bihar has 44 seats at a House of 607 and 43 at 608.
  - Prop B8: rounding only the new seats fixes house monotonicity and moves at most two seats.
- **3.6 Synthesis.**
  - **Table 1:** each rule's monotonicity, its quota violations at K = 816, whether it penalises slower growth, and the south's share.
  - State the trilemma: population-based rules can't restore the south, the rules that do ignore population, and the one popular compromise breaks monotonicity.
  - Consider turning the trilemma into a single proposition (extension 3 in `summary_of_codebase.md`).
- **3.7 Reserved seats: a second apportionment** (0.25 page, new):
  - Model the within-state SC and ST counts as Webster's method applied to the category populations at size $`k_i`$. First check how the Delimitation Commission actually rounds.
  - **Computed:** national SC, ST and women's seat totals under each formula at K = 816. Hypothesis to test: the degressive rule raises ST seats, because the Northeast is mostly ST.
  - **Possible result:** reserved-seat counts inherit house monotonicity from the state allocation only when both layers are divisor methods. Check whether the nested one-third rule for women can break it.
- **Rajagopalan.** One paragraph or footnote. Her Lok Sabha rule is the population rule, and her Revenue Sabha is in Appendix B.

Source: `theory.md` Part B.

## 4 Simulation design (1 page)

- **Votes.**
  - 2024 results pooled into the alliances that shared seats in each state.
  - Each constituency's vote is spread evenly over its assembly segments.
  - In 11 states, each segment is shifted by its lean in the latest assembly election, with constituency totals kept exact.
  - Validation: the method reproduces the actual 2024 result in every simulated state.
- **Neutral maps.** ReCom on the graph of assembly segments, with a size tolerance of about 20%. Four chains, 500 burn-in steps and 2,000 recorded maps each, for every state and seat count. That is 130 combinations and about 2.3 million maps.
- **Drawn maps.** Short bursts (500 bursts of 10 steps) towards the most NDA seats and the fewest. "Tilted" is the 5th or 95th percentile of the neutral ensemble.
- **Combining the two.** Seat formula → seats per state → interpolated seat shares → national totals.
- **Metrics.** Seat counts, efficiency gap (adapted for many parties), mean–median difference and ordered-margin plots.

Source: `README.md` Method section, `analysis/simlib.py`, `analysis/run_state.py`.

## 5 Results (2 pages)

- **5.1 Formula vs lines** (the central result):
  - **Table 2:** the headline grid of 6 formulas × 4 map types.
  - **Figure 1:** a dot plot of NDA seats, with a row per formula and a dot per map type. The majority and two-thirds lines are drawn on it. This is the key figure: the dots spread far wider within a row than across rows.
  - Interpretation: formulas move about 2 points and lines about 12. The fair comparison for the 2024 House is the "freeze at 543" row (301 seats with neutral lines), not the actual 293.
- **5.2 Was the 2008 delimitation an outlier?**
  - For each state, find where the actual map falls within the neutral ensemble.
  - **Figure 2:** ensemble histograms for 3–4 large states with a marker for the actual map.
  - Compare with Iyer, Weir and Ostermann.
- **5.3 How robust are drawn maps?**
  - **Figure 3:** the seats–votes curve. The optimised map falls from 563 seats to 513 after a one-point adverse swing, and matches a neutral map after about four points.
- **5.4 Demographic trends.** One sentence here; the details are in Appendix B: the south's share under the 2026 and 2036 projections, and the GDP convergence control for Reddy's rule.
- **5.5 (optional) Power, not seats.** Banzhaf indices for party blocs at the majority and two-thirds thresholds.

## 6 Discussion and limitations (0.5 page)

- **Policy point.** The debate fights over the formula, but safeguards on how the Delimitation Commission draws lines matter more:
  - ensemble-based audits
  - published neutral baselines
- **Design point.** If a compromise rule is adopted, use the incremental hybrid (R′) or the fertility window, which keep monotonicity.
- **Limitations:**
  - only one election is used
  - maps are built from whole assembly segments
  - 9 states have no segment-level lean
  - 39 seats are not redrawn
  - reserved-seat counts are modelled (§3.7), but the simulated maps do not choose which constituencies are reserved
  - "optimised" maps are a heuristic bound, not a forecast
- **Future work.**
  - Add the reservation layer to the simulation: whoever draws the lines also decides which areas become SC or ST seats, and that is a lever for gerrymandering that has no US equivalent.
  - Calibrate "tilted" against real gerrymanders.
  - Add a second election.

## References

These are already collected in `theory.md` and `README.md`.

---

## Appendices (no page limit)

- **A. Proofs.** Full proofs of Lemma A6, Observation A7 and Props B1, B3, B4, B5 and B8, plus any new trilemma proposition.
- **B. More results on the rules:**
  - sweeps over α, λ and the floor f
  - quota violations by state
  - R and R′ compared across K from 543 to 850
  - Rajagopalan's Revenue Sabha
  - southern share under the 2011, 2026 and 2036 counts
- **C. Data and preprocessing:**
  - sources and licences
  - matching constituencies to assembly segments
  - the Gujarat urban blocks
  - the segment-lean method and its shrinkage rule
  - validation for each state
- **D. Simulation details:**
  - chain parameters and the size tolerance rule (`eps_for`)
  - the short-burst scoring functions
  - convergence diagnostics across the 4 chains
  - seeds and runtime
- **E. Results for each state.** For all 20 states: ensemble ranges, the actual map's percentile, efficiency gap, mean–median difference and ordered-margin plots.
- **F. Interactive page.** Screenshots from `docs/screenshots/` and the link.

---

## Work needed before the report can be written

These come from `summary_of_codebase.md`.

| Needed for | Task | Effort |
|---|---|---|
| §3, §5 | Choose one census baseline (2011 or the 2026 projection), or label both throughout | decision |
| §3.2, §3.5 | Settle the open TODOs: λ and the 2021 end year; the reading of "pro rata" | decision |
| §3, App. B | Add the floor rule, R′, the α sweep and quota-violation counts to `apportion.py` so every number in §3 can be reproduced | small |
| §5.1 | Write the theory–simulation link (the TODO at `theory.md:341`) | writing |
| §5.2 | Report `actual_pct`, which `summary.py` already prints | small |
| §5.5 | Compute Banzhaf indices for party blocs, or cut §5.5 | medium |
| App. D | Fix seeding (`PYTHONHASHSEED` or explicit seeds) and add convergence diagnostics | small–medium |
| §2.1, §3.7 | Check the legal facts against primary sources: Art. 330(2); the Delimitation Act's rules for choosing reserved constituencies and for rounding; the 2023 Act's start date and rotation; and whether the 2026 bill changed any of them | small |
| §3.7 | Add 2011 census SC and ST populations by state to `apportion.py` (from the census Primary Census Abstract), with the source in a comment | small |
| §6 (future) | Get SC and ST shares for each assembly segment, so ReCom can take reservation constraints | medium–large |
