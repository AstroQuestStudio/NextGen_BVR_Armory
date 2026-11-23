"""Blender 5.2 Blueprint-Faithful Mega Arsenal Builder (18 Ballistic, Anti-Ship, SEAD, Cruise, Bunker-Buster & Loitering EDMs).
Reads textures directly on C: drive and exports all .edm shapes to Saved Games/DCS/Mods/tech/NextGen_BVR_Armory/Shapes/
Also renders TWO 1920x1080 Cycles showcases:
  - preview_ballistic_naval_sead_v3.png
  - preview_cruise_drones_bombs_v3.png
"""

from __future__ import annotations

import math
import os
from pathlib import Path

import addon_utils
import bmesh
import bpy
from mathutils import Euler, Matrix, Quaternion, Vector

SHAPES_DIR = Path(r"C:\Users\trufa\Saved Games\DCS\Mods\tech\NextGen_BVR_Armory\Shapes")
TEX_DIR = Path(r"C:\Users\trufa\Saved Games\DCS\Mods\tech\NextGen_BVR_Armory\Textures\NextGen_BVR_Armory")
DEMO_BLEND = Path(os.environ["APPDATA"]) / "Blender Foundation" / "Blender" / "5.2" / "scripts" / "addons" / "io_scene_edm" / "Learning_Demo" / "Geomerty+Animation+Collision.blend"
PREVIEW_BNS = Path(r"C:\Users\trufa\.gemini\antigravity\brain\d63eda09-3e0f-4368-acac-466f620a5bd4\preview_ballistic_naval_sead_v3.png")
PREVIEW_CDB = Path(r"C:\Users\trufa\.gemini\antigravity\brain\d63eda09-3e0f-4368-acac-466f620a5bd4\preview_cruise_drones_bombs_v3.png")

U_BODY_MAX = 0.72


def clear_scene() -> None:
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for col in (bpy.data.meshes, bpy.data.materials, bpy.data.actions):
        for item in list(col):
            if item.users == 0:
                col.remove(item)


def create_edm_pbr_material(name: str, theme: str) -> bpy.types.Material:
    with bpy.data.libraries.load(str(DEMO_BLEND), link=False) as (data_from, data_to):
        data_to.materials = ["Txt"]
    mat = data_to.materials[0].copy()
    mat.name = name
    nt = mat.node_tree
    edm_node = next((n for n in nt.nodes if n.bl_idname == "EdmDefaultShaderNodeType"), None)
    a = bpy.data.images.load(str(TEX_DIR / f"ng_{theme}_albedo.png"), check_existing=True)
    n = bpy.data.images.load(str(TEX_DIR / f"ng_{theme}_normal.png"), check_existing=True)
    n.colorspace_settings.name = "Non-Color"
    r = bpy.data.images.load(str(TEX_DIR / f"ng_{theme}_roughmet.png"), check_existing=True)
    r.colorspace_settings.name = "Non-Color"
    if edm_node:
        for sock, img in (("Base Color", a), ("Color", a), ("Normal", n), ("RoughMet", r), ("Roughness/Metallic", r)):
            if sock in edm_node.inputs:
                t = nt.nodes.new("ShaderNodeTexImage")
                t.image = img
                nt.links.new(t.outputs["Color"], edm_node.inputs[sock])
    return mat


def create_preview_material(theme: str) -> bpy.types.Material:
    mat = bpy.data.materials.new(f"Preview_{theme}")
    mat.use_nodes = True
    nt = mat.node_tree
    bsdf = nt.nodes.get("Principled BSDF")
    ta = nt.nodes.new("ShaderNodeTexImage")
    ta.image = bpy.data.images.load(str(TEX_DIR / f"ng_{theme}_albedo.png"), check_existing=True)
    nt.links.new(ta.outputs["Color"], bsdf.inputs["Base Color"])
    tr = nt.nodes.new("ShaderNodeTexImage")
    tr.image = bpy.data.images.load(str(TEX_DIR / f"ng_{theme}_roughmet.png"), check_existing=True)
    tr.image.colorspace_settings.name = "Non-Color"
    sep = nt.nodes.new("ShaderNodeSeparateColor")
    nt.links.new(tr.outputs["Color"], sep.inputs["Color"])
    nt.links.new(sep.outputs["Green"], bsdf.inputs["Roughness"])
    nt.links.new(sep.outputs["Blue"], bsdf.inputs["Metallic"])
    tn = nt.nodes.new("ShaderNodeTexImage")
    tn.image = bpy.data.images.load(str(TEX_DIR / f"ng_{theme}_normal.png"), check_existing=True)
    tn.image.colorspace_settings.name = "Non-Color"
    nmap = nt.nodes.new("ShaderNodeNormalMap")
    nmap.inputs["Strength"].default_value = 1.1
    nt.links.new(tn.outputs["Color"], nmap.inputs["Color"])
    nt.links.new(nmap.outputs["Normal"], bsdf.inputs["Normal"])
    return mat


def make_obj(name: str, bm: bmesh.types.BMesh, mat: bpy.types.Material, location: tuple[float, float, float] = (0.0, 0.0, 0.0)) -> bpy.types.Object:
    mesh = bpy.data.meshes.new(name)
    bm.to_mesh(mesh)
    bm.free()
    obj = bpy.data.objects.new(name, mesh)
    obj.location = location
    bpy.context.scene.collection.objects.link(obj)
    obj.data.materials.clear()
    obj.data.materials.append(mat)
    return obj


def animate_rot_euler(obj: bpy.types.Object, action_name: str, fa: int, ra: tuple[float, float, float], fb: int, rb: tuple[float, float, float]) -> None:
    obj.rotation_mode = "XYZ"
    act = bpy.data.actions.new(name=action_name)
    obj.animation_data_create()
    obj.animation_data.action = act
    obj.rotation_euler = Euler([math.radians(a) for a in ra], "XYZ")
    obj.keyframe_insert(data_path="rotation_euler", frame=fa)
    obj.rotation_euler = Euler([math.radians(b) for b in rb], "XYZ")
    obj.keyframe_insert(data_path="rotation_euler", frame=fb)


def animate_rot_quat(obj: bpy.types.Object, action_name: str, fa: int, qa: Quaternion, fb: int, qb: Quaternion) -> None:
    obj.rotation_mode = "QUATERNION"
    act = bpy.data.actions.new(name=action_name)
    obj.animation_data_create()
    obj.animation_data.action = act
    obj.rotation_quaternion = qa
    obj.keyframe_insert(data_path="rotation_quaternion", frame=fa)
    obj.rotation_quaternion = qb
    obj.keyframe_insert(data_path="rotation_quaternion", frame=fb)


def solve_wing_fold_deg(tip_xy: tuple[float, float], side: float, target_x_offset: float = 0.06) -> float:
    x, y = tip_xy
    r = math.hypot(x, y)
    ang_dep = math.atan2(y, x)
    tx = side * target_x_offset
    ty = -math.sqrt(max(0.01, r * r - tx * tx))
    ang_tgt = math.atan2(ty, tx)
    return math.degrees((ang_tgt - ang_dep + math.pi) % (2.0 * math.pi) - math.pi)


