---
id: pair_zero
title: "pair_style zero command"
url: https://docs.lammps.org/pair_zero.html
---

# pair_style zero command

## Syntax

```
pair_style zero cutoff [nocoeff] [full]
```

## Description

Define a global or per-type cutoff length for the purpose of
building a neighbor list and acquiring ghost atoms, but do
not compute any pairwise forces or energies.

This can be useful for fixes or computes which require a neighbor list
to enumerate pairs of atoms within some cutoff distance, but when
pairwise forces are not otherwise needed.  Examples are the fix bond/create, compute rdf,
compute voronoi/atom commands.

Note that the comm_modify cutoff command can be
used to ensure communication of ghost atoms even when a pair style is
not defined, but it will not trigger neighbor list generation.

The optional nocoeff flag allows to read data files with a PairCoeff
section for any pair style. Similarly, any pair_coeff commands
will only be checked for the atom type numbers and the rest ignored.
In this case, only the global cutoff will be used.

Added in version 3Nov2022.

The optional full flag builds a full neighbor list instead of the default
half neighbor list.

The following coefficients must be defined for each pair of atoms
types via the pair_coeff command as in the examples
above, or in the data file or restart files read by the
read_data or read_restart
commands, or by mixing as described below:

This coefficient is optional.  If not specified, the global cutoff
specified in the pair_style command is used. If the pair_style has
been specified with the optional nocoeff flag, then a cutoff
pair coefficient is ignored.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
pair_style zero 10.0
pair_style zero 5.0 nocoeff
pair_coeff * *
pair_coeff 1 2*4 3.0
```

## Restrictions

Restrictions 
none

## Related Commands

- [pair_style none](pair_none.html)

