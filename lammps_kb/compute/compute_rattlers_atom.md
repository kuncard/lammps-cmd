---
id: compute_rattlers_atom
title: "compute rattlers/atom command"
url: https://docs.lammps.org/compute_rattlers_atom.html
---

# compute rattlers/atom command

## Syntax

```
compute ID group-ID rattlers/atom cutoff zmin ntries
type = cutoffs determined based on atom types
radius = cutoffs determined based on atom diameters (atom style sphere)
```

## Description

Added in version 7Feb2024.

Define a compute that identifies rattlers in a system. Rattlers are often
identified in granular or glassy packings as under-coordinated atoms that
do not have the required number of contacts to constrain their translational
degrees of freedom. Such atoms are not considered rigid and can often freely
rattle around in the system. This compute identifies rattlers which can be
helpful for excluding them from analysis or providing extra damping forces
to accelerate relaxation processes.

Rattlers are identified using an interactive approach. The coordination
number of all atoms is first calculated.  The type and radius settings
are used to select whether interaction cutoffs are determined by atom
types or by the sum of atomic radii (atom style sphere), respectively.
Rattlers are then identified as atoms with a coordination number less
than zmin and are removed from consideration. Atomic coordination
numbers are then recalculated, excluding previously identified rattlers,
to identify a new set of rattlers. This process is iterated up to a maximum
of ntries or until no new rattlers are identified and the remaining
atoms form a stable network of contacts.

In dense homogeneous systems where the average atom coordination number
is expected to be larger than zmin, this process usually only takes a few
iterations and a value of ntries around ten may be sufficient. In systems
with significant heterogeneity or average coordination numbers less than
zmin, an appropriate value of ntries depends heavily on the specific
system. For instance, a linear chain of N rattler atoms with a zmin of 2
would take N/2 iterations to identify that all the atoms are rattlers.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 all rattlers/atom type 4 10
```

## Restrictions

Restrictions 
This compute is part of the EXTRA-COMPUTE package.  It is only enabled if
LAMMPS was built with that package.  See the
Build package page for more info.
The radius cutoff option requires that atoms store a radius as defined by the
atom_style sphere or similar commands.

## Related Commands

- [compute coord/atom](compute_coord_atom.html)
- [compute contact/atom](compute_contact_atom.html)