def loft_rings(bm: bmesh.types.BMesh, uv, profile: list[tuple[float, float]], segs: int, y_min: float, y_max: float) -> None:
    rings = [[bm.verts.new((r * math.sin(2 * math.pi * i / segs), y, r * math.cos(2 * math.pi * i / segs))) for i in range(segs)] for y, r in profile]
    length = max(0.01, y_max - y_min)
    for idx in range(len(rings) - 1):
        y0, y1 = profile[idx][0], profile[idx + 1][0]
        v0 = 1.0 - max(0.0, min(1.0, (y_max - y0) / length))
        v1 = 1.0 - max(0.0, min(1.0, (y_max - y1) / length))
        r0, r1 = rings[idx], rings[idx + 1]
        for i in range(segs):
            ni = (i + 1) % segs
            u0, u1 = (i / segs) * U_BODY_MAX, ((i + 1) / segs) * U_BODY_MAX
            f = bm.faces.new((r0[i], r0[ni], r1[ni], r1[i]))
            f.smooth = True
            for lp, uvc in zip(f.loops, ((u0, v0), (u1, v0), (u1, v1), (u0, v1))):
                lp[uv].uv = uvc
    bm.faces.new(rings[-1]).smooth = True
    bm.faces.new(list(reversed(rings[0])))


def add_airfoil(bm: bmesh.types.BMesh, uv, root_le: Vector, tip_le: Vector, tip_te: Vector, root_te: Vector, ht_r: float, ht_t: float) -> None:
    n_up = (tip_le - root_le).cross(root_te - root_le)
    if n_up.length < 1e-6:
        n_up = Vector((0, 0, 1))
    n_up.normalize()
    vr = [bm.verts.new(root_le), bm.verts.new(root_le.lerp(root_te, 0.35) + n_up * ht_r), bm.verts.new(root_te), bm.verts.new(root_le.lerp(root_te, 0.35) - n_up * ht_r)]
    vt = [bm.verts.new(tip_le), bm.verts.new(tip_le.lerp(tip_te, 0.35) + n_up * ht_t), bm.verts.new(tip_te), bm.verts.new(tip_le.lerp(tip_te, 0.35) - n_up * ht_t)]
    u_pairs = [(0.728, 0.86), (0.86, 0.99), (0.99, 0.86), (0.86, 0.728)]
    for i in range(4):
        ni = (i + 1) % 4
        f = bm.faces.new((vr[i], vr[ni], vt[ni], vt[i]))
        ua, ub = u_pairs[i]
        for lp, uvc in zip(f.loops, ((ua, 0.48), (ub, 0.48), (ub, 0.97), (ua, 0.97))):
            lp[uv].uv = uvc
    for f in (bm.faces.new(list(reversed(vr))), bm.faces.new(vt)):
        for lp in f.loops:
            lp[uv].uv = (0.86, 0.97)


def build_cyl_body(name: str, length: float, diam: float, nose_len: float, blunt: float, mat: bpy.types.Material, segs: int = 56, boat: float = 0.82) -> bpy.types.Object:
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    r, half = diam * 0.5, length * 0.5
    nb = half - nose_len
    prof = [(-half + length * 0.03, 0.005), (-half, r * boat), (-half + length * 0.06, r), (nb, r)]
    for i in range(1, 15):
        t = i / 14.0
        rad = max(0.004, r * math.pow(max(0.0, 1.0 - t * 0.96), blunt))
        prof.append((nb + t * nose_len, rad))
    loft_rings(bm, uv, prof, segs, -half, half)
    return make_obj(name, bm, mat)


def fill_zone_uv(bm: bmesh.types.BMesh, uv, uvc: tuple[float, float]) -> None:
    for f in bm.faces:
        for lp in f.loops:
            if lp[uv].uv.length == 0:
                lp[uv].uv = uvc


# =========================================================================
# BALLISTIC & AEROBALLISTIC MISSILES
# =========================================================================
def b_kinzhal(mat: bpy.types.Material) -> list[bpy.types.Object]:
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    r = 0.525
    # 7.40m aeroballistic missile + white tapered carrier tail cone fairing
    prof = [(-3.70, 0.008), (-3.50, 0.16), (-3.05, r * 0.86), (-2.85, r), (1.75, r)]
    for i in range(1, 15):
        t = i / 14.0
        prof.append((1.75 + t * 1.95, max(0.008, r * math.pow(max(0.0, 1.0 - t * 0.94), 0.55))))
    loft_rings(bm, uv, prof, 64, -3.70, 3.70)
    # 4 compact aft cropped control fins right ahead of white tail fairing
    for k in range(4):
        rot = Matrix.Rotation(math.radians(45 + k * 90), 3, "Y")
        add_airfoil(bm, uv, rot @ Vector((0, -2.45, r * 0.92)), rot @ Vector((0, -2.72, r + 0.28)), rot @ Vector((0, -2.96, r + 0.28)), rot @ Vector((0, -2.92, r * 0.92)), 0.022, 0.010)
    return [make_obj("Kinzhal_Body", bm, mat)]


def b_arrw(mat: bpy.types.Material) -> list[bpy.types.Object]:
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    # Faceted 6-sided hypersonic boost-glide shroud nose + cylindrical booster + cruciform tail
    stations = [
        (-3.25, 0.26, 16), (-3.10, 0.36, 16), (0.60, 0.36, 16),
        (1.05, 0.36, 6), (2.25, 0.22, 6), (3.25, 0.01, 6),
    ]
    rings = []
    for y, r, _ in stations:
        rings.append([bm.verts.new((r * math.sin(2 * math.pi * i / 6), y, r * math.cos(2 * math.pi * i / 6))) for i in range(6)])
    for idx in range(len(rings) - 1):
        s0, s1 = rings[idx], rings[idx + 1]
        v0 = 1.0 - (3.25 - stations[idx][0]) / 6.50
        v1 = 1.0 - (3.25 - stations[idx + 1][0]) / 6.50
        for i in range(6):
            ni = (i + 1) % 6
            f = bm.faces.new((s0[i], s0[ni], s1[ni], s1[i]))
            for lp, uvc in zip(f.loops, (((i / 6) * U_BODY_MAX, v0), (((i + 1) / 6) * U_BODY_MAX, v0), (((i + 1) / 6) * U_BODY_MAX, v1), ((i / 6) * U_BODY_MAX, v1))):
                lp[uv].uv = uvc
    bm.faces.new(rings[-1])
    bm.faces.new(list(reversed(rings[0])))
    for k in range(4):
        rot = Matrix.Rotation(math.radians(45 + k * 90), 3, "Y")
        add_airfoil(bm, uv, rot @ Vector((0, -2.55, 0.32)), rot @ Vector((0, -2.90, 0.72)), rot @ Vector((0, -3.24, 0.72)), rot @ Vector((0, -3.18, 0.32)), 0.018, 0.008)
    return [make_obj("ARRW_Body", bm, mat)]


def b_rampage(mat: bpy.types.Material) -> list[bpy.types.Object]:
    objs = [build_cyl_body("Rampage_Body", 4.70, 0.306, 0.92, 0.65, mat)]
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    for k in range(4):
        rot = Matrix.Rotation(math.radians(45 + k * 90), 3, "Y")
        add_airfoil(bm, uv, rot @ Vector((0, 1.35, 0.14)), rot @ Vector((0, 1.24, 0.25)), rot @ Vector((0, 1.12, 0.25)), rot @ Vector((0, 1.12, 0.14)), 0.009, 0.004)
        add_airfoil(bm, uv, rot @ Vector((0, -1.78, 0.14)), rot @ Vector((0, -2.04, 0.42)), rot @ Vector((0, -2.28, 0.42)), rot @ Vector((0, -2.24, 0.14)), 0.012, 0.005)
    objs.append(make_obj("Rampage_Fins", bm, mat))
    return objs


