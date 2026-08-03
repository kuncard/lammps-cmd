---
id: dihedral_helix
title: "dihedral_style helix command"
url: https://docs.lammps.org/dihedral_helix.html
---

# dihedral_style helix command

## Syntax

```
dihedral_style helix
```

## Description

The helix dihedral style uses the potential

\[E = A [1 - \cos(\theta)] + B [1 + \cos(3 \theta)] +
    C [1 + \cos(\theta + \frac{\pi}{4})]\]

This coarse-grain dihedral potential is described in (Guo).
For dihedral angles in the helical region, the energy function is
represented by a standard potential consisting of three minima, one
corresponding to the trans (t) state and the other to gauche states
(g+ and g-).  The paper describes how the \(A\), \(B\) and,
\(C\) parameters are chosen so as to balance secondary (largely
driven by local interactions) and
tertiary structure (driven by long-range interactions).

The following coefficients must be defined for each dihedral type via the
dihedral_coeff command as in the example above, or in
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
dihedral_style helix
dihedral_coeff 1 80.0 100.0 40.0
```

## Restrictions

Restrictions 
This dihedral style can only be used if LAMMPS was built with the
EXTRA-MOLECULE package.  See the Build package doc page
for more info.

## Related Commands

- [dihedral_coeff](dihedral_coeff.html)

