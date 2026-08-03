---
id: fix_align_self
title: "fix align/self command"
url: https://docs.lammps.org/fix_align_self.html
---

# fix align/self command

## Syntax

```
fix ID group-ID align/self mode magnitude keyword values
qvector value = direction of self-propulsion force in ellipsoid frame
 sx, sy, sz = components of qvector
```

## Description

Added in version 10Dec2025.

Add a torque to each atom in the group which accounts for the
reorientation of each particle toward its own velocity, a generic
phenomenon called self-alignment (see (Baconnier2025)). The torque is given by :

\[\mathbf{\tau}_i = \zeta(\mathbf{e}_i \times \mathbf{v}_i)\]

where i is the particle the torque is being applied to, \(\zeta\)
is the magnitude of the torque, \(\mathbf{e}_i\) is the orientation
of the particle, and \(\mathbf{v}_i\) is its velocity. The
self-alignment term, introduced in (Shimoyama1996) with the study of collective motion in systems of
self-propelled particles, is an effective torque arising from
differential drag in asymmetric rigid bodies.

For mode dipole, \(e_i\) is just equal to the dipole vectors of
the atoms in the group. Therefore, if the dipoles are not unit vectors,
the \(e_i\) will not be unit vectors.

Note
If another command changes the magnitude of the dipole, the applied
torque will change accordingly and no warning will be provided by
LAMMPS. This is almost never what you want, so ensure you are not
changing dipole magnitudes with another LAMMPS fix or pair style.
Furthermore, self-propulsion forces (almost) always set \(e_i\)
to be a unit vector for all times, so it s best to set all the dipole
magnitudes to 1.0 unless you have a good reason not to (see the
set command on how to do this).

For mode quat, \(e_i\) points in the direction of a unit vector,
oriented in the coordinate frame of the ellipsoidal particles, which
defaults to point along the x-direction. This default behavior can be
changed by via the qvector keyword.

The optional qvector keyword specifies the direction of
self-propulsion via a unit vector (sx,sy,sz). The arguments sx, sy,
and sz, are defined within the coordinate frame of the atom s
ellipsoid. For instance, for an ellipsoid with long axis along its
x-direction, if one wanted the self-propulsion force to also be along
this axis, set sx equal to 1 and sy, sz both equal to zero. This
keyword may only be specified for mode quat.

Note
In using keyword qvector, the three arguments sx, sy, and sz
will be automatically normalized to components of a unit vector
internally to avoid users having to explicitly do so
themselves. Therefore, in mode quat, the vectors \(e_i\) will
always be of unit length.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix active all align/self dipole 40.0
fix active all align/self quat 15.7 qvector 1.0 0.0 0.0
```

## Restrictions

Restrictions 
This fix is part of the BROWNIAN package.  It is only enabled if LAMMPS
was built with that package.  See the Build package doc page for more info.
The keyword dipole requires that atoms store torque as defined by the
atom_style sphere command, as well as a dipole
moment as defined by the atom_style dipole command
which is part of the DIPOLE package.  The keyword quat requires that
atoms store torque and quaternions as defined by the atom_style
ellipsoid command.

## Related Commands

- [fix propel/self](fix_propel_self.html)
- [fix brownian](fix_brownian.html)
- [fix addtorque/group](fix_addtorque_group.html)

