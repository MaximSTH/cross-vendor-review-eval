#!/usr/bin/env python3
"""Step-3 group-sequential boundary constants (pre-registration §3.7).

Computes the EXACT boundaries for the ratified design:
  EFFICACY (LOCKED, D-054):
  - O'Brien-Fleming-type Lan-DeMets alpha-spending (sfLDOF), two-sided FWER 0.05
    (i.e. one-sided 0.025 per side for the symmetric test)
  - K = 4 looks at information fractions t = 0.25 / 0.50 / 0.75 / 1.00
  FUTILITY (LOCKED, D-060 — ratifying the 2026-07-29 external review's §3.4
  proposal; supersedes the PROVISIONAL set this file previously printed):
  - NON-BINDING beta-spending lower bound, beta = 0.10 (90% power) at the
    calibrating alternative delta* = 0.30 under the pre-registered nuisance
    model p_A2 = 0.05 / p_B = 0.35 (cross-arm independence)
  - one-sided sfLDOF beta-spending on the shared timing grid
  - the maximum-information inflation factor r is solved so the final lower
    bound meets the final efficacy bound with beta exactly spent — the
    gsDesign test.type=4 construction (the earlier test.type=6 run computed an
    H0-spent astar lower bound, a different concept: D-059c; its output is
    superseded and its spurious "inflation" figure quarantined).

This reproduces the canonical gsDesign run (boundary_constants.R / .R.out,
test.type=2 efficacy + test.type=4 futility) as an INDEPENDENT from-scratch
sequential numerical-integration recursion (Armitage-McPherson-Rowe; Lan &
DeMets 1983; Jennison & Turnbull 2000), validated to <1e-3 at every look.

Directional precedence (D-059d): the recursion masks the continuation region
at BOTH efficacy bounds (|B| < u_k) and the futility bound — the futility
recommendation zone is Z in (-b_k, a_k]; Z <= -b_k is a reverse-direction
efficacy crossing and takes precedence. (Numerically negligible under the
calibrating drift; kept because the code should state the ratified rule.)

Monitoring note (D-059a): these Z-constants are SPENDING TARGETS. At analysis
time the monitored statistic is the exact conditional sign test on discordant
pairs (b of m; b ~ Bin(m, 1/2) under H0), with the sfLDOF spend implemented
via exact tail probabilities <= the nominal spend at each look; information
is m/m_max, n_max = 44 is an administrative accrual cap, and no futility
evaluation occurs at any look with fewer than 8 observed discordant pairs
(D-060 minimum-information gate).

NOTE (self-correction, kept per the project's incoherence discipline): a first
version used the two-sided critical value z_.975 as the sfLDOF characteristic
constant and matched a two-sided exit; that is a NON-standard sfLDOF variant
and disagreed with gsDesign at early looks. The reference sfLDOF uses the
per-side z_.9875 and matches the upper-tail crossing (one-sided 0.025). This
file uses the reference definition; the gsDesign cross-check is what surfaced
the discrepancy.

Run:  python3 boundary_constants.py        (needs numpy, scipy)
"""
from __future__ import annotations
import numpy as np
from scipy.stats import norm
from scipy.optimize import brentq
from scipy.signal import fftconvolve

ALPHA_2S = 0.05                    # two-sided family-wise (D-054f: A2-vs-B at full alpha)
ALPHA_1S = ALPHA_2S / 2            # 0.025 per side (symmetric test)
T = np.array([0.25, 0.50, 0.75, 1.00])   # information fractions (D-054c)
ZC = norm.ppf(1 - ALPHA_1S / 2)    # sfLDOF characteristic constant = z_.9875 = 2.24140

# gsDesign 3.10.1 reference values (boundary_constants.R.out, this timing):
GSDESIGN_EFF = np.array([4.3326, 2.9631, 2.3590, 2.0141])   # test.type=2 (LOCKED)
GSDESIGN_FUT = np.array([-1.4027, 0.3249, 1.2911, 2.0141])  # test.type=4 (LOCKED, D-060)
GSDESIGN_INFL = 1.083                                       # max-info inflation, test.type=4

# ---- grid on the B-value (score) scale; B_k = Z_k*sqrt(t_k), independent increments
DX = 0.0004
BMAX = 9.0
XG = np.arange(-BMAX, BMAX + DX, DX)


