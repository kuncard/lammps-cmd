---
id: fix_temp_csvr
title: "fix temp/csvr command"
url: https://docs.lammps.org/fix_temp_csvr.html
---

# fix temp/csvr command

## Syntax

```
fix ID group-ID temp/csvr Tstart Tstop Tdamp seed
fix ID group-ID temp/csld Tstart Tstop Tdamp seed
Tstart can be a variable (see below)
```

## Description

Adjust the temperature with a canonical sampling thermostat that uses
global velocity rescaling with Hamiltonian dynamics (temp/csvr)
(Bussi1), or Langevin dynamics (temp/csld)
(Bussi2).  In the case of temp/csvr the thermostat is
similar to the empirical Berendsen thermostat in
temp/berendsen, but chooses the actual
scaling factor from a suitably chosen (gaussian) distribution rather
than having it determined from the time constant directly. In the case
of temp/csld the velocities are updated to a linear combination of
the current velocities with a gaussian distribution of velocities at
the desired temperature.  Both thermostats are applied every timestep.

The thermostat is applied to only the translational degrees of freedom
for the particles, which is an important consideration for finite-size
particles which have rotational degrees of freedom are being
thermostatted with these fixes.  The translational degrees of freedom
can also have a bias velocity removed from them before thermostatting
takes place; see the description below.

The desired temperature at each timestep is a ramped value during the
run from Tstart to Tstop.  The Tdamp parameter is specified in
time units and determines how rapidly the temperature is relaxed.  For
example, a value of 100.0 means to relax the temperature in a timespan
of (roughly) 100 time units (tau or fs or ps - see the
units command).

Tstart can be specified as an equal-style variable.
In this case, the Tstop setting is ignored.  If the value is a
variable, it should be specified as v_name, where name is the variable
name.  In this case, the variable will be evaluated each timestep, and
its value used to determine the target temperature.

Equal-style variables can specify formulas with various mathematical
functions, and include thermo_style command
keywords for the simulation box parameters and timestep and elapsed
time.  Thus it is easy to specify a time-dependent temperature.

Note
Unlike the fix nvt command which performs
Nose/Hoover thermostatting AND time integration, these fixes do NOT
perform time integration. They only modify velocities to effect
thermostatting.  Thus you must use a separate time integration fix,
like fix nve to actually update the positions of atoms
using the modified velocities.  Likewise, these fixes should not
normally be used on atoms that also have their temperature controlled
by another fix - e.g. by fix nvt or fix langevin commands.

See the Howto thermostat page for a
discussion of different ways to compute temperature and perform
thermostatting.

These fixes compute a temperature each timestep.  To do this, the fix
creates its own compute of style  temp , as if this command had been
issued:

compute fix-ID_temp group-ID temp

See the compute temp command for details.  Note
that the ID of the new compute is the fix-ID + underscore +  temp ,
and the group for the new compute is the same as the fix group.

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

An important feature of these thermostats is that they have an
associated effective energy that is a constant of motion.  The
effective energy is the total energy (kinetic + potential) plus the
accumulated kinetic energy changes due to the thermostat. The latter
quantity is the global scalar computed by these fixes. This feature is
useful to check the integration of the equations of motion against
discretization errors. In other words, the conservation of the
effective energy can be used to choose an appropriate integration
timestep. This is similar to the usual paradigm of
checking the conservation of the total energy in the microcanonical
ensemble.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 1 all temp/csvr 300.0 300.0 100.0 54324
fix 1 all temp/csld 100.0 300.0 10.0 123321
```

## Restrictions

Restrictions 
Fix temp/csld is not compatible with fix shake.
These fixes are part of the EXTRA-FIX package.  They are only enabled if LAMMPS
was built with that package.  See the Build package page for more info.
These fixes can be used with dynamic groups as defined by the
group command.  Likewise it can be used with groups to
which atoms are added or deleted over time, e.g. a deposition
simulation.  However, the conservation properties of the thermostat
and barostat are defined for systems with a static set of atoms.  You
may observe odd behavior if the atoms in a group vary dramatically
over time or the atom count becomes very small.

## Related Commands

- [fix nve](fix_nve.html)
- [fix nvt](fix_nh.html)
- [fix temp/rescale](fix_temp_rescale.html)
- [fix langevin](fix_langevin.html)
- [fix_modify](fix_modify.html)
- [compute temp](compute_temp.html)
- [fix temp/berendsen](fix_temp_berendsen.html)

