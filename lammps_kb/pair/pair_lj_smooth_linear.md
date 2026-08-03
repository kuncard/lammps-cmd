---
id: pair_lj_smooth_linear
title: "pair_style lj/smooth/linear command"
url: https://docs.lammps.org/pair_lj_smooth_linear.html
---

# pair_style lj/smooth/linear command

## Syntax

```
pair_style lj/smooth/linear cutoff
```

## Description

Style lj/smooth/linear computes a truncated and force-shifted LJ
interaction (aka Shifted Force Lennard-Jones) that combines the
standard 12/6 Lennard-Jones function and subtracts a linear term based
on the cutoff distance, so that both, the potential and the force, go
continuously to zero at the cutoff \(r_c\) (Toxvaerd):

\[\begin{split}\phi\left(r\right) & =  4 \epsilon \left[ \left(\frac{\sigma}{r}\right)^{12} -
                    \left(\frac{\sigma}{r}\right)^6 \right] \\
E\left(r\right) & =  \phi\left(r\right)  - \phi\left(r_c\right) - \left(r - r_c\right) \left.\frac{d\phi}{d r} \right|_{r=r_c}       \qquad r < r_c\end{split}\]

The following coefficients must be defined for each pair of atoms
types via the pair_coeff command as in the examples
above, or in the data file or restart files read by the
read_data or read_restart
commands, or by mixing as described below:

The last coefficient is optional. If not specified, the global
LJ cutoff specified in the pair_style command is used.

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
pair_style lj/smooth/linear 2.5
pair_coeff * * 1.0 1.0
pair_coeff 1 1 0.3 3.0 9.0
```

## Restrictions

Restrictions 
This pair style is part of the EXTRA-PAIR package.  It is only enabled if
LAMMPS was built with that package.  See the
Build package page for more info.

## Related Commands

- [pair_coeff](pair_coeff.html)
- [pair lj/smooth](pair_lj_smooth.html)

