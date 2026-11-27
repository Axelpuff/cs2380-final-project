# Committee-flavored apportionment: links to Lecture 12, extensions, and literature

Written 27 November 2026. This file is a companion to `report_outline.md` and does not change it. The numbers marked *Computed* came from ad hoc runs against `analysis/apportion.py` on the date above. They are not yet in committed code.

**Novelty at a glance.**

- **Section 3 is known theory applied to India.** It links Lecture 12 to Lectures 16–17 and is useful framing, but it is not a contribution.
- **The main novelty claim is X3,** the properties of India's nested reservation layer. X2 and X4 are new applications. X5 is open theory.
- These claims rest on a handful of searches, not a systematic review. Before the report claims anything as new, search specifically for "nested quotas apportionment" and for work on how India apportions reserved seats.

## 1. Why this matters for the project

The codebase treats apportionment only in the framework of Lectures 16–17: divisor methods, house and population monotonicity, and quota. Two features of the Indian case fit committee elections (Lecture 12) better than classical apportionment:

1. **Groups overlap.** A citizen belongs to a state, possibly to the Scheduled Castes (SC) or Scheduled Tribes (ST), and to a gender. Each group has reserved seats: SC and ST seats under Art. 330, and one third for women under the 106th Amendment (2023). Classical apportionment assumes disjoint groups (states). Committee elections are built for overlapping approval sets.
2. **Voters support more than one party.** Indian elections are fought by seat-sharing alliances, so an NDA voter is plausibly content with a BJP, JD(U) or TDP member. This is approval over parties, not a single party choice.

Nothing in the current code models either feature. This file sets out the bridge and the extensions it suggests.

## 2. Lecture 12 in brief

- **Setting.** Voters $`N`$ (with $`n=|N|`$), candidates $`A`$, and each voter $`i`$ approves a set $`\alpha_i\subseteq A`$. A committee $`W\subseteq A`$ has $`|W|=k`$. Voter utility is $`u_i(W)=|\alpha_i\cap W|`$.
- **Thiele methods.** Given weights $`s_1,s_2,\dots`$, choose $`W`$ to maximise $`\sum_i (s_1+\dots+s_{u_i(W)})`$.
  - **AV** (approval voting): $`s=(1,1,1,\dots)`$.
  - **CC** (Chamberlin–Courant): $`s=(1,0,0,\dots)`$.
  - **PAV** (proportional approval voting): $`s=(1,\tfrac12,\tfrac13,\dots)`$.
- **JR (justified representation).** If a group $`S`$ has $`|S|\ge n/k`$ and its members share at least one approved candidate, some member of $`S`$ has at least one approved candidate on $`W`$. CC satisfies JR; AV does not.
- **EJR (extended JR).** If $`|S|\ge \ell n/k`$ and the members share at least $`\ell`$ approved candidates, some member of $`S`$ has at least $`\ell`$ approved candidates on $`W`$. PAV satisfies EJR; CC does not.
- **Core.** $`W`$ is in the core if no group $`S`$ can take a committee $`W'`$ with $`|W'|\le k|S|/n`$ that every member of $`S`$ strictly prefers. The lecture cites Becker, Greger and Peters (2026) for the result that the core is always nonempty.

## 3. The bridge: apportionment is a party-list committee election

Treat each state as a "party" with unlimited candidates. Each citizen of state $`i`$ approves exactly the candidates from state $`i`$. Approval sets are disjoint, so this is a **party-list profile**, the special case slide 10 discusses before asking "how do we define proportionality when approval sets intersect?"

**Proposition C1 (known; Brill, Laslier and Skowron 2018).** On party-list profiles, the Thiele method with non-increasing weights $`s`$ is the divisor method with signposts $`d(k)=1/s_{k+1}`$.

- **Why.** The Thiele score splits into a sum over parties, $`\sum_i p_i(s_1+\dots+s_{k_i})`$, and each term is concave in $`k_i`$. So adding seats greedily is optimal, and the greedy step gives the next seat to the largest $`p_i\,s_{k_i+1}=p_i/d(k_i)`$. That is the sequential form of a divisor method (`theory.md` A.3).
- **The dictionary:**

  | Thiele method | Weights $`s_j`$ | Apportionment method |
  |---|---|---|
  | PAV | $`1/j`$ | Jefferson / D'Hondt |
  | Sainte-Laguë Thiele | $`1/(2j-1)`$ | Webster / Sainte-Laguë |
  | AV | $`1`$ | every seat to the largest state |
  | CC | $`(1,0,0,\dots)`$ | one seat to each of the $`k`$ largest states |

