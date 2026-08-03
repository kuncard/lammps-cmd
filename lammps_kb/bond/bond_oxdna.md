---
id: bond_oxdna
title: "bond_style oxdna/fene command"
url: https://docs.lammps.org/bond_oxdna.html
---

# bond_style oxdna/fene command

## Syntax

```
bond_style oxdna/fene

bond_style oxdna2/fene

bond_style oxdna3/fene

bond_style oxrna2/fene
```

## Description

The oxdna/fene, oxdna2/fene, oxdna3/fene and oxrna2/fene bond styles use the potential

\[E = - \frac{\epsilon}{2} \ln \left[ 1 - \left(\frac{r-r_0}{\Delta}\right)^2\right]\]

to define a modified finite extensible nonlinear elastic (FENE)
potential (Ouldridge) to model the connectivity of
the phosphate backbone in the oxDNA/oxRNA force field for coarse-grained
modelling of DNA/RNA.

The following coefficients must be defined for the bond type via the
bond_coeff command as given in the above example, or
in the data file or restart files read by the read_data or read_restart commands:

Note
The oxDNA bond style has to be used together with the corresponding
oxDNA pair styles for excluded volume interaction oxdna/excv ,
stacking oxdna/stk , cross-stacking oxdna/xstk and coaxial
stacking interaction oxdna/coaxstk as well as hydrogen-bonding
interaction oxdna/hbond (see also documentation of pair_style
oxdna/excv). For the oxDNA2 (Snodin)
bond style the analogous pair styles oxdna2/excv , oxdna2/stk ,
oxdna2/xstk , oxdna2/coaxstk , oxdna2/hbond and an additional
Debye-Hueckel pair style oxdna2/dh have to be defined. The same
applies to the oxDNA3 (Bonato)
and oxRNA2 (Sulc1) styles.

Note
This bond style has to be used with the atom_style hybrid bond
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

Example input and data files for DNA and RNA duplexes can be found in
examples/PACKAGES/cgdna/examples/lj_units/oxDNA/`, `.../oxDNA2/`, `.../oxDNA3/
and .../oxRNA2/ or in the corresponding folder for real units.
A simple python setup tool which creates single
straight or helical DNA strands, DNA/RNA duplexes or arrays of DNA/RNA
duplexes can be found in examples/PACKAGES/cgdna/util/.

Please cite (Henrich) in any publication that uses
this implementation. An updated documentation that contains general information
on the model, its implementation and performance as well as the structure of
the data and input file can be found here.

Please cite also the relevant oxDNA/oxRNA publications. These are
(Ouldridge) and
(Ouldridge-DPhil) for oxDNA,
(Snodin) for oxDNA2,
(Bonato) for oxDNA3,
(Sulc1) for oxRNA2
and for sequence-specific hydrogen-bonding and stacking interactions
(Sulc2).

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
# LJ units
bond_style oxdna/fene
bond_coeff * 2.0 0.25 0.7525

bond_style oxdna2/fene
bond_coeff * 2.0 0.25 0.7564

bond_style oxdna3/fene
bond_coeff * oxdna3_lj.cgdna

bond_style oxrna2/fene
bond_coeff * 2.0 0.25 0.76107

# Real units
bond_style oxdna/fene
bond_coeff * 11.92337812042065 2.1295 6.409795

bond_style oxdna2/fene
bond_coeff * 11.92337812042065 2.1295 6.4430152

bond_style oxdna3/fene
bond_coeff * oxdna3_real.cgdna

bond_style oxrna2/fene
bond_coeff * 11.92337812042065 2.1295 6.482800913
```

## Restrictions

Restrictions 
This bond style can only be used if LAMMPS was built with the
CG-DNA package and the MOLECULE and ASPHERE package.  See the
Build package page for more info.

## Related Commands

- [pair_style oxdna/excv](pair_oxdna.html)
- [pair_style oxdna2/excv](pair_oxdna2.html)
- [pair_style oxdna3/excv](pair_oxdna3.html)
- [pair_style oxrna2/excv](pair_oxrna2.html)
- [bond_coeff](bond_coeff.html)
- [atom_style oxdna](atom_style.html)
- [fix nve/dotc/langevin](fix_nve_dotc_langevin.html)

