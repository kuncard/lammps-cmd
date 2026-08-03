---
id: fix_nonaffine_displacement
title: "fix nonaffine/displacement command"
url: https://docs.lammps.org/fix_nonaffine_displacement.html
---

# fix nonaffine/displacement command

## Syntax

```
fix ID group nonaffine/displacement nevery style args reference/style nstep keyword values
d2min args = cutoff args
  cutoff = type or radius or custom
    type args = none, cutoffs determined by atom types
    radius args = none, cutoffs determined based on atom diameters (atom style sphere)
    custom args = rmax, cutoff set by a constant numeric value rmax (distance units)
integrated args = none
fixed = use a fixed reference frame at nstep
update = update the reference frame every nstep timesteps
offset = update the reference frame nstep timesteps before calculating the nonaffine displacement
z/min values = zmin
  zmin = minimum coordination number to calculate D2min
intensive/d2min values = yes or no
  specifies whether output uses an intensive or extensive value of d2min
```

## Description

Added in version 7Feb2024.

This fix computes different metrics of the nonaffine displacement of
particles. The first metric, d2min calculates the \(D^2_\mathrm{min}\)
nonaffine displacement by Falk and Langer in (Falk).
For each atom, the fix computes the two tensors

\[X = \sum_{\mathrm{neighbors}} \vec{r} \left(\vec{r}_{0} \right)^T\]

and

\[Y = \sum_{\mathrm{neighbors}} \vec{r}_0 \left(\vec{r}_{0} \right)^T\]

where the neighbors include all other atoms within the distance criterion
set by the cutoff option, discussed below, \(\vec{r}\) is the current
displacement between particles, and \(\vec{r}_0\) is the reference
displacement. A deformation gradient tensor is then calculated as
\(F = X Y^{-1}\) from which

\[D^2_\mathrm{min} = \frac{1}{N_n} \sum_{\mathrm{neighbors}} \left| \vec{r} - F \vec{r}_0 \right|^2\]

and a strain tensor is calculated \(E = F F^{T} - I\) where \(I\)
is the identity tensor and \(N_n\) is the number of neighbors. This calculation is
only performed on timesteps that are a multiple of nevery (including timestep zero).
Data accessed before this occurs will simply be zeroed.

This formulation of D2min is intensive in the sense that it is normalized by the number
of neighbors that contribute to it. Alternatively, this factor can be removed using
the intensive/d2min option to calculate a quantity extensive in the number of
neighbors.

For particles with low coordination numbers, calculations of \(D^2_\mathrm{min}\)
may not be accurate. An optional minimum coordination number can be defined using
the z/min keyword. If any particle has fewer than the specified number of particles
in the cutoff distance or in contact, the above calculations will be skipped and the
corresponding peratom array entries will be zero.

The integrated style simply integrates the velocity of particles
every timestep to calculate a displacement. This style only works if
used in conjunction with another fix that deforms the box and displaces
atom positions such as fix deform with remap x,
fix press/berendsen, or fix nh.

Both of these methods require defining a reference state. With the fixed reference
style, the user picks a specific timestep nstep at which particle positions are saved.
If peratom data is accessed from this compute prior to this timestep, it will simply be
zeroed. The update reference style implies the reference state will be updated every
nstep timesteps. The offset reference will update the reference state nstep
timesteps before a multiple of nevery timesteps.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 1 all nonaffine/displacement 100 integrated update 100
fix 1 all nonaffine/displacement 1000 d2min type fixed 0
fix 1 all nonaffine/displacement 1000 d2min custom 2.0 offset 100 intensive/d2min no
```

## Restrictions

Restrictions 
This compute is part of the EXTRA-FIX package.  It is only enabled if
LAMMPS was built with that package.  See the
Build package page for more info.
As this fix depends on a run including specific reference timesteps, it
currently does not update peratom values if used in conjunction with the
rerun command since it cannot ensure the necessary reference
timesteps are included.

## Related Commands

Related commands 
none