- *Checked:* across 300 random three-state instances, brute-force Thiele optima matched divisor allocations except where there were ties. None of the divisor allocations scored below the Thiele optimum.

**Observation C2 (known; folklore level).** The literature already says that EJR-type axioms generalise lower quota on party-list profiles, and that D'Hondt, and so PAV, satisfies lower quota (Peters 2018; Skowron 2021; Balinski and Young). The step to the core is short. Present C2 as an observation with citations, not as a new result. On party-list profiles, with $`q_i`$ the standard quota:

- **JR** holds if and only if every state with $`q_i\ge1`$ gets at least one seat.
- **EJR** holds if and only if **lower quota** holds: $`k_i\ge\lfloor q_i\rfloor`$ for every $`i`$.
  - *Sketch:* the strongest EJR claim of state $`i`$'s citizens has $`\ell=\lfloor q_i\rfloor`$. All of them have the same utility $`k_i`$, and groups mixing states share no candidates.
- **The core** also holds if and only if lower quota holds.
  - *Sketch:* a deviating group does best by taking whole states, since part of a state lowers its seat budget without lowering what its members need. So a deviation exists exactly when $`\sum_{i\in T}(k_i+1)\le\sum_{i\in T}q_i`$ for some set of states $`T`$. If that holds for $`T`$, then $`k_i+1\le q_i`$ for some $`i\in T`$, which is a violation of lower quota.
  - The edge cases where quotas are exact integers need care.

**Consequences:**

1. **The two lectures meet.** Restricted to party lists, Lecture 12's theorem that PAV satisfies EJR becomes the classical fact that Jefferson's method satisfies lower quota.
2. **Webster can fail EJR.** This is a restatement of Webster's known failure of lower quota (Balinski and Young), so it is an illustration, not a result. Take populations $`(7,8,7,33)`$ and $`k=5`$.
   - Webster gives $`(1,1,1,2)`$, but state 4's quota is exactly 3.
   - Its 33 citizens are a group of size $`3n/k`$ with 3 common candidates, yet they get only 2 seats.
   - Corollary A5 in `theory.md` says such cases exist; this is a concrete one. It also answers the slide 16 poll for party lists.
3. **The bill uses the member of the Thiele family that can fail EJR.** Guaranteeing EJR means switching to Jefferson (PAV), which tilts towards large states.
   - *Computed* (2026 projections, $`K=816`$, same floors as the simulation): Jefferson gives UP +2 seats, Bihar +1 and Maharashtra +1. Andhra Pradesh, Kerala, Uttarakhand and Delhi each lose one.
   - So EJR costs the south seats.
4. **Every rule restated in committee language.** A state below its lower quota is a group of citizens whose EJR claim is violated. This is new as a calculation on India, but it is essentially the quota-violation counts in `theory.md`, renamed. The one substantive finding is about Indian law, not committee theory: the 6-million floor pushes UP and Maharashtra below lower quota under the bill.

   *Computed* (2026, $`K=816`$, simulation floors):

   | Rule | States below lower quota | Seats short in total | Worst-hit states |
   |---|---|---|---|
   | Flat scale-up | 9 | 61 | UP, BR, RJ, MP, GJ |
   | Reddy hybrid | 7 | 71 | UP, BR, RJ, MP, JH |
   | Tharoor degressive (α = 0.517) | 9 | 139 | UP, BR, MH, WB, MP |
   | Fertility window (λ = 0.5) | 6 | 11 | UP, RJ, BR, DL, MP |
   | Bill (Webster on population) | 2 | 2 | UP, MH |
   | Jefferson on population | 0 | 0 | none |

