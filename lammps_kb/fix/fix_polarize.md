---
id: fix_polarize
title: "fix polarize/bem/gmres command"
url: https://docs.lammps.org/fix_polarize.html
---

# fix polarize/bem/gmres command

## Syntax

```
fix ID group-ID style nevery tolerance
```

## Description

These fixes compute induced charges at the interface between two
impermeable media with different dielectric constants. The interfaces
need to be discretized into vertices, each representing a boundary
element.  The vertices are treated as if they were regular atoms or
particles.  atom_style dielectric should be used
since it defines the additional properties of each interface particle
such as interface normal vectors, element areas, and local dielectric
mismatch.  These fixes also require the use of pair_style and kspace_style with the
dielectric suffix.  At every time step, given a configuration of the
physical charges in the system (such as atoms and charged particles)
these fixes compute and update the charge of the interface
particles. The interfaces are allowed to move during the simulation if
the appropriate time integrators are also set (for example, with
fix_rigid).

Consider an interface between two media: one with dielectric constant of
78 (water), the other of 4 (silica). The interface is discretized into
2000 boundary elements, each represented by an interface
particle. Suppose that each interface particle has a normal unit vector
pointing from the silica medium to water.  The dielectric difference
along the normal vector is then 78 - 4 = 74, the mean dielectric value
is (78 + 4) / 2 = 41. Each boundary element also has its area and the
local mean curvature, which is used by these fixes for computing a
correction term in the local electric field.  To model charged
interfaces, an interface particle will have a non-zero charge value,
coming from its area and surface charge density, and its local dielectric
constant set to the mean dielectric value.

For non-interface particles such as atoms and charged particles, the
interface normal vectors, element area, and dielectric mismatch are
irrelevant and unused. Their local dielectric value is used internally
to rescale their given charge when computing the Coulombic
interactions. For instance, to simulate a cation carrying a charge of +2
(in simulation charge units) in an implicit solvent with a dielectric
constant of 40, the cation s charge should be set to +2 and its local
dielectric constant property (defined in the atom_style dielectric) should be set to 40; there is no need to manually rescale
charge. This will produce the proper force for any pair_style with the dielectric suffix.  It is assumed that the
particles cannot pass through the interface during the simulation
because the value of the local dielectric constant property does not
change.

There are some example scripts for using these fixes with LAMMPS in the
examples/PACKAGES/dielectric directory. The README file therein
contains specific details on the system setup. Note that the example
data files show the additional fields (columns) needed for
atom_style dielectric beyond the conventional fields
id, mol, type, q, x, y, and z.

For fix polarize/bem/gmres and fix polarize/bem/icc the induced
charges of the atoms in the specified group, which are the vertices on
the interface, are computed using the equation:

\[\sigma_b(\mathbf{s}) = \dfrac{1 - \bar{\epsilon}}{\bar{\epsilon}}
   \sigma_f(\mathbf{s}) - \epsilon_0 \dfrac{\Delta \epsilon}{\bar{\epsilon}}
   \mathbf{E}(\mathbf{s}) \cdot \mathbf{n}(\mathbf{s})\]

Fix polarize/bem/gmres employs the Generalized Minimum Residual
(GMRES) as described in (Barros) to solve
\(\sigma_b\).

Fix polarize/bem/icc employs the successive over-relaxation algorithm
as described in (Tyagi) to solve \(\sigma_b\).

The iterative solvers would terminate either when the maximum relative
change in the induced charges in consecutive iterations is below the set
tolerance, or when the number of iterations reaches iter_max (see
below).

Fix polarize/functional employs the energy functional variation
approach as described in (Jadhao) to solve
\(\sigma_b\).

The induced charges computed by these fixes are stored in the q_scaled field,
and can be accessed as in the following example:

compute qs all property/atom q_scaled
dump 1 all custom 1000 all.txt id type q x y z c_qs

Note that the q field is the regular atom charges, which do not change
during the simulation. For interface particles, q_scaled is the sum
of the real charge, divided by the local dielectric constant epsilon,
and their induced charges. For non-interface particles, q_scaled is
the real charge, divided by the local dielectric constant epsilon.

More details on the implementation of these fixes and their recommended
use are described in (NguyenTD).

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 2 interface polarize/bem/gmres 5 0.0001
fix 1 interface polarize/bem/icc 1 0.0001
fix 3 interface polarize/functional 1 0.0001
```

```
examples/PACKAGES/dielectric/in.confined
examples/PACKAGES/dielectric/in.nopbc
```

## Restrictions

Restrictions 
These fixes are part of the DIELECTRIC package.  They are only enabled
if LAMMPS was built with that package, which requires that also the
KSPACE package is installed.  See the Build package page for more info.
Note that the polarize/bem/gmres and polarize/bem/icc fixes only
support units lj, real, metal, si and nano at
the moment.
Note that polarize/functional does not yet support charged interfaces.

## Related Commands

- [pair_coeff](pair_coeff.html)
- [fix polarize](#)
- [read_data](read_data.html)
- [pair_style lj/cut/coul/long/dielectric](pair_dielectric.html)
- [kspace_style pppm/dielectric](kspace_style.html)
- [compute efield/atom](compute_efield_atom.html)

