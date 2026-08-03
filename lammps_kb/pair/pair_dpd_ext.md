---
id: pair_dpd_ext
title: "pair_style dpd/ext command"
url: https://docs.lammps.org/pair_dpd_ext.html
---

# pair_style dpd/ext command

## Syntax

```
pair_style dpd/ext T cutoff seed
pair_style dpd/ext/tstat Tstart Tstop cutoff seed
```

## Description

The style dpd/ext computes an extended force field for dissipative
particle dynamics (DPD) following the exposition in (Groot), (Junghans).

Style dpd/ext/tstat invokes an extended DPD thermostat on pairwise
interactions, equivalent to the non-conservative portion of the extended
DPD force field. To use dpd/ext/tstat as a thermostat for another pair
style, use the pair_style hybrid/overlay command to
compute both the desired pair interaction and the thermostat for each
pair of particles.

For the style dpd/ext, the force on atom I due to atom J is given as
a sum of 3 terms

\[\begin{split}\mathbf{f}  = & f^C + f^D + f^R \qquad \qquad r < r_c \\
f^C      = & A_{ij} w(r) \hat{\mathbf{r}}_{ij} \\
f^D      = & - \gamma_{\parallel} w_{\parallel}^2(r) (\hat{\mathbf{r}}_{ij} \cdot \mathbf{v}_{ij}) \hat{\mathbf{r}}_{ij}  - \gamma_{\perp} w_{\perp}^2 (r) ( \mathbf{I} - \hat{\mathbf{r}}_{ij} \hat{\mathbf{r}}_{ij}^\mathrm{T} ) \mathbf{v}_{ij} \\
f^R      = & \sigma_{\parallel} w_{\parallel}(r) \frac{\alpha}{\sqrt{\Delta t}} \hat{\mathbf{r}}_{ij}  + \sigma_{\perp} w_{\perp} (r) ( \mathbf{I} - \hat{\mathbf{r}}_{ij} \hat{\mathbf{r}}_{ij}^\mathrm{T} ) \frac{\mathbf{\xi}_{ij}}{\sqrt{\Delta t}}\\
w(r)     = & 1 - r/r_c \\\end{split}\]

where \(\mathbf{f}^C\) is a conservative force, \(\mathbf{f}^D\)
is a dissipative force, and \(\mathbf{f}^R\) is a random
force. \(A_{ij}\) is the maximum repulsion between the two atoms,
\(\hat{\mathbf{r}}_{ij}\) is a unit vector in the direction
\(\mathbf{r}_i - \mathbf{r}_j\), \(\mathbf{v}_{ij} =
\mathbf{v}_i - \mathbf{v}_j\) is the vector difference in velocities of
the two atoms, \(\alpha\) and \(\mathbf{\xi}_{ij}\) are Gaussian
random numbers with zero mean and unit variance, \(\Delta t\) is the
timestep, \(w (r) = 1 - r / r_c\) is a weight function for the
conservative interactions that varies between 0 and 1, \(r_c\) is
the corresponding cutoff, \(w_{\alpha} ( r ) = ( 1 - r / \bar{r}_c
)^{s_{\alpha}}\), \(\alpha \equiv ( \parallel, \perp )\), are weight
functions with coefficients \(s_\alpha\) that vary between 0 and 1,
\(\bar{r}_c\) is the corresponding cutoff, \(\mathbf{I}\) is the
unit matrix, \(\sigma_{\alpha} = \sqrt{2 k_B T \gamma_{\alpha}}\),
where \(k_B\) is the Boltzmann constant and \(T\) is the
temperature in the pair_style command.

For the style dpd/ext/tstat, the force on atom I due to atom J is
the same as the above equation, except that the conservative
\(\mathbf{f}^C\) term is dropped. Also, during the run, T is set
each timestep to a ramped value from Tstart to Tstop.

For the style dpd/ext, the pairwise energy associated with style
dpd/ext is only due to the conservative force term
\(\mathbf{f}^C\), and is shifted to be zero at the cutoff distance
\(r_c\). The pairwise virial is calculated using all three
terms. There is no pairwise energy for style dpd/ext/tstat, but the
last two terms of the formula contribute the virial.

For the style dpd/ext/tstat, the force on atom I due to atom J is the
same as the above equation, except that the conservative
\(\mathbf{f}^C\) term is dropped.  Also, during the run, T is set
each timestep to a ramped value from Tstart to Tstop.

For the style dpd/ext, the pairwise energy associated with style
dpd/ext is only due to the conservative force term
\(\mathbf{f}^C\), and is shifted to be zero at the cutoff distance
\(r_c\). The pairwise virial is calculated using all three
terms. There is no pairwise energy for style dpd/ext/tstat, but the
last two terms of the formula contribute the virial.

For the style dpd/ext, the following coefficients must be defined for
each pair of atoms types via the pair_coeff command
as in the examples above:

The last coefficient is optional. If not specified, the global DPD
cutoff is used. Note that \(\sigma\) s are set equal to
\(\sqrt{2 k_B T \gamma}\), where \(T\) is the temperature set by
the pair_style command so it does not need to be
specified.

For the style dpd/ext/tstat, the coefficients defined for each pair of
atoms types via the pair_coeff command are:

The last coefficient is optional.

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

Mixing, shift, table, tail correction, restart, rRESPA info:

The style dpd/ext does not support mixing. Thus, coefficients for all
I,J pairs must be specified explicitly.

The pair styles do not support the pair_modify
shift option for the energy of the pair interaction. Note that as
discussed above, the energy due to the conservative \(\mathbf{f}^C\)
term is already shifted to be zero at the cutoff distance \(r_c\).

The pair_modify table option is not relevant for
the style dpd/ext.

The style dpd/ext does not support the pair_modify tail option for adding long-range tail corrections to
energy and pressure.

The pair styles can only be used via the pair keyword of the
run_style respa command. They do not support the
inner, middle, and outerkeywords.

The style dpd/ext/tstat can ramp its target temperature over multiple
runs, using the start and stop keywords of the run
command. See the run command for details of how to do this.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
pair_style dpd/ext 1.0 2.5 34387
pair_coeff 1 1 25.0 4.5 4.5 0.5 0.5 1.2
pair_coeff 1 2 40.0 4.5 4.5 0.5 0.5 1.2

pair_style hybrid/overlay lj/cut 2.5 dpd/ext/tstat 1.0 1.0 2.5 34387
pair_coeff * * lj/cut 1.0 1.0
pair_coeff * * 4.5 4.5 0.5 0.5 1.2
```

## Restrictions

Restrictions 
These styles are part of the DPD-BASIC package.  They are only enabled if
LAMMPS was built with that package.  See the Build package page for more info.
The default frequency for rebuilding neighbor lists is every 10 steps
(see the neigh_modify command). This may be too
infrequent for style dpd/ext simulations since particles move rapidly
and can overlap by large amounts. If this setting yields a non-zero
number of say{dangerous} reneighborings (printed at the end of a
simulation), you should experiment with forcing reneighboring more often
and see if system energies/trajectories change.
The pair styles require to use the comm_modify vel yes command so that velocities are stored by ghost atoms.
The pair styles will not restart exactly when using the
read_restart command, though they should provide
statistically similar results. This is because the forces they compute
depend on atom velocities. See the read_restart
command for more details.

## Related Commands

- [pair_style dpd](pair_dpd.html)
- [pair_coeff](pair_coeff.html)
- [fix nvt](fix_nh.html)
- [fix langevin](fix_langevin.html)
- [pair_style srp](pair_srp.html)
- [fix mvv/dpd](fix_mvv_dpd.html)

