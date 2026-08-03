---
id: compute_born_matrix
title: "compute born/matrix command"
url: https://docs.lammps.org/compute_born_matrix.html
---

# compute born/matrix command

## Syntax

```
compute ID group-ID born/matrix keyword value ...
keyword = numdiff or pair or bond or angle or dihedral or improper
  numdiff values = delta virial-ID
    delta = magnitude of strain (dimensionless)
    virial-ID = ID of pressure compute for virial (string)
    (numdiff cannot be used with any other keyword)
  pair = compute pair-wise contributions
  bond = compute bonding contributions
  angle = compute angle contributions
  dihedral = compute dihedral contributions
  improper = compute improper contributions
```

## Description

Added in version 4May2022.

Define a compute that calculates
\(\frac{\partial{}^2U}{\partial\varepsilon_{i}\partial\varepsilon_{j}},\) the
second derivatives of the potential energy \(U\) with respect to the strain
tensor \(\varepsilon\) elements. These values are related to:

\[C^{B}_{i,j}=\frac{1}{V}\frac{\partial{}^2U}{\partial{}\varepsilon_{i}\partial\varepsilon_{j}}\]

also called the Born term of elastic constants in the stress-stress fluctuation
formalism. This quantity can be used to compute the elastic constant tensor.
Using the symmetric Voigt notation, the elastic constant tensor can be written
as a 6x6 symmetric matrix:

\[C_{i,j} = \langle{}C^{B}_{i,j}\rangle
         + \frac{V}{k_{B}T}\left(\langle\sigma_{i}\sigma_{j}\rangle\right.
         \left.- \langle\sigma_{i}\rangle\langle\sigma_{j}\rangle\right)
         + \frac{Nk_{B}T}{V}
           \left(\delta_{i,j}+(\delta_{1,i}+\delta_{2,i}+\delta_{3,i})\right.
           \left.*(\delta_{1,j}+\delta_{2,j}+\delta_{3,j})\right)\]

In the above expression, \(\sigma\) stands for the virial stress
tensor, \(\delta\) is the Kronecker delta and the usual notation apply for
the number of particle, the temperature and volume respectively \(N\),
\(T\) and \(V\). \(k_{B}\) is the Boltzmann constant. For a
more detailed explanation of the terms appearing in the above equation,
see (Lutsko).

The Born term is a symmetric 6x6 matrix, as is the matrix of second derivatives
of potential energy w.r.t strain,
whose 21 independent elements are output in this order:

\[\begin{split}\begin{bmatrix}
   C_{1}  & C_{7}   & C_{8}  & C_{9}  & C_{10} & C_{11} \\
   C_{7}  & C_{2}   & C_{12} & C_{13} & C_{14} & C_{15} \\
   \vdots & C_{12}  & C_{3}  & C_{16} & C_{17} & C_{18} \\
   \vdots & C_{13}  & C_{16} & C_{4}  & C_{19} & C_{20} \\
   \vdots & \vdots  & \vdots & C_{19} & C_{5}  & C_{21} \\
   \vdots & \vdots  & \vdots & \vdots & C_{21} & C_{6}
\end{bmatrix}\end{split}\]

in this matrix the indices of \(C_{k}\) value are the corresponding element
\(k\) in the global vector output by this compute. Each term comes from the sum
of the derivatives of every contribution to the potential energy
in the system as explained in (VanWorkum).

The output can be accessed using the usual LAMMPS routines:

compute 1 all born/matrix
compute 2 all pressure NULL virial
variable S1 equal -c_2[1]
variable S2 equal -c_2[2]
variable S3 equal -c_2[3]
variable S4 equal -c_2[6]
variable S5 equal -c_2[5]
variable S6 equal -c_2[4]
fix 1 all ave/time 1 1 1 v_S1 v_S2 v_S3 v_S4 v_S5 v_S6 c_1[*] file born.out

