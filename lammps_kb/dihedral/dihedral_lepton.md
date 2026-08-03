---
id: dihedral_lepton
title: "dihedral_style lepton command"
url: https://docs.lammps.org/dihedral_lepton.html
---

# dihedral_style lepton command

## Syntax

```
dihedral_style lepton
```

## Description

Added in version 8Feb2023.

Dihedral style lepton computes dihedral interactions between four
atoms forming a dihedral angle with a custom potential function.  The
potential function must be provided as an expression string using  phi 
as the dihedral angle variable.  For example  200.0*(phi-120.0)^2 
represents a quadratic dihedral potential
around a 120 degree dihedral angle with a force constant K of 200.0
energy units:

\[U_{dihedral,i} = K (\phi_i - \phi_0)^2\]

The Lepton library, that the
lepton dihedral style interfaces with, evaluates this expression
string at run time to compute the pairwise energy.  It also creates an
analytical representation of the first derivative of this expression
with respect to  phi  and then uses that to compute the force between
the dihedral atoms as defined by the topology data.

The potential function expression for each dihedral type is provided via the
dihedral_coeff command as in the example above, or in
the data file or restart files read by the read_data
or read_restart commands.  The expression is in energy units.

The Lepton expression must be either enclosed in quotes or must not
contain any whitespace so that LAMMPS recognizes it as a single keyword.
More on valid Lepton expressions below.  Dihedral angles are internally
computed in radians and thus the expression must assume  phi  is in
radians.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
dihedral_style lepton

dihedral_coeff  1 "k*(1 + d*cos(n*phi)); k=75.0; d=1; n=2"
dihedral_coeff  2 "45*(1-cos(4*phi))"
dihedral_coeff  2 "k2*cos(phi) + k3*cos(phi)^2; k2=100.0"
dihedral_coeff  3 "k*(phi-phi0)^2; k=85.0; phi0=120.0"
```

## Restrictions

Restrictions 
This dihedral style is part of the LEPTON package and only enabled if LAMMPS
was built with this package.  See the Build package page for more info.

## Related Commands

- [dihedral_coeff](dihedral_coeff.html)
- [dihedral_style table](dihedral_table.html)
- [bond_style lepton](bond_lepton.html)
- [angle_style lepton](angle_lepton.html)

