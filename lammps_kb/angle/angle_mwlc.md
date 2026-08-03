---
id: angle_mwlc
title: "angle_style mwlc command"
url: https://docs.lammps.org/angle_mwlc.html
---

# angle_style mwlc command

## Syntax

```
angle_style mwlc
```

## Description

Added in version 4Feb2025.

The mwlc angle style models a meltable wormlike chain and can be used
to model non-linear bending elasticity of polymers, e.g. DNA.  mwlc
uses a potential that is a canonical-ensemble superposition of a
non-melted and a melted state (Farrell).  The potential
is

\[E = -k_{B}T\,\log [q + q^{m}] + E_{0},\]

where the non-melted and melted partition functions are

\[\begin{split}q = \exp [-k_{1}(1+\cos{\theta})/k_{B}T]; \\
q^{m} = \exp [-(\mu+k_{2}(1+\cos{\theta}))/k_{B}T].\end{split}\]

\(k_1\) is the bending elastic constant of the non-melted state,
\(k_2\) is the bending elastic constant of the melted state,
\(\mu\) is the melting energy, and
\(T\) is the reference temperature.
The reference energy,

\[E_{0} = -k_{B}T\,\log [1 + \exp[-\mu/k_{B}T]],\]

ensures that E is zero for a fully extended chain.

This potential is a continuous version of the two-state potential
introduced by (Yan).

The following coefficients must be defined for each angle type via the
angle_coeff command as in the example above, or in
the data file or restart files read by the read_data
or read_restart commands:

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
angle_style mwlc
angle_coeff * 25 1 10 1
```

## Restrictions

Restrictions 
This angle style can only be used if LAMMPS was built with the
EXTRA-MOLECULE package.  See the Build package
doc page for more info.

## Related Commands

- [angle_coeff](angle_coeff.html)

