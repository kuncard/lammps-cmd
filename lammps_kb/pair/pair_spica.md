---
id: pair_spica
title: "pair_style lj/spica command"
url: https://docs.lammps.org/pair_spica.html
---

# pair_style lj/spica command

## Syntax

```
pair_style style args
lj/spica args = cutoff
  cutoff = global cutoff for Lennard Jones interactions (distance units)
lj/spica/coul/long args = cutoff (cutoff2)
  cutoff = global cutoff for LJ (and Coulombic if only 1 arg) (distance units)
  cutoff2 = global cutoff for Coulombic (optional) (distance units)
```

## Description

The lj/spica styles compute a 9/6, 12/4, 12/5, or 12/6 Lennard-Jones potential,
given by

\[\begin{split}E = & \frac{27}{4} \epsilon \left[ \left(\frac{\sigma}{r}\right)^{9} -
                      \left(\frac{\sigma}{r}\right)^6 \right]
                      \qquad r < r_c \\
E = & \frac{3\sqrt{3}}{2} \epsilon \left[ \left(\frac{\sigma}{r}\right)^{12} -
                      \left(\frac{\sigma}{r}\right)^4 \right]
                      \qquad r < r_c \\
E = & \frac{12}{7}\left(\frac{12}{5}\right)^{\left(\frac{5}{7}\right)} \epsilon
                      \left[ \left(\frac{\sigma}{r}\right)^{12} -
                      \left(\frac{\sigma}{r}\right)^5 \right]
                      \qquad r < r_c \\
E = &  4 \epsilon  \left[ \left(\frac{\sigma}{r}\right)^{12} -
                      \left(\frac{\sigma}{r}\right)^6 \right]
                      \qquad r < r_c\end{split}\]

as required for the SPICA (formerly called SDK) and the pSPICA Coarse-grained MD parameterization discussed in
(Shinoda), (DeVane), (Seo), and (Miyazaki).
\(r_c\) is the cutoff.
Summary information on these force fields can be found at https://www.spica-ff.org

Style lj/spica/coul/long computes the adds Coulombic interactions
with an additional damping factor applied so it can be used in
conjunction with the kspace_style command and
its ewald or pppm or pppm/cg option.  The Coulombic cutoff
specified for this style means that pairwise interactions within
this distance are computed directly; interactions outside that
distance are computed in reciprocal space.

The following coefficients must be defined for each pair of atoms
types via the pair_coeff command as in the examples
above, or in the data file or restart files read by the
read_data or read_restart
commands, or by mixing as described below:

Note that sigma is defined in the LJ formula as the zero-crossing
distance for the potential, not as the energy minimum. The prefactors
are chosen so that the potential minimum is at -epsilon.

The latter 2 coefficients are optional.  If not specified, the global
LJ and Coulombic cutoffs specified in the pair_style command are used.
If only one cutoff is specified, it is used as the cutoff for both LJ
and Coulombic interactions for this type pair.  If both coefficients
are specified, they are used as the LJ and Coulombic cutoffs for this
type pair.

For lj/spica/coul/long and lj/spica/coul/msm only the LJ cutoff can be
specified since a Coulombic cutoff cannot be specified for an
individual I,J type pair.  All type pairs use the same global
Coulombic cutoff specified in the pair_style command.

The original implementation of the above styles are
style lj/sdk, lj/sdk/coul/long, and lj/sdk/coul/msm,
and available for backward compatibility.

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
pair_style lj/spica 2.5
pair_coeff 1 1 lj12_6 1 1.1 2.8

pair_style lj/spica/coul/long 10.0
pair_style lj/spica/coul/long 10.0 12.0
pair_coeff 1 1 lj9_6 100.0 3.5 12.0

pair_style lj/spica/coul/msm 10.0
pair_style lj/spica/coul/msm 10.0 12.0
pair_coeff 1 1 lj9_6 100.0 3.5 12.0
```

## Restrictions

Restrictions 
All of the lj/spica pair styles are part of the CG-SPICA package.  The
lj/spica/coul/long style also requires the KSPACE package to be built
(which is enabled by default).  They are only enabled if LAMMPS was
built with that package.  See the Build package
doc page for more info.

## Related Commands

- [pair_coeff](pair_coeff.html)
- [angle_style spica](angle_spica.html)

