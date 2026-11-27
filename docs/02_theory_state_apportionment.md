# Theory: the seat rules, the math behind them, and what they do in India

*Read after: [01 project origin](01_project_origin.md). Leads to: [03 committee bridge](03_committee_bridge.md).*

This section has two parts.

- **Part A** sets out the mathematical framework from the course: the apportionment model, the methods, the properties and the theorems, using the lecture definitions and notation. A few extensions we need that are *not* in the lectures are marked **(ours)**.
- **Part B** takes each seat rule in the Indian debate. It first gives the rule's mathematics in the Part A framework (definition, which properties it satisfies, proofs), then applies it to India.

**Sources for the definitions.** These are the CS 2380 Fall 2026 lectures by Procaccia: [Lecture 15, The Electoral College](https://procaccia.info/courses/CS2380-F26/slides15.pdf), [Lecture 16, Apportionment in the 19th Century](https://procaccia.info/courses/CS2380-F26/slides16.pdf) and [Lecture 17, Apportionment in the 20th Century](https://procaccia.info/courses/CS2380-F26/slides17.pdf). Each item in Part A says which lecture it comes from.

Numbers marked *Computed* come from `analysis/apportion.py`: 2026 projected populations, all 36 states and union territories. The south means Andhra Pradesh, Karnataka, Kerala, Tamil Nadu, Telangana and Puducherry.

---

# Part A. The framework

## A.1 The model (Lectures 16–17)

- A set of states $`N=\lbrace 1,\dots,n\rbrace`$ and $`K`$ seats to be allocated.
- State $`i`$ has population $`p_i`$, and the total population is $`P=\sum_{i=1}^n p_i`$.
- The **standard quota** of state $`i`$ is $`q_i=\dfrac{p_i}{P}\cdot K`$: the number of seats it would get if seats could be fractional.
- The **upper quota** of $`i`$ is $`\lceil q_i\rceil`$ and the **lower quota** is $`\lfloor q_i\rfloor`$.
- $`k_i`$ is the number of seats allocated to $`i`$, with $`\sum_i k_i=K`$.

The problem is that standard quotas are fractional, and simply rounding each one to the nearest integer may not add up to $`K`$. The lecture's example has quotas $`50.6,\,30.7,\,18.7`$, which round to $`51+31+19=101\ne 100`$. An **apportionment method** is a rule for choosing integers $`k_i`$ that do add up to $`K`$.

## A.2 Hamilton's method (Lecture 16)

Give each state its lower quota $`\lfloor q_i\rfloor`$. Let $`r_i=q_i-\lfloor q_i\rfloor`$ be its residue, and hand out the remaining $`K-\sum_i\lfloor q_i\rfloor`$ seats one at a time to the states with the largest residues.

Hamilton's method is the obvious one, and Congress adopted an identical method in 1850. But it has paradoxes (A.4). The lecture's example has populations $`(6,6,2)`$. At $`K=10`$ the quotas are $`(4.29,4.29,1.43)`$ and Hamilton gives $`(4,4,2)`$. At $`K=11`$ the quotas are $`(4.71,4.71,1.57)`$ and Hamilton gives $`(5,5,1)`$, so state 3 loses a seat when the House grows. We do not use Hamilton for any rule. It matters here because the hybrid rule in Section B.6 has the same paradox.

## A.3 Divisor methods (Lectures 16–17)

Choose a divisor $`D`$ and compute each state's **modified quota** $`p_i/D`$. Fix a rounding function $`f`$ with two properties:

1. $`f(x)=x`$ whenever $`x`$ is an integer;
2. $`f(x)\ge f(y)`$ whenever $`x\ge y`$.

Choose $`D`$ so that $`\sum_i f(p_i/D)=K`$, and set $`k_i=f(p_i/D)`$. Different rounding functions give the classical methods:

| Method | Rounding $`f(x)`$ | Lecture's notes |
|---|---|---|
| Jefferson | $`\lfloor x\rfloor`$ | favours large states; used by Congress until 1830 |
| Adams | $`\lceil x\rceil`$ | favours small states; never adopted |
| **Webster** | $`[x]`$, ordinary rounding (round up at $`\lfloor x\rfloor+\tfrac12`$) | unbiased; adopted by Congress in 1842 |
| Huntington–Hill | round up iff $`x\ge\sqrt{\lfloor x\rfloor\lceil x\rceil}`$ | rounds at the geometric mean; slightly favours small states |

**Well-definedness (Lectures 16–17).** If two divisors $`D\le D'`$ both give totals of $`K`$, they give the same allocation. A smaller divisor gives every state at least as many seats, and both allocations sum to $`K`$.

**Sequential form (standard).** A divisor method can equivalently be run one seat at a time. Starting from zero seats, each new seat goes to the state with the largest priority $`p_i/d(k_i)`$, where $`d(k)`$ is the point at which $`f`$ rounds up to $`k+1`$. For Webster $`d(k)=k+\tfrac12`$, so the priority is $`p_i/(k_i+\tfrac12)`$. We use this form for computations and proofs.

**Example (Webster).** Take three states with populations $`150, 320, 530`$ and $`K=10`$. With $`D=100`$ the modified quotas are $`1.5, 3.2, 5.3`$, which round to $`2+3+5=10`$. So $`k=(2,3,5)`$. (Jefferson's method gives $`(1,3,6)`$ on the same data.)

## A.4 Properties (Lectures 16–17)

**House monotonicity.** A method is house monotonic if $`K'>K`$, with all other variables unchanged, implies $`k_i'\ge k_i`$ for all $`i\in N`$. A violation is the **Alabama paradox**: a state loses a seat when the House grows. It was discovered in 1880, when Alabama would have dropped from 8 to 7 seats as the House went from 299 to 300 under Hamilton's method.

**Population monotonicity.** Take two censuses with populations $`p_i`$ and $`p_i'`$ and apportionments $`k_i`$ and $`k_i'`$; the house sizes $`K`$ and $`K'`$ may differ. A method is population monotonic if $`k_i<k_i'`$ and $`k_j>k_j'`$ together imply $`p_i<p_i'`$ or $`p_j>p_j'`$. In words, if $`i`$ gains seats and $`j`$ loses seats, then $`i`$'s population grew or $`j`$'s shrank. A violation is the **population paradox**.

**Quota criterion.** A method satisfies quota if $`\lfloor q_i\rfloor\le k_i\le\lceil q_i\rceil`$ for all $`i`$, i.e. every state is within one seat of its standard quota.

**Neutrality.** A method is neutral if permuting the states permutes the allocation in the same way.

## A.5 Theorems (Lecture 17)

**Theorem A1.** All divisor methods are population monotonic.

*Proof (lecture).* If $`i`$ gains seats, its modified quota rose: $`p_i/D<p_i'/D'`$. If $`j`$ loses seats, its modified quota fell: $`p_j/D>p_j'/D'`$. So $`p_i'>(D'/D)p_i`$ and $`p_j'<(D'/D)p_j`$. If $`D'/D\le 1`$ then $`p_j'<p_j`$; if $`D'/D\ge 1`$ then $`p_i'>p_i`$. $`\square`$

**Theorem A2.** Any population monotonic method is house monotonic.

*Proof (lecture).* Suppose $`K'>K`$ with populations unchanged. Some state $`j`$ must gain, $`k_j'>k_j`$. If some $`i`$ lost, $`k_i'<k_i`$, population monotonicity would force $`p_j<p_j'`$ or $`p_i>p_i'`$, but populations did not change. $`\square`$

**Corollary A3.** All divisor methods are house monotonic.

**Theorem A4 (impossibility; due to Balinski and Young).** No apportionment method is neutral, population monotonic and satisfies the quota criterion.

**Corollary A5.** No divisor method satisfies the quota criterion on every instance.

So Webster's method never has the Alabama or population paradoxes, but it can occasionally give a state more than one seat away from its quota. Hamilton's method satisfies quota but has both paradoxes.

## A.6 Weighted voting and the Banzhaf index (Lecture 15)

We need this for the Penrose argument in B.4.

- A **simple cooperative game** is $`(N,v)`$ with players $`N=\lbrace 1,\dots,n\rbrace`$, $`n\ge 2`$, and $`v:2^N\to\lbrace 0,1\rbrace`$ monotone: if $`v(S)=1`$ and $`S\subseteq T`$ then $`v(T)=1`$. Coalition $`S`$ is winning if $`v(S)=1`$.
- A **weighted voting game** has a quota $`q`$ and weights $`w_i\in\mathbb{N}\cup\lbrace 0\rbrace`$ for all $`i\in N`$, with $`v(S)=1`$ iff $`\sum_{i\in S}w_i\ge q`$. Computing $`\beta_i`$ in a weighted voting game is #P-complete, but it can be estimated by sampling coalitions.
- The **Banzhaf power index** of player $`i`$ is

```math
\beta_i=\frac{1}{2^{n-1}}\sum_{S\subseteq N\setminus\lbrace i\rbrace}\bigl[v(S\cup\lbrace i\rbrace)-v(S)\bigr],
```

  the probability that $`i`$ is pivotal when the other players join a coalition independently with probability $`\tfrac12`$.
- **Pivotal voter in a state.** If each of a state's $`p=2k+1`$ voters votes for one of two alternatives independently and uniformly at random, a given voter breaks a tie with probability $`\binom{2k}{k}/2^{2k}\approx\sqrt{2/(\pi p)}`$ by Stirling's approximation.
- **Two-tier influence.** If a state's representatives vote as a bloc, a citizen affects the outcome with probability about $`\sqrt{2/(\pi p_i)}\cdot\beta_i`$, where $`\beta_i`$ is the state's Banzhaf index in the upper tier.

## A.7 Extensions we need (ours)

The lecture methods take only populations as input. Every rule in the Indian debate instead runs a divisor method on some other **weights**, so we generalise slightly.

**Definition (weight rule) (ours).** A weight rule computes a weight $`w_i>0`$ for each state from the data, then applies Webster's method with $`w_i`$ in place of $`p_i`$: choose $`D`$ with $`\sum_i[w_i/D]=K`$ and set $`k_i=[w_i/D]`$. Its **quota** is $`\tilde q_i=K w_i/\sum_j w_j`$, the quota with respect to its own weights. When we need the standard quota of A.1, computed from population, we write $`q_i`$.

**Lemma A6 (ours).** Suppose a weight rule's weights do not depend on $`K`$, and each $`w_i=\varphi_i(p_i)`$ is a strictly increasing function of state $`i`$'s own population; other data, such as past censuses, are held fixed. Then the rule is population monotonic and house monotonic.

*Proof.* Repeat the proof of Theorem A1 with $`w`$ in place of $`p`$. If $`i`$ gains and $`j`$ loses, then $`w_i'>w_i`$ or $`w_j'<w_j`$, so $`p_i'>p_i`$ or $`p_j'<p_j`$ because each $`\varphi_i`$ is strictly increasing. House monotonicity follows from Theorem A2. $`\square`$

If the weights do not depend on population at all, the same argument gives population monotonicity vacuously: the allocation never responds to population.

**Definition (region share, restoration) (ours).** For a set of states $`R\subseteq N`$ (a region), its quota share is $`Q_R=\sum_{i\in R}\tilde q_i/K`$. Let $`c_i`$ be current seats, with $`K_0=\sum_i c_i=543`$. A rule **restores** $`R`$ if $`Q_R\ge\sum_{i\in R}c_i/K_0`$, i.e. the region keeps at least its current share of seats.

**Observation A7 (ours, from the lecture's definition).** Let a rule depend only on current populations and be population monotonic. If one state's population is lower, with all other populations and $`K`$ unchanged, that state cannot have more seats.

*Proof.* Suppose $`p_i'<p_i`$, $`p_j'=p_j`$ for $`j\ne i`$, and $`k_i'>k_i`$. Since both allocations sum to $`K`$, some $`j`$ has $`k_j'<k_j`$. Then $`i`$ gains and $`j`$ loses, so population monotonicity requires $`p_i<p_i'`$ or $`p_j>p_j'`$. Neither holds. $`\square`$

This is the formal version of the southern complaint. Under any such rule, slowing your population growth can never win you seats.

---

# Part B. The rules

The rules are compared at $`K=816`$ (the House size the simulation uses; the bill's cap was 850) and, where it matters, over $`K\in[543,850]`$. Shares are quota shares before rounding, $`Q_R`$ in the notation of A.7.

## B.1 Freeze and flat scale-up

### The math

The weights are $`w_i=c_i`$, the current seats, so this is Webster's method on the vector $`c`$. At $`K=K_0`$ every quota $`\tilde q_i=c_i`$ is an integer and the rule returns $`c`$. For $`K>K_0`$ every state grows by the same proportion, up to rounding.

- **House monotonic:** yes. The weights are fixed, so Corollary A3 applies.
- **Population monotonic:** yes, vacuously. Populations never enter.
- **Quota criterion with respect to population:** no. Seats ignore population entirely.
- **Restoration:** every region keeps exactly its current share, by construction.

### In India

The 42nd Amendment of 1976 froze the allocation of seats among states at the 1971 census. It was explicitly a family-planning measure: states that controlled their population should not lose seats for it. The 84th Amendment of 2001 extended the freeze until the first census after 2026. Ministers described the 2026 plan as a uniform 50% increase for every state, which is this rule with $`K\approx 815`$.

*Computed.* At $`K=816`$ the flat scale-up puts 28 of 36 units outside $`[\lfloor q_i\rfloor,\lceil q_i\rceil]`$ of their population quota. For example, Bihar gets 60 seats against a quota of 75.8. The south keeps 23.94% of seats while holding 19.45% of the population.

## B.2 Population (the 2026 bill)

### The math

This is the lecture's model exactly: $`w_i=p_i`$, Webster's method.

- **House monotonic and population monotonic:** yes, by Theorem A1 and Corollary A3.
- **Quota criterion:** not guaranteed (Corollary A5), but on our data it holds. At $`K=816`$ every state is within one seat of its quota.
- **Slower growth:** penalised. Observation A7 applies directly.

Pure Webster gives zero seats to the smallest units. At $`K=816`$, Sikkim, the Andaman and Nicobar Islands, Ladakh and Lakshadweep have quotas below $`\tfrac12`$. The Constitution guarantees at least one seat, and the simulation keeps states under 6 million at their current seats. These floors are discussed in B.5.

### In India

Article 81 asks for the ratio of seats to population to be the same for every state "so far as practicable". The Constitution (131st Amendment) Bill of April 2026 would have restored that principle on 2011 census figures, with a cap of 850 seats. It failed in Parliament.

*Computed.* The south's share falls from 23.94% to 19.45%.

## B.3 The fertility window (new)

### The math

Growth during 1971–2021 counts at a weight $`\lambda\in[0,1]`$, while the 1971 base and growth after 2021 count in full:

```math
w_i(\lambda)=p_i^{71}+\lambda\,(p_i^{21}-p_i^{71})+(p_i-p_i^{21}).
```

At $`\lambda=1`$ this is the population rule. Holding $`p^{71}`$ and $`p^{21}`$ fixed, $`w_i`$ is strictly increasing in the current population $`p_i`$ and does not depend on $`K`$. So by Lemma A6 the rule is **house monotonic and population monotonic**.

The interesting question is how shares move as $`\lambda`$ changes.

**Proposition B1.** Write $`a_i=p_i^{71}+(p_i-p_i^{21})`$ and $`b_i=p_i^{21}-p_i^{71}`$, so $`w_i(\lambda)=a_i+\lambda b_i`$, and let $`A=\sum_i a_i`$, $`B=\sum_i b_i`$. For every region $`R`$ (in particular every single state), $`Q_R(\lambda)`$ is monotone in $`\lambda`$. It is increasing if $`b_R/a_R>B/A`$ and decreasing if $`b_R/a_R<B/A`$, where $`a_R=\sum_{i\in R}a_i`$ and $`b_R=\sum_{i\in R}b_i`$.

*Proof.* $`Q_R(\lambda)=(a_R+\lambda b_R)/(A+\lambda B)`$, so

```math
Q_R'(\lambda)=\frac{b_R(A+\lambda B)-B(a_R+\lambda b_R)}{(A+\lambda B)^2}=\frac{b_RA-a_RB}{(A+\lambda B)^2}.
```

The numerator does not depend on $`\lambda`$ and the denominator is positive. $`\square`$

**Corollary B2.** If there is no growth after the window ($`p=p^{21}`$), state $`i`$ gains as $`\lambda`$ rises exactly when its 1971–2021 growth factor $`p_i^{21}/p_i^{71}`$ exceeds the national factor.

The penalty for slower growth is softened but not removed. A state that grew less during the window still has a lower weight, just by $`\lambda`$ times as much.

### In India

No one has proposed this seat formula, so it is ours. Rewarding lower fertility does have a precedent in Indian fiscal federalism. The 15th Finance Commission (2020–26) had to switch its tax-sharing formula from 1971 to 2011 population. To compensate, it added a "demographic performance" criterion worth 12.5%: the reciprocal of each state's total fertility rate, scaled by its 1971 population. Telangana's Chief Minister made the same argument about seats in April 2026, saying a purely population-based reallocation punishes the states that implemented family planning.

> **TODO (group):** confirm the 2021 end year (around when national fertility reached replacement level) and the default $`\lambda=0.5`$.

*Computed.*
- The national 1971–2021 growth factor is 2.48. Every southern state except Puducherry grew more slowly.
- The south's share falls monotonically from 23.24% at $`\lambda=0`$ to 19.45% at $`\lambda=1`$ (20.58% at $`\lambda=0.5`$), and no state ever reverses direction.
- At $`\lambda=0.5`$, 9 states fall outside one seat of their population quota.
- Even $`\lambda=0`$ does not restore the south, because growth after 2021 counts in full.

## B.4 Degressive proportionality (Tharoor)

### The math

The weights are $`w_i=p_i^\alpha`$ for $`\alpha\in[0,1]`$. At $`\alpha=1`$ this is the population rule. At $`\alpha=0`$ every state gets the same weight, as in the US Senate. In between, larger states get more seats but fewer seats per person: seats per citizen scale like $`p_i^{\alpha-1}`$. Since $`p\mapsto p^\alpha`$ is strictly increasing and independent of $`K`$, Lemma A6 makes the rule **house monotonic and population monotonic** for every $`\alpha>0`$.

**Proposition B3.** Assume not all populations are equal. Let $`\ell_i=\ln p_i`$, let $`x_i=p_i^\alpha/\sum_k p_k^\alpha`$ be state $`i`$'s quota share, and let $`\mu(\alpha)=\sum_j x_j\ell_j`$ (the share-weighted mean log population). Then:

1. $`\frac{d}{d\alpha}\ln x_i=\ell_i-\mu(\alpha)`$, and $`\mu`$ is strictly increasing;
2. each state's share is single-peaked in $`\alpha`$: it rises while $`p_i>e^{\mu(\alpha)}`$ and falls afterwards;
3. the largest state's share is strictly increasing and the smallest state's is strictly decreasing.

*Proof.* $`\ln x_i=\alpha\ell_i-\ln\sum_k e^{\alpha\ell_k}`$, so $`\frac{d}{d\alpha}\ln x_i=\ell_i-\sum_k x_k\ell_k=\ell_i-\mu`$. Using $`x_j'=x_j(\ell_j-\mu)`$,

```math
\mu'=\sum_j x_j'\ell_j=\sum_j x_j\ell_j^2-\mu^2=\mathrm{Var}_x(\ell)>0,
```

strict because every $`x_j>0`$ and the $`\ell_j`$ are not all equal. So $`\ell_i-\mu(\alpha)`$ is strictly decreasing and changes sign at most once, from positive to negative; that is (2). For (3), $`\mu`$ is a weighted average with positive weight on every state, so $`\ell_{\min}<\mu<\ell_{\max}`$. $`\square`$

A region need not behave this way. For a region, $`\frac{d}{d\alpha}Q_R=Q_R(\mu_R-\mu)`$, where $`\mu_R`$ is the mean log population within $`R`$. Both means move with $`\alpha`$, so the sign can flip. This is unlike the fertility window, where every region always wants the dial turned the same way.

**Where $`\alpha=\tfrac12`$ comes from (Penrose's square-root law, derived from A.6).** Suppose each state's MPs voted as a bloc with weight $`w_i`$. A citizen of state $`i`$ would be decisive with probability about $`\sqrt{2/(\pi p_i)}\cdot\beta_i`$. When there are many states and none dominates, $`\beta_i`$ is roughly proportional to $`w_i`$. This approximation is not from the lecture, and the lecture's Electoral College table shows it is only rough. Under it, citizen influence is proportional to $`w_i/\sqrt{p_i}`$, which is equal across states exactly when $`w_i\propto\sqrt{p_i}`$, i.e. $`\alpha=\tfrac12`$. The argument needs bloc voting by state. Lok Sabha MPs vote by party, and the anti-defection law enforces this, so the justification does not carry over directly.

> **TODO (group):** decide whether to compute Banzhaf indices for party blocs in the Lok Sabha.

### In India

Degressive proportionality is the treaty rule for the European Parliament, which gives every member state between 6 and 96 seats; the treaty fixes no formula. In April 2026 Shashi Tharoor proposed it for the Lok Sabha, letting the number of citizens per MP rise with a state's population. He gave two examples: a state of 30 million at 1 million people per MP (30 seats) and a state of 200 million at 2.5 million per MP (80 seats). A power law through both has $`\alpha=\ln(80/30)/\ln(200/30)\approx 0.517`$, close to Penrose's $`\tfrac12`$.

*Computed.*
- The south's share is 16.7% at $`\alpha=0`$, peaks at 21.16% at $`\alpha\approx 0.558`$, and is 19.45% at $`\alpha=1`$. Tharoor's $`\alpha=0.517`$ gives 21.14%, almost exactly the south's best case, and still no $`\alpha`$ restores it.
- Most of the gain goes elsewhere. The Northeast and union territories rise from 4.0% to 10.9% of seats, mostly at the expense of the Hindi belt (48.8% to 41.6%).
- At $`\alpha=0.517`$, 35 of 36 units are more than one seat from their population quota.

## B.5 Floor plus proportional

### The math

Every state gets $`f`$ seats, and the remaining $`K-nf`$ are apportioned by Webster's method on population:

```math
k_i=f+\mathrm{Web}(p,\,K-nf)_i,\qquad \tilde q_i=f+(K-nf)\frac{p_i}{P},\qquad 0\le f\le K/n.
```

The second term is a divisor method on $`p`$ with house size $`K-nf`$, and adding the constant $`f`$ changes neither seat comparisons nor population comparisons. So the rule is **house monotonic and population monotonic** by Theorem A1 and Corollary A3.

**Proposition B4.** Let $`\theta=nf/K\in[0,1]`$ and $`\pi_R=\sum_{i\in R}p_i/P`$. Every region's quota share is

```math
Q_R=\theta\,\frac{\lvert R\rvert}{n}+(1-\theta)\,\pi_R.
```

So $`Q_R`$ lies between the region's population share $`\pi_R`$ and its share of states $`\lvert R\rvert/n`$, and no floor restores a region whose current seat share exceeds both.

*Proof.* $`Q_R=\frac1K\sum_{i\in R}\bigl(f+(K-nf)\pi_i\bigr)=\frac{\lvert R\rvert f}{K}+\bigl(1-\frac{nf}{K}\bigr)\pi_R`$, and $`\lvert R\rvert f/K=\theta\lvert R\rvert/n`$. $`\square`$

### In India

Floors are the most common departure from strict proportionality. The US Constitution guarantees every state one representative (the lecture's opening slide). Brazil gives every state between 8 and 70 deputies. The Cambridge Compromise proposed for the European Parliament is 5 base seats plus proportional seats. India already exempts states under 6 million from strict proportionality, and every small state and union territory has at least one seat. A natural question is how large a floor would need to be to keep today's north–south balance.

*Computed.*
- The south has 6 of 36 units (16.7%), 19.45% of the population and 23.94% of current seats.
- Both bounds in Proposition B4 are below its current share, so **no floor restores the south, and every floor lowers its share**. At $`K=816`$, $`f=10`$ gives 18.2%.
- Floors help regions with many small units: the Northeast and the union territories.
- At $`f=10`$, 33 units are more than one seat from their population quota.

## B.6 The hybrid rule (Reddy)

### The math

Every state keeps its current seats $`c_i`$. The $`K-K_0`$ new seats are split half in proportion to current seats and half by GDP share $`g_i`$ (with $`\sum_i g_i=1`$). With $`m_i=\tfrac12 c_i/K_0+\tfrac12 g_i`$, the targets are

```math
t_i(K)=c_i+(K-K_0)\,m_i,\qquad \sum_i t_i(K)=K.
```

$`R(K)`$ is Webster's method in sequential form (A.3) started from the floors. Begin at $`k=c`$, and give each new seat to the state with the largest priority $`t_i(K)/(k_i+\tfrac12)`$.

Unlike every other rule here, **the weights $`t(K)`$ depend on $`K`$**, so Lemma A6 does not apply. In fact the rule fails both properties.

**Proposition B5.** $`R`$ is not house monotonic.

*Proof.* Take three states with $`c=(1,1,2)`$, so $`K_0=4`$, and $`g=(\tfrac25,\tfrac12,\tfrac1{10})`$. Then $`m=(\tfrac{13}{40},\tfrac{15}{40},\tfrac{12}{40})`$.

- $`K=5`$: $`t=(1.325,\,1.375,\,2.3)`$. From $`(1,1,2)`$ the priorities are $`0.883`$, $`0.917`$ and $`0.920`$, so state 3 gets the seat and $`k=(1,1,3)`$.
- $`K=6`$: $`t=(1.65,\,1.75,\,2.6)`$. From $`(1,1,2)`$ the priorities are $`1.10`$, $`1.17`$ and $`1.04`$. State 2 gets a seat (its priority drops to $`0.70`$), then state 1, so $`k=(2,2,2)`$.

State 3 drops from 3 seats to 2 when the House grows: an Alabama paradox. $`\square`$

**Corollary B6.** $`R`$ is not population monotonic.

*Proof.* By Theorem A2, a population monotonic method is house monotonic. $`\square`$

The cause is that state 3's *target share* $`t_3(K)/K`$ falls as the House grows ($`0.46\to 0.43`$), because its GDP share is below its seat share. States just below a rounding threshold then overtake it. This is the same mechanism as Hamilton's paradox, where quotas also shift with $`K`$.

**Lemma B7.** If $`g_i=c_i/K_0`$ for all $`i`$, then $`R`$ is house monotonic.

*Proof.* Then $`t_i(K)=c_iK/K_0`$, a positive multiple of $`c`$, and Webster's priorities depend on the weights only up to scale. So $`R`$ is Webster on the fixed weights $`c`$, run from $`c`$. Webster with weights $`c`$ and house size $`K_0`$ returns $`c`$, because every quota is an integer. So the sequential run from $`c`$ coincides with $`\mathrm{Web}(c,K)`$, which is house monotonic by Corollary A3. $`\square`$

So the paradox comes from GDP shares differing from seat shares, which is the whole point of the proposal. The fix is to round only the new seats.

**Proposition B8.** The incremental hybrid $`R'(K)=c+\mathrm{Web}(m,\,K-K_0)`$ is house monotonic, gives every state at least $`c_i`$, and has the same targets $`t_i(K)`$ as $`R`$.

*Proof.* $`\mathrm{Web}(m,\cdot)`$ is a divisor method on fixed weights, so it is house monotonic (Corollary A3), and adding the constant vector $`c`$ preserves this. The floor holds because Webster's output is nonnegative, and the quota of the new seats is $`(K-K_0)m_i`$. $`\square`$

### In India

On April 13, 2026, Telangana's Chief Minister A. Revanth Reddy proposed allocating half of the new seats pro rata and half by states' GDP contribution. Press reports differ on whether "pro rata" means current seats or population. We read it as current seats, matching the government's pro-rata plan. Critics said no such model exists anywhere, and the BRS called it unconstitutional. In 2025 he had asked that the south's share rise from about 24% to 33%, in line with its GDP.

> **TODO (group):** settle the reading of "pro rata" and state it in the paper.

*Computed.*
- **The paradox happens in the real data.** With 2026 projections, Bihar has 44 seats at $`K=607`$ and 43 at $`K=608`$.
- **The fix costs almost nothing.** $`R'`$ equals $`R`$ at $`K=816`$, moves at most two seats relative to $`R`$ anywhere in $`[543,850]`$, and never violates house monotonicity.
- **The south's share.**
  - The hybrid gives the south 24.99% at $`K=816`$, the only rule besides the freeze that restores it.
  - It falls well short of 33%. Even if every new seat went by GDP, the south would get 26.0% at $`K=816`$. Its GDP share in our data is 30.2%, which the House approaches only as it grows without bound.
- At $`K=816`$, 26 units are more than one seat from their population quota.

---

## Summary

| Rule | House monotonic | Population monotonic | Quota w.r.t. population ($`K=816`$) | Penalises slower growth | South share ($`K=816`$) |
|---|---|---|---|---|---|
| Freeze / flat scale-up | yes | yes (vacuous) | no (28 states outside) | no | 23.94% |
| Population (2026 bill) | yes | yes | yes (not guaranteed, A5) | yes (A7) | 19.45% |
| Fertility window $`F_{0.5}`$ | yes | yes | no (9) | less, by factor $`\lambda`$ | 20.58% |
| Degressive $`D_{0.517}`$ | yes | yes | no (35) | less, elasticity $`\alpha`$ | 21.14% |
| Floor $`L_{10}`$ | yes | yes | no (33) | yes | 18.22% |
| Hybrid $`R`$ (Reddy) | **no** (B5) | **no** (B6) | no (26) | no (ignores population) | 24.99% |
| Incremental hybrid $`R'`$ | yes (B8) | yes (vacuous) | no (26) | no (ignores population) | 24.99% |

The south's current share is 23.94%. Every rule satisfies the quota criterion with respect to its *own* weights on our data, though Corollary A5 says this is not guaranteed.

Three conclusions follow.

1. Every rule built on population, including the two designed as compromises, leaves the south below its current share for every parameter value, and floors make it worse. Only rules anchored on current seats or GDP restore it.
2. The trade-off follows from the lecture framework. Only the population rule stays within quota with respect to population, and Observation A7 shows that any population-monotonic rule built on current population penalises slower growth.
3. The one popular proposal that restores the south, Reddy's hybrid, breaks both of the lecture's monotonicity properties as written. A one-line change, rounding only the new seats, repairs house monotonicity.

> **TODO (group):** link to the simulation: the formula differences above matter less for party seats than line-drawing does.

## References

**Course lectures (definitions in Part A)**
- A. D. Procaccia, Lecture 15: The Electoral College, CS 2380 Fall 2026: https://procaccia.info/courses/CS2380-F26/slides15.pdf
- A. D. Procaccia, Lecture 16: Apportionment in the 19th Century, CS 2380 Fall 2026: https://procaccia.info/courses/CS2380-F26/slides16.pdf
- A. D. Procaccia, Lecture 17: Apportionment in the 20th Century, CS 2380 Fall 2026: https://procaccia.info/courses/CS2380-F26/slides17.pdf
- Course site: https://sites.google.com/view/optdemocracy26

**Further theory**
- M. L. Balinski and H. P. Young. *Fair Representation: Meeting the Ideal of One Man, One Vote*. Brookings Institution Press, 2nd ed., 2001.
- L. S. Penrose. The elementary statistics of majority voting. *Journal of the Royal Statistical Society* 109(1):53–57, 1946.
- G. R. Grimmett. European apportionment via the Cambridge Compromise. *Mathematical Social Sciences* 63(2):68–73, 2012. https://arxiv.org/abs/1105.4294

**Indian law and policy**
- PRS, The Delimitation Bill, 2026: https://prsindia.org/billtrack/the-delimitation-bill-2026
- PRS, Implications of increasing the size of the Lok Sabha: https://prsindia.org/articles-by-prs-team/implications-of-increasing-the-size-of-the-lok-sabha
- PRS, Report of the 15th Finance Commission for 2021–26: https://prsindia.org/policy/report-summaries/report-15th-finance-commission-2021-26
- Business Standard, history of the 1976 freeze: https://www.business-standard.com/india-news/delimitation-india-history-population-north-south-2026-census-126041500914_1.html

**Proposals**
- Reddy's hybrid model: https://www.siasat.com/delimitation-telangana-cm-proposes-hybrid-model-for-increasing-ls-seats-3452163/
- Reddy's 33% demand (2025): https://www.business-standard.com/politics/southern-states-reject-population-formula-seek-gdp-based-representation-125032300788_1.html
- Criticism of the hybrid model: https://deccanchronicle.com/southern-states/telangana/kishan-reddy-slams-revanths-hybrid-delimitation-ploy-as-global-nonsense-1950464
- Tharoor on degressive proportionality: https://www.siasat.com/consult-states-before-delimitation-says-shashi-tharoor-to-pm-3453246/

**Other countries**
- EU composition decision, 2023: https://eur-lex.europa.eu/eli/dec/2023/2061/oj
- Brazil's Chamber of Deputies: https://aceproject.org/ace-en/topics/es/annex/esy/esy_br
