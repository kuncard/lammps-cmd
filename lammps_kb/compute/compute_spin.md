---
id: compute_spin
title: "compute spin command"
url: https://docs.lammps.org/compute_spin.html
---

# compute spin command

## Syntax

```
compute ID group-ID spin
```

## Description

Define a computation that calculates magnetic quantities for a system
of atoms having spins.

This compute calculates the following 6 magnetic quantities:

The simplest way to output the results of the compute spin calculation
is to define some of the quantities as variables, and to use the thermo and
thermo_style commands, for example:

compute out_mag         all spin

variable mag_z          equal c_out_mag[3]
variable mag_norm       equal c_out_mag[4]
variable temp_mag       equal c_out_mag[6]

thermo                  10
thermo_style            custom step v_mag_z v_mag_norm v_temp_mag

This series of commands evaluates the total magnetization along z, the norm of
the total magnetization, and the magnetic temperature. Three variables are
assigned to those quantities. The thermo and thermo_style commands print them
every 10 timesteps.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute out_mag all spin
```

## Restrictions

Restrictions 
The spin compute is part of the SPIN package.  This compute is only
enabled if LAMMPS was built with this package.  See the Build package page for more info.  The atom_style
has to be  spin  for this compute to be valid.
Related commands:
none

