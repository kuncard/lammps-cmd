---
id: fix_efield_lepton
title: "fix efield/lepton command"
url: https://docs.lammps.org/fix_efield_lepton.html
---

# fix efield/lepton command

## Syntax

```
fix ID group-ID efield/lepton V ...
region value = region-ID
  region-ID = ID of region atoms must be in to have effect
step value = h
  h = step size for numerical differentiation (distance units)
```

## Description

Added in version 4Feb2025.

Add an electric potential \(V\) that applies to a group of charged atoms a force \(\vec{F} = q \vec{E}\),
and to dipoles a force \(\vec{F} = (\vec{p} \cdot \nabla) \vec{E}\) and torque \(\vec{T} = \vec{p} \times \vec{E}\),
where \(\vec{E} = - \nabla V\). The fix also evaluates the electrostatic energy (\(U_{q} = q V\) and \(U_{p} = - \vec{p} \cdot \vec{E}\))
due to this potential when the fix_modify energy yes command is specified (see below).

Note
This command should be used instead of fix efield if you want to impose a non-uniform electric field on a system with dipoles
since the latter does not include the dipole force term. If you only have charges or if the electric field gradient is negligible,
fix efield should be used since it is faster.

The Lepton library, that the efield/lepton fix style interfaces with, evaluates
the expression string at run time to compute the energy, forces, and torques. It creates an analytical representation
of \(V\) and \(\vec{E}\), while the gradient force is computed using a central difference scheme

\[\vec{F} = \frac{|\vec{p}|}{2h} \left[ \vec{E}(\vec{x} + h \hat{p}) - \vec{E}(\vec{x} - h \hat{p}) \right] .\]

The Lepton expression must be either enclosed in quotes or must not contain any whitespace so that LAMMPS
recognizes it as a single keyword. More on valid Lepton expressions below. The final Lepton expression must
be a function of only \(x, y, z\), which refer to the current unwrapped coordinates of the atoms to ensure continuity.
Special care must be taken when using this fix with periodic boundary conditions or box-changing commands.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix ex all efield/lepton "-E*x; E=1"
fix dexx all efield/lepton "-0.5*x^2" step 1
fix yukawa all efield/lepton "A*exp(-B*r)/r; r=abs(sqrt(x^2+y^2+z^2)); A=1; B=1" step 1e-6
fix infp all efield/lepton "-abs(x)" step 1

variable th equal 2*PI*ramp(0,1)
fix erot all efield/lepton "-(x*cos(v_th)+y*sin(v_th))"
```

## Restrictions

Restrictions 
Fix style efield/lepton is part of the LEPTON package. It is only enabled if LAMMPS was built with that package.
See the Build package page for more info.

## Related Commands

- [fix efield](fix_efield.html)

