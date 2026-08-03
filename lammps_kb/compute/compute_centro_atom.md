---
id: compute_centro_atom
title: "compute centro/atom command"
url: https://docs.lammps.org/compute_centro_atom.html
---

# compute centro/atom command

## Syntax

```
compute ID group-ID centro/atom lattice keyword value ...
axes value = no or yes
  no = do not calculate 3 symmetry axes
  yes = calculate 3 symmetry axes
```

## Description

Define a computation that calculates the centro-symmetry parameter for
each atom in the group, for either FCC or BCC lattices, depending on
the choice of the lattice argument.  In solid-state systems the
centro-symmetry parameter is a useful measure of the local lattice
disorder around an atom and can be used to characterize whether the
atom is part of a perfect lattice, a local defect (e.g. a dislocation
or stacking fault), or at a surface.

The value of the centro-symmetry parameter will be 0.0 for atoms not
in the specified compute group.

This parameter is computed using the following formula from
(Kelchner)

\[CS = \sum_{i = 1}^{N/2} | \vec{R}_i + \vec{R}_{i+N/2} |^2\]

where the \(N\) nearest neighbors of each atom are identified and
\(\vec{R}_i\) and \(\vec{R}_{i+N/2}\) are vectors from the
central atom to a particular pair of nearest neighbors.  There are
\(N (N-1)/2\) possible neighbor pairs that can contribute to this
formula.  The quantity in the sum is computed for each, and the
\(N/2\) smallest are used.  This will typically be for pairs of
atoms in symmetrically opposite positions with respect to the central
atom; hence the \(i+N/2\) notation.

\(N\) is an input parameter, which should be set to correspond to
the number of nearest neighbors in the underlying lattice of atoms.
If the keyword fcc or bcc is used, N is set to 12 and 8
respectively.  More generally, N can be set to a positive, even
integer.

For an atom on a lattice site, surrounded by atoms on a perfect
lattice, the centro-symmetry parameter will be 0.  It will be near 0
for small thermal perturbations of a perfect lattice.  If a point
defect exists, the symmetry is broken, and the parameter will be a
larger positive value.  An atom at a surface will have a large
positive parameter.  If the atom does not have \(N\) neighbors
(within the potential cutoff), then its centro-symmetry parameter is
set to 0.0.

If the keyword axes has the setting yes, then this compute also
estimates three symmetry axes for each atom s local neighborhood.  The
first two of these are the vectors joining the two pairs of neighbor
atoms with smallest contributions to the centrosymmetry parameter,
i.e. the two most symmetric pairs of atoms.  The third vector is
normal to the first two by the right-hand rule.  All three vectors are
normalized to unit length.  For FCC crystals, the first two vectors
will lie along a \(\langle110\rangle\) direction, while the third vector
will lie along either a \(\langle100\rangle\) or \(\langle111\rangle\)
direction.  For HCP crystals, the first two vectors will lie along
\(\langle1000\rangle\) directions, while the third vector
will lie along \(\langle0001\rangle\).  This provides a simple way to
measure local orientation in HCP structures.  In general, the axes keyword
can be used to estimate the orientation of symmetry axes in the neighborhood
of any atom.

Only atoms within the cutoff of the pairwise neighbor list are
considered as possible neighbors.  Atoms not in the compute group are
included in the \(N\) neighbors used in this calculation.

The neighbor list needed to compute this quantity is constructed each
time the calculation is performed (e.g., each time a snapshot of atoms
is dumped).  Thus it can be inefficient to compute/dump this quantity
too frequently or to have multiple compute/dump commands, each with a
centro/atom style.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 all centro/atom fcc

compute 1 all centro/atom 8
```

## Restrictions

Restrictions 
none

## Related Commands

- [compute cna/atom](compute_cna_atom.html)

