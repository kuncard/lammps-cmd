---
id: timestep
title: "timestep command"
url: https://docs.lammps.org/timestep.html
---

# timestep command

## Syntax

```
timestep dt
```

## Description

Set the timestep size for subsequent molecular dynamics simulations.
See the units command for the time units associated with
each choice of units that LAMMPS supports.

The default value for the timestep size also depends on the choice of
units for the simulation; see the default values below.

When the run style is respa, dt is the timestep for
the outer loop (largest) timestep.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
timestep 2.0
timestep 0.003
```

## Restrictions

Restrictions 
none

## Related Commands

- [fix dt/reset](fix_dt_reset.html)
- [run](run.html)
- [run_style](run_style.html)
- [units](units.html)

