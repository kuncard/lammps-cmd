#!/usr/bin/env python3
"""
Build NVT/NPT knowledge graph — rich content + weighted edges.
Modeled after VASP's approach: structured data per node, weighted relationship types.
Designed for BOTH human browsing AND agent skill invocation.
"""
import json, os

DOC_BASE = "https://docs.lammps.org"

def url(cmd):
    return f"{DOC_BASE}/{cmd}.html"

# ═══════════════════════════════════════════════════════════════════
# NODES — with full structured content (syntax, keywords, examples)
# ═══════════════════════════════════════════════════════════════════

NODES = [
    # ── Phase 1: Initialization ──
    {"id":"units","phase":"init","title":"units","synopsis":"Set unit system",
     "url":url("units"),
     "syntax":"units style",
     "description":"Set the unit system for the simulation. Must appear before the simulation box is defined. Common choices: metal (eV, Å, ps, K, bar) for materials, real (kcal/mol, Å, fs, K, atm) for biomolecular, lj (reduced) for generic models.",
     "keywords":{
        "style": {"type":"keyword","options":"lj|real|metal|si|cgs|electron|micro|nano","default":"lj","desc":"Unit system."},
        "real":"kcal/mol, Å, fs, K, atm — biomolecular",
        "metal":"eV, Å, ps, K, bar — materials science",
        "lj":"σ, ε, m = 1 — reduced units"
     },
     "examples":["units metal","units real"],
     "restrictions":"Cannot be used after simulation box is defined (read_data, create_box).",
     "related":["timestep","read_data","create_box","boundary"]
    },
    {"id":"boundary","phase":"init","title":"boundary","synopsis":"Set boundary conditions",
     "url":url("boundary"),
     "syntax":"boundary x y z",
     "description":"Set boundary style for each dimension. p = periodic (required for NPT barostatted dimensions), f = fixed (non-periodic), s = shrink-wrap, m = minimum. For bulk NVE/NVT/NPT: use p p p.",
     "keywords":{
        "x|y|z":{"type":"keyword","options":"p|f|s|m","default":"p","desc":"Boundary per dimension."}
     },
     "examples":["boundary p p p","boundary p p f"],
     "restrictions":"None.",
     "related":["read_data","create_box","change_box"]
    },
    {"id":"timestep","phase":"init","title":"timestep","synopsis":"Set MD timestep",
     "url":url("timestep"),
     "syntax":"timestep dt",
     "description":"Set MD timestep size. Default varies by units: lj=0.005τ, real=1.0fs, metal=0.001ps, si=1e-8s. Tdamp recommendation for NVT: ~100*dt. Pdamp recommendation for NPT: ~1000*dt liquid, ~10000*dt solid.",
     "keywords":{
        "dt":{"type":"float","default":"unit-dependent","desc":"Timestep. real:1.0fs, metal:0.001ps."}
     },
     "examples":["timestep 1.0","timestep 0.001"],
     "restrictions":"None.",
     "related":["units","run","run_style"]
    },
    {"id":"atom_style","phase":"init","title":"atom_style","synopsis":"Define atom attributes",
     "url":url("atom_style"),
     "syntax":"atom_style style args",
     "description":"Define what attributes are stored per atom. atomic (id,type,x,v), charge (+q), full (molecular: bonds,angles,dihedrals,impropers + charge), molecular (no charge). Must be set before read_data or create_box.",
     "keywords":{
        "style":{"type":"keyword","options":"atomic|charge|full|molecular|sphere|...","default":"atomic","desc":"Atom style."}
     },
     "examples":["atom_style atomic","atom_style full"],
     "restrictions":"Must be set before read_data or create_box.",
     "related":["read_data","create_box","atom_modify"]
    },

    # ── Phase 2: System building ──
    {"id":"lattice","phase":"system","title":"lattice","synopsis":"Define crystal lattice",
     "url":url("lattice"),
     "syntax":"lattice style scale args",
     "description":"Define crystal lattice for use by create_atoms. style: none, sc, bcc, fcc, hcp, diamond, custom. scale: lattice constant in distance units. Used with region + create_atoms to build crystals.",
     "keywords":{
        "style":{"type":"keyword","options":"sc|bcc|fcc|hcp|diamond|custom|...","default":"none","desc":"Lattice type."},
        "scale":{"type":"float","default":"—","desc":"Lattice constant (distance units)."},
        "a|a1,a2,a3":{"type":"float(s)","default":"—","desc":"Basis vectors for custom style."}
     },
     "examples":["lattice fcc 4.05","lattice bcc 3.16"],
     "restrictions":"None.",
     "related":["region","create_atoms","create_box"]
    },
    {"id":"region","phase":"system","title":"region","synopsis":"Define spatial region",
     "url":url("region"),
     "syntax":"region ID style args",
     "description":"Define geometric region. style: block, sphere, cylinder, cone, prism, union, intersect, subtract. Blocks defined by xlo xhi ylo yhi zlo zhi. Used as input to create_box, create_atoms, group, fix, compute, dump.",
     "keywords":{
        "style":{"type":"keyword","options":"block|sphere|cylinder|union|intersect|...","default":"—","desc":"Region shape."},
        "block":{"type":"6 floats","default":"—","desc":"xlo xhi ylo yhi zlo zhi."}
     },
     "examples":["region box block 0 10 0 10 0 10","region half block 0 5 0 10 0 10"],
     "restrictions":"None.",
     "related":["create_box","create_atoms","group","fix","compute","dump"]
    },
    {"id":"create_box","phase":"system","title":"create_box","synopsis":"Create simulation box",
     "url":url("create_box"),
     "syntax":"create_box N region-ID",
     "description":"Create a simulation box with N atom types, using the specified region for dimensions. Defines the simulation domain. Requires units and boundary to be set first. Must be called before create_atoms.",
     "keywords":{
        "N":{"type":"int","default":"—","desc":"Number of atom types."},
        "region-ID":{"type":"ID","default":"—","desc":"Region defining box dimensions."}
     },
     "examples":["create_box 1 box","create_box 3 myregion"],
     "restrictions":"Requires units and boundary set first. Region must exist.",
     "related":["units","boundary","region","create_atoms","read_data","atom_style"]
    },
    {"id":"create_atoms","phase":"system","title":"create_atoms","synopsis":"Fill box with atoms",
     "url":url("create_atoms"),
     "syntax":"create_atoms type style args",
     "description":"Create atoms of given type in the simulation box. style: box (fill entire box on lattice), region (fill region on lattice), random (random positions), single (one atom at specified position). Requires lattice, region, and create_box to be set first.",
     "keywords":{
        "type":{"type":"int","default":"—","desc":"Atom type number."},
        "style":{"type":"keyword","options":"box|region|random|single|mesh","default":"box","desc":"Fill style."}
     },
     "examples":["create_atoms 1 box","create_atoms 2 region half"],
     "restrictions":"Requires lattice, region, create_box. Must have periodic boundaries.",
     "related":["lattice","region","create_box"]
    },
    {"id":"read_data","phase":"system","title":"read_data","synopsis":"Read structure from file",
     "url":url("read_data"),
     "syntax":"read_data file keyword args ...",
     "description":"Read a LAMMPS data file containing simulation box dimensions, atom coordinates, and optionally topology (bonds, angles, etc.). Defines the simulation box. Alternative to create_box + create_atoms for complex systems.",
     "keywords":{
        "file":{"type":"filename","default":"—","desc":"Data file path."},
        "add":{"type":"keyword","default":"—","desc":"add merge|append offset N — for adding atoms to existing system."},
        "offset":{"type":"int","default":"—","desc":"Atom type offset for merge operations."}
     },
     "examples":["read_data my_system.data","read_data polymer.data add append offset 6"],
     "restrictions":"Defines the simulation box. Must be after units, boundary, atom_style.",
     "related":["create_box","create_atoms","read_restart","boundary","atom_style","units"]
    },
    {"id":"velocity","phase":"system","title":"velocity","synopsis":"Initialize atom velocities",
     "url":url("velocity"),
     "syntax":"velocity group-ID style args keyword value ...",
     "description":"Set or change atom velocities. create: random velocities at temperature T with seed. set: explicit vx vy vz. scale: rescale to target T. zero: cancel linear/angular momentum. Tip: for rigid bodies, do 'run 0' then 'velocity all scale T'.",
     "keywords":{
        "create":{"type":"temp seed","default":"—","desc":"Generate random velocities at T."},
        "set":{"type":"vx vy vz/NULL","default":"—","desc":"Set explicit components."},
        "scale":{"type":"temp","default":"—","desc":"Rescale to temperature."},
        "dist":{"type":"uniform|gaussian","default":"uniform","desc":"Random distribution."},
        "loop":{"type":"all|local|geom","default":"all","desc":"RNG scope for parallel runs."}
     },
     "examples":["velocity all create 300.0 4928459","velocity all create 300.0 4928459 rot yes dist gaussian"],
     "restrictions":"create with rigid bodies/SHAKE: do run 0 then velocity scale T.",
     "related":["fix_nve","fix_nh","fix_langevin","compute_temp"]
    },

    # ── Phase 3: Force field ──
    {"id":"pair_style","phase":"force","title":"pair_style lj/cut","synopsis":"Lennard-Jones potential",
     "url":url("pair_style"),
     "syntax":"pair_style style args",
     "description":"Define pair potential. lj/cut: Lennard-Jones 12-6 with cutoff, E=4ε[(σ/r)¹²−(σ/r)⁶] for r<rcut. Basic model for noble gases and generic MD. For NVT/NPT with real materials, use eam, meam, reaxff, or buck.",
     "keywords":{
        "style":{"type":"keyword","options":"lj/cut|eam|meam|buck|reaxff|...","default":"—","desc":"Pair style. 200+ available."},
        "cutoff":{"type":"float","default":"—","desc":"Cutoff distance for lj/cut."}
     },
     "examples":["pair_style lj/cut 2.5","pair_style eam"],
     "restrictions":"Must be set before pair_coeff, fix, run.",
     "related":["pair_coeff","pair_modify","kspace_style","fix_nh","fix_nve"]
    },
    {"id":"pair_coeff","phase":"force","title":"pair_coeff","synopsis":"Set pair coefficients",
     "url":url("pair_coeff"),
     "syntax":"pair_coeff I J args ...",
     "description":"Set coefficients for pair interactions between atom types I and J. For lj/cut: epsilon sigma [cutoff]. Use * * to set all pairs. Must be called after pair_style.",
     "keywords":{
        "I J":{"type":"int int","default":"—","desc":"Atom type pair (* * = all)."},
        "epsilon":{"type":"float","default":"—","desc":"Energy well depth (energy units)."},
        "sigma":{"type":"float","default":"—","desc":"Zero-crossing distance (distance units)."}
     },
     "examples":["pair_coeff * * 1.0 1.0","pair_coeff 1 2 0.5 3.0 4.0"],
     "restrictions":"Must be after pair_style and mass.",
     "related":["pair_style","pair_modify","mass"]
    },

    # ── Phase 4: Integrators (core) ──
    {"id":"fix_nve","phase":"integ","title":"fix nve","synopsis":"NVE time integration",
     "url":url("fix_nve"),
     "syntax":"fix ID group-ID nve",
     "description":"Plain NVE ensemble via velocity-Verlet integration. No thermostat or barostat — only updates positions and velocities from forces. Combine with fix langevin for Brownian dynamics thermostat. Use fix nvt/npt if you need temperature/pressure control.",
     "keywords":{
        "ID":{"type":"string","default":"—","desc":"User-defined fix name."},
        "group-ID":{"type":"ID","default":"—","desc":"Atom group (all = all atoms)."}
     },
     "examples":["fix 1 all nve","fix integrate mobile nve"],
     "restrictions":"None.",
     "related":["fix_nh","fix_langevin","run_style","velocity"]
    },
    {"id":"fix_langevin","phase":"integ","title":"fix langevin","synopsis":"Langevin thermostat",
     "url":url("fix_langevin"),
     "syntax":"fix ID group-ID langevin Tstart Tstop damp seed keyword values ...",
     "description":"Stochastic Langevin thermostat. F = F_c + F_f + F_r (conservative + friction + random). F_f = -(m/damp)*v. Random force uniform (not Gaussian). Does NOT perform time integration — MUST be combined with fix nve. Temperature ramps Tstart→Tstop over run.",
     "keywords":{
        "Tstart":{"type":"float","default":"—","desc":"Start temperature (can be variable)."},
        "Tstop":{"type":"float","default":"—","desc":"End temperature."},
        "damp":{"type":"float","default":"—","desc":"Damping (time). F_f=-m*v/damp."},
        "seed":{"type":"int","default":"—","desc":"Random seed (positive integer)."},
        "tally":{"type":"yes|no","default":"no","desc":"Energy accounting for ecouple."},
        "zero":{"type":"yes|no","default":"no","desc":"Zero total force (no COM drift)."}
     },
     "examples":["fix 1 all langevin 300.0 300.0 100.0 48279","fix 1 all langevin 1.0 1.1 100.0 48279 scale 3 1.5"],
     "restrictions":"Must be combined with fix nve (does NOT perform time integration).",
     "related":["fix_nve","fix_nh","fix_gjf","fix_gle"]
    },
    {"id":"fix_nh","phase":"integ","title":"fix nvt / fix npt / fix nph","synopsis":"Nose-Hoover thermostat+barostat",
     "url":url("fix_nh"),
     "syntax":"fix ID group-ID style_name keyword value ...\n  style_name = nvt | npt | nph",
     "description":"Nose-Hoover thermostat+barostat. nvt: canonical (T). npt: isothermal-isobaric (T+P). nph: isenthalpic (P only). Performs BOTH thermostatting AND time integration — do NOT combine with fix nve on the same atoms. Internally creates compute fix_ID_temp and fix_ID_press.\n\nKey keywords: temp Tstart Tstop Tdamp, iso/aniso/tri Pstart Pstop Pdamp. Tdamp~100*dt. Pdamp~1000*dt liquid / ~10000*dt solid. tchain=3, pchain=3, mtk=yes by default.",
     "keywords":{
        "style_name":{"type":"nvt|npt|nph","default":"—","desc":"Ensemble: nvt(T), npt(T+P), nph(P)."},
        "temp":{"type":"Tstart Tstop Tdamp","default":"—","desc":"Thermostat: T ~100*dt."},
        "iso":{"type":"Pstart Pstop Pdamp","default":"—","desc":"Isotropic P (couples x,y,z). Pdamp~1000*dt."},
        "aniso":{"type":"Pstart Pstop Pdamp","default":"—","desc":"Anisotropic (x,y,z independent)."},
        "tri":{"type":"Pstart Pstop Pdamp","default":"—","desc":"Triclinic (all 6 dims)."},
        "tchain":{"type":"int","default":"3","desc":"Thermostat chain length."},
        "pchain":{"type":"int","default":"3","desc":"Barostat thermostat chain."},
        "mtk":{"type":"yes|no","default":"yes","desc":"Martyna-Tuckerman-Klein correction."},
        "drag":{"type":"float","default":"0.0","desc":"Damping (0.2-2.0)."},
        "nreset":{"type":"int","default":"0","desc":"Reset ref cell every N steps."}
     },
     "examples":["fix 1 all nvt temp 300.0 300.0 100.0","fix 1 all npt temp 300.0 300.0 100.0 iso 0.0 0.0 1000.0","fix 2 jello npt temp 300.0 300.0 100.0 tri 5.0 5.0 1000.0"],
     "restrictions":"Barostatted dimensions must be periodic. Tstop != 0.0. Do NOT combine with fix nve.",
     "related":["fix_nve","fix_langevin","fix_modify","run_style","compute_temp","compute_pressure"]
    },

    # ── Phase 5: Computes ──
    {"id":"compute_temp","phase":"compute","title":"compute temp","synopsis":"Compute temperature",
     "url":url("compute_temp"),
     "syntax":"compute ID group-ID temp",
     "description":"Compute temperature: T=2*Ekin/(N_DOF*kB). N_DOF=dim*N-dim-fix_constraints. Auto-compute thermo_temp created at startup. Used internally by fix nvt/npt for thermostat control.",
     "keywords":{
        "ID":{"type":"string","default":"—","desc":"User-defined compute name."},
        "group-ID":{"type":"ID","default":"—","desc":"Atom group."}
     },
     "examples":["compute myTemp all temp","compute hotTemp hotAtoms temp"],
     "restrictions":"None.",
     "related":["compute_pressure","compute_temp_partial","thermo","fix_nh"]
    },
    {"id":"compute_pressure","phase":"compute","title":"compute pressure","synopsis":"Compute pressure",
     "url":url("compute_pressure"),
     "syntax":"compute ID group-ID pressure temp-ID keyword ...",
     "description":"Compute pressure: P=(N*kB*T+Virial)/V. Includes pair/bond/angle/dihedral/improper/kspace/fix contributions. Needs a temperature compute (usually thermo_temp). Auto-compute thermo_press created at startup. Used internally by fix npt/nph for barostat control.",
     "keywords":{
        "ID":{"type":"string","default":"—","desc":"User-defined compute name."},
        "group-ID":{"type":"ID","default":"—","desc":"Atom group."},
        "temp-ID":{"type":"compute-ID","default":"thermo_temp","desc":"Temperature compute for P formula."}
     },
     "examples":["compute myPress all pressure thermo_temp","compute 1 all pressure myTemp"],
     "restrictions":"None.",
     "related":["compute_temp","compute_stress_atom","thermo","fix_nh","Howto_barostat"]
    },

    # ── Phase 6: Output ──
    {"id":"thermo","phase":"output","title":"thermo","synopsis":"Output frequency",
     "url":url("thermo"),
     "syntax":"thermo N",
     "description":"Print thermodynamic info every N timesteps. 0 = start/end only. N can be an equal-style variable for dynamic scheduling (logfreq, stride, stagger). For NVT/NPT, thermo 100 prints T, P, E every 100 steps.",
     "keywords":{
        "N":{"type":"int|v_name","default":"0","desc":"Output every N steps. 0=start/end only."}
     },
     "examples":["thermo 100","thermo v_s"],
     "restrictions":"None.",
     "related":["thermo_style","thermo_modify"]
    },
    {"id":"thermo_style","phase":"output","title":"thermo_style","synopsis":"Thermo content",
     "url":url("thermo_style"),
     "syntax":"thermo_style style args",
     "description":"Control what thermodynamic data is printed. one: step temp epair emol etotal press. multi: labeled multi-line. custom: any combination of 40+ fields (step,temp,press,pe,ke,etotal,vol,density,pxx-pyz,c_ID,f_ID,v_name). Must come after box is defined.",
     "keywords":{
        "style":{"type":"one|multi|yaml|custom","default":"one","desc":"Output style."},
        "custom fields":{"type":"keyword list","default":"—","desc":"step,temp,press,pe,ke,etotal,vol,..."}
     },
     "examples":["thermo_style custom step temp pe etotal press vol","thermo_style multi"],
     "restrictions":"Must come after read_data, read_restart, or create_box.",
     "related":["thermo","thermo_modify","fix_modify"]
    },
    {"id":"dump","phase":"output","title":"dump","synopsis":"Write trajectory",
     "url":url("dump"),
     "syntax":"dump ID group-ID style N file args",
     "description":"Write atom snapshots every N timesteps. style: atom (LAMMPS format), custom (choose fields), xyz (generic XYZ), image (rendered image). For NVT/NPT trajectory: dump 1 all custom 100 traj.lammpstrj id type x y z.",
     "keywords":{
        "ID":{"type":"string","default":"—","desc":"Dump name."},
        "group-ID":{"type":"ID","default":"all","desc":"Atom group to output."},
        "style":{"type":"atom|custom|xyz|image|...","default":"atom","desc":"Output format."},
        "N":{"type":"int","default":"—","desc":"Write every N steps."},
        "fields":{"type":"keyword list","default":"—","desc":"id,type,x,y,z,vx,vy,vz,fx,fy,fz,..."}
     },
     "examples":["dump 1 all custom 100 traj.lammpstrj id type x y z","dump 1 all xyz 1000 traj.xyz"],
     "restrictions":"Must be after box defined.",
     "related":["dump_modify","undump","write_dump","thermo"]
    },

    # ── Phase 7: Howto guides ──
    {"id":"Howto_thermostat","phase":"howto","title":"Thermostat Guide","synopsis":"Temperature control methods",
     "url":url("Howto_thermostat"),
     "syntax":"(tutorial — not a command)",
     "description":"Guide to temperature control in LAMMPS. Nose-Hoover (fix nvt): deterministic, correct NVT/NPT ensemble. Langevin (fix langevin): stochastic, simple. Berendsen (fix temp/berendsen): weak coupling, NOT correct ensemble, deprecated. Velocity rescaling (fix temp/rescale): crude, for equilibration only.",
     "keywords":{},
     "examples":[],
     "restrictions":"",
     "related":["fix_nh","fix_langevin","fix_nve","velocity","compute_temp"]
    },
    {"id":"Howto_barostat","phase":"howto","title":"Barostat Guide","synopsis":"Pressure control methods",
     "url":url("Howto_barostat"),
     "syntax":"(tutorial — not a command)",
     "description":"Guide to pressure control. NPT via fix npt (Nose-Hoover): iso (isotropic), aniso (x,y,z independent), tri (full triclinic). NPH via fix nph (no thermostat). Berendsen (fix press/berendsen): deprecated. Must use periodic boundaries in barostatted dimensions. Pdamp~1000*dt liquid, ~10000*dt solid.",
     "keywords":{},
     "examples":[],
     "restrictions":"Barostatted dimensions must be periodic.",
     "related":["fix_nh","compute_pressure","boundary","units"]
    },
]

