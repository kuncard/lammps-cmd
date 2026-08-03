---
id: compute_gyration_chunk
title: "compute gyration/chunk command"
url: https://docs.lammps.org/compute_gyration_chunk.html
---

# compute gyration/chunk command

## Syntax

```
compute ID group-ID gyration/chunk chunkID keyword value ...
tensor value = none
```

## Description

Define a computation that calculates the radius of gyration \(R_g\) for
multiple chunks of atoms.

In LAMMPS, chunks are collections of atoms defined by a
compute chunk/atom command, which assigns each atom
to a single chunk (or no chunk).  The ID for this command is specified
as chunkID.  For example, a single chunk could be the atoms in a
molecule or atoms in a spatial bin.
See the compute chunk/atom and
Howto chunk
doc pages for details of how chunks can be defined and examples of how
they can be used to measure properties of a system.

This compute calculates the radius of gyration \(R_g\) for each chunk,
which includes all effects due to atoms passing through periodic
boundaries.

\(R_g\) is a measure of the size of a chunk, and is computed by the
formula

\[R_g^2 = \frac{1}{M} \sum_i m_i (r_i - r_{\text{cm}})^2\]

where \(M\) is the total mass of the chunk, \(r_{\text{cm}}\) is
the center-of-mass position of the chunk, and the sum is over all atoms in the
chunk.

Note that only atoms in the specified group contribute to the
calculation.  The compute chunk/atom command
defines its own group; atoms will have a chunk ID = 0 if they are not
in that group, signifying they are not assigned to a chunk, and will
thus also not contribute to this calculation.  You can specify the
 all  group for this command if you simply want to include atoms with
non-zero chunk IDs.

If the tensor keyword is specified, then the scalar \(R_g\) value is not
calculated, but an \(R_g\) tensor is instead calculated for each chunk.
The formula for the components of the tensor is the same as the above
formula, except that \((r_i - r_{\text{cm}})^2\) is replaced by
\((r_{i,x} - r_{\text{cm},x}) \cdot (r_{i,y} - r_{\text{cm},y})\) for the
\(xy\) component, and so on.  The six components of the tensor are
ordered \(xx\), \(yy\), \(zz\), \(xy\), \(xz\), \(yz\).

Note
The coordinates of an atom contribute to \(R_g\) in  unwrapped  form,
by using the image flags associated with each atom.  See the dump custom
command for a discussion of  unwrapped  coordinates.
See the Atoms section of the read_data command for a
discussion of image flags and how they are set for each atom.  You can
reset the image flags (e.g., to 0) before invoking this compute by
using the set image command.

The simplest way to output the results of the compute gyration/chunk
calculation to a file is to use the fix ave/time
command, for example:

compute cc1 all chunk/atom molecule
compute myChunk all gyration/chunk cc1
fix 1 all ave/time 100 1 100 c_myChunk file tmp.out mode vector

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 molecule gyration/chunk molchunk
compute 2 molecule gyration/chunk molchunk tensor
```

## Restrictions

Restrictions 
none

## Related Commands

- [compute gyration](compute_gyration.html)

