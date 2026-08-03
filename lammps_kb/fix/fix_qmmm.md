---
id: fix_qmmm
title: "fix qmmm command"
url: https://docs.lammps.org/fix_qmmm.html
---

# fix qmmm command

## Syntax

```
fix ID group-ID qmmm
```

## Description

This fix provides functionality to enable a quantum
mechanics/molecular mechanics (QM/MM) coupling of LAMMPS to a quantum
mechanical code.  The current implementation only supports an ONIOM
style mechanical coupling to the Quantum ESPRESSO plane
wave DFT package.  Electrostatic coupling is in preparation and the
interface has been written in a manner that coupling to other QM codes
should be possible without changes to LAMMPS itself.

The interface code for this is in the lib/qmmm directory of the LAMMPS
distribution and is being made available at this early stage of
development in order to encourage contributions for interfaces to
other QM codes.  This will allow the LAMMPS side of the implementation
to be adapted if necessary before being finalized.

Details about how to use this fix are currently documented in the
description of the QM/MM interface code itself in lib/qmmm/README.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 1 qmol qmmm
```

## Restrictions

Restrictions 
This fix is part of the QMMM package.  It is only enabled if
LAMMPS was built with that package. It also requires building a
library provided with LAMMPS.  See the Build package page for more info.
The fix is only functional when LAMMPS is built as a library and
linked with a compatible QM program and a QM/MM front end into a QM/MM
executable.  See the lib/qmmm/README file for details.

## Related Commands

Related commands 
none

