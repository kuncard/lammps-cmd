---
id: fix_numdiff_virial
title: "fix numdiff/virial command"
url: https://docs.lammps.org/fix_numdiff_virial.html
---

# fix numdiff/virial command

## Syntax

```
fix ID group-ID numdiff/virial Nevery delta
```

## Description

Added in version 17Feb2022.

Calculate the virial stress tensor through a finite difference calculation of
energy versus strain.  These values can be compared to the analytic virial
tensor computed by pair styles, bond styles, etc.  This can be useful for
debugging or other purposes. The specified group must be  all .

This fix applies linear strain fields of magnitude delta to all the
atoms relative to a point at the center of the box.  The
strain fields are in six different directions, corresponding to the
six Cartesian components of the stress tensor defined by LAMMPS.
For each direction it applies the strain field in both the positive
and negative senses, and the new energy of the entire system
is calculated after each. The difference in these two energies
divided by two times delta, approximates the corresponding
component of the virial stress tensor, after applying
a suitable unit conversion.

Note
It is important to choose a suitable value for delta, the magnitude of
strains that are used to generate finite difference
approximations to the exact virial stress.  For typical systems, a value in
the range of 1 part in 1e5 to 1e6 will be sufficient.
However, the best value will depend on a multitude of factors
including the stiffness of the interatomic potential, the thermodynamic
state of the material being probed, and so on. The only way to be sure
that you have made a good choice is to do a sensitivity study on a
representative atomic configuration, sweeping over a wide range of
values of delta.  If delta is too small, the output values will vary
erratically due to truncation effects. If delta is increased beyond a
certain point, the output values will start to vary smoothly with
delta, due to growing contributions from higher order derivatives. In
between these two limits, the numerical virial values should be largely
independent of delta.

The Nevery argument specifies on what timesteps the force will
be used calculated by finite difference.

The delta argument specifies the size of the displacement each
atom will undergo.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 1 all numdiff/stress 10 1e-6
```

## Restrictions

Restrictions 
This fix is part of the EXTRA-FIX package.  It is only enabled if LAMMPS
was built with that package.  See the Build package page for more info.

## Related Commands

- [fix numdiff](fix_numdiff.html)
- [compute pressure](compute_pressure.html)

