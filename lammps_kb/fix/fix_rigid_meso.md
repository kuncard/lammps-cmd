---
id: fix_rigid_meso
title: "fix rigid/meso command"
url: https://docs.lammps.org/fix_rigid_meso.html
---

# fix rigid/meso command

## Syntax

```
fix ID group-ID rigid/meso bodystyle args keyword values ...
single args = none
molecule args = none
custom args = i_propname or v_varname
  i_propname = an integer property defined via fix property/atom
  v_varname  = an atom-style or atomfile-style variable
group args = N groupID1 groupID2 ...
  N = # of groups
  groupID1, groupID2, ... = list of N group IDs
reinit = yes or no
force values = M xflag yflag zflag
  M = which rigid body from 1-Nbody (see asterisk form below)
  xflag,yflag,zflag = off/on if component of center-of-mass force is active
torque values = M xflag yflag zflag
  M = which rigid body from 1-Nbody (see asterisk form below)
  xflag,yflag,zflag = off/on if component of center-of-mass torque is active
infile filename
  filename = file with per-body values of mass, center-of-mass, moments of inertia
```

## Description

Treat one or more sets of mesoscopic SPH/SDPD particles as independent
rigid bodies.  This means that each timestep the total force and torque
on each rigid body is computed as the sum of the forces and torques on
its constituent particles.  The coordinates and velocities of the
particles in each body are then updated so that the body moves and
rotates as a single entity using the methods described in the paper by
(Miller). Density and internal energy of the particles will
also be updated. This is implemented by creating internal data structures
for each rigid body and performing time integration on these data
structures.  Positions and velocities of the constituent particles are
regenerated from the rigid body data structures in every time step. This
restricts which operations and fixes can be applied to rigid bodies. See
below for a detailed discussion.

The operation of this fix is exactly like that described by the
fix rigid/nve command, except that particles  density,
internal energy and extrapolated velocity are also updated.

Note
You should not update the particles in rigid bodies via other
time-integration fixes (e.g. fix sph, fix
sph/stationary), or you will have conflicting
updates to positions and velocities resulting in unphysical
behavior in most cases. When performing a hybrid simulation with
some atoms in rigid bodies, and some not, a separate time
integration fix like fix sph should be used for
the non-rigid particles.

Note
These fixes are overkill if you simply want to hold a collection of
particles stationary or have them move with a constant velocity. To
hold particles stationary use fix sph/stationary instead. If you would like to move particles
with a constant velocity use fix meso/move.

Warning
The aggregate properties of each rigid body are
calculated at the start of a simulation run and are maintained in
internal data structures. The properties include the position and
velocity of the center-of-mass of the body, its moments of inertia, and
its angular momentum.  This is done using the properties of the
constituent particles of the body at that point in time (or see the infile
keyword option).  Thereafter, changing these properties of individual
particles in the body will have no effect on a rigid body s dynamics, unless
they effect any computation of per-particle forces or torques. If the
keyword reinit is set to yes (the default), the rigid body data
structures will be recreated at the beginning of each run command;
if the keyword reinit is set to no, the rigid body data structures
will be built only at the very first run command and maintained for
as long as the rigid fix is defined. For example, you might think you
could displace the particles in a body or add a large velocity to each particle
in a body to make it move in a desired direction before a second run is
performed, using the set or
displace_atoms or velocity
commands.  But these commands will not affect the internal attributes
of the body unless reinit is set to yes. With reinit set to no
(or using the infile option, which implies reinit no) the position
and velocity of individual particles in the body will be reset when time
integration starts again.

Each rigid body must have two or more particles.  A particle can belong
to at most one rigid body.  Which particles are in which bodies can be
defined via several options.

For bodystyle single the entire fix group of particles is treated as
one rigid body.

For bodystyle molecule, particles are grouped into rigid bodies by their
respective molecule IDs: each set of particles in the fix group with the
same molecule ID is treated as a different rigid body.  Note that particles
with a molecule ID = 0 will be treated as a single rigid body. For a
system with solvent (typically this is particles with molecule ID = 0)
surrounding rigid bodies, this may not be what you want.  Thus you
should be careful to use a fix group that only includes particles you
want to be part of rigid bodies.

