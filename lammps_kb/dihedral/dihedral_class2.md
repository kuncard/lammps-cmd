---
id: dihedral_class2
title: "dihedral_style class2 command"
url: https://docs.lammps.org/dihedral_class2.html
---

# dihedral_style class2 command

## Syntax

```
dihedral_style class2
```

## Description

The class2 dihedral style uses the potential

\[\begin{split}E        = & E_d + E_{mbt} + E_{ebt} + E_{at} + E_{aat} + E_{bb13} \\
E_d      = & \sum_{n=1}^{3} K_n [ 1 - \cos (n \phi - \phi_n) ] \\
E_{mbt}  = & (r_{jk} - r_2) [ A_1 \cos (\phi) + A_2 \cos (2\phi) + A_3 \cos (3\phi) ] \\
E_{ebt}  = & (r_{ij} - r_1) [ B_1 \cos (\phi) + B_2 \cos (2\phi) + B_3 \cos (3\phi) ] + \\
           & (r_{kl} - r_3) [ C_1 \cos (\phi) + C_2 \cos (2\phi) + C_3 \cos (3\phi) ] \\
E_{at}   = & (\theta_{ijk} - \theta_1) [ D_1 \cos (\phi) + D_2 \cos (2\phi) + D_3 \cos (3\phi) ] + \\
           & (\theta_{jkl} - \theta_2) [ E_1 \cos (\phi) + E_2 \cos (2\phi) + E_3 \cos (3\phi) ] \\
E_{aat}  = & M (\theta_{ijk} - \theta_1) (\theta_{jkl} - \theta_2) \cos (\phi) \\
E_{bb13} = & N (r_{ij} - r_1) (r_{kl} - r_3)\end{split}\]

where \(E_d\) is the dihedral term, \(E_{mbt}\) is a
middle-bond-torsion term, \(E_{ebt}\) is an end-bond-torsion term,
\(E_{at}\) is an angle-torsion term, \(E_{aat}\) is an
angle-angle-torsion term, and \(E_{bb13}\) is a bond-bond-13 term.

\(\theta_1\) and \(\theta_2\) are equilibrium angles and
:math:\(r_1\), \(r_2\), and r_3 are equilibrium bond lengths.

See (Sun) for a description of the COMPASS class2
force field.

Coefficients for the \(E_d\), \(E_{mbt}\), \(E_{ebt}\),
\(E_{at}\), \(E_{aat}\), and \(E_{bb13}\) formulas must be
defined for each dihedral type via the dihedral_coeff command as in the example above, or in the data file
or restart files read by the read_data or
read_restart commands.

These are the 6 coefficients for the \(E_d\) formula:

For the \(E_{mbt}\) formula, each line in a dihedral_coeff command in the input script lists 5 coefficients, the
first of which is mbt to indicate they are MiddleBondTorsion
coefficients.  In a data file, these coefficients should be listed under
a MiddleBondTorsion Coeffs heading and you must leave out the mbt,
i.e. only list 4 coefficients after the dihedral type.

For the \(E_{ebt}\) formula, each line in a dihedral_coeff command in the input script lists 9 coefficients, the
first of which is ebt to indicate they are EndBondTorsion
coefficients.  In a data file, these coefficients should be listed under
a EndBondTorsion Coeffs heading and you must leave out the ebt,
i.e. only list 8 coefficients after the dihedral type.

For the \(E_{at}\) formula, each line in a dihedral_coeff command in the input script lists 9 coefficients, the
first of which is at to indicate they are AngleTorsion coefficients.
In a data file, these coefficients should be listed under a
AngleTorsion Coeffs heading and you must leave out the at, i.e. only
list 8 coefficients after the dihedral type.

\(\theta_1\) and \(\theta_2\) are specified in degrees, but
LAMMPS converts them to radians internally; hence the various \(D\)
and \(E\) are effectively energy per radian.

For the \(E_{aat}\) formula, each line in a dihedral_coeff command in the input script lists 4 coefficients, the
first of which is aat to indicate they are AngleAngleTorsion
coefficients.  In a data file, these coefficients should be listed under
a AngleAngleTorsion Coeffs heading and you must leave out the aat,
i.e. only list 3 coefficients after the dihedral type.

\(\theta_1\) and \(\theta_2\) are specified in degrees, but
LAMMPS converts them to radians internally; hence \(M\) is
effectively energy per radian^2.

For the \(E_{bb13}\) formula, each line in a dihedral_coeff command in the input script lists 4 coefficients, the
first of which is bb13 to indicate they are BondBond13 coefficients.
In a data file, these coefficients should be listed under a BondBond13
Coeffs heading and you must leave out the bb13, i.e. only list 3
coefficients after the dihedral type.

Added in version 30Mar2026.

The class2xe dihedral style uses the potential

