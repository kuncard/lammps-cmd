---
id: fix_gemc
title: "fix gemc command"
url: https://docs.lammps.org/fix_gemc.html
---

# fix gemc command

## Syntax

```
fix ID group-ID gemc N M X V T displace maxvol seed
```

## Description

Added in version 4Jul2026.

This fix performs Gibbs ensemble Monte Carlo (GEMC) exchanges of atoms
and volume between two simulation cells at specified T.  It also
attempts Monte Carlo (MC) moves (atom translations) within the
simulation cell.  This is usually used to establish thermodynamic
equilibrium between bulk vapor and liquid phases, as discussed in
(Frenkel).  If used with the fix nvt
command, hybrid MD/MC simulations in the Gibbs ensemble (equal pressure,
equal chemical potential, constant total volume, and constant
temperature) can be performed.  Specific uses include computing
vapor-liquid coexistence curves.

Every N timesteps the fix attempts GEMC atom exchanges, GEMC volume
changes, and MC moves of atoms.  On those timesteps, the average number
of attempted GEMC atom exchanges is X, the average number of volume
changes is V, and the average number of attempted MC moves is M.

This fix requires that LAMMPS be run with two partitions that
instantiate the two simulation cells.  This requires using the
-partition command-line switch.  For example, on a
workstation with 12 cores, -partition 2x6 could be used.  For better
performance, it is recommended that the two partitions be initialized at
two different densities.  This allows assigning only one core to the
partition running the vapor phase and all the other cores to the
partition running the liquid phase.  This can be achieved in a single
script by using the partition command to initiate the
two partitions at different densities. On a workstation with 12
processor cores, the command line option -partition 1 8 can be used
to assign 1 core to the first (vapor) partition and 8 cores to the
second (liquid) partition.

If used with fix nvt, the temperature of the Gibbs
ensemble, T, should be set to be equivalent to the target temperature
used in fix nvt.  Otherwise, the imaginary reservoir will not be in
thermal equilibrium with the simulation cell.  Also, it is important
that the temperature used by fix nvt is dynamically updated, which can
be achieved as follows:

compute mdtemp mdatoms temp
compute_modify mdtemp dynamic/dof yes
fix mdnvt mdatoms nvt temp 300.0 300.0 10.0
fix_modify mdnvt temp mdtemp

Note that neighbor lists are re-built every timestep that this fix is
invoked, so you should not set N to be too small.  However, periodic
rebuilds are necessary in order to avoid dangerous rebuilds and missed
interactions.  Specifically, avoid performing so many MC translations
per timestep that atoms can move beyond the neighbor list skin distance.
See the neighbor command for details.

When an atom is inserted in either partition, its coordinates are chosen
at a random position within the current simulation cell, and new atom
velocities are randomly chosen from the specified temperature
distribution given by T.

Some fixes have an associated potential energy. Examples of such fixes
include: efield, gravity,
addforce, langevin,
restrain, temp/berendsen, temp/rescale, and
wall fixes.  For that energy to be included in the
total potential energy of the system (the quantity used when performing
GEMC atom exchange, GEMC volume exchange and MC moves), you MUST enable
the fix_modify energy option for that fix.  The
doc pages for individual fix commands specify if this
should be done.

Use of this fix typically will cause the number of atoms in each cell to
fluctuate, therefore, you will want to use the compute_modify
dynamic/dof command to ensure that the current number
of atoms is used as a normalizing factor each time temperature is
computed. A simple example of this is:

compute_modify thermo_temp dynamic/dof yes

A more complicated example is listed earlier on this page in the context
of NVT dynamics.

Note
If the density of the cell is initially very small or zero, and
increases to a much larger density after a period of equilibration,
then certain quantities that are only calculated once at the start
(kspace parameters) may no longer be accurate.  The solution is to
start a new simulation after the equilibrium density has been
reached.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 2 all gemc 100 10 20 30 1.1 0.5 100.0 29494
```

## Restrictions

Restrictions 
This fix is part of the MC package.  It is only enabled if LAMMPS was
built with that package.  See the Build package
doc page for more info.
Do not set neigh_modify once yes or else this fix
will never be called.  Reneighboring is required.
Fix gemc currently only supports MC moves and exchanges on
individual atoms.
Use of multiple fix gemc commands in the same input script can be
problematic.

## Related Commands

- [fix gcmc](fix_gcmc.html)
- [fix widom](fix_widom.html)
- [fix atom/swap](fix_atom_swap.html)

