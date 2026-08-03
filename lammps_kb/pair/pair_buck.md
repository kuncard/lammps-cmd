---
id: pair_buck
title: "pair_style buck command"
url: https://docs.lammps.org/pair_buck.html
---

# pair_style buck command

## Syntax

```
pair_style style args
buck args = cutoff
  cutoff = global cutoff for Buckingham interactions (distance units)
buck/coul/cut args = cutoff (cutoff2)
  cutoff = global cutoff for Buckingham (and Coulombic if only 1 arg) (distance units)
  cutoff2 = global cutoff for Coulombic (optional) (distance units)
buck/coul/long args = cutoff (cutoff2)
  cutoff = global cutoff for Buckingham (and Coulombic if only 1 arg) (distance units)
  cutoff2 = global cutoff for Coulombic (optional) (distance units)
buck/coul/msm args = cutoff (cutoff2)
  cutoff = global cutoff for Buckingham (and Coulombic if only 1 arg) (distance units)
  cutoff2 = global cutoff for Coulombic (optional) (distance units)
```

## Description

The buck style computes a Buckingham potential (exp/6 instead of
Lennard-Jones 12/6) given by

\[E = A e^{-r / \rho} - \frac{C}{r^6} \qquad r < r_c\]

where \(\rho\) is an ionic-pair dependent length parameter, and
\(r_c\) is the cutoff on both terms.

The styles with coul/cut or coul/long or coul/msm add a
Coulombic term as described for the lj/cut pair styles.
For buck/coul/long and buc/coul/msm, an additional damping factor
is applied to the Coulombic term so it can be used in conjunction with
the kspace_style command and its ewald or pppm
or msm option.  The Coulombic cutoff specified for this style means
that pairwise interactions within this distance are computed directly;
interactions outside that distance are computed in reciprocal space.

If one cutoff is specified for the born/coul/cut and
born/coul/long and born/coul/msm styles, it is used for both the
A,C and Coulombic terms.  If two cutoffs are specified, the first is
used as the cutoff for the A,C terms, and the second is the cutoff for
the Coulombic term.

Note that these potentials are related to the Born-Mayer-Huggins potential.

Note
For all these pair styles, the terms with A and C are always
cutoff.  The additional Coulombic term can be cutoff or long-range (no
cutoff) depending on whether the style name includes coul/cut or
coul/long or coul/msm.  If you wish the C/r^6 term to be long-range
(no cutoff), then see the pair_style buck/long/coul/long command.

The following coefficients must be defined for each pair of atoms
types via the pair_coeff command as in the examples
above, or in the data file or restart files read by the
read_data or read_restart
commands:

The second coefficient, \(\rho\), must be greater than zero.
The coefficients A, \(\rho\), and C can be written as analytical expressions
of \(\epsilon\) and \(\sigma\), in analogy to the Lennard-Jones potential
(Khrapak).

The latter 2 coefficients are optional.  If not specified, the global
A,C and Coulombic cutoffs are used.  If only one cutoff is specified,
it is used as the cutoff for both A,C and Coulombic interactions for
this type pair.  If both coefficients are specified, they are used as
the A,C and Coulombic cutoffs for this type pair.  You cannot specify
2 cutoffs for style buck, since it has no Coulombic terms.
For buck/coul/long only the LJ cutoff can be specified since a
Coulombic cutoff cannot be specified for an individual I,J type pair.
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
pair_style buck 2.5
pair_coeff * * 100.0 1.5 200.0
pair_coeff * * 100.0 1.5 200.0 3.0

pair_style buck/coul/cut 10.0
pair_style buck/coul/cut 10.0 8.0
pair_coeff * * 100.0 1.5 200.0
pair_coeff 1 1 100.0 1.5 200.0 9.0
pair_coeff 1 1 100.0 1.5 200.0 9.0 8.0

pair_style buck/coul/long 10.0
pair_style buck/coul/long 10.0 8.0
pair_coeff * * 100.0 1.5 200.0
pair_coeff 1 1 100.0 1.5 200.0 9.0

pair_style buck/coul/msm 10.0
pair_style buck/coul/msm 10.0 8.0
pair_coeff * * 100.0 1.5 200.0
pair_coeff 1 1 100.0 1.5 200.0 9.0
```

## Restrictions

Restrictions 
The buck/coul/long style is part of the KSPACE package.  They are
only enabled if LAMMPS was built with that package.  See the Build package page for more info.

## Related Commands

- [pair_coeff](pair_coeff.html)
- [pair_style born](pair_born.html)