def sfLDOF_spend(t: float, total: float) -> float:
    """Lan-DeMets O'Brien-Fleming spending (gsDesign sfLDOF): f(1) = total."""
    return 2.0 * (1.0 - norm.cdf(norm.ppf(1 - total / 2) / np.sqrt(t)))


def _increment_pdf(dt: float, drift: float = 0.0) -> np.ndarray:
    return norm.pdf(XG, loc=drift, scale=np.sqrt(dt))


def efficacy_boundaries():
    """Per-look: Z-boundary b_k (symmetric +/-), nominal two-sided p, incremental
    & cumulative one-sided alpha spent (validation)."""
    astar = np.array([sfLDOF_spend(t, ALPHA_1S) for t in T])
    pi = np.diff(np.concatenate([[0.0], astar]))   # incremental (one-sided) alpha
    dt = np.diff(np.concatenate([[0.0], T]))

    g = None                       # survivor sub-density entering current look
    out, spent_cum = [], 0.0
    for k in range(len(T)):
        g = _increment_pdf(dt[0]) if k == 0 else fftconvolve(g, _increment_pdf(dt[k]), mode="same") * DX
        g_mass = float(np.trapezoid(g, XG))
        def exit_upper(b):
            u = b * np.sqrt(T[k])                  # B-scale boundary
            below = XG < u                         # contiguous; upper tail = mass - below
            return g_mass - float(np.trapezoid(g[below], XG[below]))
        b = brentq(lambda b: exit_upper(b) - pi[k], 0.0, 9.0, xtol=1e-10)
        u = b * np.sqrt(T[k])
        spent_cum += exit_upper(b)
        out.append({"look": k + 1, "t": T[k], "b_Z": b,
                    "nominal_p_2sided": 2 * (1 - norm.cdf(b)),
                    "alpha_incremental_1s": pi[k], "alpha_cumulative_1s": spent_cum})
        g = np.where(np.abs(XG) < u, g, 0.0)       # symmetric continuation: stop on either bound
    return out, spent_cum


# ---------------------------------------------------------------------------
# LOCKED futility (non-binding, beta-spending) — D-060 calibration:
#   calibrating alternative delta* = 0.30 (p_A2 = 0.05, p_B = 0.35), 90% power
#   -> fixed-design drift THETA_FIX = z_.975 + z_.90; under information
#   inflation r the drift at look k is THETA_FIX*sqrt(r*t_k). r is solved so
#   the final lower bound equals the final efficacy bound with beta = 0.10
#   exactly spent (the gsDesign test.type=4 construction, non-binding: the
#   efficacy bounds above are computed ignoring the lower bound).
BETA = 0.10
THETA_FIX = norm.ppf(1 - ALPHA_1S) + norm.ppf(1 - BETA)   # 3.241516 (z_.975+z_.90)
DELTA_STAR = 0.30                                          # calibrating alternative (D-060)
P_A2, P_B = 0.05, 0.35                                     # pre-registered nuisance model


def futility_boundaries(eff, r):
    """Lower bounds a_1..a_K under inflation factor r; a_K forced to b_K.
    Returns (bounds, total beta spent). sfLDOF beta-spending, gsDesign form."""
    bstar = np.array([sfLDOF_spend(t, BETA) for t in T])
    pi_b = np.diff(np.concatenate([[0.0], bstar]))
    dt = np.diff(np.concatenate([[0.0], T]))
    u_eff = [e["b_Z"] * np.sqrt(e["t"]) for e in eff]
    theta = THETA_FIX * np.sqrt(r)                 # drift per unit information fraction

    g, out, spent = None, [], 0.0
    for k in range(len(T)):
        inc = _increment_pdf(dt[k], drift=theta * dt[k])
        g = inc.copy() if k == 0 else fftconvolve(g, inc, mode="same") * DX
        def below_prob(a):
            m = XG <= a * np.sqrt(T[k])
            return float(np.trapezoid(g[m], XG[m]))
        if k < len(T) - 1:
            a = brentq(lambda a: below_prob(a) - pi_b[k], -9.0, eff[k]["b_Z"], xtol=1e-10)
        else:
            a = eff[k]["b_Z"]                      # final: lower meets upper
        spent += below_prob(a)
        out.append({"look": k + 1, "t": T[k], "a_Z": a,
                    "beta_incremental": pi_b[k] if k < len(T) - 1 else None,
                    "beta_cumulative": spent})
        # D-059d precedence: continuation masked at BOTH efficacy bounds
        # (|B| < u) and above the futility bound; Z <= -b_k is a
        # reverse-direction efficacy crossing, not futility.
        g = np.where((np.abs(XG) < u_eff[k]) & (XG > a * np.sqrt(T[k])), g, 0.0)
    return out, spent


