---
id: pair_dispersion_d3
title: "pair_style dispersion/d3 command"
url: https://docs.lammps.org/pair_dispersion_d3.html
---

# pair_style dispersion/d3 command

## Syntax

```
pair_style dispersion/d3 damping functional cutoff cn_cutoff
```

## Description

Added in version 4Feb2025.

Style dispersion/d3 computes the dispersion energy-correction used in
the DFT-D3 method of Grimme (Grimme1).  It would
typically be used with a machine learning (ML) potential that was
trained with results from plain DFT calculations without the dispersion
correction through pair_style hybrid/overlay. ML potentials are often
combined a posteriori with dispersion energy-correction schemes (see
e.g. (Qamar) and (Batatia)).

The energy contribution \(E_i\) for an atom \(i\) is given by:

\[E_i = \frac{1}{2} \sum_{j \neq i} \big(
             s_6 \frac{C_{6,ij}}{r^6_{ij}} f_6^{damp}(r_{ij}) +
             s_8 \frac{C_{8,ij}}{r^8_{ij}} f_8^{damp}(r_{ij}) \big)\]

where \(C_n\) is the averaged, geometry-dependent nth-order
dispersion coefficient for atom pair \(ij\), \(r_{ij}\) their
inter-nuclear distance, \(s_n\) are XC functional-dependent scaling
factor, and \(f_n^{damp}\) are damping functions.

Note
It is currently not possible to calculate three-body dispersion
contributions, according to, for example, the Axilrod-Teller-Muto
model.

Changed in version 2Apr2025: renamed zero keyword to original to avoid conflicts with
pair style zero when used as hybrid
sub-style.

Available damping functions are the original  zero-damping  (original)
(Grimme1), Becke-Johnson damping (bj) (Grimme2), and their revised forms (zerom and bjm, respectively)
(Sherrill).

Available XC functional scaling factors are listed in the table below,
and depend on the selected damping function.

This style is primarily supposed to be used combined with a
machine-learned interatomic potential trained on a DFT dataset (the
selected XC functional should be chosen accordingly) via the
pair_style hybrid command.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
pair_style dispersion/d3 original pbe 30.0 20.0
pair_coeff * * C
```

## Restrictions

Restrictions 
Style dispersion/d3 is part of the EXTRA-PAIR package. It is only
enabled if LAMMPS was built with that package.  See the Build
package page for more info.
The compiled in parameters require the use of metal units.
It is currently not possible to calculate three-body dispersion
contributions according to, for example, the Axilrod-Teller-Muto model.

## Related Commands

- [pair_coeff](pair_coeff.html)

