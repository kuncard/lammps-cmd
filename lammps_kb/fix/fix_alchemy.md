---
id: fix_alchemy
title: "fix alchemy command"
url: https://docs.lammps.org/fix_alchemy.html
---

# fix alchemy command

## Syntax

```
fix ID group-ID alchemy v_name
```

## Description

Added in version 28Mar2023.

This fix command enables an  alchemical transformation  to be performed
between two systems, whereby one system slowly transforms into the other
over the course of a molecular dynamics run.  This is useful for
measuring thermodynamic differences between two different systems.  It
also allows transformations that are not easily possible with the
pair style hybrid/scaled, fix adapt or fix adapt/fep commands.

Example inputs are included in the examples/PACKAGES/alchemy
directory for (a) transforming a pure copper system into a
copper/aluminum bronze alloy and (b) transforming two water molecules
in a box of water into a hydronium and a hydroxyl ion.

The two systems must be defined as separate replica and run in separate partitions of processors using the
-partition command-line switch.  Exactly two
partitions must be specified, and each partition must use the same number
of processors and the same domain decomposition.

Because the forces applied to the atoms are the same mix of the forces
from each partition and the simulation starts with the same atom
positions across both partitions, they will generate the same trajectory
of coordinates for each atom, and the same simulation box size and
shape.  The latter two conditions are enforced by this fix; it
exchanges coordinates and box information between the replicas.  This is
not strictly required, but since MD simulations are an example of a
chaotic system, even the tiniest random difference will eventually grow
exponentially into an unwanted divergence.

Otherwise, the properties of each atom (type, charge, bond and angle
partners, etc.), as well as energy and forces between interacting atoms
(pair, bond, angle styles, etc.) can be different in the two systems.

This can be initialized in the same input script by using commands which
only apply to one or the other replica.  The example scripts use a
world-style variable command along with
if/then/else commands for this purpose.  The
partition command can also be used.

create_box 2 box
create_atoms 1 box
pair_style eam/alloy
pair_coeff * * AlCu.eam.alloy Cu Al

# replace 5% of copper with aluminum on the second partition only

variable name world pure alloy
if "${name} == alloy" then &
  "set type 1 type/fraction 2 0.05 6745234"

Both replicas must define an instance of this fix, but with a different
v_name variable.  The named variable must be an equal-style or
equivalent variable.  The two variables should be
defined so that one ramps down from 1.0 to 0.0 for the first replica
(R=0) and the other ramps up from 0.0 to 1.0 for the second
replica (R=1).  A simple way is to do this is linearly, which can be
done using the ramp() function of the variable
command.  You could also define a variable which returns a value between
0.0 and 1.0 as a non-linear function of the timestep.  Here is a linear
example:

partition yes 1 variable ramp equal ramp(1.0,0.0)
partition yes 2 variable ramp equal ramp(0.0,1.0)
fix 2 all alchemy v_ramp

Note
For an alchemical transformation, the two variables should sum to
exactly 1.0 at any timestep.  LAMMPS does NOT check that this is
the case.

If you use the ramp() function to define the two variables, this fix
can easily be used across successive runs in the same input script by
ensuring each instance of the run command specifies the
appropriate start or stop options.

At each timestep of an MD run, the two instances of this fix evaluate
their respective variables as a \(\lambda_R\) factor, where R = 0
or 1 for each replica.  The forces used by each system for the
propagation of their atoms is set to the sum of the forces for the two
systems, each scaled by their respective \(\lambda_R\) factor.  Thus,
during the MD run, the system will transform incrementally from the
first system to the second system.

Note
As mentioned above, the coordinates of the atoms and box size/shape
must be exactly the same in the two replicas.  Therefore, it is
generally not a good idea to initialize the two replicas by reading
different data files or creating them individually from scratch.
Rather, a single system should be initialized and then desired
modifications applied to the system to either replica.  If your
input script somehow induces the two systems to become different
(e.g. by performing atom_modify sort
differently, or by adding or depositing a different number of atoms),
then LAMMPS will detect the mismatch and generate an error.  This is
done by ensuring that each step the number and ordering of atoms is
identical within each pair of processors in the two replicas.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix trans all alchemy v_ramp
```

## Restrictions

Restrictions 
This fix is part of the REPLICA package.  It is only enabled if LAMMPS
was built with that package.  See the Build package page for more info.
There may be only one instance of this fix in use at a time within
each replica.

## Related Commands

- [compute pressure/alchemy](compute_pressure_alchemy.html)
- [fix adapt](fix_adapt.html)
- [fix adapt/fep](fix_adapt_fep.html)
- [pair_style hybrid/scaled](pair_hybrid.html)

