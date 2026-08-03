---
id: pair_oxdna3
title: "pair_style oxdna3/excv command"
url: https://docs.lammps.org/pair_oxdna3.html
---

# pair_style oxdna3/excv command

## Syntax

```
pair_style style1

pair_coeff * * style2 args (keyword value)
oxdna3/excv args = oxdna3_lj.cgdna or oxdna3_real.cgdna
oxdna3/stk args = T oxdna3_lj.cgdna or oxdna3_real.cgdna
  T = temperature (LJ units: 0.1 = 300 K, real units: 300 = 300 K)
oxdna3/hbond args = oxdna3_lj.cgdna or oxdna3_real.cgdna
oxdna3/xstk args = oxdna3_lj.cgdna or oxdna3_real.cgdna
oxdna3/coaxstk args = oxdna3_lj.cgdna or oxdna3_real.cgdna
oxdna3/dh args [keyword value] = T rhos oxdna3_lj.cgdna or oxdna3_real.cgdna [half_charged_ends no|yes]
  T = temperature (LJ units: 0.1 = 300 K, real units: 300 = 300 K)
  rhos = salt concentration (mole per litre)
  half_charged_ends yes = set half charge at terminal nucleotides
  half_charged_ends no  = set full charge at terminal nucleotides
```

## Description

Added in version 30Mar2026.

The oxdna3 pair styles compute the pairwise-additive parts of the
oxDNA force field for coarse-grained modelling of DNA. The effective
interaction between the nucleotides consists of potentials for the
excluded volume interaction oxdna3/excv, the stacking oxdna3/stk,
cross-stacking oxdna3/xstk and coaxial stacking interaction
oxdna3/coaxstk, electrostatic Debye-Hueckel interaction oxdna3/dh as
well as the hydrogen-bonding interaction oxdna3/hbond between
complementary pairs of nucleotides on opposite strands.

The exact functional form of the pair styles is rather complex.  The
individual potentials consist of products of modulation factors, which
themselves are constructed from a number of more basic potentials
(Morse, Lennard-Jones, harmonic angle and distance) as well as quadratic
smoothing and modulation terms.  We refer to (Bonato)
and the original oxDNA publications (Ouldridge-DPhil) and (Ouldridge)
for a detailed description of the oxDNA3 force field.

Note
These pair styles have to be used together with the related oxDNA3
bond style oxdna3/fene for the connectivity of the phosphate
backbone (see also documentation of bond_style oxdna3/fene). All coefficients in the above mentioned potential files
have to be kept fixed and cannot be changed without reparameterizing the
entire model.  The first coefficient after oxdna3/stk
(T=0.1 and corresponding real unit equivalents in the above examples)
and the two coefficients after oxdna3/dh (T=0.1 and rhos=0.2 in the
above example) have to be set to the temperature and salt concentration
of the system.
oxdna3/dh has the option to set half a charge at terminal nucleotides
(half_charged_ends yes) to aid coaxial stacking. When using a
Langevin thermostat e.g. through fix langevin or
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
examples/PACKAGES/cgdna/examples/lj_units/oxDNA3/ or in the
corresponding folder for real units.
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
pair_style hybrid/overlay oxdna3/excv oxdna3/stk oxdna3/hbond oxdna3/xstk oxdna3/coaxstk oxdna3/dh
pair_coeff * * oxdna3/excv     oxdna3_lj.cgdna
pair_coeff * * oxdna3/stk      0.1 oxdna3_lj.cgdna
pair_coeff * * oxdna3/hbond    oxdna3_lj.cgdna
pair_coeff 1 4 oxdna3/hbond    oxdna3_lj.cgdna
pair_coeff 2 3 oxdna3/hbond    oxdna3_lj.cgdna
pair_coeff * * oxdna3/xstk     oxdna3_lj.cgdna
pair_coeff * * oxdna3/coaxstk  oxdna3_lj.cgdna
pair_coeff * * oxdna3/dh       0.1 0.2 oxdna3_lj.cgdna

# Real units
pair_style hybrid/overlay oxdna3/excv oxdna3/stk oxdna3/hbond oxdna3/xstk oxdna3/coaxstk oxdna3/dh
pair_coeff * * oxdna3/excv     oxdna3_real.cgdna
pair_coeff * * oxdna3/stk      300.0 oxdna3_real.cgdna
pair_coeff * * oxdna3/hbond    oxdna3_real.cgdna
pair_coeff 1 4 oxdna3/hbond    oxdna3_real.cgdna
pair_coeff 2 3 oxdna3/hbond    oxdna3_real.cgdna
pair_coeff * * oxdna3/xstk     oxdna3_real.cgdna
pair_coeff * * oxdna3/coaxstk  oxdna3_real.cgdna
pair_coeff * * oxdna3/dh       300.0 0.2 oxdna3_real.cgdna
```

## Restrictions

Restrictions 
These pair styles can only be used if LAMMPS was built with the
CG-DNA package and the MOLECULE and ASPHERE package.  See the
Build package page for more info.

## Related Commands

- [bond_style oxdna3/fene](bond_oxdna.html)
- [bond_style oxdna/fene](bond_oxdna.html)
- [pair_style oxdna/excv](pair_oxdna.html)
- [bond_style oxdna2/fene](bond_oxdna.html)
- [pair_style oxdna2/excv](pair_oxdna2.html)
- [bond_style oxrna2/fene](bond_oxdna.html)
- [pair_style oxrna2/excv](pair_oxrna2.html)
- [pair_coeff](pair_coeff.html)
- [atom_style oxdna](atom_style.html)
- [fix nve/dotc/langevin](fix_nve_dotc_langevin.html)

