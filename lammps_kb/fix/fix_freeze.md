---
id: fix_freeze
title: "fix freeze command"
url: https://docs.lammps.org/fix_freeze.html
---

# fix freeze command

## Syntax

```
fix ID group-ID freeze
```

## Description

Zero out the force and torque on a granular particle.  This is useful
for preventing certain particles from moving in a simulation.  The
granular pair styles also detect if this fix has been
defined and compute interactions between frozen and non-frozen
particles appropriately, as if the frozen particle has infinite mass.
A similar functionality for normal (point) particles can be obtained
using fix setforce.

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
fix 2 bottom freeze
```

## Restrictions

Restrictions 
This fix is part of the GRANULAR package.  It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.
There can only be a single freeze fix defined.  This is because other
the granular pair styles treat frozen particles
differently and need to be able to reference a single group to which
this fix is applied.

## Related Commands

- [atom_style sphere](atom_style.html)
- [fix setforce](fix_setforce.html)

