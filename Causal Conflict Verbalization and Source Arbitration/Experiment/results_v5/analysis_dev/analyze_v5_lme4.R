# lme4 fits for the v5 verdict transplant (prereg §7.4). Model-based estimates only.
# Run on Colab:  Rscript analyze_v5_lme4.R long_v5.csv lme4_out.txt
suppressPackageStartupMessages(library(lme4))
args <- commandArgs(trailingOnly = TRUE)
d <- read.csv(args[1], stringsAsFactors = FALSE)
sink(args[2])
for (g in unique(paste(d$model_id, d$regime))) {
  s <- d[paste(d$model_id, d$regime) == g, ]
  s$K <- factor(s$k); contrasts(s$K) <- contr.sum(4)
  cat("\n=====", g, "=====\n")
  fit_lmm <- function(f) tryCatch(lmer(f, data = subset(s, outcome == "dl")), error = function(e) e)
  m <- fit_lmm(dl ~ D*B + D*O + K + (1 + D | item))
  if (inherits(m, "error") || isSingular(m)) { cat("lmer: by-item slope dropped\n"); m <- fit_lmm(dl ~ D*B + D*O + K + (1 | item)) }
  if (inherits(m, "error") || isSingular(m)) cat("lmer: FAILED (singular or error)\n") else print(summary(m))
  b <- subset(s, outcome == "beh" & !is.na(y_image))
  if (nrow(b) > 0) {
    ctl <- glmerControl(optimizer = "bobyqa", optCtrl = list(maxfun = 2e5))
    fit_glmm <- function(f) tryCatch(glmer(f, data = b, family = binomial, control = ctl), error = function(e) e)
    gm <- fit_glmm(y_image ~ D*B + D*O + (1 + D | item))  # behavioural rows use k = 1 only, so no K term
    if (inherits(gm, "error") || isSingular(gm)) { cat("glmer: by-item slope dropped\n"); gm <- fit_glmm(y_image ~ D*B + D*O + (1 | item)) }
    if (inherits(gm, "error") || isSingular(gm)) cat("glmer: FAILED (singular or error)\n") else print(summary(gm))
  }
}
cat("\n"); print(sessionInfo())
sink()
