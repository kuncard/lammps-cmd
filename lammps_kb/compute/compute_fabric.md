---
id: compute_fabric
title: "compute fabric command"
url: https://docs.lammps.org/compute_fabric.html
---

# compute fabric command

## Syntax

```
compute ID group-ID fabric cutoff attribute ... keyword values ...
type = cutoffs determined based on atom types
radius = cutoffs determined based on atom diameters (atom style sphere)
contact = contact tensor
branch = branch tensor
force/normal = normal force tensor
force/tangential = tangential force tensor
type/include value = arg1 arg2
  arg = separate lists of types (see below)
```

## Description

Define a compute that calculates various fabric tensors for pairwise
interaction (Ouadfel). Fabric tensors are commonly used
to quantify the anisotropy or orientation of granular contacts but can also
be used to characterize the direction of pairwise interactions in general
systems. The type and radius settings are used to select whether interactions
cutoffs are determined by atom types or by the sum of atomic radii (atom
style sphere), respectively. Calling this compute is roughly the cost of a
pair style invocation as it involves a loop over the neighbor list. If the
normal or tangential force tensors are requested, it will be more expensive
than a pair style invocation as it will also recalculate all pair forces.

Four fabric tensors are available: the contact, branch, normal force, or
tangential force tensor. The contact tensor is calculated as

\[C_{ab}  =  \frac{15}{2} (\phi_{ab} - \frac{1}{3} \mathrm{Tr}(\phi) \delta_{ab})\]

where \(a\) and \(b\) are the \(x\), \(y\), \(z\)
directions, \(\delta_{ab}\) is the Kronecker delta function, and
the tensor \(\phi\) is defined as

\[\phi_{ab}  =  \sum_{n = 1}^{N_p} \frac{r_{a} r_{b}}{r^2}\]

where \(n\) loops over the \(N_p\) pair interactions in the simulation,
\(r_{a}\) is the \(a\) component of the radial vector between the
two pairwise interacting particles, and \(r\) is the magnitude of the
radial vector.

The branch tensor is calculated as

\[B_{ab}  =  \frac{15}{2\, \mathrm{Tr}(D)} (D_{ab} - \frac{1}{3} \mathrm{Tr}(D) \delta_{ab})\]

where the tensor \(D\) is defined as

\[D_{ab}  =  \sum_{n = 1}^{N_p}
             \frac{1}{N_c (r^2 + C_{cd} r_c r_d)}
             \frac{r_{a} r_{b}}{r}\]

where \(N_c\) is the total number of contacts in the system and the
subscripts \(c\) and \(d\) indices are summed according to Einstein
notation.

The normal force fabric tensor is calculated as

\[F^n_{ab}  =  \frac{15}{2\, \mathrm{Tr}(N)} (N_{ab} - \frac{1}{3} \mathrm{Tr}(N) \delta_{ab})\]

where the tensor \(N\) is defined as

\[N_{ab}  =  \sum_{n = 1}^{N_p}
             \frac{1}{N_c (r^2 + C_{cd} r_c r_d)}
             \frac{r_{a} r_{b}}{r^2} f_n\]

and \(f_n\) is the magnitude of the normal, central-body force between the two atoms.

Finally, the tangential force fabric tensor is only defined for pair styles that
apply tangential forces to particles, namely granular pair styles. It is calculated
as

\[F^t_{ab}  =  \frac{5}{\mathrm{Tr}(N)} (T_{ab} - \frac{1}{3} \mathrm{Tr}(T) \delta_{ab})\]

where the tensor \(T\) is defined as

\[T_{ab}  =  \sum_{n = 1}^{N_p}
             \frac{1}{N_c (r^2 + C_{cd} r_c r_d)}
             \frac{r_{a} r_{b}}{r^2} f_t\]

and \(f_t\) is the magnitude of the tangential force between the two atoms.

The type/include keyword filters interactions based on the types of the two atoms.
Interactions between two atoms are only included in calculations if the atom types
are in the two lists. Each list consists of a series of type
ranges separated by commas. The range can be specified as a
single numeric value, or a wildcard asterisk can be used to specify a range
of values.  This takes the form  *  or  *n  or  m*  or  m*n .  For
example, if \(M\) is the number of atom types, then an asterisk with no
numeric values means all types from 1 to \(M\).  A leading asterisk means
all types from 1 to n (inclusive).  A trailing asterisk means all types from
m to \(M\) (inclusive).  A middle asterisk means all types from m to n
(inclusive).  Multiple type/include keywords may be added.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 all fabric type contact force/normal type/include 1,2 3*4
compute 1 all fabric radius force/normal force/tangential
```

## Restrictions

Restrictions 
This fix is part of the GRANULAR package.  It is only enabled if LAMMPS
was built with that package.  See the Build package
doc page for more info.
Currently, compute fabric does not support pair styles
with many-body interactions.  It also does not
support models with long-range Coulombic or dispersion forces,
i.e. the kspace_style command in LAMMPS.  It also does not support the
following fixes which add rigid-body constraints: fix shake, fix rattle, fix rigid, fix rigid/small. It does not support
granular pair styles that extend beyond the contact of atomic radii
(e.g., JKR and DMT).

## Related Commands

Related commands 
none