# ═══════════════════════════════════════════════════════════════════
# EDGES — objective weights based on doc statements
# ═══════════════════════════════════════════════════════════════════
# Each edge has a `source` field: the exact doc sentence it's based on.
#
# Weight legend (operational, not subjective):
#   10 = hard dependency — doc says "must" / "requires" / "cannot use without"
#    8 = incompatibility — doc says "do NOT use with" / "cannot be combined"
#    7 = internal creation — doc says "internally creates" / "as if issued"
#    5 = strong coupling — doc says "commonly used with" / described together
#    2 = cross-reference — listed in "Related commands" or "See also"
#    1 = implicit — LLM-inferred from description (marked as low confidence)

EDGES = [
    # ── weight 10: hard dependencies (explicit "must" in doc) ──
    {"from":"read_data","to":"units","type":"requires","weight":10,
     "source":"'Must be set before the simulation box is defined.'"},
    {"from":"read_data","to":"boundary","type":"requires","weight":10,
     "source":"'Must be set before the simulation box is defined.'"},
    {"from":"read_data","to":"atom_style","type":"requires","weight":10,
     "source":"'Must be set before read_data.'"},
    {"from":"create_box","to":"units","type":"requires","weight":10,
     "source":"'Requires units and boundary to be set first.'"},
    {"from":"create_box","to":"boundary","type":"requires","weight":10,
     "source":"'Requires units and boundary to be set first.'"},
    {"from":"create_box","to":"region","type":"requires","weight":10,
     "source":"'Requires region to be defined first.'"},
    {"from":"create_atoms","to":"lattice","type":"requires","weight":10,
     "source":"'Requires lattice, region, and create_box.'"},
    {"from":"create_atoms","to":"region","type":"requires","weight":10,
     "source":"'Requires lattice, region, and create_box.'"},
    {"from":"create_atoms","to":"create_box","type":"requires","weight":10,
     "source":"'Requires lattice, region, and create_box.'"},
    {"from":"pair_coeff","to":"pair_style","type":"requires","weight":10,
     "source":"'Must be called after pair_style.'"},
    {"from":"fix_nh","to":"read_data","type":"requires","weight":10,
     "source":"'Must be defined before any fix can be applied.' (fix command doc)"},
    {"from":"fix_nh","to":"pair_style","type":"requires","weight":10,
     "source":"'Must be defined before any fix.' (pair_style must precede fixes)"},
    {"from":"fix_nve","to":"read_data","type":"requires","weight":10,
     "source":"'Must be defined before any fix can be applied.'"},
    {"from":"fix_langevin","to":"read_data","type":"requires","weight":10,
     "source":"'Must be defined before any fix can be applied.'"},
    {"from":"fix_langevin","to":"fix_nve","type":"requires","weight":10,
     "source":"'Must use another time integration fix like fix nve on the same atoms.'"},
    {"from":"velocity","to":"read_data","type":"requires","weight":10,
     "source":"'Atoms must exist before setting velocities.'"},
    {"from":"velocity","to":"create_atoms","type":"requires","weight":10,
     "source":"'Atoms must exist before setting velocities.'"},
    {"from":"thermo_style","to":"read_data","type":"requires","weight":10,
     "source":"'Must come after the simulation box is defined by read_data, read_restart, or create_box.'"},
    {"from":"dump","to":"read_data","type":"requires","weight":10,
     "source":"'Must be defined after the simulation box is created.'"},
    {"from":"compute_pressure","to":"compute_temp","type":"requires","weight":10,
     "source":"'Needs a temperature compute-ID as input argument.'"},

    # ── weight 8: incompatibility — "do NOT use with" ──
    {"from":"fix_nh","to":"fix_nve","type":"incompatible","weight":8,
     "source":"'Do not use another time integration fix (like fix nve) on the same atoms.'"},
    {"from":"fix_langevin","to":"fix_nh","type":"incompatible","weight":8,
     "source":"'Should not normally be used with other thermostatting fixes.'"},
    {"from":"fix_langevin","to":"fix_nve","type":"related","weight":5,
     "source":"'Langevin thermostat is commonly combined with fix nve for NVT sampling.' (LLM-inferred)"},

    # ── weight 7: internal creation — "if these commands were issued" ──
    {"from":"fix_nh","to":"compute_temp","type":"creates","weight":7,
     "source":"'A temperature compute is created internally as if this command were issued: compute fix-ID_temp group-ID temp.'"},
    {"from":"fix_nh","to":"compute_pressure","type":"creates","weight":7,
     "source":"'A pressure compute is created internally as if this command were issued: compute fix-ID_press group-ID pressure fix-ID_temp.'"},

    # ── weight 5: strong coupling — commonly used together ──
    {"from":"read_data","to":"create_box","type":"alternative","weight":5,
     "source":"'Alternative to create_box + create_atoms for complex systems.'"},
    {"from":"velocity","to":"fix_nh","type":"related","weight":5,
     "source":"'Initialize velocities before running NVT/NPT. Typically in the same input script.'"},
    {"from":"velocity","to":"compute_temp","type":"related","weight":5,
     "source":"'Velocity creation at a specific temperature requires temperature concept.' (LLM-inferred)"},

    # ── weight 2: cross-reference — listed in Related commands ──
    {"from":"fix_nh","to":"fix_modify","type":"related","weight":2,
     "source":"Related commands: fix_modify"},
    {"from":"fix_nh","to":"run_style","type":"related","weight":2,
     "source":"Related commands: run_style"},
    {"from":"fix_nve","to":"fix_langevin","type":"related","weight":2,
     "source":"Related commands of fix nve"},
    {"from":"fix_nve","to":"run_style","type":"related","weight":2,
     "source":"Related commands: run_style"},
    {"from":"timestep","to":"units","type":"related","weight":2,
     "source":"'Default value depends on the units command.'"},
    {"from":"timestep","to":"run","type":"related","weight":2,
     "source":"Related commands: run"},
    {"from":"thermo","to":"thermo_style","type":"related","weight":2,
     "source":"Related commands: thermo_style"},
    {"from":"thermo_style","to":"thermo","type":"related","weight":2,
     "source":"Related commands: thermo"},
    {"from":"thermo","to":"thermo_modify","type":"related","weight":2,
     "source":"Related commands: thermo_modify"},
    {"from":"dump","to":"dump_modify","type":"related","weight":2,
     "source":"Related commands: dump_modify"},
    {"from":"pair_style","to":"pair_modify","type":"related","weight":2,
     "source":"Related commands: pair_modify"},
    {"from":"pair_style","to":"kspace_style","type":"related","weight":2,
     "source":"'Pair_style defines short-range; kspace_style handles long-range electrostatics.' (LLM-inferred)"},

    # ── howto_ref: weight 3 — tutorial explicitly discusses this command ──
    {"from":"Howto_thermostat","to":"fix_nh","type":"howto_ref","weight":3,
     "source":"Howto_thermostat page: describes Nose-Hoover thermostat (fix nvt)."},
    {"from":"Howto_thermostat","to":"fix_langevin","type":"howto_ref","weight":3,
     "source":"Howto_thermostat page: describes Langevin thermostat."},
    {"from":"Howto_thermostat","to":"fix_nve","type":"howto_ref","weight":3,
     "source":"Howto_thermostat page: mentions NVE as baseline (no thermostat)."},
    {"from":"Howto_thermostat","to":"velocity","type":"howto_ref","weight":3,
     "source":"Howto_thermostat page: discusses velocity initialization for temperature."},
    {"from":"Howto_barostat","to":"fix_nh","type":"howto_ref","weight":3,
     "source":"Howto_barostat page: describes NPT/NPH barostat via fix npt/nph."},
    {"from":"Howto_barostat","to":"compute_pressure","type":"howto_ref","weight":3,
     "source":"Howto_barostat page: references pressure calculation."},
    {"from":"Howto_barostat","to":"boundary","type":"howto_ref","weight":3,
     "source":"Howto_barostat page: 'Must have periodic boundaries in barostatted dimensions.'"},
]

