---
id: fix_numdiff
title: "fix numdiff command"
url: https://docs.lammps.org/fix_numdiff.html
---

# fix numdiff command

## Syntax

```
fix ID group-ID numdiff Nevery delta
```

## Description

Calculate forces through finite difference calculations of energy
versus position.  These forces can be compared to analytic forces
computed by pair styles, bond styles, etc.  This can be useful for
debugging or other purposes.

The group specified with the command means only atoms within the group
have their averages computed.  Results are set to 0.0 for atoms not in
the group.

This fix performs a loop over all atoms in the group.  For each atom
and each component of force it adds delta to the position, and
computes the new energy of the entire system.  It then subtracts
delta from the original position and again computes the new energy
of the system.  It then restores the original position.  That
component of force is calculated as the difference in energy divided
by two times delta.

Note
It is important to choose a suitable value for delta, the magnitude of
atom displacements that are used to generate finite difference
approximations to the exact forces.  For typical systems, a value in
the range of 1 part in 1e4 to 1e5 of the typical separation distance
between atoms in the liquid or solid state will be sufficient.
However, the best value will depend on a multitude of factors
including the stiffness of the interatomic potential, the thermodynamic
state of the material being probed, and so on. The only way to be sure
that you have made a good choice is to do a sensitivity study on a
representative atomic configuration, sweeping over a wide range of
values of delta.  If delta is too small, the output forces will vary
erratically due to truncation effects. If delta is increased beyond a
certain point, the output forces will start to vary smoothly with
delta, due to growing contributions from higher order derivatives. In
between these two limits, the numerical force values should be largely
independent of delta.

Note
The cost of each energy evaluation is essentially the cost of an MD
timestep.  Thus invoking this fix once for a 3d system has a cost
of 6N timesteps, where N is the total number of atoms in the system.
So this fix can be very expensive to use for large systems.
One expedient alternative is to define the fix for a group containing
only a few atoms.

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
fix 1 all numdiff 10 1e-6
fix 1 movegroup numdiff 100 0.01
```

## Restrictions

Restrictions 
This fix is part of the EXTRA-FIX package.  It is only enabled if LAMMPS
was built with that package.  See the Build package page for more info.

## Related Commands

- [dynamical_matrix](dynamical_matrix.html)
- [fix numdiff/virial](fix_numdiff_virial.html)

