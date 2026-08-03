---
id: compute_temp_ramp
title: "compute temp/ramp command"
url: https://docs.lammps.org/compute_temp_ramp.html
---

# compute temp/ramp command

## Syntax

```
compute ID group-ID temp/ramp vdim vlo vhi dim clo chi keyword value ...
units value = lattice or box
```

## Description

Define a computation that calculates the temperature of a group of atoms,
after subtracting out an ramped velocity profile before computing the kinetic
energy.  A compute of this style can be used by any command that computes a
temperature (e.g. thermo_modify,
fix temp/rescale, fix npt).

The meaning of the arguments for this command which define the
velocity ramp are the same as for the velocity ramp
command which was presumably used to impose the velocity.

After the ramp velocity has been subtracted from the specified
dimension for each atom, the temperature is calculated by the formula

\[\text{KE} = \frac{\text{dim}}{2} N k_B T,\]

where KE is the total kinetic energy of the group of atoms (sum of
\(\frac12 m v^2\)), dim = 2 or 3 is the dimensionality of the simulation,
\(N\) is the number of atoms in the group, \(k_B\) is the Boltzmann
constant, and \(T\) is the absolute temperature.

The units keyword determines the meaning of the distance units used
for coordinates (clo, chi) and velocities (vlo, vhi).  A box value
selects standard distance units as defined by the units
command (e.g., \(\AA\) for units = real or metal).  A
lattice value means the distance units are in lattice spacings (i.e.,
velocity in lattice spacings per unit time).  The lattice
command must have been previously used to define the lattice spacing.

A symmetric tensor, stored as a six-element vector, is also calculated
by this compute for use in the computation of a pressure tensor by the
compute pressue command.  The formula for
the components of the tensor is the same as the above expression for
\(E_\mathrm{kin}\), except that the 1/2 factor is NOT included and
the \(v_i^2\) is replaced by \(v_{i,x} v_{i,y}\) for the
\(xy\) component, and so on.  Note that because it lacks the 1/2
factor, these tensor components are twice those of the traditional
kinetic energy tensor.  The six components of the vector are ordered
\(xx\), \(yy\), \(zz\), \(xy\), \(xz\),
\(yz\).

The number of atoms contributing to the temperature is assumed to be constant
for the duration of the run; use the dynamic option of the
compute_modify command if this is not the case.

The removal of the ramped velocity component by this fix is
essentially computing the temperature after a  bias  has been removed
from the velocity of the atoms.  If this compute is used with a fix
command that performs thermostatting then this bias will be subtracted
from each atom, thermostatting of the remaining thermal velocity will
be performed, and the bias will be added back in.  Thermostatting
fixes that work in this way include fix nvt,
fix temp/rescale,
fix temp/berendsen, and
fix langevin.

This compute subtracts out degrees-of-freedom due to fixes that
constrain molecular motion, such as fix shake and
fix rigid.  This means the temperature of groups of
atoms that include these constraints will be computed correctly.  If
needed, the subtracted degrees-of-freedom can be altered using the
extra option of the compute_modify command.

See the Howto thermostat page for a
discussion of different ways to compute temperature and perform
thermostatting.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 2nd middle temp/ramp vx 0 8 y 2 12 units lattice
```

## Restrictions

Restrictions 
none

## Related Commands

- [compute temp](compute_temp.html)
- [compute temp/profile](compute_temp_profile.html)
- [compute temp/deform](compute_temp_deform.html)
- [compute pressure](compute_pressure.html)

