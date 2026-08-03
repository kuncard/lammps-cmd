---
id: fix_plumed
title: "fix plumed command"
url: https://docs.lammps.org/fix_plumed.html
---

# fix plumed command

## Syntax

```
fix ID group-ID plumed keyword value ...
plumedfile arg = name of PLUMED input file to use (default: NULL)
outfile arg = name of file on which to write the PLUMED log (default: NULL)
```

## Description

This fix instructs LAMMPS to call the PLUMED library, which
allows one to perform various forms of trajectory analysis on the fly
and to also use methods such as umbrella sampling and metadynamics to
enhance the sampling of phase space.

The documentation included here only describes the fix plumed command
itself.  This command is LAMMPS specific, whereas most of the
functionality implemented in PLUMED will work with a range of MD codes,
and when PLUMED is used as a stand alone code for analysis.  The full
documentation for PLUMED is available online and included
in the PLUMED source code.  The PLUMED library development is hosted at
https://github.com/plumed/plumed2
A detailed discussion of the code can be found in (Tribello).

There is an example input for using this package with LAMMPS in the
examples/PACKAGES/plumed directory.

The command to make LAMMPS call PLUMED during a run requires two keyword
value pairs pointing to the PLUMED input file and an output file for the
PLUMED log. The user must specify these arguments every time PLUMED is
to be used.  Furthermore, the fix plumed command should appear in the
LAMMPS input file after relevant input parameters (e.g. the timestep)
have been set.

The group-ID entry is ignored. LAMMPS will always pass all the atoms
to PLUMED and there can only be one instance of the plumed fix at a
time. The way the plumed fix is implemented ensures that the minimum
amount of information required is communicated.  Furthermore, PLUMED
supports multiple, completely independent collective variables, multiple
independent biases and multiple independent forms of analysis.  There is
thus really no restriction in functionality by only allowing only one
plumed fix in the LAMMPS input.

The plumedfile keyword allows the user to specify the name of the
PLUMED input file.  Instructions as to what should be included in a
plumed input file can be found in the documentation for PLUMED

The outfile keyword allows the user to specify the name of a file in
which to output the PLUMED log.  This log file normally just repeats the
information that is contained in the input file to confirm it was
correctly read and parsed.  The names of the files in which the results
are stored from the various analysis options performed by PLUMED will
be specified by the user in the PLUMED input file.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix pl all plumed plumedfile plumed.dat outfile p.log
```

## Restrictions

Restrictions 
This fix is part of the PLUMED package.  It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.
There can only be one fix plumed command active at a time.

## Related Commands

- [fix smd](fix_smd.html)
- [fix colvars](fix_colvars.html)

