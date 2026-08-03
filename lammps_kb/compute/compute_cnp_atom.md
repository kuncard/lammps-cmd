---
id: compute_cnp_atom
title: "compute cnp/atom command"
url: https://docs.lammps.org/compute_cnp_atom.html
---

# compute cnp/atom command

## Syntax

```
compute ID group-ID cnp/atom cutoff
```

## Description

Define a computation that calculates the Common Neighborhood
Parameter (CNP) for each atom in the group.  In solid-state systems
the CNP is a useful measure of the local crystal structure
around an atom and can be used to characterize whether the
atom is part of a perfect lattice, a local defect (e.g., a dislocation
or stacking fault), or at a surface.

The value of the CNP parameter will be 0.0 for atoms not in the
specified compute group.  Note that normally a CNP calculation should
only be performed on single component systems.

This parameter is computed using the following formula from
(Tsuzuki)

\[Q_{i} = \frac{1}{n_i}\sum_{j = 1}^{n_i} \left\lVert \sum_{k = 1}^{n_{ij}}  \vec{R}_{ik} + \vec{R}_{jk} \right\rVert^{2}\]

where the index j goes over the \(n_i\) nearest neighbors of atom
i, and the index k goes over the \(n_{ij}\) common nearest neighbors
between atom i and atom j. \(\vec{R}_{ik}\) and
\(\vec{R}_{jk}\) are the vectors connecting atom k to atoms i
and j.  The quantity in the double sum is computed
for each atom.

The CNP calculation is sensitive to the specified cutoff value.
You should ensure that the appropriate nearest neighbors of an atom are
found within the cutoff distance for the presumed crystal structure.
E.g. 12 nearest neighbor for perfect FCC and HCP crystals, 14 nearest
neighbors for perfect BCC crystals.  These formulas can be used to
obtain a good cutoff distance:

\[\begin{split}r_{c}^{\mathrm{fcc}} = & \frac{1}{2} \left(\frac{\sqrt{2}}{2} + 1\right) a
  \approx 0.8536 a \\
r_{c}^{\mathrm{bcc}} = & \frac{1}{2}(\sqrt{2} + 1) a
  \approx 1.207 a \\
r_{c}^{\mathrm{hcp}} = & \frac{1}{2}\left(1+\sqrt{\frac{4+2x^{2}}{3}}\right) a\end{split}\]

where \(a\) is the lattice constant for the crystal structure concerned
and in the HCP case, \(x = (c/a) / 1.633\), where 1.633 is the ideal
\(c/a\) for HCP crystals.

Also note that since the CNP calculation in LAMMPS uses the neighbors
of an owned atom to find the nearest neighbors of a ghost atom, the
following relation should also be satisfied:

\[r_c + r_s > 2*\mathrm{cutoff}\]

where \(r_c\) is the cutoff distance of the potential, \(r_s\) is
the skin
distance as specified by the neighbor command, and
cutoff is the argument used with the compute cnp/atom command.  LAMMPS
will issue a warning if this is not the case.

The neighbor list needed to compute this quantity is constructed each
time the calculation is performed (e.g., each time a snapshot of atoms
is dumped).  Thus it can be inefficient to compute/dump this quantity
too frequently or to have multiple compute/dump commands, each with a
cnp/atom style.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 all cnp/atom 3.08
```

## Restrictions

Restrictions 
This compute is part of the EXTRA-COMPUTE package.  It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.

## Related Commands

- [compute cna/atom](compute_cna_atom.html)
- [compute centro/atom](compute_centro_atom.html)

