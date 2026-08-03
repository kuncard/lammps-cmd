---
id: fix_nph_body
title: "fix nph/body command"
url: https://docs.lammps.org/fix_nph_body.html
---

# fix nph/body command

## Syntax

```
fix ID group-ID nph/body args keyword value ...
```

## Description

Perform constant NPH integration to update position, velocity,
orientation, and angular velocity each timestep for body
particles in the group using a Nose/Hoover pressure
barostat.  P is pressure; H is enthalpy.  This creates a system
trajectory consistent with the isenthalpic ensemble.

This fix differs from the fix nph command, which assumes
point particles and only updates their position and velocity.

Additional parameters affecting the barostat are specified by keywords
and values documented with the fix nph command.  See,
for example, discussion of the aniso, and dilate keywords.

The particles in the fix group are the only ones whose velocities and
positions are updated by the velocity/position update portion of the
NPH integration.

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

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 1 all nph/body iso 0.0 0.0 1000.0
fix 2 all nph/body x 5.0 5.0 1000.0
fix 2 all nph/body x 5.0 5.0 1000.0 drag 0.2
fix 2 water nph/body aniso 0.0 0.0 1000.0 dilate partial
```

## Restrictions

Restrictions 
This fix is part of the BODY package.  It is only enabled if LAMMPS
was built with that package.  See the Build package page for more info.
This fix requires that atoms store torque and angular momentum and a
quaternion as defined by the atom_style body
command.

## Related Commands

- [fix nph](fix_nh.html)
- [fix nve_body](fix_nve_body.html)
- [fix nvt_body](fix_nvt_body.html)
- [fix npt_body](fix_npt_body.html)
- [fix_modify](fix_modify.html)

