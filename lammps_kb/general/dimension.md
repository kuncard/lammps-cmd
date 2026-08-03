---
id: dimension
title: "dimension command"
url: https://docs.lammps.org/dimension.html
---

# dimension command

## Syntax

```
dimension N
```

## Description

Set the dimensionality of the simulation.  By default LAMMPS runs 3d
simulations.  To run a 2d simulation, this command should be used
prior to setting up a simulation box via the
create_box or read_data commands.
Restart files also store this setting.

See the discussion on the Howto 2d page for
additional instructions on how to run 2d simulations.

Note
Some models in LAMMPS treat particles as finite-size spheres or
ellipsoids, as opposed to point particles.  In 2d, the particles will
still be spheres or ellipsoids, not circular disks or ellipses,
meaning their moment of inertia will be the same as in 3d.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
dimension 2
```

## Restrictions

Restrictions 
This command must be used before the simulation box is defined by a
read_data or create_box command.

## Related Commands

- [fix enforce2d](fix_enforce2d.html)

