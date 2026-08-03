---
id: compute_vcm_chunk
title: "compute vcm/chunk command"
url: https://docs.lammps.org/compute_vcm_chunk.html
---

# compute vcm/chunk command

## Syntax

```
compute ID group-ID vcm/chunk chunkID
```

## Description

Define a computation that calculates the center-of-mass velocity for
multiple chunks of atoms.

In LAMMPS, chunks are collections of atoms defined by a
compute chunk/atom command, which assigns each atom
to a single chunk (or no chunk).  The ID for this command is specified as
chunkID.  For example, a single chunk could be the atoms in a molecule or atoms
in a spatial bin.  See the compute chunk/atom and
Howto chunk doc pages for details of how chunks can be
defined and examples of how they can be used to measure properties of a system.

This compute calculates the \((x,y,z)\) components of the center-of-mass
velocity for each chunk.  This is done by summing mass*velocity for
each atom in the chunk and dividing the sum by the total mass of the
chunk.

Note that only atoms in the specified group contribute to the
calculation.  The compute chunk/atom command
defines its own group; atoms will have a chunk ID = 0 if they are not
in that group, signifying they are not assigned to a chunk, and will
thus also not contribute to this calculation.  You can specify the
 all  group for this command if you simply want to include atoms with
non-zero chunk IDs.

The simplest way to output the results of the compute vcm/chunk
calculation to a file is to use the fix ave/time
command, for example:

compute cc1 all chunk/atom molecule
compute myChunk all vcm/chunk cc1
fix 1 all ave/time 100 1 100 c_myChunk[*] file tmp.out mode vector

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 fluid vcm/chunk molchunk
```

## Restrictions

Restrictions 
none

## Related Commands

Related commands 
none

