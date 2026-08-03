---
id: dump_adios
title: "dump atom/adios  command"
url: https://docs.lammps.org/dump_adios.html
---

# dump atom/adios  command

## Syntax

```
dump ID group-ID atom/adios N file.bp
dump ID group-ID custom/adios N file.bp args
```

## Description

Dump a snapshot of atom coordinates every \(N\) timesteps in the ADIOS-based  BP  file format, or using different I/O solutions in
ADIOS, to a stream that can be read on-line by another program.
ADIOS-BP files are binary, portable, and self-describing.

Note
To be able to use ADIOS, a file adios2_config.xml with specific
configuration settings is expected in the current working directory.
If the file is not present, LAMMPS will try to create a minimal
default file.  Please refer to the ADIOS documentation for details on
how to adjust this file for optimal performance and desired features.

Use from write_dump:

It is possible to use these dump styles with the
write_dump command.  In this case, the sub-intervals
must not be set at all.  The write_dump command can be used to
create a new file at each individual dump.

dump 4     all atom/adios 100 dump.bp
write_dump all atom/adios singledump.bp

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
dump adios1 all atom/adios   100 atoms.bp
dump 4a     all custom/adios 100 dump_adios.bp id v_p x y z
dump 2 subgroup custom/adios 100 dump_adios.bp mass type xs ys zs vx vy vz
```

## Restrictions

Restrictions 
The number of atoms per snapshot can change with the adios style.
When using the ADIOS tool  bpls  to list the content of a .bp file,
bpls will print __ for the size of the output table indicating that
its size is changing every step.
The atom/adios and custom/adios dump styles are part of the ADIOS
package.  They are only enabled if LAMMPS was built with that package.
See the Build package page for more info.

## Related Commands

- [dump](dump.html)
- [dump_modify](dump_modify.html)
- [undump](undump.html)

