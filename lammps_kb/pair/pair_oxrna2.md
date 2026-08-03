---
id: pair_oxrna2
title: "pair_style oxrna2/excv command"
url: https://docs.lammps.org/pair_oxrna2.html
---

# pair_style oxrna2/excv command

## Syntax

```
pair_style style1

pair_coeff * * style2 args
oxrna2/stk args = seq T xi kappa 6.0 0.43 0.93 0.35 0.78 0.9 0 0.95 0.9 0 0.95 1.3 0 0.8 1.3 0 0.8 2.0 0.65 2.0 0.65
  seq = seqav (for average sequence stacking strength) or seqdep (for sequence-dependent stacking strength)
  T = temperature (LJ units: 0.1 = 300 K, real units: 300 = 300 K)
  xi = 1.40206 (LJ units) or 8.35864576375849 (real units), temperature-independent coefficient in stacking strength
  kappa = 2.77 (LJ units) or 0.005504556 (real units), coefficient of linear temperature dependence in stacking strength
oxrna2/hbond args = seq eps 8.0 0.4 0.75 0.34 0.7 1.5 0 0.7 1.5 0 0.7 1.5 0 0.7 0.46 3.141592653589793 0.7 4.0 1.5707963267948966 0.45 4.0 1.5707963267948966 0.45
  seq = seqav (for average sequence base-pairing strength) or seqdep (for sequence-dependent base-pairing strength)
  eps = 0.870439 (LJ units) or 5.18928666388042 (real units), average hydrogen bonding strength between A-U and C-G Watson-Crick and G-U wobble base pairs, 0 between all other pairs
oxrna2/dh args = T rhos qeff
  T = temperature (LJ units: 0.1 = 300 K, real units: 300 = 300 K)
  rhos = salt concentration (mole per litre)
  qeff = 1.02455 (effective charge in elementary charges)
```

## Description

The oxrna2 pair styles compute the pairwise-additive parts of the
oxDNA force field for coarse-grained modelling of RNA. The effective
interaction between the nucleotides consists of potentials for the
excluded volume interaction oxrna2/excv, the stacking oxrna2/stk,
cross-stacking oxrna2/xstk and coaxial stacking interaction
oxrna2/coaxstk, electrostatic Debye-Hueckel interaction oxrna2/dh as
well as the hydrogen-bonding interaction oxrna2/hbond between
complementary pairs of nucleotides on opposite strands. Average sequence
or sequence-dependent stacking and base-pairing strengths are supported
(Sulc2).

The exact functional form of the pair styles is rather complex.  The
individual potentials consist of products of modulation factors, which
themselves are constructed from a number of more basic potentials
(Morse, Lennard-Jones, harmonic angle and distance) as well as quadratic
smoothing and modulation terms.  We refer to (Sulc1) and
the original oxDNA publications (Ouldridge-DPhil) and (Ouldridge) for a detailed
description of the oxRNA2 force field.

Note
These pair styles have to be used together with the related oxDNA2
bond style oxrna2/fene for the connectivity of the phosphate
backbone (see also documentation of bond_style oxrna2/fene). Most of the coefficients in the above example have to
be kept fixed and cannot be changed without reparameterizing the
entire model.  Exceptions are the first two coefficients after
oxrna2/stk (seq=seqdep and T=0.1 and
corresponding real unit equivalents in the above examples), the
first coefficient after oxrna2/hbond (seq=seqdep in the above
example) and the two coefficients after oxrna2/dh (T=0.1 and
rhos=0.5 in the above example). When using a Langevin
thermostat e.g. through fix langevin or
fix nve/dotc/langevin the temperature
coefficients have to be matched to the one used in the fix.

Note
These pair styles have to be used with the atom_style hybrid bond
ellipsoid oxdna (see documentation of atom_style). The atom_style oxdna stores the 3 -to-5  polarity
of the nucleotide strand, which is set through the bond topology in
the data file. The first (second) atom in a bond definition is
understood to point towards the 3 -end (5 -end) of the strand.

Warning
If data files are produced with write_data, then
the newton command should be set to newton on.
Otherwise the data files will not have the same 3 -to-5  polarity
as the initial data file. This limitation does not apply to
binary restart files produced with write_restart.

