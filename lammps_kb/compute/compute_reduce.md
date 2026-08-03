---
id: compute_reduce
title: "compute reduce command"
url: https://docs.lammps.org/compute_reduce.html
---

# compute reduce command

## Syntax

```
compute ID group-ID style arg mode input1 input2 ... keyword args ...
reduce arg = none
reduce/region arg = region-ID
  region-ID = ID of region to use for choosing atoms
x,y,z,vx,vy,vz,fx,fy,fz = atom attribute (position, velocity, force component)
c_ID = per-atom or local vector calculated by a compute with ID
c_ID[I] = Ith column of per-atom or local array calculated by a compute with ID, I can include wildcard (see below)
f_ID = per-atom or local vector calculated by a fix with ID
f_ID[I] = Ith column of per-atom or local array calculated by a fix with ID, I can include wildcard (see below)
v_name = per-atom vector calculated by an atom-style variable with name
replace args = vec1 vec2
  vec1 = reduced value from this input vector will be replaced
  vec2 = replace it with vec1[N] where N is index of max/min value from vec2
inputs arg = peratom or local
  peratom = all inputs are per-atom quantities (default)
  local = all input are local quantities
```

## Description

Define a calculation that  reduces  one or more vector inputs into
scalar values, one per listed input.  For the compute reduce command,
the inputs can be either per-atom or local quantities and must all be
of the same kind (per-atom or local); see discussion of the optional
inputs keyword below.  The compute reduce/region command can only be
used with per-atom inputs.

Atom attributes are per-atom quantities, computes and
fixes can generate either per-atom or local quantities,
and atom-style variables generate per-atom
quantities.  See the variable command and its
special functions which can perform the same reduction operations as
the compute reduce command on global vectors.

The reduction operation is specified by the mode setting.  The sum
option adds the values in the vector into a global total.  The min
or max options find the minimum or maximum value across all vector
values.  The minabs or maxabs options find the minimum or maximum
value across all absolute vector values.  The ave setting adds the
vector values into a global total, then divides by the number of
values in the vector.  The sumsq option sums the square of the
values in the vector into a global total.  The avesq setting does
the same as sumsq, then divides the sum of squares by the number of
values.  The last two options can be useful for calculating the
variance of some quantity (e.g., variance = avesq \(-\) ave\(^2\)).  The sumabs option sums the absolute values in the
vector into a global total.  The aveabs setting does the same as
sumabs, then divides the sum of absolute values by the number of
values.

Each listed input is operated on independently.  For per-atom inputs,
the group specified with this command means only atoms within the
group contribute to the result.  Likewise for per-atom inputs, if the
compute reduce/region command is used, the atoms must also currently
be within the region.  Note that an input that produces per-atom
quantities may define its own group which affects the quantities it
returns.  For example, if a compute is used as an input which
generates a per-atom vector, it will generate values of 0.0 for atoms
that are not in the group specified for that compute.

Each listed input can be an atom attribute (position, velocity, force
component) or can be the result of a compute or
fix or the evaluation of an atom-style
variable.

Note that for values from a compute or fix, the bracketed index \(I\) can
be specified using a wildcard asterisk with the index to effectively
specify multiple values.  This takes the form  *  or  *n  or  m*  or
 m*n .  If \(N\) is the size of the vector (for mode = scalar) or the
number of columns in the array (for mode = vector), then an asterisk
with no numeric values means all indices from 1 to \(N\).  A leading
asterisk means all indices from 1 to n (inclusive).  A trailing
asterisk means all indices from m to \(N\) (inclusive).  A middle asterisk
means all indices from m to n (inclusive).

Using a wildcard is the same as if the individual columns of the array
had been listed one by one. For example, the following two compute reduce
commands are equivalent, since the
compute stress/atom command creates a per-atom
array with six columns:

compute myPress all stress/atom NULL
compute 2 all reduce min c_myPress[*]
compute 2 all reduce min c_myPress[1] c_myPress[2] c_myPress[3] &
                         c_myPress[4] c_myPress[5] c_myPress[6]

The atom attribute values (x, y, z, vx, vy, vz, fx,
fy, and fz) are self-explanatory.  Note that other atom attributes
can be used as inputs to this fix by using the compute
property/atom command and then specifying an
input value from that compute.

