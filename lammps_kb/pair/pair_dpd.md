---
id: pair_dpd
title: "pair_style dpd command"
url: https://docs.lammps.org/pair_dpd.html
---

# pair_style dpd command

## Syntax

```
pair_style dpd T cutoff seed
pair_style dpd/tstat Tstart Tstop cutoff seed
```

## Description

Style dpd computes a force field for dissipative particle dynamics
(DPD) following the exposition in (Groot).

Style dpd/tstat invokes a DPD thermostat on pairwise interactions,
which is equivalent to the non-conservative portion of the DPD force
field.  This pairwise thermostat can be used in conjunction with any
pair style, and instead of per-particle thermostats
like fix langevin or ensemble thermostats like
Nose Hoover as implemented by fix nvt.  To use
dpd/tstat as a thermostat for another pair style, use the
pair_style hybrid/overlay command to compute both
the desired pair interaction and the thermostat for each pair of
particles.

For style dpd, the force on atom I due to atom J is given as a sum
of 3 terms

\[\begin{split}\vec{f}  = & (F^C + F^D + F^R) \hat{r_{ij}} \qquad \qquad r < r_c \\
F^C      = & A w(r) \\
F^D      = & - \gamma w^2(r) (\hat{r_{ij}} \bullet \vec{v}_{ij}) \\
F^R      = & \sigma w(r) \alpha (\Delta t)^{-1/2} \\
w(r)     = & 1 - \frac{r}{r_c}\end{split}\]

where \(F^C\) is a conservative force, \(F^D\) is a dissipative
force, and \(F^R\) is a random force.  \(\hat{r_{ij}}\) is a
unit vector in the direction \(r_i - r_j\), \(\vec{v}_{ij}\) is
the vector difference in velocities of the two atoms \(\vec{v}_i -
\vec{v}_j\), \(\alpha\) is a Gaussian random number with zero mean
and unit variance, dt is the timestep size, and \(w(r)\) is a
weighting factor that varies between 0 and 1.  \(r_c\) is the
pairwise cutoff.  \(\sigma\) is set equal to \(\sqrt{2 k_B T
\gamma}\), where \(k_B\) is the Boltzmann constant and T is the
temperature parameter in the pair_style command.

For style dpd/tstat, the force on atom I due to atom J is the same as
the above equation, except that the conservative \(F^C\) term is
dropped.  Also, during the run, T is set each timestep to a ramped
value from Tstart to Tstop.

For style dpd, the pairwise energy associated with style dpd is only
due to the conservative force term \(F^C\), and is shifted to be
zero at the cutoff distance \(r_c\).  The pairwise virial is
calculated using all 3 terms.  For style dpd/tstat there is no
pairwise energy, but the last two terms of the formula make a
contribution to the virial.

For style dpd, the following coefficients must be defined for each
pair of atoms types via the pair_coeff command as in
the examples above, or in the data file or restart files read by the
read_data or read_restart
commands:

The cutoff coefficient is optional.  If not specified, the global DPD
cutoff is used.  Note that sigma is set equal to sqrt(2 T gamma),
where T is the temperature set by the pair_style
command so it does not need to be specified.

For style dpd/tstat, the coefficients defined for each pair of
atoms types via the pair_coeff command are:

The cutoff coefficient is optional.

Styles with a gpu suffix are implemented based on
the work of (Afshar) and (Phillips).

Note
If you are modeling DPD polymer chains, you may want to use the
pair_style srp command in conjunction with these pair
styles.  It is a soft segmental repulsive potential (SRP) that can
prevent DPD polymer chains from crossing each other.

Note
The virial calculation for pressure when using these pair styles
includes all the components of force listed above, including the
random force.  Since the random force depends on random numbers,
everything that changes the order of atoms in the neighbor list
(e.g. different number of MPI ranks or a different neighbor list
skin distance) will also change the sequence in which the random
numbers are applied and thus the individual forces and therefore
also the virial/pressure.

Note
For more consistent time integration and force computation you may
consider using fix mvv/dpd instead of fix
nve.

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
pair_style dpd 1.0 2.5 34387
pair_coeff * * 3.0 1.0
pair_coeff 1 1 3.0 1.0 1.0

pair_style hybrid/overlay lj/cut 2.5 dpd/tstat 1.0 1.0 2.5 34387
pair_coeff * * lj/cut 1.0 1.0
pair_coeff * * dpd/tstat 1.0
```

## Restrictions

Restrictions 
These styles are part of the DPD-BASIC package.  They are only enabled if
LAMMPS was built with that package.  See the Build package page for more info.
The default frequency for rebuilding neighbor lists is every 10 steps
(see the neigh_modify command). This may be too
infrequent for style dpd simulations since particles move rapidly and
can overlap by large amounts.  If this setting yields a non-zero number
of  dangerous  reneighborings (printed at the end of a simulation), you
should experiment with forcing reneighboring more often and see if
system energies/trajectories change.
These pair styles requires you to use the comm_modify vel yes command so that velocities are stored by ghost atoms.
These pair styles will not restart exactly when using the
read_restart command, though they should provide
statistically similar results.  This is because the forces they compute
depend on atom velocities.  See the read_restart
command for more details.

## Related Commands

- [pair_style dpd/ext](pair_dpd_ext.html)
- [pair_coeff](pair_coeff.html)
- [fix nvt](fix_nh.html)
- [fix langevin](fix_langevin.html)
- [pair_style srp](pair_srp.html)
- [fix mvv/dpd](fix_mvv_dpd.html)

