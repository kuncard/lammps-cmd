---
id: fix_smd
title: "fix smd command"
url: https://docs.lammps.org/fix_smd.html
---

# fix smd command

## Syntax

```
fix ID group-ID smd type values keyword values
cvel values = K vel
  K = spring constant (force/distance units)
  vel = velocity of pulling (distance/time units)
cfor values = force
  force = pulling force (force units)
tether values = x y z R0
  x,y,z = point to which spring is tethered
  R0 = distance of end of spring from tether point (distance units)
couple values = group-ID2 x y z R0
  group-ID2 = 2nd group to couple to fix group with a spring
  x,y,z = direction of spring, automatically computed with 'auto'
  R0 = distance of end of spring (distance units)
```

## Description

Fix smd is unmaintained
Please note that fix smd is unmaintained and has multiple known
issues.  We recommend to use the equivalent functionality in either
fix colvars or fix plumed
instead, which are both actively maintained.

This fix implements several options of steered MD (SMD) as reviewed in
(Izrailev), which allows to induce conformational
changes in systems and to compute the potential of mean force (PMF)
along the assumed reaction coordinate (Park) based on
Jarzynski s equality (Jarzynski).  This fix borrows
a lot from fix spring and fix setforce.

You can apply a moving spring force to a group of atoms (tether
style) or between two groups of atoms (couple style).  The spring
can then be used in either constant velocity (cvel) mode or in
constant force (cfor) mode to induce transitions in your systems.
When running in tether style, you may need some way to fix some
other part of the system (e.g. via fix spring/self)

The tether style attaches a spring between a point at a distance of
R0 away from a fixed point x,y,z and the center of mass of the fix
group of atoms.  A restoring force of magnitude K (R - R0) Mi / M is
applied to each atom in the group where K is the spring constant, Mi
is the mass of the atom, and M is the total mass of all atoms in the
group.  Note that K thus represents the total force on the group of
atoms, not a per-atom force.

In cvel mode the distance R is incremented or decremented
monotonously according to the pulling (or pushing) velocity.
In cfor mode a constant force is added and the actual distance
in direction of the spring is recorded.

The couple style links two groups of atoms together.  The first
group is the fix group; the second is specified by group-ID2.  The
groups are coupled together by a spring that is at equilibrium when
the two groups are displaced by a vector in direction x,y,z with
respect to each other and at a distance R0 from that displacement.
Note that x,y,z only provides a direction and will be internally
normalized. But since it represents the absolute displacement of
group-ID2 relative to the fix group, (1,1,0) is a different spring
than (-1,-1,0).  For each vector component, the displacement can be
described with the auto parameter. In this case the direction is
re-computed in every step, which can be useful for steering a local
process where the whole object undergoes some other change.  When the
relative positions and distance between the two groups are not in
equilibrium, the same spring force described above is applied to atoms
in each of the two groups.

For both the tether and couple styles, any of the x,y,z values can
be specified as NULL which means do not include that dimension in the
distance calculation or force application.

For constant velocity pulling (cvel mode), the running integral
over the pulling force in direction of the spring is recorded and
can then later be used to compute the potential of mean force (PMF)
by averaging over multiple independent trajectories along the same
pulling path.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix  pull    cterm smd cvel 20.0 -0.00005 tether NULL NULL 100.0 0.0
fix  pull    cterm smd cvel 20.0 -0.0001 tether 25.0 25 25.0 0.0
fix  stretch cterm smd cvel 20.0  0.0001 couple nterm auto auto auto 0.0
fix  pull    cterm smd cfor  5.0 tether 25.0 25.0 25.0 0.0
```

## Restrictions

Restrictions 
This fix is part of the EXTRA-FIX package.  It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.

## Related Commands

- [fix drag](fix_drag.html)
- [fix spring](fix_spring.html)
- [fix spring/self](fix_spring_self.html)
- [fix spring/rg](fix_spring_rg.html)
- [fix colvars](fix_colvars.html)
- [fix plumed](fix_plumed.html)

