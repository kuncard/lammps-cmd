---
id: compute_nbond_atom
title: "compute nbond/atom command"
url: https://docs.lammps.org/compute_nbond_atom.html
---

# compute nbond/atom command

## Syntax

```
compute ID group-ID nbond/atom keyword value
bond/type value = btype
  btype = bond type included in count
```

## Description

Added in version 4May2022.

Define a computation that computes the number of bonds each atom is
part of.  Bonds which are broken are not counted in the tally.  See
the Howto broken bonds page for more information.
The number of bonds will be zero for atoms not in the specified
compute group. This compute does not depend on Newton bond settings.

If the keyword bond/type is specified, only bonds of btype are
counted.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 all nbond/atom
compute 1 all nbond/atom bond/type 2
```

## Restrictions

Restrictions 
This compute is part of the BPM package.  It is only enabled if LAMMPS was
built with that package.  See the Build package
page for more info.

## Related Commands

Related commands

