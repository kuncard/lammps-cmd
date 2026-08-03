---
id: pair_uf3
title: "pair_style uf3 command"
url: https://docs.lammps.org/pair_uf3.html
---

# pair_style uf3 command

## Syntax

```
pair_style style BodyFlag
BodyFlag = Indicates whether to calculate only 2-body or 2 and 3-body interactions. Possible values: 2 or 3
```

## Description

Added in version 27June2024.

The uf3 style computes the Ultra-Fast Force Fields (UF3) potential, a machine-learning interatomic potential. In UF3,
the total energy of the system is defined via two- and three-body
interactions:

\[\begin{split}E & = \sum_{i,j} V_2(r_{ij}) + \sum_{i,j,k} V_3 (r_{ij},r_{ik},r_{jk}) \\
V_2(r_{ij}) & = \sum_{n=0}^N c_n B_n(r_{ij}) \\
V_3 (r_{ij},r_{ik},r_{jk}) & = \sum_{l=0}^{N_l} \sum_{m=0}^{N_m} \sum_{n=0}^{N_n} c_{l,m,n} B_l(r_{ij}) B_m(r_{ik}) B_n(r_{jk})\end{split}\]

where \(V_2(r_{ij})\) and \(V_3 (r_{ij},r_{ik},r_{jk})\) are the
two- and three-body interactions, respectively. For the two-body the
summation is over all neighbors J and for the three-body the summation
is over all neighbors J and K of atom I within a cutoff distance
determined from the potential files. \(B_n(r_{ij})\) are the cubic
b-spline basis, \(c_n\) and \(c_{l,m,n}\) are the machine-learned
interaction parameters and \(N\), \(N_l\), \(N_m\), and
\(N_n\) denote the number of basis functions per spline or tensor
spline dimension.

With uf3 style only a single pair_coeff command is used to indicate the
UF3 LAMMPS potential file containing all the two- and three-body interactions
followed by N additional arguments specifying the mapping of UF3 elements to
LAMMPS atom types, where N is the number of LAMMPS atom types:

As an example, if a LAMMPS simulation contains 2 atom types (elements
 A  and  B ), the pair_coeff command will be:

pair_style uf3 3
pair_coeff * * AB.uf3 A B

The AB.uf3 file should contain all two-body (A-A, A-B, B-B) and three-body
(A-A-A, A-A-B, A-B-B, B-A-A, B-A-B, B-B-B).

If a value of  2  is specified in the pair_style uf3 command,
only the two-body potentials are needed. For 3-body interaction the
first atom type is the central atom. We recommend using the
generate_uf3_lammps_pots.py script (found here) for
generating the UF3 LAMMPS potential file from the UF3 JSON potentials.

UF3 LAMMPS potential file in the potentials directory of the LAMMPS
distribution have a  .uf3  suffix. The interaction block in UF3 LAMMPS potential
file should start with #UF3 POT and end with # characters.
Following shows the format of a generic 2-body and 3-body potential block in
UF3 LAMMPS potential file-

#UF3 POT UNITS: units DATE: POT_GEN_DATE AUTHOR: AUTHOR_NAME CITATION: CITE
2B ELEMENT1 ELEMENT2 LEADING_TRIM TRAILING_TRIM
Rij_CUTOFF NUM_OF_KNOTS
BSPLINE_KNOTS
NUM_OF_COEFF
COEFF
#
#UF3 POT UNITS: units DATE: POT_GEN_DATE AUTHOR: AUTHOR_NAME CITATION: CITE
3B ELEMENT1 ELEMENT2 ELEMENT3 LEADING_TRIM TRAILING_TRIM
Rjk_CUTOFF Rik_CUTOFF Rij_CUTOFF NUM_OF_KNOTS_JK NUM_OF_KNOTS_IK NUM_OF_KNOTS_IJ
BSPLINE_KNOTS_FOR_JK
BSPLINE_KNOTS_FOR_IK
BSPLINE_KNOTS_FOR_IJ
SHAPE_OF_COEFF_MATRIX[I][J][K]
COEFF_MATRIX[0][0][K]
COEFF_MATRIX[0][1][K]
COEFF_MATRIX[0][2][K]
.
.
.
COEFF_MATRIX[1][0][K]
COEFF_MATRIX[1][1][K]
COEFF_MATRIX[1][2][K]
.
.
.
#

The second line indicates whether the block contains data for 2-body
(2B) or 3-body (3B) interaction. This is followed by element
combination interaction, LEADING_TRIM and TRAILING_TRIM
number on the same line. The current implementation is only tested for
LEADING_TRIM=0 and TRAILING_TRIM=3.
If other values are used LAMMPS is terminated after issuing an error message.
The Rij_CUTOFF sets the 2-body cutoff for the interaction described
by the potential block. NUM_OF_KNOTS is the number of knots
(or the length of the knot vector) present on the very next line. The
BSPLINE_KNOTS line should contain all the knots in ascending order.
NUM_OF_COEFF is the number of coefficients in the COEFF line.
All the numbers in the BSPLINE_KNOTS and COEFF line should be space-separated.
Similar to the 2-body potential block, the third line sets the cutoffs and
length of the knots. The cutoff distance between atom-type I and J is
Rij_CUTOFF, atom-type I and K is Rik_CUTOFF and between
J and K is Rjk_CUTOFF.

Note
The current implementation only works for UF3 potentials with cutoff
distances for 3-body interactions that follows
2Rij_CUTOFF=2Rik_CUTOFF=Rjk_CUTOFF relation.

The BSPLINE_KNOTS_FOR_JK, BSPLINE_KNOTS_FOR_IK, and
BSPLINE_KNOTS_FOR_IJ lines (note the order) contain the knots in
increasing order for atoms J and K, I and K, and atoms I and J
respectively. The number of knots is defined by the
NUM_OF_KNOTS_* characters in the previous line.  The shape of
the coefficient matrix is defined on the
SHAPE_OF_COEFF_MATRIX[I][J][K] line followed by the columns of
the coefficient matrix, one per line, as shown above. For example, if
the coefficient matrix has the shape of 8x8x13, then
SHAPE_OF_COEFF_MATRIX[I][J][K] will be 8 8 13 followed
by 64 (8x8) lines each containing 13 coefficients separated by space.

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
pair_style uf3 3
pair_coeff * * Nb.uf3 Nb

pair_style uf3 2
pair_coeff * * NbSn.uf3 Nb Sn

pair_style uf3 3
pair_coeff * * NbSn.uf3 Nb Sn
```

## Restrictions

Restrictions 
The  uf3  pair style is part of the ML-UF3 package. It is only enabled
if LAMMPS was built with that package. See the Build package page for more info.
This pair style requires the newton setting to be  on .
The UF3 LAMMPS potential file provided with LAMMPS (see the potentials
directory) are parameterized for metal units.
The single() function of  uf3  pair style only return the 2-body
interaction energy.

## Related Commands

- [pair_coeff](pair_coeff.html)

