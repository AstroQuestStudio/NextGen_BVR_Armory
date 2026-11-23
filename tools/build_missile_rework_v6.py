"""Blender 5.2 Wave-6 Missile Rework & New Silhouette Expansion (18 High-Detail +X Forward EDM Models).
Fixes DF-17 seam, upgrades all 15 v1/v2 legacy silhouettes to photo-faithful Blender bevels/intakes/ring-tails/folding kits,
and adds brand-new dedicated silhouettes:
  - ng_shahed_238.edm  (Black stealth jet-powered Geran-3 / Shahed-238 delta with dorsal jet hump & EO/IR turret!)
  - ng_prsm_atacms.edm (US PrSM / ATACMS Block IVA stepped tactical ballistic missile)
  - ng_df17_waverider.edm (Seamless sculpted HGV waverider + interstage booster skirt)
  - Plus photo-faithful upgrades to ng_brahmos_intake (recessed annular intake + protruding shock cone!),
    ng_kh31_ramjet, ng_heavy_umpk (FAB-500 ring-tail + bolted inverted wing kit + DrawArg 25!),
    ng_umpb_d30, ng_glide_sdb, ng_aasm_hammer, ng_durandal_runway, ng_loitering_x (Lancet-3 double-X + pusher prop DrawArg 407),
    ng_atgm_quad, ng_guided_rocket, ng_hypersonic, ng_aim120a, ng_aim120cd, ng_asraam_sleek, ng_peregrine.
"""

from __future__ import annotations

import math
import os
from pathlib import Path

import addon_utils
import bmesh
import bpy
from mathutils import Euler, Matrix, Vector

SHAPES_DIR = Path(r"C:\Users\trufa\Saved Games\DCS\Mods\tech\NextGen_BVR_Armory\Shapes")
TEX_DIR = Path(r"C:\Users\trufa\Saved Games\DCS\Mods\tech\NextGen_BVR_Armory\Textures\NextGen_BVR_Armory")
DEMO_BLEND = Path(os.environ["APPDATA"]) / "Blender Foundation" / "Blender" / "5.2" / "scripts" / "addons" / "io_scene_edm" / "Learning_Demo" / "Geomerty+Animation+Collision.blend"
PREVIEW_OUT = Path(r"C:\Users\trufa\.gemini\antigravity\brain\d63eda09-3e0f-4368-acac-466f620a5bd4\preview_rework_v6.png")


def clear_scene() -> None:
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for col in (bpy.data.meshes, bpy.data.materials, bpy.data.actions):
        for item in list(col):
            if item.users == 0:
                col.remove(item)


def load_tex(theme: str):
    a = bpy.data.images.load(str(TEX_DIR / f"ng_{theme}_albedo.png"), check_existing=True)
    n = bpy.data.images.load(str(TEX_DIR / f"ng_{theme}_normal.png"), check_existing=True)
    n.colorspace_settings.name = "Non-Color"
    r = bpy.data.images.load(str(TEX_DIR / f"ng_{theme}_roughmet.png"), check_existing=True)
    r.colorspace_settings.name = "Non-Color"
    return a, n, r


def create_edm_pbr_material(name: str, theme: str) -> bpy.types.Material:
    with bpy.data.libraries.load(str(DEMO_BLEND), link=False) as (_, data_to):
        data_to.materials = ["Txt"]
    mat = data_to.materials[0].copy()
    mat.name = name
    nt = mat.node_tree
    edm_node = next((nd for nd in nt.nodes if nd.bl_idname == "EdmDefaultShaderNodeType"), None)
    a, n, r = load_tex(theme)
    if edm_node:
        for sock, img in (("Base Color", a), ("Color", a), ("Normal", n), ("RoughMet", r), ("Roughness/Metallic", r)):
            if sock in edm_node.inputs:
                t = nt.nodes.new("ShaderNodeTexImage")
                t.image = img
                nt.links.new(t.outputs["Color"], edm_node.inputs[sock])
    return mat


def create_preview_material(theme: str) -> bpy.types.Material:
    mat = bpy.data.materials.new(f"Prev_{theme}")
    mat.use_nodes = True
    nt = mat.node_tree
    bsdf = nt.nodes.get("Principled BSDF")
    a, n, r = load_tex(theme)
    ta = nt.nodes.new("ShaderNodeTexImage"); ta.image = a
    nt.links.new(ta.outputs["Color"], bsdf.inputs["Base Color"])
    tr = nt.nodes.new("ShaderNodeTexImage"); tr.image = r
    sep = nt.nodes.new("ShaderNodeSeparateColor")
    nt.links.new(tr.outputs["Color"], sep.inputs["Color"])
    nt.links.new(sep.outputs["Green"], bsdf.inputs["Roughness"])
    nt.links.new(sep.outputs["Blue"], bsdf.inputs["Metallic"])
    tn = nt.nodes.new("ShaderNodeTexImage"); tn.image = n
    nmap = nt.nodes.new("ShaderNodeNormalMap"); nmap.inputs["Strength"].default_value = 1.0
    nt.links.new(tn.outputs["Color"], nmap.inputs["Color"])
    nt.links.new(nmap.outputs["Normal"], bsdf.inputs["Normal"])
    return mat


def make_obj(name: str, bm: bmesh.types.BMesh, mat: bpy.types.Material, location=(0.0, 0.0, 0.0), parent=None) -> bpy.types.Object:
    mesh = bpy.data.meshes.new(name)
    bm.to_mesh(mesh)
    bm.free()
    obj = bpy.data.objects.new(name, mesh)
    obj.location = location
    bpy.context.scene.collection.objects.link(obj)
    obj.data.materials.clear()
    obj.data.materials.append(mat)
    if parent is not None:
        obj.parent = parent
    return obj


