---
id: fix_phonon
title: "fix phonon command"
url: https://docs.lammps.org/fix_phonon.html
---

# fix phonon command

## Syntax

```
fix ID group-ID phonon N Noutput Nwait map_file prefix keyword values ...
file is the file that contains the mapping info between atom ID and the lattice indices.
GAMMA flags to treate the whole simulation box as a unit cell, so that the mapping
info can be generated internally. In this case, dynamical matrix at only the gamma-point
will/can be evaluated.
sysdim value = d
  d = dimension of the system, usually the same as the MD model dimension
nasr value = n
  n = number of iterations to enforce the acoustic sum rule
```

## Description

Calculate the dynamical matrix from molecular dynamics simulations
based on fluctuation-dissipation theory for a group of atoms.

Consider a crystal with \(N\) unit cells in three dimensions labeled
\(l = (l_1, l_2, l_3)\) where \(l_i\) are integers.  Each unit cell is
defined by three linearly independent vectors \(\mathbf{a}_1\),
\(\mathbf{a}_2\), \(\mathbf{a}_3\) forming a parallelepiped,
containing \(K\) basis atoms labeled \(k\).

Based on fluctuation-dissipation theory, the force constant
coefficients of the system in reciprocal space are given by
(Campana , Kong)

\[\mathbf{\Phi}_{k\alpha,k^\prime \beta}(\mathbf{q}) = k_B T \mathbf{G}^{-1}_{k\alpha,k^\prime \beta}(\mathbf{q})\]

where \(\mathbf{G}\) is the Green s functions coefficients given by

\[\mathbf{G}_{k\alpha,k^\prime \beta}(\mathbf{q}) = \left< \mathbf{u}_{k\alpha}(\mathbf{q}) \bullet \mathbf{u}_{k^\prime \beta}^*(\mathbf{q}) \right>\]

where \(\left< \ldots \right>\) denotes the ensemble average, and

\[\mathbf{u}_{k\alpha}(\mathbf{q}) = \sum_l \mathbf{u}_{l k \alpha} \exp{(i\mathbf{qr}_l)}\]

is the \(\alpha\) component of the atomic displacement for the \(k\)
th atom in the unit cell in reciprocal space at \(\mathbf{q}\). In
practice, the Green s functions coefficients can also be measured
according to the following formula,

\[\mathbf{G}_{k\alpha,k^\prime \beta}(\mathbf{q}) =
\left< \mathbf{R}_{k \alpha}(\mathbf{q}) \bullet \mathbf{R}^*_{k^\prime \beta}(\mathbf{q}) \right>
- \left<\mathbf{R}\right>_{k \alpha}(\mathbf{q}) \bullet \left<\mathbf{R}\right>^*_{k^\prime \beta}(\mathbf{q})\]

where \(\mathbf{R}\) is the instantaneous positions of atoms, and
\(\left<\mathbf{R}\right>\) is the averaged atomic positions. It
gives essentially the same results as the displacement method and is
easier to implement in an MD code.

Once the force constant matrix is known, the dynamical matrix
\(\mathbf{D}\) can then be obtained by

\[\mathbf{D}_{k\alpha, k^\prime\beta}(\mathbf{q}) =
(m_k m_{k^\prime})^{-\frac{1}{2}} \mathbf{\Phi}_{k \alpha, k^\prime \beta}(\mathbf{q})\]

whose eigenvalues are exactly the phonon frequencies at \(\mathbf{q}\).

This fix uses positions of atoms in the specified group and calculates
two-point correlations.  To achieve this. the positions of the atoms
are examined every Nevery steps and are Fourier-transformed into
reciprocal space, where the averaging process and correlation
computation is then done.  After every Noutput measurements, the
matrix \(\mathbf{G}(\mathbf{q})\) is calculated and inverted to
obtain the elastic stiffness coefficients.  The dynamical matrices are
then constructed and written to prefix.bin.timestep files in binary
format and to the file prefix.log for each wave-vector
\(\mathbf{q}\).

A detailed description of this method can be found in
(Kong2011).

The sysdim keyword is optional.  If specified with a value smaller
than the dimensionality of the LAMMPS simulation, its value is used
for the dynamical matrix calculation.  For example, using LAMMPS to
model a 2D or 3D system, the phonon dispersion of a 1D atomic chain
can be computed using sysdim = 1.

The nasr keyword is optional.  An iterative procedure is employed to
enforce the acoustic sum rule on \(\Phi\) at \(\Gamma\), and the number
provided by keyword nasr gives the total number of iterations. For a
system whose unit cell has only one atom, nasr = 1 is sufficient;
for other systems, nasr = 10 is typically sufficient.

The map_file contains the mapping information between the lattice
indices and the atom IDs, which tells the code which atom sits at
which lattice point; the lattice indices start from 0. An auxiliary
code, latgen, can be employed to
generate the compatible map file for various crystals.

In case one simulates a non-periodic system, where the whole simulation
box is treated as a unit cell, one can set map_file as GAMMA, so
that the mapping info will be generated internally and a file is not
needed. In this case, the dynamical matrix at only the gamma-point
will/can be evaluated. Please keep in mind that fix-phonon is designed
for cyrstals, it will be inefficient and even degrade the performance
of LAMMPS in case the unit cell is too large.

The calculated dynamical matrix elements are written out in
energy/distance^2/mass units.  The coordinates for q
points in the log file is in the units of the basis vectors of the
corresponding reciprocal lattice.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 1 all phonon 20 5000 200000 map.in LJ1D sysdim 1
fix 1 all phonon 20 5000 200000 map.in EAM3D
fix 1 all phonon 10 5000 500000 GAMMA EAM0D nasr 100
```

## Restrictions

Restrictions 
This fix assumes a crystalline system with periodical lattice. The
temperature of the system should not exceed the melting temperature to
keep the system in its solid state.
This fix is part of the PHONON package.  It is only enabled if LAMMPS
was built with that package.  This fix also requires LAMMPS to be built
with 3d-FFT support which is included in the KSPACE package.  See the
Build package page for more info.

## Related Commands

- [compute msd](compute_msd.html)
- [dynamical_matrix](dynamical_matrix.html)

