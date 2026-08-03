---
id: temper_npt
title: "temper/npt command"
url: https://docs.lammps.org/temper_npt.html
---

# temper/npt command

## Syntax

```
temper/npt  N M temp fix-ID seed1 seed2 pressure index
```

## Description

Run a parallel tempering or replica exchange simulation using multiple
replicas (ensembles) of a system in the isothermal-isobaric (NPT)
ensemble.  The command temper/npt works like temper but
requires running replicas in the NPT ensemble instead of the canonical
(NVT) ensemble and allows for pressure to be set in the ensembles.
These multiple ensembles can run in parallel at different temperatures
or different pressures.  The acceptance criteria for temper/npt is
specific to the NPT ensemble and can be found in references
(Okabe) and (Mori).

Apart from the difference in acceptance criteria and the specification
of pressure, this command works much like the temper
command. See the documentation on temper for information
on how the parallel tempering is handled in general.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
temper/npt 100000 100 $t nptfix 0 58728 1
temper/npt 2500000 1000 300 nptfix  0 32285 $p
temper/npt 5000000 2000 $t nptfix 0 12523 1 $w
```

## Restrictions

Restrictions 
This command can only be used if LAMMPS was built with the REPLICA
package.  See the Build package page for more
info.
This command should be used with a fix that maintains the
isothermal-isobaric (NPT) ensemble.

## Related Commands

- [temper](temper.html)
- [variable](variable.html)
- [fix_npt](fix_nh.html)

