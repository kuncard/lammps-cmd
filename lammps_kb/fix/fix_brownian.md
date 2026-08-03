---
id: fix_brownian
title: "fix brownian command"
url: https://docs.lammps.org/fix_brownian.html
---

# fix brownian command

## Syntax

```
fix ID group-ID style_name temp seed keyword args
rng value = uniform or gaussian or none
  uniform = use uniform random number generator
  gaussian = use gaussian random number generator
  none = turn off noise
dipole value = mux and muy and muz for brownian/asphere
  mux, muy, and muz = update orientation of dipole having direction (mux,*muy*,*muz*) in body frame of rigid body
gamma_r_eigen values = gr1 and gr2 and gr3 for brownian/asphere
  gr1, gr2, and gr3 = diagonal entries of body frame rotational friction tensor
gamma_r values = gr for brownian/sphere
  gr = magnitude of the (isotropic) rotational friction tensor
gamma_t_eigen values = gt1 and gt2 and gt3 for brownian/asphere
  gt1, gt2, and gt3 = diagonal entries of body frame translational friction tensor
gamma_t values = gt for brownian and brownian/sphere
   gt = magnitude of the (isotropic) translational friction tensor
rotation_style values = geometric or projection for brownian/sphere
   geometric = geometric, rotation-based integration scheme
   projection = projection-based integration scheme
rotation_temp values = T for brownian/sphere and brownian/asphere
   T = rotation temperature, which can be different than temp when out of equilibrium
planar_rotation values = none (constrains rotational diffusion to be in xy plane if in 3D)
```

## Description

Perform Brownian Dynamics time integration to update position, velocity,
dipole orientation (for spheres) and quaternion orientation (for
ellipsoids, with optional dipole update as well) of all particles in the
fix group in each timestep.  Brownian Dynamics uses Newton s laws of
motion in the limit that inertial forces are negligible compared to
viscous forces. The stochastic equation of motion for the center of mass
positions is

\[d\mathbf{r} = \boldsymbol{\gamma}_t^{-1}\mathbf{F}dt
+ \sqrt{2k_B T}\boldsymbol{\gamma}_t^{-1/2}d\mathbf{W}_t,\]

in the lab-frame (i.e., \(\boldsymbol{\gamma}_t\) is not diagonal, but
only depends on orientation and so the noise is still additive).

The overdamped rotational motion for the spherical and ellipsoidal particles
results from random rotations instead of translations, which are chosen in such
a way that the motion reproduces the equilibrium Boltzmann distribution for the
case of conservative torques (see (Hoefling), (Ilie), and (Delong)).

For the style brownian, only the positions of the particles are
updated. This is therefore suitable for point particle simulations.

For the style brownian/sphere, the positions of the particles are
updated, and a dipole slaved to the spherical orientation is also
updated. This style therefore requires the hybrid atom style
atom_style dipole and atom_style sphere. The equation of motion for the dipole is

\[\boldsymbol{\mu}(t+dt) = \mathrm{R}(\boldsymbol{\omega} dt) \, \boldsymbol{\mu}(t) \,,\]

where \(\mathrm{R}(\boldsymbol{\omega} dt)\) is a rotation matrix with axis
\(\boldsymbol{n} = \boldsymbol{\omega} / |\boldsymbol{\omega}|\)
and angle \(\theta = |\boldsymbol{\omega}| dt\) (see (Hoefling)).
For small angles, the action of the rotation matrix can be cast into a
tangential increment \(\boldsymbol{\omega} \times \boldsymbol{\mu}dt\) and
subsequent projection to preserve the magnitude \(|\boldsymbol{\mu}(t)|\) of
the dipole (see (Ilie)):

\[\boldsymbol{\mu}(t+dt) = |\boldsymbol{\mu}(t)| \,
   \frac{\boldsymbol{\mu}(t) + \boldsymbol{\omega} \times \boldsymbol{\mu}dt
   }{|\boldsymbol{\mu}(t) + \boldsymbol{\omega} \times \boldsymbol{\mu}dt|}\,.\]

For suitable time step \(dt\), both expressions were shown to correctly
reproduce the Boltzmann distribution of orientations and rotational diffusion
moments when

\[\boldsymbol{\omega} = \frac{\mathbf{T}}{\gamma_r} + \sqrt{\frac{2 k_B T_{rot}}{\gamma_r}\frac{d\mathbf{W}}{dt}},\]

with \(d\mathbf{W}\) being a random number with zero mean and variance
\(dt\) and \(T_{rot}\) is rotation_temp. The geometric integration
scheme, however, accepts time steps that can be an order of magnitude larger
(see (Hoefling)).

For the style brownian/asphere, the center of mass positions and the
quaternions of ellipsoidal particles are updated. This fix style is
suitable for equations of motion where the rotational and translational
friction tensors can be diagonalized in a certain (body) reference
frame. In this case, the rotational equation of motion is updated via
the quaternion

\[\mathbf{q}(t+dt) = \frac{\mathbf{q}(t) + d\mathbf{q}}{\lVert\mathbf{q}(t) + d\mathbf{q}\rVert}\]

which correctly reproduces a Boltzmann distribution of orientations and rotational
diffusion moments [see (Ilie)] when the quaternion step is given by

