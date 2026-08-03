---
id: fix_npt_body
title: "fix npt/body command"
url: https://docs.lammps.org/fix_npt_body.html
---

# fix npt/body command

## Syntax

```
fix ID group-ID npt/body keyword value ...
```

## Description

Perform constant NPT integration to update position, velocity,
orientation, and angular velocity each timestep for body
particles in the group using a Nose/Hoover temperature
thermostat and Nose/Hoover pressure barostat.  P is pressure; T is
temperature.  This creates a system trajectory consistent with the
isothermal-isobaric ensemble.

This fix differs from the fix npt command, which
assumes point particles and only updates their position and velocity.

The thermostat is applied to both the translational and rotational
degrees of freedom for the body particles, assuming a compute is
used which calculates a temperature that includes the rotational
degrees of freedom (see below).  The translational degrees of freedom
can also have a bias velocity removed from them before thermostatting
takes place; see the description below.

Additional parameters affecting the thermostat and barostat are
specified by keywords and values documented with the fix npt command.  See, for example, discussion of the temp,
iso, aniso, and dilate keywords.

The particles in the fix group are the only ones whose velocities and
positions are updated by the velocity/position update portion of the
NPT integration.

Regardless of what particles are in the fix group, a global pressure is
computed for all particles.  Similarly, when the size of the simulation
box is changed, all particles are re-scaled to new positions, unless the
keyword dilate is specified with a value of partial, in which case
only the particles in the fix group are re-scaled.  The latter can be
useful for leaving the coordinates of particles in a solid substrate
unchanged and controlling the pressure of a surrounding fluid.

This fix computes a temperature and pressure each timestep.  To do
this, the fix creates its own computes of style  temp/body  and
 pressure , as if these commands had been issued:

compute fix-ID_temp all temp/body
compute fix-ID_press all pressure fix-ID_temp

See the compute temp/body and compute pressure commands for details.  Note that the
IDs of the new computes are the fix-ID + underscore +  temp  or fix_ID
+ underscore +  press , and the group for the new computes is  all 
since pressure is computed for the entire system.

Note that these are NOT the computes used by thermodynamic output (see
the thermo_style command) with ID = thermo_temp
and thermo_press.  This means you can change the attributes of this
fix s temperature or pressure via the
compute_modify command or print this temperature
or pressure during thermodynamic output via the thermo_style custom command using the appropriate compute-ID.
It also means that changing attributes of thermo_temp or
thermo_press will have no effect on this fix.

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
fix 1 all npt/body temp 300.0 300.0 100.0 iso 0.0 0.0 1000.0
fix 2 all npt/body temp 300.0 300.0 100.0 x 5.0 5.0 1000.0
fix 2 all npt/body temp 300.0 300.0 100.0 x 5.0 5.0 1000.0 drag 0.2
fix 2 water npt/body temp 300.0 300.0 100.0 aniso 0.0 0.0 1000.0 dilate partial
```

## Restrictions

Restrictions 
This fix is part of the BODY package.  It is only enabled if LAMMPS
was built with that package.  See the Build package page for more info.
This fix requires that atoms store torque and angular momentum and a
quaternion as defined by the atom_style body
command.

## Related Commands

- [fix npt](fix_nh.html)
- [fix nve_body](fix_nve_body.html)
- [fix nvt_body](fix_nvt_body.html)
- [fix_modify](fix_modify.html)

