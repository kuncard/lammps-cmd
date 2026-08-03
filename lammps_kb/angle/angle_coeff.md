---
id: angle_coeff
title: "angle_coeff command"
url: https://docs.lammps.org/angle_coeff.html
---

# angle_coeff command

## Syntax

```
angle_coeff N args
```

## Description

Specify the angle force field coefficients for one or more angle types.
The number and meaning of the coefficients depends on the angle style.
Angle coefficients can also be set in the data file read by the
read_data command or in a restart file.

\(N\) can be specified in one of two ways.  An explicit numeric
value can be used, as in the first example above.  Or \(N\) can be a
type label, which is an alphanumeric string defined by the
labelmap command or in a section of a data file read
by the read_data command.

For numeric values only, a wild-card asterisk can be used to set the
coefficients for multiple angle types.  This takes the form  *  or
 *n  or  n*  or  m*n .  If \(N\) is the number of angle types,
then an asterisk with no numeric values means all types from 1 to
\(N\).  A leading asterisk means all types from 1 to n (inclusive).
A trailing asterisk means all types from n to \(N\) (inclusive).  A
middle asterisk means all types from m to n (inclusive).

Note that using an angle_coeff command can
override a previous setting for the same angle type.  For example,
these commands set the coeffs for all angle types, then overwrite the
coeffs for just angle type 2:

angle_coeff * 200.0 107.0 1.2
angle_coeff 2 50.0 107.0

A line in a data file that specifies angle coefficients uses the exact
same format as the arguments of the angle_coeff
command in an input script, except that wild-card asterisks should not
be used since coefficients for all \(N\) types must be listed in the
file.  For example, under the  Angle Coeffs  section of a data file, the
line that corresponds to the first example above would be listed as

1 300.0 107.0

The angle_style class2 is an exception to this
rule, in that an additional argument is used in the input script to
allow specification of the cross-term coefficients.  See its doc page
for details.

The list of all angle styles defined in LAMMPS is given on the
angle_style doc page.  They are also listed in more
compact form on the Commands angle doc page.

On either of those pages, click on the style to display the formula it
computes and its coefficients as specified by the associated
angle_coeff command.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
angle_coeff 1 300.0 107.0
angle_coeff * 5.0
angle_coeff 2*10 5.0

labelmap angle 1 hydroxyl
angle_coeff hydroxyl 300.0 107.0
```

## Restrictions

Restrictions 
This command must come after the simulation box is defined by a
read_data, read_restart, or
create_box command.
An angle style must be defined before any angle coefficients are
set, either in the input script or in a data file.

## Related Commands

- [angle_style](angle_style.html)