def key_euler(obj: bpy.types.Object, action_name: str, frames: list[tuple[int, tuple[float, float, float]]]) -> None:
    obj.rotation_mode = "XYZ"
    act = bpy.data.actions.new(name=action_name)
    obj.animation_data_create()
    obj.animation_data.action = act
    for fr, rot_rad in frames:
        obj.rotation_euler = rot_rad
        obj.keyframe_insert(data_path="rotation_euler", frame=fr)


def add_revolve(bm: bmesh.types.BMesh, uv, profile_xr: list[tuple[float, float]], segs: int = 32, z_off: float = 0.0, close_front: bool = True, close_back: bool = True) -> list[list]:
    rings = [
        [bm.verts.new((x, r * math.cos(2 * math.pi * i / segs), z_off + r * math.sin(2 * math.pi * i / segs))) for i in range(segs)]
        for x, r in profile_xr
    ]
    xmin, xmax = min(x for x, _ in profile_xr), max(x for x, _ in profile_xr)
    span = max(0.01, xmax - xmin)
    for k in range(len(rings) - 1):
        u0 = 0.04 + 0.90 * ((profile_xr[k][0] - xmin) / span)
        u1 = 0.04 + 0.90 * ((profile_xr[k + 1][0] - xmin) / span)
        r0, r1 = rings[k], rings[k + 1]
        for i in range(segs):
            ni = (i + 1) % segs
            f = bm.faces.new((r0[i], r0[ni], r1[ni], r1[i]))
            f.smooth = True
            va = 0.06 + 0.88 * (i / segs)
            vb = 0.06 + 0.88 * ((i + 1) / segs)
            for lp, uvc in zip(f.loops, ((u0, va), (u0, vb), (u1, vb), (u1, va))):
                lp[uv].uv = uvc
    if close_front:
        bm.faces.new(rings[-1])
    if close_back:
        bm.faces.new(list(reversed(rings[0])))
    return rings


def add_box(bm: bmesh.types.BMesh, uv, center: tuple[float, float, float], size: tuple[float, float, float], rot=(0.0, 0.0, 0.0), bevel: float = 0.0, uv_rect=(0.12, 0.72, 0.12, 0.88)) -> None:
    ret = bmesh.ops.create_cube(bm, size=1.0)
    verts = ret["verts"]
    for v in verts:
        v.co.x *= size[0]
        v.co.y *= size[1]
        v.co.z *= size[2]
    edges = list({e for v in verts for e in v.link_edges})
    if bevel > 0.002 and min(size) > bevel * 2.5:
        bres = bmesh.ops.bevel(bm, geom=edges, offset=bevel, segments=1, affect="EDGES")
        valid = [v for v in ({v for f in bres["faces"] for v in f.verts} | set(verts)) if v.is_valid]
    else:
        valid = [v for v in verts if v.is_valid]
    m = Matrix.Translation(center) @ Euler(rot, "XYZ").to_matrix().to_4x4()
    for v in valid:
        v.co = m @ v.co
    u0, u1, v0, v1 = uv_rect
    coords = [(u0, v0), (u1, v0), (u1, v1), (u0, v1)]
    for f in bm.faces:
        if any(v in valid for v in f.verts) and all(lp[uv].uv.length == 0 for lp in f.loops):
            for i, lp in enumerate(f.loops):
                lp[uv].uv = coords[i % 4]


def add_swept_fin(bm: bmesh.types.BMesh, uv, x_le_root: float, root_c: float, tip_c: float, span: float, sweep_back: float, r_base: float, ang_deg: float, thickness: float = 0.012, uv_rect=(0.74, 0.94, 0.25, 0.85)) -> None:
    """Create a proper thin airfoil trapezoid prism rotated cleanly radially at ang_deg around X."""
    ang = math.radians(ang_deg)
    rot_m = Matrix.Rotation(ang, 3, "X")
    ht = thickness * 0.5
    p_pts = [
        Vector((x_le_root, r_base - 0.004, -ht)),
        Vector((x_le_root - root_c, r_base - 0.004, -ht)),
        Vector((x_le_root - sweep_back - tip_c, r_base + span, -ht * 0.65)),
        Vector((x_le_root - sweep_back, r_base + span, -ht * 0.65)),
        Vector((x_le_root, r_base - 0.004, ht)),
        Vector((x_le_root - root_c, r_base - 0.004, ht)),
        Vector((x_le_root - sweep_back - tip_c, r_base + span, ht * 0.65)),
        Vector((x_le_root - sweep_back, r_base + span, ht * 0.65)),
    ]
    vs = [bm.verts.new(rot_m @ p) for p in p_pts]
    faces = [
        (vs[0], vs[1], vs[2], vs[3]),
        (vs[7], vs[6], vs[5], vs[4]),
        (vs[0], vs[3], vs[7], vs[4]),
        (vs[1], vs[5], vs[6], vs[2]),
        (vs[3], vs[2], vs[6], vs[7]),
        (vs[0], vs[4], vs[5], vs[1]),
    ]
    u0, u1, v0, v1 = uv_rect
    coords = [(u0, v0), (u1, v0), (u1, v1), (u0, v1)]
    for fvs in faces:
        f = bm.faces.new(fvs)
        for i, lp in enumerate(f.loops):
            lp[uv].uv = coords[i % 4]