If a value begins with  c_ , a compute ID must follow which has been
previously defined in the input script.  Valid computes can generate
per-atom or local quantities.  See the individual compute page for details.  If no bracketed integer is appended, the
vector calculated by the compute is used.  If a bracketed integer is
appended, the Ith column of the array calculated by the compute is
used.  Users can also write code for their own compute styles and
add them to LAMMPS.  See the discussion above for how
\(I\) can be specified with a wildcard asterisk to effectively
specify multiple values.

If a value begins with  f_ , a fix ID must follow which has been
previously defined in the input script.  Valid fixes can generate
per-atom or local quantities.  See the individual fix
page for details.  Note that some fixes only produce their values on
certain timesteps, which must be compatible with when compute reduce
references the values, else an error results.  If no bracketed integer
is appended, the vector calculated by the fix is used.  If a bracketed
integer is appended, the Ith column of the array calculated by the fix
is used.  Users can also write code for their own fix style and
add them to LAMMPS.  See the discussion above for how
\(I\) can be specified with a wildcard asterisk to effectively
specify multiple values.

If a value begins with  v_ , a variable name must follow which has
been previously defined in the input script.  It must be an
atom-style variable.  Atom-style variables can
reference thermodynamic keywords and various per-atom attributes, or
invoke other computes, fixes, or variables when they are evaluated, so
this is a very general means of generating per-atom quantities to
reduce.

If the replace keyword is used, two indices vec1 and vec2 are
specified, where each index ranges from 1 to the number of input
values.  The replace keyword can only be used if the mode is min
or max.  It works as follows.  A min/max is computed as usual on
the vec2 input vector.  The index \(N\) of that value within
vec2 is also stored.  Then, instead of performing a min/max on the
vec1 input vector, the stored index is used to select the \(N\)th element of the vec1 vector.

Thus, for example, if you wish to use this compute to find the bond
with maximum stretch, you can do it as follows:

compute batoms all property/local batom1 batom2
compute blength all bond/local dist
compute 3 all reduce max c_batoms[1] c_batoms[2] c_blength replace 1 3 replace 2 3 inputs local
thermo_style custom step temp c_3[1] c_3[2] c_3[3]

The first two input values in the compute reduce command are vectors
with the IDs of the two atoms in each bond, using the
compute property/local command.  The last input
value is bond distance, using the
compute bond/local command.  Instead of taking the
max of the two atom ID vectors, which does not yield useful
information in this context, the replace keywords will extract the
atom IDs for the two atoms in the bond of maximum stretch.  These atom
IDs and the bond stretch will be printed with thermodynamic output.

Added in version 21Nov2023.

The inputs keyword allows selection of whether all the inputs are
per-atom or local quantities.  As noted above, all the inputs must be
the same kind (per-atom or local).  Per-atom is the default setting.  If
a compute or fix is specified as an input, it must produce per-atom or
local data to match this setting.  If it produces both, like for example
the compute voronoi/atom command, then
this keyword selects between them.  If a compute only produces local
data, like for example the compute bond/local command, the setting  inputs local  is required.

If a single input is specified this compute produces a global scalar
value.  If multiple inputs are specified, this compute produces a
global vector of values, the length of which is equal to the number of
inputs specified.

As discussed below, for the sum, sumabs, and sumsq modes, the
value(s) produced by this compute are all  extensive , meaning their
value scales linearly with the number of atoms involved.  If
normalized values are desired, this compute can be accessed by the
thermo_style custom command with
thermo_modify norm yes set as an option.  Or it
can be accessed by a variable that divides by the
appropriate atom count.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
compute 1 all reduce sum c_force
compute 1 all reduce/region subbox sum c_force
compute 2 all reduce min c_press[2] f_ave v_myKE
compute 2 all reduce min c_press[*] f_ave v_myKE inputs peratom
compute 3 fluid reduce max c_index[1] c_index[2] c_dist replace 1 3 replace 2 3
compute 4 all reduce max c_bond inputs local
```

## Restrictions

Restrictions 
As noted above, the compute reduce/region command can only be used
with per-atom inputs.

## Related Commands

- [compute](compute.html)
- [fix](fix.html)
- [variable](variable.html)

