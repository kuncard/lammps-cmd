---
id: fix_restrain
title: "fix restrain command"
url: https://docs.lammps.org/fix_restrain.html
---

# fix restrain command

## Syntax

```
fix ID group-ID restrain keyword args ...
bond args = atom1 atom2 Kstart Kstop r0start (r0stop)
  atom1,atom2 = IDs of two atoms in bond
  Kstart,Kstop = restraint coefficients at start/end of run (energy units)
  r0start = equilibrium bond distance at start of run (distance units)
  r0stop = equilibrium bond distance at end of run (optional) (distance units). If not
    specified it is assumed to be equal to r0start
lbound args = atom1 atom2 Kstart Kstop r0start (r0stop)
  atom1,atom2 = IDs of two atoms in bond
  Kstart,Kstop = restraint coefficients at start/end of run (energy units)
  r0start = equilibrium bond distance at start of run (distance units)
  r0stop = equilibrium bond distance at end of run (optional) (distance units). If not
    specified it is assumed to be equal to r0start
angle args = atom1 atom2 atom3 Kstart Kstop theta0
  atom1,atom2,atom3 = IDs of three atoms in angle, atom2 = middle atom
  Kstart,Kstop = restraint coefficients at start/end of run (energy units)
  theta0 = equilibrium angle theta (degrees)
dihedral args = atom1 atom2 atom3 atom4 Kstart Kstop phi0 keyword/value
  atom1,atom2,atom3,atom4 = IDs of 4 atoms in dihedral in linear order
  Kstart,Kstop = restraint coefficients at start/end of run (energy units)
  phi0 = equilibrium dihedral angle phi (degrees)
  keyword/value = optional keyword value pairs. supported keyword/value pairs:
    mult n = dihedral multiplicity n (integer >= 0, default = 1)
```

## Description

Restrain the motion of the specified sets of atoms by making them part
of a bond or angle or dihedral interaction whose strength can vary
over time during a simulation.  This is functionally similar to
creating a bond or angle or dihedral for the same atoms in a data
file, as specified by the read_data command, albeit
with a time-varying prefactor coefficient, and except for exclusion
rules, as explained below.

For the purpose of force field parameter-fitting or mapping a molecular
potential energy surface, this fix reduces the hassle and risk
associated with modifying data files.  In other words, use this fix to
temporarily force a molecule to adopt a particular conformation.  To
create a permanent bond or angle or dihedral, you should modify the
data file.

Note
Adding a bond/angle/dihedral with this command does not apply
the exclusion rules and weighting factors specified by the
special_bonds command to atoms in the restraint
that are now bonded (1-2,1-3,1-4 neighbors) as a result.  If they are
close enough to interact in a pair_style sense
(non-bonded interaction), then the bond/angle/dihedral restraint
interaction will simply be superposed on top of that interaction.

The group-ID specified by this fix is ignored.

The second example above applies a restraint to hold the dihedral
angle formed by atoms 1, 2, 3, and 4 near 120 degrees using a constant
restraint coefficient.  The fourth example applies similar restraints
to multiple dihedral angles using a restraint coefficient that
increases from 0.0 to 2000.0 over the course of the run.

Note
Adding a force to atoms implies a change in their potential
energy as they move due to the applied force field.  For dynamics via
the run command, this energy can be added to the system s
potential energy for thermodynamic output (see below).  For energy
minimization via the minimize command, this energy
must be added to the system s potential energy to formulate a
self-consistent minimization problem (see below).

In order for a restraint to be effective, the restraint force must
typically be significantly larger than the forces associated with
conventional force field terms.  If the restraint is applied during a
dynamics run (as opposed to during an energy minimization), a large
restraint coefficient can significantly reduce the stable timestep
size, especially if the atoms are initially far from the preferred
conformation.  You may need to experiment to determine what value of \(K\)
works best for a given application.

For the case of finding a minimum energy structure for a single
molecule with particular restraints (e.g. for fitting force field
parameters or constructing a potential energy surface), commands such
as the following may be useful:

# minimize molecule energy with restraints
velocity all create 600.0 8675309 mom yes rot yes dist gaussian
fix NVE all nve
fix TFIX all langevin 600.0 0.0 100 24601
fix REST all restrain dihedral 2 1 3 8 0.0 5000.0 ${angle1} dihedral 3 1 2 9 0.0 5000.0 ${angle2}
fix_modify REST energy yes
run 10000
fix TFIX all langevin 0.0 0.0 100 24601
fix REST all restrain dihedral 2 1 3 8 5000.0 5000.0 ${angle1} dihedral 3 1 2 9 5000.0 5000.0 ${angle2}
fix_modify REST energy yes
run 10000
# sanity check for convergence
minimize 1e-6 1e-9 1000 100000
# report unrestrained energies
unfix REST
run 0

The bond keyword applies a bond restraint to the specified atoms
using the same functional form used by the bond_style harmonic command.  The potential associated with
the restraint is

\[E = K (r - r_0)^2\]

with the following coefficients:

\(K\) and \(r_0\) are specified with the fix.  Note that the usual 1/2 factor
is included in \(K\).

The lbound keyword applies a lower bound bond restraint to the specified atoms
using the same functional form used by the bond_style harmonic command if the distance between
the atoms is smaller than the equilibrium bond distance and 0 otherwise. The potential associated with
the restraint is

\[E = K (r - r_0)^2 ,if\;r < r_0\]

\[E = 0 \qquad\quad\quad ,if\;r \ge r_0\]

with the following coefficients:

\(K\) and \(r_0\) are specified with the fix.  Note that the usual 1/2 factor
is included in \(K\).

The angle keyword applies an angle restraint to the specified atoms
using the same functional form used by the angle_style harmonic command.  The potential associated with
the restraint is

\[E = K (\theta - \theta_0)^2\]

with the following coefficients:

\(K\) and \(\theta_0\) are specified with the fix.
\(\theta_0\) is specified in degrees, but LAMMPS converts it to
radians internally; hence \(K\) is effectively energy per
radian^2.  Note that the usual 1/2 factor is included in \(K\).

The dihedral keyword applies a dihedral restraint to the specified
atoms using a simplified form of the function used by the
dihedral_style charmm command.  The potential
associated with the restraint is

\[E = K [ 1 + \cos (n \phi - d) ]\]

with the following coefficients:

\(K\) and \(\phi_0\) are specified with the fix.  Note that the value of the
dihedral multiplicity \(n\) is set by default to 1. You can use the
optional mult keyword to set it to a different positive integer.
Also note that the energy will be a minimum when the
current dihedral angle \(\phi\) is equal to \(\phi_0\).

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix holdem all restrain bond 45 48 2000.0 2000.0 2.75
fix holdem all restrain lbound 45 48 2000.0 2000.0 2.75
fix holdem all restrain dihedral 1 2 3 4 2000.0 2000.0 120.0
fix holdem all restrain bond 45 48 2000.0 2000.0 2.75 dihedral 1 2 3 4 2000.0 2000.0 120.0
fix texas_holdem all restrain dihedral 1 2 3 4 0.0 2000.0 120.0 dihedral 1 2 3 5 0.0 2000.0 -120.0 dihedral 1 2 3 6 0.0 2000.0 0.0
```

## Restrictions

Restrictions 
none

## Related Commands

Related commands 
none