# =========================================================================
# NEW & ULTRA-FAITHFUL REWORKED HERO MODELS (+X Forward Native!)
# =========================================================================
def m_shahed_238(mat: bpy.types.Material) -> list[bpy.types.Object]:
    """Photo-faithful Shahed-238 / Geran-3 Jet-Powered Stealth Delta (#16, #17, #18 in ref_bank!):
    Stealth cropped delta flying wing, wide S-duct dorsal jet engine hump & open exhaust nozzle, chin EO/IR turret, NO propeller."""
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    # Main blended fuselage chine + jet nacelle hump
    add_revolve(bm, uv, [(-1.68, 0.145), (-1.52, 0.175), (-0.45, 0.185), (0.85, 0.145), (1.42, 0.085), (1.68, 0.015)], 24, z_off=0.05)
    # Recessed black jet exhaust throat cup
    add_revolve(bm, uv, [(-1.72, 0.085), (-1.58, 0.125), (-1.54, 0.145)], 20, z_off=0.05)
    # Top dorsal NACA/flush air-intake ramp hump (#16, #18)
    add_box(bm, uv, (-0.15, 0.0, 0.22), (1.15, 0.22, 0.14), bevel=0.04, uv_rect=(0.74, 0.96, 0.2, 0.8))
    add_box(bm, uv, (0.35, 0.0, 0.26), (0.38, 0.18, 0.09), rot=(0, math.radians(-12), 0), bevel=0.01, uv_rect=(0.82, 0.96, 0.1, 0.4))
    # Chin EO/IR gyro dome ball (#17)
    ret_s = bmesh.ops.create_uvsphere(bm, u_segments=16, v_segments=10, radius=0.095)
    for v in ret_s["verts"]:
        v.co += Vector((1.05, 0.0, -0.05))
    # Cropped delta wings (span 3.0m) with smooth leading-edge sweep (#16, #17, #18)
    for side in (-1.0, 1.0):
        pts = [
            Vector((0.85, side * 0.10, 0.02)), Vector((-1.42, side * 0.12, 0.02)),
            Vector((-1.52, side * 1.48, 0.03)), Vector((-0.88, side * 1.48, 0.03)),
            Vector((0.85, side * 0.10, -0.035)), Vector((-1.42, side * 0.12, -0.035)),
            Vector((-1.52, side * 1.48, -0.015)), Vector((-0.88, side * 1.48, -0.015)),
        ]
        vs = [bm.verts.new(p) for p in pts]
        for fvs in ((vs[0], vs[1], vs[2], vs[3]), (vs[7], vs[6], vs[5], vs[4]), (vs[0], vs[3], vs[7], vs[4]), (vs[3], vs[2], vs[6], vs[7]), (vs[1], vs[5], vs[6], vs[2])):
            f = bm.faces.new(fvs)
            for i, lp in enumerate(f.loops):
                lp[uv].uv = ((0.2, 0.2), (0.7, 0.2), (0.7, 0.8), (0.2, 0.8))[i % 4]
        # Dual upward & downward clipped wingtip vertical endplates (#16, #18)
        add_box(bm, uv, (-1.22, side * 1.48, 0.14), (0.58, 0.018, 0.34), bevel=0.004, uv_rect=(0.74, 0.94, 0.2, 0.8))
    return [make_obj("Shahed238_JetDelta", bm, mat)]


def m_df17_waverider(mat: bpy.types.Material) -> list[bpy.types.Object]:
    """Seamless DF-17 Boost-Glide Waverider HGV: Rocket booster + flared interstage collar + 3-plane wedge HGV glider (no gap!)."""
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    # Heavy solid booster with flared nozzle skirt & smooth adapter transition (x: -4.25 .. 0.35)
    add_revolve(bm, uv, [(-4.25, 0.56), (-3.95, 0.44), (0.05, 0.44), (0.45, 0.38)], 32)
    for ang in (45, 135, 225, 315):
        add_swept_fin(bm, uv, -3.35, 0.72, 0.48, 0.42, 0.22, 0.44, ang, 0.025)
    # Seamless sculpted Waverider HGV forebody overlapping adapter at x = 0.05 .. 4.35
    rings_x = [
        (0.05, 0.40, 0.26, 0.16),
        (1.05, 0.58, 0.22, 0.14),
        (2.25, 0.44, 0.15, 0.10),
        (3.40, 0.22, 0.07, 0.05),
        (4.35, 0.025, 0.015, 0.012),
    ]
    cross = []
    for x, hw, th_up, th_dn in rings_x:
        # 8-vertex waverider faceted chine cross-section
        pts = [
            Vector((x, 0.0, th_up)), Vector((x, hw * 0.48, th_up * 0.65)),
            Vector((x, hw, -0.02)), Vector((x, hw * 0.45, -th_dn)),
            Vector((x, 0.0, -th_dn * 1.15)), Vector((x, -hw * 0.45, -th_dn)),
            Vector((x, -hw, -0.02)), Vector((x, -hw * 0.48, th_up * 0.65)),
        ]
        cross.append([bm.verts.new(p) for p in pts])
    for k in range(len(cross) - 1):
        r0, r1 = cross[k], cross[k + 1]
        u0 = 0.08 + 0.84 * (k / (len(cross) - 1))
        u1 = 0.08 + 0.84 * ((k + 1) / (len(cross) - 1))
        for i in range(8):
            ni = (i + 1) % 8
            f = bm.faces.new((r0[i], r0[ni], r1[ni], r1[i]))
            f.smooth = False
            va = 0.12 + 0.76 * (i / 8.0)
            vb = 0.12 + 0.76 * ((i + 1) / 8.0)
            for lp, c in zip(f.loops, ((u0, va), (u0, vb), (u1, vb), (u1, va))):
                lp[uv].uv = c
    bm.faces.new(cross[-1])
    bm.faces.new(list(reversed(cross[0])))
    # Twin canted tail stabilizing fins on HGV aft deck
    for ang in (-35, 35):
        add_swept_fin(bm, uv, 0.85, 0.65, 0.35, 0.36, 0.25, 0.20, 90 + ang, 0.018)
    return [make_obj("DF17_Waverider_HGV", bm, mat)]


