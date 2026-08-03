---
id: pair_lj_smooth
title: "pair_style lj/smooth command"
url: https://docs.lammps.org/pair_lj_smooth.html
---

# pair_style lj/smooth command

## Syntax

```
pair_style lj/smooth Rin Rc
```

## Description

Style lj/smooth computes a LJ interaction with a force smoothing
applied between the inner and outer cutoff.

\[\begin{split}E & =  4 \epsilon \left[ \left(\frac{\sigma}{r}\right)^{12} -
                      \left(\frac{\sigma}{r}\right)^6 \right]
                      \qquad r < r_{in} \\
F & =  C_1 + C_2 (r - r_{in}) + C_3 (r - r_{in})^2 + C_4 (r - r_{in})^3
                    \qquad r_{in} < r < r_c\end{split}\]

The polynomial coefficients C1, C2, C3, C4 are computed by LAMMPS to
cause the force to vary smoothly from the inner cutoff \(r_{in}\) to the
outer cutoff \(r_c\).

At the inner cutoff the force and its first derivative
will match the non-smoothed LJ formula.  At the outer cutoff the force
and its first derivative will be 0.0.  The inner cutoff cannot be 0.0.

Explicit expressions for the coefficients C1, C2, C3, C4, as well as the
energy discontinuity at the cutoff can be found here (Leoni_1)
and here (Leoni_2)

Note
this force smoothing causes the energy to be discontinuous both
in its values and first derivative.  This can lead to poor energy
conservation and may require the use of a thermostat.  The energy
value discontinuity can be eliminated by shifting the potential
energy to be zero at the outer cutoff using the pair_modify shift
option. With or without shifting, you can plot the resulting energy
and force via the pair_write command to see the effect.

The following coefficients must be defined for each pair of atoms
types via the pair_coeff command as in the examples
above, or in the data file or restart files read by the
read_data or read_restart
commands, or by mixing as described below:

The last 2 coefficients are optional inner and outer cutoffs.  If not
specified, the global values for \(r_{in}\) and \(r_c\) are used.

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
pair_style lj/smooth 8.0 10.0
pair_coeff * * 10.0 1.5
pair_coeff 1 1 20.0 1.3 7.0 9.0
```

## Restrictions

Restrictions 
This pair style is part of the EXTRA-PAIR package.  It is only enabled if
LAMMPS was built with that package.  See the
Build package page for more info.

## Related Commands

- [pair_coeff](pair_coeff.html)
- [pair lj/smooth/linear](pair_lj_smooth_linear.html)

