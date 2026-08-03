---
id: fix_ilves
title: "fix ilves command"
url: https://docs.lammps.org/fix_ilves.html
---

# fix ilves command

## Syntax

```
fix ID group-ID ilves tol iter N selectors ... [keyword args ...]
b values = one or more bond types (may use type labels)
a values = one or more angle types (may use type labels)
t values = one or more atom types (may use type labels)
m values = one or more atom masses
mode value = converge or fixed
  converge = iterate until the tolerance is met (default)
  fixed = always perform iter Newton iterations
linearangle values = style threshold
  style = error or skip or restrain
    error = stop if a selected angle type is near-linear (default)
    skip = do not constrain near-linear angle types
    restrain = replace the near-linear A-C constraint with a stiff harmonic restraint
  threshold = equilibrium angle (in degrees) at or above which an angle type is near-linear
kbond value = dynamics force constant of the harmonic-bond substitute used
  for the linearangle restrain mode (the energy-minimization substitute is a
  fixed factor stiffer); in the active unit system
store value = yes or no
  yes exposes the per-atom constraint forces via a per-atom array
```

## Description

Added in version 4Jul2026.

Apply bond-length and angle constraints using the ILVES algorithm of
(Lopez-Villellas).  ILVES enforces holonomic
distance constraints with Newton s method on a sparse system of nonlinear
equations.  Unlike fix shake, ILVES handles arbitrarily
large connected constraint clusters   for example all the C-C backbone bonds
of a long polymer or protein chain   in a single solve.

This command is a LAMMPS port of the reference ILVES implementation that the
algorithm authors integrated into GROMACS; the constraint solver itself
(the parallel Schur-complement sparse direct solver and the constraint
topology handling) is reused largely unchanged, while the interface to the
LAMMPS data structures and the time integration follow fix shake.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 1 all ilves 1.0e-6 25 0 b 4 6 8 10
fix 2 wat ilves 1.0e-8 25 1000 b 18 a 31
fix 3 all ilves 1.0e-6 25 0 b 1 mode fixed
fix 4 sol ilves 1.0e-8 25 0 t 1 m 1.008 store yes
fix 5 co2 ilves 1.0e-8 25 0 b 1 a 1 linearangle restrain 170 kbond 2000
```

## Restrictions

Restrictions 
This fix is part of the RIGID package.  It is only enabled if LAMMPS was
built with that package.  See the Build package
page for more info.
The molecular topology (bonds) must be defined; an atom_style such as full, molecular, or bond (or a hybrid atom
style including them) is required, and an atom map
must be enabled.
Only one fix ilves instance may be defined at a time.  fix ilves
and fix shake may be used at the same time, but the
sets of constrained atoms must not overlap.
fix ilves supports run_style respa.  As for
fix shake, the constraints are enforced at every
r-RESPA level using the level-dependent effective timestep.
All atoms of a constraint cluster must lie within the communication
cutoff of each other on every rank.  For small clusters (water, methyl,
hydrogen-only constraints) this is satisfied automatically; for clusters
that span large distances increase the cutoff with comm_modify
cutoff.  The fix stops with an error if a constraint
partner is not available locally.
fix ilves does not support dynamic topologies.  Fixes or commands
that add, remove, or change constrained bonds during a run (for example
fix bond/create, fix bond/break, or fix bond/react) must not
be applied to the constrained atoms.

## Related Commands

- [fix shake](fix_shake.html)
- [fix rattle](fix_shake.html)
- [fix restrain](fix_restrain.html)
- [fix rigid](fix_rigid.html)

