---
id: package
title: "package command"
url: https://docs.lammps.org/package.html
---

# package command

## Syntax

```
package style args
gpu args = Ngpu keyword value ...
  Ngpu = # of GPUs per node
  zero or more keyword/value pairs may be appended
  keywords = neigh or newton or pair/only or binsize or split or gpuID or tpa or blocksize or omp or platform or device_type or ocl_args
    neigh value = yes or no or hybrid
      yes = neighbor list build on GPU (default)
      no = neighbor list build on CPU
      hybrid = perform binning on the CPU but build neighbor list on the GPU
    newton = off or on
      off = set Newton pairwise flag off (default and required)
      on = set Newton pairwise flag on (currently not allowed)
    pair/only = off or on
      off = apply "gpu" suffix to all available styles in the GPU package (default)
      on = apply "gpu" suffix only pair styles
    binsize value = size
      size = bin size for neighbor list construction (distance units)
    split = fraction
      fraction = fraction of atoms assigned to GPU (default = 1.0)
    tpa value = Nlanes
      Nlanes = # of GPU vector lanes (CUDA threads) used per atom
    blocksize value = size
      size = thread block size for pair force computation
    omp value = Nthreads
      Nthreads = number of OpenMP threads to use on CPU (default = 0)
    platform value = id
      id = For OpenCL, platform ID for the GPU or accelerator
    gpuID values = id
      id = ID of first GPU to be used on each node
    device_type value = intelgpu or nvidiagpu or amdgpu or applegpu or generic or custom,val1,val2,...
      val1,val2,... = custom OpenCL accelerator configuration parameters (see below for details)
    ocl_args value = args
      args = List of additional OpenCL compiler arguments delimited by colons
intel args = Narg keyword value ...
  Narg = accepted for backward compatibility and ignored
  zero or more keyword/value pairs may be appended
  keywords = mode or omp or lrt or pppm_table
    mode value = single or mixed or double
      single = perform force calculations in single precision
      mixed = perform force calculations in mixed precision
      double = perform force calculations in double precision
    omp value = Nthreads
      Nthreads = number of OpenMP threads to use on CPU (default = 0)
    lrt value = yes or no
      yes = use additional thread dedicated for some PPPM calculations
      no = do not dedicate an extra thread for some PPPM calculations
    pppm_table value = yes or no
      yes = Precompute pppm values in table (doesn't change accuracy)
      no = Compute pppm values on the fly
kokkos args = keyword value ...
  zero or more keyword/value pairs may be appended
  keywords = neigh or neigh/qeq or neigh/thread or neigh/transpose or newton or binsize or comm or comm/exchange or comm/forward or comm/pair/forward or comm/fix/forward or comm/compute/forward or comm/reverse or comm/pair/reverse or comm/fix/reverse or sort or atom/map or gpu/aware or pair/only
    neigh value = full or half
      full = full neighbor list
      half = half neighbor list built in thread-safe manner
    neigh/qeq value = full or half
      full = full neighbor list
      half = half neighbor list built in thread-safe manner
    neigh/thread value = off or on
      off = thread only over atoms
      on = thread over both atoms and neighbors
    neigh/transpose value = off or on
      off = use same memory layout for GPU neigh list build as pair style
      on = use transposed memory layout for GPU neigh list build
    newton = off or on
      off = set Newton pairwise and bonded flags off
      on = set Newton pairwise and bonded flags on
    binsize value = size
      size = bin size for neighbor list construction (distance units)
    comm value = no or host or device
      use value for comm/exchange and comm/forward and comm/pair/forward and comm/fix/forward and comm/compute/forward and comm/reverse and comm/fix/reverse
    comm/exchange value = no or host or device
    comm/forward value = no or host or device
    comm/pair/forward value = no or device
    comm/fix/forward value = no or device
    comm/compute/forward value = no or device
    comm/reverse value = no or host or device
      no = perform communication pack/unpack in non-KOKKOS mode
      host = perform pack/unpack on host (e.g. with OpenMP threading)
      device = perform pack/unpack on device (e.g. on GPU)
    comm/pair/reverse value = no or device
      no = perform communication pack/unpack in non-KOKKOS mode
      device = perform pack/unpack on device (e.g. on GPU)
    comm/fix/reverse value = no or host or device
      no = perform communication pack/unpack in non-KOKKOS mode
      host = perform pack/unpack on host (e.g. with OpenMP threading)
      device = perform pack/unpack on device (e.g. on GPU)
    sort value = no or device
      no = perform atom sorting in non-KOKKOS mode
      device = perform atom sorting on device (e.g. on GPU)
    atom/map value = no or device
      no = build atom map in non-KOKKOS mode
      device = build atom map on device (e.g. on GPU)
    gpu/aware = off or on
      off = do not use GPU-aware MPI
      on = use GPU-aware MPI (default)
    pair/only = off or on
      off = use device acceleration (e.g. GPU) for all available styles in the KOKKOS package (default)
      on  = use device acceleration only for pair styles (and host acceleration for others)
    threads/per/atom args = Ntpa
      Ntpa = # of threads per atom for multiple GPU threads over the neighbor list per atom
    pair/team/size args = Nteamsize
      Nteamsize = # of threads per block used for the pair compute kernel
    nbin/atoms/per/bin = Natomsperbin
      Natomsperbin = # of atoms per bin used for neighbor list builds
    *nbor/chunk/size = chunksize
      chunksize = # of iterations each thread will perform for the flat neighbor build method
    *bond/chunk/size = blocksize
      chunksize = # of iterations each thread will perform for the bond force computation
    *auto/tuning = nevery nsamples mode reltol
      nevery = # timesteps between auto-tuning adjustments (default = 0, no auto-tuning)
      nsamples = # samples the tuner(s) collects for each parameter combination
      mode = how to pick a performance value from the samples collected, i.e. maximum, average or median value
      reltol = relative tolerance for performance degradation that triggers re-tuning of parameter values
*omp args = Nthreads keyword value ...
  Nthreads = # of OpenMP threads to associate with each MPI process
  zero or more keyword/value pairs may be appended
  keywords = neigh
    neigh value = yes or no
      yes = threaded neighbor list build (default)
      no = non-threaded neighbor list build
```