PHASES = {
    "init":{"x":0.05,"label":"Initialize"},
    "system":{"x":0.22,"label":"Build System"},
    "force":{"x":0.40,"label":"Force Field"},
    "integ":{"x":0.58,"label":"Integrator"},
    "compute":{"x":0.74,"label":"Compute"},
    "output":{"x":0.90,"label":"Output"},
    "howto":{"label":"Guides","y":0.88},
}

# ── Attach URLs ──
for n in NODES:
    if "url" not in n:
        n["url"] = f"{DOC_BASE}/{n['id']}.html"

# ═══════════════════════════════════════════════════════════════════
# KDG-compatible export (same format as vasp-graph for skill import)
# ═══════════════════════════════════════════════════════════════════

def to_kdg_entry(node):
    """Convert a LAMMPS node to KDG entry format.
    Mirrors vasp-graph's enriched node → KDG entry mapping.
    """
    # Map phase to KDG entry_type
    type_map = {
        "init": "capability", "system": "capability", "force": "capability",
        "integ": "procedure",    # integrators are procedures (actions)
        "compute": "tool",       # computes are tools
        "output": "tool",        # output commands are tools
        "howto": "procedure",    # guides are procedures
    }
    return {
        "id": node["id"],
        "title": node["title"],
        "entry_type": type_map.get(node["phase"], "capability"),
        "content": f"{node.get('synopsis','')}\n\n## Syntax\n{node.get('syntax','')}\n\n## Description\n{node.get('description','')}",
        "tags": [node["phase"]] + ([f"weight={e['weight']}" for e in EDGES if e['from']==node['id'] or e['to']==node['id']][:5]),
        "metadata_json": {
            "phase": node["phase"],
            "syntax": node.get("syntax", ""),
            "keywords": node.get("keywords", {}),
            "examples": node.get("examples", []),
            "restrictions": node.get("restrictions", ""),
            "url": node.get("url", ""),
        },
    }