Example input and data files for DNA duplexes can be found in
examples/PACKAGES/cgdna/examples/lj_units/oxRNA2/ or in the
corresponding folder for real units.
A simple python setup tool which creates single straight or helical
DNA strands, DNA duplexes or arrays of DNA duplexes can be found in
examples/PACKAGES/cgdna/util/.

Please cite (Henrich) in any publication that uses
this implementation.  The article contains general information on the
model, its implementation and performance as well as the structure of
the data and input file. The preprint version of the article can be
found here.  Please cite also the relevant oxRNA2
publications (Sulc1) and (Sulc2).

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
# LJ units
pair_style hybrid/overlay oxrna2/excv oxrna2/stk oxrna2/hbond oxrna2/xstk oxrna2/coaxstk oxrna2/dh
pair_coeff * * oxrna2/excv    2.0 0.7 0.675 2.0 0.515 0.5 2.0 0.33 0.32
pair_coeff * * oxrna2/stk     seqdep 0.1 1.40206 2.77 6.0 0.43 0.93 0.35 0.78 0.9 0 0.95 0.9 0 0.95 1.3 0 0.8 1.3 0 0.8 2.0 0.65 2.0 0.65
pair_coeff * * oxrna2/hbond   seqdep 0.0 8.0 0.4 0.75 0.34 0.7 1.5 0 0.7 1.5 0 0.7 1.5 0 0.7 0.46 3.141592653589793 0.7 4.0 1.5707963267948966 0.45 4.0 1.5707963267948966 0.45
pair_coeff 1 4 oxrna2/hbond   seqdep 0.870439 8.0 0.4 0.75 0.34 0.7 1.5 0 0.7 1.5 0 0.7 1.5 0 0.7 0.46 3.141592653589793 0.7 4.0 1.5707963267948966 0.45 4.0 1.5707963267948966 0.45
pair_coeff 2 3 oxrna2/hbond   seqdep 0.870439 8.0 0.4 0.75 0.34 0.7 1.5 0 0.7 1.5 0 0.7 1.5 0 0.7 0.46 3.141592653589793 0.7 4.0 1.5707963267948966 0.45 4.0 1.5707963267948966 0.45
pair_coeff 3 4 oxrna2/hbond   seqdep 0.870439 8.0 0.4 0.75 0.34 0.7 1.5 0 0.7 1.5 0 0.7 1.5 0 0.7 0.46 3.141592653589793 0.7 4.0 1.5707963267948966 0.45 4.0 1.5707963267948966 0.45
pair_coeff * * oxrna2/xstk    59.9626 0.5 0.6 0.42 0.58 2.25 0.505 0.58 1.7 1.266 0.68 1.7 1.266 0.68 1.7 0.309 0.68 1.7 0.309 0.68
pair_coeff * * oxrna2/coaxstk 80 0.5 0.6 0.42 0.58 2.0 2.592 0.65 1.3 0.151 0.8 0.9 0.685 0.95 0.9 0.685 0.95 2.0 -0.65 2.0 -0.65
pair_coeff * * oxrna2/dh      0.1 0.5 1.02455

pair_style hybrid/overlay oxrna2/excv oxrna2/stk oxrna2/hbond oxrna2/xstk oxrna2/coaxstk oxrna2/dh
pair_coeff * * oxrna2/excv    oxrna2_lj.cgdna
pair_coeff * * oxrna2/stk     seqdep 0.1 oxrna2_lj.cgdna
pair_coeff * * oxrna2/hbond   seqdep oxrna2_lj.cgdna
pair_coeff 1 4 oxrna2/hbond   seqdep oxrna2_lj.cgdna
pair_coeff 2 3 oxrna2/hbond   seqdep oxrna2_lj.cgdna
pair_coeff 3 4 oxrna2/hbond   seqdep oxrna2_lj.cgdna
pair_coeff * * oxrna2/xstk    oxrna2_lj.cgdna
pair_coeff * * oxrna2/coaxstk oxrna2_lj.cgdna
pair_coeff * * oxrna2/dh      0.1 0.5 oxrna2_lj.cgdna

