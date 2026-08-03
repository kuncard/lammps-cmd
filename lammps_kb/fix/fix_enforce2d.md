---
id: fix_enforce2d
title: "fix enforce2d command"
url: https://docs.lammps.org/fix_enforce2d.html
---

# fix enforce2d command

## Syntax

```
fix ID group-ID enforce2d
```

## Description

Zero out the z-dimension velocity and force on each atom in the group.
This is useful when running a 2d simulation to ensure that atoms do
not move from their initial z coordinate.

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
fix 5 all enforce2d
```

## Restrictions

Restrictions 
none

## Related Commands

Related commands 
none

