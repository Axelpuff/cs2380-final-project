# Theory: the candidate seat rules, their background, and what they do in India

The simulation compares seat rules by what they do to party seat counts. This section looks at each rule on its own terms. For every method we first give its **background**: where the idea comes from, where it is used, and what is known about it. We then **apply it to India**: who has proposed it, what we can prove about it, and what it does with Indian data.

Everything here is about the **allocation between states**; nothing depends on how lines are drawn inside a state.

Numbers marked *Computed* come from the data in `analysis/apportion.py`: 2026 projected populations, all 36 states and union territories, and quota shares before rounding. The south means Andhra Pradesh, Karnataka, Kerala, Tamil Nadu, Telangana and Puducherry.

> **TODO (group):** decide whether the paper uses 2026 projected populations throughout, and whether union territories are included (they are below).

---

## 0. Model and properties

There are $n$ units (states and union territories), $N=\lbrace 1,\dots,n\rbrace$; in our data $n=36$. Unit $i$ currently holds $c_i$ seats, with $H_0=\sum_i c_i=543$. Its population is $p_i$ today, $p_i^{71}$ at the 1971 census and $p_i^{21}$ in 2021. Write $P=\sum_i p_i$ and $\pi_i=p_i/P$ for the population share, and $g_i\ge 0$ with $\sum_i g_i=1$ for unit $i$'s share of national GDP.

A **rule** takes this data and a House size $H\ge H_0$ and returns seats $s(H)\in\mathbb{Z}_{\ge 0}^n$ with $\sum_i s_i(H)=H$. Most rules below are **weight rules**: compute weights $w_i>0$, then round. The **quota** of unit $i$ is $q_i=Hw_i/\sum_j w_j$. For a region $R\subseteq N$, $Q_R=\sum_{i\in R}q_i/H$ is its quota share.

**Definition (properties).** A rule satisfies

- **(a) house monotonicity** if $s_i(H+1)\ge s_i(H)$ for every $i$ and $H$, i.e. no state loses a seat when the House grows;
- **(b) population monotonicity** if, whenever populations change from $p$ to $p'$ at fixed $H$ with $p'_i/p'_j>p_i/p_j$, it is not the case that $i$ loses seats while $j$ gains;
- **(c) exactness** ("one person, one vote") if whenever every $H\pi_i$ is an integer, $s_i=H\pi_i$ for all $i$;
- **(d) restoration** for a region $R$ if $Q_R\ge\sum_{i\in R}c_i/H_0$, i.e. the region keeps at least its current share.

## 1. Rounding: Webster's method

### Background

Every rule produces fractional quotas, and seats are whole numbers, so a rounding method is needed. This is the classic apportionment problem from the US House. Daniel Webster proposed his method in 1832, and the US used it after the 1840, 1910 and 1930 censuses. André Sainte-Laguë rediscovered it in 1910 for allocating seats to parties, and under his name it is used today in Germany, New Zealand, Norway and Sweden.

The method picks a divisor $d$ and rounds every $w_i/d$ to the nearest integer, adjusting $d$ until the seats add up to $H$:

$$\mathrm{Web}(w,H)_i=\left[\,w_i/d\,\right],\qquad \textstyle\sum_i [w_i/d]=H.$$

Equivalently, it hands out seats one at a time, each to the unit with the largest priority $w_i/(s_i+\tfrac12)$.

Balinski and Young's theory of apportionment gives three facts we use throughout:

1. Webster's method, like every divisor method, is house monotone and population monotone **as long as the weights do not depend on $H$**.
2. Divisor methods are exactly the population-monotone methods.
3. No method is both population monotone and always within one seat of quota.

Among divisor methods, Webster's is the one that is unbiased between large and small states.

### Applying it to India

The Constitution says seats should be allotted so that the ratio of seats to population is the same for every state "so far as practicable" (Article 81), but it names no rounding method. We use Webster for every rule, because it is unbiased and because property 1 lets us separate the effect of a formula from the effect of rounding. Rounding usually moves each state by less than one seat, so the results below are stated for quotas.

## 2. The freeze and the flat scale-up

### Background

