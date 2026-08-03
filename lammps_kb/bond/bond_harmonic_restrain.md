---
id: bond_harmonic_restrain
title: "bond_style harmonic/restrain command"
url: https://docs.lammps.org/bond_harmonic_restrain.html
---

# bond_style harmonic/restrain command

## Syntax

```
bond_style harmonic/restrain
```

## Description

Added in version 28Mar2023.

The harmonic/restrain bond style uses the potential

\[E = K (r - r_{t=0})^2\]

where \(r_{t=0}\) is the distance between the bonded atoms at the
beginning of the first run or minimize
command after the bond style has been defined (t=0).  Note that the
usual 1/2 factor is included in \(K\).  This will effectively
restrain bonds to their initial length, whatever that is.  This is where
this bond style differs from bond style harmonic
where the bond length is set through the per bond type coefficients.

The following coefficient must be defined for each bond type via the
bond_coeff command as in the example above, or in
the data file or restart files read by the read_data
or read_restart commands

This bond style differs from other options to add harmonic restraints
like fix restrain or pair style list or fix colvars in that it requires a
bond topology, and thus the defined bonds will trigger exclusion of
special neighbors from the neighbor list according to the
special_bonds settings.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
bond_style harmonic
bond_coeff 5 80.0
```

## Restrictions

Restrictions 
This bond style can only be used if LAMMPS was built with the
EXTRA-MOLECULE package.  See the Build package
page for more info.
This bond style maintains internal data to determine the original bond
lengths \(r_{t=0}\).  This information will be written to
binary restart files but not to data
files.  Thus, continuing a simulation is only possible
with read_restart.  When using the read_data
command, the reference bond lengths \(r_{t=0}\) will be
re-initialized from the current geometry.
This bond style cannot be used with fix shake or fix rattle, with fix filter/corotate, or
any tip4p pair style since there is no specific
equilibrium distance for a given bond type.

## Related Commands

- [bond_coeff](bond_coeff.html)
- [bond_harmonic](bond_harmonic.html)
- [fix restrain](fix_restrain.html)
- [pair style list](pair_list.html)

