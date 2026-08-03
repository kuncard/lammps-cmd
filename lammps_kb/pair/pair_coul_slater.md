---
id: pair_coul_slater
title: "pair_style coul/slater command"
url: https://docs.lammps.org/pair_coul_slater.html
---

# pair_style coul/slater command

## Syntax

```
pair_style coul/slater/cut lambda cutoff
pair_style coul/slater/long lambda cutoff
```

## Description

Styles coul/slater/* compute electrostatic interactions in mesoscopic models
which employ potentials without explicit excluded-volume interactions.
The goal is to prevent artificial ionic pair formation by including a charge
distribution in the Coulomb potential, following the formulation of
(Melchor):

\[E  =  \frac{Cq_iq_j}{\epsilon r} \left( 1- \left( 1 + \frac{r_{ij}}{\lambda} exp\left( -2r_{ij}/\lambda \right) \right) \right)                       \qquad r < r_c\]

where \(r_c\) is the cutoff distance and \(\lambda\) is the decay length of the charge.
C is the same Coulomb conversion factor as in the pair_styles coul/cut and coul/long. In this way the Coulomb
interaction between ions is corrected at small distances r.
For the coul/slater/cut style, the potential energy for distances larger than the cutoff is zero,
while for the coul/slater/long, the long-range interactions are computed either by the Ewald or the PPPM technique.

Phenomena that can be captured at a mesoscopic level using this type of electrostatic
interactions include the formation of polyelectrolyte-surfactant aggregates,
charge stabilization of colloidal suspensions, and the formation of
complexes driven by charged species in biological systems. (Vaiwala).

The cutoff distance is optional. If it is not used,
the default global value specified in the pair_style command is used.
For each pair of atom types, a specific cutoff distance can be defined via the pair_coeff command as in the example
above, or in the data file or restart files read by the
read_data or read_restart
commands:

The global decay length of the charge (\(\lambda\)) specified in the pair_style command is used for all pairs.

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
pair_style coul/slater/cut 1.0 3.5
pair_coeff * *
pair_coeff 2 2 2.5

pair_style coul/slater/long 1.0 12.0
pair_coeff * *
pair_coeff 1 1 5.0
```

## Restrictions

Restrictions 
The  coul/slater/long style requires the long-range solvers included in the KSPACE package.
These styles are part of the EXTRA-PAIR package.  They are only enabled if
LAMMPS was built with that package.  See the Build package page for more info.

## Related Commands

- [pair_coeff](pair_coeff.html)
- [pair_style, hybrid/overlay](pair_hybrid.html)
- [kspace_style](kspace_style.html)

