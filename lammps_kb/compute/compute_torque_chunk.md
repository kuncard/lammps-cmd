---
id: compute_torque_chunk
title: "compute torque/chunk command"
url: https://docs.lammps.org/compute_torque_chunk.html
---

# compute torque/chunk command

## Syntax

```
compute ID group-ID torque/chunk chunkID
```

## Description

Define a computation that calculates the torque on multiple chunks of
atoms.

In LAMMPS, chunks are collections of atoms defined by a
compute chunk/atom command, which assigns each atom
to a single chunk (or no chunk).  The ID for this command is specified
as chunkID.  For example, a single chunk could be the atoms in a
molecule or atoms in a spatial bin.  See the
compute chunk/atom and
Howto chunk
doc pages for details of how chunks can be defined and examples of how
they can be used to measure properties of a system.

This compute calculates the three components of the torque vector for eqch
chunk, due to the forces on the individual atoms in the chunk around
the center-of-mass of the chunk.  The calculation includes all effects
due to atoms passing through periodic boundaries.

Note that only atoms in the specified group contribute to the
calculation.  The compute chunk/atom command
defines its own group; atoms will have a chunk ID = 0 if they are not
in that group, signifying they are not assigned to a chunk, and will
thus also not contribute to this calculation.  You can specify the
 all  group for this command if you simply want to include atoms with
non-zero chunk IDs.

Note
The coordinates of an atom contribute to the chunk s torque in
 unwrapped  form, by using the image flags associated with each atom.
See the dump custom command for a discussion of
 unwrapped  coordinates.  See the Atoms section of the
read_data command for a discussion of image flags and
how they are set for each atom.  You can reset the image flags
(e.g., to 0) before invoking this compute by using the
set image command.

The simplest way to output the results of the compute torque/chunk
calculation to a file is to use the fix ave/time
command, for example:

compute cc1 all chunk/atom molecule
compute myChunk all torque/chunk cc1
fix 1 all ave/time 100 1 100 c_myChunk[*] file tmp.out mode vector

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 fluid torque/chunk molchunk
```

## Restrictions

Restrictions 
none

## Related Commands

- [variable torque() function](variable.html)