# =========================================================================
# ANTI-SHIP & NAVAL MISSILES
# =========================================================================
def b_exocet_am39(mat: bpy.types.Material) -> list[bpy.types.Object]:
    objs = [build_cyl_body("Exocet_Body", 4.70, 0.350, 0.85, 0.58, mat)]
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    for k in range(4):
        rot = Matrix.Rotation(math.radians(45 + k * 90), 3, "Y")
        # 4 wide cropped delta mid-wings + 4 aft fins (NO side intakes!)
        add_airfoil(bm, uv, rot @ Vector((0, 0.35, 0.16)), rot @ Vector((0, -0.35, 0.55)), rot @ Vector((0, -0.58, 0.55)), rot @ Vector((0, -0.58, 0.16)), 0.015, 0.007)
        add_airfoil(bm, uv, rot @ Vector((0, -1.78, 0.15)), rot @ Vector((0, -2.02, 0.40)), rot @ Vector((0, -2.24, 0.40)), rot @ Vector((0, -2.22, 0.15)), 0.012, 0.005)
    objs.append(make_obj("Exocet_Wings", bm, mat))
    return objs


def b_kh35u(mat: bpy.types.Material) -> list[bpy.types.Object]:
    objs = [build_cyl_body("Kh35_Body", 3.85, 0.420, 0.65, 0.46, mat)]
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    # Distinctive semi-submerged ventral turbojet intake duct
    in_f = [Vector((-0.10, 0.15, -0.18)), Vector((0.10, 0.15, -0.18)), Vector((0.085, 0.10, -0.33)), Vector((-0.085, 0.10, -0.33))]
    in_b = [Vector((-0.09, -1.35, -0.18)), Vector((0.09, -1.35, -0.18)), Vector((0.075, -1.35, -0.25)), Vector((-0.075, -1.35, -0.25))]
    vf = [bm.verts.new(p) for p in in_f]
    vb = [bm.verts.new(p) for p in in_b]
    for i in range(4):
        ni = (i + 1) % 4
        f = bm.faces.new((vf[i], vf[ni], vb[ni], vb[i]))
        for lp in f.loops:
            lp[uv].uv = (0.85, 0.30)
    f_m = bm.faces.new(vf)
    for lp in f_m.loops:
        lp[uv].uv = (0.85, 0.06)
    for k in range(4):
        rot = Matrix.Rotation(math.radians(45 + k * 90), 3, "Y")
        add_airfoil(bm, uv, rot @ Vector((0, -1.42, 0.19)), rot @ Vector((0, -1.64, 0.44)), rot @ Vector((0, -1.86, 0.44)), rot @ Vector((0, -1.82, 0.19)), 0.012, 0.005)
    objs.append(make_obj("Kh35_Intake_Tail", bm, mat))

    # 4 Animated Folding Cruciform Mid-Wings (DrawArg 25)
    for k in range(4):
        rot = Matrix.Rotation(math.radians(45 + k * 90), 3, "Y")
        bm_w = bmesh.new()
        uv_w = bm_w.loops.layers.uv.new("UVMap")
        add_airfoil(bm_w, uv_w, rot @ Vector((0, 0.20, 0)), rot @ Vector((0, 0.02, 0.48)), rot @ Vector((0, -0.20, 0.48)), rot @ Vector((0, -0.20, 0)), 0.012, 0.005)
        piv = rot @ Vector((0, 0.12, 0.195))
        w_obj = make_obj(f"Kh35_Wing_{k}", bm_w, mat, location=(piv.x, 0.12, piv.z))
        axis = (rot @ Vector((1, 0, 0))).normalized()
        animate_rot_quat(w_obj, f"25_Kh35_Wing_{k}", 100, Quaternion(axis, math.radians(82.0)), 200, Quaternion((1, 0, 0, 0)))
        objs.append(w_obj)
    return objs


def b_nsm_jsm(mat: bpy.types.Material) -> list[bpy.types.Object]:
    objs = []
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    L = 3.96
    half = L * 0.5

    def pent_ring(y: float, w: float, ht: float, hb: float) -> list[bmesh.types.BMVert]:
        pts = [(0, y, ht), (w * 0.50, y, ht * 0.35), (w * 0.36, y, -hb), (-w * 0.36, y, -hb), (-w * 0.50, y, ht * 0.35)]
        return [bm.verts.new(p) for p in pts]

    sts = [(-1.98, 0.18, 0.10, 0.10), (-1.55, 0.38, 0.18, 0.17), (1.05, 0.38, 0.18, 0.17), (1.62, 0.24, 0.11, 0.10), (1.98, 0.03, 0.015, 0.015)]
    rings = [pent_ring(*s) for s in sts]
    for idx in range(len(rings) - 1):
        s0, s1 = rings[idx], rings[idx + 1]
        v0 = 1.0 - (half - sts[idx][0]) / L
        v1 = 1.0 - (half - sts[idx + 1][0]) / L
        for i in range(5):
            ni = (i + 1) % 5
            f = bm.faces.new((s0[i], s0[ni], s1[ni], s1[i]))
            for lp, uvc in zip(f.loops, (((i / 5) * U_BODY_MAX, v0), (((i + 1) / 5) * U_BODY_MAX, v0), (((i + 1) / 5) * U_BODY_MAX, v1), ((i / 5) * U_BODY_MAX, v1))):
                lp[uv].uv = uvc
    bm.faces.new(rings[-1])
    bm.faces.new(list(reversed(rings[0])))
    for k in range(4):
        rot = Matrix.Rotation(math.radians(45 + k * 90), 3, "Y")
        add_airfoil(bm, uv, rot @ Vector((0, -1.52, 0.13)), rot @ Vector((0, -1.72, 0.34)), rot @ Vector((0, -1.92, 0.34)), rot @ Vector((0, -1.88, 0.13)), 0.008, 0.004)
    objs.append(make_obj("NSM_StealthBody", bm, mat))

    # DrawArg 25 Folding Swept Mid-Wings
    for side, s_name in ((-1.0, "L"), (1.0, "R")):
        r_le, t_le, t_te, r_te = Vector((0, 0.16, 0)), Vector((side * 0.62, -0.38, 0)), Vector((side * 0.62, -0.56, 0)), Vector((0, -0.16, 0))
        fd = solve_wing_fold_deg((t_le.x, t_le.y), side, target_x_offset=0.05)
        bm_w = bmesh.new()
        uv_w = bm_w.loops.layers.uv.new("UVMap")
        add_airfoil(bm_w, uv_w, r_le, t_le, t_te, r_te, 0.011, 0.005)
        w_obj = make_obj(f"NSM_Wing_{s_name}", bm_w, mat, location=(side * 0.10, 0.12, 0.145))
        animate_rot_euler(w_obj, f"25_NSM_Wing_{s_name}", 100, (0, 0, fd), 200, (0, 0, 0))
        objs.append(w_obj)
    return objs


