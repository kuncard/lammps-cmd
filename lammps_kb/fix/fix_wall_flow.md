---
id: fix_wall_flow
title: "fix wall/flow command"
url: https://docs.lammps.org/fix_wall_flow.html
---

# fix wall/flow command

## Syntax

```
fix ID group-ID wall/flow axis vflow T seed N coords ... keyword value
units value = lattice or box
  lattice = wall positions are defined in lattice units
  box = the wall positions are defined in simulation box units
```

## Description

Added in version 17Apr2024.

This fix implements flow boundary conditions (FBC) introduced in
(Pavlov1) and (Pavlov2).
The goal is to generate a stationary flow with a shifted Maxwell
velocity distribution:

\[f_a(v_a) \propto \exp{\left(-\frac{m (v_a-v_{\text{flow}})^2}{2 kB T}\right)}\]

where \(v_a\) is the component of velocity along the specified
axis argument (a = x,y,z), \(v_{\text{flow}}\) is the flow
velocity specified as the vflow argument, T is the specified flow
temperature, m is the particle mass, and kB is the Boltzmann
constant.

This is achieved by defining a series of N transparent walls along
the flow axis direction.  Each wall is at the specified position
listed in the coords argument.  Note that an additional transparent
wall is defined by the code at the boundary of the (periodic)
simulation domain in the axis direction.  So there are effectively
N+1 walls.

Each time a particle in the specified group passes through one of the
transparent walls, its velocity is re-assigned.  Particles not in the
group do not interact with the wall. This can be used, for example, to
add obstacles composed of atoms, or to simulate a solution of complex
molecules in a one-atom liquid (note that the fix has been tested for
one-atom systems only).

Conceptually, the velocity re-assignment represents creation of a new
particle within the system with simultaneous removal of the particle
which passed through the wall.  The velocity components in directions
parallel to the wall are re-assigned according to the standard Maxwell
velocity distribution for the specified temperature T.  The velocity
component perpendicular to the wall is re-assigned according to the
shifted Maxwell distribution defined above:

\[f_{\text{a generated}}(v_a) \propto v_a f_a(v_a)\]

It can be shown that for an ideal-gas scenario this procedure makes
the velocity distribution of particles between walls exactly as
desired.

Since in most cases simulated systems are not an ideal gas, multiple
walls can be defined, since a single wall may not be sufficient for
maintaining a stationary flow without  congestion  which can manifest
itself as regions in the flow with increased particle density located
upstream from static obstacles.

For the same reason, the actual temperature and velocity of the
generated flow may differ from what is requested.  The degree of
discrepancy is determined by how different from an ideal gas the
simulated system is.  Therefore, a calibration procedure may be
required for such a system as described in (Pavlov).

Note that the interactions between particles on different sides of a
transparent wall are not disabled or neglected.  Likewise particle
positions are not altered by the velocity reassignment.  This removes
the need to modify the force field to work correctly in cases when a
particle is close to a wall.

For example, if particle positions were uniformly redistributed across
the surface of a wall, two particles could end up too close to each
other, potentially causing the simulation to explode.  However due to
this compromise, some collective phenomena such as regions with
increased/decreased density or collective movements are not fully
removed when particles cross a wall.  This unwanted consequence can
also be potentially mitigated by using more multiple walls.

Note
When the specified flow has a high velocity, a lost atoms error can
occur (see error messages).  If this
happens, you should ensure the checks for neighbor list rebuilds,
set via the neigh_modify command, are as
conservative as possible (every timestep if needed).  Those are the
default settings.

Styles with a gpu, intel, kk, omp, or opt suffix are
functionally the same as the corresponding style without the suffix.
They have been optimized to run faster, depending on your available
hardware, as discussed on the Accelerator packages
page.  The accelerated styles take the same arguments and should
produce the same results, except for round-off and precision issues.

These accelerated styles are part of the GPU, INTEL, KOKKOS,
OPENMP, and OPT packages, respectively.  They are only enabled if
LAMMPS was built with those packages.  See the Build package page for more info.

You can specify the accelerated styles explicitly in your input script
by including their suffix, or you can use the -suffix command-line switch when you invoke LAMMPS, or you can use the
suffix command in your input script.

See the Accelerator packages page for more
instructions on how to use the accelerated styles effectively.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 1 all wall/flow x 0.4 1.5 593894 4 2.0 4.0 6.0 8.0
```

## Restrictions

Restrictions 
Fix wall_flow is part of the EXTRA-FIX package.  It is only enabled
if LAMMPS was built with that package.  See the Build package page for more info.
Flow boundary conditions should not be used with rigid bodies such as
those defined by a  fix rigid  command.
This fix can only be used with periodic boundary conditions along the
flow axis. The size of the box in this direction must not change. Also,
the fix is designed to work only in an orthogonal simulation box.

## Related Commands

- [fix wall/reflect](fix_wall.html)

