---
id: angle_lepton
title: "angle_style lepton command"
url: https://docs.lammps.org/angle_lepton.html
---

# angle_style lepton command

## Syntax

```
angle_style style args
args = auto_offset or no_offset
  auto_offset = offset the potential energy so that the value at theta0 is 0.0 (default)
  no_offset = do not offset the potential energy
```

## Description

Added in version 8Feb2023.

Angle style lepton computes angular interactions between three atoms
with a custom potential function.  The potential function must be
provided as an expression string using  theta  as the angle variable
relative to the reference angle \(\theta_0\) which is provided as an
angle coefficient.  For example  200.0*theta^2  represents a
harmonic angle potential with a force constant
K of 200.0 energy units:

\[U_{angle,i} = K (\theta_i - \theta_0)^2 = K \theta^2 \qquad \theta = \theta_i - \theta_0\]

Changed in version 7Feb2024.

By default the potential energy U is shifted so that the value U is 0.0
for $theta = theta_0$.  This is equivalent to using the optional keyword
auto_offset.  When using the keyword no_offset instead, the
potential energy is not shifted.

The Lepton library, that the
lepton angle style interfaces with, evaluates this expression string
at run time to compute the pairwise energy.  It also creates an
analytical representation of the first derivative of this expression
with respect to  theta  and then uses that to compute the force between
the angle atoms as defined by the topology data.

The following coefficients must be defined for each angle type via the
angle_coeff command as in the example above, or in
the data file or restart files read by the read_data
or read_restart commands:

The Lepton expression must be either enclosed in quotes or must not
contain any whitespace so that LAMMPS recognizes it as a single keyword.
More on valid Lepton expressions below.  The \(\theta_0\)
coefficient is the  equilibrium angle .  It is entered in degrees, but
internally converted to radians.  Thus the expression must assume
 theta  is in radians.  The potential energy function in the Lepton
expression is shifted in such a way, that the potential energy is 0 for
a angle \(\theta_i == \theta_0\).

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
angle_style lepton
angle_style lepton no_offset

angle_coeff  1  120.0  "k*theta^2; k=250.0"
angle_coeff  2   90.0  "k2*theta^2 + k3*theta^3 + k4*theta^4; k2=300.0; k3=-100.0; k4=50.0"
angle_coeff  3  109.47 "k*theta^2; k=350.0"
```

## Restrictions

Restrictions 
This angle style is part of the LEPTON package and only enabled if LAMMPS
was built with this package.  See the Build package page for more info.

## Related Commands

- [angle_coeff](angle_coeff.html)
- [angle_style table](angle_table.html)
- [bond_style lepton](bond_lepton.html)

