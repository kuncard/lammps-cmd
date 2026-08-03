---
id: fix_reaxff_bonds
title: "fix reaxff/bonds command"
url: https://docs.lammps.org/fix_reaxff_bonds.html
---

# fix reaxff/bonds command

## Syntax

```
fix ID group-ID reaxff/bonds Nevery filename
```

## Description

Write out the bond information computed by the ReaxFF potential specified
by pair_style reaxff in the exact same format as the
original stand-alone ReaxFF code of Adri van Duin.  The bond information
is written to filename on timesteps that are multiples of Nevery,
including timestep 0.  For time-averaged chemical species analysis,
please see the fix reaxff/species command.

The specified group-ID is ignored by this fix except for the dump
image related functionality (see below).

The format of the output file should be reasonably self-explanatory.
The meaning of the column header abbreviations is as follows:

If the filename ends with  .gz  or some other supported
compression format suffix, the output file is written in
compressed format.  A compressed output file can be significantly
smaller than the text version, but will also take longer to write.

Added in version 2Apr2025.

If the filename contains the wildcard character  * , a new file is
created on every timestep where bond information is written.  The  * 
character is replaced with the timestep value.  Note that the
fix_modify pad command can be used so that all
timestep numbers have the same length by adding leading zeroes
(e.g. 00010 for a pad value of 5).  The default pad value is 0, i.e. no
leading zeroes.

Added in version 11Feb2026.

If the filename is  NULL , then no output is created.  This can be
useful when using fix reaxff/bonds in combination with dump
image fix keyword to visualize the bonds computed by
the ReaxFF force field.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 1 all reaxff/bonds 100 bonds.reaxff
```

## Restrictions

Restrictions 
The fix reaxff/bonds command requires that the pair_style reaxff is invoked.  This fix is part of the REAXFF package.  It
is only enabled if LAMMPS was built with that package.  See the
Build package page for more info.
To write compressed bond files, you must compile LAMMPS with the
-DLAMMPS_GZIP option.  See the Build settings
doc page for details.

## Related Commands

- [pair_style reaxff](pair_reaxff.html)
- [fix reaxff/species](fix_reaxff_species.html)

