---
id: pair_peri
title: "pair_style peri/pmb command"
url: https://docs.lammps.org/pair_peri.html
---

# pair_style peri/pmb command

## Syntax

```
pair_style style
```

## Description

The peridynamic pair styles implement material models that can be used
at the mesoscopic and macroscopic scales.  See this document for an overview of LAMMPS commands for
Peridynamics modeling.

Style peri/pmb implements the Peridynamic bond-based prototype
microelastic brittle (PMB) model.

Style peri/lps implements the Peridynamic state-based linear
peridynamic solid (LPS) model.

Style peri/ves implements the Peridynamic state-based linear
peridynamic viscoelastic solid (VES) model.

Style peri/eps implements the Peridynamic state-based elastic-plastic
solid (EPS) model.

The canonical papers on Peridynamics are (Silling 2000) and (Silling 2007).  The
implementation of Peridynamics in LAMMPS is described in (Parks).  Also see the Peridynamics Howto for more
details about its implementation.

The peridynamic VES and EPS models in PDLAMMPS were implemented by
R. Rahman and J. T. Foster at University of Texas at San Antonio.  The
original VES formulation is described in  (Mitchell2011)  and the
original EPS formulation is in  (Mitchell2011a) .  Additional PDF docs
that describe the VES and EPS implementations are include in the LAMMPS
distribution in doc/PDF/PDLammps_VES.pdf and
doc/PDF/PDLammps_EPS.pdf.  For questions
regarding the VES and EPS models in LAMMPS you can contact R. Rahman
(rezwanur.rahman at utsa.edu).

The following coefficients must be defined for each pair of atom types
via the pair_coeff command as in the examples above,
or in the data file or restart files read by the read_data or read_restart commands, or by
mixing as described below.

For the peri/pmb style:

C is the effectively a spring constant for Peridynamic bonds, the
horizon is a cutoff distance for truncating interactions, and s00 and
\(\alpha\) are used as a bond breaking criteria.  The units of c are
such that c/distance = stiffness/volume^2, where stiffness is
energy/distance^2 and volume is distance^3.  See the users guide for
more details.

For the peri/lps style:

K is the bulk modulus and G is the shear modulus.  The horizon is a
cutoff distance for truncating interactions, and s00 and \(\alpha\)
are used as a bond breaking criteria. See the users guide for more
details.

For the peri/ves style:

K is the bulk modulus and G is the shear modulus. The horizon is a
cutoff distance for truncating interactions, and s00 and \(\alpha\)
are used as a bond breaking criteria. m_lambdai and m_taubi are the
viscoelastic relaxation parameter and time constant,
respectively. m_lambdai varies within zero to one. For very small values
of m_lambdai the viscoelastic model responds very similar to a linear
elastic model. For details please see the description in
 (Mitchell2011) .

For the peri/eps style:

K is the bulk modulus and G is the shear modulus. The horizon is a
cutoff distance and s00 and \(\alpha\) are used as a bond breaking
criteria.  m_yield_stress is the yield stress of the material. For
details please see the description in  (Mitchell2011a) .

Changed in version 4Jul2026.

Note
Prior versions of LAMMPS, had an incorrect the plasticity model in style
peri/eps relative to the source report (Mitchell2011a).
These affected the evolution of the plastic deviatoric extension and caused
significant overshooting of the yield surface. These have since been corrected,
however, there is still no radial return rule to ensure the plastic deviatoric
extension does not leave the yield surface. This may cause some drift off the
surface during long simulations. This possibility for future improvement is
tracked as issue #5064.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
pair_style peri/pmb
pair_coeff * * 1.6863e22 0.0015001 0.0005 0.25

pair_style peri/lps
pair_coeff * * 14.9e9 14.9e9 0.0015001 0.0005 0.25

pair_style peri/ves
pair_coeff * * 14.9e9 14.9e9 0.0015001 0.0005 0.25 0.5 0.001

pair_style peri/eps
pair_coeff * * 14.9e9 14.9e9 0.0015001 0.0005 0.25 118.43
```

## Restrictions

Restrictions 
All of these styles are part of the PERI package. They are only enabled
if LAMMPS was built with that package.  See the Build package page for more info.

## Related Commands

- [pair_coeff](pair_coeff.html)

