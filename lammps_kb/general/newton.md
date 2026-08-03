---
id: newton
title: "newton command"
url: https://docs.lammps.org/newton.html
---

# newton command

## Syntax

```
newton flag
newton flag1 flag2
```

## Description

This command turns Newton s third law on or off for pairwise and
bonded interactions.  For most problems, setting Newton s third law to
on means a modest savings in computation at the cost of two times
more communication.  Whether this is faster depends on problem size,
force cutoff lengths, a machine s compute/communication ratio, and how
many processors are being used.

Setting the pairwise newton flag to off means that if two
interacting atoms are on different processors, both processors compute
their interaction and the resulting force information is not
communicated.  Similarly, for bonded interactions, newton off means
that if a bond, angle, dihedral, or improper interaction contains
atoms on 2 or more processors, the interaction is computed by each
processor.

LAMMPS should produce the same answers for any newton flag settings,
except for round-off issues.

With run_style respa and only bonded interactions
(bond, angle, etc) computed in the innermost timestep, it may be
faster to turn newton off for bonded interactions, to avoid extra
communication in the innermost loop.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
newton off
newton on off
```

## Restrictions

Restrictions 
The newton bond setting cannot be changed after the simulation box is
defined by a read_data or
create_box command.

## Related Commands

- [run_style](run_style.html)