Bodystyle custom is similar to bodystyle molecule except that it
is more flexible in using other per-atom properties to define the sets
of particles that form rigid bodies.  An integer vector defined by the
fix property/atom command can be used.  Or an
atom-style or atomfile-style variable can be used; the
floating-point value produced by the variable is rounded to an
integer.  As with bodystyle molecule, each set of particles in the fix
groups with the same integer value is treated as a different rigid
body.  Since fix property/atom vectors and atom-style variables
produce values for all particles, you should be careful to use a fix group
that only includes particles you want to be part of rigid bodies.

For bodystyle group, each of the listed groups is treated as a
separate rigid body.  Only particles that are also in the fix group are
included in each rigid body.

Note
To compute the initial center-of-mass position and other
properties of each rigid body, the image flags for each particle in the
body are used to  unwrap  the particle coordinates.  Thus you must
ensure that these image flags are consistent so that the unwrapping
creates a valid rigid body (one where the particles are close together)
, particularly if the particles in a single rigid body straddle a
periodic boundary.  This means the input data file or restart file must
define the image flags for each particle consistently or that you have
used the set command to specify them correctly.  If a
dimension is non-periodic then the image flag of each particle must be
0 in that dimension, else an error is generated.

By default, each rigid body is acted on by other particles which induce
an external force and torque on its center of mass, causing it to
translate and rotate.  Components of the external center-of-mass force
and torque can be turned off by the force and torque keywords.
This may be useful if you wish a body to rotate but not translate, or
vice versa, or if you wish it to rotate or translate continuously
unaffected by interactions with other particles.  Note that if you
expect a rigid body not to move or rotate by using these keywords, you
must ensure its initial center-of-mass translational or angular
velocity is 0.0. Otherwise the initial translational or angular
momentum, the body has, will persist.

An xflag, yflag, or zflag set to off means turn off the component of
force or torque in that dimension.  A setting of on means turn on
the component, which is the default.  Which rigid body(s) the settings
apply to is determined by the first argument of the force and
torque keywords.  It can be an integer M from 1 to Nbody, where
Nbody is the number of rigid bodies defined.  A wild-card asterisk can
be used in place of, or in conjunction with, the M argument to set the
flags for multiple rigid bodies.  This takes the form  *  or  *n  or
 n*  or  m*n .  If N = the number of rigid bodies, then an asterisk
with no numeric values means all bodies from 1 to N.  A leading
asterisk means all bodies from 1 to n (inclusive).  A trailing
asterisk means all bodies from n to N (inclusive).  A middle asterisk
means all bodies from m to n (inclusive).  Note that you can use the
force or torque keywords as many times as you like.  If a
particular rigid body has its component flags set multiple times, the
settings from the final keyword are used.

For computational efficiency, you should typically define one fix
rigid/meso command which includes all the desired rigid bodies. LAMMPS
will allow multiple rigid/meso fixes to be defined, but it is more
expensive.

The keyword/value option pairs are used in the following ways.

The reinit keyword determines, whether the rigid body properties
are re-initialized between run commands. With the option yes (the
default) this is done, with the option no this is not done. Turning
off the re-initialization can be helpful to protect rigid bodies against
unphysical manipulations between runs or when properties cannot be
easily re-computed (e.g. when read from a file). When using the infile
keyword, the reinit option is automatically set to no.

The infile keyword allows a file of rigid body attributes to be read
in from a file, rather then having LAMMPS compute them.  There are 5
such attributes: the total mass of the rigid body, its center-of-mass
position, its 6 moments of inertia, its center-of-mass velocity, and
the 3 image flags of the center-of-mass position.  For rigid bodies
consisting of point particles or non-overlapping finite-size
particles, LAMMPS can compute these values accurately.  However, for
rigid bodies consisting of finite-size particles which overlap each
other, LAMMPS will ignore the overlaps when computing these 4
attributes.  The amount of error this induces depends on the amount of
overlap.  To avoid this issue, the values can be pre-computed
(e.g. using Monte Carlo integration).