def b_kh22_32(mat: bpy.types.Material) -> list[bpy.types.Object]:
    objs = []
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    r = 0.460
    # 11.60m heavy missile with annular nose lip + central shock cone
    prof = [(-5.80, 0.22), (-5.55, 0.34), (-4.80, r), (4.60, r), (5.35, r * 0.85), (5.50, r * 0.72), (5.20, r * 0.55), (5.80, 0.01)]
    loft_rings(bm, uv, prof, 64, -5.80, 5.80)
    # Wide swept delta wings + tall dorsal vertical stabilizer + horizontal tailplanes
    for side in (-1.0, 1.0):
        add_airfoil(bm, uv, Vector((side * 0.42, 0.60, -0.04)), Vector((side * 1.55, -2.40, -0.06)), Vector((side * 1.55, -3.10, -0.06)), Vector((side * 0.42, -3.00, -0.04)), 0.032, 0.012)
        add_airfoil(bm, uv, Vector((side * 0.34, -4.40, 0.02)), Vector((side * 1.10, -5.15, 0.02)), Vector((side * 1.10, -5.65, 0.02)), Vector((side * 0.34, -5.60, 0.02)), 0.022, 0.008)
    add_airfoil(bm, uv, Vector((0, -3.80, 0.40)), Vector((0, -4.95, 1.48)), Vector((0, -5.70, 1.48)), Vector((0, -5.65, 0.40)), 0.024, 0.010)
    objs.append(make_obj("Kh22_Airframe", bm, mat))

    # DrawArg 25 Folding Ventral Stabilizer Fin (folds 90 deg sideways for bomber clearance!)
    bm_v = bmesh.new()
    uv_v = bm_v.loops.layers.uv.new("UVMap")
    add_airfoil(bm_v, uv_v, Vector((0, 0.40, 0)), Vector((0, -0.10, -0.68)), Vector((0, -0.58, -0.68)), Vector((0, -0.55, 0)), 0.020, 0.009)
    vf_obj = make_obj("Kh22_VentralFin", bm_v, mat, location=(0.0, -4.95, -0.40))
    animate_rot_euler(vf_obj, "25_Kh22_VentralFin", 100, (0, 88.0, 0), 200, (0, 0, 0))
    objs.append(vf_obj)
    return objs


def b_zircon(mat: bpy.types.Material) -> list[bpy.types.Object]:
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    L = 8.50
    half = L * 0.5

    def wr(y: float, w: float, ht: float, hb: float) -> list[bmesh.types.BMVert]:
        return [bm.verts.new(p) for p in ((0, y, ht), (w * 0.48, y, ht * 0.25), (w * 0.52, y, -hb * 0.25), (w * 0.28, y, -hb), (-w * 0.28, y, -hb), (-w * 0.52, y, -hb * 0.25), (-w * 0.48, y, ht * 0.25))]

    sts = [(-4.25, 0.34, 0.16, 0.16), (-3.85, 0.56, 0.26, 0.24), (2.20, 0.56, 0.26, 0.24), (3.45, 0.38, 0.16, 0.12), (4.25, 0.03, 0.015, 0.01)]
    rings = [wr(*s) for s in sts]
    for idx in range(len(rings) - 1):
        s0, s1 = rings[idx], rings[idx + 1]
        v0 = 1.0 - (half - sts[idx][0]) / L
        v1 = 1.0 - (half - sts[idx + 1][0]) / L
        for i in range(7):
            ni = (i + 1) % 7
            f = bm.faces.new((s0[i], s0[ni], s1[ni], s1[i]))
            for lp, uvc in zip(f.loops, (((i / 7) * U_BODY_MAX, v0), (((i + 1) / 7) * U_BODY_MAX, v0), (((i + 1) / 7) * U_BODY_MAX, v1), ((i / 7) * U_BODY_MAX, v1))):
                lp[uv].uv = uvc
    bm.faces.new(rings[-1])
    bm.faces.new(list(reversed(rings[0])))
    for k in range(4):
        rot = Matrix.Rotation(math.radians(45 + k * 90), 3, "Y")
        add_airfoil(bm, uv, rot @ Vector((0, -3.20, 0.24)), rot @ Vector((0, -3.65, 0.56)), rot @ Vector((0, -4.15, 0.56)), rot @ Vector((0, -4.10, 0.24)), 0.016, 0.007)
    return [make_obj("Zircon_Waverider", bm, mat)]


# =========================================================================
# SEAD / ANTI-RADIATION MISSILES
# =========================================================================
def b_aargm_er(mat: bpy.types.Material) -> list[bpy.types.Object]:
    objs = [build_cyl_body("AARGMER_Body", 4.06, 0.292, 0.78, 0.62, mat)]
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    for k in range(4):
        rot = Matrix.Rotation(math.radians(45 + k * 90), 3, "Y")
        # Long low-profile conformal mid-body strakes + small aft control fins
        add_airfoil(bm, uv, rot @ Vector((0, 0.68, 0.140)), rot @ Vector((0, 0.35, 0.208)), rot @ Vector((0, -1.25, 0.208)), rot @ Vector((0, -1.35, 0.140)), 0.014, 0.006)
        add_airfoil(bm, uv, rot @ Vector((0, -1.58, 0.140)), rot @ Vector((0, -1.78, 0.320)), rot @ Vector((0, -1.98, 0.320)), rot @ Vector((0, -1.96, 0.140)), 0.011, 0.005)
    objs.append(make_obj("AARGMER_StrakesFins", bm, mat))
    return objs


def b_kh58ushke(mat: bpy.types.Material) -> list[bpy.types.Object]:
    objs = [build_cyl_body("Kh58_Body", 4.19, 0.380, 0.85, 0.64, mat)]
    # Animated Folding Mid-Body Delta Wings + Folding Aft Tail Fins (DrawArg 25)
    for k in range(4):
        rot = Matrix.Rotation(math.radians(45 + k * 90), 3, "Y")
        axis = (rot @ Vector((1, 0, 0))).normalized()

        bm_w = bmesh.new()
        uv_w = bm_w.loops.layers.uv.new("UVMap")
        add_airfoil(bm_w, uv_w, rot @ Vector((0, 0.42, 0)), rot @ Vector((0, -0.18, 0.34)), rot @ Vector((0, -0.45, 0.34)), rot @ Vector((0, -0.45, 0)), 0.012, 0.005)
        pw = rot @ Vector((0, 0.05, 0.182))
        w_obj = make_obj(f"Kh58_Wing_{k}", bm_w, mat, location=(pw.x, 0.05, pw.z))
        animate_rot_quat(w_obj, f"25_Kh58_Wing_{k}", 100, Quaternion(axis, math.radians(82.0)), 200, Quaternion((1, 0, 0, 0)))
        objs.append(w_obj)

        bm_f = bmesh.new()
        uv_f = bm_f.loops.layers.uv.new("UVMap")
        add_airfoil(bm_f, uv_f, rot @ Vector((0, 0.22, 0)), rot @ Vector((0, -0.02, 0.26)), rot @ Vector((0, -0.22, 0.26)), rot @ Vector((0, -0.22, 0)), 0.010, 0.004)
        pf = rot @ Vector((0, -1.80, 0.180))
        f_obj = make_obj(f"Kh58_Fin_{k}", bm_f, mat, location=(pf.x, -1.80, pf.z))
        animate_rot_quat(f_obj, f"25_Kh58_Fin_{k}", 100, Quaternion(axis, math.radians(82.0)), 200, Quaternion((1, 0, 0, 0)))
        objs.append(f_obj)
    return objs


