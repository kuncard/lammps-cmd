---
id: fix_spring_chunk
title: "fix spring/chunk command"
url: https://docs.lammps.org/fix_spring_chunk.html
---

# fix spring/chunk command

## Syntax

```
fix ID group-ID spring/chunk K chunkID comID
```

## Description

Apply a spring force to the center-of-mass (COM) of chunks of atoms as
defined by the compute chunk/atom command.
Chunks can be molecules or spatial bins or other groupings of atoms.
This is a way of tethering each chunk to its initial COM coordinates.

The chunkID is the ID of a compute chunk/atom command defined in the
input script.  It is used to define the chunks.  The comID is the ID
of a compute com/chunk command defined in the input script.  It is
used to compute the COMs of each chunk.

At the beginning of the first run or
minimize command after this fix is defined, the
initial COM of each chunk is calculated and stored as R0m, where M is
the chunk number.  Thereafter, at every timestep (or minimization
iteration), the current COM of each chunk is calculated as Rm.  A
restoring force of magnitude K (Rm - R0m) Mi / Mm is applied to each
atom in each chunk where K is the specified spring constant, Mi is
the mass of the atom, and Mm is the total mass of all atoms in the
chunk.  Note that K thus represents the spring constant for the
total force on each chunk of atoms, not for a spring applied to each
atom.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix restrain all spring/chunk 100 chunkID comID
```

## Restrictions

Restrictions 
none

## Related Commands

- [fix spring](fix_spring.html)
- [fix spring/self](fix_spring_self.html)
- [fix spring/rg](fix_spring_rg.html)

