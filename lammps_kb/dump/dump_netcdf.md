---
id: dump_netcdf
title: "dump netcdf command"
url: https://docs.lammps.org/dump_netcdf.html
---

# dump netcdf command

## Syntax

```
dump ID group-ID netcdf N file args
dump ID group-ID netcdf/mpiio N file args
```

## Description

Dump a snapshot of atom coordinates every N timesteps in AMBER-style
NetCDF file format.  NetCDF files are binary, portable and
self-describing.  This dump style will write only one file on the root
node.  The dump style netcdf uses the standard NetCDF library.  All data is collected on one processor and then
written to the dump file.  Dump style netcdf/mpiio uses the
parallel NetCDF library and MPI-IO to write to the dump
file in parallel; it has better performance on a larger number of
processors.  Note that style netcdf outputs all atoms sorted by atom
tag while style netcdf/mpiio outputs atoms in order of their MPI
rank.

NetCDF files can be directly visualized via the following tools:

In addition to per-atom data, thermo data can be included in the
dump file. The data included in the dump file is identical to the data specified
by thermo_style.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
dump 1 all netcdf 100 traj.nc type x y z vx vy vz
dump_modify 1 append yes at -1 thermo yes
dump 1 all netcdf/mpiio 1000 traj.nc id type x y z
dump 1 all netcdf 1000 traj.*.nc id type x y z
```

## Restrictions

Restrictions 
The netcdf and netcdf/mpiio dump styles are part of the
NETCDF package.  They are only enabled if LAMMPS was built with
that package. See the Build package page for
more info.
The netcdf and netcdf/mpiio dump styles currently cannot dump
string properties or properties from variables.

## Related Commands

- [dump](dump.html)
- [dump_modify](dump_modify.html)
- [undump](undump.html)

