# Reserved seats: India's nested quota layer

*Read after: [03 committee bridge](03_committee_bridge.md). Leads to: [05 report outline](05_report_outline.md).*

Written 27 November 2026. This file develops X3 in `03_committee_bridge.md`, focusing on two of its questions:

- **Q1:** is the nested rule monotone?
- **Q3:** how do reserved-seat totals change across the seat formulas?

Numbers marked *Computed* come from scratch scripts, not committed code. A † marks a source I did not check against a fetched copy.

**What is known and what is proposed.**

- §1 describes the law.
- §2 applies known theory (Lecture 12 and the party-list results) to India.
- §3 is the proposed contribution: theory directives for a two-level hierarchy, with SC and ST counts first and women's seats second.
- §4 and §5 relate the setup to voting rules and to Lecture 10.
- **Nested reservations are already studied in market design**, for Indian jobs and admissions, under the name vertical and horizontal reservations (§1.3). What is new here is narrower: those nested quotas as **legislative apportionment** that sits downstream of a seat formula. The candidates for novelty are T1–T4.

---

## 1. The current method of apportioning and assigning quotas

Sources were fetched on 27 November 2026, and the short quotations below are from them. Anything not fetched is marked †.

### 1.1 The pipeline

```
Layer 1  Art. 81(2)(a)   H seats  ->  k_i seats per state      (population ratio; small-state proviso)
Layer 2  Art. 330(2)     k_i      ->  s_i SC, t_i ST, rest General   (per state, "as nearly as may be")
Layer 3  Art. 330A       s_i,t_i  ->  1/3 of SC and of ST seats for SC/ST women;
                         H        ->  1/3 of all seats for women (counting the above)
Assign   Delim. Act s.9  counts   ->  which constituencies carry each label
                                      (SC: "distributed in different parts of the State",
                                       where SC share is "comparatively large";
                                       ST: where ST share is largest; women: rotation, Art. 334A)
```

### 1.2 Each step

- **Layer 1, state seats.**
  - Art. 81(2)(a) allots seats "in such manner that the ratio" of seats to population is, as far as practicable, the same for all states.
  - The ratio rule does not apply "to any State so long as the population of that State does not exceed six millions". This is the small-state floor in `apportion.py`.
  - The allocation is frozen on the 1971 census "until the relevant figures for the first census taken after the year 2026 have been published" (Art. 81(3), Art. 82; 42nd and 84th Amendments).
  - In 2008 no apportionment took place, because the state totals were frozen. So **no rounding rule for layer 1 has ever been written down.**
  - PRS's projection on the 2011 census rounds each state independently and gets 548 seats, not 543, "due to rounding off for each state". That is why a divisor method is the natural reading, as Carnegie (2019) also assumes with Webster.
- **Layer 2, SC/ST counts.**
  - Art. 330(2): the reserved number in a state "shall bear, as nearly as may be, the same proportion to the total number of seats allotted to that State" as the SC (or ST) population bears to the state's population.
  - The count is **per state** and **per category**. No national total has to be hit, and no numerical rounding rule appears in the Constitution or in the Delimitation Act 2002.
  - Delimitation Act s.8 has the Commission fix "the number of seats, if any, to be reserved" in each state. The 2008 outcome was **84 SC and 47 ST** of 543 (MEA state-wise table, 2009).
  - The census base for reservations is 2001 until the first census after 2026.
- **The Assam exception.** Art. 330(3) says ST seats for Assam's autonomous districts must be in "a proportion not less than" the ST share there. That is a **floor**, not "as nearly as may be", and the model must treat Assam differently.
- **Layer 3, women (106th Amendment, 2023).**
  - Art. 330A(2): "one-third of the total number of seats reserved under clause (2) of article 330 shall be reserved for women" belonging to SCs or STs.
  - Art. 330A(3): "one-third of the total number of seats to be filled by direct election to the House of the People shall be reserved for women", and the 330A(2) seats count towards it.
  - The Amendment was **notified on 16 April 2026**. Reservation starts only "after an exercise of delimitation is undertaken" on the first census published after commencement (Art. 334A(1)). Rotation "shall take effect after each subsequent exercise of delimitation as the Parliament may by law determine" (Art. 334A(3)).
