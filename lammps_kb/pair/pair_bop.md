---
id: pair_bop
title: "pair_style bop command"
url: https://docs.lammps.org/pair_bop.html
---

# pair_style bop command

## Syntax

```
pair_style bop keyword ...
save = pre-compute and save some values
```

## Description

The bop pair style computes Bond-Order Potentials (BOP) based on
quantum mechanical theory incorporating both \(\sigma\) and
\(\pi\) bonding.  By analytically deriving the BOP from quantum
mechanical theory its transferability to different phases can approach
that of quantum mechanical methods.  This potential is similar to the
original BOP developed by Pettifor (Pettifor_1,
Pettifor_2, Pettifor_3) and
later updated by Murdick, Zhou, and Ward (Murdick,
Ward).  Currently, BOP potential files for these systems
are provided with LAMMPS: AlCu, CCu, CdTe, CdTeSe, CdZnTe, CuH, GaAs.  A
system with only a subset of these elements, including a single element
(e.g. C or Cu or Al or Ga or Zn or CdZn), can also be modeled by using
the appropriate alloy file and assigning all atom types to the single
element or subset of elements via the pair_coeff command, as discussed below.

The BOP potential consists of three terms:

\[E = \frac{1}{2} \sum_{i=1}^{N} \sum_{j=i_1}^{i_N} \phi_{ij} \left( r_{ij} \right) - \sum_{i=1}^{N} \sum_{j=i_1}^{i_N} \beta_{\sigma,ij} \left( r_{ij} \right) \cdot \Theta_{\sigma,ij} - \sum_{i=1}^{N} \sum_{j=i_1}^{i_N} \beta_{\pi,ij} \left( r_{ij} \right) \cdot \Theta_{\pi,ij} + U_{prom}\]

where \(\phi_{ij}(r_{ij})\) is a short-range two-body function
representing the repulsion between a pair of ion cores,
\(\beta_{\sigma,ij}(r_{ij})\) and \(\beta_{\sigma,ij}(r_{ij})\)
are respectively sigma and \(\pi\) bond integrals, \(\Theta_{\sigma,ij}\)
and \(\Theta_{\pi,ij}\) are \(\sigma\) and \(\pi\)
bond-orders, and U_prom is the promotion energy for sp-valent systems.

The detailed formulas for this potential are given in Ward
(Ward); here we provide only a brief description.

The repulsive energy \(\phi_{ij}(r_{ij})\) and the bond integrals
\(\beta_{\sigma,ij}(r_{ij})\) and \(\beta_{\phi,ij}(r_{ij})\) are functions of the
interatomic distance \(r_{ij}\) between atom i and j.  Each of these
potentials has a smooth cutoff at a radius of \(r_{cut,ij}\).  These
smooth cutoffs ensure stable behavior at situations with high sampling
near the cutoff such as melts and surfaces.

The bond-orders can be viewed as environment-dependent local variables
that are ij bond specific.  The maximum value of the \(\sigma\)
bond-order (\(\Theta_{\sigma}\) is 1, while that of the \(\pi\)
bond-order (\(\Theta_{\pi}\)) is 2, attributing to a maximum value
of the total bond-order (\(\Theta_{\sigma}+\Theta_{\pi}\)) of 3.
The \(\sigma\) and \(\pi\) bond-orders reflect the ubiquitous
single-, double-, and triple- bond behavior of chemistry. Their
analytical expressions can be derived from tight- binding theory by
recursively expanding an inter-site Green s function as a continued
fraction. To accurately represent the bonding with a computationally
efficient potential formulation suitable for MD simulations, the derived
BOP only takes (and retains) the first two levels of the recursive
representations for both the \(\sigma\) and the \(\pi\) bond-orders. Bond-order
terms can be understood in terms of molecular orbital hopping paths
based upon the Cyrot-Lackmann theorem (Pettifor_1).
The \(\sigma\) bond-order with a half-full valence shell is used to
interpolate the bond-order expression that incorporated explicit valance
band filling.  This \(\pi\) bond-order expression also contains also contains
a three-member ring term that allows implementation of an asymmetric
density of states, which helps to either stabilize or destabilize
close-packed structures.  The \(\pi\) bond-order includes hopping paths of
length 4.  This enables the incorporation of dihedral angles effects.

Note
Note that unlike for other potentials, cutoffs for BOP
potentials are not set in the pair_style or pair_coeff command; they
are specified in the BOP potential files themselves.  Likewise, the
BOP potential files list atomic masses; thus you do not need to use
the mass command to specify them.  Note that for BOP
potentials with hydrogen, you will likely want to set the mass of H
atoms to be 10x or 20x larger to avoid having to use a tiny timestep.
You can do this by using the mass command after using the
pair_coeff command to read the BOP potential
file.

One option can be specified as a keyword with the pair_style command.

The save keyword gives you the option to calculate in advance and
store a set of distances, angles, and derivatives of angles.  The
default is to not do this, but to calculate them on-the-fly each time
they are needed.  The former may be faster, but takes more memory.
The latter requires less memory, but may be slower.  It is best to
test this option to optimize the speed of BOP for your particular
system configuration.

Only a single pair_coeff command is used with the bop style which
specifies a BOP potential file, with parameters for all needed
elements.  These are mapped to LAMMPS atom types by specifying
N additional arguments after the filename in the pair_coeff command,
where N is the number of LAMMPS atom types:

As an example, imagine the CdTe.bop file has BOP values for Cd
and Te.  If your LAMMPS simulation has 4 atoms types and you want the
first 3 to be Cd, and the fourth to be Te, you would use the following
pair_coeff command:

pair_coeff * * CdTe Cd Cd Cd Te

The first 2 arguments must be * * so as to span all LAMMPS atom types.
The first three Cd arguments map LAMMPS atom types 1,2,3 to the Cd
element in the BOP file.  The final Te argument maps LAMMPS atom type
4 to the Te element in the BOP file.

BOP files in the potentials directory of the LAMMPS distribution
have a  .bop  suffix.  The potentials are in tabulated form containing
pre-tabulated pair functions for phi_ij(r_ij), beta_(sigma,ij)(r_ij),
and beta_pi,ij)(r_ij).

