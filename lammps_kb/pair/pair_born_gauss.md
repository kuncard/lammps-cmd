---
id: pair_born_gauss
title: "pair_style born/gauss command"
url: https://docs.lammps.org/pair_born_gauss.html
---

# pair_style born/gauss command

## Syntax

```
pair_style born/gauss cutoff
```

## Description

Added in version 28Mar2023.

Pair style born/gauss computes pairwise interactions from a combination of a Born-Mayer
repulsive term and a Gaussian attractive term according to (Bomont):

\[E = A_0 \exp \left( -\alpha r \right) - A_1 \exp\left[ -\beta \left(r - r_0 \right)^2 \right]
    \qquad r < r_c\]

\(r_c\) is the cutoff.

The following coefficients must be defined for each pair of atoms
types via the pair_coeff command as in the examples
above, or in the data file or restart files read by the
read_data or read_restart
commands:

The last coefficient is optional.  If not specified, the global cutoff is used.

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
pair_style born/gauss 10.0
pair_coeff 1 1 8.2464e13 12.48 0.042644277 0.44 3.56
```

## Restrictions

Restrictions 
This pair style is only enabled if LAMMPS was built with the EXTRA-PAIR
package.  See the Build package page for more
info.

## Related Commands

- [pair_coeff](pair_coeff.html)
- [pair_style born](pair_born.html)

