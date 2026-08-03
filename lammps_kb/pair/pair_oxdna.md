---
id: pair_oxdna
title: "pair_style oxdna/excv command"
url: https://docs.lammps.org/pair_oxdna.html
---

# pair_style oxdna/excv command

## Syntax

```
pair_style style1

pair_coeff * * style2 args
oxdna/stk args = seq T xi kappa 6.0 0.4 0.9 0.32 0.75 1.3 0 0.8 0.9 0 0.95 0.9 0 0.95 2.0 0.65 2.0 0.65
  seq = seqav (for average sequence stacking strength) or seqdep (for sequence-dependent stacking strength)
  T = temperature (LJ units: 0.1 = 300 K, real units: 300 = 300 K)
  xi = 1.3448 (LJ units) or 8.01727944817084 (real units), temperature-independent coefficient in stacking strength
  kappa = 2.6568 (LJ units) or 0.005279604 (real units), coefficient of linear temperature dependence in stacking strength
oxdna/hbond args = seq eps 8.0 0.4 0.75 0.34 0.7 1.5 0 0.7 1.5 0 0.7 1.5 0 0.7 0.46 3.141592653589793 0.7 4.0 1.5707963267948966 0.45 4.0 1.5707963267948966 0.45
  seq = seqav (for average sequence base-pairing strength) or seqdep (for sequence-dependent base-pairing strength)
  eps = 1.077 (LJ units) or 6.42073911784652 (real units), average hydrogen bonding strength between A-T and C-G Watson-Crick base pairs, 0 between all other pairs
```

## Description

The oxdna pair styles compute the pairwise-additive parts of the oxDNA
force field for coarse-grained modelling of DNA. The effective
interaction between the nucleotides consists of potentials for the
excluded volume interaction oxdna/excv, the stacking oxdna/stk,
cross-stacking oxdna/xstk and coaxial stacking interaction
oxdna/coaxstk as well as the hydrogen-bonding interaction
oxdna/hbond between complementary pairs of nucleotides on opposite
strands. Average sequence or sequence-dependent stacking and
base-pairing strengths are supported (Sulc).

The exact functional form of the pair styles is rather complex.  The
individual potentials consist of products of modulation factors, which
themselves are constructed from a number of more basic potentials
(Morse, Lennard-Jones, harmonic angle and distance) as well as quadratic
smoothing and modulation terms.  We refer to (Ouldridge-DPhil) and (Ouldridge) for a detailed
description of the oxDNA force field.

Note
These pair styles have to be used together with the related oxDNA
bond style oxdna/fene for the connectivity of the phosphate
backbone (see also documentation of bond_style oxdna/fene). Most of the coefficients in the above example have to
be kept fixed and cannot be changed without reparameterizing the
entire model.  Exceptions are the first two coefficients after
oxdna/stk (seq=seqdep and T=0.1 and
corresponding real unit equivalents in the above examples) and the
first coefficient after oxdna/hbond (seq=seqdep in the above
example).  When using a Langevin thermostat, e.g. through fix
langevin or fix nve/dotc/langevin the temperature coefficients have to be
matched to the one used in the fix.

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
examples/PACKAGES/cgdna/examples/lj_units/oxDNA/
or in the corresponding folder for real units.
A simple python setup tool which creates single straight or helical DNA
strands, DNA duplexes or arrays of DNA duplexes can be found in
examples/PACKAGES/cgdna/util/.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
# LJ units
pair_style hybrid/overlay oxdna/excv oxdna/stk oxdna/hbond oxdna/xstk oxdna/coaxstk
pair_coeff * * oxdna/excv    2.0 0.7 0.675 2.0 0.515 0.5 2.0 0.33 0.32
pair_coeff * * oxdna/stk     seqdep 0.1 1.3448 2.6568 6.0 0.4 0.9 0.32 0.75 1.3 0 0.8 0.9 0 0.95 0.9 0 0.95 2.0 0.65 2.0 0.65
pair_coeff * * oxdna/hbond   seqdep 0.0 8.0 0.4 0.75 0.34 0.7 1.5 0 0.7 1.5 0 0.7 1.5 0 0.7 0.46 3.141592653589793 0.7 4.0 1.5707963267948966 0.45 4.0 1.5707963267948966 0.45
pair_coeff 1 4 oxdna/hbond   seqdep 1.077 8.0 0.4 0.75 0.34 0.7 1.5 0 0.7 1.5 0 0.7 1.5 0 0.7 0.46 3.141592653589793 0.7 4.0 1.5707963267948966 0.45 4.0 1.5707963267948966 0.45
pair_coeff 2 3 oxdna/hbond   seqdep 1.077 8.0 0.4 0.75 0.34 0.7 1.5 0 0.7 1.5 0 0.7 1.5 0 0.7 0.46 3.141592653589793 0.7 4.0 1.5707963267948966 0.45 4.0 1.5707963267948966 0.45
pair_coeff * * oxdna/xstk    47.5 0.575 0.675 0.495 0.655 2.25 0.791592653589793 0.58 1.7 1.0 0.68 1.7 1.0 0.68 1.5 0 0.65 1.7 0.875 0.68 1.7 0.875 0.68
pair_coeff * * oxdna/coaxstk 46.0 0.4 0.6 0.22 0.58 2.0 2.541592653589793 0.65 1.3 0 0.8 0.9 0 0.95 0.9 0 0.95 2.0 -0.65 2.0 -0.65

