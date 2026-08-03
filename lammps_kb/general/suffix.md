---
id: suffix
title: "suffix command"
url: https://docs.lammps.org/suffix.html
---

# suffix command

## Syntax

```
suffix style args
```

## Description

This command allows you to use variants of various styles if they
exist.  In that respect it operates the same as the -suffix command-line switch.  It also has options to turn
off or back on any suffix setting made via the command-line.

The specified style can be gpu, intel, kk, omp, opt or
hybrid. These refer to optional packages that LAMMPS can be built
with, as described on the Build package doc page.
The  gpu  style corresponds to the GPU package, the  intel  style to
the INTEL package, the  kk  style to the KOKKOS package, the
 omp  style to the OPENMP package, and the  opt  style to the OPT
package.

These are the variants these packages provide:

As an example, all of the packages provide a pair_style lj/cut variant, with style names lj/cut/opt, lj/cut/omp,
lj/cut/gpu, lj/cut/intel, or lj/cut/kk.  A variant styles
can be specified explicitly in your input script, e.g. pair_style
lj/cut/gpu. If the suffix command is used with the appropriate style,
you do not need to modify your input script.  The specified suffix
(opt,omp,gpu,intel,kk) is automatically appended whenever your
input script command creates a new atom,
pair, bond,
angle, dihedral,
improper, kspace,
fix, compute, or run style.
If the variant version does not exist, the standard version is
created.

For  hybrid , two packages are specified. The first is used whenever
available. If a style with the first suffix is not available, the style
with the suffix for the second package will be used if available. For
example,  hybrid intel omp  will use styles from the INTEL package
as a first choice and styles from the OPENMP package as a second choice
if no INTEL variant is available.

If the specified style is off, then any previously specified suffix
is temporarily disabled, whether it was specified by a command-line
switch or a previous suffix command.  If the specified style is on,
a disabled suffix is turned back on.  The use of these 2 commands lets
your input script use a standard LAMMPS style (i.e. a non-accelerated
variant), which can be useful for testing or benchmarking purposes.
Of course this is also possible by not using any suffix commands, and
explicitly appending or not appending the suffix to the relevant
commands in your input script.

Note
The default run_style verlet is invoked prior to
reading the input script and is therefore not affected by a suffix command
in the input script. The KOKKOS package requires  run_style verlet/kk ,
so when using the KOKKOS package it is necessary to either use the command
line  -sf kk  command or add an explicit  run_style verlet  command to the
input script.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
suffix off
suffix on
suffix gpu
suffix intel
suffix hybrid intel omp
suffix kk
```

## Restrictions

Restrictions 
none

## Related Commands

- [-suffix command-line switch](Run_options.html)

