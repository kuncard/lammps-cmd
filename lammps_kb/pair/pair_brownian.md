---
id: pair_brownian
title: "pair_style brownian command"
url: https://docs.lammps.org/pair_brownian.html
---

# pair_style brownian command

## Syntax

```
pair_style style mu flaglog flagfld cutinner cutoff t_target seed flagHI flagVF
```

## Description

Styles brownian and brownian/poly compute Brownian forces and
torques on finite-size spherical particles.  The former requires
monodisperse spherical particles; the latter allows for polydisperse
spherical particles.

These pair styles are designed to be used with either the
pair_style lubricate or pair_style
lubricateU commands to provide thermostatting when
dissipative lubrication forces are acting.  Thus the parameters mu,
flaglog, flagfld, cutinner, and cutoff should be specified
consistent with the settings in the lubrication pair styles.  For
details, refer to either of the lubrication pair styles.

The t_target setting is used to specify the target temperature of
the system.  The random number seed is used to generate random
numbers for the thermostatting procedure.

The flagHI and flagVF settings are optional.  Neither should be
used, or both must be defined.

Changed in version 4Jul2026.

For brownian/poly the pairwise random Brownian force is now generated
once per pair from a deterministic random number stream (keyed on the
pair of atom IDs and the timestep) and applied equal and opposite to
both particles, so that linear momentum is conserved exactly and the
system is no longer heated spuriously.  In addition the near-field
resistance functions now use the symmetric Jeffrey & Onishi gap so the
force magnitude is independent of which particle is taken as the
reference, consistent with pair_style lubricate/poly.  Previously the random force on the two members of a
pair was drawn independently (violating Newton s third law) and the
resistance was evaluated with one particle s radius as the reference
length, both of which were incorrect for polydisperse systems.

The following coefficients must be defined for each pair of atoms
types via the pair_coeff command as in the examples
above, or in the data file or restart files read by the
read_data or read_restart
commands, or by mixing as described below:

The two coefficients are optional.  If neither is specified, the two
cutoffs specified in the pair_style command are used.  Otherwise both
must be specified.

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
pair_style brownian 1.5 1 1 2.01 2.5 2.0 5878567 # (assuming radius = 1)
pair_coeff 1 1 2.05 2.8
pair_coeff * *
```

## Restrictions

Restrictions 
These styles are part of the COLLOID package.  They are only enabled if
LAMMPS was built with that package.  See the Build package page for more info.
Only spherical monodisperse particles are allowed for pair_style
brownian.
Only spherical particles are allowed for pair_style brownian/poly.  The
volume fraction correction is not supported by pair_style brownian/poly.
These pair styles are only compatible with the following wall fixes:
fix wall/lj93, fix wall/lj126, fix wall/lj1043, fix wall/colloid,
fix wall/harmonic, fix wall/lepton, fix wall/morse, fix wall/table.

## Related Commands

- [pair_coeff](pair_coeff.html)
- [pair_style lubricate](pair_lubricate.html)
- [pair_style lubricateU](pair_lubricateU.html)

