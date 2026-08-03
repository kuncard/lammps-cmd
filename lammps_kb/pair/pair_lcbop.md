---
id: pair_lcbop
title: "pair_style lcbop command"
url: https://docs.lammps.org/pair_lcbop.html
---

# pair_style lcbop command

## Syntax

```
pair_style lcbop
```

## Description

The lcbop pair style computes the long-range bond-order potential
for carbon (LCBOP) of (Los and Fasolino).  See section II in
that paper for the analytic equations associated with the potential.

Only a single pair_coeff command is used with the lcbop style which
specifies an LCBOP potential file with parameters for specific
elements.  These are mapped to LAMMPS atom types by specifying N
additional arguments after the filename in the pair_coeff command,
where N is the number of LAMMPS atom types:

See the pair_coeff page for alternate ways
to specify the path for the potential file.

As an example, if your LAMMPS simulation has 4 atom types and you want
the first 3 to be C you would use the following pair_coeff command:

pair_coeff * * C.lcbop C C C NULL

The first 2 arguments must be * * so as to span all LAMMPS atom types.
The first C argument maps LAMMPS atom type 1 to the C element in the
LCBOP file. If a mapping value is specified as NULL, the mapping is
not performed.  This can be used when a lcbop potential is used as
part of the hybrid pair style.  The NULL values are placeholders for
atom types that will be used with other potentials.

The parameters/coefficients for the LCBOP potential as applied to C
are listed in the C.lcbop file to agree with the original (Los and Fasolino) paper.  Thus the parameters are specific to this
potential and the way it was fit, so modifying the file should be done
carefully.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
pair_style lcbop
pair_coeff * * ../potentials/C.lcbop C
```

## Restrictions

Restrictions 
This pair style is part of the MANYBODY package.  It is only enabled
if LAMMPS was built with that package.
See the Build package page for more info.
This pair potential requires the newton setting to be
 on  for pair interactions.
The C.lcbop potential file provided with LAMMPS (see the potentials
directory) is parameterized for metal units.  You can use
the LCBOP potential with any LAMMPS units, but you would need to
create your own LCBOP potential file with coefficients listed in the
appropriate units if your simulation does not use  metal  units.

## Related Commands

- [pair_airebo](pair_airebo.html)
- [pair_coeff](pair_coeff.html)