- **Assignment.** Delimitation Act s.9(1)(c): SC constituencies "shall be distributed in different parts of the State", where the SC share is "comparatively large". s.9(1)(d)†, paraphrased: ST seats go where the ST share is largest. No implementing law yet says which seats are reserved for women.
- **Where things stand in 2026.**
  - The Constitution (131st Amendment) Bill would have done three things: raised the cap to 850 (815 from states), used the 2011 census, and dropped the wait for the next census.
  - It was defeated on 17 April 2026 by 298 to 230, short of two thirds. The Delimitation Bill 2026 was withdrawn.
  - The census reference date is 1 March 2027. PRS thinks delimitation is unlikely to finish before the 2029 election.

  So the women's layer is **law but not yet in force**, and its rounding rules are still to be written. That makes the design questions in §3 live policy questions, not just academic ones.

### 1.3 Terminology from Indian law

Indian reservation law calls SC/ST/OBC categories **vertical** reservations and the women's quota inside each category a **horizontal** reservation. That is exactly the two-level hierarchy here. Market-design work on Indian job and college admissions studies this structure:

- Sönmez and Yenmez (2022), *Econometrica*†: vertical and horizontal reservations
- Aygün and Turhan: hierarchical ("nested"/"laminar") horizontal reservations (arXiv 2602.09189; 2310.02660)
- a PKU working paper on reservation rosters using Webster-style divisor methods†

**Effect on novelty.** Nested reservations are *not* new as a structure. What has not been found is work that studies them as **apportionment of legislative seats**, where the counts come out of a seat formula in layer 1 and are then labelled geographically. The X3 claim should be stated that narrowly.

### 1.4 Model assumptions

| Step | What the law says | Practice | Our assumption (model M, §3) |
|---|---|---|---|
| Layer 1 rounding | "as far as practicable" | no apportionment since 1976 | Webster with floors, as in `apportion.py` |
| SC/ST count rounding | "as nearly as may be", per state | 84 SC / 47 ST in 2008; rule not published | nearest integer, ½ up, per state and per category, General as the remainder |
| Rounding precedent | none | ECI Assam 2023 (district seats): fraction ≥ 0.5 → 1, else 0; leftover seats to the largest fractions, ties broken by area | consistent with M |
| Women: per state or national | not specified | none yet | per state (keeps the structure laminar, T5); national as an alternative |
| Women: rounding of "one-third" | not specified† (the clauses may begin "as nearly as may be"†) | none yet | nearest integer |
| Assam autonomous districts | ST floor (Art. 330(3)) | 2 ST + 1 SC of 14 (2023) | handled separately |
| Census year | 1971 (Layer 1) / 2001 (reservations) until post-2026 census | n/a | 2011 PCA, with year stated |

---

## 2. How Lecture 12 applies

### 2.1 Direct: the counting step is a party-list apportionment

Fix state $`i`$ with $`k_i`$ seats, population $`p_i`$, SC share $`\sigma_i`$ and ST share $`\tau_i`$. Splitting the $`k_i`$ seats into {SC, ST, General} is an apportionment with three "parties", where the groups' populations play the role of voters. In Lecture 12's language, this is a **party-list profile**: an SC citizen "approves" SC seats, an ST citizen ST seats, and everyone else General seats. The approval sets are disjoint. So the results from `03_committee_bridge.md` §3 apply as they stand:

- **Thiele ↔ divisor** (Brill, Laslier and Skowron 2018). A Thiele rule picking the split is the divisor method with signposts $`d(j)=1/s_{j+1}`$. PAV gives D'Hondt.
- **EJR = PJR = core = lower quota** on party-list profiles. The PJR ⇒ lower quota direction is Brill, Laslier and Skowron (2018), Prop. 6. The full equivalence is Dong and Peters (2026), arXiv:2605.04612, Prop. 1 in the PDF version.

  So "does India's reservation count satisfy EJR?" means exactly "does every category get at least $`\lfloor k_i\cdot\text{share}\rfloor`$ seats?"
- **Rounding.** Suppose India rounds each reserved category to the nearest integer independently, with General taking the remainder. That is model M. The law doesn't specify it, but it matches the per-state wording of Art. 330(2) and the ECI's ½-up rounding precedent (§1.4). Then the split satisfies quota for all three categories, except at double exact ties (*Computed*: exhaustive check with exact fractions, $`k\le 99`$, shares on a 1/200 grid).

  The reason: SC and ST each lie within ½ of their quotas, so General lies strictly within 1 of its quota. **So the counting step satisfies EJR and the core.** This rule is not a divisor method. With two rounded categories plus a residual, it is closest to Hamilton's method, and it inherits Hamilton's weakness (§3, T1).

