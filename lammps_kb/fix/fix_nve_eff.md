---
id: fix_nve_eff
title: "fix nve/eff command"
url: https://docs.lammps.org/fix_nve_eff.html
---

# fix nve/eff command

## Syntax

```
fix ID group-ID nve/eff
```

## Description

Perform constant NVE integration to update position and velocity for
nuclei and electrons in the group for the electron force field model.  V is volume; E is energy.  This creates a
system trajectory consistent with the microcanonical ensemble.

The operation of this fix is exactly like that described by the fix nve command, except that the radius and radial velocity
of electrons are also updated.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 1 all nve/eff
```

## Restrictions

Restrictions 
This fix is part of the EFF package.  It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.

## Related Commands

- [fix nve](fix_nve.html)
- [fix nvt/eff](fix_nh_eff.html)
- [fix npt/eff](fix_nh_eff.html)