pair_style hybrid/overlay oxdna/excv oxdna/stk oxdna/hbond oxdna/xstk oxdna/coaxstk
pair_coeff * * oxdna/excv    oxdna_lj.cgdna
pair_coeff * * oxdna/stk     seqav 0.1 oxdna_lj.cgdna
pair_coeff * * oxdna/hbond   seqav oxdna_lj.cgdna
pair_coeff 1 4 oxdna/hbond   seqav oxdna_lj.cgdna
pair_coeff 2 3 oxdna/hbond   seqav oxdna_lj.cgdna
pair_coeff * * oxdna/xstk    oxdna_lj.cgdna
pair_coeff * * oxdna/coaxstk oxdna_lj.cgdna

# Real units
pair_style hybrid/overlay oxdna/excv oxdna/stk oxdna/hbond oxdna/xstk oxdna/coaxstk
pair_coeff * * oxdna/excv    11.92337812042065 5.9626 5.74965 11.92337812042065 4.38677 4.259 11.92337812042065 2.81094 2.72576
pair_coeff * * oxdna/stk     seqdep 300.0 8.01727944817084 0.005279604 0.70439070204273 3.4072 7.6662 2.72576 6.3885 1.3 0.0 0.8 0.9 0.0 0.95 0.9 0.0 0.95 2.0 0.65 2.0 0.65
pair_coeff * * oxdna/hbond   seqdep 0.0 0.93918760272364 3.4072 6.3885 2.89612 5.9626 1.5 0.0 0.7 1.5 0.0 0.7 1.5 0.0 0.7 0.46 3.141592654 0.7 4.0 1.570796327 0.45 4.0 1.570796327 0.45
pair_coeff 1 4 oxdna/hbond   seqdep 6.42073911784652 0.93918760272364 3.4072 6.3885 2.89612 5.9626 1.5 0.0 0.7 1.5 0.0 0.7 1.5 0.0 0.7 0.46 3.141592654 0.7 4.0 1.570796327 0.45 4.0 1.570796327 0.45
pair_coeff 2 3 oxdna/hbond   seqdep 6.42073911784652 0.93918760272364 3.4072 6.3885 2.89612 5.9626 1.5 0.0 0.7 1.5 0.0 0.7 1.5 0.0 0.7 0.46 3.141592654 0.7 4.0 1.570796327 0.45 4.0 1.570796327 0.45
pair_coeff * * oxdna/xstk    3.9029021145006 4.89785 5.74965 4.21641 5.57929 2.25 0.791592654 0.58 1.7 1.0 0.68 1.7 1.0 0.68 1.5 0.0 0.65 1.7 0.875 0.68 1.7 0.875 0.68
pair_coeff * * oxdna/coaxstk 3.77965257404268 3.4072 5.1108 1.87396 4.94044 2.0 2.541592654 0.65 1.3 0.0 0.8 0.9 0.0 0.95 0.9 0.0 0.95 2.0 -0.65 2.0 -0.65

pair_style hybrid/overlay oxdna/excv oxdna/stk oxdna/hbond oxdna/xstk oxdna/coaxstk
pair_coeff * * oxdna/excv    oxdna_real.cgdna
pair_coeff * * oxdna/stk     seqav 300.0 oxdna_real.cgdna
pair_coeff * * oxdna/hbond   seqav oxdna_real.cgdna
pair_coeff 1 4 oxdna/hbond   seqav oxdna_real.cgdna
pair_coeff 2 3 oxdna/hbond   seqav oxdna_real.cgdna
pair_coeff * * oxdna/xstk    oxdna_real.cgdna
pair_coeff * * oxdna/coaxstk oxdna_real.cgdna
```

## Restrictions

Restrictions 
These pair styles can only be used if LAMMPS was built with the
CG-DNA package and the MOLECULE and ASPHERE package.  See the
Build package page for more info.

## Related Commands

- [bond_style oxdna/fene](bond_oxdna.html)
- [pair_coeff](pair_coeff.html)
- [bond_style oxdna2/fene](bond_oxdna.html)
- [pair_style oxdna2/excv](pair_oxdna2.html)
- [bond_style oxrna2/fene](bond_oxdna.html)
- [pair_style oxrna2/excv](pair_oxrna2.html)
- [atom_style oxdna](atom_style.html)
- [fix nve/dotc/langevin](fix_nve_dotc_langevin.html)

