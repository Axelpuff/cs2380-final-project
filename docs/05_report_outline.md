# Report outline (8 pages + appendix)

*Read after: [04 reserved seats](04_reserved_seats.md). Leads to: [06 status and open work](06_status_and_open_work.md).*

Rewritten 27 November 2026. Structure: background → Module 1 (state apportionment, two levers) → Module 2 (filling the quotas) → conclusion. The previous outline is in git history.

Working title: **Seats, Lines, and Quotas: Auditing India's Delimitation as a Three-Layer Apportionment**

**Thesis (one sentence the whole paper defends).** Every layer of India's delimitation is an apportionment, and one axiom can audit each of them: lower quota, which on party-list profiles is exactly EJR. At layer 1 the debated seat formulas move party power far less than line-drawing does. At layers 2–3 the rules for SC, ST and women's seats are unwritten. Their natural reading meets lower quota for SC and ST, but it has paradoxes of its own, and it falls short of proportionality for women by design.

---

## Claims ledger

Each claim's honest status, so the paper never over-claims. *Proved* = proof in `02`/`03`/`04`. *Computed* = a number from committed code. *Scratch* = computed ad hoc and not yet reproducible. *To do* = not yet computed.

| # | Claim | Status | Evidence | § |
|---|---|---|---|---|
| 1 | Divisor methods ⇒ house and population monotone; Balinski–Young impossibility | known (lectures) | cited | 2.3 |
| 2 | Thiele ↔ divisor on party lists; EJR = lower quota = core | known (BLS 2018; Dong–Peters 2026) | proof sketch | 2.3 |
| 3 | Lemma A6 (weight rules are monotone); Obs. A7 (slower growth never wins seats) | new, easy | proved | 3.1 |
| 4 | Fertility-window rule; shares monotone in λ (B1) | new | proved + computed | 3.1 |
| 5 | Tharoor's shares single-peaked in α (B3); no α restores the south | new application | proved + computed | 3.1 |
| 6 | Reddy's hybrid fails both monotonicities (B5, B6); Bihar 44→43 at 607→608; R′ fixes it (B8) | new | proved + computed | 3.1 |
| 7 | The trilemma | new synthesis | Table 2 | 3.1 |
| 8 | The bill + 6M floor violates lower quota (EJR) for UP and Maharashtra | new application | scratch | 3.1 |
| 9 | First ensemble study of Indian delimitation; formula moves ~2 points, lines ~12 | new empirical | computed | 3.3 |
| 10 | Under model M, the SC/ST/General split meets quota, hence EJR | new application | scratch (exhaustive k ≤ 99) | 4.2 |
| 11 | General seats can fall as k rises (T1); frequency ≈ στ | new | scratch examples, to do with real shares | 4.3 |
| 12 | Layer-1 paradoxes propagate to SC seats (T2) | new, easy | to do (rerun B5 with shares) | 4.3 |
| 13 | SC population up, SC seats down (T3) | new | scratch toy example | 4.3 |
| 14 | Reserved totals across six formulas + women's layer | new beyond the population row (Carnegie 2019) | to do | 4.4 |
| 15 | Under party approval, reservation constraints are free for EJR | new, easy | to prove (one line) | 4.5 |
| 16 | Under crossing approval, constrained PAV can violate EJR | open | to do (brute force) | 4.5 |

---

## Page budget

| Section | Pages |
|---|---|
| Abstract | 0.25 |
| §1 Introduction | 1.0 |
| §2 Background and framework | 1.0 |
| §3 Module 1: state apportionment, two levers | 3.0 |
| §4 Module 2: filling the quotas within states | 2.25 |
| §5 Conclusion: novelties and applications | 0.5 |
| **Total** | **8.0** |

Body: 5 figures, 3–4 tables. Proofs are sketched in the body and given in full in Appendix A. References don't count toward the 8 pages. These are the conventions of the CS 238 examples; Project 1, "Optimal Size of Congress", is the closest model.

## Figures and tables (body)

