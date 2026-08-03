---
id: pair_ilp_graphene_hbn
title: "pair_style ilp/graphene/hbn command"
url: https://docs.lammps.org/pair_ilp_graphene_hbn.html
---

# pair_style ilp/graphene/hbn command

## Syntax

```
pair_style [hybrid/overlay ...] ilp/graphene/hbn cutoff tap_flag
```

## Description

The ilp/graphene/hbn style computes the registry-dependent interlayer
potential (ILP) potential as described in (Leven1),
(Leven2) and (Maaravi).
The normals are calculated in the way as described
in (Kolmogorov).

\[\begin{split}E  = & \frac{1}{2} \sum_i \sum_{j \neq i} V_{ij} \\
V_{ij}  = & \mathrm{Tap}(r_{ij})\left \{ e^{-\alpha (r_{ij}/\beta -1)}
             \left [ \epsilon + f(\rho_{ij}) + f(\rho_{ji})\right ] -
              \frac{1}{1+e^{-d\left [ \left ( r_{ij}/\left (s_R \cdot r^{eff} \right ) \right )-1 \right ]}}
              \cdot \frac{C_6}{r^6_{ij}} \right \}\\
\rho_{ij}^2 = & r_{ij}^2 - (\mathbf{r}_{ij} \cdot \mathbf{n}_i)^2 \\
\rho_{ji}^2  = & r_{ij}^2 - (\mathbf{r}_{ij} \cdot \mathbf{n}_j)^2 \\
f(\rho)  = &  C e^{ -( \rho / \delta )^2 } \\
\mathrm{Tap}(r_{ij})  = & 20\left ( \frac{r_{ij}}{R_{cut}} \right )^7 -
                        70\left ( \frac{r_{ij}}{R_{cut}} \right )^6 +
                        84\left ( \frac{r_{ij}}{R_{cut}} \right )^5 -
                        35\left ( \frac{r_{ij}}{R_{cut}} \right )^4 + 1\end{split}\]

Where \(\mathrm{Tap}(r_{ij})\) is the taper function which provides
a continuous cutoff (up to third derivative) for interatomic separations
larger than \(r_c\) (Maaravi). The definitions of
each parameter in the above equation can be found in (Leven1) and (Maaravi).

It is important to include all the pairs to build the neighbor list for
calculating the normals.

Note
This potential (ILP) is intended for interlayer interactions between two
different layers of graphene, hexagonal boron nitride (h-BN) and their hetero-junction.
To perform a realistic simulation, this potential must be used in combination with
intralayer potential, such as AIREBO or Tersoff potential.
To keep the intralayer properties unaffected, the interlayer interaction
within the same layers should be avoided. Hence, each atom has to have a layer
identifier such that atoms residing on the same layer interact via the
appropriate intralayer potential and atoms residing on different layers
interact via the ILP. Here, the molecule id is chosen as the layer identifier,
thus a data file with the  full  atom style is required to use this potential.

The parameter file (e.g. BNCH.ILP), is intended for use with metal
units, with energies in meV. Two additional parameters,
S, and rcut are included in the parameter file. S is designed to
facilitate scaling of energies. rcut is designed to build the neighbor
list for calculating the normals for each atom pair.

Note
The parameters presented in the parameter file (e.g. BNCH.ILP),
are fitted with taper function by setting the cutoff equal to 16.0
Angstrom.  Using different cutoff or taper function should be careful.
The parameters for atoms pairs between Boron and Nitrogen are fitted with
a screened Coulomb interaction coul/shield. Therefore,
to simulated the properties of h-BN correctly, this potential must be used in
combination with the pair style coul/shield.

Note
Four new sets of parameters of ILP for 2D layered Materials with bilayer and
bulk configurations are presented in (Ouyang1) and (Ouyang2), respectively.
These parameters provide a good description in both short- and long-range interaction regimes.
While the old ILP parameters published in (Leven2) and
(Maaravi) are only suitable for long-range interaction
regime. This feature is essential for simulations in high pressure
regime (i.e., the interlayer distance is smaller than the equilibrium
distance). The benchmark tests and comparison of these parameters can
be found in (Ouyang1) and (Ouyang2).

This potential must be used in combination with hybrid/overlay.
Other interactions can be set to zero using pair_style none.

This pair style tallies a breakdown of the total interlayer potential
energy into sub-categories, which can be accessed via the compute pair command as a vector of values of length 2.
The 2 values correspond to the following sub-categories:

To print these quantities to the log file (with descriptive column
headings) the following commands could be included in an input script:

compute 0 all pair ilp/graphene/hbn
variable Evdw  equal c_0[1]
variable Erep  equal c_0[2]
thermo_style custom step temp epair v_Erep v_Evdw

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
pair_style  hybrid/overlay ilp/graphene/hbn 16.0 1
pair_coeff  * * ilp/graphene/hbn  BNCH.ILP B N C

pair_style  hybrid/overlay rebo tersoff ilp/graphene/hbn 16.0 coul/shield 16.0
pair_coeff  * * rebo              CH.rebo     NULL NULL C
pair_coeff  * * tersoff           BNC.tersoff B    N    NULL
pair_coeff  * * ilp/graphene/hbn  BNCH.ILP    B    N    C
pair_coeff  1 1 coul/shield 0.70
pair_coeff  1 2 coul/shield 0.695
pair_coeff  2 2 coul/shield 0.69
```

## Restrictions

Restrictions 
This pair style is part of the INTERLAYER package.  It is only enabled
if LAMMPS was built with that package.  See the Build package page for more info.
This pair style requires the newton setting to be on for pair
interactions.
The BNCH.ILP potential file provided with LAMMPS (see the potentials
directory) are parameterized for metal units.  You can use this
potential with any LAMMPS units, but you would need to create your own
custom BNCH.ILP potential file with coefficients listed in the appropriate
units, if your simulation does not use metal units.

## Related Commands

- [pair_coeff](pair_coeff.html)
- [pair_none](pair_none.html)
- [pair_style hybrid/overlay](pair_hybrid.html)
- [pair_style drip](pair_drip.html)
- [pair_style ilp_tmd](pair_ilp_tmd.html)
- [pair_style saip_metal](pair_saip_metal.html)
- [pair_style pair_kolmogorov_crespi_z](pair_kolmogorov_crespi_z.html)
- [pair_style pair_kolmogorov_crespi_full](pair_kolmogorov_crespi_full.html)
- [pair_style pair_lebedeva_z](pair_lebedeva_z.html)
- [pair_style pair_coul_shield](pair_coul_shield.html)

