#!/usr/bin/env python3
"""Step-3 paired-EXACT power table (pre-registration §3.2a; D-059b).

Replaces the struck "powered for a >20 pp delta" claim (which was a per-arm
Wilson half-width statement, not a paired power computation — external review
finding 2, adopted). Computes the EXACT unconditional power of the paired
comparison at the administrative accrual cap n = 44 under a pre-registered
nuisance model.

Model. Each confirmed-defective case yields a paired binary catch outcome
(A2, B). Under cross-arm independence: p01 = p_B*(1-p_A2) (B catches, A2
misses), p10 = p_A2*(1-p_B), discordance pi_D = p01 + p10, conditional
discordant-pair probability pi* = p01/pi_D. The primary test is the exact
conditional sign test: given m discordant pairs, b ~ Bin(m, pi*) with
pi* = 1/2 under H0. Unconditionally m ~ Bin(44, pi_D).

Test level. Power is computed for the FINAL analysis at the locked design's
nominal final two-sided level 0.0440 (Z 2.0141; boundary_constants.*): reject
if the exact two-sided sign-test p-value = min(1, 2*min(P(X<=b), P(X>=b)))
<= 0.0440. This slightly UNDERSTATES the sequential design's total power
(interim efficacy looks add at most the alpha they spend, < 0.001 through
look 2) and slightly OVERSTATES power vs the exact-tail implementation
(exact spending <= nominal). Both margins are noted, not hidden. No futility
stopping is modeled (the rule is non-binding, D-054e/D-060).

Run:  python3 power_table.py        (needs scipy)
"""
from __future__ import annotations
from scipy.stats import binom

N = 44                    # administrative accrual cap (D-054b as amended by D-059a)
FINAL_P = 0.0440          # locked final-look nominal two-sided level (Z=2.0141)


def exact_sign_reject(m: int, level: float) -> list[int]:
    """b-values (successes for B) rejecting the exact two-sided sign test at `level`."""
    out = []
    for b in range(m + 1):
        lo, hi = binom.cdf(b, m, 0.5), 1 - binom.cdf(b - 1, m, 0.5)
        if min(1.0, 2 * min(lo, hi)) <= level:
            out.append(b)
    return out


def power(p_a2: float, p_b: float, n: int = N, level: float = FINAL_P):
    p01 = p_b * (1 - p_a2)          # B catches, A2 misses
    p10 = p_a2 * (1 - p_b)
    pi_d = p01 + p10
    pi_star = p01 / pi_d if pi_d > 0 else 0.5
    pw = 0.0
    for m in range(n + 1):
        pm = binom.pmf(m, n, pi_d)
        if pm < 1e-12 or m == 0:
            continue
        rej = exact_sign_reject(m, level)
        pw += pm * sum(binom.pmf(b, m, pi_star) for b in rej)
    return pw, pi_d, pi_star, N * pi_d


def row(p_a2, p_b):
    pw, pi_d, pi_star, em = power(p_a2, p_b)
    print(f"{p_a2:>6.2f} {p_b:>6.2f} {p_b-p_a2:>7.2f} {pi_d:>8.4f} {pi_star:>8.4f} "
          f"{em:>7.1f} {pw:>9.3f}")


def main():
    print("=" * 66)
    print(f"STEP-3 PAIRED-EXACT POWER at n = {N} (administrative cap)")
    print(f"Exact two-sided sign test at the final nominal level {FINAL_P}")
    print("(locked final bound Z = 2.0141); m ~ Bin(44, pi_D), b|m ~ Bin(m, pi*)")
    print("=" * 66)
    print(f"{'p_A2':>6} {'p_B':>6} {'delta':>7} {'pi_D':>8} {'pi*':>8} "
          f"{'E[m]':>7} {'power':>9}")
    print("-" * 66)
    print("# pre-registered nuisance model row set (p_A2 = 0.05):")
    for d in (0.10, 0.15, 0.20, 0.25, 0.30, 0.35):
        row(0.05, 0.05 + d)
    print("# sensitivity (higher same-vendor arm, p_A2 = 0.15):")
    for d in (0.20, 0.30):
        row(0.15, 0.15 + d)
    print("-" * 66)
    print("READING (pre-registration §3.2a): ~90% power requires delta ~0.30 with")
    print("a near-zero same-vendor arm (p_A2=0.05, p_B=0.35). At delta = 0.20 the")
    print("exact paired power is ~47-67% depending on the nuisance rates: 20 pp")
    print("effects are DETECTABLE ONLY DESCRIPTIVELY (estimation, adjusted CI at")
    print("stopping), and the futility calibration is drawn at delta* = 0.30")
    print("(D-060) - never at an alternative the design cannot detect.")


if __name__ == "__main__":
    main()