The parameters/coefficients format for the different kinds of BOP
files are given below with variables matching the formulation of Ward
(Ward) and Zhou (Zhou). Each header line containing a
 :  is preceded by a blank line.

No angular table file format:

The parameters/coefficients format for the BOP potentials input file
containing pre-tabulated functions of g is given below with variables
matching the formulation of Ward (Ward).  This format also
assumes the angular functions have the formulation of (Ward).

The first line is followed by N lines containing the atomic
number, mass, and element symbol of each element.

Following the definition of the elements several global variables for
the tabulated functions are given.

Following this N lines for e_1-e_N containing p_pi.

The next section contains several pair constants for the number of
interaction types e_i-e_j, with i=1->N, j=i->N

The next section contains a line for each three body interaction type
e_j-e_i-e_k with i=0->N, j=0->N, k=j->N

The next section contains a block for each interaction type for the
phi_ij(r_ij).  Each block has nr entries with 5 entries per line.

The next section contains a block for each interaction type for the
beta_(sigma,ij)(r_ij).  Each block has nr entries with 5 entries per
line.

The next section contains a block for each interaction type for
beta_(pi,ij)(r_ij).  Each block has nr entries with 5 entries per line.

The next section contains a block for each interaction type for the
THETA_(S,ij)((THETA_(sigma,ij))^(1/2), f_(sigma,ij)).  Each block has
nBOt entries with 5 entries per line.

The next section contains a block of N lines for e_1-e_N

The last section contains more constants for e_i-e_j interactions with
i=0->N, j=i->N

Angular spline table file format:

The parameters/coefficients format for the BOP potentials input file
containing pre-tabulated functions of g is given below with variables
matching the formulation of Ward (Ward).  This format also
assumes the angular functions have the formulation of (Zhou).

The first line is followed by N lines containing the atomic
number, mass, and element symbol of each element.

Following the definition of the elements several global variables for
the tabulated functions are given.

Following this N lines for e_1-e_N containing p_pi.

The next section contains several pair constants for the number of
interaction types e_i-e_j, with i=1->N, j=i->N

The next section contains a line for each three body interaction type
e_j-e_i-e_k with i=0->N, j=0->N, k=j->N

The rest of the table has the same structure as the previous section
(see above).

Angular no-spline table file format:

The parameters/coefficients format for the BOP potentials input file
containing pre-tabulated functions of g is given below with variables
matching the formulation of Ward (Ward).  This format also
assumes the angular functions have the formulation of (Zhou).

The first two lines are followed by N lines containing the atomic
number, mass, and element symbol of each element.

Following the definition of the elements several global variables for
the tabulated functions are given.

Following this N lines for e_1-e_N containing p_pi.

The next section contains several pair constants for the number of
interaction types e_i-e_j, with i=1->N, j=i->N

The next section contains a line for each three body interaction type
e_j-e_i-e_k with i=0->N, j=0->N, k=j->N

The rest of the table has the same structure as the previous section (see above).

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
pair_style bop
pair_coeff * * ../potentials/CdTe_bop Cd Te
pair_style bop save
pair_coeff * * ../potentials/CdTe.bop.table Cd Te Te
comm_modify cutoff 14.70
```

## Restrictions

Restrictions 
These pair styles are part of the MANYBODY package.  They are only
enabled if LAMMPS was built with that package.  See the Build package page for more info.
These pair potentials require the newtion setting to be
 on  for pair interactions.
Pair style bop is not compatible with being used as a sub-style with
doc:hybrid pair styles <pair_hybrid>. Pair style bop is also not
compatible with multi-cutoff neighbor lists or
multi-cutoff communitcation.
The .bop.table potential files provided with LAMMPS (see the
potentials directory) are parameterized for metal units.
You can use the BOP potential with any LAMMPS units, but you would need
to create your own BOP potential file with coefficients listed in the
appropriate units if your simulation does not use  metal  units.

## Related Commands

- [pair_coeff](pair_coeff.html)

