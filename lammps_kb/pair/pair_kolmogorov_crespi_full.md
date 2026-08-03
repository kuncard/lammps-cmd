---
id: pair_kolmogorov_crespi_full
title: "pair_style kolmogorov/crespi/full command"
url: https://docs.lammps.org/pair_kolmogorov_crespi_full.html
---

# pair_style kolmogorov/crespi/full command

## Syntax

```
pair_style hybrid/overlay kolmogorov/crespi/full cutoff tap_flag
```

## Description

The kolmogorov/crespi/full style computes the Kolmogorov-Crespi (KC)
interaction potential as described in (Kolmogorov).
No simplification is made,

\[\begin{split} E  = & \frac{1}{2} \sum_i \sum_{j \neq i} V_{ij} \\
 V_{ij}  = & e^{-\lambda (r_{ij} -z_0)} \left [ C + f(\rho_{ij}) + f(\rho_{ji}) \right ] - A \left ( \frac{r_{ij}}{z_0}\right )^{-6} \\
\rho_{ij}^2 = & r_{ij}^2 - (\mathbf{r}_{ij}\cdot \mathbf{n}_{i})^2 \\
\rho_{ji}^2 = & r_{ij}^2 - (\mathbf{r}_{ij}\cdot  \mathbf{n}_{j})^2 \\
f(\rho) & =  e^{-(\rho/\delta)^2} \sum_{n=0}^2 C_{2n} { (\rho/\delta) }^{2n}\end{split}\]

It is important to have a sufficiently large cutoff to ensure smooth
forces and to include all the pairs to build the neighbor list for
calculating the normals.  Energies are shifted so that they go
continuously to zero at the cutoff assuming that the exponential part of
\(V_{ij}\) (first term) decays sufficiently fast.  This shift is achieved by
the last term in the equation for \(V_{ij}\) above. This is essential only
when the tapper function is turned off. The formula of taper function
can be found in pair style ilp/graphene/hbn.

Note
This potential (ILP) is intended for interlayer interactions between two
different layers of graphene. To perform a realistic simulation, this potential
must be used in combination with intralayer potential, such as
AIREBO or Tersoff potential.
To keep the intralayer properties unaffected, the interlayer interaction
within the same layers should be avoided. Hence, each atom has to have a layer
identifier such that atoms residing on the same layer interact via the
appropriate intralayer potential and atoms residing on different layers
interact via the ILP. Here, the molecule id is chosen as the layer identifier,
thus a data file with the  full  atom style is required to use this potential.

The parameter file (e.g. CH.KC), is intended for use with metal
units, with energies in meV. Two additional parameters, S,
and rcut are included in the parameter file. S is designed to
facilitate scaling of energies. rcut is designed to build the neighbor
list for calculating the normals for each atom pair.

Note
Two new sets of parameters of KC potential for hydrocarbons, CH.KC
(without the taper function) and CH_taper.KC (with the taper function)
are presented in (Ouyang1).  The energy for the KC potential
with the taper function goes continuously to zero at the cutoff.  The
parameters in both CH.KC and CH_taper.KC provide a good description in
both short- and long-range interaction regimes. While the original
parameters (CC.KC) published in (Kolmogorov) are only
suitable for long-range interaction regime.  This feature is essential
for simulations in high pressure regime (i.e., the interlayer distance
is smaller than the equilibrium distance).  The benchmark tests and
comparison of these parameters can be found in (Ouyang1) and (Ouyang2).

This potential must be used in combination with hybrid/overlay.
Other interactions can be set to zero using pair_style none.

This pair style tallies a breakdown of the total interlayer potential
energy into sub-categories, which can be accessed via the compute pair command as a vector of values of length 2.
The 2 values correspond to the following sub-categories:

To print these quantities to the log file (with descriptive column
headings) the following commands could be included in an input script:

compute 0 all pair kolmogorov/crespi/full
variable Evdw  equal c_0[1]
variable Erep  equal c_0[2]
thermo_style custom step temp epair v_Erep v_Evdw

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
pair_style hybrid/overlay kolmogorov/crespi/full 20.0 0
pair_coeff * * none
pair_coeff * * kolmogorov/crespi/full  CH.KC   C C

pair_style hybrid/overlay rebo kolmogorov/crespi/full 16.0 1
pair_coeff * * rebo                    CH.rebo      C H
pair_coeff * * kolmogorov/crespi/full  CH_taper.KC  C H
```

## Restrictions

Restrictions 
This pair style is part of the INTERLAYER package.  It is only enabled
if LAMMPS was built with that package.  See the Build package page for more info.
This pair style requires the newton setting to be on for pair
interactions.
The CH.KC potential file provided with LAMMPS (see the potentials
folder) is parameterized for metal units.  You can use this pair style
with any LAMMPS units, but you would need to create your own custom
CH.KC potential file with all coefficients converted to the appropriate
units.

## Related Commands

- [pair_coeff](pair_coeff.html)
- [pair_none](pair_none.html)
- [pair_style hybrid/overlay](pair_hybrid.html)
- [pair_style drip](pair_drip.html)
- [pair_style pair_lebedeva_z](pair_lebedeva_z.html)
- [pair_style kolmogorov/crespi/z](pair_kolmogorov_crespi_z.html)
- [pair_style ilp/graphene/hbn](pair_ilp_graphene_hbn.html)

