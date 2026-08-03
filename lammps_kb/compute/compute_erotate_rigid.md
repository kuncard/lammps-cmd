---
id: compute_erotate_rigid
title: "compute erotate/rigid command"
url: https://docs.lammps.org/compute_erotate_rigid.html
---

# compute erotate/rigid command

## Syntax

```
compute ID group-ID erotate/rigid fix-ID
```

## Description

Define a computation that calculates the rotational kinetic energy of
a collection of rigid bodies, as defined by one of the
fix rigid command variants.

The rotational energy of each rigid body is computed as
\(\frac12 I \omega_\text{body}^2\),
where \(I\) is the inertia tensor for the rigid body and
\(\omega_\text{body}\) is its angular velocity vector.
Both \(I\) and \(\omega_\text{body}\) are in the frame of
reference of the rigid body (i.e., \(I\) is diagonal).

The fix-ID should be the ID of one of the fix rigid
commands which defines the rigid bodies.  The group specified in the
compute command is ignored.  The rotational energy of all the rigid
bodies defined by the fix rigid command in included in the calculation.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 all erotate/rigid myRigid
```

## Restrictions

Restrictions 
This compute is part of the RIGID package.  It is only enabled if
LAMMPS was built with that package.  See the
Build package page for more info.

## Related Commands

- [compute ke/rigid](compute_ke_rigid.html)

