---
id: pair_yukawa
title: "pair_style yukawa command"
url: https://docs.lammps.org/pair_yukawa.html
---

# pair_style yukawa command

## Syntax

```
pair_style yukawa kappa cutoff
```

## Description

Style yukawa computes pairwise interactions with the formula

\[E = A \frac{e^{- \kappa r}}{r} \qquad r < r_c\]

\(r_c\) is the cutoff.

The following coefficients must be defined for each pair of atoms
types via the pair_coeff command as in the examples
above, or in the data file or restart files read by the
read_data or read_restart
commands, or by mixing as described below:

The last coefficient is optional.  If not specified, the global yukawa
cutoff is used.

Styles with a gpu, intel, kk, omp, or opt suffix are
functionally the same as the corresponding style without the suffix.
They have been optimized to run faster, depending on your available
hardware, as discussed on the Accelerator packages
page.  The accelerated styles take the same arguments and should
produce the same results, except for round-off and precision issues.

These accelerated styles are part of the GPU, INTEL, KOKKOS,
OPENMP, and OPT packages, respectively.  They are only enabled if
LAMMPS was built with those packages.  See the Build package page for more info.

You can specify the accelerated styles explicitly in your input script
by including their suffix, or you can use the -suffix command-line switch when you invoke LAMMPS, or you can use the
suffix command in your input script.

See the Accelerator packages page for more
instructions on how to use the accelerated styles effectively.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
pair_style yukawa 2.0 2.5
pair_coeff 1 1 100.0 2.3
pair_coeff * * 100.0
```

## Restrictions

Restrictions 
none

## Related Commands

- [pair_coeff](pair_coeff.html)

