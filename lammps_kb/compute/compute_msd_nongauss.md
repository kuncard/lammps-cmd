---
id: compute_msd_nongauss
title: "compute msd/nongauss command"
url: https://docs.lammps.org/compute_msd_nongauss.html
---

# compute msd/nongauss command

## Syntax

```
compute ID group-ID msd/nongauss keyword values ...
com value = yes or no
```

## Description

Define a computation that calculates the mean-squared displacement
(MSD) and non-Gaussian parameter (NGP) of the group of atoms,
including all effects due to atoms passing through periodic boundaries.

A vector of three quantities is calculated by this compute.  The first
element of the vector is the total squared displacement,
\(dr^2 = dx^2 + dy^2 + dz^2\), of the atoms, and the second is the
fourth power of these displacements, \(dr^4 = (dx^2 + dy^2 + dz^2)^2\),
summed and averaged over atoms in the group.  The third component is the
non-Gaussian diffusion parameter NGP,

\[\text{NGP}(t) = \frac{3\left\langle(r(t)-r(0))^4\right\rangle}
                     {5\left\langle(r(t)-r(0))^2\right\rangle^2} - 1.\]

The NGP is a commonly used quantity in studies of dynamical
heterogeneity.  Its minimum theoretical value \((-0.4)\) occurs when all
atoms have the same displacement magnitude.  \(\text{NGP}=0\) for Brownian
diffusion, while \(\text{NGP} > 0\) when some mobile atoms move faster than
others.

If the com option is set to yes then the effect of any drift in
the center-of-mass of the group of atoms is subtracted out before the
displacement of each atom is calculated.

See the compute msd page for further important
NOTEs, which also apply to this compute.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 all msd/nongauss
compute 1 upper msd/nongauss com yes
```

## Restrictions

Restrictions 
Compute msd/nongauss cannot be used with a dynamic group.
This compute is part of the EXTRA-COMPUTE package.  It is only enabled
if LAMMPS was built with that package.  See the Build package page for more info.

## Related Commands

- [compute msd](compute_msd.html)

