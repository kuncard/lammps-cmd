---
id: fix_dt_reset
title: "fix dt/reset command"
url: https://docs.lammps.org/fix_dt_reset.html
---

# fix dt/reset command

## Syntax

```
fix ID group-ID dt/reset N Tmin Tmax Xmax keyword values ...
emax value = Emax
  Emax = maximum kinetic energy change for an atom in one timestep (energy units)
units value = lattice or box
  lattice = Xmax is defined in lattice units
  box = Xmax is defined in simulation box units
```

## Description

Reset the timestep size every N steps during a run, so that no atom
moves further than the specified Xmax distance, based on current
atom velocities and forces.  Optionally an additional criterion is
imposed by the emax keyword, so that no atom s kinetic energy
changes by more than the specified Emax.

This can be useful when starting from a configuration with overlapping
atoms, where forces will be large.  Or it can be useful when running
an impact simulation where one or more high-energy atoms collide with
a solid, causing a damage cascade.

This fix overrides the timestep size setting made by the
timestep command.  The new timestep size dt is
computed in the following manner.

For each atom, the timestep is computed that would cause it to
displace Xmax on the next integration step, as a function of its
current velocity and force.  Since performing this calculation exactly
would require the solution to a quartic equation, a cheaper estimate
is generated.  The estimate is conservative in that the atom s
displacement is guaranteed not to exceed Xmax, though it may be
smaller.

In addition if the emax keyword is used, the specified Emax value
is enforced as a limit on how much an atom s kinetic energy can
change.  If the timestep required is even smaller than for the Xmax
displacement, then the smaller timestep is used.

Given this putative timestep for each atom, the minimum timestep value
across all atoms is computed.  Then the Tmin and Tmax bounds are
applied, if specified.  If one (or both) is specified as NULL, it is
not applied.

When the run style is respa, this fix resets the
outer loop (largest) timestep, which is the same timestep that the
timestep command sets.

Note that the cumulative simulation time (in time units), which
accounts for changes in the timestep size as a simulation proceeds,
can be accessed by the thermo_style time
keyword.

Also note that the dump_modify every/time option
allows dump files to be written at intervals specified by simulation
time, rather than by timesteps.  Simulation time is in time units;
see the units doc page for details.

Styles with a gpu, intel, kk, omp, or opt suffix are
functionally the same as the corresponding style without the suffix.
They have been optimized to run faster, depending on your available
hardware, as discussed on the Accelerator packages
page.  The accelerated styles take the same arguments and should
produce the same results, except for round-off and precision issues.

These accelerated styles are part of the GPU, INTEL, KOKKOS,
OPENMP, and OPT packages, respectively.  They are only enabled if
LAMMPS was built with those packages.  See the Build package page for more info.

You can specify the accelerated styles explicitly in your input script
by including their suffix, or you can use the -suffix command-line switch when you invoke LAMMPS, or you can use the
suffix command in your input script.

See the Accelerator packages page for more
instructions on how to use the accelerated styles effectively.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 5 all dt/reset 10 1.0e-5 0.01 0.1
fix 5 all dt/reset 10 0.01 2.0 0.2 units box
fix 5 all dt/reset 5 NULL 0.001 0.5 emax 30 units box
```

## Restrictions

Restrictions 
none

## Related Commands

- [timestep](timestep.html)
- [dump_modify every/time](dump_modify.html)

