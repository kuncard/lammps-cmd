---
id: read_data
title: "read_data command"
url: https://docs.lammps.org/read_data.html
---

# read_data command

## Syntax

```
read_data file keyword args ...
add arg = append or IDoffset or IDoffset MOLoffset or merge
  append = add new atoms with atom IDs appended to current IDs
  IDoffset = add new atoms with atom IDs having IDoffset added
  MOLoffset = add new atoms with molecule IDs having MOLoffset added (only when molecule IDs are enabled)
  merge = add new atoms with their atom IDs (and molecule IDs) unchanged
offset args = toff boff aoff doff ioff
  toff = offset to add to atom types
  boff = offset to add to bond types
  aoff = offset to add to angle types
  doff = offset to add to dihedral types
  ioff = offset to add to improper types
shift args = Sx Sy Sz
  Sx,Sy,Sz = distance to shift atoms when adding to system (distance units)
extra/atom/types arg = # of extra atom types
extra/bond/types arg = # of extra bond types
extra/angle/types arg = # of extra angle types
extra/dihedral/types arg = # of extra dihedral types
extra/improper/types arg = # of extra improper types
extra/bond/per/atom arg = leave space for this many new bonds per atom
extra/angle/per/atom arg = leave space for this many new angles per atom
extra/dihedral/per/atom arg = leave space for this many new dihedrals per atom
extra/improper/per/atom arg = leave space for this many new impropers per atom
extra/special/per/atom arg = leave space for extra 1-2,1-3,1-4 interactions per atom
group args = groupID
  groupID = add atoms in data file to this group
nocoeff = ignore force field parameters
fix args = fix-ID header-string section-string
  fix-ID = ID of fix to process header lines and sections of data file
  header-string = header lines containing this string will be passed to fix
  section-string = section names with this string will be passed to fix
```

## Description

Read in a data file containing information LAMMPS needs to run a
simulation.  The file can be ASCII text or a compressed text file
(detected by its suffix) if LAMMPS has been compiled with support
for compression commands.

This is one of 3 ways to specify the simulation box: see the
create_box and read_restart
and commands for alternative methods.  It is also one of 3 ways to
specify initial atom coordinates: see the create_atoms and read_restart and commands
for alternative methods.  Also see the explanation of the
-restart command-line switch which can convert a
restart file to a data file.

This command can be used multiple times to add new atoms and their
properties to an existing system by using the add, offset, and
shift keywords.  However, it is important to understand that several
system parameters, like the number of types of different kinds and per
atom settings are locked in after the first read_data command,
which means that no type ID (including its offset) may have a larger
value when processing additional data files than what is set by the
first data file and the corresponding read_data command options.  See
more details on this situation below, which includes the use case for
the extra keywords.

The group keyword adds all the atoms in the data file to the
specified group-ID.  The group will be created if it does not already
exist.  This is useful if you are reading multiple data files and wish
to put sets of atoms into different groups so they can be operated on
later.  E.g. a group of added atoms can be moved to new positions via
the displace_atoms command.  Note that atoms
read from the data file are also always added to the  all  group.  The
group command discusses atom groups, as used in LAMMPS.

The nocoeff keyword tells read_data to ignore force field parameters.
The various Coeff sections are still read and have to have the correct
number of lines, but they are not applied. This also allows to read a
data file without having any pair, bond, angle, dihedral or improper
styles defined, or to read a data file for a different force field.

The use of the fix keyword is discussed below.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
read_data data.lj
read_data ../run7/data.polymer.gz
read_data data.protein fix mycmap crossterm CMAP
read_data data.water add append offset 3 1 1 1 1 shift 0.0 0.0 50.0
read_data data.water add merge group solvent
```

## Restrictions

Restrictions 
To read compressed data files, you must compile LAMMPS with the
-DLAMMPS_GZIP option.  See the Build settings
doc page for details.
Label maps are currently not supported when using the KOKKOS package.

## Related Commands

- [read_dump](read_dump.html)
- [read_restart](read_restart.html)
- [create_atoms](create_atoms.html)
- [write_data](write_data.html)
- [labelmap](labelmap.html)

