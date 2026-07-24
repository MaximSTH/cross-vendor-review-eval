#!/usr/bin/env python3
"""Step-3 group-sequential boundary constants (pre-registration §3.7).

Computes the EXACT efficacy boundaries for the ratified design (D-054):
  - O'Brien-Fleming-type Lan-DeMets alpha-spending (sfLDOF), two-sided FWER 0.05
    (i.e. one-sided 0.025 per side for the symmetric test)
  - K = 4 looks at information fractions t = 0.25 / 0.50 / 0.75 / 1.00
and a PROVISIONAL non-binding beta-spending futility boundary (flagged for the
supervisor's external-review pass — it depends on two inputs the rulings did NOT
pin: the calibrating alternative effect size and the beta-spending shape).

This reproduces the reference implementation gsDesign (sfLDOF, test.type=2); the
gsDesign cross-check script + output are committed alongside (boundary_constants.R
/ .R.out). Method: the standard sequential numerical-integration recursion
(Armitage-McPherson-Rowe; Lan & DeMets 1983; Jennison & Turnbull 2000). The
efficacy result is validated against gsDesign to <1e-3 and by cumulative-alpha.

NOTE (self-correction, kept per the project's incoherence discipline): a first
version used the two-sided critical value z_.975 as the sfLDOF characteristic
constant and matched a two-sided exit; that is a NON-standard sfLDOF variant and
disagreed with gsDesign at early looks. The reference sfLDOF uses the per-side
z_.9875 and matches the upper-tail crossing (one-sided 0.025). This file uses the
reference definition; the gsDesign cross-check is what surfaced the discrepancy.

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

# gsDesign 3.10.1 reference values (sfLDOF, test.type=2, alpha=0.025, this timing):
GSDESIGN_EFF = np.array([4.3326, 2.9631, 2.3590, 2.0141])

# ---- grid on the B-value (score) scale; B_k = Z_k*sqrt(t_k), independent increments
DX = 0.0004
BMAX = 9.0
XG = np.arange(-BMAX, BMAX + DX, DX)


def sfLDOF_spend(t: float) -> float:
    """Lan-DeMets O'Brien-Fleming spending (gsDesign sfLDOF): astar(1)=ALPHA_1S."""
    return 2.0 * (1.0 - norm.cdf(ZC / np.sqrt(t)))


def _increment_pdf(dt: float) -> np.ndarray:
    return norm.pdf(XG, loc=0.0, scale=np.sqrt(dt))


def efficacy_boundaries():
    """Per-look: Z-boundary b_k (symmetric +/-), nominal two-sided p, incremental
    & cumulative one-sided alpha spent (validation)."""
    astar = np.array([sfLDOF_spend(t) for t in T])
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
# PROVISIONAL futility (non-binding, beta-spending). Depends on inputs NOT pinned
# by the rulings -> flagged for external review:
#   (i)  calibrating alternative: design powered 1-BETA at drift THETA_MAX
#   (ii) beta-spending shape (here: one-sided sfLDOF, OBF-like)
BETA = 0.10
Z_BETA = norm.ppf(1 - BETA)                        # 1.281552
THETA_MAX = norm.ppf(1 - ALPHA_1S) + Z_BETA        # 3.241516  (z_.975+z_.90, 90% power)


def sfLDOF_one_sided_beta(t: float) -> float:
    return 1.0 - norm.cdf(Z_BETA / np.sqrt(t))     # bstar(1)=BETA


def futility_boundaries(eff):
    bstar = np.array([sfLDOF_one_sided_beta(t) for t in T])
    pi_b = np.diff(np.concatenate([[0.0], bstar]))
    dt = np.diff(np.concatenate([[0.0], T]))
    u_eff = [e["b_Z"] * np.sqrt(e["t"]) for e in eff]

    g, out, spent = None, [], 0.0
    for k in range(len(T)):
        drift = THETA_MAX * dt[k]
        inc = norm.pdf(XG, loc=drift, scale=np.sqrt(dt[k]))
        g = inc.copy() if k == 0 else fftconvolve(g, inc, mode="same") * DX
        def below_prob(a):
            m = XG <= a * np.sqrt(T[k])
            return float(np.trapezoid(g[m], XG[m]))
        a = brentq(lambda a: below_prob(a) - pi_b[k], -9.0, THETA_MAX + 3, xtol=1e-10)
        spent += below_prob(a)
        out.append({"look": k + 1, "t": T[k], "a_Z": a,
                    "beta_incremental": pi_b[k], "beta_cumulative": spent})
        g = np.where((XG < u_eff[k]) & (XG > a * np.sqrt(T[k])), g, 0.0)
    return out, spent


def main():
    eff, spent = efficacy_boundaries()
    print("=" * 76)
    print("STEP-3 EFFICACY BOUNDARIES  (LOCKED)")
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
          f"{eff[-1]['b_Z']:.4f} vs fixed 1.9600 -> OBF-type ~1.01-1.02x max-info inflation.")

    fut, bspent = futility_boundaries(eff)
    print()
    print("=" * 76)
    print("PROVISIONAL FUTILITY BOUNDARIES  (non-binding; FOR EXTERNAL REVIEW)")
    print(f"one-sided sfLDOF beta-spending, BETA={BETA}; calibrating drift "
          f"THETA_MAX={THETA_MAX:.4f} (=z_.975+z_.90, 90% power at the design")
    print("alternative). BOTH inputs are review items, not ruled constants.")
    print("=" * 76)
    print(f"{'look':>4} {'t':>6} {'Z-lower a_k':>12} {'beta incr':>12} {'beta cum':>10}")
    for f in fut:
        print(f"{f['look']:>4} {f['t']:>6.2f} {f['a_Z']:>12.4f} "
              f"{f['beta_incremental']:>12.6g} {f['beta_cumulative']:>10.5f}")
    print("-" * 76)
    print(f"VALIDATION: cumulative beta spent = {bspent:.6f} (target {BETA}), "
          f"non-binding (efficacy bounds in place).")
    print("NOTE: futility a_k is a STOP-RECOMMENDATION threshold escalated to the")
    print("supervisor (D-054e / D-058) — never automatic. Provisional pending review.")


if __name__ == "__main__":
    main()
