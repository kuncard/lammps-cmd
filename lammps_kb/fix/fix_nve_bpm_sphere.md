---
id: fix_nve_bpm_sphere
title: "fix nve/bpm/sphere command"
url: https://docs.lammps.org/fix_nve_bpm_sphere.html
---

# fix nve/bpm/sphere command

## Syntax

```
fix ID group-ID nve/bpm/sphere
update value = dipole or dipole/dlm
  dipole = update orientation of dipole moment during integration
  dipole/dlm = use DLM integrator to update dipole orientation
disc value = none = treat particles as 2d discs, not spheres
```

## Description

Added in version 4May2022.

Perform constant NVE integration to update position, velocity, angular
velocity, and quaternion orientation for finite-size spherical
particles in the group each timestep.  V is volume; E is energy.  This
creates a system trajectory consistent with the microcanonical
ensemble.

This fix differs from the fix nve command, which
assumes point particles and only updates their position and velocity.
It also differs from the fix nve/sphere
command which assumes finite-size spheroid particles which do not
store a quaternion.  It thus does not update a particle s orientation
or quaternion.

If the disc keyword is used, then each particle is treated as a 2d
disc (circle) instead of as a sphere.  This is only possible for 2d
simulations, as defined by the dimension keyword.
The only difference between discs and spheres in this context is their
moment of inertia, as used in the time integration.

Added in version 4Jul2026.

If the update keyword is used with the dipole value, then the
orientation of the dipole moment of each particle is also updated
during the time integration,
similar to the fix nve/sphere command.
This option should be used for models where a dipole moment is
assigned to finite-size particles, e.g. spheroids via use of the
atom_style hybrid bpm/sphere dipole command.

The default dipole orientation integrator can be changed to the
Dullweber-Leimkuhler-McLachlan integration scheme
(Dullweber) when using update with the value
dipole/dlm. This integrator is symplectic and time-reversible,
giving better energy conservation and allows slightly longer timesteps
at only a small additional computational cost.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 1 all nve/bpm/sphere
fix 1 all nve/bpm/sphere disc
```

## Restrictions

Restrictions 
This fix is part of the BPM package.  It is only enabled if LAMMPS was
built with that package.  See the Build package
page for more info.
This fix requires that atoms store torque, angular velocity (omega), a
radius, and a quaternion as defined by the atom_style bpm/sphere command.
All particles in the group must be finite-size spheres with
quaternions.  They cannot be point particles.
Use of the disc keyword is only allowed for 2d simulations, as
defined by the dimension keyword.

## Related Commands

- [fix nve](fix_nve.html)
- [fix nve/sphere](fix_nve_sphere.html)

