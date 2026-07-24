# Step-3 group-sequential boundary constants — NAMED-TOOL cross-check (pre-reg §3.7).
# gsDesign (Keaven Anderson) reproduction of boundary_constants.py.
# The LOCKED efficacy constants (D-054 a,c,d,f): two-sided alpha=0.05,
# O'Brien-Fleming-type Lan-DeMets spending (sfLDOF), K=4 at t=.25/.5/.75/1.
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

## PROVISIONAL non-binding futility (test.type = 6, beta-spending) — FOR REVIEW.
## Inputs NOT pinned by the rulings: beta and the futility spending shape.
prov <- gsDesign(k = 4, test.type = 6, alpha = 0.025, beta = 0.10,
                 sfu = sfLDOF, sfl = sfLDOF, timing = c(.25, .50, .75, 1))
cat("PROVISIONAL efficacy Z-bounds (test.type=6):\n"); print(round(prov$upper$bound, 4))
cat("PROVISIONAL futility Z-bounds (lower):\n");        print(round(prov$lower$bound, 4))
cat("max information inflation vs fixed-n:\n");         print(round(prov$n.I[4], 4))