> **Inconsistency found in `theory.md` B.2.** It says every state is within one seat of its quota under the bill at $`K=816`$. That holds with a one-seat floor. With the simulation's floors (states under 6 million keep their current seats), UP gets 138 against a quota of 139.22, and Maharashtra gets 73 against 74.13. The 6.3 extra seats given to small states come out of the big states. `theory.md` needs to name the floor rule it uses.

## 4. Extensions, ranked by value for effort

### X1. Apportionment as a committee election (cheap; framing, not novelty)

- **Content:** C1, C2, the $`(7,8,7,33)`$ example, and the table above, all presented as known results applied to India.
- **Remaining work:** add a Jefferson rule and a lower-quota counter to `apportion.py` so the table can be reproduced.
- **Why it's worth it:** it connects the project to a second lecture and gives the trilemma a fourth column: does the rule satisfy EJR with respect to population? It also sets up the vocabulary X3 needs.

### X2. Alliances as approval sets: party-approval apportionment (medium)

- **Idea:** model each voter as approving every party in their alliance. This is the **approval-based apportionment** setting of Brill, Gölz, Peters, Schmidt-Kraepelin and Wilker (2020/2022). Voters approve parties, and seats go to parties.
- **Questions:**
  1. Within each state's delegation (a committee of $`k_i`$), how many seats short of lower quota is each alliance, under each map type? This gives an axiomatic disproportionality measure next to the efficiency gap.
  2. Does counting allies, rather than the leading party only, change which maps look gerrymandered?
- **Data:** alliance vote shares are already in `analysis/out/*.json` (`voteshare`). Party-level breakdowns are in the stage-1 pickle.
- **Caveat:** a single-member plurality system will violate EJR under every formula. The useful quantity is how much drawn maps add to the shortfall relative to neutral maps.
- **Related:** Delemazure et al. (2023) show that strategyproofness and proportionality cannot both hold in party-approval elections. That limit should be noted if any alliance-based rule is proposed.

### X3. Reserved seats as committee selection with overlapping groups (medium–large; the main novelty claim)

This is where the project could add something new. Related work uses biproportional or flat quota constraints. India's structure is different: hierarchical rounding (states, then categories, then women) followed by single-member districts. Questions 1 and 2 need only state-level census data plus theory, so they are the cheap core of the claim.

- **Idea:** after the formula fixes $`k_i`$ seats per state, two more allocations follow:
  1. **Category counts.** These are SC seats $`s_i\approx k_i\cdot\mathrm{SC}_i/p_i`$ and the matching ST seats. Rounded within each state, the national result is a two-dimensional (state × category) apportionment: the **biproportional** problem (Balinski and Demange 1989; used in Zurich since 2003).
  2. **Labels.** Constituencies are then labelled SC, ST or women, with quotas that overlap, since one third of SC and ST seats must also go to women. Mathieu and Verdugo (2022) study exactly this for gender parity in Chile's 2021 Constitutional Convention. Cembrano et al. (2025) handle several dimensions at once.
- **Questions:**
  1. **Monotonicity of the nested rule.** Can a state's SC or ST seats fall when the House grows, or when the seat formula changes? That would be an Alabama paradox in the second layer. Is the composite rule population monotonic?
  2. **Rounding and quota.** Does India's rule satisfy multi-attribute proportionality (Lang and Skowron 2018)? Its layers are Webster across states, then rounded SC and ST counts within states, then one third women nested inside. Check whether the nested rounding pushes some group below its lower quota, such as SC women in small states.
  3. **Reserved-seat totals by formula.** A seat formula also changes the national count of reserved seats, because SC and ST shares vary widely by state. Carnegie (Vaishnav and Hintson 2019) already estimated how reserved seats shift under population-based reapportionment, including the south losing reserved seats. So this question is new only across the other five formulas and the women's layer. One hypothesis: Tharoor's degressive rule raises ST seats, because the Northeast is mostly ST.
  4. **Design option:** pick which constituencies are reserved with a quota-respecting committee rule. Options are a diversity-constrained Thiele rule (Bredereck et al. 2018; Celis, Huang and Vishnoi 2018) or a quota-sampling approach like citizens'-assembly selection (Flanigan et al. 2021). Compare it with the current practice of reserving where a group's share is highest while spreading reserved seats geographically (Jensenius 2017).
