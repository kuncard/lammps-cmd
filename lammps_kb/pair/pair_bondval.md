---
id: pair_bondval
title: "pair_style bondval command"
url: https://docs.lammps.org/pair_bondval.html
---

# pair_style bondval command

## Syntax

```
pair_style bondval power cutoff
pair_style bondval/vec power cutoff
```

## Description

Added in version 4Jul2026.

The bond-valence potential is an empirical potential based on the
conservation of the bond-valence (bondval) and bond-valence vector
(bondval/vec), fitted to DFT calculations for a given bulk semiconductor.
It is typically used with pair_style hybrid/overlay
to combine Coulombic, Lennard-Jones repulsion, bond-valence, and
bond-valence vector contributions.

The bond-valence for a given atom pair (\(V_{ij}\)) is a measure
of the bonding strength calculated from the length of the bond
(\(r_{ij}\)) by:

\[V_{ij} = \left( \frac{r0_{ij}}{r_{ij}} \right)^{\alpha_{ij}}\]

where \(r0_{ij}\) and \(\alpha_{ij}\) are Brown s empirical
parameters for bond-valence.  The bond-valence vector is a vector lying
along the bond between atom i and j:
\(\vec{V}_{ij} = V_{ij} \hat{R}_{ij}\), where
\(\hat{R}_{ij}\) is the unit vector pointing from atom i toward atom j.

The total potential energy of the system consists of a Coulombic energy
(\(E_c\)), a short-range repulsive energy (\(E_r\)), a
bond-valence energy (\(E_{BV}\)), a bond-valence vector energy
(\(E_{BVV}\)), and an optional angle potential (\(E_a\)):

\[E = E_c + E_r + E_{BV} + E_{BVV} + E_a\]

\[E_c = \sum_{i<j} \frac{q_i q_j}{r_{ij}}\]

\[E_r = \sum_{i<j} \left(\frac{B_{ij}}{r_{ij}}\right)^{12}\]

\[E_{BV} = \sum_i S_i \left(V_i - V_{0,i}\right)^2\]

\[E_{BVV} = \sum_i D_i \left(|\vec{W}_i|^2-|\vec{W}_{0,i}|^2\right)^2\]

\[E_a = k \sum_i^{N_{\mathrm{oxygen}}} \left(\theta_i - 180^{\circ}\right)^2\]

where \(V_i = \sum_{j \neq i} V_{ij}\) is the bond-valence sum
(BVS), and \(\vec{W}_i = \sum_{j \neq i} \vec{V}_{ij}\) is
the bond-valence vector sum (BVVS), \(q_i\) is the ionic
charge, \(B_{ij}\) is the short-range repulsion parameter,
\(S_i\) and \(D_i\) are scaling parameters (energy units),
\(k\) is the angle spring constant, and \(\theta_i\) is the
O-O-O angle along the common axis of two adjacent oxygen octahedra.

The pair style bondval computes \(E_{BV}\), the bond-valence
energy term.  The pair style bondval/vec computes \(E_{BVV}\), the
bond-valence vector energy term.  The remaining energy contributions
(\(E_c\) and \(E_r\)) are typically provided by pair_style
lj/cut/coul/long, and \(E_a\) by an
angle_style.  The power argument to the
pair_style command specifies the exponent used in computing the forces
and is usually set to 2.0.

The quantities \(r_{ij}\), \(V_i\), and \(\vec{W}_i\)
are computed at each timestep from the current atom positions.  All
other parameters must be provided by the user.

The potential parameters are obtained by training against DFT energies
for a given system.  Trained and tested parameters for several bulk
perovskite oxide materials are published by the group of Andrew M. Rappe
(see references below).  The published parameters use LAMMPS metal
units.  Atom charges are also fitted parameters; they can be set via
read_data or set.  The angle potential,
if used, can be set with angle_style harmonic
together with angle_coeff.

The following coefficients must be defined for each pair of atom types
via the pair_coeff command as in the examples
above, or in the data file or restart files read by the
read_data or read_restart
commands.  When used within pair_style hybrid/overlay,
the pair style name must be included as shown in the examples.

For bondval:

The first two parameters (\(r0_{ij}\) and \(\alpha_{ij}\)) are
pair atom-type dependent and contribute to the bond-valence calculation for all
atom-type pairs.  The penalty constant \(S_i\) and ideal value
\(V_{0,i}\) are single atom-type dependent. Thus only same-species values
(I = J) are nonzero in input file.

