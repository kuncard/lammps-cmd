#!/usr/bin/env python3
"""
Build LAMMPS multi-layer relationship graph.
4 layers of edges: requires / alternative / creates / howto_ref

Exports JSON for the frontend graph visualization.
"""
import json, os

OUT = os.path.join(os.path.dirname(__file__), "graph_data.json")

# ═══════════════════════════════════════════════════════════════════
# NODE DEFINITIONS
# ═══════════════════════════════════════════════════════════════════

# ── Phase groups (for graph layout) ──
PHASES = {
    "init":     {"label": "Initialize",   "x": 0.05, "color": "#f778ba"},
    "system":   {"label": "Build System", "x": 0.22, "color": "#58a6ff"},
    "force":    {"label": "Force Field",  "x": 0.39, "color": "#3fb950"},
    "settings": {"label": "Settings",     "x": 0.56, "color": "#d29922"},
    "integ":    {"label": "Run",          "x": 0.73, "color": "#a371f7"},
    "output":   {"label": "Output",       "x": 0.90, "color": "#f0883e"},
    "howto":    {"label": "Guides",       "y": 0.85, "color": "#8b949e"},
}

NODES = []

def node(cmd_id, title, phase, desc="", keywords=None):
    NODES.append({
        "id": cmd_id, "title": title, "phase": phase,
        "desc": desc, "keywords": keywords or [],
    })

# ── Initialization (must come first in any script) ──
node("units",          "units",             "init",     "Unit system: lj / real / metal / si / cgs / electron / micro / nano")
node("boundary",       "boundary",          "init",     "Boundary conditions: p(eriodic) / f(ixed) / s(hrink-wrap) / m(inimum)")
node("dimension",      "dimension",         "init",     "2D or 3D simulation")
node("processors",     "processors",        "init",     "MPI processor grid layout")
node("newton",         "newton",            "init",     "Newton's 3rd law: on/off for pair/bond")
node("atom_style",     "atom_style",        "init",     "Atom attributes: atomic / charge / full / molecular / sphere...")
node("atom_modify",    "atom_modify",       "init",     "Modify atom style parameters")
node("comm_style",     "comm_style",        "init",     "Communication style: brick / tiled")
node("comm_modify",    "comm_modify",       "init",     "Modify communication parameters")
node("neighbor",       "neighbor",          "init",     "Neighbor list build style: nsq / bin / multi")
node("neigh_modify",   "neigh_modify",      "init",     "Neighbor list parameters: delay / every / check")
node("suffix",         "suffix",            "init",     "Accelerator suffix: gpu / intel / kk / omp / opt")
node("package",        "package",           "init",     "Accelerator package settings")
node("lattice",        "lattice",           "init",     "Crystal lattice definition (for create_atoms)")
node("timestep",       "timestep",          "init",     "MD timestep size (time units)")
node("echo",           "echo",              "init",     "Echo input commands to screen/log")

# ── System building ──
node("region",         "region",            "system",   "Geometric region: block / sphere / cylinder / cone / union / intersect")
node("create_box",     "create_box",        "system",   "Create simulation box from regions")
node("create_atoms",   "create_atoms",      "system",   "Create atoms on lattice: box / region / random / single")
node("create_bonds",   "create_bonds",      "system",   "Create bonds between atoms")
node("delete_atoms",   "delete_atoms",      "system",   "Delete atoms by group / region")
node("delete_bonds",   "delete_bonds",      "system",   "Delete bonds")
node("displace_atoms", "displace_atoms",    "system",   "Move atoms by translation / rotation")
node("read_data",      "read_data",         "system",   "Read structure from data file (defines box)")
node("read_dump",      "read_dump",         "system",   "Read atoms from dump file")
node("read_restart",   "read_restart",      "system",   "Read restart file (continues simulation)")
node("replicate",      "replicate",         "system",   "Replicate system in x,y,z (make supercell)")
node("change_box",     "change_box",        "system",   "Change simulation box size/shape")
node("reset_atoms",    "reset_atoms",       "system",   "Reset atom properties: image flags / molecule IDs")
node("mass",           "mass",              "system",   "Set per-type atomic masses")
node("group",          "group",             "system",   "Define atom groups: type / region / id / variable...")
node("set",            "set",               "system",   "Set atom properties: type / charge / position...")
node("velocity",       "velocity",          "system",   "Initialize velocities: create / set / scale / ramp / zero")
node("molecule",       "molecule",          "system",   "Define molecule templates")
node("labelmap",       "labelmap",          "system",   "Map atom type labels to numbers")