The 42nd Amendment of 1976, passed during the Emergency, froze the allocation of Lok Sabha seats among states at the 1971 census. The stated purpose was family planning: states that controlled their population should not lose seats for it. The 84th Amendment of 2001 extended the freeze until the first census after 2026. The 2008 delimitation redrew constituency boundaries inside states using the 2001 census but did not move seats between states.

A "flat scale-up" keeps the frozen shares and simply enlarges the House: every state's seats grow by the same percentage. In weight-rule terms both are $w_i=c_i$.

### Applying it to India

In 2026 the government's ministers described their plan as a uniform 50% increase for every state, but the bill itself allocated seats by population (Section 3). The flat scale-up is the government's verbal assurance turned into a formula.

With fixed weights $c$, the flat scale-up is house monotone (Section 1). It keeps every regional share exactly where it is, so it trivially satisfies restoration for the south. But it fails exactness as badly as the current House does.

*Computed.* The south keeps 23.94% of seats under the freeze and the flat scale-up, against 19.45% of the 2026 population.

## 3. Population (the 2026 bill)

### Background

Proportional representation of states by population is the default in federations. It is required for the US House, and it is the principle of India's Article 81. Its weakness is that a state's representation depends only on its current headcount. The 1976 framers saw this as a disincentive for family planning.

### Applying it to India

The Constitution (131st Amendment) Bill, introduced in April 2026, removed the freeze, gave each state seats in proportion to its population, and raised the maximum size of the Lok Sabha from 550 to 850. It was based on the 2011 census and failed in Parliament. In our notation it is $w_i=p_i$, the only rule here that satisfies exactness.

The southern objection can be stated as a theorem.

**Observation 1.** Let a rule depend only on current populations and be population monotone. If one unit's population is lower (others unchanged, $H$ fixed), that unit cannot have more seats.

*Proof.* Suppose $p'_i<p_i$, $p'_j=p_j$ for $j\ne i$, and $s'_i>s_i$. Since $\sum s'=\sum s=H$, some $j$ has $s'_j<s_j$. But $p'_j/p'_i>p_j/p_i$, so $j$'s relative population rose while $j$ lost and $i$ gained, contradicting population monotonicity. $\square$

So under the bill, and under every other monotone rule that looks only at today's census, a state that slowed its growth is never better off. Such a rule can at most soften the penalty. The degressive rule (Section 5) softens it for all growth alike. The fertility window (Section 4) softens it only for growth during a chosen period, and to do that it has to use past census data.

*Computed.* The south's quota share falls from 23.94% today to 19.45%.

## 4. The fertility window (new)

### Background

Rewarding states for lowering fertility already has a precedent in Indian fiscal federalism. The Finance Commission divides central tax revenue among states by a formula. Until the 14th Commission (2015–20), that formula used 1971 population at a weight of 17.5%. The 15th Commission (2020–26) was told to use 2011 population, and to compensate it added a **demographic performance** criterion worth 12.5%. This criterion is the reciprocal of each state's total fertility rate, scaled by its 1971 population, so states with lower fertility score higher.

The same argument recurs in the delimitation debate. Telangana's Chief Minister argued in April 2026 that a purely population-based reallocation would punish states that implemented family planning.

### Applying it to India

No one has proposed a seat formula of this kind, so this rule is ours. It discounts exactly the growth that happened during the population-control era. Growth during 1971–2021 counts at weight $\lambda\in[0,1]$, while the 1971 base and growth after 2021 count in full:

$$w_i(\lambda)=p_i^{71}+\lambda\,(p_i^{21}-p_i^{71})+(p_i-p_i^{21}).$$

At $\lambda=1$ it is the bill. The window ends in 2021 because national fertility reached replacement level around then.

> **TODO (group):** confirm the end year and the default $\lambda=0.5$, which the simulation also uses.

**Proposition 2.** Write $a_i=p_i^{71}+(p_i-p_i^{21})$ and $b_i=p_i^{21}-p_i^{71}$, so $w_i(\lambda)=a_i+\lambda b_i$, and let $A=\sum_i a_i$, $B=\sum_i b_i$. For every region $R$ (in particular every single unit), the quota share $Q_R(\lambda)$ is monotone in $\lambda$: increasing if $b_R/a_R>B/A$ and decreasing if $b_R/a_R<B/A$, where $a_R=\sum_{i\in R}a_i$ and $b_R=\sum_{i\in R}b_i$.

