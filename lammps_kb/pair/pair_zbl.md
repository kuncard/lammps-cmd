---
id: pair_zbl
title: "pair_style zbl command"
url: https://docs.lammps.org/pair_zbl.html
---

# pair_style zbl command

## Syntax

```
pair_style zbl inner outer
```

## Description

Style zbl computes the Ziegler-Biersack-Littmark (ZBL) screened
nuclear repulsion for describing high-energy collisions between atoms.
(Ziegler). It includes an additional switching function
that ramps the energy, force, and curvature smoothly to zero between an
inner and outer cutoff. The potential energy due to a pair of atoms at a
distance r_ij is given by:

\[\begin{split}E^{ZBL}_{ij} & = \frac{1}{4\pi\epsilon_0} \frac{Z_i Z_j \,e^2}{r_{ij}} \phi(r_{ij}/a)+ S(r_{ij})\\
a & =  \frac{0.46850}{Z_{i}^{0.23} + Z_{j}^{0.23}}\\
\phi(x) & =  0.18175e^{-3.19980x} + 0.50986e^{-0.94229x} + 0.28022e^{-0.40290x} + 0.02817e^{-0.20162x}\\\end{split}\]

where e is the electron charge, \(\epsilon_0\) is the electrical
permittivity of vacuum, and \(Z_i\) and \(Z_j\) are the nuclear
charges of the two atoms.  The switching function \(S(r)\) is
identical to that used by pair_style lj/gromacs.
Here, the inner and outer cutoff are the same for all pairs of atom
types.

The following coefficients must be defined for each pair of atom types
via the pair_coeff command as in the examples above,
or in the LAMMPS data file.

The values of \(Z_i\) and \(Z_j\) are normally equal to the
atomic numbers of the two atom types. Thus, the user may optionally
specify only the coefficients for each \(i==j\) pair, and rely on
the obvious mixing rule for cross interactions (see below).  Note that
when \(i==j\) it is required that \(Z_i == Z_j\).  When used
with hybrid/overlay and pairs are assigned to more
than one sub-style, the mixing rule is not used and each pair of types
interacting with the ZBL sub-style must be included in a pair_coeff
command.

Note
The numerical values of the exponential decay constants in the
screening function depend on the unit of distance. In the above
equation they are given for units of Angstroms. LAMMPS will
automatically convert these values to the distance unit of the
specified LAMMPS units setting.  The values of Z
should always be given as multiples of a proton s charge, e.g. 29.0
for copper.

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
pair_style zbl 3.0 4.0
pair_coeff * * 73.0 73.0
pair_coeff 1 1 14.0 14.0
```

## Restrictions

Restrictions 
none

## Related Commands

- [pair_coeff](pair_coeff.html)

