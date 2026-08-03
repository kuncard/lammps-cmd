---
id: pair_aip_water_2dm
title: "pair_style aip/water/2dm command"
url: https://docs.lammps.org/pair_aip_water_2dm.html
---

# pair_style aip/water/2dm command

## Syntax

```
pair_style [hybrid/overlay ...] aip/water/2dm cutoff tap_flag
```

## Description

Added in version 15Jun2023.

The aip/water/2dm style computes the anisotropic interfacial potential
(AIP) potential for interfaces of water with two-dimensional (2D)
materials as described in (Feng1) and (Feng2).

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
larger than \(r_c\) pair_style ilp_graphene_hbn.

Note
This pair style uses the atomic normal vector definition from
(Feng1)), where the atomic normal vectors of the
hydrogen atoms are assumed to lie along the corresponding
oxygen-hydrogen bonds and the normal vector of the central oxygen
atom is defined as their average.

The provided parameter file, CBNOH.aip.water.2dm, is intended for use
with metal units, with energies in meV.  Two additional
parameters, S, and rcut are included in the parameter file. S is
designed to facilitate scaling of energies; rcut is the cutoff for an
internal, short distance neighbor list that is generated for speeding up
the calculation of the normals for all atom pairs.

Note
The parameters presented in the provided parameter file,
CBNOH.aip.water.2dm, are fitted with the taper function enabled by
setting the cutoff equal to 16.0 Angstrom.  Using a different cutoff
or taper function setting should be carefully checked as they can
lead to significant errors.  These parameters provide a good
description in both short- and long-range interaction regimes. This
is essential for simulations in high pressure regime (i.e., the
interlayer distance is smaller than the equilibrium distance).

This potential must be used in combination with hybrid/overlay.  Other
interactions can be set to zero using pair_coeff settings with the pair style set to none.

This pair style tallies a breakdown of the total interlayer potential
energy into sub-categories, which can be accessed via the compute
pair command as a vector of values of length 2.  The 2
values correspond to the following sub-categories:

To print these quantities to the log file (with descriptive column
headings) the following commands could be included in an input script:

compute 0 all pair aip/water/2dm
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
pair_style  hybrid/overlay aip/water/2dm 16.0 1
pair_coeff  * * aip/water/2dm  CBNOH.aip.water.2dm C Ow Hw

pair_style  hybrid/overlay aip/water/2dm 16.0 lj/cut/tip4p/long 2 3 1 1 0.1546 10 8.5
pair_coeff  2 2   lj/cut/tip4p/long    8.0313e-3  3.1589      # O-O
pair_coeff  2 3   lj/cut/tip4p/long    0.0        0.0         # O-H
pair_coeff  3 3   lj/cut/tip4p/long    0.0        0.0         # H-H
pair_coeff  * *   aip/water/2dm        CBNOH.aip.water.2dm    C Ow Hw

pair_style  hybrid/overlay aip/water/2dm 16.0 lj/cut/tip4p/long 3 4 1 1 0.1546 10 8.5 coul/shield 16.0 1
pair_coeff  1*2 1*2   none
pair_coeff  3 3   lj/cut/tip4p/long    8.0313e-3  3.1589      # O-O
pair_coeff  3 4   lj/cut/tip4p/long    0.0        0.0         # O-H
pair_coeff  4 4   lj/cut/tip4p/long    0.0        0.0         # H-H
pair_coeff  * *   aip/water/2dm        CBNOH.aip.water.2dm  B N Ow Hw
pair_coeff  1 3   coul/shield          1.333
pair_coeff  1 4   coul/shield          1.333
pair_coeff  2 3   coul/shield          1.333
pair_coeff  2 4   coul/shield          1.333
```

## Restrictions

Restrictions 
This pair style is part of the INTERLAYER package.  It is only enabled
if LAMMPS was built with that package.  See the Build package page for more info.
This pair style requires the newton setting to be on for pair
interactions.
The CBNOH.aip.water.2dm potential file provided with LAMMPS is
parameterized for metal units.  You can use this pair style with any
LAMMPS units, but you would need to create your own potential file with
parameters in the appropriate units, if your simulation does not use
metal units.

## Related Commands

- [pair_coeff](pair_coeff.html)
- [pair_none](pair_none.html)
- [pair_style hybrid/overlay](pair_hybrid.html)
- [pair_style drip](pair_drip.html)
- [pair_style ilp_tmd](pair_ilp_tmd.html)
- [pair_style saip_metal](pair_saip_metal.html)
- [pair_style ilp_graphene_hbn](pair_ilp_graphene_hbn.html)
- [pair_style pair_kolmogorov_crespi_z](pair_kolmogorov_crespi_z.html)
- [pair_style pair_kolmogorov_crespi_full](pair_kolmogorov_crespi_full.html)
- [pair_style pair_lebedeva_z](pair_lebedeva_z.html)
- [pair_style pair_coul_shield](pair_coul_shield.html)