| | Content | § | Source |
|---|---|---|---|
| Fig. 1 | **Pipeline.** H → k_i (formula, lever 1) → s_i, t_i (SC/ST, Art. 330) → women's seats (Art. 330A) → constituency lines (lever 2) and labels (Delimitation Act s.9). Each arrow is annotated with its legal source and with the section that analyses it. | 2.1 | new diagram, from `04` §1.1 |
| Table 1 | US House vs Lok Sabha, layer by layer | 2.2 | previous outline (git history) |
| Table 2 | Rules × {house mono, pop mono, states outside quota, **states below lower quota (EJR)**, penalises slower growth, south share}, with floor and R′ as indented variants | 3.1 | `02` Summary + `03` §3 table; needs code (work row 2) |
| Fig. 2 | South's quota share against each rule's parameter, in three panels (λ ∈ [0,1], α ∈ [0,1], f ∈ [0,15]), with a horizontal line at the current 23.94%. No curve crosses it. | 3.1 | needs code (work row 2) |
| Table 3 | Headline grid: 6 formulas × 4 map types, NDA seats | 3.3 | `analysis/summary.py` |
| Fig. 3 | (a) Dot plot of NDA seats, one row per formula and one dot per map type, with majority (409) and two-thirds (544) lines: the spread within a row dwarfs the spread across rows. (b) Seats–votes swing for the bill: optimised 563 → 513 at a one-point swing, neutral by about four points. | 3.3 | `summary.py`, `page/sim.json` |
| Fig. 4 | **Residual-paradox map.** Heatmap over (σ, τ) of the fraction of steps k → k+1 (k ≤ 100) where model M's General count falls, with each state plotted as a point at its 2011 (σ_i, τ_i) and labelled with its seat range across the six formulas. | 4.3 | needs code (work row 3), exact and cheap |
| Fig. 5 | Reserved-seat totals by formula: grouped bars for SC, ST, women, SC-women and ST-women, each next to the single-layer benchmark round(H·share). Annotated with the rounding and malapportionment decomposition. | 4.4 | needs code (work row 4) |
| (Table 4) | Worked T1/T3 examples with real shares. Optional: inline in the text if space is short. | 4.3 | needs code (work row 3) |

---

## Abstract (~150 words; draft, [brackets] = numbers still to compute)

