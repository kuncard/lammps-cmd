---
id: pair_tracker
title: "pair_style tracker command"
url: https://docs.lammps.org/pair_tracker.html
---

# pair_style tracker command

## Syntax

```
pair_style tracker fix_ID N keyword values attribute1 attribute2 ...
finite value = none
   pair style uses atomic diameters to identify contacts
time/min value = T
   T = minimum number of timesteps of interaction
type/include value = list1 list2
   list1,list2 = separate lists of types (see below)
possible attributes = id1 id2 time/created time/broken time/total
                      r/min r/ave x y z
id1, id2 = IDs of the two atoms in each pair interaction
time/created = the timestep that the two atoms began interacting
time/broken = the timestep that the two atoms stopped interacting
time/total = the total number of timesteps the two atoms interacted
r/min = the minimum radial distance between the two atoms during the interaction (distance units)
r/ave = the average radial distance between the two atoms during the interaction (distance units)
x, y, z = the center of mass position of the two atoms when they stopped interacting (distance units)
```

## Description

Style tracker monitors information about pairwise interactions.  It
does not calculate any forces on atoms. Pair hybrid/overlay can be used to combine this pair style with any other
pair style, as shown in the examples above.

At each timestep, if two neighboring atoms move beyond the interaction
cutoff, pairwise data is processed and transferred to an internal fix
labeled fix_ID. This allows the local data to be accessed by other
LAMMPS commands. Additional
filters can be applied using the time/min or type/include keywords
described below.  Note that this is the interaction cutoff defined by
this pair style, not the short-range cutoff defined by the pair style
that is calculating forces on atoms.

Following any optional keyword/value arguments, a list of one or more
attributes is specified.  These include the IDs of the two atoms in
the pair.  The other attributes for the pair of atoms are the
duration of time they were  interacting  or at the point in time they
started or stopped interacting.  In this context,  interacting  means
the time window during which the two atoms were closer than the
interaction cutoff distance.  The attributes for time/* refer to
timesteps.

Data is continuously accumulated by the internal fix over intervals of N
timesteps. At the end of each interval, all of the saved accumulated
data is deleted to make room for new data. Individual datum may
therefore persist anywhere between 1 to N timesteps depending on
when they are saved. This data can be accessed using the fix_ID and a
dump local command. To ensure all data is output,
the dump frequency should correspond to the same interval of N
timesteps. A dump frequency of an integer multiple of N can be used
to regularly output a sample of the accumulated data.

The following optional keywords may be used.

If the finite keyword is not used, the following coefficients must
be defined for each pair of atom types via the pair_coeff command as in the examples above, or in the data file or
restart files read by the read_data or
read_restart commands, or by mixing as described
below:

If the finite keyword is used, there are no additional coefficients
to set for each pair of atom types via the
pair_coeff command. Interaction cutoffs are
instead calculated based on the diameter of finite particles. However
you must still use the pair_coeff for all atom
types. For example the command

pair_coeff * *

should be used.

The time/min keyword sets a minimum amount of time that an
interaction must persist to be included.  This setting can be used to
exclude short-lived interactions.

The type/include keyword filters interactions based on the types of
the two atoms.  Data is only saved for interactions between atoms
whose two atom types appear in list1 and list2.  Atom type 1 must
be in list1 and atom type 2 in list2.  Or vice versa.

Each type list consists of a series of type ranges separated by
commas.  Each range can be specified as a single numeric value, or a
wildcard asterisk can be used to specify a range of values.  This
takes the form  *  or  *n  or  n*  or  m*n .  For example, if M =
the number of atom types, then an asterisk with no numeric values
means all types from 1 to M.  A leading asterisk means all types from
1 to n (inclusive).  A trailing asterisk means all types from n to M
(inclusive).  A middle asterisk means all types from m to n
(inclusive).  Note that the type/include keyword can be specified
multiple times.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
pair_style hybrid/overlay tracker myfix 1000 id1 id2 type/include 1 * type/include 2 3,4  lj/cut 2.5
pair_coeff 1 1 tracker 2.0

pair_style hybrid/overlay tracker myfix 1000 finite x y z time/min 100 granular
pair_coeff * * tracker

dump 1 all local 1000 dump.local f_myfix[1] f_myfix[2] f_myfix[3]
dump_modify 1 write_header no
```

## Restrictions

Restrictions 
This pair style is part of the MISC package.  It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.
This pair style is currently incompatible with granular pair styles
that extend beyond the contact (e.g. JKR and DMT).

## Related Commands

Related commands