# ── Force field ──
node("pair_style",     "pair_style",        "force",    "Define pair potential: lj/cut / eam / reaxff / buck / ... (200+ styles)")
node("pair_coeff",     "pair_coeff",        "force",    "Set pair coefficients: ε, σ per atom type pair")
node("pair_modify",    "pair_modify",       "force",    "Modify pair style: shift / mix / tail / table...")
node("pair_write",     "pair_write",        "force",    "Write pair coefficients to file")
node("bond_style",     "bond_style",        "force",    "Bond potential: harmonic / morse / fene / table...")
node("bond_coeff",     "bond_coeff",        "force",    "Bond coefficients per type")
node("bond_write",     "bond_write",        "force",    "Write bond coefficients to file")
node("angle_style",    "angle_style",       "force",    "Angle potential: harmonic / cosine / charmm / class2...")
node("angle_coeff",    "angle_coeff",       "force",    "Angle coefficients per type")
node("angle_write",    "angle_write",       "force",    "Write angle coefficients to file")
node("dihedral_style", "dihedral_style",    "force",    "Dihedral potential: charmm / opls / harmonic / multi...")
node("dihedral_coeff", "dihedral_coeff",    "force",    "Dihedral coefficients per type")
node("dihedral_write", "dihedral_write",    "force",    "Write dihedral coefficients to file")
node("improper_style", "improper_style",    "force",    "Improper potential: harmonic / cvff / umbrella...")
node("improper_coeff", "improper_coeff",    "force",    "Improper coefficients per type")
node("kspace_style",   "kspace_style",      "force",    "Long-range solver: pppm / ewald / msm...")
node("kspace_modify",  "kspace_modify",     "force",    "Modify kspace parameters")
node("special_bonds",  "special_bonds",     "force",    "Weighting of 1-2, 1-3, 1-4 neighbor interactions")
node("dielectric",     "dielectric",        "force",    "Dielectric constant for Coulomb interactions")

# ── Settings (middle layer between force field and run) ──
node("min_style",      "min_style",         "settings", "Energy minimization algorithm: cg / hftn / sd / quickmin / fire")
node("min_modify",     "min_modify",        "settings", "Modify minimization parameters")
node("run_style",      "run_style",         "settings", "Time integrator: verlet / respa")
node("fix",            "fix",               "settings", "Apply operation every timestep: nve / nvt / npt / langevin / ... (150+ styles)")
node("fix_modify",     "fix_modify",        "settings", "Modify fix parameters: temp / press / energy...")
node("unfix",          "unfix",             "settings", "Remove a fix")
node("compute",        "compute",           "settings", "Compute quantity: temp / pressure / msd / rdf / ... (100+ styles)")
node("compute_modify", "compute_modify",    "settings", "Modify compute parameters")
node("uncompute",      "uncompute",         "settings", "Remove a compute")
node("variable",       "variable",          "settings", "Define variable: equal / atom / string / file / python...")
node("reset_timestep", "reset_timestep",    "settings", "Reset timestep counter")
node("restart",        "restart",           "settings", "Write restart files periodically")

# ── Run / integrators ──
node("minimize",       "minimize",          "integ",    "Run energy minimization")
node("run",            "run",               "integ",    "Run MD for N timesteps")
node("rerun",          "rerun",             "integ",    "Re-process trajectory from dump file")

# ── Specific fix examples (NVT/NPT family) ──
node("fix_nh",         "fix nvt / npt / nph","integ",  "Nose-Hoover thermostat+barostat. NVT: T control. NPT: T+P control.")
node("fix_nve",        "fix nve",            "integ",   "Velocity-Verlet (NVE). No thermostat/barostat.")
node("fix_langevin",   "fix langevin",       "integ",   "Langevin thermostat (stochastic). Use WITH fix nve.")
node("fix_temp_rescale","fix temp/rescale",   "integ",  "Simple velocity rescaling thermostat.")
node("fix_press_berendsen","fix press/berendsen","integ","Berendsen barostat (weak coupling, deprecated).")
node("fix_deform",     "fix deform",         "integ",   "Deform simulation box during run.")

