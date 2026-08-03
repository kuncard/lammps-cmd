---
id: fix_nh_uef
title: "fix nvt/uef command"
url: https://docs.lammps.org/fix_nh_uef.html
---

# fix nvt/uef command

## Syntax

```
fix ID group-ID style_name erate edot_x edot_y temp Tstart Tstop Tdamp keyword value ...
keyword = erate or ext or strain or temp or iso or x or y or z or tchain or pchain or tloop or ploop or mtk
  erate values = e_x e_y = true strain rates (required)
  ext value = x or y or z or xy or yz or xz = external dimensions
    sets the external dimensions used to calculate the scalar pressure
  strain values = e_x e_y = initial strain
    usually not needed, but may be needed to resume a run with a data file.
  temp, iso, x, y, z, tchain, pchain, tloop, ploop, mtk
    keywords documented by the fix npt command
```

## Description

These fixes can be used to simulate non-equilibrium molecular dynamics
(NEMD) under diagonal flow fields, including uniaxial and bi-axial flow.
Simulations under continuous extensional flow may be carried out for an
indefinite amount of time.  It is an implementation of the boundary
conditions from (Dobson), and also uses numerical
lattice reduction as was proposed by (Hunt). The lattice
reduction algorithm is from (Semaev). The fix is
intended for simulations of homogeneous flows, and integrates the SLLOD
equations of motion, originally proposed by Hoover and Ladd (see
(Evans and Morriss)).  Additional detail about this
implementation can be found in (Nicholson and Rutledge).

Note that NEMD simulations of a continuously strained system can be
performed using the fix deform, fix nvt/sllod, and compute temp/deform
commands.

The applied flow field is set by the erate keyword. The values
edot_x and edot_y correspond to the strain rates in the xx and yy
directions.  It is implicitly assumed that the flow field is
traceless, and therefore the strain rate in the zz direction is eqal
to -(edot_x + edot_y).

Note
Due to an instability in the SLLOD equations under extension,
fix momentum should be used to regularly reset the
linear momentum.

The boundary conditions require a simulation box that does not have a
consistent alignment relative to the applied flow field. Since LAMMPS
utilizes an upper-triangular simulation box, it is not possible to
express the evolving simulation box in the same coordinate system as the
flow field.  These fixes keep track of two coordinate systems: the flow
frame, and the upper triangular LAMMPS frame. The coordinate systems are
related to each other through the QR decomposition, as is illustrated in
the image below.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix uniax_nvt all nvt/uef temp 400 400 100 erate 0.00001 -0.000005
fix biax_nvt all nvt/uef temp 400 400 100 erate 0.000005 0.000005
fix uniax_npt all npt/uef temp 400 400 300 iso 1 1 3000 erate 0.00001 -0.000005 ext yz
fix biax_npt all npt/uef temp 400 400 100 erate -0.00001 0.000005 x 1 1 3000
```

## Restrictions

Restrictions 
These fixes are part of the UEF package. They are only enabled if LAMMPS
was built with that package. See the Build package page for more info.
Due to requirements of the boundary conditions, when the strain
keyword is set to zero (or unset), the initial simulation box must be
cubic and have style triclinic. If the box is initially of type ortho,
use change_box before invoking the fix.

## Related Commands

- [fix nvt](fix_nh.html)
- [fix npt](fix_nh.html)
- [fix nvt/sllod](fix_nvt_sllod.html)
- [compute temp/uef](compute_temp_uef.html)
- [compute pressure/uef](compute_pressure_uef.html)
- [dump cfg/uef](dump_cfg_uef.html)

