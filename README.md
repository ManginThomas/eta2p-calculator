# Eta²p Calculator

A lightweight graphical application for computing ANOVA effect sizes from F-statistics.

The application computes:

* Partial eta-squared (η²p)
* Confidence intervals for η²p
* Cohen's f
* Exact p-values

from ANOVA F statistics and degrees of freedom.

---

# Download

Latest release:

https://github.com/ManginThomas/eta2p-calculator/releases/latest

Available for:

* Windows
* macOS

No installation is required.

---

# Input Parameters

The user provides:

* F statistic
* Numerator degrees of freedom (df₁)
* Denominator degrees of freedom (df₂)
* Confidence level (e.g., 90%, 95%, 99%)
* Confidence interval type (one-sided or two-sided)

---

# Statistical Background

## Partial Eta-Squared

Partial eta-squared is computed directly from the F statistic:

```text
η²p = (F × df₁) / (F × df₁ + df₂)
```

where:

* F = observed F statistic
* df₁ = numerator degrees of freedom
* df₂ = denominator degrees of freedom

This measure represents the proportion of variance explained by the effect after removing variance attributable to other effects.

---

## Cohen's f

Cohen's f is derived from η²p (as in G*Power):

```text
f = √(η²p / (1 − η²p))
```

Common benchmarks:

| Effect size | Cohen's f |
| ----------- | --------- |
| Small       | 0.10      |
| Medium      | 0.25      |
| Large       | 0.40      |

(Cohen, 1988)

---

## p-value

The exact p-value is computed from the upper tail of the F distribution:

```text
p = P(F(df₁,df₂) ≥ Fobserved)
```

---

# Confidence Intervals

## Method

Confidence intervals are computed using inversion of the noncentral F distribution.

This is the same general approach used by:

* R package effectsize

The procedure is:

1. Compute the observed F statistic.
2. Estimate lower and upper confidence limits of the noncentrality parameter (λ).
3. Transform these limits into partial eta-squared confidence limits.
4. Restrict the resulting interval to the theoretical range [0,1].

---

## Two-Sided Confidence Intervals

The calculator can compute true two-sided confidence intervals.

Example:

Input:

```text
F = 5
df₁ = 1
df₂ = 60
95% CI
```

Output:

```text
η²p = 0.077
95% CI = [0.000 ; 0.224]
```

This result matches:

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

## One-Sided Confidence Intervals

The calculator can also reproduce the default behaviour of the R package effectsize.

Example:

```R
effectsize::F_to_eta2(
  f = 5,
  df = 1,
  df_error = 60,
  ci = 0.95
)
```

returns:

```text
η²p = 0.077
95% CI = [0.000 ; 1.000]
```

The software provides this option for compatibility with published analyses and existing workflows.

---

# Validation

Results have been verified against:

* R package effectsize



---

# Software Requirements

Standalone executables are available for:

* Windows
* macOS

## macOS Security Warning

Because this application is distributed without an Apple Developer certificate,
macOS may prevent it from opening the first time.

If this happens:

1. Right-click on `eta2p_calculator.app`
2. Select **Open**
3. Confirm the dialog

If macOS still blocks the application, open Terminal and run:

```bash
xattr -rd com.apple.quarantine eta2p_calculator.app
```
or, if the file is in the download
```bash
cd ~/Downloads && xattr -rd com.apple.quarantine eta2p_calculator.app
```

Then launch the application again.

For users wishing to run the source code:

```bash
pip install scipy
python eta2p_calculator.py
```

