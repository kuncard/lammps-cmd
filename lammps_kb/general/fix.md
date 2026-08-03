---
id: fix
title: "fix command"
url: https://docs.lammps.org/fix.html
---

# fix command

## Syntax

```
fix ID group-ID style args
```

## Description

Set a fix that will be applied to a group of atoms.  In LAMMPS, a
 fix  is any operation that is applied to the system during
timestepping or minimization.  Examples include updating of atom
positions and velocities due to time integration, controlling
temperature, applying constraint forces to atoms, enforcing boundary
conditions, computing diagnostics, etc.  There are hundreds of fixes
defined in LAMMPS and new ones can be added; see the
Modify page for details.

Fixes perform their operations at different stages of the timestep.
If two or more fixes operate at the same stage of the timestep, they are
invoked in the order they were specified in the input script.

The ID of a fix can only contain alphanumeric characters and
underscores.

Fixes can be deleted with the unfix command.

Note
The unfix command is the only way to turn off a
fix; simply specifying a new fix with a similar style will not turn
off the first one.  This is especially important to realize for
integration fixes.  For example, using a fix nve
command for a second run after using a fix nvt command
for the first run will not cancel out the NVT time integration
invoked by the  fix nvt  command.  Thus, two time integrators would be
in place!

If you specify a new fix with the same ID and style as an existing
fix, the old fix is deleted and the new one is created (presumably
with new settings).  This is the same as if an  unfix  command were
first performed on the old fix, except that the new fix is kept in the
same order relative to the existing fixes as the old one originally
was.  Note that this operation also wipes out any additional changes
made to the old fix via the fix_modify command.

The fix modify command allows settings for some
fixes to be reset.  See the page for individual fixes for details.

Some fixes store an internal  state  which is written to binary
restart files via the restart or
write_restart commands.  This allows the fix to
continue on with its calculations in a restarted simulation.  See the
read_restart command for info on how to re-specify
a fix in an input script that reads a restart file.  See the doc pages
for individual fixes for info on which ones can be restarted.

Some fixes calculate and store any of four styles of quantities:
global, per-atom, local, or per-grid.

A global quantity is one or more system-wide values, e.g. the energy
of a wall interacting with particles.  A per-atom quantity is one or
more values per atom, e.g. the original coordinates of each atom at
time 0.  Per-atom values are set to 0.0 for atoms not in the specified
fix group.  Local quantities are calculated by each processor based on
the atoms it owns, but there may be zero or more per atom, e.g. values
for each bond.  Per-grid quantities are calculated on a regular 2d or
3d grid which overlays a 2d or 3d simulation domain.  The grid points
and the data they store are distributed across processors; each
processor owns the grid points which fall within its subdomain.

As a general rule of thumb, fixes that produce per-atom quantities
have the word  atom  at the end of their style, e.g. ave/atom.
Fixes that produce local quantities have the word  local  at the end
of their style, e.g. store/local.  Fixes that produce per-grid
quantities have the word  grid  at the end of their style,
e.g. ave/grid.

Global, per-atom, local, and per-grid quantities can also be of three
kinds: a single scalar value (global only), a vector of values, or a
2d array of values.  For per-atom, local, and per-grid quantities, a
 vector  means a single value for each atom, each local entity
(e.g. bond), or grid cell.  Likewise an  array , means multiple values
for each atom, each local entity, or each grid cell.

Note that a single fix can produce any combination of global,
per-atom, local, or per-grid values.  Likewise it can produce any
combination of scalar, vector, or array output for each style.  The
exception is that for per-atom, local, and per-grid output, either a
vector or array can be produced, but not both.  The doc page for each
fix explains the values it produces, if any.

When a fix output is accessed by another input script command it is
referenced via the following bracket notation, where ID is the ID of
the fix:

In other words, using one bracket reduces the dimension of the
quantity once (vector \(\to\) scalar, array \(\to\) vector).
Using two brackets reduces the dimension twice (array \(\to\)
scalar).  Thus, for example, a command that uses global scalar fix
values as input can also process elements of a vector or array.
Depending on the command, this can either be done directly using the
syntax in the table, or by first defining a variable
of the appropriate style to store the quantity, then using the
variable as an input to the command.

Note that commands and variables which take fix
outputs as input typically do not allow for all styles and kinds of
data (e.g., a command may require global but not per-atom values, or
it may require a vector of values, not a scalar).  This means there is
typically no ambiguity about referring to a fix output as c_ID even if
it produces, for example, both a scalar and vector.  The doc pages for
various commands explain the details, including how any ambiguities
are resolved.

In LAMMPS, the values generated by a fix can be used in several ways:

See the Howto output page for a summary of
various LAMMPS output options, many of which involve fixes.

The results of fixes that calculate global quantities can be either
 intensive  or  extensive  values.  Intensive means the value is
independent of the number of atoms in the simulation
(e.g., temperature).  Extensive means the value scales with the number of
atoms in the simulation (e.g., total rotational kinetic energy).
Thermodynamic output will normalize extensive
values by the number of atoms in the system, depending on the
 thermo_modify norm  setting.  It will not normalize intensive values.
If a fix value is accessed in another way (e.g., by a
variable), you may want to know whether it is an
intensive or extensive value.  See the page for individual fix styles
for further info.

Each fix style has its own page that describes its arguments and
what it does, as listed below.  Here is an alphabetical list of fix
styles available in LAMMPS.  They are also listed in more compact form
on the Commands fix doc page.

There are also additional accelerated fix styles included in the
LAMMPS distribution for faster performance on CPUs, GPUs, and KNLs.
The individual style names on the Commands fix doc
page are followed by one or more of (g,i,k,o,t) to indicate which
accelerated styles exist.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 1 all nve
fix 3 all nvt temp 300.0 300.0 0.01
fix mine top setforce 0.0 NULL 0.0
```

## Restrictions

Restrictions 
Some fix styles are part of specific packages.  They are only enabled
if LAMMPS was built with that package.  See the
Build package page for more info.  The doc pages for
individual fixes tell if it is part of a package.

## Related Commands

- [unfix](unfix.html)
- [fix_modify](fix_modify.html)

