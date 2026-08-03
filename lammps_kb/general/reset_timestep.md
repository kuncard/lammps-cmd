---
id: reset_timestep
title: "reset_timestep command"
url: https://docs.lammps.org/reset_timestep.html
---

# reset_timestep command

## Syntax

```
reset_timestep N keyword values ...
time value = atime
   atime = accumulated simulation time
```

## Description

Set the timestep counter to the specified value.  This command
usually comes after the timestep has been set by reading a restart
file via the read_restart command, or a previous
simulation run or minimization advanced the timestep.

The optional time keyword allows to also set the accumulated
simulation time.  This is usually the number of timesteps times
the size of the timestep, but when using variable size timesteps
with fix dt/reset it can differ.

The read_data and create_box
commands set the timestep to 0; the read_restart
command sets the timestep to the value it had when the restart file
was written.  The same applies to the accumulated simulation time.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
reset_timestep 0
reset_timestep 4000000
reset_timestep 1000 time 100.0
```

## Restrictions

Restrictions 
This command cannot be used when any fixes are defined that keep track
of elapsed time to perform certain kinds of time-dependent operations.
Examples are the fix deposit and fix dt/reset commands.  The former adds atoms on specific timesteps.
The latter keeps track of accumulated time.
Various fixes use the current timestep to calculate related quantities.
If the timestep is reset, this may produce unexpected behavior, but
LAMMPS allows the fixes to be defined even if the timestep is reset.
For example, commands which thermostat the system, e.g. fix nvt, allow you to specify a target temperature which ramps from
Tstart to Tstop which may persist over several runs.  If you change the
timestep, you may induce an instantaneous change in the target
temperature.
Resetting the timestep clears flags for computes that
may have calculated some quantity from a previous run.  This means these
quantity cannot be accessed by a variable in between runs until a new
run is performed.  See the variable command for more
details.

## Related Commands

- [rerun](rerun.html)
- [timestep](timestep.html)
- [fix dt/reset](fix_dt_reset.html)

