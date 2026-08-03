---
id: pair_lj_cubic
title: "pair_style lj/cubic command"
url: https://docs.lammps.org/pair_lj_cubic.html
---

# pair_style lj/cubic command

## Syntax

```
pair_style lj/cubic
```

## Description

The lj/cubic style computes a truncated LJ interaction potential
whose energy and force are continuous everywhere.  Inside the
inflection point the interaction is identical to the standard 12/6
Lennard-Jones potential.  The LJ function outside the
inflection point is replaced with a cubic function of distance. The
energy, force, and second derivative are continuous at the inflection
point.  The cubic coefficient A3 is chosen so that both energy and
force go to zero at the cutoff distance.  Outside the cutoff distance
the energy and force are zero.

\[\begin{split}E & = u_{LJ}(r) \qquad r \leq r_s \\
  & = u_{LJ}(r_s) + (r-r_s) u'_{LJ}(r_s) - \frac{1}{6} A_3 (r-r_s)^3 \qquad r_s < r \leq r_c \\
  & = 0 \qquad r > r_c\end{split}\]

The location of the inflection point \(r_s\) is defined by the LJ
diameter, \(r_s/\sigma = (26/7)^{1/6}\). The cutoff distance is
defined by \(r_c/r_s = 67/48\) or \(r_c/\sigma = 1.737...\) The
analytic expression for the cubic coefficient \(A_3
r_{min}^3/\epsilon = 27.93...\) is given in the paper by Holian and
Ravelo (Holian).

This potential is commonly used to study the shock mechanics of FCC
solids, as in Ravelo et al. (Ravelo).

The following coefficients must be defined for each pair of atom types
via the pair_coeff command as in the example above,
or in the data file or restart files read by the
read_data or read_restart
commands, or by mixing as described below:

Note that \(\sigma\) is defined in the LJ formula as the
zero-crossing distance for the potential, not as the energy minimum,
which is located at \(r_{min} = 2^{\frac{1}{6}} \sigma\). In the
above example, \(\sigma = 0.8908987\), so \(r_{min} = 1.0\).

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
pair_style lj/cubic
pair_coeff * * 1.0 0.8908987
```

## Restrictions

Restrictions 
This pair style is part of the EXTRA-PAIR package.  It is only enabled if
LAMMPS was built with that package.  See the
Build package page for more info.

## Related Commands

- [pair_coeff](pair_coeff.html)

