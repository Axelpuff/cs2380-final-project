# Theory: properties of the candidate seat rules

The simulation compares seat rules by what they do to party seat counts. This section compares them by the properties the Indian debate is about: whether a rule rewards states that slowed their population growth, whether it can give the south back its current share of seats, and whether it behaves sensibly as the House grows. Everything here is about the **allocation between states**; nothing depends on how lines are drawn inside a state.

Numbers marked as computed come from the data in `analysis/apportion.py` (2026 projected populations, all 36 units, quota shares before rounding).

> **TODO (group):** decide whether the paper uses 2026 projected populations throughout, and whether union territories are included (they are below).

## 1. Model

There are $n$ units (states and union territories), $N=\lbrace 1,\dots,n\rbrace$; in our data $n=36$. Unit $i$ currently holds $c_i$ seats, with $H_0=\sum_i c_i=543$. Its population is $p_i$ today, $p_i^{71}$ at the 1971 census and $p_i^{21}$ in 2021. Write $P=\sum_i p_i$ and $\pi_i=p_i/P$ for the population share, and $g_i\ge 0$ with $\sum_i g_i=1$ for unit $i$'s share of national GDP.

A **rule** takes this data and a House size $H\ge H_0$ and returns seats $s(H)\in\mathbb{Z}_{\ge 0}^n$ with $\sum_i s_i(H)=H$. Most rules below are **weight rules**: compute weights $w_i>0$ and round with Webster's method,

$$\mathrm{Web}(w,H)_i=\left[\,w_i/d\,\right],\qquad d\text{ chosen so that }\textstyle\sum_i [w_i/d]=H,$$

where $[\cdot]$ is ordinary rounding. The **quota** of unit $i$ is $q_i=Hw_i/\sum_j w_j$. For a region $R\subseteq N$, $Q_R=\sum_{i\in R}q_i/H$ is its quota share. Results about quotas ignore rounding, which usually moves each unit by less than one seat.

**Definition (properties).** A rule satisfies

- **(a) house monotonicity** if $s_i(H+1)\ge s_i(H)$ for every $i$ and $H$ (no Alabama paradox);
- **(b) population monotonicity** if, whenever populations change from $p$ to $p'$ at fixed $H$ with $p'_i/p'_j>p_i/p_j$, it is not the case that $i$ loses seats while $j$ gains;
- **(c) exactness** ("one person, one vote") if whenever every $H\pi_i$ is an integer, $s_i=H\pi_i$ for all $i$;
- **(d) restoration** for a region $R$ if $Q_R\ge\sum_{i\in R}c_i/H_0$, i.e. the region keeps at least its current share.

Two standard facts (Balinski and Young): Webster's method with weights that do not depend on $H$ is house monotone and population monotone, as is every divisor method; and no method is both population monotone and always within one seat of quota.

## 2. The rules

- **Freeze / flat scale-up:** $w_i=c_i$.
- **Population (the 2026 bill):** $w_i=p_i$.
- **Fertility window $F_\lambda$, $\lambda\in[0,1]$:** growth during 1971–2021, the period of the population-control programme, counts at weight $\lambda$:
  $$w_i(\lambda)=p_i^{71}+\lambda\,(p_i^{21}-p_i^{71})+(p_i-p_i^{21}).$$
  $F_1$ is the population rule.
