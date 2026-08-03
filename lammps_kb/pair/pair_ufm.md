---
id: pair_ufm
title: "pair_style ufm command"
url: https://docs.lammps.org/pair_ufm.html
---

# pair_style ufm command

## Syntax

```
pair_style ufm cutoff
```

## Description

Style ufm computes pairwise interactions using the Uhlenbeck-Ford model (UFM) potential (Paula Leite2016) which is given by

\[\begin{split}E & = -\varepsilon\, \ln{\left[1-\exp{\left(-r^{2}/\sigma^{2}\right)}\right]} \qquad  r < r_c \\
\varepsilon & = p\,k_B\,T\end{split}\]

where \(r_c\) is the cutoff, \(\sigma\) is a distance-scale and
\(\epsilon\) is an energy-scale, i.e., a product of Boltzmann constant
\(k_B\), temperature \(T\) and the Uhlenbeck-Ford p-parameter which
is responsible
to control the softness of the interactions (Paula Leite2017).
This model is useful as a reference system for fluid-phase free-energy calculations (Paula Leite2016).

The following coefficients must be defined for each pair of atom types
via the pair_coeff command as in the examples above,
or in the data file or restart files read by the
read_data or read_restart
commands, or by mixing as described below:

The last coefficient is optional.  If not specified, the global ufm
cutoff is used.

The fix adapt command can be used to vary epsilon and sigma for this pair style over the course of a simulation, in which case
pair_coeff settings for epsilon and sigma must still be specified, but will be
overridden.  For example these commands will vary the prefactor epsilon for
all pairwise interactions from 10.0 at the beginning to 100.0 at the end
of a run:

variable prefactor equal ramp(10,100)
fix 1 all adapt 1 pair ufm epsilon * * v_prefactor

Note
The thermodynamic integration procedure can be performed with this
potential using fix adapt. This command will
rescale the force on each atom by varying a scale variable, which
always starts with value 1.0. The syntax is the same described above,
however, changing epsilon to scale. A detailed explanation of how to
use this command and perform nonequilibrium thermodynamic integration
in LAMMPS is given in the paper by (Freitas).

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
pair_style ufm 4.0
pair_coeff 1 1 100.0 1.0 2.5
pair_coeff * * 100.0 1.0

pair_style ufm 4.0
pair_coeff * * 10.0 1.0
variable prefactor equal ramp(10,100)
fix 1 all adapt 1 pair ufm epsilon * * v_prefactor
```

## Restrictions

Restrictions 
This pair style is part of the EXTRA-PAIR package.  It is only enabled if
LAMMPS was built with that package.  See the
Build package page for more info.

## Related Commands

- [pair_coeff](pair_coeff.html)
- [fix adapt](fix_adapt.html)

