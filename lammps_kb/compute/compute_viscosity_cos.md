---
id: compute_viscosity_cos
title: "compute viscosity/cos command"
url: https://docs.lammps.org/compute_viscosity_cos.html
---

# compute viscosity/cos command

## Syntax

```
compute ID group-ID viscosity/cos
```

## Description

Define a computation that calculates the velocity amplitude of a group of atoms
with an cosine-shaped velocity profile and the temperature of them
after subtracting out the velocity profile before computing the kinetic energy.
A compute of this style can be used by any command that computes a temperature
(e.g., thermo_modify, fix npt).

This command together with fix_accelerate/cos
enables viscosity calculation with periodic perturbation method,
as described by Hess.
An acceleration along the \(x\)-direction is applied to the simulation
system by using fix_accelerate/cos command.
The acceleration is a periodic function along the \(z\)-direction:

\[a_{x}(z) = A \cos \left(\frac{2 \pi z}{l_{z}}\right)\]

where \(A\) is the acceleration amplitude, \(l_z\) is the
\(z\)-length of the simulation box. At steady state, the acceleration
generates a velocity profile:

\[v_{x}(z) = V \cos \left(\frac{2 \pi z}{l_{z}}\right)\]

The generated velocity amplitude \(V\) is related to the
shear viscosity \(\eta\) by

\[V = \frac{A \rho}{\eta}\left(\frac{l_{z}}{2 \pi}\right)^{2},\]

and it can be obtained from ensemble average of the velocity profile via

\[V = \frac{\sum\limits_i 2 m_{i} v_{i, x} \cos \left(\frac{2 \pi z_i}{l_{z}}\right)}{\sum\limits_i m_{i}}\]

where \(m_i\), \(v_{i,x}\) and \(z_i\) are the mass,
\(x\)-component velocity, and \(z\)-coordinate of a particle,
respectively.

After the cosine-shaped collective velocity in the \(x\)-direction has been
subtracted for each atom, the temperature is calculated by the formula

\[\text{KE} = \frac{\text{dim}}{2} N k_B T,\]

where KE is the total kinetic energy of the group of atoms (sum of
\(\frac12 m v^2\)), dim = 2 or 3 is the dimensionality of the simulation,
\(N\) is the number of atoms in the group, \(k_B\) is the Boltzmann
constant, and \(T\) is the absolute temperature.

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

The number of atoms contributing to the temperature is assumed to be
constant for the duration of the run; use the dynamic option of the
compute_modify command if this is not the case.
However, in order to get meaningful results, the group ID of this compute should
be all.

The removal of the cosine-shaped velocity component by this command is
essentially computing the temperature after a  bias  has been removed
from the velocity of the atoms.  If this compute is used with a fix
command that performs thermostatting then this bias will be subtracted
from each atom, thermostatting of the remaining thermal velocity will
be performed, and the bias will be added back in.  Thermostatting
fixes that work in this way include fix nvt,
fix temp/rescale,
fix temp/berendsen, and
fix langevin.

This compute subtracts out degrees of freedom due to fixes that
constrain molecular motion, such as fix shake and
fix rigid.  This means that the temperature of groups of
atoms that include these constraints will be computed correctly.  If
needed, the subtracted degrees of freedom can be altered using the
extra option of the compute_modify command.

See the Howto thermostat page for a discussion of
different ways to compute temperature and perform thermostatting.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
units    real
compute  cos all viscosity/cos
variable V equal c_cos[7]
variable A equal 0.02E-5  # A/fs^2
variable density equal density
variable lz equal lz
variable reciprocalViscosity equal v_V/${A}/v_density*39.4784/v_lz/v_lz*100  # 1/(Pa*s)
```

## Restrictions

Restrictions 
This compute is part of the MISC package.  It is only enabled if LAMMPS
was built with that package.  See the Build package page for more info.
Since this compute depends on fix accelerate/cos
which can only work for 3d systems, it cannot be used for 2d systems.

## Related Commands

- [fix accelerate/cos](fix_accelerate_cos.html)

