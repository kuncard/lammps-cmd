---
id: pair_dpd_coul_slater_long
title: "pair_style dpd/coul/slater/long command"
url: https://docs.lammps.org/pair_dpd_coul_slater_long.html
---

# pair_style dpd/coul/slater/long command

## Syntax

```
pair_style dpd/coul/slater/long T cutoff_DPD seed lambda cutoff_coul
```

## Description

Added in version 27June2024.

Style dpd/coul/slater/long computes a force field for dissipative
particle dynamics (DPD) following the exposition in (Groot).  It also allows for the use of charged particles in the
model by adding a long-range Coulombic term to the DPD interactions.
The short-range portion of the Coulombics is calculated by this pair
style.  The long-range Coulombics are computed by use of the
kspace_style command, e.g. using the Ewald or
PPPM styles.

Coulombic forces in mesoscopic models such as DPD employ potentials
without explicit excluded-volume interactions.  The goal is to prevent
artificial ionic pair formation by including a charge distribution in
the Coulomb potential, following the formulation in (Melchor1).

Note
This pair style is effectively the combination of the
pair_style dpd and pair_style
coul/slater/long commands, but should be more
efficient (especially on GPUs) than using pair_style
hybrid/overlay dpd coul/slater/long. That is
particularly true for the GPU package version of the pair style since
this version is compatible with computing neighbor lists on the GPU
instead of the CPU as is required for hybrid styles.

In the charged DPD model, the force on bead I due to bead J is given
as a sum of 4 terms:

\[\begin{split}\vec{f}  = & (F^C + F^D + F^R + F^E) \hat{r_{ij}} \\
F^C      = & A w(r) \qquad \qquad \qquad \qquad \qquad r < r_{DPD} \\
F^D      = & - \gamma w^2(r) (\hat{r_{ij}} \bullet \vec{v}_{ij}) \qquad \qquad r < r_{DPD} \\
F^R      = & \sigma w(r) \alpha (\Delta t)^{-1/2} \qquad \qquad \qquad r < r_{DPD} \\
w(r)     = & 1 - \frac{r}{r_{DPD}} \\
F^E      = & \frac{C q_iq_j}{\epsilon r^2} \left( 1- exp\left( \frac{2r_{ij}}{\lambda} \right) \left( 1 + \frac{2r_{ij}}{\lambda} \left( 1 + \frac{r_{ij}}{\lambda} \right)\right) \right)\end{split}\]

where \(F^C\) is a conservative force, \(F^D\) is a
dissipative force, \(F^R\) is a random force, and \(F^E\) is
an electrostatic force.  \(\hat{r_{ij}}\) is a unit vector in the
direction \(r_i - r_j\), \(\vec{v}_{ij}\) is the vector
difference in velocities of the two atoms \(\vec{v}_i -
\vec{v}_j\), \(\alpha\) is a Gaussian random number with zero mean
and unit variance, dt is the timestep size, and \(w(r)\) is a
weighting factor that varies between 0 and 1.

\(\sigma\) is set equal to \(\sqrt{2 k_B T \gamma}\), where
\(k_B\) is the Boltzmann constant and T is the temperature
parameter in the pair_style command.

\(r_{DPD}\) is the pairwise cutoff for the first 3 DPD terms in
the formula as specified by cutoff_DPD.  For the \(F^E\) term,
pairwise interactions within the specified cutoff_coul distance are
computed directly; interactions beyond that distance are computed in
reciprocal space.  C is the same Coulomb conversion factor used in
the Coulombic formulas described on the pair_coul
doc page.

The following parameters must be defined for each pair of atoms types
via the pair_coeff command as in the examples
above, or in the data file or restart files read by the
read_data or read_restart
commands:

The is_charged parameter is optional and can be specified as yes or
no.  Yes should be used for interactions between two types of
charged particles.  No is the default and should be used for
interactions between two types of particles when one or both are
uncharged.

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
pair_style dpd/coul/slater/long 1.0 2.5 34387 0.25 3.0

pair_coeff 1 1 78.0 4.5          # not charged by default
pair_coeff 2 2 78.0 4.5 yes
```

## Restrictions

Restrictions 
This style is part of the DPD-BASIC package.  It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.
The default frequency for rebuilding neighbor lists is every 10 steps
(see the neigh_modify command). This may be too
infrequent since particles move rapidly and can overlap by large
amounts.  If this setting yields a non-zero number of  dangerous 
reneighborings (printed at the end of a simulation), you should
experiment with forcing reneighboring more often and see if system
energies/trajectories change.
This pair style requires use of the comm_modify vel yes command so that velocities are stored by ghost atoms.
This pair style also requires use of a long-range solvers from the
KSPACE package.
This pair style will not restart exactly when using the
read_restart command, though they should provide
statistically similar results.  This is because the forces they compute
depend on atom velocities.  See the read_restart
command for more details.

## Related Commands

- [pair_style dpd](pair_dpd.html)
- [pair_style coul/slater/long](pair_coul_slater.html)

