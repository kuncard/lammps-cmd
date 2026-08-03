---
id: compute_slice
title: "compute slice command"
url: https://docs.lammps.org/compute_slice.html
---

# compute slice command

## Syntax

```
compute ID group-ID slice Nstart Nstop Nskip input1 input2 ...
c_ID = global vector calculated by a compute with ID
c_ID[I] = Ith column of global array calculated by a compute with ID
f_ID = global vector calculated by a fix with ID
f_ID[I] = Ith column of global array calculated by a fix with ID
v_name = vector calculated by an vector-style variable with name
```

## Description

Define a calculation that  slices  one or more vector inputs into
smaller vectors, one per listed input.  The inputs can be global
quantities; they cannot be per-atom or local quantities.
Computes and fixes and vector-style
variables can generate such global quantities.  The
group specified with this command is ignored.

The values extracted from the input vector(s) are determined by the
Nstart, Nstop, and Nskip parameters.  The elements of an input
vector of length N are indexed from 1 to N.  Starting at element
Nstart, every Mth element is extracted, where M = Nskip, until
element Nstop is reached.  The extracted quantities are stored as a
vector, which is typically shorter than the input vector.

Each listed input is operated on independently to produce one output
vector.  Each listed input must be a global vector or column of a
global array calculated by another compute or
fix.

If an input value begins with  c_ , a compute ID must follow which has
been previously defined in the input script and which generates a
global vector or array.  See the individual compute doc
page for details.  If no bracketed integer is appended, the vector
calculated by the compute is used.  If a bracketed integer is
appended, the Ith column of the array calculated by the compute is
used.  Users can also write code for their own compute styles and add them to LAMMPS.

If a value begins with  f_ , a fix ID must follow which has been
previously defined in the input script and which generates a global
vector or array.  See the individual fix page for
details.  Note that some fixes only produce their values on certain
timesteps, which must be compatible with when compute slice references
the values, else an error results.  If no bracketed integer is
appended, the vector calculated by the fix is used.  If a bracketed
integer is appended, the Ith column of the array calculated by the fix
is used.  Users can also write code for their own fix style and add them to LAMMPS.

If an input value begins with  v_ , a variable name must follow which
has been previously defined in the input script.  Only vector-style
variables can be referenced.  See the variable command
for details.  Note that variables of style vector define a formula
which can reference individual atom properties or thermodynamic
keywords, or they can invoke other computes, fixes, or variables when
they are evaluated, so this is a very general means of specifying
quantities to slice.

If a single input is specified this compute produces a global vector,
even if the length of the vector is 1.  If multiple inputs are
specified, then a global array of values is produced, with the number
of columns equal to the number of inputs specified.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 all slice 1 100 10 c_msdmol[4]
compute 1 all slice 301 400 1 c_msdmol[4] v_myVec
```

## Restrictions

Restrictions 
none

## Related Commands

- [compute](compute.html)
- [fix](fix.html)
- [compute reduce](compute_reduce.html)