Note interchange of 4th and 6th stress values to satisfy Voigt notation.
In this example, the file born.out will contain the information needed to
compute the first and second terms of the elastic constant matrix in a post
processing procedure. The third term depends only on T, which can
be specified directly or estimated by sampling the atom velocities.
Several examples of this method are
provided in the examples/ELASTIC_T/BORN_MATRIX directory
described on the Examples doc page.

NOTE: In the above \(C_{i,j}\) computation, the fluctuation
term involving the virial stress tensor \(\sigma\) is the
covariance between each elements. In a
solid the stress fluctuations can vary rapidly, while average
fluctuations can be slow to converge.
A detailed analysis of the convergence rate of all the terms in
the elastic tensor
is provided in the paper by Clavier et al. (Clavier).

Two different computation methods for the Born matrix are implemented in this
compute and are mutually exclusive.

The first one is a direct computation from the analytical formula from the
different terms of the potential used for the simulations (VanWorkum). However, the implementation of such derivations must be done
for every potential form. This has not been done yet and can be very
complicated for complex potentials. At the moment a warning message is
displayed for every term that is not supporting the compute at the moment.
This method is the default for now.

The second method uses finite differences of energy to numerically approximate
the second derivatives (Zhen). This is useful when using
interaction styles for which the analytical second derivatives have not been
implemented. In this cases, the compute applies linear strain fields of
magnitude delta to all the atoms relative to a point at the center of the
box. The strain fields are in six different directions, corresponding to the
six Cartesian components of the stress tensor defined by LAMMPS. For each
direction it applies the strain field in both the positive and negative senses,
and the new stress virial tensor of the entire system is calculated after each.
The difference in these two virials divided by two times delta, approximates
the corresponding components of the second derivative, after applying a
suitable unit conversion.

Note
It is important to choose a suitable value for delta, the magnitude of
strains that are used to generate finite difference
approximations to the exact virial stress.  For typical systems, a value in
the range of 1 part in 1e5 to 1e6 will be sufficient.
However, the best value will depend on a multitude of factors
including the stiffness of the interatomic potential, the thermodynamic
state of the material being probed, and so on. The only way to be sure
that you have made a good choice is to do a sensitivity study on a
representative atomic configuration, sweeping over a wide range of
values of delta. If delta is too small, the output values will vary
erratically due to truncation effects. If delta is increased beyond a
certain point, the output values will start to vary smoothly with
delta, due to growing contributions from higher order derivatives. In
between these two limits, the numerical virial values should be largely
independent of delta.

The keyword requires the additional arguments delta and virial-ID.
delta gives the size of the applied strains. virial-ID gives
the ID string of the pressure compute that provides the virial stress tensor,
requiring that it use the virial keyword e.g.

compute myvirial all pressure NULL virial
compute 1 all born/matrix numdiff 1.0e-4 myvirial

Output info:

This compute calculates a global vector with 21 values that are
the second derivatives of the potential energy with respect to strain.
The values are in energy units.
The values are ordered as explained above. These values can be used
by any command that uses global values from a compute as input. See
the Howto output doc page for an overview of
LAMMPS output options.

The array values calculated by this compute are all  extensive .

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 all born/matrix
compute 1 all born/matrix bond angle
compute 1 all born/matrix numdiff 1.0e-4 myvirial
```

## Restrictions

Restrictions 
This compute is part of the EXTRA-COMPUTE package.  It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.  LAMMPS was built with that package.  See
the Build package page for more info.
The Born term can be decomposed as a product of two terms. The first one is a
general term which depends on the configuration. The second one is specific to
every interaction composing your force field (non-bonded, bonds, angle,  ).
Currently not all LAMMPS interaction styles implement the born_matrix method
giving first and second order derivatives and LAMMPS will exit with an error if
this compute is used with such interactions unless the numdiff option is
also used. The numdiff option cannot be used with any other keyword. In this
situation, LAMMPS will also exit with an error.

