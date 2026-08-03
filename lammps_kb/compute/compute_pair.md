---
id: compute_pair
title: "compute pair command"
url: https://docs.lammps.org/compute_pair.html
---

# compute pair command

## Syntax

```
compute ID group-ID pair pstyle [nstyle] [evalue]
```

## Description

Define a computation that extracts additional values calculated by a
pair style, and makes them accessible for output or further processing
by other commands.

Note
The group specified for this command is ignored.

The specified pstyle must be a pair style used in your simulation
either by itself or as a sub-style in a pair_style hybrid or hybrid/overlay command. If the sub-style is
used more than once, an additional number nsub has to be specified
in order to choose which instance of the sub-style will be used by
the compute. Not specifying the number in this case will cause the
compute to fail.

The evalue setting is optional.  All
pair styles tally a potential energy epair which may be broken into
two parts: evdwl and ecoul such that epair = evdwl + ecoul.
If the pair style calculates Coulombic interactions, their energy will
be tallied in ecoul.  Everything else (whether it is a Lennard-Jones
style van der Waals interaction or not) is tallied in evdwl.  If
evalue is blank or specified as epair, then epair is stored
as a global scalar by this compute.  This is useful when using
pair_style hybrid if you want to know the portion
of the total energy contributed by one sub-style.  If evalue is
specified as evdwl or ecoul, then just that portion of the energy
is stored as a global scalar.

Note
The energy returned by the evdwl keyword does not include tail
corrections, even if they are enabled via the
pair_modify command.

Some pair styles tally additional quantities, e.g. a breakdown of
potential energy into 14 components is tallied by the
pair_style reaxff command.  These values (1 or more)
are stored as a global vector by this compute.  See the page for
individual pair styles for info on these values.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 all pair gauss
compute 1 all pair lj/cut/coul/cut ecoul
compute 1 all pair tersoff 2 epair
compute 1 all pair reaxff
```

## Restrictions

Restrictions 
none

## Related Commands

- [compute pe](compute_pe.html)
- [compute bond](compute_bond.html)
- [fix pair](fix_pair.html)

