---
id: fix_dpd_energy
title: "fix dpd/energy command"
url: https://docs.lammps.org/fix_dpd_energy.html
---

# fix dpd/energy command

## Syntax

```
fix ID group-ID dpd/energy
```

## Description

Perform constant energy dissipative particle dynamics (DPD-E)
integration.  This fix updates the internal energies for particles in
the group at each timestep.  It must be used in conjunction with a
deterministic integrator (e.g. fix nve) that updates
the particle positions and velocities.

For fix dpd/energy, the particle internal temperature is related to
the particle internal energy through a mesoparticle equation of state.
An additional fix must be specified that defines the equation of state
for each particle, e.g. fix eos/cv.

This fix must be used with the pair_style dpd/fdt/energy command.

Note that numerous variants of DPD can be specified by choosing an
appropriate combination of the integrator and pair_style dpd/fdt/energy command.  DPD under isoenergetic conditions
can be specified by using fix dpd/energy, fix nve and pair_style
dpd/fdt/energy.  DPD under isoenthalpic conditions can
be specified by using fix dpd/energy, fix nph and pair_style
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
fix 1 all dpd/energy
```

## Restrictions

Restrictions 
This command is part of the DPD-REACT package.  It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.
This fix must be used with an additional fix that specifies time
integration, e.g. fix nve.
The fix dpd/energy requires the dpd atom_style
to be used in order to properly account for the particle internal
energies and temperature.
The fix dpd/energy must be used with an additional fix that specifies the
mesoparticle equation of state for each particle.

## Related Commands

- [fix nve](fix_nve.html)
- [fix eos/cv](fix_eos_cv.html)