*Proof.* $Q_R(\lambda)=(a_R+\lambda b_R)/(A+\lambda B)$, so

$$Q_R'(\lambda)=\frac{b_R(A+\lambda B)-B(a_R+\lambda b_R)}{(A+\lambda B)^2}=\frac{b_RA-a_RB}{(A+\lambda B)^2},$$

whose numerator does not depend on $\lambda$ and whose denominator is positive. $\square$

**Corollary 3.** If there is no growth after the window ($p=p^{21}$), unit $i$ gains as $\lambda$ rises exactly when its 1971–2021 growth factor $p_i^{21}/p_i^{71}$ exceeds the national factor.

The weights do not depend on $H$, so the rule is also house monotone.

*Computed.*
- The national growth factor for 1971–2021 is 2.48. Every southern state except Puducherry grew more slowly.
- With 2026 populations the condition in Proposition 2 still holds for the south as a region. Its quota share falls monotonically from 23.24% at $\lambda=0$ to 19.45% at $\lambda=1$ (20.58% at $\lambda=0.5$).
- No state's share ever reverses direction along the way.

So $\lambda$ is a **one-dimensional compromise in which every state knows which way it wants the dial turned**, much like the Finance Commission's 12.5% weight. But even $\lambda=0$ does not restore the south (23.24% against 23.94%), because growth after 2021 still counts in full.

## 5. Degressive proportionality (Tharoor)

### Background

Degressive proportionality means larger units get more seats, but fewer seats per person. It is the treaty rule for the European Parliament. Article 14(2) of the Treaty on European Union requires representation to be degressively proportional, with at least 6 and at most 96 seats per member state.

The treaty does not fix a formula, and mathematicians have proposed several. The best known is the Cambridge Compromise of 2011, which gives each state 5 base seats plus seats in proportion to population, capped at 96. That is a floor rule (Section 6). Power laws $w_i=p_i^\alpha$, which give a smooth version, have also been studied for the Parliament.

A related classical result is Penrose's square-root law (1946). Suppose each state's delegation votes as a single bloc and citizens vote independently at random. Then giving state $i$ voting weight proportional to $\sqrt{p_i}$ makes every citizen's Banzhaf power roughly equal. The Jagiellonian Compromise proposed this for voting in the EU Council.

### Applying it to India

In April 2026 Shashi Tharoor proposed degressive proportionality for the Lok Sabha, citing the European Parliament. His proposal let the number of citizens per MP rise with a state's population. He gave no formula, only two examples: a state of 30 million at 1 million people per MP and a state of 200 million at 2.5 million per MP. A power law through both examples has $\alpha=\ln(80/30)/\ln(200/30)\approx 0.517$, so we study $D_\alpha$ with $w_i=p_i^\alpha$. $D_1$ is the bill, and $D_0$ gives every unit the same weight, as in the US Senate.