def solve_inflation(eff):
    """Solve the max-information inflation r so total beta spent = BETA."""
    return brentq(lambda r: futility_boundaries(eff, r)[1] - BETA, 1.0, 1.5, xtol=1e-8)


def main():
    eff, spent = efficacy_boundaries()
    print("=" * 76)
    print("STEP-3 EFFICACY BOUNDARIES  (LOCKED, D-054)")
    print("O'Brien-Fleming-type Lan-DeMets alpha-spending (sfLDOF), two-sided FWER 0.05")
    print("K=4 looks at t = 0.25 / 0.50 / 0.75 / 1.00   (D-054 a,c,d,f)")
    print("=" * 76)
    print(f"{'look':>4} {'t':>6} {'Z-bound b_k':>12} {'nominal p(2s)':>15} "
          f"{'a incr (1s)':>13} {'a cum (1s)':>11} {'gsDesign':>9}")
    ok = True
    for e, gd in zip(eff, GSDESIGN_EFF):
        match = abs(e["b_Z"] - gd) < 1e-3
        ok = ok and match
        print(f"{e['look']:>4} {e['t']:>6.2f} {e['b_Z']:>12.4f} "
              f"{e['nominal_p_2sided']:>15.6g} {e['alpha_incremental_1s']:>13.6g} "
              f"{e['alpha_cumulative_1s']:>11.6f} {gd:>9.4f}")
    print("-" * 76)
    print(f"VALIDATION: cumulative one-sided alpha = {spent:.6f} (target {ALPHA_1S}) "
          f"-> {'PASS' if abs(spent-ALPHA_1S)<1e-4 else 'FAIL'}")
    print(f"VALIDATION: matches gsDesign 3.10.1 sfLDOF to <1e-3 at every look "
          f"-> {'PASS' if ok else 'FAIL'}")
    print(f"NOTE: two-sided FWER = {ALPHA_2S} (0.025 per side); final bound "
          f"{eff[-1]['b_Z']:.4f} vs fixed 1.9600.")

    r = solve_inflation(eff)
    fut, bspent = futility_boundaries(eff, r)
    print()
    print("=" * 76)
    print("STEP-3 FUTILITY BOUNDARIES  (LOCKED, D-060 — non-binding, escalated)")
    print(f"one-sided sfLDOF beta-spending, beta={BETA} (90% power) at delta*="
          f"{DELTA_STAR} (p_A2={P_A2}, p_B={P_B});")
    print(f"gsDesign test.type=4 construction: solved max-info inflation r = {r:.4f}")
    print("=" * 76)
    print(f"{'look':>4} {'t':>6} {'Z-lower a_k':>12} {'beta cum':>10} {'gsDesign':>9}")
    okf = True
    for f, gd in zip(fut, GSDESIGN_FUT):
        match = abs(f["a_Z"] - gd) < 1e-3
        okf = okf and match
        print(f"{f['look']:>4} {f['t']:>6.2f} {f['a_Z']:>12.4f} "
              f"{f['beta_cumulative']:>10.5f} {gd:>9.4f}")
    print("-" * 76)
    print(f"VALIDATION: cumulative beta spent = {bspent:.6f} (target {BETA}) "
          f"-> {'PASS' if abs(bspent-BETA)<1e-4 else 'FAIL'}")
    print(f"VALIDATION: matches gsDesign 3.10.1 test.type=4 to <1e-3 at every look "
          f"-> {'PASS' if okf else 'FAIL'}")
    print(f"VALIDATION: inflation r = {r:.4f} vs gsDesign n.I[4] = {GSDESIGN_INFL} "
          f"-> {'PASS' if abs(r-GSDESIGN_INFL)<2e-3 else 'FAIL'}")
    print("NOTE: futility a_k is a STOP-RECOMMENDATION threshold escalated to the")
    print("supervisor (D-054e / D-058 / D-060) — never automatic. Recommendation")
    print("zone Z in (-b_k, a_k]; Z <= -b_k is reverse-direction efficacy (D-059d).")
    print("Applied only at looks with >= 8 observed discordant pairs (D-060 gate);")
    print("monitored via the exact conditional sign test, Z_k=(2b-m)/sqrt(m).")


if __name__ == "__main__":
    main()
