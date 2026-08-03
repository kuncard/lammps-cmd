---
id: compute_temp_region
title: "compute temp/region command"
url: https://docs.lammps.org/compute_temp_region.html
---

# compute temp/region command

## Syntax

```
compute ID group-ID temp/region region-ID
```

## Description

Define a computation that calculates the temperature of a group of atoms in a
geometric region.  This can be useful for thermostatting one portion of the
simulation box.  For example, a McDLT simulation where one side is cooled, and
the other side is heated.  A compute of this style can be used by any command
that computes a temperature (e.g., thermo_modify,
fix temp/rescale).

Note that a region-style temperature can be used to thermostat with
fix temp/rescale or
fix langevin, but should probably not be used with
Nose Hoover style fixes (fix nvt, fix npt,
or fix nph) if the degrees of freedom included in the computed
temperature vary with time.

The temperature is calculated by the formula

\[\text{KE} = \frac{\text{dim}}{2} N k_B T,\]

where KE = is the total kinetic energy of the group of atoms (sum of
\(\frac12 m v^2\)), dim = 2 or 3 is the dimensionality of the simulation,
\(N\) is the  number of atoms in both the group and region, \(k_B\) is
the Boltzmann constant, and \(T\) temperature.

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

The number of atoms contributing to the temperature is calculated each
time the temperature is evaluated since it is assumed atoms can
enter/leave the region.  Thus there is no need to use the dynamic
option of the compute_modify command for this
compute style.

The removal of atoms outside the region by this fix is essentially
computing the temperature after a  bias  has been removed, which in
this case is the velocity of any atoms outside the region.  If this
compute is used with a fix command that performs thermostatting then
this bias will be subtracted from each atom, thermostatting of the
remaining thermal velocity will be performed, and the bias will be
added back in.  Thermostatting fixes that work in this way include
fix nvt, fix temp/rescale,
fix temp/berendsen, and
fix langevin.  This means that when this compute
is used to calculate the temperature for any of the thermostatting
fixes via the fix modify temp command, the thermostat
will operate only on atoms that are currently in the geometric region.

Unlike other compute styles that calculate temperature, this compute
does not subtract out degrees-of-freedom due to fixes that constrain
motion, such as fix shake and fix rigid.  This is because those degrees of freedom (e.g., a
constrained bond) could apply to sets of atoms that straddle the
region boundary, and hence the concept is somewhat ill-defined.  If
needed the number of subtracted degrees of freedom can be set
explicitly using the extra option of the compute_modify command.

See the Howto thermostat page for a
discussion of different ways to compute temperature and perform
thermostatting.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute mine flow temp/region boundary
```

## Restrictions

Restrictions 
none

## Related Commands

- [compute temp](compute_temp.html)
- [compute pressure](compute_pressure.html)

