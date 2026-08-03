---
id: fix_viscous
title: "fix viscous command"
url: https://docs.lammps.org/fix_viscous.html
---

# fix viscous command

## Syntax

```
fix ID group-ID viscous gamma keyword values ...
keyword = scale
  scale values = type ratio
    type = atom type (1-N)
    ratio = factor to scale the damping coefficient by
```

## Description

Add a viscous damping force to atoms in the group that is proportional
to the velocity of the atom.  The added force can be thought of as a
frictional interaction with implicit solvent, i.e. the no-slip Stokes
drag on a spherical particle.  In granular simulations this can be
useful for draining the kinetic energy from the system in a controlled
fashion.  If used without additional thermostatting (to add kinetic
energy to the system), it has the effect of slowly (or rapidly)
freezing the system; hence it can also be used as a simple energy
minimization technique.

The damping force \(F_i\) is given by \(F_i = - \gamma v_i\).
The larger the coefficient, the faster the kinetic energy is reduced.
If the optional keyword scale is used, \(\gamma\) can scaled up or
down by the specified factor for atoms of that type.  It can be used
multiple times to adjust \(\gamma\) for several atom types.

Note
You should specify gamma in force/velocity units.  This is not
the same as mass/time units, at least for some of the LAMMPS
units options like  real  or  metal  that are not
self-consistent.

In a Brownian dynamics context, \(\gamma = \frac{k_B T}{D}\), where
\(k_B =\) Boltzmann s constant, \(T\) = temperature, and D =
particle diffusion coefficient.  D can be written as \(\frac{k_B
T}{3 \pi \eta d}\), where \(\eta =\) dynamic viscosity of the
frictional fluid and d = diameter of particle.  This means \(\gamma
= 3 \pi \eta d\), and thus is proportional to the viscosity of the fluid
and the particle diameter.

In the current implementation, rather than have the user specify a
viscosity, \(\gamma\) is specified directly in force/velocity units.
If needed, \(\gamma\) can be adjusted for atoms of different sizes
(i.e. \(\sigma\)) by using the scale keyword.

Note that Brownian dynamics models also typically include a randomized
force term to thermostat the system at a chosen temperature.  The
fix langevin command does this.  It has the same
viscous damping term as fix viscous and adds a random force to each
atom.  The random force term is proportional to the square root of the
chosen thermostatting temperature.  Thus if you use fix langevin with a
target \(T = 0\), its random force term is zero, and you are
essentially performing the same operation as fix viscous.  Also note
that the gamma of fix viscous is related to the damping parameter of
fix langevin, however the former is specified in
units of force/velocity and the latter in units of time, so that it can
more easily be used as a thermostat.

Styles with a gpu, intel, kk, omp, or opt suffix are
functionally the same as the corresponding style without the suffix.
They have been optimized to run faster, depending on your available
hardware, as discussed on the Accelerator packages
page.  The accelerated styles take the same arguments and should
produce the same results, except for round-off and precision issues.

These accelerated styles are part of the GPU, INTEL, KOKKOS,
OPENMP, and OPT packages, respectively.  They are only enabled if
LAMMPS was built with those packages.  See the Build package page for more info.

You can specify the accelerated styles explicitly in your input script
by including their suffix, or you can use the -suffix command-line switch when you invoke LAMMPS, or you can use the
suffix command in your input script.

See the Accelerator packages page for more
instructions on how to use the accelerated styles effectively.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 1 flow viscous 0.1
fix 1 damp viscous 0.5 scale 3 2.5
```

## Restrictions

Restrictions 
none

## Related Commands

- [fix langevin](fix_langevin.html)
- [fix viscous/sphere](fix_viscous_sphere.html)
- [fix damping/cundall](fix_damping_cundall.html)