def b_alarm_sead(mat: bpy.types.Material) -> list[bpy.types.Object]:
    objs = [build_cyl_body("ALARM_Body", 4.24, 0.230, 0.72, 0.65, mat)]
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    for k in range(4):
        rot = Matrix.Rotation(math.radians(45 + k * 90), 3, "Y")
        add_airfoil(bm, uv, rot @ Vector((0, 0.48, 0.110)), rot @ Vector((0, -0.18, 0.42)), rot @ Vector((0, -0.45, 0.42)), rot @ Vector((0, -0.45, 0.110)), 0.011, 0.005)
        add_airfoil(bm, uv, rot @ Vector((0, -1.68, 0.108)), rot @ Vector((0, -1.92, 0.30)), rot @ Vector((0, -2.08, 0.30)), rot @ Vector((0, -2.06, 0.108)), 0.009, 0.004)
    objs.append(make_obj("ALARM_Fins", bm, mat))
    return objs


def b_spear_ew(mat: bpy.types.Material) -> list[bpy.types.Object]:
    objs = [build_cyl_body("SPEAR_Body", 1.80, 0.180, 0.32, 0.54, mat)]
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    for k in range(4):
        rot = Matrix.Rotation(math.radians(45 + k * 90), 3, "Y")
        add_airfoil(bm, uv, rot @ Vector((0, -0.68, 0.082)), rot @ Vector((0, -0.78, 0.22)), rot @ Vector((0, -0.88, 0.22)), rot @ Vector((0, -0.86, 0.082)), 0.007, 0.003)
    objs.append(make_obj("SPEAR_Tail", bm, mat))
    for side, sn in ((-1.0, "L"), (1.0, "R")):
        r_le, t_le, t_te, r_te = Vector((0, 0.16, 0)), Vector((side * 0.78, -0.42, 0)), Vector((side * 0.78, -0.56, 0)), Vector((0, -0.14, 0))
        fd = solve_wing_fold_deg((t_le.x, t_le.y), side, target_x_offset=0.05)
        bm_w = bmesh.new()
        uv_w = bm_w.loops.layers.uv.new("UVMap")
        add_airfoil(bm_w, uv_w, r_le, t_le, t_te, r_te, 0.009, 0.004)
        w_obj = make_obj(f"SPEAR_Wing_{sn}", bm_w, mat, location=(side * 0.04, 0.08, 0.095))
        animate_rot_euler(w_obj, f"25_SPEAR_Wing_{sn}", 100, (0, 0, fd), 200, (0, 0, 0))
        objs.append(w_obj)
    return objs


# =========================================================================
# BUNKER BUSTERS, SMART BOMBS, CRUISE & LOITERING DRONES
# =========================================================================
def b_gbu57_mop(mat: bpy.types.Material) -> list[bpy.types.Object]:
    objs = [build_cyl_body("MOP_Body", 6.20, 0.800, 1.15, 0.50, mat, segs=64, boat=0.92)]
    bm_s = bmesh.new()
    uv_s = bm_s.loops.layers.uv.new("UVMap")
    for k in range(4):
        rot = Matrix.Rotation(math.radians(45 + k * 90), 3, "Y")
        add_airfoil(bm_s, uv_s, rot @ Vector((0, 0.65, 0.38)), rot @ Vector((0, 0.35, 0.48)), rot @ Vector((0, -0.65, 0.48)), rot @ Vector((0, -0.75, 0.38)), 0.018, 0.008)
    objs.append(make_obj("MOP_Strakes", bm_s, mat))

    # 4 Huge Open Lattice Grid Tail Fins (DrawArg 25)
    for k in range(4):
        rot = Matrix.Rotation(math.radians(45 + k * 90), 3, "Y")
        bm_g = bmesh.new()
        uv_g = bm_g.loops.layers.uv.new("UVMap")
        bar = 0.014
        w, h, d, cells = 0.52, 0.56, 0.11, 4
        for i in range(cells + 1):
            x = -w * 0.5 + (i / cells) * w
            ret = bmesh.ops.create_cube(bm_g, size=1.0)
            for v in ret["verts"]:
                v.co = rot @ Vector((v.co.x * bar + x, v.co.y * d, (v.co.z + 0.5) * h))
        for j in range(cells + 1):
            z = (j / cells) * h
            ret = bmesh.ops.create_cube(bm_g, size=1.0)
            for v in ret["verts"]:
                v.co = rot @ Vector((v.co.x * w, v.co.y * d, v.co.z * bar + z))
        fill_zone_uv(bm_g, uv_g, (0.85, 0.30))
        piv = rot @ Vector((0, -2.72, 0.38))
        g_obj = make_obj(f"MOP_GridFin_{k}", bm_g, mat, location=(piv.x, -2.72, piv.z))
        axis = (rot @ Vector((1, 0, 0))).normalized()
        animate_rot_quat(g_obj, f"25_MOP_Grid_{k}", 100, Quaternion(axis, math.radians(84.0)), 200, Quaternion((1, 0, 0, 0)))
        objs.append(g_obj)
    return objs


def b_spice_glide(mat: bpy.types.Material) -> list[bpy.types.Object]:
    objs = [build_cyl_body("SPICE_Body", 3.60, 0.360, 0.55, 0.42, mat, boat=0.80)]
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    for k in range(4):
        rot = Matrix.Rotation(math.radians(45 + k * 90), 3, "Y")
        add_airfoil(bm, uv, rot @ Vector((0, 1.15, 0.16)), rot @ Vector((0, 1.02, 0.32)), rot @ Vector((0, 0.88, 0.32)), rot @ Vector((0, 0.88, 0.16)), 0.011, 0.005)
        add_airfoil(bm, uv, rot @ Vector((0, -1.35, 0.16)), rot @ Vector((0, -1.55, 0.42)), rot @ Vector((0, -1.75, 0.42)), rot @ Vector((0, -1.72, 0.16)), 0.012, 0.005)
    objs.append(make_obj("SPICE_CanardTail", bm, mat))
    for side, sn in ((-1.0, "L"), (1.0, "R")):
        r_le, t_le, t_te, r_te = Vector((0, 0.20, 0)), Vector((side * 0.96, -0.45, 0)), Vector((side * 0.96, -0.68, 0)), Vector((0, -0.22, 0))
        fd = solve_wing_fold_deg((t_le.x, t_le.y), side, target_x_offset=0.06)
        bm_w = bmesh.new()
        uv_w = bm_w.loops.layers.uv.new("UVMap")
        add_airfoil(bm_w, uv_w, r_le, t_le, t_te, r_te, 0.013, 0.005)
        w_obj = make_obj(f"SPICE_Wing_{sn}", bm_w, mat, location=(side * 0.08, 0.10, 0.175))
        animate_rot_euler(w_obj, f"25_SPICE_Wing_{sn}", 100, (0, 0, fd), 200, (0, 0, 0))
        objs.append(w_obj)
    return objs


def b_shahed_136(mat: bpy.types.Material) -> list[bpy.types.Object]:
    objs = [build_cyl_body("Shahed_Fuselage", 3.50, 0.320, 0.55, 0.55, mat, boat=0.72)]
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    for side in (-1.0, 1.0):
        # Iconic cropped-delta flying wing (2.5m total span)
        add_airfoil(bm, uv, Vector((side * 0.12, 1.05, 0.0)), Vector((side * 1.25, -0.95, 0.0)), Vector((side * 1.25, -1.65, 0.0)), Vector((side * 0.12, -1.65, 0.0)), 0.042, 0.018)
        # Up-and-down wingtip endplate rudders
        add_airfoil(bm, uv, Vector((side * 1.24, -0.95, 0.0)), Vector((side * 1.24, -1.18, 0.30)), Vector((side * 1.24, -1.65, 0.30)), Vector((side * 1.24, -1.65, 0.0)), 0.012, 0.006)
        add_airfoil(bm, uv, Vector((side * 1.24, -0.95, 0.0)), Vector((side * 1.24, -1.18, -0.26)), Vector((side * 1.24, -1.65, -0.26)), Vector((side * 1.24, -1.65, 0.0)), 0.012, 0.006)
    objs.append(make_obj("Shahed_DeltaWing", bm, mat))
    bm_p = bmesh.new()
    uv_p = bm_p.loops.layers.uv.new("UVMap")
    for side in (-1.0, 1.0):
        add_airfoil(bm_p, uv_p, Vector((side * 0.02, 0.016, 0)), Vector((side * 0.34, 0.020, 0)), Vector((side * 0.34, -0.020, 0)), Vector((side * 0.02, -0.016, 0)), 0.008, 0.003)
    prop = make_obj("Shahed_Prop", bm_p, mat, location=(0, -1.72, 0))
    animate_rot_euler(prop, "407_Shahed_Prop", 100, (0, 0, 0), 200, (0, 360, 0))
    objs.append(prop)
    return objs


