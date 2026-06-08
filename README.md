# Eta²p Calculator

A lightweight graphical application for computing:

* Partial eta-squared (η²p)
* Confidence intervals for η²p
* Cohen's f
* Exact p-values

from ANOVA F-statistics and degrees of freedom.

The application is available for Windows and macOS through the Releases page.

---

# Input Parameters

The user must provide:

* F statistic
* Numerator degrees of freedom (df₁)
* Denominator degrees of freedom (df₂)
* Confidence level (e.g., 90%, 95%, 99%)

---

# Statistical Background

## Partial Eta-Squared

Partial eta-squared is computed directly from the F statistic:

[
\eta_p^2 = \frac{F \times df_1}{F \times df_1 + df_2}
]

where:

* (F) is the observed F statistic
* (df_1) is the numerator degrees of freedom
* (df_2) is the denominator degrees of freedom

This measure represents the proportion of variance explained by the effect after removing variance attributable to other effects.

---

## Cohen's f

Cohen's f is derived from η²p as:

[
f = \sqrt{\frac{\eta_p^2}{1-\eta_p^2}}
]

Common benchmarks:

| Effect size | Cohen's f |
| ----------- | --------- |
| Small       | 0.10      |
| Medium      | 0.25      |
| Large       | 0.40      |

(Cohen, 1988)

---

## p-value

The exact p-value is computed from the F distribution:

[
p = P(F_{df_1,df_2} \geq F_{obs})
]

using the upper tail of the central F distribution.

---

# Confidence Intervals

## Method

Confidence intervals are obtained using the noncentral F distribution inversion method.

This approach is the same method used by:

* MBESS
* effectsize
* ESCI
* SPSS confidence interval procedures for effect sizes

and is currently considered the reference approach for ANOVA effect size confidence intervals.

The procedure:

1. Compute the observed F statistic.
2. Find the lower and upper noncentrality parameters ((\lambda_L) and (\lambda_U)) such that:

[
P(F_{nc} \leq F_{obs})
======================

\alpha/2
]

and

[
P(F_{nc} \leq F_{obs})
======================

1-\alpha/2
]

3. Convert the resulting confidence limits on the noncentrality parameter into limits on partial eta-squared:

[
\eta_{p,L}^2
============

\frac{\lambda_L}
{\lambda_L + df_1 + df_2 + 1}
]

[
\eta_{p,U}^2
============

\frac{\lambda_U}
{\lambda_U + df_1 + df_2 + 1}
]

The resulting interval is then truncated to the theoretical range:

[
0 \le \eta_p^2 \le 1
]

---
## Confidence Interval Type

The software allows computation of:

- Two-sided confidence intervals
- One-sided confidence intervals (effectsize-compatible)

The one-sided interval reproduces the default behaviour of:

effectsize::F_to_eta2()

The two-sided interval reproduces:

effectsize::F_to_eta2(
  alternative = "two.sided"
)

## Two-Sided Confidence Intervals

The software computes true two-sided confidence intervals.

For example:

Input:

* F = 5
* df₁ = 1
* df₂ = 60
* 95% CI

Output:

[
\eta_p^2 = 0.077
]

[
95%~CI = [0.000,\ 0.224]
]

These values match those returned by:

```R
effectsize::F_to_eta2(
  f = 5,
  df = 1,
  df_error = 60,
  ci = 0.95,
  alternative = "two.sided"
)
```

---

# Validation

Results have been verified against:

* R package effectsize

---

# Software Requirements

No installation is required.

Standalone executables are available for:

* Windows
* macOS

