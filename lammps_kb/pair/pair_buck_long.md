---
id: pair_buck_long
title: "pair_style buck/long/coul/long command"
url: https://docs.lammps.org/pair_buck_long.html
---

# pair_style buck/long/coul/long command

## Syntax

```
pair_style buck/long/coul/long flag_buck flag_coul cutoff (cutoff2)
long = use Kspace long-range summation for the dispersion term 1/r^6
cut = use a cutoff
long = use Kspace long-range summation for the Coulombic term 1/r
off = omit the Coulombic term
```

## Description

The buck/long/coul/long style computes a Buckingham potential (exp/6
instead of Lennard-Jones 12/6) and Coulombic potential, given by

\[\begin{split}E = & A e^{-r / \rho} - \frac{C}{r^6} \qquad r < r_c \\
E = & \frac{C q_i q_j}{\epsilon  r} \qquad r < r_c\end{split}\]

\(r_c\) is the cutoff.  If one cutoff is specified in the pair_style
command, it is used for both the Buckingham and Coulombic terms.  If
two cutoffs are specified, they are used as cutoffs for the Buckingham
and Coulombic terms respectively.

The purpose of this pair style is to capture long-range interactions
resulting from both attractive 1/r^6 Buckingham and Coulombic 1/r
interactions.  This is done by use of the flag_buck and flag_coul
settings.  The Ismail paper has more details on when it is
appropriate to include long-range 1/r^6 interactions, using this
potential.

If flag_buck is set to long, no cutoff is used on the Buckingham
1/r^6 dispersion term.  The long-range portion can be calculated by
using the kspace_style ewald/disp or pppm/disp
commands.  The specified Buckingham cutoff then determines which
portion of the Buckingham interactions are computed directly by the
pair potential versus which part is computed in reciprocal space via
the Kspace style.  If flag_buck is set to cut, the Buckingham
interactions are simply cutoff, as with pair_style buck.

If flag_coul is set to long, no cutoff is used on the Coulombic
interactions.  The long-range portion can calculated by using any of
several kspace_style command options such as
pppm or ewald.  Note that if flag_buck is also set to long, then
the ewald/disp or pppm/disp Kspace style needs to be used to
perform the long-range calculations for both the Buckingham and
Coulombic interactions.  If flag_coul is set to off, Coulombic
interactions are not computed.

The following coefficients must be defined for each pair of atoms
types via the pair_coeff command as in the examples
above, or in the data file or restart files read by the
read_data or read_restart
commands:

The second coefficient, rho, must be greater than zero.

The latter 2 coefficients are optional.  If not specified, the global
Buckingham and Coulombic cutoffs specified in the pair_style command
are used.  If only one cutoff is specified, it is used as the cutoff
for both Buckingham and Coulombic interactions for this type pair.  If
both coefficients are specified, they are used as the Buckingham and
Coulombic cutoffs for this type pair.  Note that if you are using
flag_buck set to long, you cannot specify a Buckingham cutoff for
an atom type pair, since only one global Buckingham cutoff is allowed.
Similarly, if you are using flag_coul set to long, you cannot
specify a Coulombic cutoff for an atom type pair, since only one
global Coulombic cutoff is allowed.

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
pair_style buck/long/coul/long cut off 2.5
pair_style buck/long/coul/long cut long 2.5 4.0
pair_style buck/long/coul/long long long 4.0
pair_coeff * * 1 1
pair_coeff 1 1 1 3 4
```

## Restrictions

Restrictions 
This style is part of the KSPACE package.  It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.

## Related Commands

- [pair_coeff](pair_coeff.html)

