---
id: pair_smtbq
title: "pair_style smtbq command"
url: https://docs.lammps.org/pair_smtbq.html
---

# pair_style smtbq command

## Syntax

```
pair_style smtbq
```

## Description

This pair style computes a variable charge SMTB-Q (Second-Moment
tight-Binding QEq) potential as described in SMTB-Q_1 and
SMTB-Q_2.
This potential was first proposed in SMTB-Q_0.
Briefly, the energy of metallic-oxygen systems is given by three contributions:

\[\begin{split}E_{tot} & =  E_{ES} + E_{OO} + E_{MO} \\
E_{ES}  & =  \sum_i{\biggl[ \chi_{i}^{0}Q_i + \frac{1}{2}J_{i}^{0}Q_{i}^{2} +
\frac{1}{2} \sum_{j\neq i}{ J_{ij}(r_{ij})f_{cut}^{R_{coul}}(r_{ij})Q_i Q_j } \biggr] } \\
E_{OO}  & =  \sum_{i,j}^{i,j = O}{\biggl[Cexp( -\frac{r_{ij}}{\rho} ) - Df_{cut}^{r_1^{OO}r_2^{OO}}(r_{ij}) exp(Br_{ij})\biggr]}  \\
E_{MO}  & =  \sum_i{E_{cov}^{i} + \sum_{j\neq i}{ Af_{cut}^{r_{c1}r_{c2}}(r_{ij})exp\bigl[-p(\frac{r_{ij}}{r_0} -1) \bigr] } }\end{split}\]

where \(E_{tot}\) is the total potential energy of the system,
\(E_{ES}\) is the electrostatic part of the total energy,
\(E_{OO}\) is the interaction between oxygen atoms and
\(E_{MO}\) is a short-range interaction between metal and oxygen
atoms. This interactions depend on interatomic distance \(r_{ij}\)
and/or the charge \(Q_{i}\) of atoms i. Cut-off function enables
smooth convergence to zero interaction.

The parameters appearing in the upper expressions are set in the
ffield.SMTBQ.Syst file where Syst corresponds to the selected system
(e.g. field.SMTBQ.Al2O3). Examples for \(\mathrm{TiO_2}\),
\(\mathrm{Al_2O_3}\) are provided.  A single pair_coeff command
is used with the SMTBQ styles which provides the path to the potential
file with parameters for needed elements. These are mapped to LAMMPS
atom types by specifying additional arguments after the potential
filename in the pair_coeff command. Note that atom type 1 must always
correspond to oxygen atoms. As an example, to simulate a \(\mathrm{TiO_2}\) system,
atom type 1 has to be oxygen and atom type 2 Ti. The following
pair_coeff command should then be used:

pair_coeff * * PathToLammps/potentials/ffield.smtbq.TiO2 O Ti

The electrostatic part of the energy consists of two components

self-energy of atom i in the form of a second order charge dependent
polynomial and a long-range Coulombic electrostatic interaction. The
latter uses the wolf summation method described in Wolf,
spherically truncated at a longer cutoff, \(R_{coul}\). The
charge of each ion is modeled by an orbital Slater which depends on
the principal quantum number (n) of the outer orbital shared by the
ion.

Interaction between oxygen, \(E_{OO}\), consists of two parts,
an attractive and a repulsive part. The attractive part is effective
only at short range (< \(r_2^{OO}\)). The attractive
contribution was optimized to study surfaces reconstruction
(e.g. SMTB-Q_2 in \(\mathrm{TiO_2}\)) and is not necessary
for oxide bulk modeling. The repulsive part is the Pauli interaction
between the electron clouds of oxygen. The Pauli repulsion and the
coulombic electrostatic interaction have same cut off value. In the
ffield.SMTBQ.Syst, the keyword  buck  allows to consider only the
repulsive O-O interactions. The keyword  buckPlusAttr  allows to
consider the repulsive and the attractive O-O interactions.

The short-range interaction between metal-oxygen, \(E_{MO}\) is
based on the second moment approximation of the density of states with
a N-body potential for the band energy term,
\(E^i_{cov}\), and a Born-Mayer type repulsive terms
as indicated by the keyword  second_moment  in the
ffield.SMTBQ.Syst. The energy band term is given by:

