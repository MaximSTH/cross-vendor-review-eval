# Step-3 group-sequential boundary constants — NAMED-TOOL canonical run (pre-reg §3.7).
# gsDesign (Keaven Anderson); cross-validated by boundary_constants.py.
#
# LOCKED efficacy constants (D-054 a,c,d,f): two-sided alpha=0.05,
# O'Brien-Fleming-type Lan-DeMets spending (sfLDOF), K=4 at t=.25/.5/.75/1.
#
# LOCKED futility constants (D-060, ratifying the 2026-07-29 external review's
# §3.4 proposal): NON-BINDING beta-spending lower bound (test.type=4),
# beta=0.10 at the calibrating alternative delta*=0.30 (nuisance p_A2=0.05,
# p_B=0.35), one-sided sfLDOF beta-spending on the shared timing grid.
# This supersedes the earlier test.type=6 run (D-059c): test.type=6 is an
# H0-spent (astar) lower bound, not beta-spending — a different boundary
# concept, not a calibration variant. Its output (including its spurious
# "inflation" figure, an artifact of that mislabeled design) is QUARANTINED.
#
# Directional precedence (D-059d): the futility zone is Z in (-b_k, a_k];
# Z <= -b_k is a reverse-direction efficacy crossing and takes precedence.
# Under D-060 the a_k are recommendation thresholds (escalated, never
# automatic), applied only at looks with >= 8 observed discordant pairs.
#   Run:  Rscript boundary_constants.R
suppressMessages(library(gsDesign))

cat("== gsDesign", as.character(packageVersion("gsDesign")), "==\n\n")

## LOCKED efficacy boundaries — two-sided symmetric (test.type = 2)
eff <- gsDesign(k = 4, test.type = 2, alpha = 0.025,        # one-sided 0.025 = two-sided 0.05
                sfu = sfLDOF, timing = c(.25, .50, .75, 1))
cat("LOCKED efficacy Z-bounds (sfLDOF, two-sided 0.05):\n")
print(round(eff$upper$bound, 4))
cat("nominal two-sided p per look:\n")
print(signif(2 * (1 - pnorm(eff$upper$bound)), 6))
cat("cumulative alpha spent:\n")
print(signif(cumsum(eff$upper$prob[, 1]), 6))
cat("\n")

## LOCKED non-binding beta-spending futility (test.type = 4) — D-060 calibration:
## beta = 0.10 (90% power at delta* = 0.30 under p_A2=0.05/p_B=0.35), sfLDOF
## beta-spending, shared timing grid. Non-binding: efficacy bounds computed
## ignoring the lower bound, so they must reproduce the LOCKED set unchanged.
fut <- gsDesign(k = 4, test.type = 4, alpha = 0.025, beta = 0.10,
                sfu = sfLDOF, sfl = sfLDOF, timing = c(.25, .50, .75, 1))
cat("test.type=4 efficacy Z-bounds (must equal LOCKED):\n")
print(round(fut$upper$bound, 4))
stopifnot(max(abs(fut$upper$bound - eff$upper$bound)) < 1e-6)
cat("-> efficacy reproduction check PASS (<1e-6)\n\n")
cat("LOCKED futility Z-bounds (lower, non-binding beta-spending):\n")
print(round(fut$lower$bound, 4))
cat("cumulative beta spent at delta*:\n")
print(signif(cumsum(fut$lower$prob[, 2]), 6))
cat("max information inflation vs fixed-n (test.type=4):\n")
print(round(fut$n.I[4], 4))
