---
id: compute_cna_atom
title: "compute cna/atom command"
url: https://docs.lammps.org/compute_cna_atom.html
---

# compute cna/atom command

## Syntax

```
compute ID group-ID cna/atom cutoff
```

## Description

Define a computation that calculates the CNA (Common Neighbor
Analysis) pattern for each atom in the group.  In solid-state systems
the CNA pattern is a useful measure of the local crystal structure
around an atom.  The CNA methodology is described in (Faken)
and (Tsuzuki).

Currently, there are five kinds of CNA patterns LAMMPS recognizes:

The value of the CNA pattern will be 0 for atoms not in the specified
compute group.  Note that normally a CNA calculation should only be
performed on mono-component systems.

The CNA calculation can be sensitive to the specified cutoff value.
You should ensure the appropriate nearest neighbors of an atom are
found within the cutoff distance for the presumed crystal structure
(e.g., 12 nearest neighbor for perfect FCC and HCP crystals, 14 nearest
neighbors for perfect BCC crystals).  These formulas can be used to
obtain a good cutoff distance:

\[\begin{split}r_{c}^{\mathrm{fcc}} = & \frac{1}{2} \left(\frac{\sqrt{2}}{2} + 1\right) a
  \approx 0.8536 a \\
r_{c}^{\mathrm{bcc}} = & \frac{1}{2}(\sqrt{2} + 1) a
  \approx 1.207 a \\
r_{c}^{\mathrm{hcp}} = & \frac{1}{2}\left(1+\sqrt{\frac{4+2x^{2}}{3}}\right) a\end{split}\]

where \(a\) is the lattice constant for the crystal structure concerned
and in the HCP case, \(x = (c/a) / 1.633\), where 1.633 is the ideal
\(c/a\) for HCP crystals.

Also note that since the CNA calculation in LAMMPS uses the neighbors
of an owned atom to find the nearest neighbors of a ghost atom, the
following relation should also be satisfied:

\[r_c + r_s > 2*\mathrm{cutoff}\]

where \(r_c\) is the cutoff distance of the potential, \(r_s\)
is the skin
distance as specified by the neighbor command, and
cutoff is the argument used with the compute cna/atom command.  LAMMPS
will issue a warning if this is not the case.

The neighbor list needed to compute this quantity is constructed each
time the calculation is performed (e.g. each time a snapshot of atoms
is dumped).  Thus it can be inefficient to compute/dump this quantity
too frequently or to have multiple compute/dump commands, each with a
cna/atom style.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 all cna/atom 3.08
```

## Restrictions

Restrictions 
none

## Related Commands

- [compute centro/atom](compute_centro_atom.html)

