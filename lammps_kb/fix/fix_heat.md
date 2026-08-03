---
id: fix_heat
title: "fix heat command"
url: https://docs.lammps.org/fix_heat.html
---

# fix heat command

## Syntax

```
fix ID group-ID heat N eflux
region value = region-ID
  region-ID = ID of region atoms must be in to have added force
```

## Description

Add non-translational kinetic energy (heat) to a group of atoms in a
manner that conserves their aggregate momentum.  Two of these fixes
can be used to establish a temperature gradient across a simulation
domain by adding heat (energy) to one group of atoms (hot reservoir)
and subtracting heat from another (cold reservoir).  E.g. a simulation
sampling from the McDLT ensemble.

If the region keyword is used, the atom must be in both the group
and the specified geometric region in order to have
energy added or subtracted to it.  If not specified, then the atoms in
the group are affected wherever they may move to.

Heat addition/subtraction is performed every N timesteps.

The eflux parameter can be specified as a numeric constant or as an
equal- or atom-style variable.  If the value is a
variable, it should be specified as v_name, where name is the variable
name.  In this case, the variable will be evaluated each timestep, and
its current value(s) used to determine the flux.

If eflux is a numeric constant or equal-style variable which evaluates
to a scalar value, then eflux determines the change in aggregate energy
of the entire group of atoms per unit time, e.g. in eV/ps for
metal units.  In this case it is an  extensive  quantity,
meaning its magnitude should be scaled with the number of atoms in the
group.  Note that since eflux also has per-time units (i.e. it is a
flux), this means that a larger value of N will add/subtract a larger
amount of energy each time the fix is invoked.

Note
The heat-exchange (HEX) algorithm implemented by this fix is
known to exhibit a pronounced energy drift. An improved algorithm
(eHEX) is available as a fix ehex command and might be
preferable if energy conservation is important.

If eflux is specified as an atom-style variable (see below), then
the variable computes one value per atom.  In this case, each value is
the energy flux for a single atom, again in units of energy per unit
time.  In this case, each value is an  intensive  quantity, which need
not be scaled with the number of atoms in the group.

Equal-style variables can specify formulas with various mathematical
functions, and include thermo_style command
keywords for the simulation box parameters and timestep and elapsed
time.  Thus it is easy to specify a time-dependent flux.

Atom-style variables can specify the same formulas as equal-style
variables but can also include per-atom values, such as atom
coordinates.  Thus it is easy to specify a spatially-dependent flux
with optional time-dependence as well.

Note
If heat is subtracted from the system too aggressively so that
the group s kinetic energy would go to zero, or any individual atom s
kinetic energy would go to zero for the case where eflux is an
atom-style variable, then LAMMPS will halt with an error message.

Fix heat is different from a thermostat such as fix nvt
or fix temp/rescale in that energy is
added/subtracted continually.  Thus if there is not another mechanism
in place to counterbalance this effect, the entire system will heat or
cool continuously.  You can use multiple heat fixes so that the net
energy change is 0.0 or use fix viscous to drain
energy from the system.

This fix does not change the coordinates of its atoms; it only scales
their velocities.  Thus you must still use an integration fix
(e.g. fix nve) on the affected atoms.  This fix should
not normally be used on atoms that have their temperature controlled
by another fix - e.g. fix nvt or fix langevin fix.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 3 qin heat 1 1.0
fix 3 qin heat 10 v_flux
fix 4 qout heat 1 -1.0 region top
```

## Restrictions

Restrictions 
none

## Related Commands

- [fix ehex](fix_ehex.html)
- [compute temp](compute_temp.html)
- [compute temp/region](compute_temp_region.html)

