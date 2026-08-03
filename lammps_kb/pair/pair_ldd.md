---
id: pair_ldd
title: "pair_style ldd command"
url: https://docs.lammps.org/pair_ldd.html
---

# pair_style ldd command

## Syntax

```
pair_style ldd
pair_coeff * * file.ldd S1 S2 ...
```

## Description

Added in version 4Jul2026.

Style ldd implements the local density potential as first described by
Pagonabarraga and Frenkel (Pagonabarraga) and
additionally the square gradient of local densities first introduced by
(DeLyser).  The pair_style ldd is compatible with a
variety of molecular and atomic topologies (see the Howto ldd page for details) and offers a variety of options for how to
define the local density.

Following the manybody potential convention (as for pair_style sw or tersoff), all interactions are read
from a potential file with a single pair_coeff * * command.  The file
defines a set of species; the arguments after the file name map each
LAMMPS atom type to one of these species (one species name per atom type,
in order).  Several atom types may map to the same species.  The set and
number of species are inferred from the file.  The cutoff of each
interaction is the rc of its indicator function; there is no separate
global cutoff.

Each line of the potential file specifies the interaction for one
ordered species pair Si Sj (the local density of species Sj
around a central atom of species Si), so the Si Sj and Sj Si
interactions can differ.  All \(N_{\text{species}}^2\) ordered pairs
must be listed (use the ignore keyword for pairs with no interaction).
Comment lines (starting with #) and the customary
# DATE: ... UNITS: ... CONTRIBUTOR: ... header are allowed.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
# two atom types mapped to species A and B
pair_style ldd
pair_coeff * * LDINDSET1.ldd A B

# combine local-density interactions with other pair styles
pair_style hybrid/overlay ldd lj/cut 14.0
pair_coeff 1 1 lj/cut 1.0 1.0
pair_coeff * * ldd ld_input_file.ldd A
```

```
Si Sj indicator wtype r0 rc self yes/no potential ptype args [gradient gtype args] [ignore]
```

## Restrictions

Restrictions 
This pair style is part of the BOCS package. It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.
This pair style requires newton on for pair interactions.
The pair_style ldd command must be issued after the simulation box
has been created (e.g. with read_data,
read_restart, or create_box),
because it sizes its per-type species map and inter-processor communication
buffers from the number of atom types.  Since ldd is a manybody-style
potential that does not read per-type Pair Coeffs from a data file,
there is no need to define it earlier.  When continuing from a binary
restart, re-specify pair_style ldd and its pair_coeff settings after
the read_restart command.
The indicator, self, and potential keywords are mandatory for each
species pair unless the ignore keyword is provided; the gradient
keyword is optional.  Every ordered species pair must appear exactly once
in the potential file.
Indicator styles with a non-zero \(r_0\) (sphere, shell,
smooth) are non-zero inside \(r_0\); lucy and dpd require
\(r_0 = 0\).

## Related Commands

- [pair_coeff](pair_coeff.html)
- [fix pair](fix_pair.html)
- [Howto ldd](Howto_ldd.html)

