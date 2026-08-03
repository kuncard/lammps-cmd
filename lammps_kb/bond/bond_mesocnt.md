---
id: bond_mesocnt
title: "bond_style mesocnt command"
url: https://docs.lammps.org/bond_mesocnt.html
---

# bond_style mesocnt command

## Syntax

```
bond_style mesocnt
```

## Description

Added in version 15Sep2022.

The mesocnt bond style is a wrapper for the harmonic style, and uses the potential

\[E = K (r - r_0)^2\]

where \(r_0\) is the equilibrium bond distance.  Note that the
usual 1/2 factor is included in \(K\).  The style implements
parameterization presets of \(K\) for mesoscopic simulations of
carbon nanotubes based on the atomistic simulations of
(Srivastava).

Other presets can be readily implemented in the future.

The following coefficients must be defined for each bond type via the
bond_coeff command as in the example above, or in
the data file or restart files read by the read_data or read_restart commands:

Preset C is for carbon nanotubes, and the additional parameters are:

Preset custom is simply a direct wrapper for the harmonic style, and the additional parameters are:

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
bond_style mesocnt
bond_coeff 1 C 10 10 20.0
bond_coeff 4 custom 800.0 10.0
```

## Restrictions

Restrictions 
This bond style can only be used if LAMMPS was built with the MOLECULE
and MESONT packages.  See the Build package
page for more info.

## Related Commands

- [bond_coeff](bond_coeff.html)
- [delete_bonds](delete_bonds.html)

