---
id: compute_temp_deform_eff
title: "compute temp/deform/eff command"
url: https://docs.lammps.org/compute_temp_deform_eff.html
---

# compute temp/deform/eff command

## Syntax

```
compute ID group-ID temp/deform/eff keyword value ...
temp value = compute ID that calculates a temperature
```

## Description

Define a computation that calculates the temperature of a group of
nuclei and electrons in the electron force field
model, after subtracting out a streaming velocity induced by the
simulation box changing size and/or shape, for example in a
non-equilibrium MD (NEMD) simulation.  The size/shape change is
induced by use of the fix deform command.  A
compute of this style is created by the fix nvt/sllod/eff command to compute the thermal temperature of
atoms for thermostatting purposes.  A compute of this style can also
be used by any command that computes a temperature (e.g.,
thermo_modify, fix npt/eff).

The calculation performed by this compute is exactly like that
described by the compute temp/deform
command, except that the formulas for the temperature (scalar) and
diagonal components of the symmetric tensor (vector) include the
radial electron velocity contributions, as discussed by the
compute temp/eff command.  Note that only
the translational degrees of freedom for each nuclei or electron are
affected by the streaming velocity adjustment.  The radial velocity
component of the electrons is not affected.

Changed in version 11Feb2026.

By default, the internal temperature compute has the style
compute temp/eff.  If an internal
temperature compute is used which does not have the /eff suffix,
the contribution to the scalar and vector values due to the
radial electron velocity will be added in by this compute.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute myTemp all temp/deform/eff
```

## Restrictions

Restrictions 
This compute is part of the EFF package.  It is only enabled if
LAMMPS was built with that package.  See the
Build package page for more info.

## Related Commands

- [compute temp/ramp](compute_temp_ramp.html)
- [fix deform](fix_deform.html)
- [fix nvt/sllod/eff](fix_nvt_sllod_eff.html)