\[\begin{split}\begin{aligned}
E_{mbt}    = & \left[ 1 - e^{-\alpha_2 (r_{jk} - r_2)} \right] [ A_1 \cos (\phi) + A_2 \cos (2\phi) + A_3 \cos (3\phi) ] \\
E_{ebt}    = & \left[ 1 - e^{-\alpha_1 (r_{ij} - r_1)} \right] [ B_1 \cos (\phi) + B_2 \cos (2\phi) + B_3 \cos (3\phi) ] + \\
             & \left[ 1 - e^{-\alpha_3 (r_{kl} - r_3)} \right] [ C_1 \cos (\phi) + C_2 \cos (2\phi) + C_3 \cos (3\phi) ] \\
E_{bb13} = & D \left[ 1 - e^{-\alpha (r_{ij} - r_1)} \right] \left[ 1 - e^{-\alpha (r_{kl} - r_3)} \right]
\end{aligned}\end{split}\]

where \(E_{mbt}\) is a middle-bond-torsion term, \(E_{ebt}\) is
an end-bond-torsion term, and \(E_{bb13}\) is a bond-bond-13 term
(\(D\) is the dissociation energy).

\(\theta_1\) and \(\theta_2\) are equilibrium angles and
:math:\(r_1\), \(r_2\), and r_3 are equilibrium bond lengths.

See (Kemppainen) for a description of the
ClassII-xe force field and see Howto bioFF page for
a motivation for the ClassII-xe force field.

Note
The class2xe dihedral style only describes the dissociation of
a bond stretch. However once a bond is dissociated and stretched
beyond the processor communication cutoff distance in parallel,
the simulation will crash with atoms missing errors. This is
often after the material fractures and thus for post-fracture
phenomena the bonded interactions need to be removed for proper
parallel communication.
To disconnect the dissociated bond and remove higher order
interactions (angles, dihedrals, and impropers) the following
LAMMPS commands can be used with the class2xe dihedral style
fix bond/react or
fix bond/break. See the
Howto bioFF page for more details.

Coefficients for the \(E_{mbt}\), \(E_{ebt}\),
and \(E_{bb13}\) formulas must be
defined for each dihedral type via the dihedral_coeff
command as in the example above, or in the data file
or restart files read by the read_data or
read_restart commands.

For the \(E_{mbt}\) formula, each line in a
dihedral_coeff command in the input script lists
6 coefficients, the first of which is mbt to indicate they are
MiddleBondTorsion coefficients.  In a data file, these coefficients
should be listed under a MiddleBondTorsion Coeffs heading and you
must leave out the mbt, i.e. only list 5 coefficients after the
dihedral type.

For the \(E_{ebt}\) formula, each line in a
dihedral_coeff command in the input script lists
11 coefficients, the first of which is ebt to indicate they are
EndBondTorsion coefficients.  In a data file, these coefficients
should be listed under a EndBondTorsion Coeffs heading and you must
leave out the ebt, i.e. only list 10 coefficients after the dihedral
type.

For the \(E_{bb13}\) formula, each line in a
dihedral_coeff command in the input script lists
5 coefficients, the first of which is bb13 to indicate they are
BondBond13 coefficients.  In a data file, these coefficients should be
listed under a BondBond13 Coeffs heading and you must leave out the
bb13, i.e. only list 4 coefficients after the dihedral type.

The dihedral, AngleTorsion and AngleAngleTorsion terms remain unchanged.

Styles with a gpu, intel, kk, omp, or opt suffix are
functionally the same as the corresponding style without the suffix.
They have been optimized to run faster, depending on your available
hardware, as discussed on the Accelerator packages
page.  The accelerated styles take the same arguments and should
produce the same results, except for round-off and precision issues.

These accelerated styles are part of the GPU, INTEL, KOKKOS,
OPENMP, and OPT packages, respectively.  They are only enabled if
LAMMPS was built with those packages.  See the Build package page for more info.

You can specify the accelerated styles explicitly in your input script
by including their suffix, or you can use the -suffix command-line switch when you invoke LAMMPS, or you can use the
suffix command in your input script.

See the Accelerator packages page for more
instructions on how to use the accelerated styles effectively.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
dihedral_style class2
dihedral_coeff 1 100 75 100 70 80 60
dihedral_coeff * mbt 3.5945 0.1704 -0.5490 1.5228
dihedral_coeff * ebt 0.3417 0.3264 -0.9036 0.1368 0.0 -0.8080 1.0119 1.1010
dihedral_coeff 2 at 0.0 -0.1850 -0.7963 -2.0220 0.0 -0.3991 110.2453 105.1270
dihedral_coeff * aat -13.5271 110.2453 105.1270
dihedral_coeff * bb13 0.0 1.0119 1.1010
```

## Restrictions

Restrictions 
This dihedral style can only be used if LAMMPS was built with the CLASS2
package.  See the Build package doc page for more
info.

## Related Commands

- [dihedral_coeff](dihedral_coeff.html)

