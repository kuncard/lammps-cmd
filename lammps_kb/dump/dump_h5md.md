---
id: dump_h5md
title: "dump h5md command"
url: https://docs.lammps.org/dump_h5md.html
---

# dump h5md command

## Syntax

```
dump ID group-ID h5md N file.h5 args
position options
image
velocity options
force options
species options
file_from ID = do not open a new file, re-use the already opened file from dump ID
box value = yes or no
create_group value = yes or no
author value = quoted string
options = every N_element
```

## Description

Dump a snapshot of atom coordinates every N timesteps in the
HDF5 based H5MD file format (de Buyl).
HDF5 files are binary, portable and self-describing.  This dump style
will write only one file, on the root node.

Several dumps may write to the same file, by using file_from and
referring to a previously defined dump.  Several groups may also be
stored within the same file by defining several dumps.  A dump that
refers (via file_from) to an already open dump ID and that concerns
another particle group must specify create_group yes.

Each data element is written every N*N_element steps. For image, no
sub-interval is needed as it must be present at the same interval as
position.  image must be given after position in any case.  The
box information (edges in each dimension) is stored at the same
interval than the position element, if present. Else it is stored
every N steps.

Note
Because periodic boundary conditions are enforced only on
timesteps when neighbor lists are rebuilt, the coordinates of an atom
written to a dump file may be slightly outside the simulation box.

Use from write_dump:

It is possible to use this dump style with the
write_dump command.  In this case, the sub-intervals
must not be set at all.  The write_dump command can be used either to
create a new file or to add current data to an existing dump file by
using the file_from keyword.

Typically, the species data is fixed. The following two commands
store the position data every 100 timesteps, with the image data, and
store once the species data in the same file.

dump h5md1 all h5md 100 dump.h5 position image
write_dump all h5md dump.h5 file_from h5md1 species

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
dump h5md1 all h5md 100 dump_h5md.h5 position image
dump h5md1 all h5md 100 dump_h5md.h5 position velocity every 10
dump h5md1 all h5md 100 dump_h5md.h5 velocity author "John Doe"
```

## Restrictions

Restrictions 
The number of atoms per snapshot cannot change with the h5md style.
The position data is stored wrapped (box boundaries not enforced, see
note above).  Only orthogonal domains are currently supported. This is
a limitation of the present dump h5md command and not of H5MD itself.
The h5md dump style is part of the H5MD package. It is only
enabled if LAMMPS was built with that package. See the Build package page for more info. It also requires
(i) building the ch5md library provided with LAMMPS (See the Build package page for more info.) and (ii) having
the HDF5 library installed (C bindings are sufficient) on
your system.  The library ch5md is compiled with the h5cc wrapper
provided by the HDF5 library.

## Related Commands

- [dump](dump.html)
- [dump_modify](dump_modify.html)
- [undump](undump.html)