# Real units
pair_style hybrid/overlay oxrna2/excv oxrna2/stk oxrna2/hbond oxrna2/xstk oxrna2/coaxstk oxrna2/dh
pair_coeff * * oxrna2/excv    11.92337812042065 5.9626 5.74965 11.92337812042065 4.38677 4.259 11.92337812042065 2.81094 2.72576
pair_coeff * * oxrna2/stk     seqdep 300.0 8.35864576375849 0.005504556 0.70439070204273 3.66274 7.92174 2.9813 6.64404 0.9 0.0 0.95 0.9 0.0 0.95 1.3 0.0 0.8 1.3 0.0 0.8 2.0 0.65 2.0 0.65
pair_coeff * * oxrna2/hbond   seqdep 0.0 0.93918760272364 3.4072 6.3885 2.89612 5.9626 1.5 0.0 0.7 1.5 0.0 0.7 1.5 0.0 0.7 0.46 3.141592653589793 0.7 4.0 1.5707963267948966 0.45 4.0 1.5707963267948966 0.45
pair_coeff 1 4 oxrna2/hbond   seqdep 5.18928666388042 0.93918760272364 3.4072 6.3885 2.89612 5.9626 1.5 0.0 0.7 1.5 0.0 0.7 1.5 0.0 0.7 0.46 3.141592653589793 0.7 4.0 1.5707963267948966 0.45 4.0 1.5707963267948966 0.45
pair_coeff 2 3 oxrna2/hbond   seqdep 5.18928666388042 0.93918760272364 3.4072 6.3885 2.89612 5.9626 1.5 0.0 0.7 1.5 0.0 0.7 1.5 0.0 0.7 0.46 3.141592653589793 0.7 4.0 1.5707963267948966 0.45 4.0 1.5707963267948966 0.45
pair_coeff 3 4 oxrna2/hbond   seqdep 5.18928666388042 0.93918760272364 3.4072 6.3885 2.89612 5.9626 1.5 0.0 0.7 1.5 0.0 0.7 1.5 0.0 0.7 0.46 3.141592653589793 0.7 4.0 1.5707963267948966 0.45 4.0 1.5707963267948966 0.45
pair_coeff * * oxrna2/xstk    4.92690859644113 4.259 5.1108 3.57756 4.94044 2.25 0.505 0.58 1.7 1.266 0.68 1.7 1.266 0.68 1.7 0.309 0.68 1.7 0.309 0.68
pair_coeff * * oxrna2/coaxstk 6.57330882442206 4.259 5.1108 3.57756 4.94044 2.0 2.592 0.65 1.3 0.151 0.8 0.9 0.685 0.95 0.9 0.685 0.95 2.0 -0.65 2.0 -0.65
pair_coeff * * oxrna2/dh      300.0 0.5 1.02455

pair_style hybrid/overlay oxrna2/excv oxrna2/stk oxrna2/hbond oxrna2/xstk oxrna2/coaxstk oxrna2/dh
pair_coeff * * oxrna2/excv    oxrna2_real.cgdna
pair_coeff * * oxrna2/stk     seqdep 300.0 oxrna2_real.cgdna
pair_coeff * * oxrna2/hbond   seqdep oxrna2_real.cgdna
pair_coeff 1 4 oxrna2/hbond   seqdep oxrna2_real.cgdna
pair_coeff 2 3 oxrna2/hbond   seqdep oxrna2_real.cgdna
pair_coeff 3 4 oxrna2/hbond   seqdep oxrna2_real.cgdna
pair_coeff * * oxrna2/xstk    oxrna2_real.cgdna
pair_coeff * * oxrna2/coaxstk oxrna2_real.cgdna
pair_coeff * * oxrna2/dh      300.0 0.5 oxrna2_real.cgdna
```

## Restrictions

Restrictions 
These pair styles can only be used if LAMMPS was built with the
CG-DNA package and the MOLECULE and ASPHERE package.  See the
Build package page for more info.

## Related Commands

- [bond_style oxrna2/fene](bond_oxdna.html)
- [pair_coeff](pair_coeff.html)
- [bond_style oxdna/fene](bond_oxdna.html)
- [pair_style oxdna/excv](pair_oxdna.html)
- [bond_style oxdna2/fene](bond_oxdna.html)
- [pair_style oxdna2/excv](pair_oxdna2.html)
- [atom_style oxdna](atom_style.html)
- [fix nve/dotc/langevin](fix_nve_dotc_langevin.html)