## Description

This command invokes package-specific settings for the various
accelerator packages available in LAMMPS.  Currently the following
packages use settings from this command: GPU, INTEL, KOKKOS, and
OPENMP.

If this command is specified in an input script, it must be near the
top of the script, before the simulation box has been defined.  This
is because it specifies settings that the accelerator packages use in
their initialization, before a simulation is defined.

This command can also be specified from the command-line when
launching LAMMPS, using the  -pk  command-line switch.  The syntax is exactly the same as when used
in an input script.

Note that all of the accelerator packages require the package command
to be specified (except the OPT package), if the package is to be used
in a simulation (LAMMPS can be built with an accelerator package
without using it in a particular simulation).  However, in all cases,
a default version of the command is typically invoked by other
accelerator settings.

The KOKKOS package requires a  -k on  command-line switch respectively, which invokes a  package
kokkos  command with default settings.

For the GPU, INTEL, and OPENMP packages, if a  -sf gpu  or  -sf
intel  or  -sf omp  command-line switch is used to
auto-append accelerator suffixes to various styles in the input
script, then those switches also invoke a  package gpu ,  package
intel , or  package omp  command with default settings.

Note
A package command for a particular style can be invoked multiple
times when a simulation is setup, e.g. by the -c on, -k on, -sf, and -pk command-line switches, and by using this command
in an input script.  Each time it is used all of the style options are
set, either to default values or to specified settings.  I.e. settings
from previous invocations do not persist across multiple invocations.

See the Accelerator packages page for more details
about using the various accelerator packages for speeding up LAMMPS
simulations.

## Keywords

- **LAMMPS Branch:**: develop
- **Downloads:**: PDF
- **Git Info:**: 4Jul2026

## Examples

```
package gpu 0
package gpu 1 split 0.75
package gpu 2 split -1.0
package gpu 0 omp 2 device_type intelgpu
package kokkos neigh half comm device
package omp 0 neigh no
package omp 4
package intel 1
package intel 2 omp 4 mode mixed
```

## Restrictions

Restrictions 
This command cannot be used after the simulation box is defined by a
read_data or create_box command.
The gpu style of this command can only be invoked if LAMMPS was built
with the GPU package.  See the Build package doc
page for more info.
The intel style of this command can only be invoked if LAMMPS was
built with the INTEL package.  See the Build package page for more info.
The kokkos style of this command can only be invoked if LAMMPS was built
with the KOKKOS package.  See the Build package
doc page for more info.
The omp style of this command can only be invoked if LAMMPS was built
with the OPENMP package.  See the Build package
doc page for more info.

## Related Commands

- [Related commands](#contents)
- [suffix](suffix.html)
- [-pk command-line switch](Run_options.html)