def m_prsm_atacms(mat: bpy.types.Material) -> list[bpy.types.Object]:
    """Precision Strike Missile (PrSM) / ATACMS Block IVA Cylindrical Stepped Tactical Ballistic Missile."""
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    add_revolve(bm, uv, [(-2.00, 0.16), (-1.88, 0.215), (1.15, 0.215), (1.42, 0.175), (2.00, 0.010)], 32)
    for ang in (45, 135, 225, 315):
        add_swept_fin(bm, uv, -1.42, 0.48, 0.28, 0.22, 0.18, 0.215, ang, 0.016)
    return [make_obj("PrSM_ATACMS", bm, mat)]


def m_brahmos_intake(mat: bpy.types.Material) -> list[bpy.types.Object]:
    """Photo-faithful BrahMos / P-800 Oniks (#08, #11, #12):
    Recessed open annular circular intake cowl + sharp protruding shock cone + 4 small mid strakes + 4 tail fins!"""
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    # Hollow annular inlet cowl (outer lip x=3.65, recessed inner duct throat at x=2.85, solid fuselage back to -4.10)
    add_revolve(bm, uv, [
        (-4.10, 0.22), (-3.85, 0.335), (2.95, 0.335), (3.55, 0.295),
        (3.62, 0.255), (3.55, 0.215), (2.75, 0.195),
    ], 32, close_front=False, close_back=True)
    # Iconic sharp central shock cone protruding from inside throat (x=2.75 .. 4.15!)
    add_revolve(bm, uv, [(2.70, 0.195), (3.45, 0.165), (4.15, 0.008)], 28)
    for ang in (45, 135, 225, 315):
        add_swept_fin(bm, uv, 0.55, 0.85, 0.45, 0.36, 0.35, 0.335, ang, 0.022)
        add_swept_fin(bm, uv, -3.10, 0.72, 0.40, 0.38, 0.32, 0.335, ang, 0.022)
    return [make_obj("BrahMos_Supersonic", bm, mat)]


def m_kh31_ramjet(mat: bpy.types.Material) -> list[bpy.types.Object]:
    """Kh-31PM / YJ-12 / ASM-3: Sleek ogive fuselage + 4 side-mounted ramjet inlet nacelles with shock cones + X-fins."""
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    add_revolve(bm, uv, [(-2.35, 0.125), (-2.15, 0.180), (1.75, 0.180), (2.18, 0.095), (2.35, 0.008)], 32)
    for k in range(4):
        ang = math.radians(45 + k * 90)
        dy, dz = math.cos(ang) * 0.205, math.sin(ang) * 0.205
        # Side ramjet duct housing + conical intake plug along X
        rings = [
            [bm.verts.new((x, dy + r * math.cos(2 * math.pi * i / 16), dz + r * math.sin(2 * math.pi * i / 16))) for i in range(16)]
            for x, r in ((-1.15, 0.03), (-0.85, 0.075), (0.85, 0.075), (1.12, 0.055), (1.28, 0.006))
        ]
        for idx in range(len(rings) - 1):
            r0, r1 = rings[idx], rings[idx + 1]
            for i in range(16):
                ni = (i + 1) % 16
                f = bm.faces.new((r0[i], r0[ni], r1[ni], r1[i])); f.smooth = True
                for lp, c in zip(f.loops, ((0.3, 0.2), (0.7, 0.2), (0.7, 0.8), (0.3, 0.8))):
                    lp[uv].uv = c
        bm.faces.new(rings[-1]); bm.faces.new(list(reversed(rings[0])))
        add_swept_fin(bm, uv, -0.25, 0.48, 0.22, 0.22, 0.20, 0.180, 45 + k * 90, 0.012)
        add_swept_fin(bm, uv, -1.78, 0.36, 0.18, 0.24, 0.18, 0.180, 45 + k * 90, 0.012)
    return [make_obj("Kh31_Ramjet", bm, mat)]