- **Data needed:** 2011 Primary Census Abstract SC and ST populations, by state for questions 1–3 and by assembly segment for question 4.
- **Modelling caveat:** treating descriptive representation as approval ("an SC voter approves SC candidates") is a modelling choice, not standard. The report would need to defend it.

### X4. Reserved-seat constraints in the redistricting ensembles (large)

- **Idea:** whoever draws the lines also decides which areas become SC or ST seats, a lever for gerrymandering that has no US equivalent. Becker, Duchin, Gold and Hirsch (2021) build ensembles under Voting Rights Act constraints. The analogue here is ReCom with reservation quotas.
- **Needs:** SC and ST shares for each segment, plus a rule for labelling seats inside each simulated map.

### X5. The core of the overlapping problem (stretch; theory)

- On party lists the core reduces to lower quota (C2). With overlapping groups (X3) it does not.
- **Question:** is India's actual allocation in the core of the overlapping profile? Look for a deviating coalition with a small integer program. A core allocation always exists, so a violation would mean a better allocation is available.

## 5. Literature review

### 5.1 Classical apportionment

Balinski and Young (2001) is the standard treatment of divisor methods, monotonicity and quota, including the impossibility result used in `theory.md` (A4). Pukelsheim (2017) covers apportionment as practised in European electoral law, including biproportional methods. Penrose (1946) is the origin of the square-root law behind Tharoor's degressive rule. Grimmett (2012) analyses the Cambridge Compromise for the European Parliament, which combines a floor with proportional seats. All of these treat states as disjoint groups and do not handle quotas within a state.

### 5.2 Committee elections and proportionality axioms

Aziz et al. (2017) introduced JR and EJR and showed that PAV satisfies EJR. Sánchez-Fernández et al. (2017) proposed proportional justified representation, a weaker axiom that more rules satisfy. Peters and Skowron (2020) moved beyond Thiele methods to rules that satisfy EJR and run in polynomial time, the line leading to the Method of Equal Shares. Lackner and Skowron (2023) survey the field.

The **core** was the main open problem. Peters (2025) showed existence for committees of up to 8 seats. Becker, Greger and Peters (arXiv 2605.06194, 2026) showed it for up to seven voter types. Lecture 12 cites Becker, Greger and Peters (September 2026) for existence in general. An arXiv paper with that title (2609.11912) exists, but this review did not confirm its authors.

### 5.3 Committee elections as apportionment (the bridge)

Brill, Laslier and Skowron (2018) show that approval-based multiwinner rules restricted to party lists induce apportionment methods. PAV induces D'Hondt (Jefferson), and Monroe's rule induces largest remainder (Hamilton). This is the basis of C1.

Brill, Gölz, Peters, Schmidt-Kraepelin and Wilker (2020; journal version 2022) go further: voters approve several parties. They generalise D'Hondt to that setting and show that EJR can coexist with committee monotonicity, the committee analogue of house monotonicity. Delemazure et al. (2023) prove that in party-approval elections, strategyproofness and proportional representation cannot both hold.

C2, which characterises JR, EJR and the core as quota conditions on party lists, is folklore. Peters (2018) and Skowron (2021) both note that EJR-type axioms generalise lower quota and that D'Hondt, and so PAV, satisfies it. The project should cite it, not claim it.

### 5.4 Proportionality across several dimensions

- Balinski and Demange (1989) give an axiomatic theory of proportional matrices. Their biproportional divisor method has been used in Zurich since 2003 (Pukelsheim 2017).
- Lang and Skowron (2018) define proportional representation over several attributes, which reduces to party-list apportionment when there is a single attribute.
- Mathieu and Verdugo (2022) study apportionment with gender parity, motivated by Chile's 2021 Constitutional Convention, and compare a greedy mechanism with a biproportional one. Cembrano, Correa, Díaz and Verdugo (2025) extend this to several dimensions.
- Bredereck et al. (2018) and Celis, Huang and Vishnoi (2018) study committee selection under diversity or fairness constraints, mainly its computational complexity.
- Flanigan et al. (2021) select citizens' assemblies under quotas over overlapping features, with a fairness objective (from this course's instructor's group).

