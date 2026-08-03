---
id: compute_temp_partial
title: "compute temp/partial command"
url: https://docs.lammps.org/compute_temp_partial.html
---

# compute temp/partial command

## Syntax

```
compute ID group-ID temp/partial xflag yflag zflag
```

## Description

Define a computation that calculates the temperature of a group of
atoms, after excluding one or more velocity components.  A compute of
this style can be used by any command that computes a temperature
(e.g. thermo_modify,
fix temp/rescale, fix npt).

The temperature is calculated by the formula

\[\text{KE} = \frac{\text{dim}}{2} N k_B T,\]

where KE is the total kinetic energy of the group of atoms (sum of
\(\frac12 m v^2\)), dim = 2 or 3 is the dimensionality of the simulation,
\(N\) is the number of atoms in the group, \(k_B\) is the Boltzmann
constant, and \(T\) = temperature.  The calculation of KE excludes the
\(x\), \(y\), or \(z\) dimensions if xflag, yflag, or zflag
is 0.  The dim parameter is adjusted to give the correct number of
degrees of freedom.

A symmetric tensor, stored as a six-element vector, is also calculated
by this compute for use in the computation of a pressure tensor by the
compute pressure command.  The formula for
the components of the tensor is the same as the above expression for
\(E_\mathrm{kin}\), except that the 1/2 factor is NOT included and
the \(v_i^2\) is replaced by \(v_{i,x} v_{i,y}\) for the
\(xy\) component, and so on.  Note that because it lacks the 1/2
factor, these tensor components are twice those of the traditional
kinetic energy tensor.  The six components of the vector are ordered
\(xx\), \(yy\), \(zz\), \(xy\), \(xz\),
\(yz\).

The number of atoms contributing to the temperature is assumed to be
constant for the duration of the run; use the dynamic option of the
compute_modify command if this is not the case.

The removal of velocity components by this fix is essentially
computing the temperature after a  bias  has been removed from the
velocity of the atoms.  If this compute is used with a fix command
that performs thermostatting then this bias will be subtracted from
each atom, thermostatting of the remaining thermal velocity will be
performed, and the bias will be added back in.  Thermostatting fixes
that work in this way include fix nvt,
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
compute newT flow temp/partial 1 1 0
```

## Restrictions

Restrictions 
none

## Related Commands

- [compute temp](compute_temp.html)
- [compute temp/region](compute_temp_region.html)
- [compute pressure](compute_pressure.html)

