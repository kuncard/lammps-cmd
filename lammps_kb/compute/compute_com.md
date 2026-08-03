---
id: compute_com
title: "compute com command"
url: https://docs.lammps.org/compute_com.html
---

# compute com command

## Syntax

```
compute ID group-ID com
```

## Description

Define a computation that calculates the center-of-mass of the group
of atoms, including all effects due to atoms passing through periodic
boundaries.

A vector of three quantities is calculated by this compute, which
are the \((x,y,z)\) coordinates of the center of mass.

Note
The coordinates of an atom contribute to the center-of-mass in
 unwrapped  form, by using the image flags associated with each atom.
See the dump custom command for a discussion of
 unwrapped  coordinates.  See the Atoms section of the
read_data command for a discussion of image flags and
how they are set for each atom.  You can reset the image flags
(e.g., to 0) before invoking this compute by using the
set image command.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 all com
```

## Restrictions

Restrictions 
none

## Related Commands

- [compute com/chunk](compute_com_chunk.html)

