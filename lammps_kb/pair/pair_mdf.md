---
id: pair_mdf
title: "pair_style lj/mdf command"
url: https://docs.lammps.org/pair_mdf.html
---

# pair_style lj/mdf command

## Syntax

```
pair_style style args
lj/mdf args = cutoff1 cutoff2
  cutoff1 = inner cutoff for the start of the tapering function
  cutoff1 = out cutoff for the end of the tapering function
buck/mdf args = cutoff1 cutoff2
  cutoff1 = inner cutoff for the start of the tapering function
  cutoff1 = out cutoff for the end of the tapering function
lennard/mdf args = cutoff1 cutoff2
  cutoff1 = inner cutoff for the start of the tapering function
  cutoff1 = out cutoff for the end of the tapering function
```

## Description

The lj/mdf, buck/mdf and lennard/mdf compute the standard 12-6
Lennard-Jones and Buckingham potential with the addition of a taper
function that ramps the energy and force smoothly to zero between an
inner and outer cutoff.

\[E_{smooth}(r) = E(r)*f(r)\]

The tapering, f(r), is done by using the Mei, Davenport, Fernando
function (Mei).

\[\begin{split}f(r) & = 1.0  \qquad \qquad \mathrm{for} \qquad r < r_m \\
f(r) & = (1 - x)^3*(1+3x+6x^2) \quad \mathrm{for} \qquad r_m < r < r_{cut} \\
f(r) & = 0.0  \qquad \qquad \mathrm{for} \qquad  r >= r_{cut} \\\end{split}\]

where

\[x = \frac{(r-r_m)}{(r_{cut}-r_m)}\]

Here \(r_m\) is the inner cutoff radius and \(r_{cut}\) is the
outer cutoff radius.

For the lj/mdf pair_style, the potential energy, E(r), is the
standard 12-6 Lennard-Jones written in the epsilon/sigma form:

\[E(r) = 4 \epsilon \left[ \left(\frac{\sigma}{r}\right)^{12} -
                         \left(\frac{\sigma}{r}\right)^6 \right]\]

Either the first two or all of the following coefficients must be
defined for each pair of atoms types via the pair_coeff command as in
the examples above, or in the data file read by the read_data. The two cutoffs default to the global values and
\(\epsilon\) and \(\sigma\) can also be determined by mixing as
described below:

For the buck/mdf pair_style, the potential energy, E(r), is the
standard Buckingham potential with three required coefficients.
The two cutoffs can be omitted and default to the corresponding
global values:

\[E(r) = A e^{(-r/\rho)} -\frac{C}{r^6}\]

For the lennard/mdf pair_style, the potential energy, E(r), is the
standard 12-6 Lennard-Jones written in the A/B form:

\[E(r) = \frac{A}{r^{12}} - \frac{B}{r^{6}}\]

The following coefficients must be defined for each pair of atoms
types via the pair_coeff command as in the examples above, or in the
data file read by the read_data commands, or by mixing as described below.
The two cutoffs default to their global values and must be either both
given or both left out:

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
pair_style lj/mdf 2.5 3.0
pair_coeff * * 1.0 1.0
pair_coeff 1 1 1.1 2.8 3.0 3.2

pair_style buck/mdf 2.5 3.0
pair_coeff * * 100.0 1.5 200.0
pair_coeff * * 100.0 1.5 200.0 3.0 3.5

pair_style lennard/mdf 2.5 3.0
pair_coeff * * 1.0 1.0
pair_coeff 1 1 1021760.3664 2120.317338 3.0 3.2
```

## Restrictions

Restrictions 
These pair styles can only be used if LAMMPS was built with the
EXTRA-PAIR package.  See the Build package doc
page for more info.

## Related Commands

- [pair_coeff](pair_coeff.html)

