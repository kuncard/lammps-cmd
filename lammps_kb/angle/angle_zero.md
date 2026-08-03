---
id: angle_zero
title: "angle_style zero command"
url: https://docs.lammps.org/angle_zero.html
---

# angle_style zero command

## Syntax

```
angle_style zero keyword
```

## Description

Using an angle style of zero means angle forces and energies are not
computed, but the geometry of angle triplets is still accessible to
other commands.

As an example, the compute angle/local
command can be used to compute the theta values for the list of
triplets of angle atoms listed in the data file read by the
read_data command.  If no angle style is defined,
this command cannot be used.

The optional nocoeff flag allows to read data files with AngleCoeff
section for any angle style. Similarly, any angle_coeff commands
will only be checked for the angle type number and the rest ignored.

Note that the angle_coeff command must be used for
all angle types. If specified, there can be only one value, which is
going to be used to assign an equilibrium angle, e.g. for use with
fix shake.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
angle_style zero
angle_style zero nocoeff
angle_coeff *
angle_coeff * 120.0
```

## Restrictions

Restrictions 
none

## Related Commands

- [angle_style none](angle_none.html)