\[d\mathbf{q} = \boldsymbol{\Psi}\boldsymbol{\omega}dt\]

where \(\boldsymbol{\Psi}\) has rows \((-q_1,-q_2,-q_3)\),
\((q_0,-q_3,q_2)\), \((q_3,q_0,-q_1)\), and \((-q_2,q_1,q_0)\).
\(\boldsymbol{\omega}\) is evaluated in the body frame of reference where the
friction tensor is diagonal.  See (Delong) for more details of
a similar algorithm.

Note
This integrator does not by default assume a relationship between the
rotational and translational friction tensors, though such a
relationship should exist in the case of no-slip boundary conditions
between the particles and the surrounding (implicit) solvent. For example,
in the case of spherical particles, the condition
\(\gamma_t=3\gamma_r/\sigma^2\) must be explicitly accounted for
by setting gamma_t to 3x and gamma_r to x (where \(\sigma\)
is the sphere s diameter). A similar (though more complex)
relationship holds for ellipsoids and rod-like particles. The
translational diffusion and rotational diffusion are given by
temp/gamma_t and rotation_temp/gamma_r.

Note
Temperature computation using the compute temp
will not correctly compute the temperature of these overdamped dynamics
since we are explicitly neglecting inertial effects.  Furthermore,
this time integrator does not add the stochastic terms or viscous
terms to the force and/or torques.  Rather, they are just added in to
the equations of motion to update the degrees of freedom.

If the rng keyword is used with the uniform value, then the noise
is generated from a uniform distribution (see
(Dunweg) for why this works). This is the same method
of noise generation as used in fix_langevin.

If the rng keyword is used with the gaussian value, then the noise
is generated from a Gaussian distribution. Typically this added
complexity is unnecessary, and one should be fine using the uniform
value for reasons argued in (Dunweg).

If the rng keyword is used with the none value, then the noise
terms are set to zero.

The gamma_t keyword sets the (isotropic) translational viscous damping.
Required for (and only compatible with) brownian and brownian/sphere.
The units of gamma_t are mass/time.

The gamma_r keyword sets the (isotropic) rotational viscous damping.
Required for (and only compatible with) brownian/sphere.
The units of gamma_r are mass*length**2/time.

The gamma_r_eigen, and gamma_t_eigen keywords are the eigenvalues of
the rotational and viscous damping tensors (having the same units as
their isotropic counterparts). Required for (and only compatible with)
brownian/asphere. For a 2D system, the first two values of
gamma_r_eigen must be inf (only rotation in x y plane), and the third
value of gamma_t_eigen must be inf (only diffusion in the x y plane).

If the dipole keyword is used, then the dipole moments of the particles
are updated as described above. Only compatible with brownian/asphere
(as brownian/sphere updates dipoles automatically).

Added in version 11Feb2026.

If the rotation_style keyword is used with the geometric value, then the
geometric, rotation-based integration scheme ((Hoefling))
is used. If the keyword is used with the projection value, the linearized,
projection-based scheme ((Ilie)) is used. Only
compatible with brownian/sphere.

Note: rotation_style projection reproduces the legacy behavior (the former default).

If the rotation_temp keyword is used, then the rotational diffusion
will occur at this prescribed temperature instead of temp. Only
compatible with brownian/sphere and brownian/asphere.

If the planar_rotation keyword is used, then rotation is constrained
to the x  y plane in a 3D simulation. Only compatible with
brownian/sphere and brownian/asphere in 3D.

Note
For style brownian/asphere, the components gamma_t_eigen = (x,x,x) and
gamma_r_eigen = (y,y,y), the dynamics will replicate those of the
brownian/sphere style with gamma_t = x and gamma_r = y.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
fix 1 all brownian 1.0 12908410 gamma_t 1.0
fix 1 all brownian 1.0 12908410 gamma_t 3.0 rng gaussian
fix 1 all brownian/sphere 1.0 1294019 gamma_t 3.0 gamma_r 1.0
fix 1 all brownian/sphere 1.0 19581092 gamma_t 1.0 gamma_r 0.3 rng none
fix 1 all brownian/sphere 1.0 19581092 gamma_t 1.0 gamma_r 0.3 rng gaussian rotation_style projection
fix 1 all brownian/asphere 1.0 1294019 gamma_t_eigen 1.0 2.0 3.0 gamma_r_eigen 4.0 7.0 8.0 rng gaussian
fix 1 all brownian/asphere 1.0 1294019 gamma_t_eigen 1.0 2.0 3.0 gamma_r_eigen 4.0 7.0 8.0 dipole 1.0 0.0 0.0
```

## Restrictions

Restrictions 
The style brownian/sphere fix requires that atoms store torque and
angular velocity (omega) as defined by the atom_style sphere command.  The style brownian/asphere fix requires that
atoms store torque and quaternions as defined by the atom_style
ellipsoid command.  If the dipole keyword is used, they
must also store a dipole moment as defined by the atom_style
dipole command.
This fix is part of the BROWNIAN package.  It is only enabled if LAMMPS
was built with that package.  See the Build package doc page for more info.

## Related Commands

- [fix propel/self](fix_propel_self.html)
- [fix langevin](fix_langevin.html)
- [fix nve/sphere](fix_nve_sphere.html)

