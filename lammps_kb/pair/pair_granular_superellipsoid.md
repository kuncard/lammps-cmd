---
id: pair_granular_superellipsoid
title: "pair_style granular/superellipsoid command"
url: https://docs.lammps.org/pair_granular_superellipsoid.html
---

# pair_style granular/superellipsoid command

## Syntax

```
pair_style granular/superellipsoid cutoff no_bounding_box curvature_gaussian

Optional settings, see discussion below.
* cutoff = global cutoff value
* no_bounding_box = skip oriented bounding box check
* curvature_gaussian = gaussian curvature coeff approximation for contact patch
```

## Description

Added in version 30Mar2026.

The granular/superellipsoid style calculates granular contact forces
between superellipsoidal particles (see atom style ellipsoid).  Similar to the granular pairstyle which is designed for spherical particles, various
normal, damping, and tangential contact models are available (rolling
and twisting may be added later).  The total computed forces and torques
are the sum of various models selected.

All model choices and parameters are entered in the pair_coeff command, as described below.  Coefficient values are not
global, but can be set to different values for different combinations of
particle types, as determined by the pair_coeff
command.  If the contact model choice is the same for two particle
types, the mixing for the cross-coefficients can be carried out
automatically.  This is shown in the last example, where model choices
are the same for type 1 - type 1 as for type 2 - type2 interactions, but
coefficients are different.  In this case, the mixed coefficients for
type 1 - type 2 interactions can be determined from mixing rules
discussed below.  For additional flexibility, coefficients as well as
model forms can vary between particle types.

This pair_style allows granular contact between two superellipsoid
particles whose surface is implicitly defined as:

\[f(\mathbf{x}) = \left(
\left|\frac{x}{a}\right|^{n_2} + \left|\frac{y}{b}\right|^{n_2}
\right)^{n_1 / n_2}
+ \left|\frac{z}{c}\right|^{n_1} - 1 = 0\]

for a point \(\mathbf{x} = (x, y, z)\) where the coordinates are
given in the reference of the principal directions of inertia of the
particle.  The half-diameters \(a\), \(b\), and \(c\)
correspond to the shape property, and the exponents \(n_1\) and
\(n_2\) to the block property of the ellipsoid atom.  See the doc
page for the set command for more details.

Note
The contact solver strictly requires convex particle shapes to
ensure a mathematically unique point of deepest penetration.
Therefore, the blockiness parameters must be \(n_1 \ge 2.0\) and
\(n_2 \ge 2.0\).  Attempting to simulate concave or  pointy 
particles (\(n < 2.0\)) will result in an error.

Note
For particles with high blockiness exponents (\(n > 4.0\))
involved in edge-to-edge or corner-to-corner contacts, the surface
normal vector varies rapidly over small distances.  The Newton
solver may occasionally fail to converge to the strict gradient
alignment tolerance (typically \(10^{-10}\)).  You may see
warning messages in the log indicating that the solver returned a
sub-optimal solution, but the simulation will proceed using this
best-effort contact point.

Contact detection for these aspherical particles uses the so-called
 midway  minimization approach from (Houlsby).
Considering two particles with shape functions, \(F_i\) and
\(F_j\), the contact point \(\mathbf{X}_0\) in the global frame
is obtained as:

\[\mathbf{X}_0 = \underset{\mathbf{X}}{\text{argmin}}
               \ F_i(\mathbf{X}) + F_j(\mathbf{X})
               \text{, subject to } F_i(\mathbf{X}) = F_j(\mathbf{X})\]

where the shape function is given by \(F_i(\mathbf{X}) =
f_i(\mathbf{R}_i^T (\mathbf{X} - \mathbf{X}_i))\) and where
\(\mathbf{X}_i\) and \(\mathbf{R}_i\) are the center of mass and
rotation matrix of the particle, respectively.  The constrained
minimization problem is solved using Lagrange multipliers and Newton s
method with a line search as described by (Podlozhnyuk).