The format of the file is as follows.  Note that the file does not
have to list attributes for every rigid body integrated by fix rigid.
Only bodies which the file specifies will have their computed
attributes overridden.  The file can contain initial blank lines or
comment lines starting with  #  which are ignored.  The first
non-blank, non-comment line should list N = the number of lines to
follow.  The N successive lines contain the following information:

ID1 masstotal xcm ycm zcm ixx iyy izz ixy ixz iyz vxcm vycm vzcm lx ly lz ixcm iycm izcm
ID2 masstotal xcm ycm zcm ixx iyy izz ixy ixz iyz vxcm vycm vzcm lx ly lz ixcm iycm izcm
...
IDN masstotal xcm ycm zcm ixx iyy izz ixy ixz iyz vxcm vycm vzcm lx ly lz ixcm iycm izcm

The rigid body IDs are all positive integers.  For the single
bodystyle, only an ID of 1 can be used.  For the group bodystyle,
IDs from 1 to Ng can be used where Ng is the number of specified
groups.  For the molecule bodystyle, use the molecule ID for the
atoms in a specific rigid body as the rigid body ID.

The masstotal and center-of-mass coordinates (xcm,ycm,zcm) are
self-explanatory.  The center-of-mass should be consistent with what
is calculated for the position of the rigid body with all its atoms
unwrapped by their respective image flags.  If this produces a
center-of-mass that is outside the simulation box, LAMMPS wraps it
back into the box.

The 6 moments of inertia (ixx,iyy,izz,ixy,ixz,iyz) should be the
values consistent with the current orientation of the rigid body
around its center of mass.  The values are with respect to the
simulation box XYZ axes, not with respect to the principal axes of the
rigid body itself.  LAMMPS performs the latter calculation internally.

The (vxcm,vycm,vzcm) values are the velocity of the center of mass.
The (lx,ly,lz) values are the angular momentum of the body.  The
(vxcm,vycm,vzcm) and (lx,ly,lz) values can simply be set to 0 if you
wish the body to have no initial motion.

The (ixcm,iycm,izcm) values are the image flags of the center of mass
of the body.  For periodic dimensions, they specify which image of the
simulation box the body is considered to be in.  An image of 0 means
it is inside the box as defined.  A value of 2 means add 2 box lengths
to get the true value.  A value of -1 means subtract 1 box length to
get the true value.  LAMMPS updates these flags as the rigid bodies
cross periodic boundaries during the simulation.

Note
If you use the infile keyword and write restart
files during a simulation, then each time a restart file is written,
the fix also write an auxiliary restart file with the name
rfile.rigid, where  rfile  is the name of the restart file,
e.g. tmp.restart.10000 and tmp.restart.10000.rigid.  This auxiliary
file is in the same format described above.  Thus it can be used in a
new input script that restarts the run and re-specifies a rigid fix
using an infile keyword and the appropriate filename.  Note that the
auxiliary file will contain one line for every rigid body, even if the
original file only listed a subset of the rigid bodies.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 1 ellipsoid rigid/meso single
fix 1 rods      rigid/meso molecule
fix 1 spheres   rigid/meso single force 1 off off on
fix 1 particles rigid/meso molecule force 1*5 off off off force 6*10 off off on
fix 2 spheres   rigid/meso group 3 sphere1 sphere2 sphere3 torque * off off off
```

## Restrictions

Restrictions 
This fix is part of the DPD-SMOOTH package and also depends on the RIGID
package.  It is only enabled if LAMMPS was built with both packages. See
the Build package page for more info.
This fix requires that atoms store density and internal energy as
defined by the atom_style sph command.
All particles in the group must be mesoscopic SPH/SDPD particles.

Changed in version 29Aug2024.

This fix is incompatible with deformation controls that remap velocity,
for instance the remap v option of fix deform.

## Related Commands

- [fix meso/move](fix_meso_move.html)
- [fix rigid](fix_rigid.html)
- [neigh_modify exclude](neigh_modify.html)

