---
id: fix_rheo_thermal
title: "fix rheo/thermal command"
url: https://docs.lammps.org/fix_rheo_thermal.html
---

# fix rheo/thermal command

## Syntax

```
fix ID group-ID rheo/thermal attribute values ...
conductivity args = types style args
  types = lists of types (see below)
  style = constant
    constant arg = conductivity (power/(length*temperature))
specific/heat args = types style args
  types = lists of types (see below)
  style = constant
    constant arg = specific heat (energy/(mass*temperature))
latent/heat args = types style args
  types = lists of types (see below)
  style = constant
    constant arg = latent heat (energy/mass)
Tfreeze args = types style args
  types = lists of types (see below)
  style = constant
    constant arg = freezing temperature (temperature)
react args = cut type
  cut = maximum bond distance
  type = bond type
```

## Description

Added in version 29Aug2024.

This fix performs time integration of temperature for atom style rheo/thermal.
In addition, it defines multiple thermal properties of particles and handles
melting/solidification, if applicable. For more details on phase transitions
in RHEO, see the RHEO howto.

Note that the temperature of a particle is always derived from the energy.
This implies the temperature attribute of the set command does
not affect particles. Instead, one should use the sph/e attribute.

For each atom type, one can define expressions for the conductivity,
specific/heat, latent/heat, and critical temperature (Tfreeze).
The conductivity and specific heat must be defined for all atom types.
The latent heat and critical temperature are optional. However, a
critical temperature must be defined to specify a latent heat.

Note, if shifting is turned on in fix rheo, the gradient
of the energy is used to shift energies. This may be inappropriate in systems
with multiple atom types with different specific heats.

For each property, one must first define a list of atom types. A wild-card
asterisk can be used in place of or in conjunction with the types argument to
set values for multiple atom types.  This takes the form  *  or  *n  or  m* 
or  m*n .  If \(N\) is the number of atom types, then an asterisk with no
numeric values means all types from 1 to \(N\).  A leading asterisk means
all types from 1 to n (inclusive). A trailing asterisk means all types from m
to \(N\) (inclusive).  A middle asterisk means all types from m to n
(inclusive).

The types definition for each property is followed by the style. Currently,
the only option is constant. Style constant simply applies a constant value
of respective property to each particle of the assigned type.

The react keyword controls whether bonds are created/deleted when particles
transition between a fluid and solid state. This option only applies to atom
types that have a defined value of Tfreeze. When a fluid particle s
temperature drops below Tfreeze, bonds of type btype are created between
nearby solid particles within a distance of cut. The particle s status also
swaps to a solid state. When a solid particle s temperature rises above
Tfreeze, all bonds of type btype are broken and the particle s status swaps
to a fluid state.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 1 all rheo/thermal conductivity * constant 1.0 specific/heat * constant 1.0 Tfreeze * constant 1.0
fix 1 all rheo/pressure conductivity 1*2 constant 1.0 conductivity 3*4 constant 2.0 specific/heat * constant 1.0
```

## Restrictions

Restrictions 
This fix must be used with an atom style that includes temperature,
heatflow, and conductivity such as atom_style rheo/thermal This fix
must be used in conjunction with fix rheo with the
thermal setting. The fix group must be set to all. Only one
instance of fix rheo/pressure can be defined.
This fix is part of the RHEO package.  It is only enabled if
LAMMPS was built with that package.  See the Build package
page for more info.

## Related Commands

- [fix rheo](fix_rheo.html)
- [pair rheo](pair_rheo.html)
- [compute rheo/property/atom](compute_rheo_property_atom.html)
- [fix add/heat](fix_add_heat.html)

