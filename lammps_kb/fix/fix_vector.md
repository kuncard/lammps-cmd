---
id: fix_vector
title: "fix vector command"
url: https://docs.lammps.org/fix_vector.html
---

# fix vector command

## Syntax

```
fix ID group-ID vector Nevery value1 value2 ... keyword args ...
c_ID = global scalar calculated by a compute with ID
c_ID[I] = Ith component of global vector calculated by a compute with ID
f_ID = global scalar calculated by a fix with ID
f_ID[I] = Ith component of global vector calculated by a fix with ID
v_name = value calculated by an equal-style variable with name
v_name[I] = Ith component of vector-style variable with name
nmax length = set maximal length of vector to <length>
```

## Description

Use one or more global values as inputs every few timesteps, and simply
store them as a sequence.  For a single specified value, the values are
stored as a global vector of growing length.  For multiple specified
values, they are stored as rows in a global array, whose number of rows
is growing.  The resulting vector or array can be used by other
output commands.

The optional nmax keyword can be used to restrict the length of the
vector to the given length value.  Once the restricted vector is
filled, the oldest entry will be discarded when a entry is added.

One way to to use this command is to accumulate a vector that is
numerically integrated using the variable trap()
function. For example, the velocity auto-correlation function (VACF)
can be integrated, to yield a diffusion coefficient, as follows:

compute         2 all vacf
fix             5 all vector 1 c_2[4]
variable        diff equal dt*trap(f_5)
thermo_style    custom step v_diff

The group specified with this command is ignored.  However, note that
specified values may represent calculations performed by computes and
fixes which store their own  group  definitions.

Each listed value can be the result of a compute or
fix or the evaluation of an equal-style or vector-style
variable.  In each case, the compute, fix, or variable
must produce a global quantity, not a per-atom or local quantity.  And
the global quantity must be a scalar, not a vector or array.

Computes that produce global quantities are those which
do not have the word atom in their style name.  Only a few
fixes produce global quantities.  See the doc pages for
individual fixes for info on which ones produce such values.
Variables of style equal or vector are the only
ones that can be used with this fix.  Variables of style atom cannot
be used, since they produce per-atom values.

The Nevery argument specifies on what timesteps the input values
will be used in order to be stored.  Only timesteps that are a
multiple of Nevery, including timestep 0, will contribute values.

Note

If Nevery is a small number and the simulation runs for many
steps, the accumulated vector or array can become very large and
thus consume a lot of memory. The implementation limit is about
2 billion entries. Using the nmax keyword mentioned above can
avoid that by limiting the size of the vector.

Note that if you perform multiple runs, using the  pre no  option of
the run command to avoid initialization on subsequent runs,
then you need to use the stop keyword with the first run
command with a timestep value that encompasses all the runs.  This is
so that the vector or array stored by this fix can be allocated to a
sufficient size.

If a value begins with  c_ , a compute ID must follow which has been
previously defined in the input script.  If no bracketed term is
appended, the global scalar calculated by the compute is used.  If a
bracketed term is appended, the Ith element of the global vector
calculated by the compute is used.

Note that there is a compute reduce command
which can sum per-atom quantities into a global scalar or vector which
can thus be accessed by fix vector.  Or it can be a compute defined not
in your input script, but by thermodynamic output
or other fixes such as fix nvt or fix temp/rescale.  See the doc pages for these commands which give
the IDs of these computes.  Users can also write code for their own
compute styles and add them to LAMMPS.

If a value begins with  f_ , a fix ID must follow which has been
previously defined in the input script.  If no bracketed term is
appended, the global scalar calculated by the fix is used.  If a
bracketed term is appended, the Ith element of the global vector
calculated by the fix is used.

Note that some fixes only produce their values on certain timesteps,
which must be compatible with Nevery, else an error will result.
Users can also write code for their own fix styles and add them to
LAMMPS.

If a value begins with  v_ , a variable name must follow which has
been previously defined in the input script.  An equal-style or
vector-style variable can be referenced; the latter requires a
bracketed term to specify the Ith element of the vector calculated by
the variable.  See the variable command for details.
Note that variables of style equal and vector define a formula
which can reference individual atom properties or thermodynamic
keywords, or they can invoke other computes, fixes, or variables when
they are evaluated, so this is a very general means of specifying
quantities to be stored by fix vector.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 1 all vector 100 c_myTemp
fix 1 all vector 5 c_myTemp v_integral
fix 1 all vector 50 c_myTemp nmax 200
```

## Restrictions

Restrictions 
none

## Related Commands

- [compute](compute.html)
- [variable](variable.html)