# ── Specific compute examples ──
node("compute_temp",   "compute temp",       "integ",   "Temperature: T = 2*Ekin/(N_DOF*kB). Auto: thermo_temp.")
node("compute_pressure","compute pressure",  "integ",   "Pressure: P = (N*kB*T + Virial)/V. Auto: thermo_press.")
node("compute_msd",    "compute msd",        "integ",   "Mean squared displacement of atoms.")

# ── Output ──
node("thermo",         "thermo",            "output",   "Thermo output frequency (every N steps)")
node("thermo_style",   "thermo_style",      "output",   "Thermo content: one / multi / yaml / custom (40+ fields)")
node("thermo_modify",  "thermo_modify",     "output",   "Thermo formatting: lost / norm / line / format / temp / press")
node("dump",           "dump",              "output",   "Snapshot output: atom / custom / xyz / image / netcdf...")
node("dump_modify",    "dump_modify",       "output",   "Dump formatting: sort / thresh / format / colname...")
node("undump",         "undump",            "output",   "Remove a dump")
node("write_data",     "write_data",        "output",   "Write data file")
node("write_dump",     "write_dump",        "output",   "Write single dump snapshot")
node("write_restart",  "write_restart",     "output",   "Write restart file")
node("write_coeff",    "write_coeff",       "output",   "Write force field coefficients to files")
node("log",            "log",               "output",   "Set log file name")
node("print",          "print",             "output",   "Print text/variable to screen/log")

# ── Flow control ──
node("if",             "if",                "settings", "Conditional execution block")
node("jump",           "jump",              "settings", "Jump to labeled section in script")
node("label",          "label",             "settings", "Define a jump target label")
node("next",           "next",              "settings", "Skip to next iteration of jump loop")
node("include",        "include",           "settings", "Include another input script file")
node("quit",           "quit",              "settings", "Exit LAMMPS")
node("clear",          "clear",             "settings", "Clear all data and start fresh")
node("shell",          "shell",             "settings", "Execute shell command")
node("partition",      "partition",         "settings", "Multi-partition simulations")
node("timer",          "timer",             "settings", "Timer output controls")
node("info",           "info",              "settings", "Print system/compile info")
node("balance",        "balance",           "settings", "Load balance atoms across processors")

