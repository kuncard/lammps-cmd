---
id: compute_dipole
title: "compute dipole command"
url: https://docs.lammps.org/compute_dipole.html
---

# compute dipole command

## Syntax

```
compute ID group-ID style arg
```

## Description

Define a computation that calculates the dipole vector and total dipole
for a group of atoms.

These computes calculate the x,y,z coordinates of the dipole vector and
the total dipole moment for the atoms in the compute group.  This
includes all effects due to atoms passing through periodic boundaries.
For a group with a net charge the resulting dipole is made position
independent by subtracting the position vector of the center of mass or
geometric center times the net charge from the computed dipole
vector.  Both per-atom charges and per-atom dipole moments, if present,
contribute to the computed dipole.

Added in version 28Mar2023.

Compute dipole/tip4p includes adjustments for the charge carrying
point M in molecules with TIP4P water geometry.  The corresponding
parameters are extracted from the pair style.

Note
The coordinates of an atom contribute to the dipole in  unwrapped 
form, by using the image flags associated with each atom.  See the
dump custom command for a discussion of  unwrapped 
coordinates.  See the Atoms section of the read_data command for a discussion of image flags and how they are
set for each atom.  You can reset the image flags (e.g., to 0) before
invoking this compute by using the set image command.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 fluid dipole
compute dw water dipole geometry
compute dw water dipole/tip4p
```

## Restrictions

Restrictions 
Compute style dipole/tip4p is part of the EXTRA-COMPUTE package. It is
only enabled if LAMMPS was built with that package.  See the Build
package page for more info.
Compute style dipole/tip4p can only be used with tip4p pair styles.

## Related Commands

- [compute dipole/chunk](compute_dipole_chunk.html)