For bondval/vec:

The same distinction applies: \(r0_{ij}\) and \(\alpha_{ij}\)
are pair atom-type dependent and used for all pairs, while \(D_i\) and
\(W_{0,i}\) are atom-type dependent. Thus only same-species values
(I = J) are nonzero in input file.

The final cutoff coefficient is optional for both styles.  If not
specified, the global cutoff given in the pair_style command is used.

Styles with a gpu, intel, kk, omp, or opt suffix are
functionally the same as the corresponding style without the suffix.
They have been optimized to run faster, depending on your available
hardware, as discussed on the Accelerator packages
page.  The accelerated styles take the same arguments and should
produce the same results, except for round-off and precision issues.

These accelerated styles are part of the GPU, INTEL, KOKKOS,
OPENMP, and OPT packages, respectively.  They are only enabled if
LAMMPS was built with those packages.  See the Build package page for more info.

You can specify the accelerated styles explicitly in your input script
by including their suffix, or you can use the -suffix command-line switch when you invoke LAMMPS, or you can use the
suffix command in your input script.

See the Accelerator packages page for more
instructions on how to use the accelerated styles effectively.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
pair_style hybrid/overlay lj/cut/coul/long 8.0 8.0 bondval 2.0 8.0 bondval/vec 2.0 8.0

# lj/cut/coul/long parameters: epsilon sigma
pair_coeff 1 1 lj/cut/coul/long 2.0 2.44805
pair_coeff 1 2 lj/cut/coul/long 2.0 2.32592
pair_coeff 1 3 lj/cut/coul/long 2.0 1.98792
pair_coeff 2 2 lj/cut/coul/long 2.0 2.73825
pair_coeff 2 3 lj/cut/coul/long 2.0 1.37741
pair_coeff 3 3 lj/cut/coul/long 2.0 1.99269

# bondval parameters: r0 alpha S V0
pair_coeff 1 1 bondval 0.0000000 5.0000000 0.5973900 2.0000000
pair_coeff 1 2 bondval 0.0000000 5.0000000 0.0000000 0.0000000
pair_coeff 1 3 bondval 2.2900000 8.9400000 0.0000000 0.0000000
pair_coeff 2 2 bondval 0.0000000 5.0000000 0.1653300 4.0000000
pair_coeff 2 3 bondval 1.7980000 5.2000000 0.0000000 0.0000000
pair_coeff 3 3 bondval 0.0000000 5.0000000 0.9306300 2.0000000

# bondval/vec parameters: r0 alpha D W0
pair_coeff 1 1 bondval/vec 0.0000000 5.0000000 0.0842900 0.1156100
pair_coeff 1 2 bondval/vec 0.0000000 5.0000000 0.0000000 0.0000000
pair_coeff 1 3 bondval/vec 2.1430000 8.9400000 0.0000000 0.0000000
pair_coeff 2 2 bondval/vec 0.0000000 5.0000000 0.8248400 0.3943700
pair_coeff 2 3 bondval/vec 1.7980000 5.2000000 0.0000000 0.0000000
pair_coeff 3 3 bondval/vec 0.0000000 5.0000000 0.2800600 0.3165100
```

## Restrictions

Restrictions 
These pair styles are part of the EXTRA-PAIR package.  They are only
enabled if LAMMPS was built with that package.  See the
Build package page for more info.
These pair styles must be used with
pair_style hybrid/overlay.  They cannot be used
as standalone pair styles.
For a physically correct simulation, bondval, bondval/vec, and a
pair_style lj/cut/coul/long contribution
for \(E_c\) and \(E_r\) must all be combined via
hybrid/overlay.  The published parameters for this potential are
fitted to only include \(r^{-12}\) repulsion term
(\(E_r\)) in the Lennard-Jones potential, while the attractive \(r^{-6}\)
contribution is set to 0.
To run with the published parameters correctly, users must manually initialize
the internal variables lj2 and lj4 in the source code of
pair_style lj/cut/coul/long to be zero
in order to remove the attractive \(r^{-6}\) contribution.

## Related Commands

- [pair_style hybrid/overlay](pair_hybrid.html)
- [pair_style lj/cut/coul/long](pair_lj_cut_coul.html)
- [angle_style harmonic](angle_harmonic.html)
- [kspace_style](kspace_style.html)

