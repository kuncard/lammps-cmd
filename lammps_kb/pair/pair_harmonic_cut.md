---
id: pair_harmonic_cut
title: "pair_style harmonic/cut command"
url: https://docs.lammps.org/pair_harmonic_cut.html
---

# pair_style harmonic/cut command

## Syntax

```
pair_style style
```

## Description

Added in version 17Feb2022.

Style harmonic/cut computes pairwise repulsive-only harmonic interactions with the formula

\[E = k (r_c - r)^2  \qquad r < r_c\]

where \(r_c\) is the cutoff.  Note that the usual 1/2 factor is
included in \(k\).

The following coefficients must be defined for each pair of atoms
types via the pair_coeff command as in the examples
above, or in the data file or restart files read by the
read_data or read_restart
commands:

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
pair_style harmonic/cut
pair_coeff * * 0.2 2.0
pair_coeff 1 1 0.5 2.5
```

## Restrictions

Restrictions 
The harmonic/cut pair style is only enabled if LAMMPS was
built with the EXTRA-PAIR package.
See the Build package page for more info.

## Related Commands

- [pair_coeff](pair_coeff.html)

