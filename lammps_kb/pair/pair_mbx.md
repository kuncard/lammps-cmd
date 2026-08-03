---
id: pair_mbx
title: "pair_style mbx command"
url: https://docs.lammps.org/pair_mbx.html
---

# pair_style mbx command

## Syntax

```
pair_style mbx cutoff
```

## Description

Added in version 11Feb2026.

The MBX (Many-Body eXpansion) software is a C++ library that provides
access to many-body energy (MB-nrg) potential energy functions, such as
the MB-pol water model.  Developed over the past decade, these potential
energy functions integrate physics-based and machine-learned many-body
terms trained on electronic structure data calculated at the  gold
standard  coupled-cluster level of theory. (Gupta)

This pair_style instructs LAMMPS to call the
MBX library in order to simulate
MB-nrg models such as MB-pol. The MBX library source code is available at
https://github.com/paesanilab/MBX.
MBX is heavily OpenMP parallelized (OMP), and the OMP_NUM_THREADS
environment variable should be properly set to the number of threads desired.
A detailed discussion of the code structure can be found in the
manuscript (Riera), while a detailed description of the
performance scaling can be found in the manuscript (Gupta).

The cutoff argument specifies the real-space cutoff for MBX in
Angstroms. This real-space cutoff is used for the dispersion interactions of the
MB-nrg monomers, as well as for the electrostatics of the entire system.
For periodic systems, a safe value for the real-space cutoff is 9.0 Angstroms,
and all classical interactions beyond this cutoff will then be handled via particle-mesh
Ewald (PME) within MBX. For non-periodic systems, the cutoff can be set to a
large value, such as 100.0 Angstroms, to ensure that all interactions are
captured in the real-space.

Warning
MBX must currently be used with processors mapping style xyz. If you
do not, MBX will throw the error:
[MBX] Inconsistent proc mapping: 'processors * * * map xyz' required for PME solver

For hybrid simulations involving MB-nrg and non-MB-nrg molecules in the
same simulation, one can use pair_style hybrid/overlay to combine the MB-nrg molecules with other pair styles,
such as lj/cut. This has been used to simulate
MB-pol water within host frameworks such as metal-organic
frameworks (MOFs) and carbon nanotubes (CNTs).
If using MBX in a hybrid simulation involving special_bonds,
(such as when using the CHARMM, Amber, OPLS, or ClayFF force fields etc.),
please see the warning below for more details about
using special_bonds with MBX dp1. See examples/PACKAGES/mbx for
a complete hybrid example.

If you have questions not answered by this documentation, please
reference the MBX website
mbxsimulations.com or reach out to the MBX team at
https://groups.google.com/g/mbx-users

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
pair_style      mbx 9.0
pair_coeff      * * 1 h2o 1 2 2 json mbx.json
compute         mbx all pair mbx

# For a system involving ch4 (atom types C=1, H=2) and
# water (atom types O=3, H=4)
pair_style      mbx 9.0
pair_coeff      * * 2 ch4 1 2 2 2 2 h2o 3 4 4 json mbx.json
compute         mbx all pair mbx

# For a system involving water (atom types O=12, H=13) in a hybrid simulation
pair_style      hybrid/overlay mbx 9.0 lj/cut 9.0 coul/exclude 9.0
pair_coeff      * * mbx 2 dp1 1*11 h2o 12 13 13 json mbx.json
pair_coeff      1*11 1*11 coul/exclude
compute         mbx all pair mbx

# For a system involving water (atom types O=12, H=13) in a hybrid simulation
# with special_bonds and coul/exclude to exclude 1-2, 1-3, and 1-4 electrostatics
# for the charmm framework
special_bonds   charmm
pair_style      hybrid/overlay mbx 9.0 lj/cut 9.0 coul/exclude 9.0
pair_coeff      * * mbx 2 dp1 1*11 h2o 12 13 13 json mbx.json
pair_coeff      1*11 1*11 coul/exclude
compute         mbx all pair mbx
```

## Restrictions

Restrictions 
This pair_style is part of the MBX package.  A pair style is only
enabled if LAMMPS was built with its corresponding package.
See the Build package page for more info.
MBX requires the FFTW3 library to be installed. This is needed
as part of the internal PME solver used for long-range electrostatics.
All electrostatic interactions are calculated internally in MBX.
Therefore one should never calculate coulombic interactions in
LAMMPS such as using coul/cut or coul/long when also using MBX.
See the warning above for more details.
MBX currently only supports processors mapping style xyz.
MBX is primarily tested to work with units real and atom_style full. If you encounter
issues with other unit or atom styles, please contact the MBX developers.

## Related Commands

- [pair hybrid/overlay](pair_hybrid.html)
- [pair coul/exclude](pair_coul.html)

