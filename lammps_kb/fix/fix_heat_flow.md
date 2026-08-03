---
id: fix_heat_flow
title: "fix heat/flow command"
url: https://docs.lammps.org/fix_heat_flow.html
---

# fix heat/flow command

## Syntax

```
fix ID group-ID heat/flow style values ...
style = constant or type
  constant = cp
    cp = value of specifc heat (energy/(mass * temperature) units)
  type = cp1 ... cpN
    cpN = value of specifc heat for type N (energy/(mass * temperature) units)
```

## Description

Perform plain time integration to update temperature for atoms in the
group each timestep. The specific heat of atoms can be defined using either
the constant or type keywords. For style constant, the specific heat
is a constant value cp for all atoms. For style type, N different values
of the specific heat are defined, one for each of the N types of atoms.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 1 all heat/flow constant 1.0
fix 1 all heat/flow type 1.0 0.5
```

## Restrictions

Restrictions 
This pair style is part of the GRANULAR package.  It is
only enabled if LAMMPS was built with that package.
See the Build package page for more info.
This fix requires that atoms store temperature and heat flow
as defined by the fix property/atom command.

## Related Commands

- [pair granular](pair_granular.html)
- [fix add/heat](fix_add_heat.html)
- [fix property/atom](fix_property_atom.html)