# ── Howto guides (Layer 4 — tutorial layer) ──
HOWTO_TOPICS = [
    ("Howto_restart",        "Restart a Simulation",                    "Save/restart simulation state"),
    ("Howto_2d",             "2D Simulations",                          "Setup for 2D systems"),
    ("Howto_triclinic",      "Triclinic Boxes",                         "Non-orthogonal simulation cells"),
    ("Howto_thermostat",     "Thermostats",                             "Temperature control: Nose-Hoover / Langevin / Berendsen / rescale"),
    ("Howto_barostat",       "Barostats",                               "Pressure control: Nose-Hoover / Berendsen"),
    ("Howto_walls",          "Walls",                                   "Reflecting / LJ walls for confinement"),
    ("Howto_nemd",           "NEMD Simulations",                        "Non-equilibrium MD"),
    ("Howto_dispersion",     "Long-Range Dispersion",                   "Tail corrections, long-range vdW"),
    ("Howto_broken_bonds",   "Broken Bonds",                            "Bond breaking and formation"),
    ("Howto_output",         "Output from LAMMPS",                      "Thermo, dumps, computes, fixes, variables"),
    ("Howto_structured_data","Output Structured Data",                  "JSON/YAML output from LAMMPS"),
    ("Howto_chunk",          "Use Chunks",                              "Spatial binning for analysis"),
    ("Howto_grid",           "Distributed Grids",                       "Grid-based calculations"),
    ("Howto_temperature",    "Calculate Temperature",                   "Temperature computation details"),
    ("Howto_elastic",        "Calculate Elastic Constants",             "Elastic tensor from MD"),
    ("Howto_kappa",          "Calculate Thermal Conductivity",          "Green-Kubo / Muller-Plathe"),
    ("Howto_viscosity",      "Calculate Viscosity",                     "Shear viscosity from MD"),
    ("Howto_diffusion",      "Calculate Diffusion Coefficient",         "MSD → D"),
    ("Howto_ff",             "Force Field Considerations",              "Choosing and using force fields"),
    ("Howto_charmm",         "CHARMM/AMBER/COMPASS/OPLS Force Fields",  "Biomolecular force fields"),
    ("Howto_amoeba",         "AMOEBA/HIPPO Force Fields",               "Polarizable force fields"),
    ("Howto_tip3p",          "TIP3P Water Model",                       "Rigid 3-site water"),
    ("Howto_tip4p",          "TIP4P/OPC Water Models",                  "Rigid 4-site water"),
    ("Howto_spc",            "SPC/SPC-E Water Model",                   "Simple point charge water"),
    ("Howto_body",           "Body Particles",                          "Rigid bodies, ellipsoids"),
    ("Howto_granular",       "Granular Models",                         "Granular interaction models"),
    ("Howto_bpm",            "Bonded Particle Models",                  "BPM for fracture"),
    ("Howto_polarizable",    "Polarizable Models",                      "Core-shell, Drude, CO2"),
    ("Howto_coreshell",      "Core/Shell Model",                        "Adiabatic core-shell"),
    ("Howto_drude",          "Drude Induced Dipoles",                   "Thermalized Drude oscillators"),
    ("Howto_peri",           "Peridynamics",                            "Peridynamic modeling"),
    ("Howto_manifold",       "Manifolds (Surfaces)",                    "Curved surface constraints"),
    ("Howto_rheo",           "RHEO",                                    "Hydrodynamics and elastic objects"),
    ("Howto_spin",           "Magnetic Spins",                          "Spin-lattice dynamics"),
    ("Howto_apip",           "Adaptive-Precision Potentials (APIP)",    "On-the-fly precision switching"),
    ("Howto_ldd",            "Local Density Dependent Potentials",      "Density-dependent interactions"),
    ("Howto_cmake",          "Using CMake with LAMMPS",                 "Build LAMMPS with CMake"),
    ("Howto_github",         "LAMMPS GitHub Tutorial",                  "Contributing via GitHub"),
    ("Howto_gui",            "LAMMPS-GUI Tutorial",                     "Using the LAMMPS GUI"),
    ("Howto_moltemplate",    "Moltemplate Tutorial",                    "System building with Moltemplate"),
    ("Howto_python",         "LAMMPS Python Tutorial",                  "Using LAMMPS from Python"),
    ("Howto_wsl",            "LAMMPS on Windows 10 WSL",                "Setup on Windows Subsystem for Linux"),
    ("Howto_lib",            "Library Interface to LAMMPS",             "Call LAMMPS from C/Fortran/Python"),
    ("Howto_couple",         "Coupling LAMMPS to Other Codes",          "MDI library coupling"),
    ("Howto_mdi",            "MDI Library for Code Coupling",           "MolSSI Driver Interface"),
    ("Howto_visualize",      "Visualize LAMMPS Snapshots",              "VMD / OVITO / ParaView"),
    ("Howto_dump_image",     "Advanced Dump Image Graphics",            "Ray-traced snapshot rendering"),
    ("Howto_multi_replica",  "Multi-Replica Simulations",               "Parallel replica runs"),
    ("Howto_multiple",       "Multiple Simulations from One Script",    "Multi-partition runs"),
    ("Howto_restart",        "Restart a Simulation",                    "Save/restart simulation state"),  # duplicate from above — intentional, restart is both general and settings
]
# Deduplicate
seen_h = set()
unique_howto = []
for h in HOWTO_TOPICS:
    if h[0] not in seen_h:
        unique_howto.append(h)
        seen_h.add(h[0])
HOWTO_TOPICS = unique_howto

for hid, htitle, hdesc in HOWTO_TOPICS:
    node(hid, htitle, "howto", hdesc)


# ═══════════════════════════════════════════════════════════════════
# EDGE DEFINITIONS (4 layers)
# ═══════════════════════════════════════════════════════════════════

EDGES = []