def b_harop(mat: bpy.types.Material) -> list[bpy.types.Object]:
    objs = [build_cyl_body("Harop_Fuselage", 2.50, 0.280, 0.45, 0.55, mat, boat=0.68)]
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    for side in (-1.0, 1.0):
        # Forward canards + large swept delta wing
        add_airfoil(bm, uv, Vector((side * 0.11, 0.85, 0.02)), Vector((side * 0.48, 0.65, 0.02)), Vector((side * 0.48, 0.48, 0.02)), Vector((side * 0.11, 0.52, 0.02)), 0.012, 0.005)
        add_airfoil(bm, uv, Vector((side * 0.12, 0.35, 0.0)), Vector((side * 1.48, -0.82, 0.0)), Vector((side * 1.48, -1.16, 0.0)), Vector((side * 0.12, -1.08, 0.0)), 0.024, 0.008)
    # Single tall dorsal vertical stabilizer
    add_airfoil(bm, uv, Vector((0, -0.45, 0.12)), Vector((0, -0.92, 0.56)), Vector((0, -1.22, 0.56)), Vector((0, -1.18, 0.12)), 0.016, 0.006)
    # Spherical EO/IR gimbal ball under chin
    ret = bmesh.ops.create_uvsphere(bm, u_segments=24, v_segments=16, radius=0.11)
    bmesh.ops.translate(bm, verts=ret["verts"], vec=(0.0, 0.92, -0.14))
    for f in bm.faces:
        if all(v.co.y > 0.78 and v.co.z < -0.02 for v in f.verts):
            for lp in f.loops:
                lp[uv].uv = (0.85, 0.05)
    objs.append(make_obj("Harop_Airframe", bm, mat))
    bm_p = bmesh.new()
    uv_p = bm_p.loops.layers.uv.new("UVMap")
    for side in (-1.0, 1.0):
        add_airfoil(bm_p, uv_p, Vector((side * 0.02, 0.015, 0)), Vector((side * 0.32, 0.018, 0)), Vector((side * 0.32, -0.018, 0)), Vector((side * 0.02, -0.015, 0)), 0.007, 0.003)
    prop = make_obj("Harop_Prop", bm_p, mat, location=(0, -1.25, 0))
    animate_rot_euler(prop, "407_Harop_Prop", 100, (0, 0, 0), 200, (0, 360, 0))
    objs.append(prop)
    return objs


def b_scalp_blunt(mat: bpy.types.Material) -> list[bpy.types.Object]:
    """Photo-faithful SCALP-EG / Storm Shadow with blunt rounded-chisel nose + DrawArg 25 wings/tails."""
    objs = []
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    L = 5.10
    half = L * 0.5

    def sc_ring(y: float, w: float, ht: float, hb: float, zs: float = 0.0) -> list[bmesh.types.BMVert]:
        pts = [
            (0.0, y, ht + zs), (w * 0.24, y, ht * 0.94 + zs), (w * 0.40, y, ht * 0.70 + zs),
            (w * 0.49, y, ht * 0.28 + zs), (w * 0.52, y, 0.0 + zs), (w * 0.46, y, -hb * 0.48 + zs),
            (w * 0.34, y, -hb * 0.86 + zs), (w * 0.16, y, -hb + zs), (-w * 0.16, y, -hb + zs),
            (-w * 0.34, y, -hb * 0.86 + zs), (-w * 0.46, y, -hb * 0.48 + zs), (-w * 0.52, y, 0.0 + zs),
            (-w * 0.49, y, ht * 0.28 + zs), (-w * 0.40, y, ht * 0.70 + zs), (-w * 0.24, y, ht * 0.94 + zs),
        ]
        return [bm.verts.new(p) for p in pts]

    stations = []
    for k in range(31):
        t = k / 30.0
        y = -half + t * L
        if t < 0.08:
            st = t / 0.08
            w, ht, hb, zs = 0.30 + 0.18 * math.sin(st * math.pi * 0.5), 0.15 + 0.07 * math.sin(st * math.pi * 0.5), 0.15 + 0.07 * math.sin(st * math.pi * 0.5), 0.02 * (1 - st)
        elif t < 0.78:
            w, ht, hb, zs = 0.63, 0.24, 0.24, 0.0
        else:
            # Blunt rounded-chisel nose (like Storm Shadow #03, #06, #14!)
            st = (t - 0.78) / 0.22
            e = math.pow(max(0.0, 1.0 - st * 0.96), 0.44)
            w, ht, hb, zs = max(0.05, 0.63 * e), max(0.025, 0.24 * e), max(0.025, 0.24 * e), -0.05 * st
        stations.append((y, w, ht, hb, zs))

    rings = [sc_ring(*st) for st in stations]
    np_v = len(rings[0])
    for idx in range(len(rings) - 1):
        s0, s1 = rings[idx], rings[idx + 1]
        v0, v1 = 1.0 - (half - stations[idx][0]) / L, 1.0 - (half - stations[idx + 1][0]) / L
        for i in range(np_v):
            ni = (i + 1) % np_v
            f = bm.faces.new((s0[i], s0[ni], s1[ni], s1[i]))
            f.smooth = True
            for lp, uvc in zip(f.loops, (((i / np_v) * U_BODY_MAX, v0), (((i + 1) / np_v) * U_BODY_MAX, v0), (((i + 1) / np_v) * U_BODY_MAX, v1), ((i / np_v) * U_BODY_MAX, v1))):
                lp[uv].uv = uvc
    bm.faces.new(rings[-1])
    bm.faces.new(list(reversed(rings[0])))

    spine = bmesh.ops.create_cube(bm, size=1.0)
    for v in spine["verts"]:
        v.co.x *= 0.24
        v.co.y = v.co.y * 2.10 + 0.10
        v.co.z = v.co.z * 0.032 + 0.245
    in_f = [Vector((-0.14, 0.30, -0.22)), Vector((0.14, 0.30, -0.22)), Vector((0.11, 0.24, -0.35)), Vector((-0.11, 0.24, -0.35))]
    in_b = [Vector((-0.12, -1.15, -0.22)), Vector((0.12, -1.15, -0.22)), Vector((0.09, -1.15, -0.26)), Vector((-0.09, -1.15, -0.26))]
    vf = [bm.verts.new(p) for p in in_f]
    vb = [bm.verts.new(p) for p in in_b]
    for i in range(4):
        ni = (i + 1) % 4
        bm.faces.new((vf[i], vf[ni], vb[ni], vb[i]))
    fm = bm.faces.new(vf)
    for lp in fm.loops:
        lp[uv].uv = (0.85, 0.06)
    fill_zone_uv(bm, uv, (0.35, 0.55))
    objs.append(make_obj("SCALP_Blunt_Airframe", bm, mat))

    for side, sn in ((-1.0, "L"), (1.0, "R")):
        r_le, t_le, t_te, r_te = Vector((0, 0.28, 0)), Vector((side * 1.36, -0.66, -0.02)), Vector((side * 1.36, -0.94, -0.02)), Vector((0, -0.22, 0))
        fd = solve_wing_fold_deg((t_le.x, t_le.y), side, target_x_offset=0.06)
        bm_w = bmesh.new()
        uv_w = bm_w.loops.layers.uv.new("UVMap")
        add_airfoil(bm_w, uv_w, r_le, t_le, t_te, r_te, 0.015, 0.007)
        w_obj = make_obj(f"SCALP_Wing_{sn}", bm_w, mat, location=(side * 0.14, 0.35, 0.245))
        animate_rot_euler(w_obj, f"25_SCALP_Wing_{sn}", 100, (0, 0, fd), 200, (0, 0, 0))
        objs.append(w_obj)

        hr_le, ht_le, ht_te, hr_te = Vector((0, 0.12, 0)), Vector((side * 0.44, -0.18, 0)), Vector((side * 0.44, -0.34, 0)), Vector((0, -0.22, 0))
        hf = solve_wing_fold_deg((ht_le.x, ht_le.y), side, target_x_offset=0.02)
        bm_h = bmesh.new()
        uv_h = bm_h.loops.layers.uv.new("UVMap")
        add_airfoil(bm_h, uv_h, hr_le, ht_le, ht_te, hr_te, 0.009, 0.004)
        h_obj = make_obj(f"SCALP_HTail_{sn}", bm_h, mat, location=(side * 0.16, -2.08, 0.01))
        animate_rot_euler(h_obj, f"25_SCALP_HTail_{sn}", 100, (0, 0, hf), 200, (0, 0, 0))
        objs.append(h_obj)

        bm_v = bmesh.new()
        uv_v = bm_v.loops.layers.uv.new("UVMap")
        rot_v = Matrix.Rotation(math.radians(side * 24.0), 3, "Y")
        add_airfoil(bm_v, uv_v, rot_v @ Vector((0, 0.10, 0)), rot_v @ Vector((0, -0.18, 0.34)), rot_v @ Vector((0, -0.36, 0.34)), rot_v @ Vector((0, -0.24, 0)), 0.009, 0.005)
        v_obj = make_obj(f"SCALP_VTail_{sn}", bm_v, mat, location=(side * 0.14, -2.10, 0.17))
        animate_rot_quat(v_obj, f"25_SCALP_VTail_{sn}", 100, Quaternion((rot_v @ Vector((1, 0, 0))).normalized(), math.radians(78.0)), 200, Quaternion((1, 0, 0, 0)))
        objs.append(v_obj)
    return objs


