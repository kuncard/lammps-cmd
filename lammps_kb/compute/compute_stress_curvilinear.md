---
id: compute_stress_curvilinear
title: "compute stress/cylinder command"
url: https://docs.lammps.org/compute_stress_curvilinear.html
---

# compute stress/cylinder command

## Syntax

```
compute ID group-ID style args
stress/cylinder args = zlo zh Rmax bin_width keyword
  zlo = minimum z-boundary for cylinder
  zhi = maximum z-boundary for cylinder
  Rmax = maximum radius to perform calculation to
  bin_width = width of radial bins to use for calculation
  keyword = ke (zero or one can be specified)
    ke = yes or no
stress/spherical
  x0, y0, z0 = origin of the spherical coordinate system
  bin_width = width of spherical shells
  Rmax = maximum radius of spherical shells
```

## Description

Compute stress/cylinder, and compute
stress/spherical define computations that calculate profiles of the
diagonal components of the local stress tensor in the specified
coordinate system. The stress tensor is split into a kinetic
contribution \(P^k\) and a virial contribution \(P^v\). The sum
gives the total stress tensor \(P = P^k+P^v\). These computes can
for example be used to calculate the diagonal components of the local
stress tensor of surfaces with cylindrical or spherical
symmetry. These computes obeys momentum balance through fluid
interfaces. They use the Irving Kirkwood contour, which is the straight
line between particle pairs.

The compute stress/cylinder computes the stress profile along the
radial direction in cylindrical coordinates, as described in
(Addington). The compute stress/spherical
computes the stress profile along the radial direction in spherical
coordinates, as described in (Ikeshoji).

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 all stress/cylinder -10.0 10.0 15.0 0.25
compute 1 all stress/cylinder -10.0 10.0 15.0 0.25 ke no
compute 1 all stress/spherical 0 0 0 0.1 10
```

## Restrictions

Restrictions 
These computes calculate the stress tensor contributions for pair styles
only (i.e., no bond, angle, dihedral, etc. contributions, and in the
presence of bonded interactions, the result may be incorrect due to
exclusions for special bonds excluding pairs of atoms
completely). It requires pairwise force calculations not available for most
many-body pair styles.  Note that \(k\)-space calculations are also excluded.
These computes are part of the EXTRA-COMPUTE package.  They are only
enabled if LAMMPS was built with that package.  See the Build
package doc page for more info.

## Related Commands

- [compute stress/atom](compute_stress_atom.html)
- [compute pressure](compute_pressure.html)
- [compute stress/mop/profile](compute_stress_mop.html)
- [compute stress/cartesian](compute_stress_cartesian.html)

