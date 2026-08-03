---
id: fix_shardlow
title: "fix shardlow command"
url: https://docs.lammps.org/fix_shardlow.html
---

# fix shardlow command

## Syntax

```
fix ID group-ID shardlow
```

## Description

Specifies that the Shardlow splitting algorithm (SSA) is to be used to
integrate the DPD equations of motion.  The SSA splits the integration
into a stochastic and deterministic integration step.  The fix
shardlow performs the stochastic integration step and must be used in
conjunction with a deterministic integrator (e.g. fix nve or fix nph).  The stochastic integration of
the dissipative and random forces is performed prior to the
deterministic integration of the conservative force. Further details
regarding the method are provided in (Lisal) and
(Larentzos1).

The fix shardlow must be used with the pair_style dpd/fdt or pair_style dpd/fdt/energy command
to properly initialize the fluctuation-dissipation theorem parameter(s)
sigma (and kappa, if necessary).

Note that numerous variants of DPD can be specified by choosing an
appropriate combination of the integrator and pair_style dpd/fdt command.  DPD under isothermal conditions can be specified
by using fix shardlow, fix nve and pair_style dpd/fdt.  DPD
under isoenergetic conditions can be specified by using fix shardlow,
fix nve and pair_style dpd/fdt/energy.  DPD under isobaric
conditions can be specified by using fix shardlow, fix nph and
pair_style dpd/fdt.  DPD under isoenthalpic conditions can be
specified by using fix shardlow, fix nph and pair_style
dpd/fdt/energy.  Examples of each DPD variant are provided in the
examples/PACKAGES/dpd-react directory.

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
fix 1 all shardlow
```

## Restrictions

Restrictions 
This command is part of the DPD-REACT package.  It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.
This fix is currently limited to orthogonal simulation cell
geometries.
This fix must be used with an additional fix that specifies time
integration, e.g. fix nve or fix nph.
The Shardlow splitting algorithm requires the sizes of the subdomain
lengths to be larger than twice the cutoff+skin.  Generally, the
domain decomposition is dependent on the number of processors
requested.

## Related Commands

- [pair_style dpd/fdt](pair_dpd_fdt.html)
- [fix eos/cv](fix_eos_cv.html)

