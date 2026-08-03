---
id: fix_nve_spin
title: "fix nve/spin command"
url: https://docs.lammps.org/fix_nve_spin.html
---

# fix nve/spin command

## Syntax

```
fix ID group-ID nve/spin keyword values
lattice value = moving or frozen
  moving = integrate both spin and atomic degress of freedom
  frozen = integrate spins on a fixed lattice
```

## Description

Perform a symplectic integration for the spin or spin-lattice system.

The lattice keyword defines if the spins are integrated on a lattice
of fixed atoms (lattice = frozen), or if atoms are moving
(lattice = moving).
The first case corresponds to a spin dynamics calculation, and
the second to a spin-lattice calculation.
By default a spin-lattice integration is performed (lattice = moving).

The nve/spin fix applies a Suzuki-Trotter decomposition to
the equations of motion of the spin lattice system, following the scheme:

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 3 all nve/spin lattice moving
fix 1 all nve/spin lattice frozen
```

## Restrictions

Restrictions 
This fix style can only be used if LAMMPS was built with the SPIN
package.  See the Build package page for more
info.
To use the spin algorithm, it is necessary to define a map with
the atom_modify command. Typically, by adding the command:
atom_modify map array

before you create the simulation box. Note that the keyword  hash 
instead of  array  is also valid.

## Related Commands

- [atom_style spin](atom_style.html)
- [fix nve](fix_nve.html)

