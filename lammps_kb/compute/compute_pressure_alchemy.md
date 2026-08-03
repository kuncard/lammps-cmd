---
id: compute_pressure_alchemy
title: "compute pressure/alchemy command"
url: https://docs.lammps.org/compute_pressure_alchemy.html
---

# compute pressure/alchemy command

## Syntax

```
compute ID group-ID pressure/alchemy fix-ID
```

## Description

Added in version 28Mar2023.

Define a compute style that makes the  mixed  system pressure available
for a system that uses the fix alchemy command to
transform one topology to another.  This can be used in combination with
either thermo_modify press or fix_modify
press to output and access a pressure consistent with the
simulated combined two topology system.

The actual pressure is determined with compute pressure commands that are internally used by fix
alchemy for each topology individually and then combined.
This command just extracts the information from the fix.

The examples/PACKAGES/alchemy folder contains an example input for this command.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix trans all alchemy
compute mixed all pressure/alchemy trans
thermo_modify press mixed
```

## Restrictions

Restrictions 
This compute is part of the REPLICA package.  It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.

## Related Commands

- [fix alchemy](fix_alchemy.html)
- [compute pressure](compute_pressure.html)
- [thermo_modify](thermo_modify.html)
- [fix_modify](fix_modify.html)