**Gap.** Among the papers found, none studies a system with India's structure: a divisor method across states, then hierarchical (nested, not biproportional) quotas within states, then single-member districts drawn afterwards. This is the basis for the X3 novelty claim. A targeted search is still needed to confirm it.

### 5.5 Redistricting ensembles

DeFord, Duchin and Solomon (2021) introduced ReCom. Cannon et al. (2022) introduced short-burst optimisation. Becker, Duchin, Gold and Hirsch (2021) add Voting Rights Act constraints to ensembles. All of this work is on US maps; we know of no ensemble study of Indian delimitation.

### 5.6 India: delimitation and reserved seats

- Iyer, Weir and Ostermann (2026 working paper) study whether incumbents influenced the 2008 delimitation, using data from 23 states. They conclude the process was largely politically neutral. That is the natural benchmark for an outlier test on the 2008 map.
- Jensenius (2017) is the main study of SC reserved seats. She finds the quotas reduced discrimination mainly by creating an SC political elite. She also notes that because SCs are a minority almost everywhere, most SC legislators are elected by majority non-SC electorates. That fact matters for any model where "SC voters approve SC candidates".
- Vaishnav and Hintson (Carnegie, 2019) estimate how reapportionment would shift reserved seats. Updating to the 2011 census would add only a few reserved seats overall, and slower-growing southern states would lose reserved seats to the north. This is the closest prior work to X3's third question.
- Pande (2003) and Chattopadhyay and Duflo (2004) show that reservation changes policy outcomes, for SC and ST groups and for women in local councils respectively. That is why the reservation layer is worth modelling at all.

### 5.7 Where this project fits

| Thread | What it offers | What this project adds |
|---|---|---|
| Classical apportionment | axioms for disjoint states | applies them to India's six proposals; the trilemma |
| Committee elections | JR, EJR and core for overlapping groups | (X1, framing only) restates the proposals as committee rules; (X3, X5) India's reservations as an overlapping-group problem |
| Several dimensions | biproportional and parity apportionment | **(X3, main novelty)** properties of nested state × category × gender quotas |
| India studies of reserved seats | reserved-seat shifts under population reapportionment (Carnegie 2019) | (X3) the same shift across all six formulas, plus the women's layer |
| Redistricting ensembles | ReCom, short bursts, VRA constraints | first ensemble study of India; (X4) reservation-constrained ensembles |
| India studies | effects of reservation; neutrality of 2008 | measures formula against lines in seats |

## 6. References

All entries except those marked † were checked by web search on 27 November 2026. Entries marked † are from memory or from existing project files and should be checked before submission.

**Course**
- A. D. Procaccia. Lecture 12: Committee Elections. CS 2380, Fall 2026. https://procaccia.info/courses/CS2380-F26/slides12.pdf

