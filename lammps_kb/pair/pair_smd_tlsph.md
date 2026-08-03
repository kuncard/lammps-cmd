---
id: pair_smd_tlsph
title: "pair_style smd/tlsph command"
url: https://docs.lammps.org/pair_smd_tlsph.html
---

# pair_style smd/tlsph command

## Syntax

```
pair_style smd/tlsph args
```

## Description

The smd/tlsph style computes particle interactions according to
continuum mechanics constitutive laws and a Total-Lagrangian
Smooth-Particle Hydrodynamics algorithm.

This pair style is invoked with the following command:

pair_style smd/tlsph
pair_coeff i j *COMMON rho0 E nu Q1 Q2 hg Cp &
               *END

Here, i and j denote the LAMMPS particle types for which this
pair style is defined. Note that i and j must be equal, i.e., no
tlsph cross interactions between different particle types are
allowed.  In contrast to the usual LAMMPS pair coeff definitions,
which are given solely a number of floats and integers, the tlsph
pair coeff definition is organized using keywords. These keywords
mark the beginning of different sets of parameters for particle
properties, material constitutive models, and damage models. The pair
coeff line must be terminated with the *END keyword. The use the
line continuation operator & is recommended. A typical invocation of
the tlsph for a solid body would consist of an equation of state for
computing the pressure (the diagonal components of the stress tensor),
and a material model to compute shear stresses (the off-diagonal
components of the stress tensor). Damage and failure models can also
be added.

Please see the SMD user guide for a
complete listing of the possible keywords and material models.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
pair_style smd/tlsph
```

## Restrictions

Restrictions 
This fix is part of the MACHDYN package.  It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.

## Related Commands

- [pair_coeff](pair_coeff.html)