def edge(frm, to, etype, label=""):
    EDGES.append({"from": frm, "to": to, "type": etype, "label": label})

# ── Layer 1: REQUIRES — input script ordering ──
# "A must be set before B"

def requires(a, b, label=""):
    edge(a, b, "requires", label)

requires("read_data",    "units")
requires("read_data",    "boundary")
requires("create_box",   "units")
requires("create_box",   "boundary")
requires("create_box",   "region")
requires("create_atoms", "lattice")
requires("create_atoms", "region")
requires("create_atoms", "create_box")
requires("velocity",     "read_data")
requires("velocity",     "create_atoms")
requires("mass",         "read_data")
requires("mass",         "create_box")
requires("group",        "read_data")
requires("group",        "create_atoms")
requires("pair_coeff",   "pair_style")
requires("pair_coeff",   "mass")
requires("bond_coeff",   "bond_style")
requires("angle_coeff",  "angle_style")
requires("dihedral_coeff","dihedral_style")
requires("improper_coeff","improper_style")
requires("kspace_style", "pair_style")
requires("fix",          "read_data")
requires("fix",          "pair_style")
requires("compute",      "read_data")
requires("compute",      "group")
requires("minimize",     "read_data")
requires("minimize",     "pair_style")
requires("run",          "read_data")
requires("run",          "pair_style")
requires("run",          "fix")
requires("run",          "timestep")
requires("dump",         "read_data")
requires("dump",         "group")
requires("thermo_style", "read_data")
requires("thermo",       "read_data")
requires("timestep",     "units")
requires("write_data",   "read_data")
requires("write_restart","run")
requires("rerun",        "dump")

# Inter-fix dependencies
edge("fix_langevin",      "fix_nve",      "requires", "must use WITH")
edge("fix_temp_rescale",  "fix_nve",      "requires", "must use WITH")
edge("fix_press_berendsen","fix_nve",     "requires", "must use WITH")

# ── Layer 2: ALTERNATIVE — style family members ──
# "These are mutually-exclusive choices"

def alternative(frm, to, label=""):
    edge(frm, to, "alternative", label)

alternative("fix_nh",         "fix_nve",         "thermostat choice")
alternative("fix_nh",         "fix_langevin",    "Nose-Hoover vs Langevin")
alternative("fix_nh",         "fix_temp_rescale","Nose-Hoover vs simple rescale")
alternative("fix_langevin",   "fix_temp_rescale","Langevin vs simple rescale")
alternative("fix_press_berendsen","fix_nh",     "Berendsen vs Nose-Hoover (barostat)")
alternative("fix_deform",     "fix_nh",         "active vs passive deformation")

# ── Layer 3: CREATES — internal auto-creation by fixes/computes ──
# "This fix internally creates this compute"

def creates(frm, to, label=""):
    edge(frm, to, "creates", label)

creates("fix_nh",       "compute_temp",     "auto: fix_ID_temp")
creates("fix_nh",       "compute_pressure", "auto: fix_ID_press")
creates("fix_nve",      "compute_temp",     "auto: fix_ID_temp (if used with thermostat)")
creates("fix_langevin", "compute_temp",     "auto via fix_modify temp")
creates("compute_pressure","compute_temp",  "needs temp-ID input")
creates("thermo",       "compute_temp",     "default: thermo_temp")
creates("thermo",       "compute_pressure", "default: thermo_press")
creates("minimize",     "compute_temp",     "needs temperature")
creates("dump",         "compute_temp",     "per-atom temp (if requested)")

# ── Layer 4: HOWTO_REF — guide → commands ──
# "This tutorial covers these commands"

def howto_ref(hid, targets, label=""):
    for t in targets:
        edge(hid, t, "howto_ref", label)

