---
id: fix_lineforce
title: "fix lineforce command"
url: https://docs.lammps.org/fix_lineforce.html
---

# fix lineforce command

## Syntax

```
fix ID group-ID lineforce x y z
```

## Description

Adjust the forces on each atom in the group so that only the component
of force along the linear direction specified by the vector (x,y,z)
remains.  This is done by subtracting out components of force in the
plane perpendicular to the line.

If the initial velocity of the atom is 0.0 (or along the line), then
it should continue to move along the line thereafter.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix hold boundary lineforce 0.0 1.0 1.0
```

## Restrictions

Restrictions 
none

## Related Commands

- [fix planeforce](fix_planeforce.html)

