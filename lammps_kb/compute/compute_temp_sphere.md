---
id: compute_temp_sphere
title: "compute temp/sphere command"
url: https://docs.lammps.org/compute_temp_sphere.html
---

# compute temp/sphere command

## Syntax

```
compute ID group-ID temp/sphere keyword value ...
bias value = bias-ID
  bias-ID = ID of a temperature compute that removes a velocity bias
dof value = all or rotate
  all = compute temperature of translational and rotational degrees of freedom
  rotate = compute temperature of just rotational degrees of freedom
```

## Description

Define a computation that calculates the temperature of a group of
spherical particles, including a contribution from both their
translational and rotational kinetic energy.  This differs from the
usual compute temp command, which assumes point
particles with only translational kinetic energy.

Both point and finite-size particles can be included in the group.
Point particles do not rotate, so they have only three translational
degrees of freedom.  For 3d spherical particles, each has six degrees of
freedom (three translational, three rotational).  For 2d spherical particles,
each has three degrees of freedom (two translational, one rotational).

Note
This choice for degrees of freedom (DOF) assumes that all finite-size
spherical particles in your model will freely rotate, sampling all
their rotational DOF.  It is possible to use a combination of
interaction potentials and fixes that induce no torque or otherwise
constrain some of all of your particles so that this is not the case.
Then there are less DOF and you should use the compute_modify
extra/dof command to adjust the DOF accordingly.

The translational kinetic energy is computed the same as is described
by the compute temp command.  The rotational
kinetic energy is computed as \(\frac12 I \omega^2\), where \(I\) is
the moment of inertia for a sphere and \(\omega\) is the particle s angular
velocity.

Note
For 2d models, particles are treated as
spheres, not disks, meaning their moment of inertia will be the same
as in 3d.

A kinetic energy tensor, stored as a six-element vector, is also
calculated by this compute.  The formula for the components of the
tensor is the same as the above formulas, except that \(v^2\) and
\(\omega^2\) are replaced by \(v_x v_y\) and \(\omega_x
\omega_y\) for the \(xy\) component.  The six components of the
vector are ordered \(xx\), \(yy\), \(zz\), \(xy\),
\(xz\), \(yz\).

A symmetric tensor, stored as a six-element vector, is also calculated
by this compute for use in the computation of a pressure tensor by the
compute pressue command.  The formula for
the components of the tensor is the same as the above expression for
\(E_\mathrm{kin}\), except that the 1/2 factor is NOT included and
the \(v_i^2\) and \(\omega^2\) are replaced by \(v_x v_y\)
and \(\omega_x \omega_y\) for the \(xy\) component, and so on.
Note that because it lacks the 1/2 factor, these tensor components are
twice those of the traditional kinetic energy tensor.  The six
components of the vector are ordered \(xx\), \(yy\),
\(zz\), \(xy\), \(xz\), \(yz\).

The number of atoms contributing to the temperature is assumed to be
constant for the duration of the run; use the dynamic option of the
compute_modify command if this is not the case.

This compute subtracts out translational degrees-of-freedom due to fixes
that constrain molecular motion, such as fix shake
and fix rigid.  This means the temperature of groups
of atoms that include these constraints will be computed correctly.  If
needed, the subtracted degrees of freedom can be altered using the
extra/dof option of the compute_modify
command.

See the Howto thermostat page for a
discussion of different ways to compute temperature and perform
thermostatting.

The keyword/value option pairs are used in the following ways.

For the bias keyword, bias-ID refers to the ID of a temperature
compute that removes a  bias  velocity from each atom.  This allows
compute temp/sphere to compute its thermal temperature after the
translational kinetic energy components have been altered in a
prescribed way (e.g., to remove a flow velocity profile).  Thermostats
that use this compute will work with this bias term.  See the doc
pages for individual computes that calculate a temperature and the doc
pages for fixes that perform thermostatting for more details.

For the dof keyword, a setting of all calculates a temperature
that includes both translational and rotational degrees of freedom.
A setting of rotate calculates a temperature that includes only
rotational degrees of freedom.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 all temp/sphere
compute myTemp mobile temp/sphere bias tempCOM
compute myTemp mobile temp/sphere dof rotate
```

## Restrictions

Restrictions 
This fix requires that atoms store torque and angular velocity (omega)
and a radius as defined by the atom_style sphere
command.
All particles in the group must be finite-size spheres, or point
particles with radius = 0.0.

## Related Commands

- [compute temp](compute_temp.html)
- [compute temp/asphere](compute_temp.html)