Note
The shape function \(F\) is not a signed distance function and
does not have unit gradient \(\|\nabla F \| \neq 1\) so that the
so-called  midway  point is not actually located at an equal
distance from the surface of both particles.  For contact between
non-identical particles, the contact point tends to be closer to the
surface of the smaller and blockier particle.

Note
This formulation leads to a 4x4 system of non-linear equations.
Tikhonov regularization and step clumping is used to ensure
robustness of the direct solver and high convergence rate, even for
blocky particles with near flat faces.

The particles overlap if both shape functions are negative at the
contact point.  The contact normal is obtained as:
\(\mathbf{n}_{ij} = \nabla F_i(\mathbf{X}_0) / \| \nabla
F_i(\mathbf{X}_0)\| = - \nabla F_j(\mathbf{X}_0) / \| \nabla
F_j(\mathbf{X}_0)\|\) and the overlap \(\delta =
\|\mathbf{X}_j^{\mathrm{surf}} - \mathbf{X}_i^{\mathrm{surf}}\|\) is
computed as the distance between the points on the particles surfaces
that are closest to the contact point in the direction of the contact
normal: \(F_i(\mathbf{X}_i^{\mathrm{surf}} = \mathbf{X}_0 +
\lambda_i \mathbf{n}_{ij}) = 0\) and
\(F_j(\mathbf{X}_j^{\mathrm{surf}} = \mathbf{X}_0 + \lambda_j
\mathbf{n}_{ij}) = 0\).  Newton s method is used to solve this equation
for the scalars \(\lambda_i\) and \(\lambda_j\) and find the
surface points \(\mathbf{X}_i^{\mathrm{surf}}\) and
\(\mathbf{X}_j^{\mathrm{surf}}\).

Note
A modified representation of the particle surface is defined as
\(G(\mathbf{X}) = (F(\mathbf{X})+1)^{1/n_1}-1\) which is a
quasi-radial distance function formulation.  This formulation is used
to compute the surface points once the  midway  contact point is
found.  This formulation is also used when the geometric keyword is
specified in the pair_style command and the following optimization
problem is solved instead for the contact point: \(\mathbf{X}_0
= \underset{\mathbf{X}}{\text{argmin}} \, \left( r_i
G_i(\mathbf{X}) + r_j G_j(\mathbf{X}) \right) \text{, subject to }
r_i G_i(\mathbf{X}) = r_j G_j(\mathbf{X})\), where \(r_i\) and
\(r_j\) are the average radii of the two particles.  The
geometric formulation thus yields a better approximation of the
contact point for particles with different sizes, and it is slightly
more robust for particles with high block exponents, albeit more
computationally expensive.

A hierarchical approach is used to limit the cost of contact detection.
First, intersection of the bounding spheres of the two particles of
bounding radii \(r_i\) and \(r_j\) is checked.  If the distance
between the particles center is more than the sum of the radii
\(\|\mathbf{X}_j - \mathbf{X}_j\| > r_i + r_j\), the particles do
not intersect.  Then, if the bounding spheres intersect, intersection of
the oriented bounding box is checked.  This is done following the
equations of (Eberly).  This check is always
performed, unless the no_bounding_box keyword is used.  This is
advantageous for all particle shapes except for superellipses with
aspect ratio close to one and both blockiness indexes close to 2.

Warning
The Newton-Raphson minimization used to find the midway contact
point can fail to converge if the initial starting guess is too far
from the true physical surface.  This typically occurs if a user
specifies a manual global cutoff that is significantly larger than
the particles and enables the no_bounding_box keyword.  Under
these conditions, the solver attempts to resolve contacts between
widely separated particles, which might cause the math to diverge
and instantly crashing the simulation.  It is strongly recommended
to keep bounding box checks enabled if a large cutoff is specified.

This section provides an overview of the various normal, tangential, and
damping contact models available.  For additional context, see the
discussion in the granular pairstyle doc page
which includes all of these options.

The first required keyword for the pair_coeff command is the normal
contact model.  Currently supported options for normal contact models
and their required arguments are:

