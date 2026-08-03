---
id: compute_ke_rigid
title: "compute ke/rigid command"
url: https://docs.lammps.org/compute_ke_rigid.html
---

# compute ke/rigid command

## Syntax

```
compute ID group-ID ke/rigid fix-ID
```

## Description

Define a computation that calculates the translational kinetic energy
of a collection of rigid bodies, as defined by one of the
fix rigid command variants.

The kinetic energy of each rigid body is computed as
\(\frac12 M V_\text{cm}^2\),
where \(M\) is the total mass of the rigid body, and \(V_\text{cm}\)
is its center-of-mass velocity.

The fix-ID should be the ID of one of the fix rigid
commands which defines the rigid bodies.  The group specified in the
compute command is ignored.  The kinetic energy of all the rigid
bodies defined by the fix rigid command in included in the
calculation.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 all ke/rigid myRigid
```

## Restrictions

Restrictions 
This compute is part of the RIGID package.  It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.

## Related Commands

- [compute erotate/rigid](compute_erotate_rigid.html)

