---
id: fix_qeq_comb
title: "fix qeq/comb command"
url: https://docs.lammps.org/fix_qeq_comb.html
---

# fix qeq/comb command

## Syntax

```
fix ID group-ID qeq/comb Nevery precision keyword value ...
file value = filename
  filename = name of file to write QEQ equilibration info to
```

## Description

Perform charge equilibration (QeQ) in conjunction with the COMB
(Charge-Optimized Many-Body) potential as described in
(COMB_1) and (COMB_2).  It performs the charge
equilibration portion of the calculation using the so-called QEq
method, whereby the charge on each atom is adjusted to minimize the
energy of the system.  This fix can only be used with the COMB
potential; see the fix qeq/reaxff command for a QeQ
calculation that can be used with any potential.

Only charges on the atoms in the specified group are equilibrated.
The fix relies on the pair style (COMB in this case) to calculate the
per-atom electronegativity (effective force on the charges).  An
electronegativity equalization calculation (or QEq) is performed in an
iterative fashion, which in parallel requires communication at each
iteration for processors to exchange charge information about nearby
atoms with each other.  See Rappe_and_Goddard and
Rick_and_Stuart for details.

During a run, charge equilibration is performed every Nevery time
steps.  Charge equilibration is also always enforced on the first step
of each run.  The precision argument controls the tolerance for the
difference in electronegativity for all atoms during charge
equilibration.  Precision is a trade-off between the cost of
performing charge equilibration (more iterations) and accuracy.

If the file keyword is used, then information about each
equilibration calculation is written to the specified file.

Note
In order to solve the self-consistent equations for electronegativity
equalization, LAMMPS imposes the additional constraint that all the
charges in the fix group must add up to zero.  The initial charge
assignments should also satisfy this constraint.  LAMMPS will print a
warning if that is not the case.

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
fix 1 surface qeq/comb 10 0.0001
```

## Restrictions

Restrictions 
This fix command currently only supports pair style *comb*.

## Related Commands

- [pair_style comb](pair_comb.html)