**Committee elections**
- † H. Aziz, M. Brill, V. Conitzer, E. Elkind, R. Freeman, T. Walsh. Justified representation in approval-based committee voting. *Social Choice and Welfare* 48(2), 2017. (Also cited in Lecture 12.)
- † L. Sánchez-Fernández, E. Elkind, M. Lackner, N. Fernández, J. A. Fisteus, P. Basanta Val, P. Skowron. Proportional justified representation. AAAI 2017.
- † D. Peters, P. Skowron. Proportionality and the limits of welfarism. ACM EC 2020.
- † M. Lackner, P. Skowron. *Multi-Winner Voting with Approval Preferences.* SpringerBriefs, 2023.
- † D. Peters. Proportionality and strategyproofness in multiwinner elections. AAMAS 2018. https://arxiv.org/abs/2104.08594 (found by search; authors and venue not confirmed)
- † P. Skowron. Proportionality degree of multiwinner rules. ACM EC 2021. https://arxiv.org/abs/1810.08799 (found by search; author and venue not confirmed)
- P. Becker, M. Greger, D. Peters. Core existence in approval-based committee elections with up to seven voter types. arXiv 2605.06194, 2026. https://arxiv.org/abs/2605.06194
- P. Becker, M. Greger, D. Peters. Existence of the core in approval-based committee elections. arXiv, 2026, as cited in Lecture 12. The title matches arXiv 2609.11912 (https://arxiv.org/abs/2609.11912); authors not confirmed.

**Committee elections as apportionment**
- M. Brill, J.-F. Laslier, P. Skowron. Multiwinner approval rules as apportionment methods. *Journal of Theoretical Politics* 30(3):358–382, 2018. https://arxiv.org/abs/1611.08691
- M. Brill, P. Gölz, D. Peters, U. Schmidt-Kraepelin, K. Wilker. Approval-based apportionment. AAAI 2020, 1854–1861; *Mathematical Programming* (2022). https://arxiv.org/abs/1911.08365
- T. Delemazure, T. Demeulemeester, M. Eberl, J. Israel, P. Lederer. Strategyproofness and proportionality in party-approval multiwinner elections. AAAI 2023, 5591–5599. https://arxiv.org/abs/2211.13567

**Several dimensions and constraints**
- M. Balinski, G. Demange. An axiomatic approach to proportionality between matrices. *Mathematics of Operations Research* 14(4):700–719, 1989. https://pubsonline.informs.org/doi/10.1287/moor.14.4.700
- J. Lang, P. Skowron. Multi-attribute proportional representation. *Artificial Intelligence* 263:74–106, 2018. https://arxiv.org/abs/1509.03389
- C. Mathieu, V. Verdugo. Apportionment with parity constraints. *Mathematical Programming*, 2022. https://arxiv.org/abs/2108.04137
- J. Cembrano, J. Correa, G. Díaz, V. Verdugo. Proportionality in multiple dimensions to design electoral systems. *Social Choice and Welfare*, 2025. https://arxiv.org/abs/2410.03304
- R. Bredereck, P. Faliszewski, A. Igarashi, M. Lackner, P. Skowron. Multiwinner elections with diversity constraints. AAAI 2018, 933–940. https://arxiv.org/abs/1711.06527
- L. E. Celis, L. Huang, N. K. Vishnoi. Multiwinner voting with fairness constraints. IJCAI 2018, 144–151. https://arxiv.org/abs/1710.10057
- † B. Flanigan, P. Gölz, A. Gupta, B. Hennig, A. D. Procaccia. Fair algorithms for selecting citizens' assemblies. *Nature* 596, 2021.

**Classical apportionment**
- † M. L. Balinski, H. P. Young. *Fair Representation.* Brookings, 2nd ed., 2001.
- † F. Pukelsheim. *Proportional Representation: Apportionment Methods and Their Applications.* Springer, 2nd ed., 2017.
- † L. S. Penrose. The elementary statistics of majority voting. *JRSS* 109(1), 1946.
- † G. R. Grimmett. European apportionment via the Cambridge Compromise. *Mathematical Social Sciences* 63(2), 2012.

**Redistricting**
- † D. DeFord, M. Duchin, J. Solomon. Recombination: a family of Markov chains for redistricting. *Harvard Data Science Review*, 2021. https://arxiv.org/abs/1911.05725
- † S. Cannon, A. Goldbloom-Helzner, V. Gupta, J. N. Matthews, B. Suwal. Voter identification and optimization by short bursts. https://arxiv.org/abs/2011.02288
- A. Becker, M. Duchin, D. Gold, S. Hirsch. Computational redistricting and the Voting Rights Act. *Election Law Journal* 20(4):407–441, 2021.

**India**
- L. Iyer, C. Weir, S. L. Ostermann. Redrawing the lines: did political incumbents influence electoral redistricting in India? Working paper, February 2026. https://sites.nd.edu/lakshmi-iyer/files/2026/03/IWO_Political-Influence_Feb2026_Full.pdf
- † M. Vaishnav, J. Hintson. India's emerging crisis of representation. Carnegie Endowment for International Peace, March 2019. https://carnegieendowment.org/research/2019/03/indias-emerging-crisis-of-representation (page found by search; authors not confirmed)
- F. R. Jensenius. *Social Justice through Inclusion: The Consequences of Electoral Quotas in India.* Oxford University Press, 2017.
- † R. Pande. Can mandated political representation increase policy influence for disadvantaged minorities? Theory and evidence from India. *American Economic Review* 93(4), 2003.
- † R. Chattopadhyay, E. Duflo. Women as policy makers: evidence from a randomized policy experiment in India. *Econometrica* 72(5), 2004.
