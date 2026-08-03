---
id: fix_planeforce
title: "fix planeforce command"
url: https://docs.lammps.org/fix_planeforce.html
---

# fix planeforce command

## Syntax

```
fix ID group-ID planeforce x y z
```

## Description

Adjust the forces on each atom in the group so that only the
components of force in the plane specified by the normal vector
(x,y,z) remain.  This is done by subtracting out the component of
force perpendicular to the plane.

If the initial velocity of the atom is 0.0 (or in the plane), then it
should continue to move in the plane thereafter.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix hold boundary planeforce 1.0 0.0 0.0
```

## Restrictions

Restrictions 
none

## Related Commands

- [fix lineforce](fix_lineforce.html)