def m_heavy_umpk(mat: bpy.types.Material) -> list[bpy.types.Object]:
    """Photo-faithful Russian FAB-500/1500 UMPK (#01, #03, #04, #06 in ref_bank!):
    Bulbous Russian bomb with tail shroud ring + bolted rectangular dorsal/ventral wing-kit spine + swept DrawArg 25 wings + V-tail."""
    objs = []
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    # Bulbous FAB-500 fuselage + stepped fuse nose + cylindrical ring-tail shroud (#03, #06)
    add_revolve(bm, uv, [(-1.24, 0.08), (-1.10, 0.14), (-0.52, 0.20), (0.68, 0.20), (1.06, 0.105), (1.24, 0.012)], 28)
    add_revolve(bm, uv, [(-1.22, 0.19), (-1.04, 0.19), (-1.04, 0.178), (-1.22, 0.178)], 24, close_front=False, close_back=False)
    for ang in (0, 90, 180, 270):
        add_swept_fin(bm, uv, -0.78, 0.42, 0.28, 0.14, 0.06, 0.06, ang, 0.012)
    # Bolted UMPK aluminum spine housing (#01, #04) + twin V-tail stabilizer fins on top
    add_box(bm, uv, (0.04, 0.0, 0.245), (1.88, 0.21, 0.095), bevel=0.018)
    for ang in (38, 142):
        add_swept_fin(bm, uv, -0.75, 0.26, 0.14, 0.34, 0.14, 0.06, ang, 0.010)
    objs.append(make_obj("FAB_UMPK_Body", bm, mat))

    # Swept UMPK Folding Wings (DrawArg 25: frame 100 folded forward under wing-rack, frame 200 deployed outward!)
    for side, sn in ((-1.0, "L"), (1.0, "R")):
        bm_w = bmesh.new(); uv_w = bm_w.loops.layers.uv.new("UVMap")
        pts = [
            Vector((0.20, 0.0, 0.015)), Vector((-0.08, 0.0, 0.015)),
            Vector((-0.44, side * 1.18, 0.012)), Vector((-0.24, side * 1.18, 0.012)),
            Vector((0.20, 0.0, -0.015)), Vector((-0.08, 0.0, -0.015)),
            Vector((-0.44, side * 1.18, -0.012)), Vector((-0.24, side * 1.18, -0.012)),
        ]
        vs = [bm_w.verts.new(p) for p in pts]
        for fvs in ((vs[0], vs[1], vs[2], vs[3]), (vs[7], vs[6], vs[5], vs[4]), (vs[0], vs[3], vs[7], vs[4]), (vs[3], vs[2], vs[6], vs[7]), (vs[1], vs[5], vs[6], vs[2])):
            f = bm_w.faces.new(fvs)
            for i, lp in enumerate(f.loops):
                lp[uv_w].uv = ((0.76, 0.15), (0.96, 0.15), (0.96, 0.85), (0.76, 0.85))[i % 4]
        w_obj = make_obj(f"UMPK_Wing_{sn}", bm_w, mat, location=(0.24, side * 0.06, 0.295))
        key_euler(w_obj, f"25_UMPK_{sn}", [(100, (0, 0, side * math.radians(74.0))), (200, (0, 0, 0))])
        objs.append(w_obj)
    return objs


def m_umpb_d30(mat: bpy.types.Material) -> list[bpy.types.Object]:
    """Russian UMPB D-30SN / JDAM-ER Sleek Smart Glide Bomb with dorsal spine and DrawArg 25 wings."""
    objs = []
    bm = bmesh.new(); uv = bm.loops.layers.uv.new("UVMap")
    add_revolve(bm, uv, [(-1.42, 0.085), (-1.15, 0.150), (1.02, 0.150), (1.36, 0.055), (1.42, 0.008)], 28)
    add_box(bm, uv, (0.0, 0.0, 0.165), (1.92, 0.14, 0.055), bevel=0.012)
    for ang in (45, 135, 225, 315):
        add_swept_fin(bm, uv, -1.06, 0.28, 0.16, 0.18, 0.08, 0.145, ang, 0.010)
    objs.append(make_obj("UMPB_Body", bm, mat))
    for side, sn in ((-1.0, "L"), (1.0, "R")):
        bm_w = bmesh.new(); uv_w = bm_w.loops.layers.uv.new("UVMap")
        add_box(bm_w, uv_w, (-0.12, side * 0.56, 0.0), (0.28, 1.12, 0.022), rot=(0, 0, side * math.radians(-18)), uv_rect=(0.76, 0.96, 0.15, 0.85))
        w = make_obj(f"UMPB_Wing_{sn}", bm_w, mat, location=(0.28, side * 0.05, 0.19))
        key_euler(w, f"25_UMPB_{sn}", [(100, (0, 0, side * math.radians(-78.0))), (200, (0, 0, 0))])
        objs.append(w)
    return objs


def m_glide_sdb(mat: bpy.types.Material) -> list[bpy.types.Object]:
    """GBU-39 / GBU-53/B StormBreaker / GLSDB / SPEAR 3 / Tolun Diamond Stealth Chined SDB (DrawArg 25)."""
    objs = []
    bm = bmesh.new(); uv = bm.loops.layers.uv.new("UVMap")
    add_box(bm, uv, (0.0, 0.0, 0.0), (1.58, 0.19, 0.165), bevel=0.042)
    add_box(bm, uv, (0.84, 0.0, 0.0), (0.38, 0.155, 0.135), rot=(0, 0, 0), bevel=0.045)
    for ang in (45, 135, 225, 315):
        add_swept_fin(bm, uv, -0.62, 0.20, 0.12, 0.12, 0.06, 0.085, ang, 0.010)
    objs.append(make_obj("SDB_StealthBody", bm, mat))
    for side, sn in ((-1.0, "L"), (1.0, "R")):
        bm_w = bmesh.new(); uv_w = bm_w.loops.layers.uv.new("UVMap")
        add_box(bm_w, uv_w, (-0.12, side * 0.42, 0.0), (0.20, 0.84, 0.018), rot=(0, 0, side * math.radians(-18)), uv_rect=(0.76, 0.96, 0.15, 0.85))
        w = make_obj(f"SDB_Wing_{sn}", bm_w, mat, location=(0.22, side * 0.05, 0.092))
        key_euler(w, f"25_SDB_{sn}", [(100, (0, 0, side * math.radians(-76.0))), (200, (0, 0, 0))])
        objs.append(w)
    return objs


