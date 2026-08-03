---
id: pair_buck6d_coul_gauss
title: "pair_style buck6d/coul/gauss/dsf command"
url: https://docs.lammps.org/pair_buck6d_coul_gauss.html
---

# pair_style buck6d/coul/gauss/dsf command

## Syntax

```
pair_style style args
buck6d/coul/gauss/dsf args = smooth cutoff (cutoff2)
  smooth  = smoothing onset within Buckingham cutoff (ratio)
  cutoff  = global cutoff for Buckingham (and Coulombic if only 1 arg) (distance units)
  cutoff2 = global cutoff for Coulombic (optional) (distance units)
buck6d/coul/gauss/long args = smooth smooth2 cutoff (cutoff2)
  smooth   = smoothing onset within Buckingham cutoff (ratio)
  smooth2  = smoothing onset within Coulombic cutoff (ratio)
  cutoff   = global cutoff for Buckingham (and Coulombic if only 1 arg) (distance units)
  cutoff2  = global cutoff for Coulombic (optional) (distance units)
```

## Description

The buck6d/coul/gauss styles evaluate vdW and Coulomb
interactions following the MOF-FF force field after
(Schmid). The vdW term of the buck6d styles
computes a dispersion damped Buckingham potential:

\[\begin{split}E = A e^{-\kappa r} - \frac{C}{r^6} \cdot \frac{1}{1 + D r^{14}} \qquad r < r_c \\\end{split}\]

where A and C are a force constant, \(\kappa\) is an ionic-pair dependent
reciprocal length parameter, D is a dispersion correction parameter,
and the cutoff \(r_c\) truncates the interaction distance.
The first term in the potential corresponds to the Buckingham
repulsion term and the second term to the dispersion attraction with
a damping correction analog to the Grimme correction used in DFT.
The latter corrects for artifacts occurring at short distances which
become an issue for soft vdW potentials.

The buck6d styles include a smoothing function which is invoked
according to the global smoothing parameter within the specified
cutoff.  Hereby a parameter of i.e. 0.9 invokes the smoothing
within 90% of the cutoff.  No smoothing is applied at a value
of 1.0. For the gauss/dsf style this smoothing is only applicable
for the dispersion damped Buckingham potential. For the gauss/long
styles the smoothing function can also be invoked for the real
space coulomb interactions which enforce continuous energies and
forces at the cutoff.

Both styles buck6d/coul/gauss/dsf and buck6d/coul/gauss/long
evaluate a Coulomb potential using spherical Gaussian type charge
distributions which effectively dampen electrostatic interactions
for high charges at close distances.  The electrostatic potential
is thus evaluated as:

\[E = \frac{C_{q_i q_j}}{\epsilon r_{ij}}\,\, \textrm{erf}\left(\alpha_{ij} r_{ij}\right)\quad\quad\quad r < r_c\]

where C is an energy-conversion constant, \(q_i\) and \(q_j\)
are the charges on the two atoms, epsilon is the dielectric constant which
can be set by the dielectric command, \(\alpha\)
is the ion pair dependent damping parameter and erf() is the
error-function.  The cutoff \(r_c\) truncates the interaction distance.

The style buck6d/coul/gauss/dsf computes the Coulomb interaction
via the damped shifted force model described in (Fennell)
approximating an Ewald sum similar to the pair coul/dsf
styles. In buck6d/coul/gauss/long an additional damping factor is
applied to the Coulombic term so it can be used in conjunction with the
kspace_style command and its ewald or pppm
options. The Coulombic cutoff in this case separates the real and
reciprocal space evaluation of the Ewald sum.

If one cutoff is specified it is used for both the vdW and Coulomb
terms.  If two cutoffs are specified, the first is used as the cutoff
for the vdW terms, and the second is the cutoff for the Coulombic term.

The following coefficients must be defined for each pair of atoms
types via the pair_coeff command as in the examples
above, or in the data file or restart files read by the
read_data or read_restart
commands:

The second coefficient, \(\rho\), must be greater than zero. The
latter coefficient is optional.  If not specified, the global vdW cutoff
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
pair_style buck6d/coul/gauss/dsf    0.9000    12.0000
pair_coeff 1  1  1030.  3.061  457.179  4.521  0.608

pair_style buck6d/coul/gauss/long   0.9000  1.0000  12.0000
pair_coeff 1  1  1030.  3.061  457.179  4.521  0.608
```

## Restrictions

Restrictions 
These styles are part of the MOFFF package.  They are only
enabled if LAMMPS was built with that package.  See the Build package page for more info.

## Related Commands

- [pair_coeff](pair_coeff.html)

