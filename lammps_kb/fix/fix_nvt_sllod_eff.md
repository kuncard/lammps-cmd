---
id: fix_nvt_sllod_eff
title: "fix nvt/sllod/eff command"
url: https://docs.lammps.org/fix_nvt_sllod_eff.html
---

# fix nvt/sllod/eff command

## Syntax

```
fix ID group-ID nvt/sllod/eff keyword value ...
keyword = psllod
  psllod value = no or yes = use SLLOD or p-SLLOD variant, respectively
```

## Description

Perform constant NVT integration to update positions and velocities each
timestep for nuclei and electrons in the group for the electron
force field model, using a Nose/Hoover temperature
thermostat.  V is volume; T is temperature.  This creates a system
trajectory consistent with the canonical ensemble.

The operation of this fix is exactly like that described by the
fix nvt/sllod command, except that the radius and
radial velocity of electrons are also updated and thermostatted.
Likewise the temperature calculated by the fix, using the compute it
creates (as discussed in the fix nvt, npt, and nph doc
page), is performed with a compute temp/deform/eff command (if peculiar = no) or a
compute temp/eff command
(if peculiar = yes) that includes the eFF contribution to
the temperature from the electron radial velocity.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 1 all nvt/sllod/eff temp 300.0 300.0 0.1
fix 1 all nvt/sllod/eff temp 300.0 300.0 0.1 drag 0.2
```

## Restrictions

Restrictions 
This fix is part of the EFF package.  It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.
This fix works best without Nose-Hoover chain thermostats, i.e. using
tchain = 1.  Setting tchain to larger values can result in poor
equilibration.

## Related Commands

- [fix nve/eff](fix_nve_eff.html)
- [fix nvt/eff](fix_nh_eff.html)
- [fix langevin/eff](fix_langevin_eff.html)
- [fix nvt/sllod](fix_nvt_sllod.html)
- [fix_modify](fix_modify.html)
- [compute temp/deform/eff](compute_temp_deform_eff.html)