def m_aasm_hammer(mat: bpy.types.Material) -> list[bpy.types.Object]:
    """Safran AASM Hammer (#): Mk-82 olive curved bomb + INS/GPS strake nose kit + booster motor & deployed tail kit (DrawArg 25)."""
    objs = []
    bm = bmesh.new(); uv = bm.loops.layers.uv.new("UVMap")
    add_revolve(bm, uv, [(-1.55, 0.088), (-1.38, 0.122), (-0.70, 0.136), (0.92, 0.136), (1.36, 0.070), (1.55, 0.012)], 28)
    for ang in (45, 135, 225, 315):
        add_swept_fin(bm, uv, 1.18, 0.28, 0.14, 0.095, 0.08, 0.095, ang, 0.010)
    objs.append(make_obj("AASM_Body", bm, mat))
    for k, ang in enumerate((45, 135, 225, 315)):
        bm_f = bmesh.new(); uv_f = bm_f.loops.layers.uv.new("UVMap")
        add_swept_fin(bm_f, uv_f, 0.34, 0.38, 0.24, 0.26, 0.18, 0.0, 0.0, 0.012)
        p = Vector((0, math.cos(math.radians(ang)) * 0.122, math.sin(math.radians(ang)) * 0.122))
        fin = make_obj(f"AASM_Tail_{k}", bm_f, mat, location=(-1.32, p.y, p.z))
        key_euler(fin, f"25_AASM_{k}", [(100, (math.radians(ang), 0, 0)), (200, (math.radians(ang), math.radians(-22), 0))])
        objs.append(fin)
    return objs


def m_durandal(mat: bpy.types.Material) -> list[bpy.types.Object]:
    """BLU-107 Durandal Anti-Runway Penetrator + DrawArg 0 Brake-Chute Drogue."""
    objs = []
    bm = bmesh.new(); uv = bm.loops.layers.uv.new("UVMap")
    add_revolve(bm, uv, [(-1.25, 0.088), (-0.82, 0.112), (0.85, 0.112), (1.16, 0.042), (1.25, 0.005)], 28)
    for ang in (45, 135, 225, 315):
        add_swept_fin(bm, uv, -0.82, 0.32, 0.22, 0.11, 0.06, 0.110, ang, 0.010)
    objs.append(make_obj("Durandal_Body", bm, mat))
    bm_c = bmesh.new(); uv_c = bm_c.loops.layers.uv.new("UVMap")
    add_revolve(bm_c, uv_c, [(-2.15, 0.28), (-1.95, 0.30), (-1.45, 0.08), (-1.26, 0.03)], 20)
    ch = make_obj("Durandal_Chute", bm_c, mat)
    act = bpy.data.actions.new("0_Durandal_Chute")
    ch.animation_data_create(); ch.animation_data.action = act
    for fr, sc in ((100, (0.05, 0.05, 0.05)), (200, (1.0, 1.0, 1.0))):
        ch.scale = sc; ch.keyframe_insert("scale", frame=fr)
    objs.append(ch)
    return objs


def m_loitering_x(mat: bpy.types.Material) -> list[bpy.types.Object]:
    """Photo-faithful ZALA Lancet-3M (#00, #01, #05, #06): White/grey fuselage + black optical nose ball + dual staggered X-wings + pusher prop (DrawArg 407)."""
    objs = []
    bm = bmesh.new(); uv = bm.loops.layers.uv.new("UVMap")
    add_revolve(bm, uv, [(-0.82, 0.035), (-0.65, 0.072), (0.62, 0.072), (0.76, 0.048), (0.84, 0.012)], 24)
    for ang in (45, 135, 225, 315):
        add_swept_fin(bm, uv, 0.28, 0.26, 0.15, 0.44, 0.12, 0.070, ang, 0.010)
        add_swept_fin(bm, uv, -0.42, 0.22, 0.13, 0.34, 0.10, 0.068, ang, 0.010)
    objs.append(make_obj("Lancet_Body", bm, mat))
    bm_p = bmesh.new(); uv_p = bm_p.loops.layers.uv.new("UVMap")
    add_box(bm_p, uv_p, (0.0, 0.0, 0.0), (0.016, 0.34, 0.034))
    prop = make_obj("Lancet_Prop", bm_p, mat, location=(-0.84, 0.0, 0.0))
    key_euler(prop, "407_Lancet_Prop", [(100, (0, 0, 0)), (150, (math.pi, 0, 0)), (200, (2 * math.pi, 0, 0))])
    objs.append(prop)
    return objs


def m_atgm_quad(mat: bpy.types.Material) -> list[bpy.types.Object]:
    """AGM-179 JAGM / Brimstone 3 / Spike NLOS / Kornet-EM: Seeker glass nose + 4 full-chord strakes + 4 rear fins."""
    bm = bmesh.new(); uv = bm.loops.layers.uv.new("UVMap")
    add_revolve(bm, uv, [(-0.90, 0.072), (-0.78, 0.089), (0.76, 0.089), (0.88, 0.045), (0.90, 0.012)], 28)
    for ang in (45, 135, 225, 315):
        add_swept_fin(bm, uv, 0.56, 0.85, 0.78, 0.028, 0.04, 0.088, ang, 0.010)
        add_swept_fin(bm, uv, -0.58, 0.26, 0.18, 0.145, 0.06, 0.088, ang, 0.010)
    return [make_obj("ATGM_Quad", bm, mat)]