def b_taurus_new(mat: bpy.types.Material) -> list[bpy.types.Object]:
    objs = []
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    L = 5.10
    half = L * 0.5

    def tr(y: float, w: float, h: float, zs: float = 0.0) -> list[bmesh.types.BMVert]:
        return [bm.verts.new(p) for p in ((0, y, h * 0.48 + zs), (w * 0.38, y, h * 0.48 + zs), (w * 0.50, y, h * 0.08 + zs), (w * 0.44, y, -h * 0.46 + zs), (0, y, -h * 0.50 + zs), (-w * 0.44, y, -h * 0.46 + zs), (-w * 0.50, y, h * 0.08 + zs), (-w * 0.38, y, h * 0.48 + zs))]

    sts = []
    for k in range(25):
        t = k / 24.0
        y = -half + t * L
        if t < 0.08:
            st = t / 0.08
            w, h, zs = 0.32 + 0.24 * st, 0.24 + 0.20 * st, 0.0
        elif t < 0.76:
            w, h, zs = 0.60, 0.46, 0.0
        else:
            st = (t - 0.76) / 0.24
            e = math.pow(max(0.0, 1.0 - st * 0.94), 0.55)
            w, h, zs = max(0.06, 0.60 * e), max(0.04, 0.46 * e), -0.04 * st
        sts.append((y, w, h, zs))
    rings = [tr(*s) for s in sts]
    for idx in range(len(rings) - 1):
        s0, s1 = rings[idx], rings[idx + 1]
        v0, v1 = 1.0 - (half - sts[idx][0]) / L, 1.0 - (half - sts[idx + 1][0]) / L
        for i in range(8):
            ni = (i + 1) % 8
            f = bm.faces.new((s0[i], s0[ni], s1[ni], s1[i]))
            for lp, uvc in zip(f.loops, (((i / 8) * U_BODY_MAX, v0), (((i + 1) / 8) * U_BODY_MAX, v0), (((i + 1) / 8) * U_BODY_MAX, v1), ((i / 8) * U_BODY_MAX, v1))):
                lp[uv].uv = uvc
    bm.faces.new(rings[-1])
    bm.faces.new(list(reversed(rings[0])))
    for side in (-1.0, 1.0):
        box = bmesh.ops.create_cube(bm, size=1.0)
        for v in box["verts"]:
            v.co.x = v.co.x * 0.11 + side * 0.33
            v.co.y = v.co.y * 0.95 - 1.15
            v.co.z = v.co.z * 0.15 - 0.02
    fill_zone_uv(bm, uv, (0.85, 0.30))
    objs.append(make_obj("TAURUS_Airframe", bm, mat))

    for side, sn in ((-1.0, "L"), (1.0, "R")):
        r_le, t_le, t_te, r_te = Vector((0, 0.20, 0)), Vector((side * 1.08, -0.38, 0)), Vector((side * 1.08, -0.64, 0)), Vector((0, -0.20, 0))
        fd = solve_wing_fold_deg((t_le.x, t_le.y), side, target_x_offset=0.08)
        bm_w = bmesh.new()
        uv_w = bm_w.loops.layers.uv.new("UVMap")
        add_airfoil(bm_w, uv_w, r_le, t_le, t_te, r_te, 0.014, 0.006)
        w_obj = make_obj(f"TAURUS_Wing_{sn}", bm_w, mat, location=(side * 0.14, 0.20, 0.225))
        animate_rot_euler(w_obj, f"25_TAURUS_Wing_{sn}", 100, (0, 0, fd), 200, (0, 0, 0))
        objs.append(w_obj)

    for k in range(4):
        rot = Matrix.Rotation(math.radians(45 + k * 90), 3, "Y")
        bm_f = bmesh.new()
        uv_f = bm_f.loops.layers.uv.new("UVMap")
        add_airfoil(bm_f, uv_f, rot @ Vector((0, 0.14, 0)), rot @ Vector((0, -0.08, 0.34)), rot @ Vector((0, -0.28, 0.34)), rot @ Vector((0, -0.22, 0)), 0.010, 0.005)
        pf = rot @ Vector((0, -2.18, 0.24))
        f_obj = make_obj(f"TAURUS_XTail_{k}", bm_f, mat, location=(pf.x, -2.18, pf.z))
        axis = (rot @ Vector((1, 0, 0))).normalized()
        animate_rot_quat(f_obj, f"25_TAURUS_Tail_{k}", 100, Quaternion(axis, math.radians(80.0)), 200, Quaternion((1, 0, 0, 0)))
        objs.append(f_obj)
    return objs