Here, \(k_n\) is spring stiffness (with units that depend on model
choice, see below); \(\eta_{n0}\) is a damping prefactor (or, in its
place a coefficient of restitution \(e\), depending on the choice of
damping mode, see below).

For the hooke model, the normal, elastic component of force acting on
particle i due to contact with particle j is given by:

\[\mathbf{F}_{ne, Hooke} = k_n \delta_{ij} \mathbf{n}\]

Where \(\delta_{ij}\) is the particle overlap, (note the i-j
ordering so that \(\mathbf{F}_{ne}\) is positive for repulsion), and
\(\mathbf{n}\) is the contact normal vector at the contact point.
Therefore, for hooke, the units of the spring constant \(k_n\) are
force/distance, or equivalently mass/time^2.

For the hertz model, the normal component of force is given by:

\[\mathbf{F}_{ne, Hertz} = k_n R_{eff}^{1/2}\delta_{ij}^{3/2} \mathbf{n}\]

Here, \(R_{eff} = R = \frac{R_i R_j}{R_i + R_j}\) is the effective
radius, and \(R_i\) is the equivalent radius of the i-th particle at
the surface contact point with the j-th particle.  This radius is either
the inverse of the mean curvature coefficient, \(R_i = 2 /
(\kappa_1 + \kappa_2)\), or the gaussian curvature coefficient \(R_i
= 1 / \sqrt{\kappa_1 \kappa_2}\), where \(\kappa_{1,2}\) are the
principal curvatures of the particle surface at the contact point.  For
hertz, the units of the spring constant \(k_n\) are force/length^2, or equivalently pressure.

Note
To ensure numerical stability and preserve physical realism, the
computed contact radius is mathematically capped.  For highly blocky
particles undergoing flat-on-flat contact, the theoretical curvature
approaches zero, which would yield an infinite contact radius and
cause a force explosion.  To prevent this, the maximum contact
radius is capped at the physical bounding radius of the smallest
interacting particle.  Conversely, for sharp corner contacts where
curvature approaches infinity, the calculated radius would drop to
zero, eliminating the repulsive force entirely.  The contact radius
is therefore lower-bounded by a minimum fraction of the physical
radius (\(10^{-4} \min(r_i, r_j)\)) to prevent particles from
unphysically interpenetrating.

In addition, the normal force is augmented by a damping term of the
following general form:

\[\mathbf{F}_{n,damp} = -\eta_n \mathbf{v}_{n,rel}\]

Here, \(\mathbf{v}_{n,rel} = (\mathbf{v}_j - \mathbf{v}_i) \cdot
\mathbf{n}\ \mathbf{n}\) is the component of relative velocity along
\(\mathbf{n}\).

The optional damping keyword to the pair_coeff command followed by a
keyword determines the model form of the damping factor \(\eta_n\),
and the interpretation of the \(\eta_{n0}\) or \(e\)
coefficients specified as part of the normal contact model settings.
The damping keyword and corresponding model form selection may be
appended anywhere in the pair coeff command.  Note that the choice of
damping model affects both the normal and tangential damping.  The
options for the damping model currently supported are:

If the damping keyword is not specified, the viscoelastic model is
used by default.

For damping mass_velocity, the normal damping is given by:

\[\eta_n = \eta_{n0} m_{eff}\]

