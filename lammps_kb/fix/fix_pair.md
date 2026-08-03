---
id: fix_pair
title: "fix pair command"
url: https://docs.lammps.org/fix_pair.html
---

# fix pair command

## Syntax

```
fix ID group-ID pair N pstyle name flag ...
```

## Description

Added in version 15Sep2022.

Extract per-atom quantities from a pair style and store them in this
fix so they can be accessed by other LAMMPS commands, e.g. by a
dump command or by another fix,
compute, or variable command.

These are example use cases:

The N argument determines how often the fix is invoked.

The pstyle argument is the name of the pair style.  It can be a
sub-style used in a pair_style hybrid command.  If
there are multiple sub-styles using the same pair style, then pstyle
should be specified as  style:N , where N is the number of the
instance of the pair style you wish monitor (e.g., the first or second).
For example, pstyle could be specified as  pace/extrapolation  or
 amoeba  or  eam:1  or  eam:2 .

One or more name/flag pairs of arguments follow.  Each name is a
per-atom quantity which the pair style must recognize as an extraction
request.  See the doc pages for individual pair_styles to see what fix pair requests (if any) they support.

The flag setting determines whether this fix will also trigger the
pair style to compute the named quantity so it can be extracted.  If the
quantity is always computed by the pair style, no trigger is needed;
specify flag = 0.  If the quantity is not always computed
(e.g. because it is expensive to calculate), then specify flag = 1.
This will trigger the quantity to be calculated only on timesteps it is
needed.  Again, see the doc pages for individual pair_styles to determine which fix pair requests (if any) need to be
triggered with a flag = 1 setting.

The per-atom data extracted from the pair style is stored by this fix
as either a per-atom vector or array.  If there is only one name
argument specified and the pair style computes a single value for each
atom, then this fix stores it as a per-atom vector.  Otherwise a
per-atom array is created, with its data in the order of the name
arguments.

For example, pair_style amoeba allows extraction of
two named quantities:  uind  and  uinp , both of which are 3-vectors for
each atom, i.e. dipole moments. In the example below a 6-column per-atom
array will be created.  Columns 1-3 will store the  uind  values;
columns 4-6 will store the  uinp  values.

pair_style amoeba
fix ex all pair 10 amoeba uind 0 uinp 0

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix request all pair 100 eam rho 0
fix request all pair 100 amoeba uind 0 uinp 0
```

## Restrictions

Restrictions 
none

## Related Commands

- [compute pair](compute_pair.html)

