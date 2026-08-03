---
id: pair_gauss
title: "pair_style gauss command"
url: https://docs.lammps.org/pair_gauss.html
---

# pair_style gauss command

## Syntax

```
pair_style gauss cutoff
pair_style gauss/cut cutoff
```

## Description

Style gauss computes a tethering potential of the form

\[E = - A \exp(-B r^2) \qquad r < r_c\]

between an atom and its corresponding tether site which will typically
be a frozen atom in the simulation.  \(r_c\) is the cutoff.

The following coefficients must be defined for each pair of atom types
via the pair_coeff command as in the examples above,
or in the data file or restart files read by the
read_data or read_restart
commands:

The last coefficient is optional. If not specified, the global cutoff
is used.

Style gauss/cut computes a generalized Gaussian interaction potential
between pairs of particles:

\[E = \frac{H}{\sigma_h\sqrt{2\pi}} \exp\left[-\frac{(r-r_{mh})^2}{2\sigma_h^2}\right]\]

where H determines together with the standard deviation \(\sigma_h\)
the peak height of the Gaussian function, and \(r_{mh}\) the peak
position.  Examples of the use of the Gaussian potentials include
implicit solvent simulations of salt ions (Lenart) and
of surfactants (Jusufi).  In these instances the
Gaussian potential mimics the hydration barrier between a pair of
particles. The hydration barrier is located at \(r_{mh}\) and has a
width of \(\sigma_h\). The prefactor determines the height of the
potential barrier.

The following coefficients must be defined for each pair of atom types
via the pair_coeff command as in the example above,
or in the data file or restart files read by the
read_data or read_restart
commands:

The last coefficient is optional. If not specified, the global cutoff
is used.

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
pair_style gauss 12.0
pair_coeff * * 1.0 0.9
pair_coeff 1 4 1.0 0.9 10.0

pair_style gauss/cut 3.5
pair_coeff 1 4 0.2805 1.45 0.112
```

## Restrictions

Restrictions 
The gauss and gauss/cut styles are part of the EXTRA-PAIR package.
They are only enabled if LAMMPS is build with that package.  See the
Build package page for more info.

Changed in version 28Mar2023.

Prior to this version, the gauss pair style did not apply
special_bonds factors.

## Related Commands

- [pair_coeff](pair_coeff.html)
- [pair_style coul/diel](pair_coul_diel.html)