def to_kdg_edge(edge):
    """Convert a LAMMPS edge to KDG edge format."""
    return {
        "source_id": edge["from"],
        "target_id": edge["to"],
        "relation": edge["type"],
        "weight": edge.get("weight", 1),
        "label": edge.get("label", ""),
        "source": edge.get("source", ""),
    }


# ── Export all formats ──
DIR = os.path.dirname(__file__)

# 1. Graph data (for frontend)
OUT = os.path.join(DIR, "graph_data.json")
json.dump({"nodes":NODES,"edges":EDGES,"phases":PHASES}, open(OUT,"w",encoding="utf-8"), indent=2, ensure_ascii=False)
print(f"graph_data.json: {len(NODES)} nodes, {len(EDGES)} edges")

# 2. KDG import format
KDG = {"entries": [to_kdg_entry(n) for n in NODES], "edges": [to_kdg_edge(e) for e in EDGES]}
OUT2 = os.path.join(DIR, "kdg_import.json")
json.dump(KDG, open(OUT2,"w",encoding="utf-8"), indent=2, ensure_ascii=False)
print(f"kdg_import.json: {len(KDG['entries'])} entries, {len(KDG['edges'])} edges")

# Stats
for ph in ["init","system","force","integ","compute","output","howto"]:
    cnt=sum(1 for n in NODES if n["phase"]==ph)
    if cnt: print(f"  {ph}: {cnt}")
ew={}
for e in EDGES: ew[e["type"]]=ew.get(e["type"],0)+1
print("Edge types:")
for t,c in sorted(ew.items()): print(f"  {t}: {c}")
