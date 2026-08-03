---
id: fix_nvt_body
title: "fix nvt/body command"
url: https://docs.lammps.org/fix_nvt_body.html
---

# fix nvt/body command

## Syntax

```
fix ID group-ID nvt/body keyword value ...
```

## Description

Perform constant NVT integration to update position, velocity,
orientation, and angular velocity each timestep for body
particles in the group using a Nose/Hoover temperature
thermostat.  V is volume; T is temperature.  This creates a system
trajectory consistent with the canonical ensemble.

This fix differs from the fix nvt command, which
assumes point particles and only updates their position and velocity.

The thermostat is applied to both the translational and rotational
degrees of freedom for the body particles, assuming a compute is
used which calculates a temperature that includes the rotational
degrees of freedom (see below).  The translational degrees of freedom
can also have a bias velocity removed from them before thermostatting
takes place; see the description below.

Additional parameters affecting the thermostat are specified by
keywords and values documented with the fix nvt
command.  See, for example, discussion of the temp and drag
keywords.

This fix computes a temperature each timestep.  To do this, the fix
creates its own compute of style  temp/body , as if this command
had been issued:

compute fix-ID_temp group-ID temp/body

See the compute temp/body command for
details.  Note that the ID of the new compute is the fix-ID +
underscore +  temp , and the group for the new compute is the same as
the fix group.

Note that this is NOT the compute used by thermodynamic output (see
the thermo_style command) with ID = thermo_temp.
This means you can change the attributes of this fix s temperature
(e.g. its degrees-of-freedom) via the
compute_modify command or print this temperature
during thermodynamic output via the thermo_style custom command using the appropriate compute-ID.
It also means that changing attributes of thermo_temp will have no
effect on this fix.

Like other fixes that perform thermostatting, this fix can be used
with compute commands that remove a  bias  from the
atom velocities.  E.g. to apply the thermostat only to atoms within a
spatial region, or to remove the center-of-mass
velocity from a group of atoms, or to remove the x-component of
velocity from the calculation.

This is not done by default, but only if the fix_modify command is used to assign a temperature compute to this
fix that includes such a bias term.  See the doc pages for individual
compute temp commands to determine which ones include
a bias.  In this case, the thermostat works in the following manner:
bias is removed from each atom, thermostatting is performed on the
remaining thermal degrees of freedom, and the bias is added back in.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 1 all nvt/body temp 300.0 300.0 100.0
fix 1 all nvt/body temp 300.0 300.0 100.0 drag 0.2
```

## Restrictions

Restrictions 
This fix is part of the BODY package.  It is only enabled if LAMMPS
was built with that package.  See the Build package page for more info.
This fix requires that atoms store torque and angular momentum and a
quaternion as defined by the atom_style body
command.

## Related Commands

- [fix nvt](fix_nh.html)
- [fix nve_body](fix_nve_body.html)
- [fix npt_body](fix_npt_body.html)
- [fix_modify](fix_modify.html)