> India must soon reapportion its Lok Sabha, frozen since 1976 on the 1971 census, and the same delimitation will switch on a one-third quota for women on top of existing Scheduled Caste and Scheduled Tribe reservations. We model the process as three nested apportionments (seats to states, reserved seats within states, women's seats within categories) followed by districting. We audit every layer with lower quota, which is equivalent to extended justified representation on party-list profiles. At the state layer, we analyse six proposed formulas. A popular compromise has the Alabama paradox, a one-line fix removes it, and no population-based rule restores the south's share. In GerryChain ensembles of 2.3 million maps across 20 states, the choice of formula moves NDA seats by about 2 points and line-drawing by about 12. At the reservation layers, the natural reading of the law meets lower quota for SC and ST seats but exhibits new Alabama and population paradoxes, and the choice of formula shifts national reserved-seat totals by [X].

---

## 1 Introduction (1.0)

**Must establish:** the question is live, it has three layers, and the paper audits all of them with one axiom.

- **Hook (one paragraph).** The 1976 freeze; the 131st Amendment Bill, which failed on 17 April 2026 by 298 to 230; the north–south conflict. Open with one number: under the government's flat scale-up, Bihar gets 60 seats against a population quota of 75.8.
- **The second fact nobody debates.** The same delimitation that reallocates state seats also activates the women's quota (Art. 334A) and redraws every constituency. So the formula is one lever among several. Public debate is almost entirely about the formula.
- **Question.** At each layer, (i) what fairness standard should the rule meet, (ii) do the actual and proposed rules meet it, and (iii) how much does the layer move outcomes?
- **Contributions** (bulleted, each tagged with its claims-ledger number so known and new are visibly separated):
  1. Axiomatic analysis of six state-seat formulas. This includes a new rule (the fertility window), the Alabama paradox in Reddy's hybrid on real data with a fix, and the trilemma (claims 3–7).
  2. A lower-quota (EJR) audit of the bill: its small-state floor costs UP and Maharashtra their lower quota (claim 8).
  3. The first ensemble analysis of Indian redistricting: lines move party seats about six times as much as formulas (claim 9).
  4. The reservation layers as nested apportionment. A positive quota result, three paradoxes, and reserved-seat totals across formulas (claims 10–14).
  5. When reservation constraints conflict with EJR, and when they cost nothing (claims 15–16).
- **Roadmap** (two sentences).
- **1.1 Related work** (one paragraph, organised by layer):
  - Layer 1: Balinski–Young; Penrose; Grimmett (Cambridge Compromise).
  - The lens: Brill–Laslier–Skowron (2018); Dong–Peters (2026); Aziz et al. (2017).
  - Layers 2–3: biproportional apportionment (Balinski–Demange; Pukelsheim); parity apportionment (Mathieu–Verdugo; Cembrano et al.); Indian vertical and horizontal reservations in market design (Sönmez–Yenmez 2022; Aygün–Turhan). Note that the latter study nested quotas for jobs and admissions, not legislative seats.
  - Districting: DeFord–Duchin–Solomon; Cannon et al.; Becker–Duchin–Gold–Hirsch. All of it is on US maps.
  - India: Iyer–Weir–Ostermann on 2008; Vaishnav–Hintson (Carnegie 2019) on reserved-seat shifts; Jensenius (2017).

## 2 Background and framework (1.0)

**Must establish:** the three layers in law, how India differs from the US, and the single lens.

- **2.1 The Lok Sabha and its three layers (0.35; Figure 1).**
  - **Layer 1, state seats.** Art. 81(2)(a): seats in the same ratio to population "so far as practicable", with states under 6 million exempt. No rounding rule has ever been written down, because no reapportionment has happened since 1976.
  - **Layer 2, SC and ST seats.** Art. 330(2): in each state, "as nearly as may be" proportional to the group's share of that state's population. This is a **population-derived** quota, computed per state and per category, with no national total. 2008 outcome: 84 SC and 47 ST of 543. Assam's autonomous districts have a floor instead (Art. 330(3)).
  - **Layer 3, women's seats.** Art. 330A: one third of SC and of ST seats, and one third of all seats counting those. This is **exogenous to population**: a policy target of one third against a population share of about 48%. It is law, but it takes effect only after the next delimitation, and its rounding and rotation rules are unwritten (Art. 334A).
  - **Labels and lines.** The Delimitation Act s.9 reserves SC seats where the SC share is "comparatively large", "distributed in different parts of the State". Joint electorates: everyone votes, and only the reserved group's candidates may stand.
- **2.2 What India adds to the US model (0.25; Table 1).** The US has two layers: Huntington–Hill apportionment, then districting under *Wesberry* and the Voting Rights Act. India has three. Its minority representation is a *numerical, population-proportional* count of seats, not an outcome of litigation, so it is itself an apportionment problem. The women's quota has no US analogue at all. Almost all apportionment and ensemble theory is built on the US case. One closing sentence: this is why the paper needs a lens that works on any layer.
- **2.3 The lens: apportionment as a committee election (0.4).**
  - Model: quotas $`q_i`$, divisor methods, Webster. Cite Lectures 16–17 rather than restating them. Weight rules (`02` A.7).
  - **Prop. 1 (Thiele ↔ divisor; known).** On party-list profiles, the Thiele method with weights $`s`$ is the divisor method with $`d(k)=1/s_{k+1}`$. PAV is Jefferson, and Sainte-Laguë Thiele is Webster. One-line reason: the Thiele score is separable and concave, so greedy is optimal.
  - **Prop. 2 (EJR = lower quota = core on party lists; known).** Proof sketch in five lines (`03` C2). Cite Dong–Peters and BLS.
  - **How it is used.** Treat states as parties (§3) and categories within a state as parties (§4). In both cases, "is the group's EJR claim met?" becomes "does the group get $`\lfloor q\rfloor`$?".
  - Caveat, stated once: the axioms govern *counts*, not who wins. Under joint electorates, SC members are mostly elected by non-SC voters (Jensenius 2017). The 1932 Poona Pact is the historical choice that made this so.

## 3 Module 1: state apportionment, two levers (3.0)

**Must establish:** lever 1 (the formula) has real axiomatic trade-offs, but lever 2 (the lines) dominates partisan outcomes.

- **3.1 Lever 1: the six formulas (1.5; Table 2, Figure 2).**
  - **The six:** the README's headline rows: Freeze-at-543 (the baseline: compare with its neutral 301 seats, not the actual 293), flat scale-up, the bill, Reddy, Tharoor and the fertility window. The floor rule and R′ are indented variants in Table 2. Rajagopalan gets a footnote, since her Lok Sabha rule is the bill.
  - **Baselines.** Freeze (the 543 baseline); flat scale-up (Webster on current seats, K = 816); population (the bill). Lemma A6 in two lines. **Observation A7** framed as the south's complaint: under any population-monotone rule on current population, growing more slowly can never win a state seats.
  - **Fertility window (new).** The definition, then Prop B1 with its one-line derivative proof: every region's share moves in one direction as λ varies. Even λ = 0 does not restore the south, because growth after 2021 counts in full.
  - **Tharoor's degressive rule.** Prop B3 (single-peaked shares), as a sketch. α = 0.517 is near the south's best case (α ≈ 0.558) and still short. The gains go to the Northeast and the union territories, which sets up §4.4's ST hypothesis. Penrose's square-root law in one sentence, plus why it fails under party discipline.
  - **Reddy's hybrid.**
    - Prop B5's three-state counterexample, shown inline; it is the section's most memorable result.
    - The real-data instance: Bihar has 44 seats at K = 607 and 43 at 608.
    - Mechanism: targets that move with K, as in Hamilton's method.
    - Prop B8: rounding only the new seats (R′) fixes it, moves at most two seats, and equals R at K = 816, so the headline is unaffected.
  - **Floors.** One sentence for Prop B4: a region's share is a mix of its population share and its share of states, so no floor restores the south.
  - **The EJR column (the lens applied).** Under the bill with the simulation's 6-million floor, UP gets 138 seats against a quota of 139.22 and Maharashtra gets 73 against 74.13: their EJR claims are violated. Jefferson (PAV) fixes this but costs the south seats. This finding is about Indian law, not committee theory, and it also corrects `02` B.2, which must name its floor rule.
  - **The trilemma, stated as the section's conclusion.** Population-based rules can't restore the south. The rules that do restore it ignore population. The one popular compromise breaks monotonicity until it is fixed.
- **3.2 Lever 2: methodology (0.5).**
  - **Votes.** 2024 results pooled into seat-sharing alliances, spread over assembly segments. In 11 states each segment is shifted by its lean in the last assembly election, with constituency totals kept exact. Validation: the method reproduces 2024 in every simulated state.
  - **Neutral maps.** ReCom on the segment graph, with a size tolerance of about 20%. 4 chains × (500 burn-in + 2,000 recorded plans), for 130 state × seat-count pairs, about 2.3M plans.
  - **Drawn maps.** Short bursts (500 × 10) to maximise and to minimise NDA seats. "Tilted" = the 5th or 95th percentile of the neutral ensemble. Say plainly that this is a stand-in, not calibrated to real gerrymanders.
  - **Combination.** Formula → k_i → interpolated seat shares per state → national totals.
  - **Metrics.** Seats, efficiency gap (adapted for many parties: NDA against its strongest rival), mean–median difference.
- **3.3 Results: formula vs lines (1.0; Table 3, Figure 3).**
  - **The central comparison.** With neutral lines, the formulas span about 2 points (454–470 NDA seats). Within any formula, the lines span about 12 points in either direction. The fair 2024 comparison is the Freeze-at-543 row (301 seats neutral), not the actual 293.
  - **Thresholds.** Read Figure 3a against the 409 (majority) and 544 (two-thirds) lines. Optimised maps push every 816-seat formula past two-thirds; neutral maps leave every formula below it. This is the constitutional-amendment threshold, so it is the line that matters for the next delimitation itself.
  - **Fragility (Fig. 3b).** Optimised maps are brittle: a one-point adverse swing costs about 50 seats, and the advantage is gone by about four points.
  - **(One paragraph, if `actual_pct` is reported.)** Where the 2008 map sits in each state's neutral ensemble, compared with Iyer–Weir–Ostermann's finding of neutrality. This is the paper's only finding about the *actual* Indian map.
  - **Transition to §4.** Lever 1 barely moves parties. But the formula sets k_i, and k_i feeds the reservation layers, where §4.4 asks whether it moves *groups*.

## 4 Module 2: given k_i, how are the other quotas filled? (2.25)

**Must establish:** the reservation layers are themselves apportionments. Their natural reading passes the lens for SC and ST, falls short for women by design, and has paradoxes the single-layer theory doesn't predict.

- **4.1 The law as an algorithm: model M (0.2).** Because the law gives no rounding rule, we fix the natural reading. It matches Art. 330(2)'s per-state wording and the Election Commission's ½-up precedent (Assam, 2023).
  - $`s_i=\mathrm{rnd}(k_i\sigma_i)`$ and $`t_i=\mathrm{rnd}(k_i\tau_i)`$; General is the residual.
  - $`w^{SC}_i=\mathrm{rnd}(s_i/3)`$ and $`w^{ST}_i=\mathrm{rnd}(t_i/3)`$; $`w^G_i=\mathrm{rnd}(k_i/3)-w^{SC}_i-w^{ST}_i`$.
  - Calibration: M applied to the frozen 2008 state totals should give 84 SC and 47 ST. Report any mismatch, because it reveals the Commission's actual rule.
- **4.2 Positive result: the counting step passes the lens (0.35).**
  - The SC/ST/General split is a three-party party-list apportionment, with populations as voters.
  - **Prop. 3.** Under M, every category is within one seat of its quota (except at double exact ties). So by Prop. 2, the split satisfies EJR and the core.
    - Proof: SC and ST are each within ½ of quota, so the residual is strictly within 1.
    - *Scratch:* exhaustive check for k ≤ 99.
  - **The women's layer is different in kind.** Its "lower quota" is relative to the policy target k/3, not to population. Under descriptive approval, the guarantee falls about 0.15k seats short of women's EJR lower quota. This is the formal sense of "exogenous". Women can still win open seats; the quota is a floor, not a cap.
  - M is not a divisor method. With two rounded categories and a residual, it is closest to Hamilton's method, and so it inherits Hamilton's weakness. That sets up §4.3.
- **4.3 Where it breaks: directives and counterexamples (0.7; Figure 4, optional Table 4).**
  - **T1, residual Alabama paradox.** When the state's k rises by one, $`s_i`$ and $`t_i`$ never fall, but General can lose a seat: this happens exactly when both $`\{k\sigma\}`$ and $`\{k\tau\}`$ cross ½ in the same step. Under equidistribution this occurs on about στ of all steps (Figure 4 checks it exactly). Example: Chhattisgarh at 11 → 12 seats, recomputed with 2011 shares. The same argument applies to $`w^G`$. **Directive:** prove that no rule rounding the reserved categories independently with a residual is house monotone in all three categories. Then show that a joint divisor method on {SC, ST, General} restores monotonicity but can then break quota: the Balinski–Young trade-off, reappearing inside a state.
  - **T2, propagation.** M is monotone in k_i, so a reserved count is house monotone in H if and only if k_i is. Webster, Jefferson and R′ pass. Reddy's R fails: its Bihar paradox becomes a lost SC seat. Compute this, since it is one line of code.
  - **T3, a two-layer population paradox.** A state's SC population grows while its SC seats fall, because the state loses a seat overall. Use the toy example, then a real-data search across 2011 → 2026 projections if shares can be held fixed. Link to A7: the south's complaint, restated for its SC citizens. **Conjecture:** every nested rule has this paradox unless layer 2 ignores k_i.
  - **T6, double rounding.** $`w^{SC}_i=\mathrm{rnd}(\mathrm{rnd}(k_i\sigma_i)/3)`$ can fall below $`\lfloor k_i\sigma_i/3\rfloor`$. For example, $`s_i=1`$ gives no SC women's seat. List the states where this happens.
  - **T5 (one sentence).** State → category → gender is a laminar family, so the targets can always be rounded to within one seat. This contrasts with Lecture 10, where crossing quotas make panel selection NP-hard. India's structure becomes crossing only through geographic-spread rules, or through a national rather than per-state women's third.
- **4.4 Reserved-seat totals across the six formulas (0.5; Figure 5).**
  - Quantities: $`S(R)=\sum_i\mathrm{rnd}(R_i\sigma_i)`$, the matching ST total $`T(R)`$, and the women's totals, each against the single-layer benchmark $`\mathrm{rnd}(H\cdot\mathrm{SC}/P)`$.
  - **Decomposition.** The gap splits into a rounding term (at most ½ per state, about √n in practice) and a malapportionment term $`\sum_i(R_i-Hp_i/P)\sigma_i`$. Formulas differ only in the second term, so the figure shows exactly what a formula does to groups.
  - **Hypotheses:**
    - Tharoor's rule and the floors raise ST totals, because small, majority-ST northeastern states gain seats.
    - Restoration rules (flat, Reddy) move SC totals according to whether southern SC shares sit above or below the national average. Tamil Nadu is above it, so the sign is not obvious.
  - **Prior work.** This extends Carnegie (2019), which computed the population row at 543 only, to all six formulas plus the women's layer.
  - **The cross-module comparison.** Put the spread across formulas in reserved seats beside the spread in NDA seats from §3.3. Whatever the sign, this is the paper's bridge result.
- **4.5 Synthesis: the House as a constrained committee (0.5).** The House is a committee of size H chosen subject to the counts k_i, s_i, t_i and the women's seats. Does EJR survive the constraints? The answer depends on what voters approve.
  - **Party approval** (voters approve their alliance's candidates, and every party can field every category). **Prop. 4:** the constraints are slack. Relabel any EJR committee's seats to meet the counts; utilities depend only on party, so nothing changes, and the price of diversity is 1. One line of proof. *This is the main message: in India's party system, reservations need not cost proportionality.*
  - **Descriptive approval.** Reduces to §4.2: EJR-tight for SC and ST, short by design for women.
  - **Crossing approval** (party × identity, e.g. non-SC NDA voters approving non-SC NDA candidates). This is the only regime with real conflict. **Directive:** brute-force the smallest profile where constrained PAV violates EJR. Then define "EJR relative to the feasible set" and test constrained PAV against it.
  - **Honest limit.** Real seats are filled by single-member plurality, not by a committee rule, so this section bounds what *any* rule could achieve under the constraints. It does not describe what FPTP delivers.

## 5 Conclusion: novelties and applications (0.5)

- **What is new, in one list** (from the claims ledger):
  - the fertility-window rule
  - the Reddy paradox in real data, and its fix
  - the EJR audit of the bill's floor
  - the first Indian ensemble study, with the formula-vs-lines gap
  - lower quota for the reservation count, plus three nested-quota paradoxes
  - reserved totals across formulas
  - when reservation constraints are free for EJR
- **Applications** (the policy paragraph graders reward):
  1. **The women's-layer rounding rule is still unwritten, which makes this live law.** Recommend writing it down. Compare residual rounding (M: meets quota, has the T1 paradox) with a joint divisor method (monotone, can break quota). Recommend per-state thirds, which keep the structure laminar.
  2. **Audit the lines, not just the formula.** Require the Delimitation Commission to publish neutral ensemble baselines. Lever 2 is the bigger lever and currently has no safeguard.
  3. **If a compromise formula is adopted,** use R′ or the fertility window, both of which are monotone. Don't use Reddy's rule as written.
  4. **Read "as nearly as may be" (Art. 330(2)) as lower quota.** It is checkable, and on party lists it coincides with EJR.
- **Limitations** (one paragraph):
  - one election (2024)
  - maps built from whole assembly segments
  - 9 states without segment-level lean
  - 39 seats not redrawn
  - "tilted" is uncalibrated
  - the simulation ignores reservation labels
  - model M is a reading of the law, not the Commission's published rule
- **Future work:** reservation-constrained ReCom (`03` X4); labelling by highest share vs rotation vs Leximin (`04` T7); Banzhaf power at the two-thirds threshold; a second election.

## Appendices (no page limit)

- **A. Proofs:** Lemma A6, Obs. A7, Props B1, B3, B4, B5, B8, and Props 2, 3 and 4. T1's characterisation and impossibility, plus the T3 conjecture if proved.
- **B. More on the rules:**
  - sweeps over α, λ and f
  - quota violations by state
  - R vs R′ for K from 543 to 850
  - Rajagopalan's Revenue Sabha
  - the south's share under 2011, 2026 and 2036 figures
  - Jefferson vs Webster seat differences
- **C. Data:**
  - sources and licences
  - matching constituencies to assembly segments
  - the Gujarat urban blocks
  - the segment-lean method
  - the PCA extraction for Telangana and Ladakh (`data/README.md`)
- **D. Simulation details:**
  - chain parameters
  - `eps_for`
  - short-burst scoring
  - convergence across chains
  - seeds and runtime
- **E. Results per state:** ensemble ranges, `actual_pct`, efficiency gap, mean–median difference.
- **F. India's own committee election:** the 1952–57 two-member constituencies were approval voting with k = 2 and an SC/ST constraint (*V.V. Giri v. D. Suri Dora*). Restate the slide 13 failure of JR in this setting.
- **G. Interactive page:** screenshots and the link.

---

## Decisions the group must make first

These block numbers in the body. A recommendation is given for each.

| Decision | Blocks | Recommendation |
|---|---|---|
| Census baseline | every number | **2011** in the body (bill baseline; the only year with SC/ST shares); 2026/2036 in App. B |
| Floor rule for layer 1 | Table 2, §3.1 EJR column | the simulation's 6-million floor, named explicitly; the one-seat floor as a variant |
| Reddy's "pro rata" | §3.1 | current seats (matches the government's plan), stated as a reading |
| Fertility window end year and λ | §3.1, Fig. 2 | 2021 and λ = 0.5 as the headline; Fig. 2 shows the full λ range anyway |
| Women's third: per state or national | §4.1, §4.3 T5 | per state (keeps the structure laminar); national as a robustness check |

## Work needed, in priority order

Module 2 has no committed numbers, so it comes first.

| # | For | Task | Effort |
|---|---|---|---|
| 1 | §4 | Load 2011 SC/ST shares by state from `data/census2011/` (already downloaded; build Telangana and Ladakh from district rows per `data/README.md`) into a function next to `scheme()` in `analysis/apportion.py`, with the source in a comment | small |
| 2 | §3.1 | Add Jefferson, a lower-quota counter, the floor rule, R′ and the λ/α/f sweeps to `apportion.py` (Table 2's EJR column, Fig. 2) | small |
| 3 | §4.3 | Model M as a function; Fig. 4's exact heatmap; T1 and T6 examples with real shares; T2 (Reddy's paradox in SC seats) | small |
| 4 | §4.4 | Reserved totals for each `scheme()` name (Fig. 5); calibrate against 84/47 (needs 2001 shares, else state that it is uncalibrated) | small–medium |
| 5 | §4.5 | Write the proof of Prop. 4; brute-force the smallest crossing-approval EJR counterexample | medium |
| 6 | §3.3 | Report `actual_pct` (already printed by `summary.py`); fix seeding (`PYTHONHASHSEED`) | small |
| 7 | §2.1 | Check the legal facts marked † in `04` §1 against primary sources | small |
| 8 | §3.1 | Recompute `02`'s percentages on the chosen census baseline | small |
