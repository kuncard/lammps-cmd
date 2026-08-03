---
id: fix_nve
title: "fix nve command"
url: https://docs.lammps.org/fix_nve.html
---

# fix nve command

## Syntax

```
fix ID group-ID nve
```

## Description

Perform plain time integration to update position and velocity for
atoms in the group each timestep.  This creates a system trajectory
consistent with the microcanonical ensemble (NVE) provided there are
(full) periodic boundary conditions and no other  manipulations  of
the system (e.g. fixes that modify forces or velocities).

This fix invokes the velocity form of the Stoermer-Verlet time
integration algorithm (velocity-Verlet). Other time integration
options can be invoked using the run_style command.

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
fix 1 all nve
```

## Restrictions

Restrictions 
none

## Related Commands

- [fix nvt](fix_nh.html)
- [fix npt](fix_nh.html)
- [run_style](run_style.html)

