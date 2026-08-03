---
id: comm_style
title: "comm_style command"
url: https://docs.lammps.org/comm_style.html
---

# comm_style command

## Syntax

```
comm_style style
```

## Description

This command sets the style of inter-processor communication of atom
information that occurs each timestep as coordinates and other
properties are exchanged between neighboring processors and stored as
properties of ghost atoms.

For the default brick style, the domain decomposition used by LAMMPS
to partition the simulation box must be a regular 3d grid of bricks,
one per processor.  Each processor communicates with its 6 Cartesian
neighbors in the grid to acquire information for nearby atoms.

For the tiled style, a more general domain decomposition can be
used, as triggered by the balance or fix balance commands.  The simulation box can be
partitioned into non-overlapping rectangular-shaped  tiles  or varying
sizes and shapes.  Again there is one tile per processor.  To acquire
information for nearby atoms, communication must now be done with a
more complex pattern of neighboring processors.

Note that this command does not actually define a partitioning of the
simulation box (a domain decomposition), rather it determines what
kinds of decompositions are allowed and the pattern of communication
used to enable the decomposition.  A decomposition is created when the
simulation box is first created, via the create_box
or read_data or read_restart
commands.  For both the brick and tiled styles, the initial
decomposition will be the same, as described by
create_box and processors
commands.  The decomposition can be changed via the
balance or fix balance commands.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
comm_style brick
comm_style tiled
```

## Restrictions

Restrictions 
none

## Related Commands

- [comm_modify](comm_modify.html)
- [processors](processors.html)
- [balance](balance.html)
- [fix balance](fix_balance.html)

