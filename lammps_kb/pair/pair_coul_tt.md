---
id: pair_coul_tt
title: "pair_style coul/tt command"
url: https://docs.lammps.org/pair_coul_tt.html
---

# pair_style coul/tt command

## Syntax

```
pair_style style args
coul/tt args = n cutoff
  n = degree of polynomial
  cutoff = global cutoff (distance units)
```

## Description

The coul/tt pair style is meant to be used with force fields that
include explicit polarization through Drude dipoles.

The coul/tt pair style should be used as a sub-style within in the
pair_style hybrid/overlay command, in conjunction with a
main pair style including Coulomb interactions and thole pair style,
or with lj/cut/thole/long pair style that is equivalent to the combination
of preceding two.

The coul/tt pair styles compute the charge-dipole Coulomb interaction damped
at short distances by a function

\[f_{n,ij}(r) = 1 - c_{ij} \cdot e^{-b_{ij} r} \sum_{k=0}^n \frac{(b_{ij} r)^k}{k!}\]

This function results from an adaptation to the Coulomb interaction (Salanne) of the damping function originally proposed
by Tang Toennies for van der Waals interactions.

The polynomial takes the degree 4 for damping the Coulomb interaction.
The parameters \(b_{ij}\) and \(c_{ij}\) could be determined from
first-principle calculations for small, mainly mono-atomic, ions (Salanne), or else treated as empirical for large molecules.

In pair styles with Drude induced dipoles, this damping function is typically
applied to the interactions between a Drude charge (either \(q_{D,i}\) on
a Drude particle or \(-q_{D,i}\) on the respective
Drude core)) and a charge on a non-polarizable atom, \(q_{j}\).

The Tang-Toennies function could also be used to damp electrostatic
interactions between the (non-polarizable part of the) charge of a core,
\(q_{i}-q_{D,i}\), and the Drude charge of another, \(-q_{D,j}\).
The \(b_{ij}\) and \(c_{ij}\) are equal  to \(b_{ji}\) and
\(c_{ji}\) in the case of core-core interactions.

For pair_style coul/tt, the following coefficients must be defined for
each pair of atoms types via the pair_coeff command
as in the example above.

The last two coefficients are optional.  If not specified the global
degree of the polynomial or the global cutoff specified in the pair_style
command are used. In order to specify a cutoff (forth argument), the degree of
the polynomial (third argument) must also be specified.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
pair_style hybrid/overlay ... coul/tt 4 12.0
pair_coeff 1 2  coul/tt 4.5 1.0
pair_coeff 1 2  coul/tt 4.0 1.0 4 12.0
pair_coeff 1 3* coul/tt 4.5 1.0 4
```

## Restrictions

Restrictions 
These pair styles are part of the DRUDE package. They are only
enabled if LAMMPS was built with that package. See the Build package page for more info.
This pair_style should currently not be used with the charmm dihedral
style if the latter has non-zero 1-4 weighting
factors. This is because the coul/tt pair style does not know which
pairs are 1-4 partners of which dihedrals.

## Related Commands

- [fix drude](fix_drude.html)
- [fix langevin/drude](fix_langevin_drude.html)
- [fix drude/transform](fix_drude_transform.html)
- [compute temp/drude](compute_temp_drude.html)
- [pair_style thole](pair_thole.html)

