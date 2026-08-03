---
id: fix_temp_rescale_eff
title: "fix temp/rescale/eff command"
url: https://docs.lammps.org/fix_temp_rescale_eff.html
---

# fix temp/rescale/eff command

## Syntax

```
fix ID group-ID temp/rescale/eff N Tstart Tstop window fraction
```

## Description

Reset the temperature of a group of nuclei and electrons in the
electron force field model by explicitly rescaling
their velocities.

The operation of this fix is exactly like that described by the fix temp/rescale command, except that the rescaling
is also applied to the radial electron velocity for electron
particles.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 3 flow temp/rescale/eff 10 1.0 100.0 0.02 1.0
```

## Restrictions

Restrictions 
This fix is part of the EFF package.  It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.

## Related Commands

- [fix langevin/eff](fix_langevin_eff.html)
- [fix nvt/eff](fix_nh_eff.html)
- [fix_modify](fix_modify.html)
- [fix temp rescale](fix_temp_rescale.html)