### 2.2 Not direct: the election step

Lecture 12's axioms are about **voter groups' utility**. India's reservations constrain **candidates**, not voters. In a reserved seat:

- only SC (or ST) candidates may stand
- every registered voter in the constituency votes, under joint electorates

So the axioms govern *how many* seats each group gets. They say nothing about *whom the group's members elect*. Jensenius (2017) notes that most SC legislators are elected by mostly non-SC electorates, because SCs are a minority almost everywhere.

This choice was made explicitly in 1932:

- **The Communal Award** offered the Depressed Classes separate electorates, in which SC voters elect SC representatives. That would have made SC voters a genuine party-list voter group, and Lecture 12 would apply to the election as well.
- **The Poona Pact** replaced this with reserved seats in joint electorates, which is today's system.

The report should state this distinction once, because it fixes which parts of committee theory transfer.

### 2.3 The women's layer is not proportional

Women are about half the population, but Art. 330A reserves one third of seats. So "lower quota" for women is relative to a **policy target** $`k/3`$, not to population share. The party-list machinery still applies, with target shares in place of population shares. EJR's justification ("a group of size $`\ell n/k`$ deserves $`\ell`$ seats") does not apply. Treat the women's layer as an exogenous quota, the way Lecture 10 treats quotas.

---

## 3. Theory directives for the nested hierarchy

**Notation.**

- Layer 1: a seat formula $`R`$ gives $`k_i=R_i(p,H)`$.
- Layer 2 gives the counts $`s_i`$ (SC), $`t_i`$ (ST) and $`g_i=k_i-s_i-t_i`$ (General).
- Layer 3 gives the women's seats $`w^{SC}_i, w^{ST}_i, w^{G}_i`$.

**Working model M** (to be matched against §1):
- $`s_i=\mathrm{rnd}(k_i\sigma_i)`$ and $`t_i=\mathrm{rnd}(k_i\tau_i)`$
- $`w^{SC}_i=\mathrm{rnd}(s_i/3)`$ and $`w^{ST}_i=\mathrm{rnd}(t_i/3)`$
- $`w^{G}_i=\mathrm{rnd}(k_i/3)-w^{SC}_i-w^{ST}_i`$

### T1 (Q1). Within-state house monotonicity: the residual category breaks

- **Claim (easy).** Under M, $`s_i`$ and $`t_i`$ never decrease in $`k_i`$, and rise by at most 1 per extra seat. The reason: $`k\sigma`$ rises by $`\sigma<1`$, and nearest rounding is monotone.
- **Claim (the paradox).** $`g_i`$ can fall when $`k_i`$ rises, even though General's quota $`k_i(1-\sigma_i-\tau_i)`$ rises. This happens exactly when $`s_i`$ and $`t_i`$ both tick up at the same step. It is an Alabama paradox for the General category, in a layer whose structure resembles Hamilton's.
- *Computed*, illustrative shares close to 2011 values. These are placeholders; use the census Primary Census Abstract figures in the report.

  | state (approx. shares) | step | (SC, ST, Gen) before | after |
  |---|---|---|---|
  | Chhattisgarh (σ=.128, τ=.306) | 11 → 12 | (1, 3, 7) | (2, 4, 6) |
  | Madhya Pradesh (σ=.156, τ=.211) | 16 → 17 | (2, 3, 11) | (3, 4, 10) |
  | Jharkhand (σ=.121, τ=.262) | 20 → 21 | (2, 5, 13) | (3, 6, 12) |
  | Rajasthan (σ=.178, τ=.135) | 25 → 26 | (4, 3, 18) | (5, 4, 17) |

  Chhattisgarh's current 11 seats make its row the one to check first against real data.
