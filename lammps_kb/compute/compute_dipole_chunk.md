---
id: compute_dipole_chunk
title: "compute dipole/chunk command"
url: https://docs.lammps.org/compute_dipole_chunk.html
---

# compute dipole/chunk command

## Syntax

```
compute ID group-ID style chunkID arg
```

## Description

Define a computation that calculates the dipole vector and total dipole
for multiple chunks of atoms.

In LAMMPS, chunks are collections of atoms defined by a compute
chunk/atom command, which assigns each atom to a
single chunk (or no chunk).  The ID for this command is specified as
chunkID.  For example, a single chunk could be the atoms in a molecule
or atoms in a spatial bin.  See the compute chunk/atom and Howto chunk doc pages for
details of how chunks can be defined and examples of how they can be
used to measure properties of a system.

These computes calculate the \((x,y,z)\) coordinates of the dipole
vector and the total dipole moment for each chunk, which includes all
effects due to atoms passing through periodic boundaries.  For chunks
with a net charge the resulting dipole is made position independent by
subtracting the position vector of the center of mass or geometric
center times the net charge from the computed dipole vector.  Both
per-atom charges and per-atom dipole moments, if present, contribute to
the computed dipole.

Added in version 28Mar2023.

Compute dipole/tip4p/chunk includes adjustments for the charge
carrying point M in molecules with TIP4P water geometry.  The
corresponding parameters are extracted from the pair style.

Note that only atoms in the specified group contribute to the
calculation.  The compute chunk/atom command
defines its own group; atoms will have a chunk ID = 0 if they are not in
that group, signifying they are not assigned to a chunk, and will thus
also not contribute to this calculation.  You can specify the  all 
group for this command if you simply want to include atoms with non-zero
chunk IDs.

Note
The coordinates of an atom contribute to the chunk s dipole in
 unwrapped  form, by using the image flags associated with each atom.
See the dump custom command for a discussion of
 unwrapped  coordinates.  See the Atoms section of the
read_data command for a discussion of image flags
and how they are set for each atom.  You can reset the image flags
(e.g., to 0) before invoking this compute by using the set image command.

The simplest way to output the results of the compute com/chunk
calculation to a file is to use the fix ave/time
command, for example:

compute cc1 all chunk/atom molecule
compute myChunk all dipole/chunk cc1
fix 1 all ave/time 100 1 100 c_myChunk[*] file tmp.out mode vector

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 fluid dipole/chunk molchunk
compute dw water dipole/chunk 1 geometry
```

## Restrictions

Restrictions 
Compute style dipole/tip4p/chunk is part of the EXTRA-COMPUTE
package. It is only enabled if LAMMPS was built with that package.  See
the Build package page for more info.
Compute style dipole/tip4p/chunk can only be used with tip4p pair
styles.

## Related Commands

- [compute com/chunk](compute_com_chunk.html)
- [compute dipole](compute_dipole.html)