- **Degressive $D_\alpha$, $\alpha\in[0,1]$:** $w_i=p_i^\alpha$. $D_1$ is the population rule, $D_0$ gives every unit the same weight, and Tharoor's two examples fit $\alpha\approx 0.517$.
- **Floor plus proportional $L_f$:** every unit gets $f$ seats and the remaining $H-nf$ go by population, so $q_i=f+(H-nf)\pi_i$, for $0\le f\le H/n$.
- **Hybrid $R$ (our reading of Reddy's proposal):** every unit keeps $c_i$, and the $H-H_0$ new seats are split half in proportion to current seats and half by GDP. With $m_i=\tfrac12 c_i/H_0+\tfrac12 g_i$, the targets are $t_i(H)=c_i+(H-H_0)m_i$, which sum to $H$. $s(H)$ is Webster's method started from the floors: begin at $s=c$ and give each new seat, one at a time, to the unit with the largest $t_i(H)/(s_i+\tfrac12)$. Unlike the others, the weights $t(H)$ depend on $H$.

## 3. Slower growth never pays under current-population rules

**Observation 1.** Let a rule depend only on current populations and be population monotone. If one unit's population is lower (others unchanged, $H$ fixed), that unit cannot have more seats.

*Proof.* Suppose $p'_i<p_i$, $p'_j=p_j$ for $j\ne i$, and $s'_i>s_i$. Since $\sum s'=\sum s=H$, some $j$ has $s'_j<s_j$. But $p'_j/p'_i>p_j/p_i$, so $j$'s relative population rose while $j$ lost and $i$ gained, contradicting population monotonicity. $\square$

So under the population rule, and under every other monotone rule that looks only at today's census, a state that slowed its growth is never better off. This is the southern complaint in formal terms. Such a rule can at most soften the penalty. $D_\alpha$ softens it for all growth alike (weights scale like $p^\alpha$). $F_\lambda$ softens it only for growth during 1971–2021, and to do that it has to use past census data.

## 4. The fertility window is a clean dial

**Proposition 2.** Under $F_\lambda$, write $a_i=p_i^{71}+(p_i-p_i^{21})$ and $b_i=p_i^{21}-p_i^{71}$, so $w_i(\lambda)=a_i+\lambda b_i$, and let $A=\sum_i a_i$, $B=\sum_i b_i$. For every region $R$ (in particular every single unit), the quota share $Q_R(\lambda)$ is monotone in $\lambda$: increasing if $b_R/a_R>B/A$ and decreasing if $b_R/a_R<B/A$, where $a_R=\sum_{i\in R}a_i$ and $b_R=\sum_{i\in R}b_i$.

*Proof.* $Q_R(\lambda)=(a_R+\lambda b_R)/(A+\lambda B)$, so

$$Q_R'(\lambda)=\frac{b_R(A+\lambda B)-B(a_R+\lambda b_R)}{(A+\lambda B)^2}=\frac{b_RA-a_RB}{(A+\lambda B)^2},$$

whose numerator does not depend on $\lambda$ and whose denominator is positive. $\square$

**Corollary 3.** If there is no growth after the window ($p=p^{21}$), unit $i$ gains as $\lambda$ rises exactly when its 1971–2021 growth factor $p_i^{21}/p_i^{71}$ exceeds the national factor.

*Computed.* The national factor is 2.48. Every southern state except Puducherry grew more slowly. With 2026 populations the condition in Proposition 2 still holds for the south as a region: its quota share falls monotonically from 23.24% at $\lambda=0$ to 19.45% at $\lambda=1$, and no unit's share ever reverses direction along the way. **Lowering $\lambda$ is therefore a one-dimensional compromise in which every state knows which way it wants the dial turned.** But even $\lambda=0$ does not restore the south (23.24% against 23.94% today), because growth after 2021 still counts in full.

## 5. Degressive proportionality is not a clean dial

Degressive proportionality is the principle the European Parliament follows; the Cambridge Compromise (Grimmett 2012) is one formula proposed for it.

**Proposition 4.** Under $D_\alpha$ with not all populations equal, let $\ell_i=\ln p_i$, $x_i=p_i^\alpha/\sum_k p_k^\alpha$ (unit $i$'s quota share) and $\mu(\alpha)=\sum_j x_j\ell_j$ (the quota-weighted mean log population). Then:

1. $\frac{d}{d\alpha}\ln x_i=\ell_i-\mu(\alpha)$, and $\mu$ is strictly increasing;
2. each unit's quota share is single-peaked in $\alpha$: it rises while $p_i>e^{\mu(\alpha)}$ and falls afterwards;
3. the largest unit's share is strictly increasing and the smallest unit's is strictly decreasing.

*Proof.* $\ln x_i=\alpha\ell_i-\ln\sum_k e^{\alpha\ell_k}$, so $\frac{d}{d\alpha}\ln x_i=\ell_i-\sum_k x_k\ell_k=\ell_i-\mu$. Using $x_j'=x_j(\ell_j-\mu)$,

$$\mu'=\sum_j x_j'\ell_j=\sum_j x_j\ell_j^2-\mu^2=\mathrm{Var}_x(\ell)>0,$$

strict because every $x_j>0$ and the $\ell_j$ are not all equal. So $\ell_i-\mu(\alpha)$ is strictly decreasing and changes sign at most once, from positive to negative; that is (2). For (3), $\mu$ is a weighted average with positive weight on every unit, so $\ell_{\min}<\mu<\ell_{\max}$ for all $\alpha$. $\square$

Single units behave simply, but regions need not. For a region, $\frac{d}{d\alpha}Q_R=Q_R(\mu_R-\mu)$, where $\mu_R$ is the mean log population within $R$. Both means move with $\alpha$, so the sign can flip.

*Computed.* The south does exactly this. Its quota share is 16.7% at $\alpha=0$, peaks at 21.16% at $\alpha\approx 0.558$, and falls to 19.45% at $\alpha=1$. Tharoor's fitted $\alpha=0.517$ (south 21.14%) sits almost exactly at the south-maximising exponent. Even so, no $\alpha$ restores the south, and it is not true that "more degressive" always means "better for the south."

**Remark (Penrose).** The exponent $\tfrac12$ has a classical justification. If each state's delegation voted as a single bloc, and citizens voted independently at random, giving state $i$ weight proportional to $\sqrt{p_i}$ would make every citizen's Banzhaf power roughly equal (Penrose 1946). Lok Sabha MPs do not vote as state blocs. They vote by party, and the anti-defection law enforces this, so the argument does not carry over directly.

> **TODO (group):** decide whether to compute Banzhaf power for party blocs, which would connect to the class material on weighted voting.

## 6. Floors cannot restore the south

This answers a question we asked at the start: how large would a floor need to be to keep today's balance?

**Proposition 5.** Under $L_f$ with $\theta=nf/H\in[0,1]$, every region's quota share is

$$Q_R=\theta\,\frac{\lvert R\rvert}{n}+(1-\theta)\,\pi_R,\qquad \pi_R=\sum_{i\in R}\pi_i.$$

In particular $Q_R$ lies between $\pi_R$ and $\lvert R\rvert/n$, and no floor restores a region whose current seat share exceeds both.

*Proof.* $Q_R=\frac1H\sum_{i\in R}\bigl(f+(H-nf)\pi_i\bigr)=\frac{\lvert R\rvert f}{H}+\bigl(1-\frac{nf}{H}\bigr)\pi_R$, and $\lvert R\rvert f/H=\theta\lvert R\rvert/n$. $\square$

*Computed.* The south has 6 of 36 units (16.7%), 19.45% of the 2026 population and 23.94% of current seats. So every floor **lowers** the south's share; at $H=816$, a floor of 10 seats gives 18.2%. Floors help regions with many small units, here the Northeast and the union territories, not regions of large, slow-growing states.

## 7. The hybrid rule has an Alabama paradox

**Proposition 6.** The hybrid rule $R$ is not house monotone.

*Proof.* Take three units with $c=(1,1,2)$, so $H_0=4$, and $g=(\tfrac25,\tfrac12,\tfrac1{10})$. Then $m=(\tfrac{13}{40},\tfrac{15}{40},\tfrac{12}{40})$.

- $H=5$: $t=(1.325,\,1.375,\,2.3)$. Starting from the floors $(1,1,2)$, Webster gives the one remaining seat to the largest $t_i/(s_i+\tfrac12)$. These are 0.883, 0.917 and 0.920, so unit 3 wins and $s(5)=(1,1,3)$.
- $H=6$: $t=(1.65,\,1.75,\,2.6)$. From $(1,1,2)$ the priorities are 1.10, 1.17 and 1.04, so unit 2 gets a seat (its priority drops to 0.70), then unit 1. So $s(6)=(2,2,2)$.

Unit 3 drops from 3 seats to 2 when the House grows. $\square$

The cause is that the weights depend on $H$. Unit 3 has a large current share but a small GDP share, so its target share $t_3(H)/H$ falls as the House grows ($0.46\to 0.43$). Units just below a rounding threshold then overtake it.

*Computed.* The paradox occurs in the real data: with 2026 projections, Bihar has 44 seats at $H=607$ and 43 at $H=608$.

**Lemma 7.** If $g_i=c_i/H_0$ for all $i$, then $R$ is house monotone.

*Proof.* Then $t_i(H)=c_iH/H_0$, a positive multiple of $c$, and Webster's priorities depend on the weights only up to scale. So $R$ is Webster with the fixed weights $c$, started from $c$. Webster with weights $c$ and House $H_0$ gives exactly $c$, because all quotas are integers. Webster run one seat at a time is house monotone, so continuing from $c$ produces $\mathrm{Web}(c,H)$ for every $H\ge H_0$, and the sequence is house monotone. $\square$

The fix is to round only the new seats.

**Proposition 8.** The **incremental hybrid** $R'(H)=c+\mathrm{Web}(m,H-H_0)$ is house monotone, gives every unit at least $c_i$, and has the same targets $t_i(H)=c_i+(H-H_0)m_i$ as $R$.

*Proof.* The weights $m$ do not depend on $H$, so $\mathrm{Web}(m,\cdot)$ is house monotone, and adding the constant vector $c$ preserves this. The floor holds because Webster's output is nonnegative. The quota of the new seats is $(H-H_0)m_i$. $\square$

*Computed.* On our data $R'$ gives exactly the same allocation as $R$ at $H=816$. Over $H\in[543,850]$ at most two seats ever move between units relative to $R$, and $R'$ has no violations. In the toy instance, $R'$ gives $(1,2,2)$ then $(2,2,2)$.

## 8. Summary

| Rule | House monotone | Exact | Penalises slower growth | South quota share ($H=816$) |
|---|---|---|---|---|
| Freeze / flat scale-up | yes | no | no | 23.94% |
| Population (bill) | yes | yes | yes | 19.45% |
| Fertility window $F_{0.5}$ | yes | no | less (window growth $\times\lambda$) | 20.58% |
| Degressive $D_{0.517}$ | yes | no | less (elasticity $\alpha$) | 21.14% |
| Floor $L_{10}$ | yes | no | yes | 18.22% |
| Hybrid $R$ | **no** | no | no (ignores population) | 24.99% |
| Incremental hybrid $R'$ | yes | no | no (ignores population) | 24.99% |

Shares are quota shares before rounding, with 2026 projected populations; the south's current share is 23.94%.

Two conclusions follow. First, every rule built on population, including the two designed as compromises ($F_\lambda$ and $D_\alpha$), leaves the south below its current share for every parameter value, and floors make it worse. Only rules anchored on current seats or GDP restore it. Second, the one popular proposal that does restore the south, Reddy's hybrid, has an Alabama paradox as naturally written, and a one-line change removes it.

> **TODO (group):** link to the simulation: the formula differences above matter less for party seats than line-drawing does.

## References

- M. L. Balinski and H. P. Young. *Fair Representation: Meeting the Ideal of One Man, One Vote*. Brookings Institution Press, 2nd ed., 2001.
- L. S. Penrose. The elementary statistics of majority voting. *Journal of the Royal Statistical Society* 109(1):53–57, 1946.
- G. R. Grimmett. European apportionment via the Cambridge Compromise. *Mathematical Social Sciences* 63(2):68–73, 2012.
