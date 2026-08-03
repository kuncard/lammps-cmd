---
id: compute_smd_contact_radius
title: "compute smd/contact/radius command"
url: https://docs.lammps.org/compute_smd_contact_radius.html
---

# compute smd/contact/radius command

## Syntax

```
compute ID group-ID smd/contact/radius
```

## Description

Define a computation which outputs the contact radius, i.e., the
radius used to prevent particles from penetrating each other.  The
contact radius is used only to prevent particles belonging to
different physical bodies from penetrating each other. It is used by
the contact pair styles, e.g., smd/hertz and smd/tri_surface.

See this PDF guide to using Smooth
Mach Dynamics in LAMMPS.

The value of the contact radius will be 0.0 for particles not in the
specified compute group.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 all smd/contact/radius
```

## Restrictions

Restrictions 
This compute is part of the MACHDYN package.  It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.

## Related Commands

- [dump custom](dump.html)

