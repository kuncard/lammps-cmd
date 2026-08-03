---
id: pair_quip
title: "pair_style quip command"
url: https://docs.lammps.org/pair_quip.html
---

# pair_style quip command

## Syntax

```
pair_style quip
```

## Description

Style quip provides an interface for calling potential routines from
the QUIP package. QUIP is built separately, and then linked to
LAMMPS. The most recent version of the QUIP package can be downloaded
from GitHub:
https://github.com/libAtoms/QUIP. The
interface is chiefly intended to be used to run Gaussian Approximation
Potentials (GAP), which are described in the following publications:
(Bartok et al) and (PhD thesis of Bartok).

Only a single pair_coeff command is used with the quip style that
specifies a QUIP potential file containing the parameters of the
potential for all needed elements in XML format. This is followed by a
QUIP initialization string. Finally, the QUIP elements are mapped to
LAMMPS atom types by specifying N atomic numbers, where N is the
number of LAMMPS atom types:

See the pair_coeff page for alternate ways
to specify the path for the potential file.

A QUIP potential is fully specified by the filename which contains the
parameters of the potential in XML format, the initialization string,
and the map of atomic numbers.

GAP potentials can be obtained from the GAP models and databases page
on the libAtoms homepage `https://libatoms.github.io, where the appropriate
initialization strings are also advised. The list of atomic numbers must
be matched to the LAMMPS atom types specified in the LAMMPS data file or
elsewhere.

Two examples input scripts are provided in the examples/PACKAGES/quip
directory.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
pair_style      quip
pair_coeff      * * gap_example.xml "Potential xml_label=GAP_2014_5_8_60_17_10_38_466" 14
pair_coeff      * * sw_example.xml "IP SW" 14
```

## Restrictions

Restrictions 
This pair style is part of the ML-QUIP package.  It is only enabled
if LAMMPS was built with that package.  See the Build package page for more info.
QUIP potentials are parameterized in electron-volts and Angstroms and
therefore should be used with LAMMPS metal units.
QUIP potentials are generally not designed to work with the scaling
factors set by the special_bonds command.  The
recommended setting in molecular systems is to include all
interactions, i.e. to use special_bonds lj/coul 1.0 1.0 1.0. Scaling
factors > 0.0 will be ignored and treated as 1.0. The only exception
to this rule is if you know that your QUIP potential needs to exclude
bonded, 1-3, or 1-4 interactions and does not already do this exclusion
within QUIP. Then a factor 0.0 needs to be used which will remove such
pairs from the neighbor list. This needs to be very carefully tested,
because it may remove pairs from the neighbor list that are still
required.

## Related Commands

- [pair_coeff](pair_coeff.html)

