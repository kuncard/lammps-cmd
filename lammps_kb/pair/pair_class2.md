---
id: pair_class2
title: "pair_style lj/class2 command"
url: https://docs.lammps.org/pair_class2.html
---

# pair_style lj/class2 command

## Syntax

```
pair_style style args
lj/class2 args = cutoff
  cutoff = global cutoff for class 2 interactions (distance units)
lj/class2/coul/cut args = cutoff (cutoff2)
  cutoff = global cutoff for class 2 (and Coulombic if only 1 arg) (distance units)
  cutoff2 = global cutoff for Coulombic (optional) (distance units)
lj/class2/coul/long args = cutoff (cutoff2)
  cutoff = global cutoff for class 2 (and Coulombic if only 1 arg) (distance units)
  cutoff2 = global cutoff for Coulombic (optional) (distance units)
```

## Description

The lj/class2 styles compute a 6/9 Lennard-Jones potential given by

\[E = \epsilon \left[ 2 \left(\frac{\sigma}{r}\right)^9 -
  3 \left(\frac{\sigma}{r}\right)^6 \right]
\qquad r < r_c\]

\(r_c\) is the cutoff.

The lj/class2/coul/cut and lj/class2/coul/long styles add a
Coulombic term as described for the lj/cut pair styles.

See (Sun) for a description of the COMPASS class2 force field.

The following coefficients must be defined for each pair of atoms
types via the pair_coeff command as in the examples
above, or in the data file or restart files read by the
read_data or read_restart
commands, or by mixing as described below:

The latter 2 coefficients are optional.  If not specified, the global
class 2 and Coulombic cutoffs are used.  If only one cutoff is
specified, it is used as the cutoff for both class 2 and Coulombic
interactions for this type pair.  If both coefficients are specified,
they are used as the class 2 and Coulombic cutoffs for this type pair.
You cannot specify 2 cutoffs for style lj/class2, since it has no
Coulombic terms.

For lj/class2/coul/long only the class 2 cutoff can be specified
since a Coulombic cutoff cannot be specified for an individual I,J
type pair.  All type pairs use the same global Coulombic cutoff
specified in the pair_style command.

If the pair_coeff command is not used to define coefficients for a
particular I != J type pair, the mixing rule for \(\epsilon\) and
\(\sigma\) for all class2 potentials is to use the sixthpower
formulas documented by the pair_modify command.
The pair_modify mix setting is thus ignored for
class2 potentials for epsilon and sigma.  However it is still followed
for mixing the cutoff distance.

A version of these styles with a soft core, lj/cut/soft, suitable for use in
free energy calculations, is part of the FEP package and is documented with
the pair_style */soft styles. The version with soft core is
only available if LAMMPS was built with that package. See the Build package page for more info.

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
pair_style lj/class2 10.0
pair_coeff * * 100.0 2.5
pair_coeff 1 2* 100.0 2.5 9.0

pair_style lj/class2/coul/cut 10.0
pair_style lj/class2/coul/cut 10.0 8.0
pair_coeff * * 100.0 3.0
pair_coeff 1 1 100.0 3.5 9.0
pair_coeff 1 1 100.0 3.5 9.0 9.0

pair_style lj/class2/coul/long 10.0
pair_style lj/class2/coul/long 10.0 8.0
pair_coeff * * 100.0 3.0
pair_coeff 1 1 100.0 3.5 9.0
```

## Restrictions

Restrictions 
These styles are part of the CLASS2 package.  They are only enabled if
LAMMPS was built with that package.  See the Build package page for more info.

## Related Commands

- [pair_coeff](pair_coeff.html)
- [pair_style */soft](pair_fep_soft.html)

