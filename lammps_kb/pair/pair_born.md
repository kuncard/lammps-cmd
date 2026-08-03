---
id: pair_born
title: "pair_style born command"
url: https://docs.lammps.org/pair_born.html
---

# pair_style born command

## Syntax

```
pair_style style args
born args = cutoff
  cutoff = global cutoff for non-Coulombic interactions (distance units)
born/coul/long args = cutoff (cutoff2)
  cutoff = global cutoff for non-Coulombic (and Coulombic if only 1 arg) (distance units)
  cutoff2 = global cutoff for Coulombic (optional) (distance units)
born/coul/msm args = cutoff (cutoff2)
  cutoff = global cutoff for non-Coulombic (and Coulombic if only 1 arg) (distance units)
  cutoff2 = global cutoff for Coulombic (optional) (distance units)
born/coul/wolf args = alpha cutoff (cutoff2)
  alpha = damping parameter (inverse distance units)
  cutoff = global cutoff for non-Coulombic (and Coulombic if only 1 arg) (distance units)
  cutoff2 = global cutoff for Coulombic (optional) (distance units)
born/coul/dsf args = alpha cutoff (cutoff2)
  alpha = damping parameter (inverse distance units)
  cutoff = global cutoff for non-Coulombic (and Coulombic if only 1 arg) (distance units)
  cutoff2 = global cutoff for Coulombic (distance units)
```

## Description

The born style computes the Born-Mayer-Huggins or Tosi/Fumi
potential described in (Fumi and Tosi), given by

\[E = A \exp \left(\frac{\sigma - r}{\rho} \right) -
\frac{C}{r^6} + \frac{D}{r^8} \qquad r < r_c\]

where \(\sigma\) is an interaction-dependent length parameter,
\(\rho\) is an ionic-pair dependent length parameter, and
\(r_c\) is the cutoff.

The styles with coul/long or coul/msm add a Coulombic term as
described for the lj/cut pair styles.  An additional
damping factor is applied to the Coulombic term so it can be used in
conjunction with the kspace_style command and its
ewald or pppm of msm option.  The Coulombic cutoff specified for
this style means that pairwise interactions within this distance are
computed directly; interactions outside that distance are computed in
reciprocal space.

If one cutoff is specified for the born/coul/long and
born/coul/msm style, it is used for both the A,C,D and Coulombic
terms.  If two cutoffs are specified, the first is used as the cutoff
for the A,C,D terms, and the second is the cutoff for the Coulombic
term.

The born/coul/wolf style adds a Coulombic term as described for the
Wolf potential in the coul/wolf pair style.

The born/coul/dsf style computes the Coulomb contribution with the
damped shifted force model as in the coul/dsf style.

Note that these potentials are related to the Buckingham potential.

The following coefficients must be defined for each pair of atoms
types via the pair_coeff command as in the examples
above, or in the data file or restart files read by the
read_data or read_restart
commands, or by mixing as described below:

The second coefficient, rho, must be greater than zero.

The last coefficient is optional.  If not specified, the global A,C,D
cutoff specified in the pair_style command is used.

For born/coul/long, born/coul/wolf and born/coul/dsf no
Coulombic cutoff can be specified for an individual I,J type pair.
All type pairs use the same global Coulombic cutoff specified in the
pair_style command.

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
pair_style born 10.0
pair_coeff * * 6.08 0.317 2.340 24.18 11.51
pair_coeff 1 1 6.08 0.317 2.340 24.18 11.51

pair_style born/coul/long 10.0
pair_style born/coul/long 10.0 8.
pair_coeff * * 6.08 0.317 2.340 24.18 11.51
pair_coeff 1 1 6.08 0.317 2.340 24.18 11.51

pair_style born/coul/msm 10.0
pair_style born/coul/msm 10.0 8.0
pair_coeff * * 6.08 0.317 2.340 24.18 11.51
pair_coeff 1 1 6.08 0.317 2.340 24.18 11.51

pair_style born/coul/wolf 0.25 10.0
pair_style born/coul/wolf 0.25 10.0 9.0
pair_coeff * * 6.08 0.317 2.340 24.18 11.51
pair_coeff 1 1 6.08 0.317 2.340 24.18 11.51

pair_style born/coul/dsf 0.1 10.0 12.0
pair_coeff * *   0.0 1.00 0.00 0.00 0.00
pair_coeff 1 1 480.0 0.25 0.00 1.05 0.50
```

## Restrictions

Restrictions 
The born/coul/long style is part of the KSPACE package.  It is only
enabled if LAMMPS was built with that package.  See the
Build package page for more info.
The born/coul/dsf and born/coul/wolf pair styles are part of the
EXTRA-PAIR package.  They are only enabled if LAMMPS was built with
that package.  See the Build package page
for more info.

## Related Commands

- [pair_coeff](pair_coeff.html)
- [pair_style buck](pair_buck.html)

