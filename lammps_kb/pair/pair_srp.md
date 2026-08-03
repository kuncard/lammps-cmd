---
id: pair_srp
title: "pair_style srp command"
url: https://docs.lammps.org/pair_srp.html
---

# pair_style srp command

## Syntax

```
pair_style srp cutoff btype dist keyword value ...
pair_style srp/react cutoff btype dist react-id keyword value ...
bptype value = atom type (numeric or type label) for bond particles
exclude value = yes or no
```

## Description

Style srp computes a soft segmental repulsive potential (SRP) that
acts between pairs of bonds. This potential is useful for preventing
bonds from passing through one another when a soft non-bonded
potential acts between beads in, for example, DPD polymer chains.  An
example input script that uses this command is provided in
examples/PACKAGES/srp.

Bonds of specified type btype interact with one another through a
bond-pairwise potential, such that the force on bond i due to bond
j is as follows

\[F^{\mathrm{SRP}}_{ij} = C(1-r/r_c)\hat{r}_{ij} \qquad r < r_c\]

where r and \(\hat{r}_{ij}\) are the distance and unit vector
between the two bonds.  Note that btype can be specified as an
asterisk  * , which case the interaction is applied to all bond types.
The mid option computes r and \(\hat{r}_{ij}\) from the midpoint
distance between bonds. The min option computes r and
\(\hat{r}_{ij}\) from the minimum distance between bonds. The force
acting on a bond is mapped onto the two bond atoms according to the
lever rule,

\[\begin{split}F_{i1}^{\mathrm{SRP}} & = F^{\mathrm{SRP}}_{ij}(L) \\
F_{i2}^{\mathrm{SRP}} & = F^{\mathrm{SRP}}_{ij}(1-L)\end{split}\]

where L is the normalized distance from the atom to the point of
closest approach of bond i and j. The mid option takes L as
0.5 for each interaction as described in (Sirk).

The following coefficients must be defined via the
pair_coeff command as in the examples above, or in
the data file or restart file read by the read_data
or read_restart commands:

The last coefficient is optional. If not specified, the global cutoff
is used.

Note
Pair style srp considers each bond of type btype to be a
fictitious  particle  of type bptype, where bptype is either the
largest atom type in the system, or the type set by the bptype flag.
Any actual existing particles with this atom type will be deleted at
the beginning of a run. This means you must specify the number of
types in your system accordingly; usually to be one larger than what
would normally be the case, e.g. via the create_box
or by changing the header in your data file.  The
fictitious  bond particles  are inserted at the beginning of the run,
and serve as placeholders that define the position of the bonds.  This
allows neighbor lists to be constructed and pairwise interactions to
be computed in almost the same way as is done for actual particles.
Because bonds interact only with other bonds, pair_style hybrid should be used to turn off interactions
between atom type bptype and all other types of atoms.  An error
will be flagged if pair_style hybrid is not used.

Note
If using type labels, the type labels must be defined before calling
the pair_coeff command.

The optional exclude keyword determines if forces are computed
between first neighbor (directly connected) bonds.  For a setting of
no, first neighbor forces are computed; for yes they are not
computed. A setting of no cannot be used with the min option for
distance calculation because the minimum distance between directly
connected bonds is zero.

Pair style srp turns off normalization of thermodynamic properties
by particle number, as if the command thermo_modify norm no had been issued.

The pairwise energy associated with style srp is shifted to be zero
at the cutoff distance \(r_c\).

Added in version 3Aug2022.

Pair style srp/react interfaces the pair style srp with the
bond breaking and formation mechanisms provided by fix bond/break
and fix bond/create, respectively. When using this pair style, whenever a
bond breaking (or formation) reaction occurs, the corresponding fictitious
particle is deleted (or inserted) during the same simulation time step as
the reaction. This is useful in the simulation of reactive systems involving
large polymeric molecules (Palkar)  where the segmental repulsive
potential is necessary to minimize topological violations, and also needs to be
turned on and off according to the progress of the reaction.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
pair_style hybrid dpd 1.0 1.0 12345 srp 0.8 1 mid exclude yes
pair_coeff 1 1 dpd 60.0 4.5 1.0
pair_coeff 1 2 none
pair_coeff 2 2 srp 100.0 0.8

pair_style hybrid dpd 1.0 1.0 12345 srp 0.8 * min exclude yes
pair_coeff 1 1 dpd 60.0 50 1.0
pair_coeff 1 2 none
pair_coeff 2 2 srp 40.0

fix        create all bond/create   100  1  2  1.0 1 prob  0.2  19852
pair_style hybrid dpd 1.0 1.0 12345 srp/react 0.8 * min create exclude yes
pair_coeff 1 1 dpd 60.0 50 1.0
pair_coeff 1 2 none
pair_coeff 2 2 srp/react 40.0

pair_style hybrid srp 0.8 2 mid
pair_coeff 1 1 none
pair_coeff 1 2 none
pair_coeff 2 2 srp 100.0 0.8

labelmap bond 1 C-C
pair_style hybrid srp 0.8 C-C mid
```

## Restrictions

Restrictions 
This pair style is part of the MISC package. It is only enabled
if LAMMPS was built with that package. See the Making LAMMPS section
for more info.
This pair style must be used with pair_style hybrid.
This pair style requires the newton command to be on
for non-bonded interactions.
This pair style is not compatible with rigid body integrators

## Related Commands

- [pair_style hybrid](pair_hybrid.html)
- [pair_coeff](pair_coeff.html)
- [pair dpd](pair_dpd.html)

