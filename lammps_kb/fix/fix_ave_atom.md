---
id: fix_ave_atom
title: "fix ave/atom command"
url: https://docs.lammps.org/fix_ave_atom.html
---

# fix ave/atom command

## Syntax

```
fix ID group-ID ave/atom Nevery Nrepeat Nfreq value1 value2 ...
x,y,z,vx,vy,vz,fx,fy,fz = atom attribute (position, velocity, force component)
c_ID = per-atom vector calculated by a compute with ID
c_ID[I] = Ith column of per-atom array calculated by a compute with ID, I can include wildcard (see below)
f_ID = per-atom vector calculated by a fix with ID
f_ID[I] = Ith column of per-atom array calculated by a fix with ID, I can include wildcard (see below)
v_name = per-atom vector calculated by an atom-style variable with name
```

## Description

Use one or more per-atom vectors as inputs every few timesteps, and
average them atom by atom over longer timescales.  The resulting
per-atom averages can be used by other output commands
such as the fix ave/chunk or dump custom
commands.

The group specified with the command means only atoms within the group
have their averages computed.  Results are set to 0.0 for atoms not in
the group.

Each input value can be an atom attribute (position, velocity, force
component) or can be the result of a compute or
fix or the evaluation of an atom-style
variable.  In the latter cases, the compute, fix, or
variable must produce a per-atom vector, not a global quantity or
local quantity.  If you wish to time-average global quantities from a
compute, fix, or variable, then see the fix ave/time
command.

Each per-atom value of each input vector is averaged independently.

Computes that produce per-atom vectors or arrays are
those which have the word atom in their style name.  See the doc
pages for individual fixes to determine which ones produce
per-atom vectors or arrays.  Variables of style atom
are the only ones that can be used with this fix since they produce
per-atom vectors.

Note that for values from a compute or fix, the bracketed index I can
be specified using a wildcard asterisk with the index to effectively
specify multiple values.  This takes the form  *  or  *n  or  m*  or
 m*n .  If \(N\) is the size of the vector (for mode = scalar) or the
number of columns in the array (for mode = vector), then an asterisk
with no numeric values means all indices from 1 to \(N\).  A leading
asterisk means all indices from 1 to n (inclusive).  A trailing
asterisk means all indices from m to \(N\) (inclusive).  A middle asterisk
means all indices from m to n (inclusive).

Using a wildcard is the same as if the individual columns of the array
had been listed one by one.  For example, these two fix ave/atom commands are
equivalent, since the compute stress/atom
command creates a per-atom array with six columns:

compute my_stress all stress/atom NULL
fix 1 all ave/atom 10 20 1000 c_my_stress[*]
fix 1 all ave/atom 10 20 1000 c_my_stress[1] c_my_stress[2] &
                              c_my_stress[3] c_my_stress[4] &
                              c_my_stress[5] c_my_stress[6]

The \(N_\text{every}\), \(N_\text{repeat}\), and \(N_\text{freq}\)
arguments specify on what timesteps the input values will be used in order to
contribute to the average.  The final averaged quantities are generated on
timesteps that are a multiple of \(N_\text{freq}\).  The average is over
\(N_\text{repeat}\) quantities, computed in the preceding portion of the
simulation every \(N_\text{every}\) timesteps.  \(N_\text{freq}\) must
be a multiple of \(N_\text{every}\) and \(N_\text{every}\) must be
non-zero even if \(N_\text{repeat}\) is 1.  Also, the timesteps
contributing to the average value cannot overlap; that is,
\(N_\text{repeat} \times N_\text{every}\) cannot exceed \(N_\text{freq}\).

For example, if \(N_\text{every}=2\), \(N_\text{repeat}=6\), and
\(N_\text{freq}=100\), then values on timesteps 90, 92, 94, 96, 98, and 100
will be used to compute the final average on time step 100.  Similarly for
timesteps 190, 192, 194, 196, 198, and 200 on time step 200, etc.

The atom attribute values (x, y, z, vx, vy, vz, fx, fy, and
fz) are self-explanatory.  Note that other atom attributes can be used as
inputs to this fix by using the
compute property/atom command and then
specifying an input value from that compute.

Note
The x, y, and z attributes are values that are re-wrapped inside
the periodic box whenever an atom crosses a periodic boundary.  Thus, if
you time-average an atom that spends half of its time on either side of
the periodic box, you will get a value in the middle of the box.  If
this is not what you want, consider averaging unwrapped coordinates,
which can be provided by the
compute property/atom
command via its xu, yu, and zu attributes.

If a value begins with  c_ , a compute ID must follow which has been
previously defined in the input script.  If no bracketed term is
appended, the per-atom vector calculated by the compute is used.  If a
bracketed term containing an index \(I\) is appended, the
\(I^\text{th}\) column of the per-atom array calculated by the compute is
used.  Users can also write code for their own compute styles and
add them to LAMMPS.  See the discussion above for how
\(I\) can be specified with a wildcard asterisk to effectively specify
multiple values.

If a value begins with  f_ , a fix ID must follow which has been previously
defined in the input script.  If no bracketed term is appended, the per-atom
vector calculated by the fix is used.  If a bracketed term containing an index
\(I\) is appended, the \(I^\text{th}\) column of the per-atom array
calculated by the fix is used.  Note that some fixes only produce their values
on certain timesteps, which must be compatible with \(N_\text{every}\),
else an error will result.  Users can also write code for their own fix styles
and add them to LAMMPS.  See the discussion above for how
\(I\) can be specified with a wildcard asterisk to effectively specify
multiple values.

If a value begins with  v_ , a variable name must follow which has
been previously defined in the input script as an
atom-style variable. Variables of style atom can reference
thermodynamic keywords or invoke other computes, fixes, or variables
when they are evaluated, so this is a very general means of generating
per-atom quantities to time average.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 1 all ave/atom 1 100 100 vx vy vz
fix 1 all ave/atom 10 20 1000 c_my_stress[1]
fix 1 all ave/atom 10 20 1000 c_my_stress[*]
```

## Restrictions

Restrictions 
none

## Related Commands

- [compute](compute.html)
- [fix ave/histo](fix_ave_histo.html)
- [fix ave/chunk](fix_ave_chunk.html)
- [fix ave/time](fix_ave_time.html)
- [variable](variable.html)

