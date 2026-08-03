---
id: compute_vacf
title: "compute vacf command"
url: https://docs.lammps.org/compute_vacf.html
---

# compute vacf command

## Syntax

```
compute ID group-ID vacf
```

## Description

Define a computation that calculates the velocity auto-correlation
function (VACF), averaged over a group of atoms.  Each atom s
contribution to the VACF is its current velocity vector dotted into
its initial velocity vector at the time the compute was specified.

A vector of four quantities is calculated by this compute.  The first three
elements of the vector are \(v_x v_{x,0}\) (and similar for the
\(y\) and \(z\) components), summed and averaged over atoms in the
group, where \(v_x\) is the current \(x\)-component of the velocity of
the atom and \(v_{x,0}\) is the initial \(x\)-component of the velocity
of the atom.  The fourth element of the vector is the total VACF
(i.e., \((v_x v_{x,0} + v_y v_{y,0} + v_z v_{z,0})\)),
summed and averaged over atoms in the group.

The integral of the VACF versus time is proportional to the diffusion
coefficient of the diffusing atoms.  This can be computed in the
following manner, using the variable trap() function:

compute         2 all vacf
fix             5 all vector 1 c_2[4]
variable        diff equal dt*trap(f_5)
thermo_style    custom step v_diff

Note
If you want the quantities calculated by this compute to be
continuous when running from a restart file, then
you should use the same ID for this compute, as in the original run.
This is so that the fix this compute creates to store per-atom
quantities will also have the same ID, and thus be initialized
correctly with time=0 atom velocities from the restart file.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 all vacf
compute 1 upper vacf
```

## Restrictions

Restrictions 
none

## Related Commands

- [compute msd](compute_msd.html)
- [compute vacf/chunk](compute_vacf_chunk.html)

