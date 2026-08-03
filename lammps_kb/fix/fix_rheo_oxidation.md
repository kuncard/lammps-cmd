---
id: fix_rheo_oxidation
title: "fix rheo/oxidation command"
url: https://docs.lammps.org/fix_rheo_oxidation.html
---

# fix rheo/oxidation command

## Syntax

```
fix ID group-ID rheo/oxidation cut btype rsurf
```

## Description

Added in version 29Aug2024.

This fix dynamically creates bonds on the surface of fluids to
represent physical processes such as oxidation. It is intended
for use with bond style bond rheo/shell.

Every timestep, particles check neighbors within a distance of cut.
This distance must be smaller than the kernel length defined in
fix rheo. Bonds of type btype are created between
a fluid particle and either a fluid or solid neighbor. The fluid particles
must also be on the fluid surface, or within a distance of rsurf from
the surface. This process is further described in
(Clemmer).

If used in conjunction with solid bodies, such as those generated
by the react option of fix rheo/thermal,
it is recommended to use a hybrid bond style
with different bond types for solid and oxide bonds.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 1 all rheo/oxidation 1.5 2 0.0
fix 1 all rheo/oxidation 1.0 1 2.0
```

## Restrictions

Restrictions 
This fix must be used with the bond style rheo/shell
and fix rheo with surface detection enabled.
This fix is part of the RHEO package.  It is only enabled if
LAMMPS was built with that package.  See the Build package
page for more info.

## Related Commands

- [fix rheo](fix_rheo.html)
- [bond rheo/shell](bond_rheo_shell.html)
- [compute rheo/property/atom](compute_rheo_property_atom.html)

