---
id: compute_pe
title: "compute pe command"
url: https://docs.lammps.org/compute_pe.html
---

# compute pe command

## Syntax

```
compute ID group-ID pe keyword ...
```

## Description

Define a computation that calculates the potential energy of the
entire system of atoms.  The specified group must be  all .  See the
compute pe/atom command if you want per-atom
energies.  These per-atom values could be summed for a group of atoms
via the compute reduce command.

The energy is calculated by the various pair, bond, etc. potentials
defined for the simulation.  If no extra keywords are listed, then the
potential energy is the sum of pair, bond, angle, dihedral, improper,
\(k\)-space (long-range), and fix energy (i.e., it is as though all the
keywords were listed).  If any extra keywords are listed, then only
those components are summed to compute the potential energy.

The \(k\)-space contribution requires 1 extra FFT each timestep the energy
is calculated, if using the PPPM solver via the kspace_style pppm command.  Thus it can increase the cost of the
PPPM calculation if it is needed on a large fraction of the simulation
timesteps.

Various fixes can contribute to the total potential energy of the
system if the fix contribution is included.  See the doc pages for
individual fixes for details of which ones compute a
potential energy.

Note
The fix_modify energy yes command must also be
specified if a fix is to contribute potential energy to this command.

A compute of this style with the ID of  thermo_pe  is created when
LAMMPS starts up, as if this command were in the input script:

compute thermo_pe all pe

See the  thermo_style  command for more details.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 all pe
compute molPE all pe bond angle dihedral improper
```

## Restrictions

Restrictions 
none

## Related Commands

- [compute pe/atom](compute_pe_atom.html)

