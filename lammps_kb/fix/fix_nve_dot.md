---
id: fix_nve_dot
title: "fix nve/dot command"
url: https://docs.lammps.org/fix_nve_dot.html
---

# fix nve/dot command

## Syntax

```
fix ID group-ID nve/dot
```

## Description

Apply a rigid-body integrator as described in (Davidchack)
to a group of atoms, but without Langevin dynamics.
This command performs Molecular dynamics (MD)
via a velocity-Verlet algorithm and an evolution operator that rotates
the quaternion degrees of freedom, similar to the scheme outlined in (Miller).

This command is the equivalent of the fix nve/dotc/langevin
without damping and noise and can be used to determine the stability range
in a NVE ensemble prior to using the Langevin-type DOTC-integrator
(see also fix nve/dotc/langevin).
The command is equivalent to the fix nve.
The particles are always considered to have a finite size.

An example input file can be found in /examples/PACKAGES/cgdna/examples/duplex1/.
Further details of the implementation and stability of the integrator are contained in (Henrich).
The preprint version of the article can be found here.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 1 all nve/dot
```

## Restrictions

Restrictions 
These pair styles can only be used if LAMMPS was built with the
CG-DNA package and the MOLECULE and ASPHERE package.
See the Build package page for more info.

## Related Commands

- [fix nve/dotc/langevin](fix_nve_dotc_langevin.html)
- [fix nve](fix_nve.html)

