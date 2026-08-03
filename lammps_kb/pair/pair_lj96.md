---
id: pair_lj96
title: "pair_style lj96/cut command"
url: https://docs.lammps.org/pair_lj96.html
---

# pair_style lj96/cut command

## Syntax

```
pair_style lj96/cut cutoff
```

## Description

The lj96/cut style compute a 9/6 Lennard-Jones potential, instead
of the standard 12/6 potential, given by

\[E = 4 \epsilon \left[ \left(\frac{\sigma}{r}\right)^{9} -
\left(\frac{\sigma}{r}\right)^6 \right]
                    \qquad r < r_c\]

\(r_c\) is the cutoff.

The following coefficients must be defined for each pair of atoms
types via the pair_coeff command as in the examples
above, or in the data file or restart files read by the
read_data or read_restart
commands, or by mixing as described below:

The last coefficient is optional.  If not specified, the global LJ
cutoff specified in the pair_style command is used.

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
pair_style lj96/cut 2.5
pair_coeff * * 1.0 1.0 4.0
pair_coeff 1 1 1.0 1.0
```

## Restrictions

Restrictions 
This pair style is part of the EXTRA-PAIR package.  It is only enabled if
LAMMPS was built with that package.  See the
Build package page for more info.

## Related Commands

- [pair_coeff](pair_coeff.html)

