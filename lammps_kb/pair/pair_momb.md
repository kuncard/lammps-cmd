---
id: pair_momb
title: "pair_style momb command"
url: https://docs.lammps.org/pair_momb.html
---

# pair_style momb command

## Syntax

```
pair_style momb cutoff s6 d
```

## Description

Style momb computes pairwise van der Waals (vdW) and short-range
interactions using the Morse potential and (Grimme) method
implemented in the Many-Body Metal-Organic (MOMB) force field
described comprehensively in (Fichthorn) and
(Zhou). Grimme s method is widely used to correct for
dispersion in density functional theory calculations.

\[\begin{split} E & = D_0 [\exp^{-2 \alpha (r-r_0)} - 2\exp^{-\alpha (r-r_0)}] - s_6 \frac{C_6}{r^6} f_{damp}(r,R_r) \\
f_{damp}(r,R_r) & = \frac{1}{1 + \exp^{-d(r/R_r - 1)}}\end{split}\]

For the momb pair style, the following coefficients must be defined
for each pair of atoms types via the pair_coeff
command as in the examples above, or in the data file or restart files
read by the read_data as described below:

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
pair_style momb 12.0 0.75 20.0
pair_style hybrid/overlay eam/fs lj/charmm/coul/long 10.0 12.0 momb 12.0 0.75 20.0 morse 5.5

pair_coeff 1 2 momb 0.0 1.0 1.0 10.2847 2.361
```

## Restrictions

Restrictions 
This style is part of the EXTRA-PAIR package. It is only enabled if
LAMMPS is built with that package. See the Build package page on for more info.

## Related Commands

- [pair_coeff](pair_coeff.html)
- [pair_style morse](pair_morse.html)