howto_ref("Howto_thermostat",    ["fix_nh","fix_langevin","fix_temp_rescale","fix_nve","velocity"])
howto_ref("Howto_barostat",      ["fix_nh","fix_press_berendsen","fix_deform","compute_pressure","boundary"])
howto_ref("Howto_restart",       ["write_restart","read_restart","restart"])
howto_ref("Howto_2d",            ["dimension","boundary","change_box"])
howto_ref("Howto_triclinic",     ["change_box","boundary","read_data","create_box"])
howto_ref("Howto_walls",         ["fix","region","group"])
howto_ref("Howto_output",        ["thermo","thermo_style","thermo_modify","dump","dump_modify","compute","fix","variable"])
howto_ref("Howto_temperature",   ["compute_temp","thermo","thermo_modify"])
howto_ref("Howto_elastic",       ["compute","fix_deform","thermo_style","minimize"])
howto_ref("Howto_kappa",         ["compute","fix","thermo_style","run"])
howto_ref("Howto_viscosity",     ["compute","fix_deform","thermo_style"])
howto_ref("Howto_diffusion",     ["compute_msd","compute","fix","run"])
howto_ref("Howto_nemd",          ["fix_deform","fix","compute","thermo_style"])
howto_ref("Howto_dispersion",    ["pair_modify","kspace_style","pair_style"])
howto_ref("Howto_broken_bonds",  ["bond_style","bond_coeff","fix","pair_style"])
howto_ref("Howto_structured_data",["dump","dump_modify","thermo_style","compute","fix","variable"])
howto_ref("Howto_ff",            ["pair_style","pair_coeff","pair_modify","bond_style","angle_style","kspace_style","special_bonds"])
howto_ref("Howto_tip3p",         ["pair_style","bond_style","angle_style","fix","group","read_data"])
howto_ref("Howto_tip4p",         ["pair_style","bond_style","angle_style","fix","read_data"])
howto_ref("Howto_spc",           ["pair_style","bond_style","angle_style","fix","read_data"])
howto_ref("Howto_body",          ["fix","atom_style","pair_style","compute"])
howto_ref("Howto_granular",      ["pair_style","fix","atom_style","compute"])
howto_ref("Howto_spin",          ["fix","compute","pair_style","atom_style"])
howto_ref("Howto_coreshell",     ["pair_style","fix","atom_style","compute"])
howto_ref("Howto_drude",         ["pair_style","fix","atom_style","compute","thermo"])
howto_ref("Howto_chunk",         ["compute","fix","dump","thermo_style"])
howto_ref("Howto_grid",          ["compute","fix","dump"])
howto_ref("Howto_amoeba",        ["pair_style","bond_style","angle_style","fix","kspace_style"])
howto_ref("Howto_charmm",        ["pair_style","bond_style","angle_style","dihedral_style","improper_style","kspace_style","special_bonds"])
howto_ref("Howto_polarizable",   ["pair_style","fix","atom_style","compute","kspace_style"])
howto_ref("Howto_peri",          ["pair_style","fix","atom_style","compute","dump"])
howto_ref("Howto_manifold",      ["fix","compute"])
howto_ref("Howto_rheo",          ["fix","pair_style","compute"])
howto_ref("Howto_apip",          ["pair_style","pair_coeff"])
howto_ref("Howto_ldd",           ["pair_style","pair_coeff"])
howto_ref("Howto_multi_replica", ["partition","variable","run"])
howto_ref("Howto_multiple",      ["partition","variable","jump","label","next"])
howto_ref("Howto_couple",        ["fix","shell","molecule"])
howto_ref("Howto_lib",           ["fix","compute","dump","thermo"])
howto_ref("Howto_dump_image",    ["dump","dump_modify","region"])
howto_ref("Howto_visualize",     ["dump","dump_modify","write_dump"])


# ═══════════════════════════════════════════════════════════════════
# EXPORT
# ═══════════════════════════════════════════════════════════════════

def export():
    data = {
        "nodes": NODES,
        "edges": EDGES,
        "phases": PHASES,
    }
    json.dump(data, open(OUT, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"Exported: {len(NODES)} nodes, {len(EDGES)} edges → {OUT}")
    cats = {}
    for n in NODES:
        cats[n["phase"]] = cats.get(n["phase"], 0) + 1
    for phase, count in sorted(cats.items()):
        label = PHASES.get(phase, {}).get("label", phase)
        print(f"  {label}: {count}")

    etypes = {}
    for e in EDGES:
        etypes[e["type"]] = etypes.get(e["type"], 0) + 1
    print("Edges by type:")
    for t, c in sorted(etypes.items()):
        print(f"  {t}: {c}")


if __name__ == "__main__":
    export()
