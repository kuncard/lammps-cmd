---
id: fix_dpd_source
title: "fix edpd/source command"
url: https://docs.lammps.org/fix_dpd_source.html
---

# fix edpd/source command

## Syntax

```
fix ID group-ID edpd/source keyword values ...
fix ID group-ID tdpd/source cc_index keyword values ...
sphere args = cx cy cz radius source
  cx,cy,cz = x,y,z center of spherical domain (distance units)
  radius = radius of a spherical domain (distance units)
  source = heat source or concentration source (flux units, see below)
cuboid values = cx cy cz dLx dLy dLz source
  cx,cy,cz = x,y,z center of a cuboid domain (distance units)
  dLx,dLy,dLz = x,y,z side length of a cuboid domain (distance units)
  source = heat source or concentration source (flux units, see below)
region values = region-ID source
  region = ID of region for heat or concentration source
  source = heat source or concentration source (flux units, see below)
```

## Description

Fix edpd/source adds a heat source as an external heat flux to each
atom in a spherical or cuboid domain, where the source is in units
of energy/time.  Fix tdpd/source adds an external concentration
source of the chemical species specified by index as an external
concentration flux for each atom in a spherical or cuboid domain,
where the source is in units of mole/volume/time.

This command can be used to give an additional heat/concentration
source term to atoms in a simulation, such as for a simulation of a
heat conduction with a source term (see Fig.12 in (Li2014))
or diffusion with a source term (see Fig.1 in (Li2015)), as
an analog of a periodic Poiseuille flow problem.

Deprecated since version 15Jun2023: The sphere and cuboid keywords will be removed in a future version
of LAMMPS.  The same functionality and more can be achieved with a region.

If the sphere keyword is used, the cx, cy, cz, radius values define
a spherical domain to apply the source flux to.

If the cuboid keyword is used, the cx, cy, cz, dLx, dLy, dLz define
a cuboid domain to apply the source flux to.

If the region keyword is used, the region-ID selects which
region to apply the source flux to.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 1 all edpd/source sphere 0.0 0.0 0.0 5.0 0.01
fix 1 all edpd/source cuboid 0.0 0.0 0.0 20.0 10.0 10.0 -0.01
fix 1 all tdpd/source 1 sphere 5.0 0.0 0.0 5.0 0.01
fix 1 all tdpd/source 2 cuboid 0.0 0.0 0.0 20.0 10.0 10.0 0.01
fix 1 all tdpd/source 1 region lower -0.01
```

## Restrictions

Restrictions 
These fixes are part of the DPD-MESO package.  They are only enabled if
LAMMPS was built with that package.  See the Build package page for more info.
Fix edpd/source must be used with the pair_style edpd command.  Fix tdpd/source must be used with the
pair_style tdpd command.

## Related Commands

- [pair_style edpd](pair_mesodpd.html)
- [pair_style tdpd](pair_mesodpd.html)
- [compute edpd/temp/atom](compute_edpd_temp_atom.html)
- [compute tdpd/cc/atom](compute_tdpd_cc_atom.html)