Here, \(\eta_{n0}\) is the damping coefficient specified for the
normal contact model, in units of 1/time and \(m_{eff} = m_i
m_j/(m_i + m_j)\) is the effective mass.  Use damping mass_velocity to
reproduce the damping behavior of pair gran/hooke/*.

The damping viscoelastic model is based on the viscoelastic treatment
of (Brilliantov et al), where the normal damping is
given by:

\[\eta_n = \eta_{n0}\ a m_{eff}\]

Here, a is the contact radius, given by \(a =\sqrt{R\delta}\) for
all models.  For damping viscoelastic, \(\eta_{n0}\) is in units
of 1/(time*distance).

The total normal force is computed as the sum of the elastic and damping
components:

\[\mathbf{F}_n = \mathbf{F}_{ne} + \mathbf{F}_{n,damp}\]

The pair_coeff command also requires specification of the tangential
contact model.  The required keyword tangential is expected, followed
by the model choice and associated parameters.  Currently there is only
one supported tangential model with expected parameters as follows:

Here, \(x_{\gamma,t}\) is a dimensionless multiplier for the normal
damping \(\eta_n\) that determines the magnitude of the tangential
damping, \(\mu_t\) is the tangential (or sliding) friction
coefficient, and \(k_t\) is the tangential stiffness coefficient.

The tangential damping force \(\mathbf{F}_\mathrm{t,damp}\) is given
by:

\[\mathbf{F}_\mathrm{t,damp} = -\eta_t \mathbf{v}_{t,rel}\]

The tangential damping prefactor \(\eta_t\) is calculated by scaling
the normal damping \(\eta_n\) (see above):

\[\eta_t = -x_{\gamma,t} \eta_n\]

The normal damping prefactor \(\eta_n\) is determined by the choice
of the damping keyword, as discussed above.  Thus, the damping
keyword also affects the tangential damping.  The parameter
\(x_{\gamma,t}\) is a scaling coefficient.  Several works in the
literature use \(x_{\gamma,t} = 1\) (Marshall,
Tsuji et al, Silbert et al).
The relative tangential velocity at the point of contact is given by
\(\mathbf{v}_{t, rel} = \mathbf{v}_{t} -
(R_i\boldsymbol{\Omega}_i + R_j\boldsymbol{\Omega}_j) \times
\mathbf{n}\), where \(\mathbf{v}_{t} = \mathbf{v}_r -
\mathbf{v}_r\cdot\mathbf{n}\ \mathbf{n}\), \(\mathbf{v}_r =
\mathbf{v}_j - \mathbf{v}_i\) .
The normal force value \(F_{n0}\) used to compute the critical force
depends on the form of the contact model.  It is given by the magnitude
of the normal force:

\[F_{n0} = \|\mathbf{F}_n\|\]

The remaining tangential options all use accumulated tangential
displacement (i.e. contact history).  The accumulated tangential
displacement is discussed in details below in the context of the
linear_history option.  The same treatment of the accumulated
displacement will apply to other (future) options as well.

For tangential linear_history, the tangential force is given by:

\[\mathbf{F}_t =  \min(\mu_t F_{n0}, \|-k_t\mathbf{\xi} + \mathbf{F}_\mathrm{t,damp}\|) \mathbf{t}\]

Here, \(\mathbf{t}\) is the direction of the tangential force given by:

\[\mathbf{t} = \frac{-k_t\mathbf{\xi} + \mathbf{F}_\mathrm{t,damp}}{\|-k_t\mathbf{\xi} + \mathbf{F}_\mathrm{t,damp}\|}\]

and, \(\mathbf{\xi}\) is the tangential displacement accumulated
during the entire duration of the contact:

\[\mathbf{\xi} = \int_{t0}^t \mathbf{v}_{t,rel}(\tau) \mathrm{d}\tau\]

This accumulated tangential displacement must be adjusted to account for
changes in the frame of reference of the contacting pair of particles
during contact.  This occurs due to the overall motion of the contacting
particles in a rigid-body-like fashion during the duration of the
contact.  There are two modes of motion that are relevant: the
 tumbling  rotation of the contacting pair, which changes the
orientation of the plane in which tangential displacement occurs; and
 spinning  rotation of the contacting pair about the vector connecting
their centers of mass (\(\mathbf{n}\)).  Corrections due to the
former mode of motion are made by rotating the accumulated displacement
into the plane that is tangential to the contact vector at each step, or
equivalently removing any component of the tangential displacement that
lies along \(\mathbf{n}\), and rescaling to preserve the magnitude.
This follows the discussion in Luding, see equation
17 and relevant discussion in that work:

\[\mathbf{\xi} = \left(\mathbf{\xi'} - (\mathbf{n} \cdot \mathbf{\xi'})\mathbf{n}\right) \frac{\|\mathbf{\xi'}\|}{\|\mathbf{\xi'} - (\mathbf{n}\cdot\mathbf{\xi'})\mathbf{n}\|}\]

Here, \(\mathbf{\xi'}\) is the accumulated displacement prior to the
current time step and \(\mathbf{\xi}\) is the corrected
displacement.  Corrections to the displacement due to the second mode of
motion described above (rotations about \(\mathbf{n}\)) are not
currently implemented, but are expected to be minor for most
simulations.

Furthermore, when the tangential force exceeds the critical force, the
tangential displacement is re-scaled to match the value for the critical
force (see Luding, equation 20 and related
discussion):

\[\mathbf{\xi} = -\frac{1}{k_t}\left(\mu_t F_{n0}\mathbf{t} - \mathbf{F}_{t,damp}\right)\]

The tangential force is added to the total normal force (elastic plus
damping) to produce the total force on the particle.

Unlike perfect spheres, the surface normal at the contact point of a
superellipsoid does not generally pass through the particle s center of
mass.  Therefore, both the normal and tangential forces act at the
contact point to induce a torque on each particle.

Using the exact contact point \(\mathbf{X}_0\) determined by the
geometric solver, the branch vectors from the particle centers of mass
to the contact point are defined as \(\mathbf{r}_{ci} =
\mathbf{X}_0 - \mathbf{x}_i\) and \(\mathbf{r}_{cj} = \mathbf{X}_0 -
\mathbf{x}_j\).  The resulting torques are calculated as:

\[\mathbf{\tau}_i = \mathbf{r}_{ci} \times \mathbf{F}_{tot}\]

\[\mathbf{\tau}_j = -\mathbf{r}_{cj} \times \mathbf{F}_{tot}\]

If two particles are moving away from each other while in contact, there
is a possibility that the particles could experience an effective
attractive force due to damping.  If the optional limit_damping
keyword is used, this option will zero out the normal component of the
force if there is an effective attractive force.

LAMMPS automatically sets pairwise cutoff values for pair_style
granular/superellipsoid based on particle radii.  In the vast majority
of situations, this is adequate.  However, a cutoff value can optionally
be appended to the pair_style granular/superellipsoid command to
specify a global cutoff (i.e.  a cutoff for all atom types).  This
option may be useful in some rare cases where the automatic cutoff
determination is not sufficient.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
pair_style granular/superellipsoid
pair_coeff * * hooke 1000.0 50.0 tangential linear_history 1000.0 1.0 0.5 damping mass_velocity

pair_style granular/superellipsoid 10.0 curvature_gaussian
pair_coeff 1 1 hertz 1000.0 50.0 tangential linear_history 500.0 1.0 0.4 damping viscoelastic
pair_coeff 2 2 hertz 500.0 50.0 tangential linear_history 250.0 1.0 0.1 damping viscoelastic
```

## Restrictions

Restrictions 
The atom_style must be set to ellipsoid superellipsoid to enable
superellipsoid particles  shape parameters (3 lengths and two blockiness
parameters), see atom_style for more details.
This pair style require Newton s third law be set to off for pair
interactions.
There are currently no versions of fix wall/gran or fix
wall/gran/region that are compatible with superellipsoid particles.
This pair style is part of the ASPHERE package.  It is only enabled if
LAMMPS was built with that package.  See the Build package page for more info.
This pair style requires that atoms store per-particle bounding radius,
shapes, blockiness, inertia, torque, and angular momentum (omega) as
defined by the atom_style ellipsoid superellipsoid.
This pair style requires you to use the comm_modify vel yes command so that velocities are stored by ghost atoms.
This pair style will not restart exactly when using the
read_restart command, though it should provide
statistically similar results.  This is because the forces it computes
depend on atom velocities and the atom velocities have been propagated
half a timestep between the force computation and when the restart is
written, due to using Velocity Verlet time integration.  See the
read_restart command for more details.
Accumulated values for individual contacts are saved to restart files
but are not saved to data files.  Therefore, forces may differ
significantly when a system is reloaded using the read_data command.

## Related Commands

- [pair_coeff](pair_coeff.html)
- [pair granular](pair_granular.html)

