---
id: fix_external
title: "fix external command"
url: https://docs.lammps.org/fix_external.html
---

# fix external command

## Syntax

```
fix ID group-ID external mode args
pf/callback args = Ncall Napply
  Ncall = make callback every Ncall steps
  Napply = apply callback forces every Napply steps
pf/array args = Napply
  Napply = apply array forces every Napply steps
```

## Description

This fix allows external programs that are running LAMMPS through its
library interface to modify certain LAMMPS
properties on specific timesteps, similar to the way other fixes do.
The external driver can be a C/C++ or Fortran program or a Python script.

If mode is pf/callback then the fix will make a callback every
Ncall timesteps or minimization iterations to the external program.
The external program computes forces on atoms by setting values in an
array owned by the fix.  The fix then adds these forces to each atom
in the group, once every Napply steps, similar to the way the fix addforce command works.  Note that if Ncall >
Napply, the force values produced by one callback will persist, and
be used multiple times to update atom forces.

The callback function  foo  is invoked by the fix as:

foo(void *ptr, bigint timestep, int nlocal, tagint *ids, double **x, double **fexternal);

The arguments are as follows:

Note that timestep is a  bigint  which is defined in src/lmptype.h,
typically as a 64-bit integer. And ids is a pointer to type  tagint 
which is typically a 32-bit integer unless LAMMPS is compiled with
-DLAMMPS_BIGBIG. For more info please see the build settings section of the manual.  Finally, fexternal are the forces
returned by the driver program.

The best way to set up the callback function is to use the C-language
library interface function lammps_set_fix_external_callback().

If mode is pf/array then the fix simply stores force values in an
array.  The fix adds these forces to each atom in the group, once
every Napply steps, similar to the way the fix addforce command works.

The name of the public force array provided by the FixExternal
class is

double **fexternal;

It is allocated by the FixExternal class as an (N,3) array where N is
the number of atoms owned by a processor.  The 3 corresponds to the
fx, fy, fz components of force.

It is up to the external program to set the values in this array to
the desired quantities, as often as desired.  For example, the driver
program might perform an MD run in stages of 1000 timesteps each.  In
between calls to the LAMMPS run command, it could retrieve
atom coordinates from LAMMPS, compute forces, set values in fexternal,
etc.

To use this fix during energy minimization, the energy corresponding
to the added forces must also be set so as to be consistent with the
added forces.  Otherwise the minimization will not converge correctly.
Correspondingly, the global virial needs to be updated to be use this
fix with variable cell calculations (e.g. fix box/relax
or fix npt).

This can be done from the external driver by calling these public
methods of the FixExternal class:

void set_energy_global(double eng);
void set_virial_global(double *virial);

where eng is the potential energy, and virial an array of the 6
stress tensor components.  Eng is an extensive quantity,
meaning it should be the sum over per-atom energies of all affected
atoms.  It should also be provided in energy units
consistent with the simulation.  See the details below for how to
ensure this energy setting is used appropriately in a minimization.

Additional public methods that the caller can use to update system
properties are:

void set_energy_peratom(double *eng);
void set_virial_peratom(double **virial);
void set_vector_length(int n);
void set_vector(int idx, double val);

These enable setting per-atom energy and  per-atom stress contributions,
the length and individual values of a global vector of properties that
the caller code may want to communicate  to LAMMPS
(e.g. for use in fix ave/time or in
equal-style variables or for
custom thermo output.

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
fix 1 all external pf/callback 1 1
fix 1 all external pf/callback 100 1
fix 1 all external pf/array 10
```

## Restrictions

Restrictions 
none

## Related Commands

Related commands 
none