def m_guided_rocket(mat: bpy.types.Material) -> list[bpy.types.Object]:
    """APKWS II / AGR-20 FALCO / CIRIT 70mm Laser-Guided Rocket with mid WGU-59 seeker ring & 4 slotted canards."""
    bm = bmesh.new(); uv = bm.loops.layers.uv.new("UVMap")
    add_revolve(bm, uv, [(-0.88, 0.032), (-0.76, 0.035), (0.72, 0.035), (0.86, 0.016), (0.88, 0.005)], 24)
    for ang in (45, 135, 225, 315):
        add_swept_fin(bm, uv, 0.44, 0.14, 0.10, 0.052, 0.03, 0.034, ang, 0.006)
        add_swept_fin(bm, uv, -0.70, 0.15, 0.12, 0.068, 0.02, 0.034, ang, 0.006)
    return [make_obj("GuidedRocket", bm, mat)]


def m_hypersonic(mat: bpy.types.Material) -> list[bpy.types.Object]:
    """HALO / Hypersonic Wedge Anti-Ship Missile with biconic sharp nose & swept stabilizing tail fins."""
    bm = bmesh.new(); uv = bm.loops.layers.uv.new("UVMap")
    add_revolve(bm, uv, [(-3.25, 0.185), (-2.95, 0.240), (1.15, 0.240), (2.40, 0.135), (3.25, 0.006)], 32)
    for ang in (45, 135, 225, 315):
        add_swept_fin(bm, uv, -2.35, 0.68, 0.34, 0.26, 0.24, 0.238, ang, 0.016)
    return [make_obj("Hypersonic_Body", bm, mat)]


def m_aim120a(mat: bpy.types.Material) -> list[bpy.types.Object]:
    """AIM-120A AMRAAM: Full-span trapezoidal mid-wings + tail control fins."""
    bm = bmesh.new(); uv = bm.loops.layers.uv.new("UVMap")
    add_revolve(bm, uv, [(-1.83, 0.072), (-1.70, 0.089), (1.35, 0.089), (1.68, 0.044), (1.83, 0.004)], 28)
    for ang in (45, 135, 225, 315):
        add_swept_fin(bm, uv, 0.32, 0.46, 0.22, 0.22, 0.20, 0.088, ang, 0.010)
        add_swept_fin(bm, uv, -1.35, 0.40, 0.22, 0.21, 0.16, 0.088, ang, 0.010)
    return [make_obj("AIM120A", bm, mat)]


def m_aim120cd(mat: bpy.types.Material) -> list[bpy.types.Object]:
    """AIM-120C-5/7/8 / D-3 AMRAAM: Clipped F-22 internal-bay cropped trapezoidal fins."""
    bm = bmesh.new(); uv = bm.loops.layers.uv.new("UVMap")
    add_revolve(bm, uv, [(-1.83, 0.072), (-1.70, 0.089), (1.35, 0.089), (1.68, 0.044), (1.83, 0.004)], 28)
    for ang in (45, 135, 225, 315):
        add_swept_fin(bm, uv, 0.32, 0.38, 0.20, 0.145, 0.15, 0.088, ang, 0.010)
        add_swept_fin(bm, uv, -1.42, 0.34, 0.18, 0.145, 0.14, 0.088, ang, 0.010)
    return [make_obj("AIM120CD", bm, mat)]


def m_asraam_sleek(mat: bpy.types.Material) -> list[bpy.types.Object]:
    """MBDA ASRAAM Block 6 / Matra Magic III Sleek Wingless Tube + 4 Tail Control Fins."""
    bm = bmesh.new(); uv = bm.loops.layers.uv.new("UVMap")
    add_revolve(bm, uv, [(-1.45, 0.068), (-1.35, 0.083), (1.26, 0.083), (1.40, 0.045), (1.45, 0.008)], 28)
    for ang in (45, 135, 225, 315):
        add_swept_fin(bm, uv, -1.10, 0.30, 0.18, 0.15, 0.10, 0.082, ang, 0.010)
    return [make_obj("ASRAAM_Sleek", bm, mat)]


def m_peregrine(mat: bpy.types.Material) -> list[bpy.types.Object]:
    """Raytheon Peregrine Compact Mini-BVR Missile (1.8m): Long low-profile mid strakes + 4 tail fins."""
    bm = bmesh.new(); uv = bm.loops.layers.uv.new("UVMap")
    add_revolve(bm, uv, [(-0.90, 0.048), (-0.82, 0.060), (0.64, 0.060), (0.84, 0.025), (0.90, 0.004)], 24)
    for ang in (45, 135, 225, 315):
        add_swept_fin(bm, uv, 0.30, 0.42, 0.32, 0.065, 0.08, 0.059, ang, 0.008)
        add_swept_fin(bm, uv, -0.62, 0.22, 0.14, 0.115, 0.06, 0.059, ang, 0.008)
    return [make_obj("Peregrine", bm, mat)]