**Proposition 4.** Under $D_\alpha$ with not all populations equal, let $\ell_i=\ln p_i$, $x_i=p_i^\alpha/\sum_k p_k^\alpha$ (unit $i$'s quota share) and $\mu(\alpha)=\sum_j x_j\ell_j$ (the quota-weighted mean log population). Then:

1. $\frac{d}{d\alpha}\ln x_i=\ell_i-\mu(\alpha)$, and $\mu$ is strictly increasing;
2. each unit's quota share is single-peaked in $\alpha$: it rises while $p_i>e^{\mu(\alpha)}$ and falls afterwards;
3. the largest unit's share is strictly increasing and the smallest unit's is strictly decreasing.

*Proof.* $\ln x_i=\alpha\ell_i-\ln\sum_k e^{\alpha\ell_k}$, so $\frac{d}{d\alpha}\ln x_i=\ell_i-\sum_k x_k\ell_k=\ell_i-\mu$. Using $x_j'=x_j(\ell_j-\mu)$,

$$\mu'=\sum_j x_j'\ell_j=\sum_j x_j\ell_j^2-\mu^2=\mathrm{Var}_x(\ell)>0,$$

strict because every $x_j>0$ and the $\ell_j$ are not all equal. So $\ell_i-\mu(\alpha)$ is strictly decreasing and changes sign at most once, from positive to negative; that is (2). For (3), $\mu$ is a weighted average with positive weight on every unit, so $\ell_{\min}<\mu<\ell_{\max}$ for all $\alpha$. $\square$

Single units behave simply, but regions need not. For a region, $\frac{d}{d\alpha}Q_R=Q_R(\mu_R-\mu)$, where $\mu_R$ is the mean log population within $R$. Both means move with $\alpha$, so the sign can flip. Unlike the fertility window, this dial does not tell every region which way to turn it.

*Computed.*
- The south's quota share is 16.7% at $\alpha=0$, peaks at 21.16% at $\alpha\approx 0.558$, and falls to 19.45% at $\alpha=1$.
- Tharoor's fitted $\alpha=0.517$ gives the south 21.14%, almost exactly at the south-maximising exponent.
- Even so, no $\alpha$ restores the south, and it is not true that "more degressive" always means "better for the south." Degressive rules mainly help the Northeast and the union territories, whose combined share rises from 4.0% at $\alpha=1$ to 10.9% at $\alpha=0.517$, mostly at the expense of the Hindi belt (48.8% to 41.6%).

**Remark (does Penrose apply?).** Tharoor's exponent is close to Penrose's $\tfrac12$, but the justification does not carry over directly. Penrose assumes each state's delegation votes as a bloc. Lok Sabha MPs vote by party, not by state, and the anti-defection law (Tenth Schedule) enforces party discipline.

> **TODO (group):** decide whether to compute Banzhaf power for party blocs, which would connect to the class material on weighted voting.

## 6. Floor plus proportional

### Background

Guaranteed minimums are the most common departure from strict proportionality. The US Constitution gives every state at least one representative. Brazil's Chamber of Deputies gives every state between 8 and 70 seats; the floor helps many small states, and the cap binds only São Paulo. The Cambridge Compromise for the European Parliament is base-plus-proportional with 5 base seats. India already has a version: states under 6 million people are exempt from strict proportionality (Article 81), and every small state and union territory has at least one seat.

### Applying it to India

We study the clean version: every unit gets $f$ seats, and the remaining $H-nf$ go by population, so $q_i=f+(H-nf)\pi_i$ for $0\le f\le H/n$. It is natural to ask how large a floor would need to be to keep today's north–south balance.

**Proposition 5.** Under $L_f$ with $\theta=nf/H\in[0,1]$, every region's quota share is

$$Q_R=\theta\,\frac{\lvert R\rvert}{n}+(1-\theta)\,\pi_R,\qquad \pi_R=\sum_{i\in R}\pi_i.$$

In particular $Q_R$ lies between $\pi_R$ and $\lvert R\rvert/n$, and no floor restores a region whose current seat share exceeds both.

*Proof.* $Q_R=\frac1H\sum_{i\in R}\bigl(f+(H-nf)\pi_i\bigr)=\frac{\lvert R\rvert f}{H}+\bigl(1-\frac{nf}{H}\bigr)\pi_R$, and $\lvert R\rvert f/H=\theta\lvert R\rvert/n$. $\square$

With fixed $f$, $L_f$ is $f$ plus Webster on fixed weights $p$ for the remaining seats, so it is house monotone.

*Computed.*
- The south has 6 of 36 units (16.7%), 19.45% of the 2026 population and 23.94% of current seats. Both bounds are below its current share, so **no floor restores the south; every floor lowers its share**.
- At $H=816$, a floor of 10 seats gives the south 18.2%.
- Floors help regions with many small units, here the Northeast and the union territories, not regions of large, slow-growing states. The answer to our question is that no floor size works.

## 7. The hybrid rule (Reddy)

### Background

Weighting representation by economic contribution has no modern precedent in a lower house. Its critics in India made the same point: the Union Minister G. Kishan Reddy said no such model exists anywhere in the world, and the BRS called it unconstitutional. The closest Indian analogue runs in the opposite direction. The Finance Commission gives poorer states more revenue through its "income distance" criterion (45% of the formula).

The mathematical background here is the **Alabama paradox**. After the 1880 census, the US House was apportioned with Hamilton's method. Calculations showed that enlarging the House from 299 to 300 seats would have cut Alabama's seats from 8 to 7. Divisor methods with fixed weights never do this (Section 1). The question is whether a rule whose weights change with the House size can.

### Applying it to India

In April 2026 Telangana's Chief Minister A. Revanth Reddy proposed a "hybrid" model: half of the new seats allocated pro rata and half by states' contribution to GDP. Press reports differ on whether "pro rata" means current seats or population. We read it as current seats, since the government's own plan was a pro-rata 50% increase. Earlier, in 2025, he had asked that the five southern states' share rise from about 24% to 33%, in line with their GDP contribution.

Formally, every unit keeps $c_i$. With $m_i=\tfrac12 c_i/H_0+\tfrac12 g_i$, the targets are $t_i(H)=c_i+(H-H_0)m_i$, which sum to $H$. $R(H)$ is Webster's method started from the floors: begin at $s=c$ and give each new seat to the unit with the largest $t_i(H)/(s_i+\tfrac12)$. Unlike every other rule here, the weights $t(H)$ depend on $H$.

> **TODO (group):** settle the reading of "pro rata" and state it in the paper.

**Proposition 6.** The hybrid rule $R$ is not house monotone.

*Proof.* Take three units with $c=(1,1,2)$, so $H_0=4$, and $g=(\tfrac25,\tfrac12,\tfrac1{10})$. Then $m=(\tfrac{13}{40},\tfrac{15}{40},\tfrac{12}{40})$.

- $H=5$: $t=(1.325,\,1.375,\,2.3)$. From the floors $(1,1,2)$, the one new seat goes to the largest of 0.883, 0.917 and 0.920, so unit 3 wins and $s(5)=(1,1,3)$.
- $H=6$: $t=(1.65,\,1.75,\,2.6)$. From $(1,1,2)$ the priorities are 1.10, 1.17 and 1.04, so unit 2 gets a seat (its priority drops to 0.70), then unit 1. So $s(6)=(2,2,2)$.

Unit 3 drops from 3 seats to 2 when the House grows. $\square$

The cause is that the weights depend on $H$. Unit 3 has a large current share but a small GDP share, so its target share $t_3(H)/H$ falls as the House grows ($0.46\to 0.43$). Units just below a rounding threshold then overtake it.

**Lemma 7.** If $g_i=c_i/H_0$ for all $i$, then $R$ is house monotone.

*Proof.* Then $t_i(H)=c_iH/H_0$, a positive multiple of $c$, and Webster's priorities depend on the weights only up to scale. So $R$ is Webster with the fixed weights $c$, started from $c$. Webster with weights $c$ and House $H_0$ gives exactly $c$, because all quotas are integers. Webster run one seat at a time is house monotone, so continuing from $c$ produces $\mathrm{Web}(c,H)$ for every $H\ge H_0$, and the sequence is house monotone. $\square$

So the paradox comes precisely from GDP shares differing from seat shares, which is the whole point of the proposal. The fix is to round only the new seats.

**Proposition 8.** The **incremental hybrid** $R'(H)=c+\mathrm{Web}(m,H-H_0)$ is house monotone, gives every unit at least $c_i$, and has the same targets $t_i(H)=c_i+(H-H_0)m_i$ as $R$.

*Proof.* The weights $m$ do not depend on $H$, so $\mathrm{Web}(m,\cdot)$ is house monotone, and adding the constant vector $c$ preserves this. The floor holds because Webster's output is nonnegative. The quota of the new seats is $(H-H_0)m_i$. $\square$

*Computed.*
- **The paradox happens in the real data.** With 2026 projections, Bihar has 44 seats at $H=607$ and 43 at $H=608$.
- **The fix costs almost nothing.** $R'$ gives exactly the same allocation as $R$ at $H=816$. Over $H\in[543,850]$ at most two seats ever move between units relative to $R$, and $R'$ never violates house monotonicity. In the toy instance, $R'$ gives $(1,2,2)$ then $(2,2,2)$.
- **The south's share.**
  - The south's share of 2022–23 GDP in our data is 30.2%. (The BRS leader K. T. Rama Rao used a figure of 36% when arguing that seat shares should match GDP shares.)
  - The hybrid gives the south 24.99% at $H=816$, the only rule here other than the freeze that restores its share.
  - It falls well short of Reddy's 33% target. Even if *all* new seats went by GDP, the south would get only 26.0% at $H=816$, approaching 30.2% only as the House grows without bound.

## 8. Summary

| Rule | Proposed by | House monotone | Exact | Penalises slower growth | South quota share ($H=816$) |
|---|---|---|---|---|---|
| Freeze / flat scale-up | 1976 freeze; government's verbal assurance | yes | no | no | 23.94% |
| Population | 2026 bill | yes | yes | yes | 19.45% |
| Fertility window $F_{0.5}$ | new here | yes | no | less (window growth $\times\lambda$) | 20.58% |
| Degressive $D_{0.517}$ | Tharoor | yes | no | less (elasticity $\alpha$) | 21.14% |
| Floor $L_{10}$ | (US, Brazil, Cambridge Compromise) | yes | no | yes | 18.22% |
| Hybrid $R$ | Revanth Reddy | **no** | no | no (ignores population) | 24.99% |
| Incremental hybrid $R'$ | fix proposed here | yes | no | no (ignores population) | 24.99% |

Shares are quota shares before rounding, with 2026 projected populations; the south's current share is 23.94%.

Two conclusions follow. First, every rule built on population, including the two designed as compromises ($F_\lambda$ and $D_\alpha$), leaves the south below its current share for every parameter value, and floors make it worse. Only rules anchored on current seats or GDP restore it. Second, the one popular proposal that does restore the south, Reddy's hybrid, has an Alabama paradox as naturally written, and a one-line change removes it.

> **TODO (group):** link to the simulation: the formula differences above matter less for party seats than line-drawing does.

## References

**Apportionment theory**
- M. L. Balinski and H. P. Young. *Fair Representation: Meeting the Ideal of One Man, One Vote*. Brookings Institution Press, 2nd ed., 2001.
- L. S. Penrose. The elementary statistics of majority voting. *Journal of the Royal Statistical Society* 109(1):53–57, 1946.
- G. R. Grimmett. European apportionment via the Cambridge Compromise. *Mathematical Social Sciences* 63(2):68–73, 2012. https://arxiv.org/abs/1105.4294
- F. Pukelsheim and G. R. Grimmett, on methods for apportioning the European Parliament (2018): https://www.math.uni-augsburg.de/htdocs/emeriti/pukelsheim/2018b.pdf

**Indian law and policy**
- PRS Legislative Research, The Delimitation Bill, 2026: https://prsindia.org/billtrack/the-delimitation-bill-2026
- PRS, Implications of increasing the size of the Lok Sabha: https://prsindia.org/articles-by-prs-team/implications-of-increasing-the-size-of-the-lok-sabha
- PRS, Report of the 15th Finance Commission for 2021–26: https://prsindia.org/policy/report-summaries/report-15th-finance-commission-2021-26
- Business Standard, history of delimitation and the 1976 freeze: https://www.business-standard.com/india-news/delimitation-india-history-population-north-south-2026-census-126041500914_1.html

**Proposals**
- Reddy's hybrid model: https://www.siasat.com/delimitation-telangana-cm-proposes-hybrid-model-for-increasing-ls-seats-3452163/ and https://deccanchronicle.com/southern-states/telangana/revanth-reddy-seeks-delimitation-based-on-2026-census-1950191
- Reddy's 33% demand (2025): https://www.business-standard.com/politics/southern-states-reject-population-formula-seek-gdp-based-representation-125032300788_1.html
- Criticism of the hybrid model: https://deccanchronicle.com/southern-states/telangana/kishan-reddy-slams-revanths-hybrid-delimitation-ploy-as-global-nonsense-1950464
- Tharoor on degressive proportionality: https://telanganatoday.com/shashi-tharoor-suggests-degressive-proportionality-for-lok-sabha-delimitation and https://www.siasat.com/consult-states-before-delimitation-says-shashi-tharoor-to-pm-3453246/

**Other countries**
- EU composition decision, 2023: https://eur-lex.europa.eu/eli/dec/2023/2061/oj
- Brazil's Chamber of Deputies apportionment: https://aceproject.org/ace-en/topics/es/annex/esy/esy_br