- **Directives:**
  1. Characterise when the paradox occurs. It needs $`\{k\sigma\}`$ and $`\{k\tau\}`$ to both cross ½ between $`k`$ and $`k+1`$. Estimate how often this happens: under equidistribution, roughly $`\sigma\tau`$ of all steps.
  2. The same argument applies to $`w^G_i`$, because it is also a residual.
  3. Prove that **no** rule that rounds the reserved categories independently and leaves a residual can be house-monotone for all three categories. Then ask whether a divisor method applied to {SC, ST, General} jointly fixes this. Balinski and Young say yes for house monotonicity, but it may then break quota (Theorem A5's trade-off, now inside a state).

### T2 (Q1). Propagation through layers

- **Lemma to prove.** Layer 2 under M is monotone in $`k_i`$. So the composite count $`s_i(H)`$ is house-monotone in $`H`$ **iff** $`k_i(H)`$ is.
  - Webster, Jefferson and the fixed hybrid R′ pass (Lemma A6, Prop B8 in `02_theory_state_apportionment.md`).
  - Reddy's R fails (Prop B5): its Alabama paradox becomes an Alabama paradox in **SC seats**.
- **Directive.** Rerun `02_theory_state_apportionment.md`'s 3-state counterexample for R with a reserved share attached to the losing state. Report the SC seat that is lost.

### T3 (Q1). A two-layer population paradox

- **Claim.** A state's SC population can **grow** while its SC seats **fall**, even with a population-monotone formula. This happens when the state's total population falls enough to lose a seat.
- *Computed*: two states, $`H=20`$, Webster.

  | | state A pop. | state A SC share | state A SC pop. | $`k_A`$ | state A SC seats |
  |---|---|---|---|---|---|
  | before | 425 | .28 | 119.0 | 9 | 3 |
  | after | 385 | .31 | 119.4 | 8 | 2 |

  State B is unchanged at 575.
- **Why it matters.** A national, single-layer apportionment of SC seats would be population-monotone in SC population. The nested design trades that away for "SC seats in proportion *within each state*" (Art. 330(2)). Ask whether any nested rule avoids this. Conjecture: no, unless layer 2 ignores $`k_i`$.
- **Link to Observation A7.** Slow-growing states lose seats, and so their SC populations lose reserved seats even if the SC population itself is growing. This is the reserved-seat version of the southern complaint.

### T4 (Q3). Reserved-seat totals across the six formulas

- **Quantity.** National totals $`S(R)=\sum_i \mathrm{rnd}(R_i\sigma_i)`$, the matching ST total $`T(R)`$, and the women's totals. Compare with the single-layer benchmark $`\mathrm{rnd}(H\cdot \mathrm{SC}/P)`$.
- **Bound to prove.** $`|S(R)-H\cdot\mathrm{SC}/P|`$ splits into two terms:
  - a **rounding term**, at most ½ per state, about $`\sqrt{n}`$ in practice
  - a **malapportionment term**, $`\sum_i (R_i - Hp_i/P)\sigma_i`$
  
  The second term is where formulas differ.
- **Hypotheses to test:**
  - The degressive rule (Tharoor) and the floors raise ST totals, because small, mostly-ST northeastern states gain seats.
  - The fertility-window and restoration rules lower SC totals if southern SC shares are below the national average. Check this; Tamil Nadu's SC share is above average.
- **Recipe.**
  - For each `name` in `scheme()` in `analysis/apportion.py`, take $`k_i`$, apply M, and sum.
  - Inputs: state SC and ST shares from the 2011 Primary Census Abstract.
  - Output: a 6 × {SC, ST, women, SC-women, ST-women} table.
  - **Calibration check first.** Model M, applied to the frozen 2008 state totals with 2001-census shares, should give the actual 84 SC and 47 ST, state by state. Any mismatch shows the rounding rule the Commission actually used. Example: with 2011-like shares, M gives Chhattisgarh 3 ST seats, while 2001 shares (about 31.8%†) give 3.5, which rounds to 4.
- **Prior work.** Vaishnav and Hintson (2019) did the population-formula row. They used the 2011 census at the current size of 543 and found one more ST seat, two more SC seats, and 18 seats changing status. Tillin, Vaishnav and Robaina (Carnegie, May 2026) model House expansion (about 775 and about 824 seats) but do not project SC, ST or women's seats. The other five rows and the women's columns are the addition.

### T5. Nested quotas are laminar, so feasibility is easy

- **Structure.** The sets state → category → (women / not) form a **laminar family**: any two sets are nested or disjoint. Fractional targets on a laminar family can always be rounded to integers that stay within 1 of every target. Rounding top-down works, and so does a flow formulation with floor and ceiling bounds; Cox (1987)† covers controlled rounding.
- **Contrast with Lecture 10.** The NP-hardness of quota-feasible panels comes from **crossing** features. India becomes non-laminar when constraints cross, for example:
  - geographic spread ("SC seats distributed in different parts of the State")
  - national women's thirds that cut across states, if the third is national rather than per state (see §1)

  **Directive:** state exactly which legal clauses keep the structure laminar, and which make it crossing.
- **Prior work.** Aygün and Turhan study hierarchical ("laminar") horizontal reservations in Indian allocation problems (§1.3). The laminar-rounding fact itself is standard. So T5 is framing that borrows known tools. It is not a contribution in itself.

### T6 (optional, Q2, brief). Lower quota for SC and ST women

$`w^{SC}_i=\mathrm{rnd}(s_i/3)`$ rounds a number that was itself already rounded. Check whether there are states where $`w^{SC}_i<\lfloor k_i\sigma_i/3\rfloor`$, i.e. where double rounding falls below the one-step quota. Small $`s_i`$ (1–2 SC seats) is where this bites. For example, $`s_i=1`$ gives $`w^{SC}_i=0`$.

---

## 4. How voting rules interact with population-based reservation

The reservation counts are set by **population groups**, not geography. Geography only decides *which* constituencies carry the label. Here is what that does to voting.

### 4.1 Actual elections

- **Inside a reserved constituency,** the rule is still plurality (first past the post), over a restricted candidate set. The winner is the SC candidate preferred by a plurality of all voters. Parties choose SC nominees with the majority electorate in mind, so descriptive representation is guaranteed but substantive representation is not (Jensenius 2017).
- **Effects on policy are real.**
  - Pande (2003) finds that state-level SC/ST reservation raised targeted transfers.
  - Chattopadhyay and Duflo (2004) find that women's reservation in village councils changed which public goods were provided.

  So the label is not cosmetic, even under joint electorates.
- **India's own committee election.** In 1952 and 1957 some constituencies elected **two** members, one seat reserved for SC/ST, and each voter cast two votes. This is **bloc voting**: Lecture 12's AV with $`k=2`$, plus a constraint that at least one winner is SC/ST. Parliament abolished it in 1961 (Two-Member Constituencies (Abolition) Act†).
  - The legal controversy: can an SC candidate win the *general* seat if they finish in the top two? See *V.V. Giri v. D. Suri Dora* (1959)†.
  - This is a real, documented case of approval-style committee voting with a diversity constraint, so it fits the report's appendix. AV fails JR, and the same 1-voter / 4-voter example from slide 13 can be phrased in this setting.

### 4.2 The House as a constrained committee (theory)

- **Model.** Treat the House as a committee $`W`$, $`|W|=H`$, chosen under hard constraints: the per-state counts $`k_i`$, the reserved counts $`s_i, t_i`$ and the women's counts. Bredereck et al. (2018) and Celis, Huang and Vishnoi (2018) study Thiele rules under such constraints.
- **Directive (axioms under constraints).**
  - Constrained PAV: maximise the PAV score subject to the quotas. Unconstrained PAV satisfies EJR, so ask whether the constrained version does.
  - Expected answer: not always. Find the smallest profile where the quotas force a violation. A cohesive non-SC group of size $`\ge n/k`$ could lose its only seat to an SC reservation.
  - Then define "EJR relative to the feasible set" and test whether constrained PAV satisfies it.
- **Price of diversity.** The ratio of constrained to unconstrained PAV score. On party-list profiles where the quotas match population shares, the ratio is about 1. The interesting case is women's one third, which is far from the "approval" share of any voter group.

### 4.3 Alternatives

- **Separate electorates** (Communal Award, 1932): reserved seats elected only by SC voters. This makes the profile genuinely party-list, so Lecture 12's axioms apply to the election itself.
- **Multi-member constituencies with PAV or STV plus quotas.** These replace geographic labelling with a constrained committee rule. Proportionality then comes from the rule rather than from rotating labels.
- **Cumulative voting** gives a minority concentrated in one area a way to win a seat without reserving it. It is a long-standing alternative in US voting-rights remedies†.

---

## 5. Is Lecture 10 (sortition) helpful?

**Verdict: yes for assigning *which* constituencies are reserved; no for Q1 and Q3, which are about counting.**

- **The same quota model.** Slide 15 defines features $`F`$, values $`V_f`$, and lower and upper quotas $`\ell_{f,v}\le|\{x\in P:x_f=v\}|\le u_{f,v}`$. Read "volunteers" as constituencies and "panel" as the set reserved for a group, with features state, category, women and region. This is exactly India's labelling problem.
- **Hardness frames T5.** Slide 15 says that finding a quota-feasible panel is NP-hard. That hardness needs crossing features. India's nested layer is laminar, so it is easy. Geographic-spread rules are where crossing, and hardness, could enter.
- **Fair lotteries over labellings.** Slides 19–23 make two points:
  - a deterministic or greedy selection gives some members very low selection probability
  - Leximin maximises the minimum probability

  India today works like this:
  - **SC seats** go to the constituencies with the highest SC share, so the same seats stay reserved for decades.
  - **Women's seats** are meant to **rotate** after each delimitation (Art. 334A(3)). Rotation is a lottery spread over time.
- **Directive T7.** Compare three labelling rules over quota-feasible labellings:
  - (a) highest share
  - (b) rotation
  - (c) Leximin

  Measure two things: the minimum probability over constituencies of being reserved, and how close each reserved seat's group share is to the group's statewide share.

  Chattopadhyay and Duflo (2004) used village-council rotation as quasi-random assignment, which is empirical precedent that rotation acts like a lottery.
- **Where Lecture 10 does not help.** Q1 and Q3 are deterministic rounding questions about $`k_i`$, $`s_i`$ and $`t_i`$. No randomness or panel choice is involved.

**Recommendation.** Cite Lecture 10 in one paragraph for T5 and T7. Use Lecture 12 for §2 and §4.

---

## 6. References

Entries already in `03_committee_bridge.md` §6 are not repeated: Balinski and Young; Balinski and Demange; Bredereck et al.; Celis, Huang and Vishnoi; Flanigan et al.; Jensenius; Lang and Skowron; Mathieu and Verdugo; Pande; Chattopadhyay and Duflo; Vaishnav and Hintson.

- Brill, M., Laslier, J.-F. and Skowron, P. (2018). Multiwinner approval rules as apportionment methods. *Journal of Theoretical Politics* 30(3). Prop. 6: PJR ⇒ lower quota on party lists. (Cited as Prop. 6 in Dong and Peters 2026.)
- Dong, C. and Peters, J. (2026). An axiomatic analysis of proportionality notions in approval-based multiwinner voting. arXiv:2605.04612. Prop. 1: LQ = PJR = PJR+ = EJR = EJR+ = Core on party-list instances.
- Brill, M., Gölz, P., Peters, D., Schmidt-Kraepelin, U. and Wilker, K. (2020). Approval-based apportionment. AAAI-20; arXiv:1911.08365. §4.2: an apportionment method that fails lower quota yields a rule that fails EJR.
- Procaccia, A. *Optimized Democracy*, Fall 2026, Lecture 10 (Sortition) and Lecture 12 (Committee Elections). Lecture 10 draws on Flanigan, Gölz, Gupta, Hennig and Procaccia (2021), *Nature*.
- Sönmez, T. and Yenmez, M. B. (2022). Affirmative action in India via vertical, horizontal, and overlapping reservations. *Econometrica* 90(3).†
- Aygün, O. and Turhan, B. Hierarchical horizontal reservations (arXiv:2602.09189) and generalized lexicographic choice rules (arXiv:2310.02660). Titles paraphrased from search results.†
- Tillin, L., Vaishnav, M. and Robaina (2026). Carnegie Endowment report on Lok Sabha reapportionment, May 2026. carnegieendowment.org/research/2026/05/…
- PRS Legislative Research (2026). Issues for Consideration: Delimitation Bills of 2026. Includes the 2011-census state projections. BillTrack: Delimitation Bill 2026, marked "Infructuous".
- Constitution of India, Arts. 81, 82, 330, 330A, 334A. The Constitution (106th Amendment) Act 2023, notified 16 April 2026 (S.O. 1922(E)). Delimitation Act 2002, ss. 8–9.
- Election Commission of India (2023). Assam delimitation final paper: the ½-up rounding precedent.
- Ministry of External Affairs (2009). State-wise seats in Lok Sabha after the 2008 delimitation: 84 SC and 47 ST.
- Cox, L. H. (1987). A constructive procedure for unbiased controlled rounding. *JASA* 82.†
- *V.V. Giri v. D. Suri Dora* (1959), Supreme Court of India.†
- The Two-Member Constituencies (Abolition) Act, 1961.†
- Communal Award (1932) and Poona Pact (1932).†