ARSENAL_MODELS = [
    ("ng_kinzhal",       "kinzhal",     (1.8, 7.5, 1.8),  b_kinzhal),
    ("ng_arrw",          "arrw_hyp",    (1.6, 6.6, 1.6),  b_arrw),
    ("ng_rampage_lora",  "kinzhal",     (1.0, 4.8, 1.0),  b_rampage),
    ("ng_exocet_am39",   "exocet",      (1.2, 4.8, 1.2),  b_exocet_am39),
    ("ng_kh35u",         "kh35_uran",   (1.4, 4.0, 1.4),  b_kh35u),
    ("ng_nsm_jsm",       "stealth_dark",(1.5, 4.1, 0.8),  b_nsm_jsm),
    ("ng_kh22_32",       "kh22_32",     (3.2, 11.7, 2.5), b_kh22_32),
    ("ng_zircon",        "arrw_hyp",    (1.3, 8.6, 1.3),  b_zircon),
    ("ng_aargm_er",      "aargm_er",    (0.8, 4.2, 0.8),  b_aargm_er),
    ("ng_kh58ushke",     "kh58_sead",   (1.2, 4.3, 1.2),  b_kh58ushke),
    ("ng_alarm_sead",    "aargm_er",    (1.0, 4.3, 1.0),  b_alarm_sead),
    ("ng_spear_ew",      "glide_bomb",  (1.7, 1.9, 0.6),  b_spear_ew),
    ("ng_gbu57_mop",     "gbu57_mop",   (1.8, 6.3, 1.8),  b_gbu57_mop),
    ("ng_spice_glide",   "spice_eo",    (2.1, 3.7, 1.0),  b_spice_glide),
    ("ng_shahed_136",    "shahed_136",  (2.6, 3.6, 0.7),  b_shahed_136),
    ("ng_harop",         "harop_drone", (3.1, 2.6, 0.8),  b_harop),
    ("ng_stealth_cruise","scalp_new",   (3.1, 5.2, 0.8),  b_scalp_blunt),
    ("ng_jassm_taurus",  "taurus_new",  (2.6, 5.2, 0.9),  b_taurus_new),
]


def add_box_helper(name: str, size_xyz: tuple[float, float, float], special_type: str) -> None:
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0))
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = size_xyz
    bpy.ops.object.transform_apply(scale=True)
    if hasattr(obj, "EDMProps"):
        obj.EDMProps.SPECIAL_TYPE = special_type


def render_grid(items: list[tuple[str, float, float]], out_path: Path, cam_loc: tuple[float, float, float], cam_tgt: tuple[float, float, float]) -> None:
    clear_scene()
    spec_map = {n: (t, fn) for n, t, _, fn in ARSENAL_MODELS}
    themes = sorted({spec_map[n][0] for n, _, _ in items})
    mats = {t: create_preview_material(t) for t in themes}
    bpy.context.scene.frame_set(200)
    for n, x_pos, y_pos in items:
        t, fn = spec_map[n]
        objs = fn(mats[t])
        bpy.context.view_layer.update()
        for o in objs:
            if o.animation_data and o.animation_data.action:
                if o.rotation_mode == "QUATERNION":
                    o.rotation_quaternion = o.rotation_quaternion.copy()
                else:
                    o.rotation_euler = o.rotation_euler.copy()
                o.animation_data_clear()
            o.location.x += x_pos
            o.location.y += y_pos

    bpy.ops.mesh.primitive_plane_add(size=60, location=(0, 0, -1.10))
    floor = bpy.context.active_object
    fm = bpy.data.materials.new("Floor")
    fm.use_nodes = True
    fm.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.045, 0.05, 0.06, 1.0)
    floor.data.materials.append(fm)
    world = bpy.context.scene.world or bpy.data.worlds.new("World")
    bpy.context.scene.world = world
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.025, 0.03, 0.04, 1.0)
    tgt = Vector(cam_tgt)
    for loc, en in (((8.0, 8.0, 9.0), 3200), ((-8.0, 4.0, 6.0), 1600), ((0.0, -9.0, 5.0), 1400)):
        bpy.ops.object.light_add(type="AREA", location=loc)
        l = bpy.context.active_object
        l.data.energy, l.data.size = en, 6.0
        l.rotation_euler = (tgt - l.location).to_track_quat("-Z", "Y").to_euler()
    bpy.ops.object.camera_add(location=cam_loc)
    cam = bpy.context.active_object
    cam.data.lens = 32.0
    cam.rotation_euler = (tgt - cam.location).to_track_quat("-Z", "Y").to_euler()
    bpy.context.scene.camera = cam
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.samples = 40
    sc.cycles.use_denoising = True
    sc.render.resolution_x, sc.render.resolution_y = 1920, 1080
    sc.render.filepath = str(out_path)
    bpy.ops.render.render(write_still=True)
    print(f"[OK] Rendered {out_path}")


def main() -> None:
    addon_utils.enable("io_scene_edm", default_set=True)
    SHAPES_DIR.mkdir(parents=True, exist_ok=True)
    bpy.context.scene.frame_start = 0
    bpy.context.scene.frame_end = 200
    for name, theme, bbox, fn in ARSENAL_MODELS:
        clear_scene()
        mat = create_edm_pbr_material(f"Mat_{name}", theme)
        objs = fn(mat)
        # Rotate +Y-built weapon -90 deg Z so nose points +X Forward in DCS EDM!
        root = bpy.data.objects.new("EDM_XForward", None)
        bpy.context.scene.collection.objects.link(root)
        root.rotation_euler = (0.0, 0.0, -math.pi * 0.5)
        for o in objs:
            if o.parent is None:
                o.parent = root
        bpy.ops.edm.import_matrials()
        xb = (bbox[1], bbox[0], bbox[2])
        add_box_helper("BoundingBox", xb, "BOUNDING_BOX")
        add_box_helper("Collision", (xb[0] * 0.95, xb[1] * 0.6, xb[2] * 0.6), "COLLISION_SHELL")
        bpy.context.scene.frame_set(100)
        out = SHAPES_DIR / f"{name}.edm"
        bpy.ops.edm.export(filepath=str(out))
        print(f"[OK] Exported {name}.edm ({out.stat().st_size} B)")

    render_grid([
        ("ng_kinzhal", -6.0, 0.0), ("ng_arrw", -4.0, 0.0), ("ng_rampage_lora", -2.2, 0.0),
        ("ng_exocet_am39", -0.6, 0.0), ("ng_kh35u", 1.1, 0.0), ("ng_nsm_jsm", 2.8, 0.0),
        ("ng_aargm_er", 4.5, 0.0), ("ng_kh58ushke", 6.1, 0.0), ("ng_alarm_sead", 7.6, 0.0),
        ("ng_kh22_32", 10.6, 0.0),
    ], PREVIEW_BNS, cam_loc=(4.5, 13.0, 8.2), cam_tgt=(2.0, 0.0, 0.0))

    render_grid([
        ("ng_gbu57_mop", -4.8, 0.0), ("ng_spice_glide", -2.6, 0.0), ("ng_spear_ew", -0.8, 0.0),
        ("ng_stealth_cruise", 1.4, 0.0), ("ng_jassm_taurus", 4.0, 0.0),
        ("ng_harop", 7.2, 0.0), ("ng_shahed_136", 10.2, 0.0),
    ], PREVIEW_CDB, cam_loc=(4.5, 11.0, 7.2), cam_tgt=(2.8, 0.0, 0.0))


if __name__ == "__main__":
    main()
