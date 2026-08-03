---
id: fix_viscous_nonlinear
title: "fix viscous/nonlinear command"
url: https://docs.lammps.org/fix_viscous_nonlinear.html
---

# fix viscous/nonlinear command

## Syntax

```
fix ID group-ID viscous/nonlinear rho_fluid mu_fluid keyword values ...
keyword = velocity
  velocity values = Vx Vy Vz
    Vx,Vy,Vz = components of the (uniform) fluid velocity (velocity units)
```

## Description

Added in version 4Jul2026.

Add a nonlinear (Reynolds-number dependent) drag force to each
finite-size spherical particle in the group, modeling the interaction
with a uniform background fluid (e.g. an upward gas stream).  Unlike
fix viscous, which applies a drag force strictly
proportional to the particle velocity (Stokes drag), this fix uses the
standard drag-coefficient relation with the Schiller-Naumann
correlation, which is accurate over a much wider range of particle
Reynolds numbers.

The drag force on particle i is

\[\vec{F}_i = -\frac{1}{2}\, C_d\, \rho_f\, \pi r_i^2\, |\vec{v}_{rel}|\, \vec{v}_{rel}\]

where \(r_i\) is the particle radius, \(\rho_f\) is the fluid
mass density, \(\vec{v}_{rel} = \vec{v}_i - \vec{v}_f\) is the
particle velocity relative to the fluid, and the drag coefficient
\(C_d\) follows the Schiller-Naumann correlation

\[C_d = \frac{24}{Re}\left(1 + 0.15\, Re^{0.687}\right), \qquad
Re = \frac{\rho_f\, |\vec{v}_{rel}|\, (2 r_i)}{\mu_f}\]

with \(Re\) the particle Reynolds number based on the diameter
\(2 r_i\), the fluid density \(\rho_f\), and the dynamic viscosity
of the fluid \(\mu_f\).  In the low-Reynolds-number limit
(\(Re \rightarrow 0\)) the correlation reduces to
\(C_d = 24/Re\) and the force becomes the Stokes drag
\(\vec{F}_i = -6 \pi \mu_f r_i \vec{v}_{rel}\).

By default the fluid is at rest.  The optional velocity keyword sets a
uniform fluid velocity \(\vec{v}_f\), so the drag is computed
from the particle velocity relative to the moving fluid.  This fix only
applies a drag force; buoyancy and gravity (if desired) must be added
separately, e.g. with fix gravity.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix drag all viscous/nonlinear 1.2 1.8e-5
fix drag flow viscous/nonlinear 1.2 1.8e-5 velocity 0.0 0.0 0.4
```

## Restrictions

Restrictions 
This fix is part of the GRANULAR package.  It is only enabled if LAMMPS
was built with that package.  See the Build package page for more info.
This fix requires that atoms store a radius as defined by the
atom_style sphere command.

## Related Commands

- [fix viscous](fix_viscous.html)
- [fix viscous/sphere](fix_viscous_sphere.html)
- [fix gravity](fix_gravity.html)

