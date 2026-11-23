"""Blender 5.2 Ground Air Defense (C-RAM, Iron Dome, IRIS-T SLM, SAMP/T, Pantsir-SM, Patriot PAC-3, KEKA Pad),
KEKA Aerospace Troll Rockets, and Priority Backlog Missiles Builder (all natively +X Forward, +Z Up for DCS EDM).
Exports 21 .edm files to C:/Users/trufa/Saved Games/DCS/Mods/tech/NextGen_BVR_Armory/Shapes/
and renders 2 Cycles showcase sheets: preview_sam_cram_v4.png & preview_backlog_keka_v4.png
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
OUT_DIR = Path(r"C:\Users\trufa\.gemini\antigravity\brain\d63eda09-3e0f-4368-acac-466f620a5bd4")
PREVIEW_SAM = OUT_DIR / "preview_sam_cram_v4.png"
PREVIEW_BKL = OUT_DIR / "preview_backlog_keka_v4.png"

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
    nmap.inputs["Strength"].default_value = 1.0
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


def make_empty(name: str, location=(0.0, 0.0, 0.0), rotation_euler=(0.0, 0.0, 0.0), parent=None, special_type: str | None = None) -> bpy.types.Object:
    emp = bpy.data.objects.new(name, None)
    emp.location = location
    emp.rotation_euler = rotation_euler
    bpy.context.scene.collection.objects.link(emp)
    if parent is not None:
        emp.parent = parent
    if special_type and hasattr(emp, "EDMProps"):
        emp.EDMProps.SPECIAL_TYPE = special_type
    return emp


def key_euler(obj: bpy.types.Object, action_name: str, keyframes: list[tuple[int, tuple[float, float, float]]]) -> None:
    obj.rotation_mode = "XYZ"
    act = bpy.data.actions.new(name=action_name)
    obj.animation_data_create()
    obj.animation_data.action = act
    for fr, rot_rad in keyframes:
        obj.rotation_euler = rot_rad
        obj.keyframe_insert(data_path="rotation_euler", frame=fr)


def add_turret_azimuth(emp: bpy.types.Object, action_name: str) -> None:
    key_euler(emp, action_name, [
        (0, (0.0, 0.0, -math.pi)),
        (50, (0.0, 0.0, -math.pi * 0.5)),
        (100, (0.0, 0.0, 0.0)),
        (150, (0.0, 0.0, math.pi * 0.5)),
        (200, (0.0, 0.0, math.pi)),
    ])


def add_gun_elevation(emp: bpy.types.Object, action_name: str, min_deg: float = -15.0, max_deg: float = 85.0) -> None:
    # In DCS Learning_Demo: frame 0 -> +pi/2 (down), frame 100 -> 0 (level +X), frame 200 -> -pi/2 (up +Z)
    key_euler(emp, action_name, [
        (0, (0.0, math.radians(-min_deg), 0.0)),
        (100, (0.0, 0.0, 0.0)),
        (200, (0.0, math.radians(-max_deg), 0.0)),
    ])


def add_box(bm: bmesh.types.BMesh, uv, center: tuple[float, float, float], size: tuple[float, float, float], uv_c: tuple[float, float] = (0.35, 0.52), rot_euler=(0.0, 0.0, 0.0)) -> None:
    ret = bmesh.ops.create_cube(bm, size=1.0)
    m = Matrix.Translation(center) @ Euler(rot_euler, "XYZ").to_matrix().to_4x4() @ Matrix.Diagonal((size[0], size[1], size[2], 1.0))
    for v in ret["verts"]:
        v.co = m @ v.co
    for f in bm.faces:
        for lp in f.loops:
            if lp[uv].uv.length == 0:
                lp[uv].uv = uv_c


def add_cyl_x(bm: bmesh.types.BMesh, uv, x0: float, x1: float, y: float, z: float, radius: float, segs: int = 20, uv_c: tuple[float, float] = (0.85, 0.30)) -> None:
    r0 = [bm.verts.new((x0, y + radius * math.cos(2 * math.pi * i / segs), z + radius * math.sin(2 * math.pi * i / segs))) for i in range(segs)]
    r1 = [bm.verts.new((x1, y + radius * math.cos(2 * math.pi * i / segs), z + radius * math.sin(2 * math.pi * i / segs))) for i in range(segs)]
    for i in range(segs):
        ni = (i + 1) % segs
        f = bm.faces.new((r0[i], r0[ni], r1[ni], r1[i]))
        f.smooth = True
        for lp in f.loops:
            lp[uv].uv = uv_c
    for f in (bm.faces.new(list(reversed(r0))), bm.faces.new(r1)):
        for lp in f.loops:
            lp[uv].uv = uv_c


def add_cyl_z(bm: bmesh.types.BMesh, uv, x: float, y: float, z0: float, z1: float, radius: float, segs: int = 24, uv_c: tuple[float, float] = (0.35, 0.50)) -> None:
    r0 = [bm.verts.new((x + radius * math.cos(2 * math.pi * i / segs), y + radius * math.sin(2 * math.pi * i / segs), z0)) for i in range(segs)]
    r1 = [bm.verts.new((x + radius * math.cos(2 * math.pi * i / segs), y + radius * math.sin(2 * math.pi * i / segs), z1)) for i in range(segs)]
    for i in range(segs):
        ni = (i + 1) % segs
        f = bm.faces.new((r0[i], r0[ni], r1[ni], r1[i]))
        f.smooth = True
        for lp in f.loops:
            lp[uv].uv = uv_c
    for f in (bm.faces.new(list(reversed(r0))), bm.faces.new(r1)):
        for lp in f.loops:
            lp[uv].uv = uv_c


def add_wheel(bm: bmesh.types.BMesh, uv, x: float, y: float, z_hub: float, radius: float = 0.55, width: float = 0.34) -> None:
    # Wheel axis along Y (left/right)
    r0 = [bm.verts.new((x + radius * math.cos(2 * math.pi * i / 20), y - width * 0.5, z_hub + radius * math.sin(2 * math.pi * i / 20))) for i in range(20)]
    r1 = [bm.verts.new((x + radius * math.cos(2 * math.pi * i / 20), y + width * 0.5, z_hub + radius * math.sin(2 * math.pi * i / 20))) for i in range(20)]
    for i in range(20):
        ni = (i + 1) % 20
        f = bm.faces.new((r0[i], r0[ni], r1[ni], r1[i]))
        f.smooth = True
        for lp in f.loops:
            lp[uv].uv = (0.85, 0.90)  # Dark rubber/tarmac zone
    for f in (bm.faces.new(list(reversed(r0))), bm.faces.new(r1)):
        for lp in f.loops:
            lp[uv].uv = (0.85, 0.65)


def add_truck_chassis_8x8(bm: bmesh.types.BMesh, uv, length: float = 8.4, width: float = 2.45, cab_h: float = 2.85) -> None:
    # Armored forward cab + frame rails + 4 pairs of heavy 8x8 wheels (+X Forward, +Z Up)
    add_box(bm, uv, (0.0, 0.0, 1.05), (length, width * 0.86, 0.42), (0.35, 0.35))
    add_box(bm, uv, (length * 0.34, 0.0, 1.92), (2.20, width * 0.94, cab_h - 1.15), (0.35, 0.55))
    # Windshield visor
    add_box(bm, uv, (length * 0.34 + 1.11, 0.0, 2.22), (0.05, width * 0.80, 0.52), (0.85, 0.90))
    # 4 Outrigger stabilizer jacks
    for sx in (-length * 0.42, -0.3):
        for sy in (-width * 0.62, width * 0.62):
            add_box(bm, uv, (sx, sy, 0.45), (0.30, 0.30, 0.90), (0.85, 0.65))
    for wx in (length * 0.36, length * 0.14, -length * 0.22, -length * 0.40):
        for wy in (-width * 0.46, width * 0.46):
            add_wheel(bm, uv, wx, wy, 0.55, 0.55, 0.34)


def fill_uv(bm: bmesh.types.BMesh, uv, uvc=(0.35, 0.50)) -> None:
    for f in bm.faces:
        for lp in f.loops:
            if lp[uv].uv.length == 0:
                lp[uv].uv = uvc


# =========================================================================
# MISSILE +X PRIMITIVES (Natively +X Forward!)
# =========================================================================
def build_missile_body_x(name: str, length: float, diam: float, nose_len: float, nose_style: str, mat: bpy.types.Material, segs: int = 32, boat: float = 0.84, parent=None) -> bpy.types.Object:
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    r = diam * 0.5
    half = length * 0.5
    nb = half - nose_len
    prof = [(-half + 0.02, 0.004), (-half, r * boat), (-half + length * 0.04, r), (nb, r)]
    if nose_style == "dome":
        steps = 10
        for i in range(1, steps + 1):
            ang = (i / steps) * (math.pi * 0.5)
            prof.append((nb + math.sin(ang) * nose_len, max(0.004, r * math.cos(ang))))
    else:
        steps = 14
        pw = 0.56 if nose_style == "blunt" else 0.78
        for i in range(1, steps + 1):
            t = i / steps
            prof.append((nb + t * nose_len, max(0.004, r * math.pow(max(0.0, 1.0 - t * 0.96), pw))))
    rings = []
    for x, rad in prof:
        rings.append([bm.verts.new((x, rad * math.cos(2 * math.pi * i / segs), rad * math.sin(2 * math.pi * i / segs))) for i in range(segs)])
    for idx in range(len(rings) - 1):
        x0, x1 = prof[idx][0], prof[idx + 1][0]
        v0 = 1.0 - max(0.0, min(1.0, (half - x0) / length))
        v1 = 1.0 - max(0.0, min(1.0, (half - x1) / length))
        r0, r1 = rings[idx], rings[idx + 1]
        for i in range(segs):
            ni = (i + 1) % segs
            f = bm.faces.new((r0[i], r0[ni], r1[ni], r1[i]))
            f.smooth = True
            for lp, uvc in zip(f.loops, (((i / segs) * U_BODY_MAX, v0), (((i + 1) / segs) * U_BODY_MAX, v0), (((i + 1) / segs) * U_BODY_MAX, v1), ((i / segs) * U_BODY_MAX, v1))):
                lp[uv].uv = uvc
    bm.faces.new(rings[-1]).smooth = True
    bm.faces.new(list(reversed(rings[0])))
    return make_obj(name, bm, mat, parent=parent)


def add_fin_x(bm: bmesh.types.BMesh, uv, rot: Matrix, x_r_le: float, x_r_te: float, x_t_le: float, x_t_te: float, z0: float, z1: float, thick: float = 0.011, uv_c=(0.86, 0.25)) -> None:
    # Root & tip in X-Z plane rotated around X
    p_r_le = rot @ Vector((x_r_le, 0.0, z0))
    p_r_te = rot @ Vector((x_r_te, 0.0, z0))
    p_t_le = rot @ Vector((x_t_le, 0.0, z1))
    p_t_te = rot @ Vector((x_t_te, 0.0, z1))
    n = rot @ Vector((0.0, 1.0, 0.0))
    vr = [bm.verts.new(p_r_le), bm.verts.new(p_r_le.lerp(p_r_te, 0.35) + n * (thick * 0.5)), bm.verts.new(p_r_te), bm.verts.new(p_r_le.lerp(p_r_te, 0.35) - n * (thick * 0.5))]
    vt = [bm.verts.new(p_t_le), bm.verts.new(p_t_le.lerp(p_t_te, 0.35) + n * (thick * 0.28)), bm.verts.new(p_t_te), bm.verts.new(p_t_le.lerp(p_t_te, 0.35) - n * (thick * 0.28))]
    for i in range(4):
        ni = (i + 1) % 4
        f = bm.faces.new((vr[i], vr[ni], vt[ni], vt[i]))
        for lp in f.loops:
            lp[uv].uv = uv_c
    for f in (bm.faces.new(list(reversed(vr))), bm.faces.new(vt)):
        for lp in f.loops:
            lp[uv].uv = uv_c


# =========================================================================
# PART 1: GROUND AIR DEFENSES & LAUNCHERS (Natively +X Forward, +Z Up)
# =========================================================================
def g_cram_centurion(mat: bpy.types.Material) -> list[bpy.types.Object]:
    objs = []
    # Trailer + Diesel Generator + Outriggers
    bm_hull = bmesh.new()
    uv_h = bm_hull.loops.layers.uv.new("UVMap")
    add_box(bm_hull, uv_h, (0.0, 0.0, 0.85), (5.8, 2.35, 0.45), (0.35, 0.35))
    add_box(bm_hull, uv_h, (-1.85, 0.0, 1.48), (1.75, 1.90, 0.90), (0.35, 0.50))
    for wx in (-2.05, -0.95):
        for wy in (-1.12, 1.12):
            add_wheel(bm_hull, uv_h, wx, wy, 0.48, 0.48, 0.28)
    for sx in (-2.5, 2.5):
        for sy in (-1.45, 1.45):
            add_box(bm_hull, uv_h, (sx, sy, 0.45), (0.26, 0.26, 0.90), (0.85, 0.65))
    objs.append(make_obj("CRAM_Trailer", bm_hull, mat))

    # Turret Azimuth Empty (Arg 0) + Center Connector
    emp_az = make_empty("Empty_CRAM_Az", (1.15, 0.0, 1.12))
    add_turret_azimuth(emp_az, "0_CRAM_Az")
    objs.append(emp_az)
    objs.append(make_empty("CENTER_TOWER", (1.15, 0.0, 1.12), special_type="CONNECTOR"))

    # U-Barbette Base
    bm_bar = bmesh.new()
    uv_b = bm_bar.loops.layers.uv.new("UVMap")
    add_cyl_z(bm_bar, uv_b, 0.0, 0.0, 0.0, 0.35, 0.82, 24, (0.35, 0.40))
    add_box(bm_bar, uv_b, (0.0, -0.62, 0.82), (0.78, 0.28, 1.12), (0.35, 0.50))
    add_box(bm_bar, uv_b, (0.0, 0.62, 0.82), (0.78, 0.28, 1.12), (0.35, 0.50))
    add_box(bm_bar, uv_b, (-0.42, 0.0, 0.72), (0.45, 1.15, 0.95), (0.35, 0.55))
    objs.append(make_obj("CRAM_Barbette", bm_bar, mat, parent=emp_az))

    # Elevating Cradle (Arg 1) with iconic R2-D2 Ku-Band White Radome + FLIR
    emp_el = make_empty("Empty_CRAM_El", (0.0, 0.0, 1.12), parent=emp_az)
    add_gun_elevation(emp_el, "1_CRAM_El", -15.0, 85.0)
    objs.append(emp_el)

    bm_cr = bmesh.new()
    uv_c = bm_cr.loops.layers.uv.new("UVMap")
    # Receiver drum
    add_box(bm_cr, uv_c, (0.15, 0.0, 0.0), (0.95, 0.76, 0.62), (0.35, 0.50))
    # Iconic tall white R2-D2 radome cylinder + hemisphere cap
    add_cyl_z(bm_cr, uv_c, 0.05, 0.0, 0.32, 1.48, 0.44, 24, (0.35, 0.88))
    ret_d = bmesh.ops.create_uvsphere(bm_cr, u_segments=24, v_segments=12, radius=0.44)
    for v in ret_d["verts"]:
        v.co += Vector((0.05, 0.0, 1.48))
    for f in bm_cr.faces:
        if all(v.co.z > 1.44 for v in f.verts):
            f.smooth = True
            for lp in f.loops:
                lp[uv_c].uv = (0.35, 0.88)
    # Forward FLIR pod
    add_box(bm_cr, uv_c, (0.55, 0.44, 0.20), (0.48, 0.30, 0.34), (0.85, 0.90))
    objs.append(make_obj("CRAM_RadomeCradle", bm_cr, mat, parent=emp_el))

    # Spinning 6-barrel 20mm M61A1 Vulcan cluster (Arg 23)
    emp_spin = make_empty("Empty_CRAM_Barrels", (0.62, 0.0, -0.04), parent=emp_el)
    key_euler(emp_spin, "23_CRAM_Spin", [(100, (0.0, 0.0, 0.0)), (150, (math.pi, 0.0, 0.0)), (200, (2 * math.pi, 0.0, 0.0))])
    objs.append(emp_spin)

    bm_gn = bmesh.new()
    uv_g = bm_gn.loops.layers.uv.new("UVMap")
    for k in range(6):
        ang = k * (math.pi / 3.0)
        add_cyl_x(bm_gn, uv_g, 0.0, 1.85, 0.055 * math.cos(ang), 0.055 * math.sin(ang), 0.016, 10, (0.85, 0.65))
    for cx in (0.45, 1.25, 1.72):
        add_cyl_x(bm_gn, uv_g, cx, cx + 0.07, 0.0, 0.0, 0.088, 18, (0.85, 0.65))
    objs.append(make_obj("CRAM_VulcanBarrels", bm_gn, mat, parent=emp_spin))

    objs.append(make_empty("POINT_GUN_01", (2.52, 0.0, -0.04), parent=emp_el, special_type="CONNECTOR"))
    objs.append(make_empty("POINT_SIGHT_01", (0.82, 0.44, 0.20), parent=emp_el, special_type="CONNECTOR"))
    return objs


def g_iron_dome_ln(mat: bpy.types.Material) -> list[bpy.types.Object]:
    objs = []
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    # Heavy flat skid platform + 4 leveled jacks + electronics box
    add_box(bm, uv, (0.0, 0.0, 0.45), (4.60, 2.50, 0.36), (0.35, 0.45))
    add_box(bm, uv, (-1.45, 0.0, 1.15), (1.10, 1.95, 1.10), (0.35, 0.55))
    for sx in (-2.1, 2.1):
        for sy in (-1.3, 1.3):
            add_box(bm, uv, (sx, sy, 0.28), (0.28, 0.28, 0.56), (0.85, 0.65))
    objs.append(make_obj("IDome_Base", bm, mat))

    emp_az = make_empty("Empty_IDome_Az", (0.55, 0.0, 0.65))
    add_turret_azimuth(emp_az, "0_IDome_Az")
    objs.append(emp_az)
    objs.append(make_empty("CENTER_TOWER", (0.55, 0.0, 0.65), special_type="CONNECTOR"))

    # Tilted 20-cell (5 cols x 4 rows) canister pod elevated 55 deg
    emp_el = make_empty("Empty_IDome_Rack", (0.0, 0.0, 1.35), rotation_euler=(0.0, math.radians(-55.0), 0.0), parent=emp_az)
    objs.append(emp_el)

    bm_pod = bmesh.new()
    uv_p = bm_pod.loops.layers.uv.new("UVMap")
    add_box(bm_pod, uv_p, (0.0, 0.0, 0.0), (1.95, 2.26, 1.82), (0.35, 0.50))
    # 20 beveled launch canister tubes visibly protruding front & rear of collar cradle!
    idx = 0
    for row in range(4):
        for col in range(5):
            idx += 1
            yy = (col - 2) * 0.41
            zz = (row - 1.5) * 0.40
            add_cyl_x(bm_pod, uv_p, -1.62, 1.72, yy, zz, 0.145, 16, (0.35, 0.85))
            objs.append(make_empty(f"POINT_MISSILE_{idx:02d}", (1.76, yy, zz), parent=emp_el, special_type="CONNECTOR"))
    objs.append(make_obj("IDome_20CellPod", bm_pod, mat, parent=emp_el))
    objs.append(make_empty("POINT_SIGHT_01", (1.60, 0.0, 0.95), parent=emp_el, special_type="CONNECTOR"))
    return objs


def g_iron_dome_radar(mat: bpy.types.Material) -> list[bpy.types.Object]:
    objs = []
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    add_box(bm, uv, (0.0, 0.0, 1.05), (6.8, 2.40, 0.45), (0.35, 0.40))
    add_box(bm, uv, (2.3, 0.0, 1.90), (2.0, 2.30, 1.50), (0.35, 0.50))
    add_box(bm, uv, (-2.0, 0.0, 1.85), (2.0, 2.10, 1.35), (0.35, 0.55))
    for wx in (2.3, -1.0, -2.4):
        for wy in (-1.15, 1.15):
            add_wheel(bm, uv, wx, wy, 0.55, 0.55, 0.34)
    objs.append(make_obj("MMR_Chassis", bm, mat))

    emp_rot = make_empty("Empty_MMR_Rot", (-0.10, 0.0, 2.55))
    key_euler(emp_rot, "11_MMR_Rot", [(100, (0, 0, 0)), (150, (0, 0, math.pi)), (200, (0, 0, 2 * math.pi))])
    objs.append(emp_rot)

    bm_ant = bmesh.new()
    uv_a = bm_ant.loops.layers.uv.new("UVMap")
    add_cyl_z(bm_ant, uv_a, 0.0, 0.0, -1.25, 0.10, 0.48, 18, (0.85, 0.65))
    # Tilted flat S-band AESA array panel
    add_box(bm_ant, uv_a, (0.15, 0.0, 1.05), (0.45, 2.65, 2.25), (0.35, 0.85), rot_euler=(0.0, math.radians(-18.0), 0.0))
    objs.append(make_obj("MMR_AESAPanel", bm_ant, mat, parent=emp_rot))
    return objs


def g_vertical_sam_8cell(mat: bpy.types.Material, truck_name: str, tube_r: float = 0.24, tube_h: float = 4.6) -> list[bpy.types.Object]:
    objs = []
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    add_truck_chassis_8x8(bm, uv, 8.6, 2.48, 2.90)
    add_box(bm, uv, (-0.3, 0.0, 1.65), (3.4, 2.15, 0.85), (0.35, 0.45))
    objs.append(make_obj(f"{truck_name}_Truck", bm, mat))

    emp_tur = make_empty(f"Empty_{truck_name}_Pod", (-2.15, 0.0, 1.30))
    objs.append(emp_tur)
    objs.append(make_empty("CENTER_TOWER", (-2.15, 0.0, 1.30), special_type="CONNECTOR"))

    bm_p = bmesh.new()
    uv_p = bm_p.loops.layers.uv.new("UVMap")
    add_box(bm_p, uv_p, (0.0, 0.0, 0.90), (1.35, 2.35, 1.80), (0.35, 0.50))
    # 8 upright circular launch canisters (2x4 grid) pointed straight up (+Z -> -90 deg pitch in local Y)
    idx = 0
    for c in range(2):
        for r in range(4):
            idx += 1
            xx = (c - 0.5) * (tube_r * 2.45)
            yy = (r - 1.5) * (tube_r * 2.45)
            add_cyl_z(bm_p, uv_p, xx, yy, 0.15, 0.15 + tube_h, tube_r, 18, (0.35, 0.86))
            objs.append(make_empty(f"POINT_MISSILE_{idx:02d}", (xx, yy, 0.15 + tube_h), rotation_euler=(0.0, math.radians(-90.0), 0.0), parent=emp_tur, special_type="CONNECTOR"))
    objs.append(make_obj(f"{truck_name}_8Canisters", bm_p, mat, parent=emp_tur))
    objs.append(make_empty("POINT_SIGHT_01", (1.2, 0.0, 3.10), special_type="CONNECTOR"))
    return objs


def g_pantsir_sm(mat: bpy.types.Material) -> list[bpy.types.Object]:
    objs = []
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    add_truck_chassis_8x8(bm, uv, 9.2, 2.55, 2.95)
    add_box(bm, uv, (-0.8, 0.0, 1.85), (4.8, 2.35, 1.15), (0.35, 0.45))
    objs.append(make_obj("Pantsir_Chassis", bm, mat))

    emp_az = make_empty("Empty_Pantsir_Az", (-1.4, 0.0, 2.45))
    add_turret_azimuth(emp_az, "0_Pantsir_Az")
    objs.append(emp_az)
    objs.append(make_empty("CENTER_TOWER", (-1.4, 0.0, 2.45), special_type="CONNECTOR"))

    bm_t = bmesh.new()
    uv_t = bm_t.loops.layers.uv.new("UVMap")
    add_box(bm_t, uv_t, (0.0, 0.0, 0.65), (2.25, 1.75, 1.30), (0.35, 0.50))
    # Front track radar dish
    add_box(bm_t, uv_t, (1.18, 0.0, 0.82), (0.28, 0.98, 0.72), (0.35, 0.85))
    objs.append(make_obj("Pantsir_Turret", bm_t, mat, parent=emp_az))

    # Top Janus rotating search radar (Arg 11)
    emp_sr = make_empty("Empty_Pantsir_SR", (-0.55, 0.0, 1.55), parent=emp_az)
    key_euler(emp_sr, "11_Pantsir_SR", [(100, (0, 0, 0)), (150, (0, 0, math.pi)), (200, (0, 0, 2 * math.pi))])
    objs.append(emp_sr)
    bm_sr = bmesh.new()
    uv_sr = bm_sr.loops.layers.uv.new("UVMap")
    add_cyl_z(bm_sr, uv_sr, 0.0, 0.0, -0.30, 0.25, 0.25, 14, (0.85, 0.65))
    add_box(bm_sr, uv_sr, (0.0, 0.0, 0.58), (0.36, 1.95, 0.82), (0.35, 0.86))
    objs.append(make_obj("Pantsir_JanusRadar", bm_sr, mat, parent=emp_sr))

    # Elevating Twin Arms (Arg 1): 12 missile tubes + Twin 30mm 2A38M guns
    emp_el = make_empty("Empty_Pantsir_El", (0.15, 0.0, 0.75), parent=emp_az)
    add_gun_elevation(emp_el, "1_Pantsir_El", -5.0, 82.0)
    objs.append(emp_el)

    bm_arms = bmesh.new()
    uv_ar = bm_arms.loops.layers.uv.new("UVMap")
    idx = 0
    for side_y in (-1.22, 1.22):
        # 2x3 stack of 57E6M tubes per side
        for r in range(3):
            for c in range(2):
                idx += 1
                yy = side_y + (c - 0.5) * 0.26 * (1 if side_y > 0 else -1)
                zz = (r - 1.0) * 0.28 + 0.28
                add_cyl_x(bm_arms, uv_ar, -1.65, 1.72, yy, zz, 0.11, 14, (0.35, 0.85))
                objs.append(make_empty(f"POINT_MISSILE_{idx:02d}", (1.75, yy, zz), parent=emp_el, special_type="CONNECTOR"))
        # 30mm dual cannon inboard
        gun_y = side_y * 0.72
        add_cyl_x(bm_arms, uv_ar, 0.0, 2.25, gun_y, -0.05, 0.032, 12, (0.85, 0.65))
    objs.append(make_obj("Pantsir_PodsAndGuns", bm_arms, mat, parent=emp_el))
    objs.append(make_empty("POINT_GUN_01", (2.30, -0.88, -0.05), parent=emp_el, special_type="CONNECTOR"))
    objs.append(make_empty("POINT_GUN_02", (2.30, 0.88, -0.05), parent=emp_el, special_type="CONNECTOR"))
    objs.append(make_empty("POINT_SIGHT_01", (1.35, 0.0, 0.82), parent=emp_az, special_type="CONNECTOR"))
    return objs


def g_patriot_pac3_ln(mat: bpy.types.Material) -> list[bpy.types.Object]:
    objs = []
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    add_box(bm, uv, (0.0, 0.0, 0.80), (6.4, 2.50, 0.42), (0.35, 0.40))
    add_box(bm, uv, (2.1, 0.0, 1.45), (1.4, 1.85, 1.00), (0.35, 0.55))
    for wx in (-1.6, -2.65):
        for wy in (-1.15, 1.15):
            add_wheel(bm, uv, wx, wy, 0.50, 0.50, 0.30)
    objs.append(make_obj("Patriot_Trailer", bm, mat))

    emp_az = make_empty("Empty_Pat_Az", (-1.1, 0.0, 1.05))
    add_turret_azimuth(emp_az, "0_Pat_Az")
    objs.append(emp_az)
    objs.append(make_empty("CENTER_TOWER", (-1.1, 0.0, 1.05), special_type="CONNECTOR"))

    emp_el = make_empty("Empty_Pat_Pod", (-0.35, 0.0, 2.15), rotation_euler=(0.0, math.radians(-38.0), 0.0), parent=emp_az)
    objs.append(emp_el)
    bm_p = bmesh.new()
    uv_p = bm_p.loops.layers.uv.new("UVMap")
    # 4 rectangular quad-pack canister blocks (2x2 -> 16 PAC-3 MSE cells!)
    for c in range(2):
        for r in range(2):
            add_box(bm_p, uv_p, (0.0, (c - 0.5) * 1.15, (r - 0.5) * 0.98), (5.20, 0.98, 0.82), (0.35, 0.52))
    idx = 0
    for c in range(4):
        for r in range(4):
            idx += 1
            yy = (c - 1.5) * 0.54
            zz = (r - 1.5) * 0.45
            objs.append(make_empty(f"POINT_MISSILE_{idx:02d}", (2.65, yy, zz), parent=emp_el, special_type="CONNECTOR"))
    objs.append(make_obj("Patriot_QuadPackPod", bm_p, mat, parent=emp_el))
    return objs


def g_keka_launcher(mat: bpy.types.Material) -> list[bpy.types.Object]:
    """KEKA Aerospace Savanna Trailer Launch Rail ("Troposphere Pad")!"""
    objs = []
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    # Rugged welded square-tube trailer + 2 offroad wheels + car-battery ignition crate
    add_box(bm, uv, (0.0, 0.0, 0.55), (3.8, 1.85, 0.16), (0.85, 0.65))
    add_box(bm, uv, (-0.95, 0.55, 0.85), (0.65, 0.48, 0.44), (0.35, 0.25))  # Ignition box
    for wy in (-0.98, 0.98):
        add_wheel(bm, uv, -0.45, wy, 0.42, 0.42, 0.24)
    objs.append(make_obj("KEKA_Trailer", bm, mat))

    emp_az = make_empty("Empty_KEKA_Az", (0.10, 0.0, 0.65))
    add_turret_azimuth(emp_az, "0_KEKA_Az")
    objs.append(emp_az)
    objs.append(make_empty("CENTER_TOWER", (0.10, 0.0, 0.65), special_type="CONNECTOR"))

    emp_el = make_empty("Empty_KEKA_Rail", (0.0, 0.0, 0.90), rotation_euler=(0.0, math.radians(-58.0), 0.0), parent=emp_az)
    objs.append(emp_el)
    bm_r = bmesh.new()
    uv_r = bm_r.loops.layers.uv.new("UVMap")
    # Welded I-beam rail + blast plate + cross-braces
    add_box(bm_r, uv_r, (0.2, 0.0, 0.0), (4.60, 0.26, 0.18), (0.35, 0.85))
    add_box(bm_r, uv_r, (-2.15, 0.0, 0.22), (0.08, 0.72, 0.65), (0.85, 0.65))
    objs.append(make_obj("KEKA_LaunchRail", bm_r, mat, parent=emp_el))
    objs.append(make_empty("POINT_MISSILE_01", (1.60, 0.0, 0.34), parent=emp_el, special_type="CONNECTOR"))
    objs.append(make_empty("POINT_SIGHT_01", (1.20, 0.0, 0.90), parent=emp_el, special_type="CONNECTOR"))
    return objs


# =========================================================================
# PART 2: SAM INTERCEPTORS + KEKA TROLL + BACKLOG MISSILES (All +X Forward!)
# =========================================================================
def m_sam_tamir(mat: bpy.types.Material) -> list[bpy.types.Object]:
    objs = [build_missile_body_x("Tamir_Body", 3.00, 0.160, 0.42, "ogive", mat, boat=0.86)]
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    for k in range(4):
        rot = Matrix.Rotation(math.radians(45 + k * 90), 3, "X")
        add_fin_x(bm, uv, rot, 0.82, 0.60, 0.66, 0.60, 0.078, 0.175, 0.008)
        add_fin_x(bm, uv, rot, -1.08, -1.42, -1.26, -1.44, 0.075, 0.215, 0.009)
    objs.append(make_obj("Tamir_Fins", bm, mat))
    return objs


def m_sam_irist_slm(mat: bpy.types.Material) -> list[bpy.types.Object]:
    objs = [build_missile_body_x("IRIST_SLM_Body", 4.00, 0.152, 0.30, "dome", mat, boat=0.90)]
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    for k in range(4):
        rot = Matrix.Rotation(math.radians(45 + k * 90), 3, "X")
        add_fin_x(bm, uv, rot, 0.72, -0.68, 0.52, -0.68, 0.072, 0.125, 0.009)
        add_fin_x(bm, uv, rot, -1.45, -1.88, -1.66, -1.90, 0.072, 0.240, 0.011)
    objs.append(make_obj("IRIST_SLM_Fins", bm, mat))
    return objs


def m_sam_aster30(mat: bpy.types.Material) -> list[bpy.types.Object]:
    # Stepped tandem booster (aft) + sleek PIF-PAF Aster dart (fore)
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    L = 4.90
    prof = [(-2.45, 0.008), (-2.42, 0.18), (-0.75, 0.18), (-0.55, 0.09), (1.65, 0.09), (2.20, 0.045), (2.45, 0.005)]
    rings = [[bm.verts.new((x, r * math.cos(2 * math.pi * i / 32), r * math.sin(2 * math.pi * i / 32))) for i in range(32)] for x, r in prof]
    for idx in range(len(rings) - 1):
        x0, x1 = prof[idx][0], prof[idx + 1][0]
        v0, v1 = 1.0 - (2.45 - x0) / L, 1.0 - (2.45 - x1) / L
        r0, r1 = rings[idx], rings[idx + 1]
        for i in range(32):
            ni = (i + 1) % 32
            f = bm.faces.new((r0[i], r0[ni], r1[ni], r1[i]))
            f.smooth = True
            for lp, uvc in zip(f.loops, (((i / 32) * U_BODY_MAX, v0), (((i + 1) / 32) * U_BODY_MAX, v0), (((i + 1) / 32) * U_BODY_MAX, v1), ((i / 32) * U_BODY_MAX, v1))):
                lp[uv].uv = uvc
    bm.faces.new(rings[-1]).smooth = True
    bm.faces.new(list(reversed(rings[0])))
    for k in range(4):
        rot = Matrix.Rotation(math.radians(45 + k * 90), 3, "X")
        add_fin_x(bm, uv, rot, 1.15, -0.35, 0.65, -0.35, 0.085, 0.220, 0.010)
        add_fin_x(bm, uv, rot, -1.95, -2.38, -2.14, -2.40, 0.175, 0.410, 0.012)
    return [make_obj("Aster30_Dart", bm, mat)]


def m_sam_pac3_mse(mat: bpy.types.Material) -> list[bpy.types.Object]:
    objs = [build_missile_body_x("PAC3MSE_Body", 5.20, 0.255, 0.68, "ogive", mat, boat=0.92)]
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    for k in range(4):
        rot = Matrix.Rotation(math.radians(45 + k * 90), 3, "X")
        add_fin_x(bm, uv, rot, -1.85, -2.45, -2.12, -2.48, 0.125, 0.365, 0.012)
    objs.append(make_obj("PAC3MSE_Fins", bm, mat))
    return objs


def m_keka_tropo5(mat: bpy.types.Material) -> list[bpy.types.Object]:
    """KEKA Aerospace Troposphere-5 Troll Rocket: bolted collars, checker stripes & huge yellow sheet-metal fins."""
    objs = [build_missile_body_x("Troposphere5_Hull", 3.60, 0.280, 0.56, "ogive", mat, segs=24, boat=1.05)]
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    # Heavy homemade bolted flange rings along cylinder
    for rx in (-1.20, -0.15, 0.90):
        add_cyl_x(bm, uv, rx - 0.04, rx + 0.04, 0.0, 0.0, 0.154, 24, (0.85, 0.65))
    # Flared welded exhaust bell
    add_cyl_x(bm, uv, -1.96, -1.78, 0.0, 0.0, 0.165, 20, (0.35, 0.04))
    # 3 huge riveted yellow sheet-metal tail fins (120 deg)
    for k in range(3):
        rot = Matrix.Rotation(math.radians(k * 120.0), 3, "X")
        add_fin_x(bm, uv, rot, -1.05, -1.78, -1.45, -1.84, 0.135, 0.520, 0.022, (0.85, 0.25))
    objs.append(make_obj("Troposphere5_Fins", bm, mat))
    return objs


def m_keka_tropo6(mat: bpy.types.Material) -> list[bpy.types.Object]:
    """KEKA Aerospace Troposphere-6: tall white-orange core + TWO massive orange strap-on side boosters!"""
    objs = [build_missile_body_x("Troposphere6_Core", 5.20, 0.340, 0.72, "ogive", mat, segs=28, boat=0.95)]
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    for side_y in (-0.31, 0.31):
        # Side strap-on solid booster cylinder + nose cone + bell nozzle + strut clamps
        add_cyl_x(bm, uv, -2.55, 0.15, side_y, 0.0, 0.125, 20, (0.35, 0.85))
        add_cyl_x(bm, uv, 0.15, 0.52, side_y, 0.0, 0.070, 16, (0.35, 0.88))
        add_box(bm, uv, (-0.2, side_y * 0.5, 0.0), (0.14, 0.35, 0.10), (0.85, 0.65))
        add_box(bm, uv, (-2.1, side_y * 0.5, 0.0), (0.14, 0.35, 0.10), (0.85, 0.65))
    for k in range(4):
        rot = Matrix.Rotation(math.radians(45 + k * 90), 3, "X")
        add_fin_x(bm, uv, rot, -1.75, -2.55, -2.15, -2.60, 0.165, 0.520, 0.020, (0.85, 0.25))
    objs.append(make_obj("Troposphere6_Boosters", bm, mat))
    return objs


def m_gokdogan_astra(mat: bpy.types.Material) -> list[bpy.types.Object]:
    objs = [build_missile_body_x("Gokdogan_Body", 3.80, 0.178, 0.62, "ogive", mat, boat=0.86)]
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    for k in range(4):
        rot = Matrix.Rotation(math.radians(45 + k * 90), 3, "X")
        add_fin_x(bm, uv, rot, 0.42, -0.32, 0.08, -0.32, 0.085, 0.245, 0.010)
        add_fin_x(bm, uv, rot, -1.48, -1.86, -1.68, -1.88, 0.082, 0.220, 0.010)
    objs.append(make_obj("Gokdogan_Fins", bm, mat))
    return objs


def m_rudram_arm(mat: bpy.types.Material) -> list[bpy.types.Object]:
    objs = [build_missile_body_x("Rudram_Body", 4.80, 0.360, 0.85, "ogive", mat, boat=0.86)]
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    for k in range(4):
        rot = Matrix.Rotation(math.radians(45 + k * 90), 3, "X")
        add_fin_x(bm, uv, rot, 0.85, -0.25, 0.45, -0.25, 0.175, 0.380, 0.014)
        add_fin_x(bm, uv, rot, -1.92, -2.36, -2.14, -2.38, 0.172, 0.390, 0.014)
    objs.append(make_obj("Rudram_Fins", bm, mat))
    return objs


def m_kh38_grom(mat: bpy.types.Material) -> list[bpy.types.Object]:
    objs = [build_missile_body_x("Kh38_Body", 4.20, 0.310, 0.48, "dome", mat, boat=0.84)]
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    for k in range(4):
        rot = Matrix.Rotation(math.radians(45 + k * 90), 3, "X")
        add_fin_x(bm, uv, rot, 0.55, -0.75, 0.12, -0.75, 0.150, 0.330, 0.013)
        add_fin_x(bm, uv, rot, -1.62, -2.04, -1.82, -2.06, 0.146, 0.350, 0.013)
    objs.append(make_obj("Kh38_Fins", bm, mat))
    return objs


def m_iskander_atacms(mat: bpy.types.Material) -> list[bpy.types.Object]:
    objs = [build_missile_body_x("Iskander_Body", 6.20, 0.720, 1.45, "blunt", mat, boat=0.90)]
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    for k in range(4):
        rot = Matrix.Rotation(math.radians(45 + k * 90), 3, "X")
        add_fin_x(bm, uv, rot, -2.38, -3.02, -2.68, -3.06, 0.350, 0.620, 0.024)
    objs.append(make_obj("Iskander_Fins", bm, mat))
    return objs


def m_df17_waverider(mat: bpy.types.Material) -> list[bpy.types.Object]:
    """DF-17: cylindrical rocket booster + chined flat-belly sharp delta waverider HGV payload."""
    objs = []
    # Booster stage (-3.90 to +0.65)
    bm_b = bmesh.new()
    uv_b = bm_b.loops.layers.uv.new("UVMap")
    add_cyl_x(bm_b, uv_b, -3.90, 0.65, 0.0, 0.0, 0.425, 32, (0.35, 0.50))
    for k in range(4):
        rot = Matrix.Rotation(math.radians(45 + k * 90), 3, "X")
        add_fin_x(bm_b, uv_b, rot, -3.15, -3.85, -3.50, -3.88, 0.420, 0.720, 0.022)
    objs.append(make_obj("DF17_Booster", bm_b, mat))

    # Hypersonic Waverider Glider (+0.65 to +3.90) - wide chined triangle with raised dorsal ridge
    bm_w = bmesh.new()
    uv_w = bm_w.loops.layers.uv.new("UVMap")
    pts_a = [Vector((0.65, 0.0, 0.34)), Vector((0.65, 0.68, -0.14)), Vector((0.65, 0.0, -0.22)), Vector((0.65, -0.68, -0.14))]
    pts_m = [Vector((2.10, 0.0, 0.24)), Vector((2.10, 0.42, -0.08)), Vector((2.10, 0.0, -0.14)), Vector((2.10, -0.42, -0.08))]
    pts_n = [Vector((3.90, 0.0, 0.01)), Vector((3.90, 0.015, -0.01)), Vector((3.90, 0.0, -0.02)), Vector((3.90, -0.015, -0.01))]
    va = [bm_w.verts.new(p) for p in pts_a]
    vm = [bm_w.verts.new(p) for p in pts_m]
    vn = [bm_w.verts.new(p) for p in pts_n]
    for s0, s1 in ((va, vm), (vm, vn)):
        for i in range(4):
            ni = (i + 1) % 4
            f = bm_w.faces.new((s0[i], s0[ni], s1[ni], s1[i]))
            for lp in f.loops:
                lp[uv_w].uv = (0.35, 0.85)
    for f in (bm_w.faces.new(list(reversed(va))), bm_w.faces.new(vn)):
        for lp in f.loops:
            lp[uv_w].uv = (0.35, 0.85)
    # Cantilevered glider vertical V-stabilizers
    for sy in (-1.0, 1.0):
        add_fin_x(bm_w, uv_w, Matrix.Rotation(math.radians(sy * 36.0), 3, "X"), 1.05, 0.65, 0.82, 0.62, 0.14, 0.44, 0.016)
    objs.append(make_obj("DF17_Waverider", bm_w, mat))
    return objs


def m_javelin_top(mat: bpy.types.Material) -> list[bpy.types.Object]:
    objs = [build_missile_body_x("Javelin_Body", 1.25, 0.127, 0.14, "dome", mat, segs=24, boat=0.92)]
    for k in range(4):
        rot = Matrix.Rotation(math.radians(45 + k * 90), 3, "X")
        bm_w = bmesh.new()
        uv_w = bm_w.loops.layers.uv.new("UVMap")
        add_fin_x(bm_w, uv_w, rot, 0.14, -0.08, 0.04, -0.10, 0.0, 0.22, 0.008)
        piv = rot @ Vector((0.02, 0.0, 0.062))
        w_obj = make_obj(f"Javelin_Wing_{k}", bm_w, mat, location=piv)
        axis = (rot @ Vector((0.0, 1.0, 0.0))).normalized()
        w_obj.rotation_mode = "QUATERNION"
        act = bpy.data.actions.new(name=f"25_Javelin_Wing_{k}")
        w_obj.animation_data_create()
        w_obj.animation_data.action = act
        w_obj.rotation_quaternion = Quaternion(axis, math.radians(82.0))
        w_obj.keyframe_insert(data_path="rotation_quaternion", frame=100)
        w_obj.rotation_quaternion = Quaternion((1, 0, 0, 0))
        w_obj.keyframe_insert(data_path="rotation_quaternion", frame=200)
        objs.append(w_obj)
    return objs


def m_palianytsia_jet(mat: bpy.types.Material) -> list[bpy.types.Object]:
    """Ukrainian Palianytsia / Shahed-238 turbojet drone-missile: slender fuselage, dorsal scoop intake, swept wing & V-tail."""
    objs = [build_missile_body_x("Palianytsia_Body", 3.40, 0.320, 0.65, "ogive", mat, segs=28, boat=0.72)]
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    # Dorsal turbojet scoop
    add_box(bm, uv, (-0.85, 0.0, 0.22), (0.85, 0.18, 0.16), (0.85, 0.65))
    for sy in (-1.0, 1.0):
        # Main straight/slightly swept wings (total span 2.4m)
        add_fin_x(bm, uv, Matrix.Rotation(math.radians(sy * 90.0), 3, "X"), 0.35, -0.18, -0.25, -0.52, 0.14, 1.20, 0.024)
        # V-tail stabilizers
        add_fin_x(bm, uv, Matrix.Rotation(math.radians(sy * 48.0), 3, "X"), -1.25, -1.62, -1.48, -1.70, 0.12, 0.48, 0.014)
    objs.append(make_obj("Palianytsia_Airframe", bm, mat))
    return objs


def m_kalibr_3m54(mat: bpy.types.Material) -> list[bpy.types.Object]:
    objs = [build_missile_body_x("Kalibr_Body", 6.20, 0.533, 0.72, "dome", mat, boat=0.84)]
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    for k in range(4):
        rot = Matrix.Rotation(math.radians(45 + k * 90), 3, "X")
        add_fin_x(bm, uv, rot, -2.35, -2.98, -2.65, -3.02, 0.255, 0.58, 0.018)
    objs.append(make_obj("Kalibr_Tail", bm, mat))
    # Folding mid-wings (DrawArg 25)
    for side, sn in ((-1.0, "L"), (1.0, "R")):
        bm_w = bmesh.new()
        uv_w = bm_w.loops.layers.uv.new("UVMap")
        rot = Matrix.Rotation(math.radians(side * 90.0), 3, "X")
        add_fin_x(bm_w, uv_w, rot, 0.25, -0.20, -0.15, -0.45, 0.0, 1.45, 0.018)
        w_obj = make_obj(f"Kalibr_Wing_{sn}", bm_w, mat, location=(0.25, side * 0.25, 0.04))
        key_euler(w_obj, f"25_Kalibr_Wing_{sn}", [(100, (0, 0, side * math.radians(-82.0))), (200, (0, 0, 0))])
        objs.append(w_obj)
    return objs


MODELS_V4 = [
    # Ground SAMs & Launchers
    ("ng_cram_centurion",  "cram_centurion", (6.8, 3.2, 4.6),   g_cram_centurion, "sam"),
    ("ng_iron_dome_ln",    "iron_dome",      (5.2, 3.0, 4.4),   g_iron_dome_ln,   "sam"),
    ("ng_iron_dome_radar", "elm2084_radar",  (7.5, 3.0, 5.2),   g_iron_dome_radar,"sam"),
    ("ng_irist_slm_ln",    "sam_nato_olive", (9.2, 3.0, 5.8),   lambda m: g_vertical_sam_8cell(m, "IRIST_SLM", 0.22, 4.4), "sam"),
    ("ng_sampt_aster30",   "sam_nato_olive", (9.2, 3.0, 6.2),   lambda m: g_vertical_sam_8cell(m, "SAMPT_Mamba", 0.28, 5.2), "sam"),
    ("ng_pantsir_sm",      "pantsir_sm",     (9.5, 3.4, 5.0),   g_pantsir_sm,     "sam"),
    ("ng_patriot_pac3_ln", "sam_nato_olive", (7.2, 3.2, 5.2),   g_patriot_pac3_ln,"sam"),
    ("ng_keka_launcher",   "keka_troll",     (5.2, 2.4, 4.6),   g_keka_launcher,  "sam"),
    # SAM Interceptors, KEKA Troll & Priority Backlog Missiles
    ("ng_sam_tamir",       "iron_dome",      (3.1, 0.5, 0.5),   m_sam_tamir,      "bkl"),
    ("ng_sam_irist_slm",   "sam_nato_olive", (4.1, 0.6, 0.6),   m_sam_irist_slm,  "bkl"),
    ("ng_sam_aster30",     "sam_nato_olive", (5.0, 0.9, 0.9),   m_sam_aster30,    "bkl"),
    ("ng_sam_pac3_mse",    "sam_nato_olive", (5.3, 0.8, 0.8),   m_sam_pac3_mse,   "bkl"),
    ("ng_keka_tropo5",     "keka_troll",     (3.7, 1.1, 1.1),   m_keka_tropo5,    "bkl"),
    ("ng_keka_tropo6",     "keka_troll",     (5.3, 1.2, 1.1),   m_keka_tropo6,    "bkl"),
    ("ng_gokdogan_astra",  "pl12_15",        (3.9, 0.6, 0.6),   m_gokdogan_astra, "bkl"),
    ("ng_rudram_arm",      "aargm_er",       (4.9, 0.9, 0.9),   m_rudram_arm,     "bkl"),
    ("ng_kh38_grom",       "kh58_sead",      (4.3, 0.8, 0.8),   m_kh38_grom,      "bkl"),
    ("ng_iskander_atacms", "iskander_ru",    (6.3, 1.4, 1.4),   m_iskander_atacms,"bkl"),
    ("ng_df17_waverider",  "df17_tps",       (8.0, 1.6, 1.6),   m_df17_waverider, "bkl"),
    ("ng_javelin_top",     "javelin_dark",   (1.4, 0.6, 0.6),   m_javelin_top,    "bkl"),
    ("ng_palianytsia_jet", "palianytsia_jet",(3.5, 2.5, 0.9),   m_palianytsia_jet,"bkl"),
    ("ng_kalibr_3m54",     "kh35_uran",      (6.3, 3.0, 1.2),   m_kalibr_3m54,    "bkl"),
]


def add_box_helper(name: str, size_xyz: tuple[float, float, float], special_type: str) -> None:
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0))
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = size_xyz
    bpy.ops.object.transform_apply(scale=True)
    if hasattr(obj, "EDMProps"):
        obj.EDMProps.SPECIAL_TYPE = special_type


def render_preview(group: str, out_path: Path, cam_loc, cam_tgt, spacing_xy) -> None:
    clear_scene()
    items = [(n, t, fn) for n, t, _, fn, g in MODELS_V4 if g == group]
    mats = {t: create_preview_material(t) for _, t, _ in items}
    bpy.context.scene.frame_set(145 if group == "sam" else 200)
    for (name, theme, fn), (xp, yp) in zip(items, spacing_xy):
        objs = fn(mats[theme])
        bpy.context.view_layer.update()
        # Freeze evaluated transforms BEFORE moving roots
        for o in objs:
            if o.animation_data and o.animation_data.action:
                o.rotation_euler = o.rotation_euler.copy()
                o.rotation_quaternion = o.rotation_quaternion.copy()
                o.animation_data_clear()
        for o in objs:
            if o.parent is None:
                o.location.x += xp
                o.location.y += yp

    bpy.ops.mesh.primitive_plane_add(size=120, location=(0, 0, 0.0 if group == "sam" else -0.8))
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
    for loc, en in (((18.0, -16.0, 22.0), 12000), ((-18.0, 12.0, 14.0), 6000), ((0.0, 22.0, 12.0), 5000)):
        bpy.ops.object.light_add(type="AREA", location=loc)
        l = bpy.context.active_object
        l.data.energy, l.data.size = en, 10.0
        l.rotation_euler = (tgt - l.location).to_track_quat("-Z", "Y").to_euler()
    bpy.ops.object.camera_add(location=cam_loc)
    cam = bpy.context.active_object
    cam.data.lens = 30.0
    cam.rotation_euler = (tgt - cam.location).to_track_quat("-Z", "Y").to_euler()
    bpy.context.scene.camera = cam
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.samples = 32
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
    for name, theme, bbox, fn, grp in MODELS_V4:
        clear_scene()
        mat = create_edm_pbr_material(f"Mat_{name}", theme)
        fn(mat)
        bpy.ops.edm.import_matrials()
        add_box_helper("BoundingBox", bbox, "BOUNDING_BOX")
        add_box_helper("Collision", (bbox[0] * 0.9, bbox[1] * 0.85, bbox[2] * 0.85), "COLLISION_SHELL")
        bpy.context.scene.frame_set(100)
        out = SHAPES_DIR / f"{name}.edm"
        bpy.ops.edm.export(filepath=str(out))
        print(f"[OK] Exported {name}.edm ({out.stat().st_size} B)")

    sam_coords = [(-14, 5), (-7, 5), (0, 5), (8, 5), (-14, -6), (-5, -6), (4, -6), (12, -6)]
    render_preview("sam", PREVIEW_SAM, (16.0, -24.0, 13.0), (-1.5, -0.5, 1.5), sam_coords)

    bkl_coords = [
        (-4, 9), (-4, 6), (-4, 3), (-4, 0), (-4, -3), (-4, -6), (-4, -9),
        (5, 8), (5, 5), (5, 2), (5, -1), (5, -4), (5, -7), (5, -10),
    ]
    render_preview("bkl", PREVIEW_BKL, (16.0, -16.0, 12.0), (0.5, -0.5, 0.0), bkl_coords)


if __name__ == "__main__":
    main()