\[\begin{split}E_{cov}^{i(i=M,O)} & = - \biggl\{\eta_i(\mu \xi^{0})^2 f_{cut}^{r_{c1}r_{c2}}(r_{ij})
\biggl( \sum_{j(j=O,M)}{ exp[ -2q(\frac{r_{ij}}{r_0} - 1)] } \biggr)
\delta Q_i \bigl( 2\frac{n_0}{\eta_i} - \delta Q_i \bigr) \biggr\}^{1/2} \\
\delta Q_i & =  | Q_i^{F} | - | Q_i |\end{split}\]

where \(\eta_i\) is the stoichiometry of atom i,
\(\delta Q_i\) is the charge delocalization of atom i,
compared to its formal charge
\(Q^F_i\). \(n_0\), the number of hybridized
orbitals, is calculated with to the atomic orbitals shared
\(d_i\) and the stoichiometry
\(\eta_i\). \(r_{c1}\) and \(r_{c2}\) are the two
cutoff radius around the fourth neighbors in the cutoff function.

In the formalism used here, \(\xi^0\) is the energy
parameter. \(\xi^0\) is in tight-binding approximation the
hopping integral between the hybridized orbitals of the cation and the
anion. In the literature we find many ways to write the hopping
integral depending on whether one takes the point of view of the anion
or cation. These are equivalent vision. The correspondence between the
two visions is explained in appendix A of the article in the
SrTiO3 SMTB-Q_3 (parameter \(\beta\) shown in
this article is in fact the \(\beta_O\)). To summarize the
relationship between the hopping integral \(\xi^O\)  and the
others, we have in an oxide \(\mathrm{C_n O_m}\) the following
relationship:

\[\begin{split}\xi^0 & = \frac{\xi_O}{m} = \frac{\xi_C}{n} \\
\frac{\beta_O}{\sqrt{m}} & = \frac{\beta_C}{\sqrt{n}} = \xi^0 \frac{\sqrt{m}+\sqrt{n}}{2}\end{split}\]

Thus parameter \(\mu\), indicated above, is given by \(\mu = \frac{1}{2}(\sqrt{n}+\sqrt{m})\)

The potential offers the possibility to consider the polarizability of
the electron clouds of oxygen by changing the slater radius of the
charge density around the oxygen atoms through the parameters rBB, rB and
rS in the ffield.SMTBQ.Syst. This change in radius is performed
according to the method developed by E. Maras
SMTB-Q_2. This method needs to determine the number of
nearest neighbors around the oxygen. This calculation is based on
first (\(r_{1n}\)) and second (\(r_{2n}\)) distances
neighbors.

The SMTB-Q potential is a variable charge potential. The equilibrium
charge on each atom is calculated by the electronegativity
equalization (QEq) method. See Rick for further detail. One
can adjust the frequency, the maximum number of iterative loop and the
convergence of the equilibrium charge calculation. To obtain the
energy conservation in NVE thermodynamic ensemble, we recommend to use
a convergence parameter in the interval 10e-5 -
10e-6 eV.

The ffield.SMTBQ.Syst files are provided for few systems. They consist
of nine parts and the lines beginning with  #  are comments (note that
the number of comment lines matter). The first sections are on the
potential parameters and others are on the simulation options and
might be modified. Keywords are character type and must be enclosed in
quotation marks ( ).

For the anion (oxygen)

For each cations (metal):

Note
This last option slows down the calculation dramatically.  Use
only with a single processor simulation.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
pair_style smtbq
pair_coeff * * ffield.smtbq.Al2O3 O Al
```

## Restrictions

Restrictions 
This pair style is part of the SMTBQ package and is only enabled
if LAMMPS is built with that package.  See the Build package page for more info.
This potential requires using atom type 1 for oxygen and atom type
higher than 1 for metal atoms.
This pair style requires the newton setting to be  on 
for pair interactions.
The SMTB-Q potential files provided with LAMMPS (see the potentials
directory) are parameterized for metal units.

