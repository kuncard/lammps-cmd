---
id: pair_rheo
title: "pair_style rheo command"
url: https://docs.lammps.org/pair_rheo.html
---

# pair_style rheo command

## Syntax

```
pair_style rheo cutoff keyword values
rho/damp args = density damping prefactor \(\xi\)
artificial/visc args = artificial viscosity prefactor \(\zeta\)
harmonic/means args = none
```

## Description

Added in version 29Aug2024.

Pair style rheo computes pressure and viscous forces between particles
in the rheo package. If thermal evolution is turned
on in fix rheo, then the pair style also calculates
heat exchanged between particles.

The artificial/viscosity keyword is used to specify the magnitude
\(\zeta\) of an optional artificial viscosity contribution to forces.
This factor can help stabilize simulations by smoothing out small length
scale variations in velocity fields. Artificial viscous forces typically
are only exchanged by fluid particles. However, if interfaces are not
reconstructed in fix rheo, fluid particles will also exchange artificial
viscous forces with solid particles to improve stability.

The rho/damp keyword is used to specify the magnitude \(\xi\) of
an optional pairwise damping term between the density of particles. This
factor can help stabilize simulations by smoothing out small length
scale variations in density fields. However, in systems that develop
a density gradient in equilibrium (e.g. in a hydrostatic column underlying
gravity), this option may be inappropriate.

If particles have different viscosities or conductivities, the
harmonic/means keyword changes how they are averaged before calculating
pairwise forces or heat exchanges. By default, an arithmetic averaged is
used, however, a harmonic mean may improve stability in systems with multiple
fluid phases with large disparities in viscosities.

No coefficients are defined for each pair of atoms types via the
pair_coeff command as in the examples
above.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
pair_style rheo 3.0 rho/damp 1.0 artificial/visc 2.0
pair_coeff * *
```

## Restrictions

Restrictions 
This fix is part of the RHEO package.  It is only enabled if
LAMMPS was built with that package.  See the
Build package page for more info.

## Related Commands

- [fix rheo](fix_rheo.html)
- [fix rheo/pressure](fix_rheo_pressure.html)
- [fix rheo/thermal](fix_rheo_thermal.html)
- [fix rheo/viscosity](fix_rheo_viscosity.html)
- [compute rheo/property/atom](compute_rheo_property_atom.html)