WAVE6_MODELS = [
    ("ng_shahed_238",      "stealth_dark",    (3.5, 3.1, 0.5),  m_shahed_238),
    ("ng_prsm_atacms",     "us_bvr",          (4.1, 0.7, 0.7),  m_prsm_atacms),
    ("ng_df17_waverider",  "df17_tps",        (8.7, 1.3, 1.3),  m_df17_waverider),
    ("ng_brahmos_intake",  "ramjet_heavy",    (8.3, 1.2, 1.2),  m_brahmos_intake),
    ("ng_kh31_ramjet",     "ramjet_heavy",    (4.8, 0.9, 0.9),  m_kh31_ramjet),
    ("ng_heavy_umpk",      "heavy_bomb",      (2.6, 2.5, 0.8),  m_heavy_umpk),
    ("ng_umpb_d30",        "umpb_pab",        (2.9, 2.4, 0.7),  m_umpb_d30),
    ("ng_glide_sdb",       "glide_bomb",      (1.9, 1.8, 0.5),  m_glide_sdb),
    ("ng_aasm_hammer",     "aasm_hammer",     (3.2, 0.8, 0.8),  m_aasm_hammer),
    ("ng_durandal_runway", "durandal_cbu",    (2.6, 0.7, 0.7),  m_durandal),
    ("ng_loitering_x",     "loitering_olive", (1.7, 1.1, 1.1),  m_loitering_x),
    ("ng_atgm_quad",       "helo_atgm",       (1.9, 0.5, 0.5),  m_atgm_quad),
    ("ng_guided_rocket",   "us_bvr",          (1.8, 0.25, 0.25),m_guided_rocket),
    ("ng_hypersonic",      "hypersonic_blk",  (6.6, 0.9, 0.9),  m_hypersonic),
    ("ng_aim120a",         "us_bvr",          (3.7, 0.65, 0.65),m_aim120a),
    ("ng_aim120cd",        "us_bvr",          (3.7, 0.5, 0.5),  m_aim120cd),
    ("ng_asraam_sleek",    "us_bvr",          (3.0, 0.48, 0.48),m_asraam_sleek),
    ("ng_peregrine",       "us_bvr",          (1.9, 0.4, 0.4),  m_peregrine),
]


def add_box_helper(name: str, size_xyz: tuple[float, float, float], special_type: str) -> None:
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0))
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = size_xyz
    bpy.ops.object.transform_apply(scale=True)
    if hasattr(obj, "EDMProps"):
        obj.EDMProps.SPECIAL_TYPE = special_type


def main() -> None:
    addon_utils.enable("io_scene_edm", default_set=True)
    SHAPES_DIR.mkdir(parents=True, exist_ok=True)
    bpy.context.scene.frame_start = 0
    bpy.context.scene.frame_end = 200
    for name, theme, bbox, fn in WAVE6_MODELS:
        clear_scene()
        mat = create_edm_pbr_material(f"Mat_{name}", theme)
        fn(mat)
        bpy.ops.edm.import_matrials()
        add_box_helper("BoundingBox", bbox, "BOUNDING_BOX")
        add_box_helper("Collision", (bbox[0] * 0.9, bbox[1] * 0.7, bbox[2] * 0.7), "COLLISION_SHELL")
        bpy.context.scene.frame_set(100)
        out = SHAPES_DIR / f"{name}.edm"
        bpy.ops.edm.export(filepath=str(out))
        print(f"[OK] Exported {name}.edm ({out.stat().st_size} B)")

    # Quick hero showcase render of top reworked shapes
    clear_scene()
    grid = [
        ("ng_shahed_238",      "stealth_dark",    m_shahed_238,      (-3.5,  3.0)),
        ("ng_prsm_atacms",     "us_bvr",          m_prsm_atacms,     ( 3.0,  3.0)),
        ("ng_df17_waverider",  "df17_tps",        m_df17_waverider,  (-2.5,  0.5)),
        ("ng_brahmos_intake",  "ramjet_heavy",    m_brahmos_intake,  ( 5.0,  0.5)),
        ("ng_heavy_umpk",      "heavy_bomb",      m_heavy_umpk,      (-4.0, -2.5)),
        ("ng_loitering_x",     "loitering_olive", m_loitering_x,     (-0.5, -2.5)),
        ("ng_kh31_ramjet",     "ramjet_heavy",    m_kh31_ramjet,     ( 3.8, -2.5)),
    ]
    mats = {t: create_preview_material(t) for _, t, _, _ in grid}
    bpy.context.scene.frame_set(200)
    for _, theme, fn, (xp, yp) in grid:
        objs = fn(mats[theme])
        bpy.context.view_layer.update()
        for o in objs:
            if o.animation_data and o.animation_data.action:
                o.rotation_euler = o.rotation_euler.copy()
                o.scale = o.scale.copy()
                o.animation_data_clear()
        for o in objs:
            if o.parent is None:
                o.location.x += xp
                o.location.y += yp
                o.location.z += 0.65

    bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 0, 0))
    fl = bpy.context.active_object
    fm = bpy.data.materials.new("Floor"); fm.use_nodes = True
    fm.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.045, 0.05, 0.06, 1.0)
    fl.data.materials.append(fm)
    world = bpy.context.scene.world or bpy.data.worlds.new("World")
    bpy.context.scene.world = world; world.use_nodes = True
    world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.025, 0.03, 0.04, 1.0)
    tgt = Vector((0.5, 0.2, 0.6))
    for loc, en in (((8.0, -10.0, 12.0), 8000), ((-10.0, 6.0, 8.0), 4000)):
        bpy.ops.object.light_add(type="AREA", location=loc)
        l = bpy.context.active_object; l.data.energy = en; l.data.size = 8.0
        l.rotation_euler = (tgt - l.location).to_track_quat("-Z", "Y").to_euler()
    bpy.ops.object.camera_add(location=(6.5, -11.5, 7.2))
    cam = bpy.context.active_object; cam.data.lens = 34.0
    cam.rotation_euler = (tgt - cam.location).to_track_quat("-Z", "Y").to_euler()
    bpy.context.scene.camera = cam
    sc = bpy.context.scene; sc.render.engine = "CYCLES"; sc.cycles.samples = 32; sc.cycles.use_denoising = True
    sc.render.resolution_x, sc.render.resolution_y = 1920, 1080
    sc.render.filepath = str(PREVIEW_OUT)
    bpy.ops.render.render(write_still=True)
    print(f"[OK] Rendered {PREVIEW_OUT}")


if __name__ == "__main__":
    main()
