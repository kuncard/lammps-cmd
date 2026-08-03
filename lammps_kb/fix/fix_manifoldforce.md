---
id: fix_manifoldforce
title: "fix manifoldforce command"
url: https://docs.lammps.org/fix_manifoldforce.html
---

# fix manifoldforce command

## Syntax

```
fix ID group-ID manifoldforce manifold manifold-args ...
```

## Description

This fix subtracts each time step from the force the component along
the normal of the specified manifold.  This can be
used in combination with minimize to remove overlap
between particles while keeping them (roughly) constrained to the
given manifold, e.g. to set up a run with fix nve/manifold/rattle.  I have found that
only hftn and quickmin with a very small time step perform
adequately though.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix constrain all manifoldforce sphere 5.0
```

## Restrictions

Restrictions 
This fix is part of the MANIFOLD package. It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.
Only use this with min_style hftn or min_style quickmin. If not,
the constraints will not be satisfied very well at all. A warning is
generated if the min_style is incompatible but no error.

## Related Commands

- [fix nve/manifold/rattle](fix_nve_manifold_rattle.html)
- [fix nvt/manifold/rattle](fix_nvt_manifold_rattle.html)

