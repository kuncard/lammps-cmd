---
id: compute_smd_tlsph_shape
title: "compute smd/tlsph/shape command"
url: https://docs.lammps.org/compute_smd_tlsph_shape.html
---

# compute smd/tlsph/shape command

## Syntax

```
compute ID group-ID smd/tlsph/shape
```

## Description

Define a computation that outputs the current shape of the volume
associated with a particle as a rotated ellipsoid.  It is only
meaningful for particles which interact according to the
Total-Lagrangian SPH pair style.

See this PDF guide to use Smooth
Mach Dynamics in LAMMPS.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 all smd/tlsph/shape
```

## Restrictions

Restrictions 
This compute is part of the MACHDYN package.  It is only enabled if
LAMMPS was built with that package. See the Build package page for more info.
This quantity will be computed only for particles which interact with
the Total-Lagrangian SPH pair style.

## Related Commands

- [smd/contact/radius](compute_smd_contact_radius.html)

