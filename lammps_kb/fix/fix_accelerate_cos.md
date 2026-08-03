---
id: fix_accelerate_cos
title: "fix accelerate/cos command"
url: https://docs.lammps.org/fix_accelerate_cos.html
---

# fix accelerate/cos command

## Syntax

```
fix ID group-ID accelerate value
```

## Description

Give each atom a acceleration in x-direction based on its z coordinate.
The acceleration is a periodic function along the z-direction:

\[a_{x}(z) = A \cos \left(\frac{2 \pi z}{l_{z}}\right)\]

where \(A\) is the acceleration amplitude, \(l_z\) is the
\(z\)-length of the simulation box.
At steady state, the acceleration generates a velocity profile:

\[v_{x}(z) = V \cos \left(\frac{2 \pi z}{l_{z}}\right)\]

The generated velocity amplitude \(V\) is related to the
shear viscosity \(\eta\) by:

\[V = \frac{A \rho}{\eta}\left(\frac{l_{z}}{2 \pi}\right)^{2}\]

and it can be obtained from ensemble average of the velocity profile:

\[V = \frac{\sum\limits_i 2 m_{i} v_{i, x} \cos \left(\frac{2 \pi z_i}{l_{z}}\right)}{\sum\limits_i m_{i}},\]

where \(m_i\), \(v_{i,x}\), and \(z_i\) are the mass,
\(x\)-component velocity, and \(z\)-coordinate of a particle,
respectively.

The velocity amplitude \(V\) can be calculated with compute
viscosity/cos, which enables viscosity
calculation with periodic perturbation method, as described by
Hess.  Because the applied acceleration drives the system
away from equilibration, the calculated shear viscosity is lower than
the intrinsic viscosity due to the shear-thinning effect.  Extrapolation
to zero acceleration should generally be performed to predict the
zero-shear viscosity.  As the shear stress decreases, the
signal-to-noise ratio decreases rapidly, and the simulation time must be
extended accordingly to get converged results.

In order to get meaningful results, the group ID of this fix should be all.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 1 all accelerate/cos 2.0e-7
```

## Restrictions

Restrictions 
This fix is part of the MISC package.  It is only enabled if LAMMPS was
built with that package.  See the Build package
page for more info.
Since this fix depends on the \(z\)-coordinate of atoms, it cannot be used
in 2d simulations.

## Related Commands

- [compute viscosity/cos](compute_viscosity_cos.html)

