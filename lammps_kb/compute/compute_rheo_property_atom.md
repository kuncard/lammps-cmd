---
id: compute_rheo_property_atom
title: "compute rheo/property/atom command"
url: https://docs.lammps.org/compute_rheo_property_atom.html
---

# compute rheo/property/atom command

## Syntax

```
compute ID group-ID rheo/property/atom input1 input2 ...
possible attributes = phase, surface, surface/r,
                      surface/divr, surface/n/a, coordination,
                      shift/v/a, energy, temperature, heatflow,
                      conductivity, cv, viscosity, pressure, rho,
                      grad/v/ab, stress/v/ab, stress/t/ab, nbond/shell
phase = atom phase state
surface = atom surface status
surface/r = atom distance from the surface
surface/divr = divergence of position at atom position
surface/n/a = a-component of surface normal vector
coordination = coordination number
shift/v/a = a-component of atom shifting velocity
energy = atom energy
temperature = atom temperature
heatflow = atom heat flow
conductivity = atom conductivity
cv = atom specific heat
viscosity = atom viscosity
pressure = atom pressure
rho = atom density
grad/v/ab = ab-component of atom velocity gradient tensor
stress/v/ab = ab-component of atom viscous stress tensor
stress/t/ab = ab-component of atom total stress tensor (pressure and viscous)
nbond/shell = number of oxide bonds
```

## Description

Added in version 29Aug2024.

Define a computation that stores atom attributes specific to the RHEO
package for each atom in the group.  This is useful so that the values
can be used by other output commands that take
computes as inputs. See for example, the
compute reduce,
fix ave/atom,
fix ave/histo,
fix ave/chunk, and
atom-style variable commands.

For vector attributes, e.g. shift/v/\(\alpha\), one must specify
\(\alpha\) as the x, y, or z component, e.g. shift/v/x.
Alternatively, a wild card * will include all components, x and y in
2D or x, y, and z in 3D.

For tensor attributes, e.g. grad/v/\(\alpha \beta\), one must specify
both \(\alpha\) and \(\beta\) as  x, y, or z, e.g. grad/v/xy.
Alternatively, a wild card * will include all components. In 2D, this
includes xx, xy, yx, and yy. In 3D, this includes xx, xy, xz,
yx, yy, yz, zx, zy, and zz.

Many properties require their respective fixes, listed below in related
commands, be defined. For instance, the viscosity attribute is the
viscosity of a particle calculated by
fix rheo/viscosity. The meaning of less obvious
properties is described below.

The phase property indicates whether the particle is in a fluid state,
a value of 0, or a solid state, a value of 1.

The surface property indicates the surface designation produced by
the surface/detection option of fix rheo. Bulk
particles have a value of 0, surface particles have a value of 1, and
splash particles have a value of 2. The surface/r property is the
distance from the surface, up to the kernel cutoff length. Surface particles
have a value of 0. The surface/n/\(\alpha\) properties are the
components of the surface normal vector.

The shift/v/\(\alpha\) properties are the components of the shifting
velocity produced by the shift option of fix rheo.

The nbond/shell property is the number of shell bonds that have been
activated from bond style rheo/shell.

The values are stored in a per-atom vector or array as discussed
below.  Zeroes are stored for atoms not in the specified group or for
quantities that are not defined for a particular particle in the group

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 all rheo/property/atom phase surface/r surface/n/* pressure
compute 2 all rheo/property/atom shift/v/x grad/v/xx stress/v/*
```

## Restrictions

Restrictions 
This compute style is part of the RHEO package.  It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.

## Related Commands

- [dump custom](dump.html)
- [compute reduce](compute_reduce.html)
- [fix ave/atom](fix_ave_atom.html)
- [fix ave/chunk](fix_ave_chunk.html)
- [fix rheo/viscosity](fix_rheo_viscosity.html)
- [fix rheo/pressure](fix_rheo_pressure.html)
- [fix rheo/thermal](fix_rheo_thermal.html)
- [fix rheo/oxdiation](fix_rheo_oxidation.html)
- [fix rheo](fix_rheo.html)

