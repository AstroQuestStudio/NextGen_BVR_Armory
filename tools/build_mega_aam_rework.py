"""Blender 5.2 Blueprint-Faithful AAM Rework & Sub-Variant Builder (15 EDM shapes).
Reads reference textures & Learning_Demo EDM shader directly on C: drive.
Exports to C:/Users/trufa/Saved Games/DCS/Mods/tech/NextGen_BVR_Armory/Shapes/
and renders a 1920x1080 Cycles showcase: preview_mega_aam_v3.png
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
PREVIEW_OUT = Path(r"C:\Users\trufa\.gemini\antigravity\brain\d63eda09-3e0f-4368-acac-466f620a5bd4\preview_mega_aam_v3.png")

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


def animate_rot_quat(obj: bpy.types.Object, action_name: str, frame_a: int, q_a: Quaternion, frame_b: int, q_b: Quaternion) -> None:
    obj.rotation_mode = "QUATERNION"
    act = bpy.data.actions.new(name=action_name)
    obj.animation_data_create()
    obj.animation_data.action = act
    obj.rotation_quaternion = q_a
    obj.keyframe_insert(data_path="rotation_quaternion", frame=frame_a)
    obj.rotation_quaternion = q_b
    obj.keyframe_insert(data_path="rotation_quaternion", frame=frame_b)


def build_fuselage(name: str, length: float, diam: float, nose_len: float, dome_style: str, mat: bpy.types.Material, boat_tail: float = 0.80) -> bpy.types.Object:
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    segs = 64
    r = diam * 0.5
    half = length * 0.5
    nose_base = half - nose_len
    tail = -half + length * 0.05

    profile = [
        (-half + length * 0.04, 0.004),
        (-half + length * 0.015, r * 0.42),
        (-half, r * boat_tail),
        (tail, r),
    ]
    for frac, clamp in ((0.18, True), (0.38, False), (0.58, True)):
        ys = -half + length * frac
        if ys < nose_base - 0.08:
            if clamp:
                profile.extend([(ys - 0.014, r), (ys - 0.009, r * 1.022), (ys + 0.009, r * 1.022), (ys + 0.014, r)])
            else:
                profile.extend([(ys - 0.005, r), (ys, r * 0.985), (ys + 0.005, r)])
    profile.append((nose_base, r))

    steps = 16
    for i in range(1, steps + 1):
        t = i / steps
        y = nose_base + t * nose_len
        if dome_style == "ir_glass":
            if t < 0.52:
                st = t / 0.52
                rad = r * (1.0 - 0.24 * st)
            else:
                st = (t - 0.52) / 0.48
                ang = st * (math.pi * 0.5)
                rad = max(0.003, r * 0.76 * math.cos(ang))
                y = nose_base + 0.52 * nose_len + (r * 0.76) * math.sin(ang)
        elif dome_style == "blunt_ogive":
            rad = r * math.pow(max(0.0, 1.0 - t * 0.96), 0.48)
        else:
            rad = r * math.pow(max(0.0, 1.0 - t * 0.97), 0.65)
        if i == steps:
            rad = 0.004
        profile.append((y, rad))

    rings = [[bm.verts.new((rad * math.sin(2 * math.pi * i / segs), y, rad * math.cos(2 * math.pi * i / segs))) for i in range(segs)] for y, rad in profile]
    for idx in range(len(rings) - 1):
        y0, y1 = profile[idx][0], profile[idx + 1][0]
        v0 = 1.0 - max(0.0, min(1.0, (half - y0) / length))
        v1 = 1.0 - max(0.0, min(1.0, (half - y1) / length))
        r0, r1 = rings[idx], rings[idx + 1]
        for i in range(segs):
            ni = (i + 1) % segs
            u0, u1 = (i / segs) * U_BODY_MAX, ((i + 1) / segs) * U_BODY_MAX
            f = bm.faces.new((r0[i], r0[ni], r1[ni], r1[i]))
            f.smooth = True
            for loop, uvc in zip(f.loops, ((u0, v0), (u1, v0), (u1, v1), (u0, v1))):
                loop[uv].uv = uvc
    bm.faces.new(rings[-1]).smooth = True
    bm.faces.new(list(reversed(rings[0])))
    return make_obj(name, bm, mat)


def add_airfoil_fin(bm: bmesh.types.BMesh, uv, rot: Matrix, y_r_le: float, y_r_te: float, y_t_le: float, y_t_te: float, z0: float, z1: float, thick: float = 0.011) -> None:
    p_r_le = rot @ Vector((0, y_r_le, z0))
    p_r_te = rot @ Vector((0, y_r_te, z0))
    p_t_le = rot @ Vector((0, y_t_le, z1))
    p_t_te = rot @ Vector((0, y_t_te, z1))
    n = rot @ Vector((1, 0, 0))
    vr = [bm.verts.new(p_r_le), bm.verts.new(p_r_le.lerp(p_r_te, 0.35) + n * (thick * 0.5)), bm.verts.new(p_r_te), bm.verts.new(p_r_le.lerp(p_r_te, 0.35) - n * (thick * 0.5))]
    vt = [bm.verts.new(p_t_le), bm.verts.new(p_t_le.lerp(p_t_te, 0.35) + n * (thick * 0.28)), bm.verts.new(p_t_te), bm.verts.new(p_t_le.lerp(p_t_te, 0.35) - n * (thick * 0.28))]
    u_pairs = [(0.728, 0.86), (0.86, 0.99), (0.99, 0.86), (0.86, 0.728)]
    for i in range(4):
        ni = (i + 1) % 4
        f = bm.faces.new((vr[i], vr[ni], vt[ni], vt[i]))
        ua, ub = u_pairs[i]
        for loop, uvc in zip(f.loops, ((ua, 0.48), (ub, 0.48), (ub, 0.97), (ua, 0.97))):
            loop[uv].uv = uvc
    for f in (bm.faces.new(list(reversed(vr))), bm.faces.new(vt)):
        for loop in f.loops:
            loop[uv].uv = (0.86, 0.97)


def build_fin_set(name: str, r_base: float, specs: list[tuple[float, float, float, float, float]], mat: bpy.types.Material, roll_deg: float = 45.0, thick: float = 0.010, rolleron: bool = False) -> bpy.types.Object:
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    for y_r_le, y_r_te, y_t_le, y_t_te, span in specs:
        for k in range(4):
            rot = Matrix.Rotation(math.radians(roll_deg + k * 90.0), 3, "Y")
            add_airfoil_fin(bm, uv, rot, y_r_le, y_r_te, y_t_le, y_t_te, r_base - 0.005, r_base + span, thick)
            if rolleron:
                ret = bmesh.ops.create_cube(bm, size=1.0)
                for v in ret["verts"]:
                    v.co.x = v.co.x * 0.014
                    v.co.y = v.co.y * 0.055 + (y_t_te + 0.03)
                    v.co.z = v.co.z * 0.016 + (r_base + span)
                    v.co = rot @ v.co
    for f in bm.faces:
        for loop in f.loops:
            if loop[uv].uv.length == 0:
                loop[uv].uv = (0.86, 0.72)
    return make_obj(name, bm, mat)


def build_lattice_grid_fin_bm(bm: bmesh.types.BMesh, uv, rot: Matrix, width: float, height: float, depth: float, cells: int = 3) -> None:
    """True 3D perforated waffle-iron lattice grid fin in local pivot space."""
    bar = 0.005
    # Outer frame + vertical & horizontal inner lattice ribs
    for i in range(cells + 1):
        x = -width * 0.5 + (i / cells) * width
        ret = bmesh.ops.create_cube(bm, size=1.0)
        for v in ret["verts"]:
            v.co = rot @ Vector((v.co.x * bar + x, v.co.y * depth, (v.co.z + 0.5) * height))
    for j in range(cells + 1):
        z = (j / cells) * height
        ret = bmesh.ops.create_cube(bm, size=1.0)
        for v in ret["verts"]:
            v.co = rot @ Vector((v.co.x * width, v.co.y * depth, v.co.z * bar + z))
    # Root actuator stem
    stem = bmesh.ops.create_cube(bm, size=1.0)
    for v in stem["verts"]:
        v.co = rot @ Vector((v.co.x * 0.018, v.co.y * 0.030, v.co.z * 0.035 - 0.01))
    for f in bm.faces:
        for loop in f.loops:
            loop[uv].uv = (0.85, 0.30)


# =========================================================================
# AAM BUILDERS (15 Blueprint-Faithful Shapes)
# =========================================================================
def b_iris_t(mat: bpy.types.Material) -> list[bpy.types.Object]:
    objs = [build_fuselage("IRIST_Body", 2.94, 0.127, 0.22, "ir_glass", mat, boat_tail=0.90)]
    objs.append(build_fin_set("IRIST_Fins", 0.0635, [
        (0.55, -0.82, 0.35, -0.82, 0.048),     # Very long low-profile mid-body strakes
        (-1.12, -1.40, -1.26, -1.42, 0.160),   # Clipped aft control fins
    ], mat, thick=0.009))
    # TVC jet-vane shrouds around nozzle
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    for k in range(4):
        rot = Matrix.Rotation(math.radians(45 + k * 90), 3, "Y")
        c = bmesh.ops.create_cube(bm, size=1.0)
        for v in c["verts"]:
            v.co = rot @ Vector((v.co.x * 0.014, v.co.y * 0.07 - 1.44, v.co.z * 0.016 + 0.058))
    for f in bm.faces:
        for loop in f.loops:
            loop[uv].uv = (0.85, 0.30)
    objs.append(make_obj("IRIST_TVC", bm, mat))
    return objs


def b_r77_grid(mat: bpy.types.Material) -> list[bpy.types.Object]:
    objs = [build_fuselage("R77_Body", 3.71, 0.200, 0.62, "blunt_ogive", mat, boat_tail=0.76)]
    objs.append(build_fin_set("R77_Strakes", 0.100, [
        (0.45, -1.05, 0.22, -1.05, 0.068),     # 4 long narrow mid-body strakes
    ], mat, thick=0.010))
    # 4 Animated Open Lattice Grid Fins (DrawArg 25: folded flat backward at Frame 100 -> deployed radial at Frame 200)
    for k in range(4):
        rot = Matrix.Rotation(math.radians(45 + k * 90), 3, "Y")
        bm_g = bmesh.new()
        uv_g = bm_g.loops.layers.uv.new("UVMap")
        build_lattice_grid_fin_bm(bm_g, uv_g, rot, width=0.22, height=0.23, depth=0.045, cells=3)
        piv = rot @ Vector((0, -1.68, 0.095))
        g_obj = make_obj(f"R77_GridFin_{k}", bm_g, mat, location=(piv.x, -1.68, piv.z))
        axis = (rot @ Vector((1, 0, 0))).normalized()
        animate_rot_quat(g_obj, f"25_R77_Grid_{k}", 100, Quaternion(axis, math.radians(84.0)), 200, Quaternion((1, 0, 0, 0)))
        objs.append(g_obj)
    return objs


def b_r77m(mat: bpy.types.Material) -> list[bpy.types.Object]:
    objs = [build_fuselage("R77M_Body", 3.71, 0.200, 0.68, "ogive", mat, boat_tail=0.80)]
    objs.append(build_fin_set("R77M_Fins", 0.100, [
        (0.42, -0.95, 0.22, -0.95, 0.072),
        (-1.45, -1.78, -1.62, -1.78, 0.210),
    ], mat, thick=0.011))
    return objs


def b_pl12a(mat: bpy.types.Material) -> list[bpy.types.Object]:
    objs = [build_fuselage("PL12A_Body", 3.93, 0.203, 0.72, "ogive", mat, boat_tail=0.82)]
    objs.append(build_fin_set("PL12A_Fins", 0.1015, [
        (0.22, -0.24, -0.04, -0.24, 0.230),   # Clipped-tip delta mid-wings
        (-1.52, -1.92, -1.74, -1.94, 0.265),  # Clipped-root aft fins
    ], mat, thick=0.012))
    return objs


def b_pl15(mat: bpy.types.Material, fold: bool = False) -> list[bpy.types.Object]:
    objs = [build_fuselage("PL15_Body", 4.00, 0.203, 0.76, "ogive", mat, boat_tail=0.82)]
    objs.append(build_fin_set("PL15_MidWings", 0.1015, [(0.26, -0.18, 0.02, -0.18, 0.175)], mat, thick=0.011))
    if not fold:
        objs.append(build_fin_set("PL15_AftFins", 0.1015, [(-1.58, -1.94, -1.76, -1.94, 0.195)], mat, thick=0.011))
    else:
        for k in range(4):
            rot = Matrix.Rotation(math.radians(45 + k * 90), 3, "Y")
            bm_f = bmesh.new()
            uv_f = bm_f.loops.layers.uv.new("UVMap")
            add_airfoil_fin(bm_f, uv_f, rot, 0.18, -0.18, 0.02, -0.18, 0.0, 0.185, 0.010)
            piv = rot @ Vector((0, -1.76, 0.098))
            f_obj = make_obj(f"PL15E_AftFin_{k}", bm_f, mat, location=(piv.x, -1.76, piv.z))
            axis = (rot @ Vector((1, 0, 0))).normalized()
            animate_rot_quat(f_obj, f"25_PL15E_Fin_{k}", 100, Quaternion(axis, math.radians(82.0)), 200, Quaternion((1, 0, 0, 0)))
            objs.append(f_obj)
    return objs


def b_python5(mat: bpy.types.Material) -> list[bpy.types.Object]:
    objs = [build_fuselage("Python5_Body", 3.10, 0.160, 0.24, "ir_glass", mat, boat_tail=0.86)]
    objs.append(build_fin_set("Python5_Surfaces", 0.080, [
        (1.18, 1.06, 1.10, 1.06, 0.065),      # 4 tiny front destabilizers
        (0.98, 0.80, 0.90, 0.80, 0.155),      # 4 forward rectangular control canards
        (-0.55, -1.48, -1.20, -1.48, 0.240),  # 4 huge swept aft delta wings
    ], mat, thick=0.009))
    return objs


def b_r74m2(mat: bpy.types.Material) -> list[bpy.types.Object]:
    objs = [build_fuselage("R74M2_Body", 2.93, 0.170, 0.22, "ir_glass", mat, boat_tail=0.84)]
    objs.append(build_fin_set("R74M2_Canards", 0.085, [
        (1.14, 1.06, 1.12, 1.06, 0.040),      # 4 tiny AOA nose vanes
        (0.98, 0.88, 0.92, 0.88, 0.065),      # 4 forward destabilizer strakes
        (0.76, 0.56, 0.68, 0.56, 0.140),      # 4 forward control canards
    ], mat, thick=0.008))
    objs.append(build_fin_set("R74M2_AftRollerons", 0.085, [
        (-0.98, -1.38, -1.24, -1.40, 0.185),  # Swept aft wings with rolleron pods
    ], mat, thick=0.010, rolleron=True))
    return objs


def b_aim9x_b3(mat: bpy.types.Material) -> list[bpy.types.Object]:
    objs = [build_fuselage("AIM9XB3_Body", 3.02, 0.127, 0.20, "ir_glass", mat, boat_tail=0.88)]
    objs.append(build_fin_set("AIM9XB3_Fins", 0.0635, [
        (1.10, 0.92, 1.00, 0.92, 0.115),      # 4 tiny clipped forward canards
        (-1.12, -1.44, -1.32, -1.46, 0.125),  # 4 compact swept aft fins
    ], mat, thick=0.008))
    return objs


def b_aim54e(mat: bpy.types.Material) -> list[bpy.types.Object]:
    objs = [build_fuselage("AIM54E_Body", 4.01, 0.380, 0.74, "ogive", mat, boat_tail=0.84)]
    objs.append(build_fin_set("AIM54E_Fins", 0.190, [
        (0.75, -0.78, -0.35, -0.78, 0.270),   # 4 long-chord mid-body delta wings
        (-1.42, -1.92, -1.64, -1.92, 0.275),  # 4 large aft control fins
    ], mat, thick=0.016))
    return objs


def b_meteor(mat: bpy.types.Material) -> list[bpy.types.Object]:
    objs = [build_fuselage("Meteor_Body", 3.65, 0.178, 0.72, "ogive", mat, boat_tail=0.82)]
    objs.append(build_fin_set("Meteor_TailFins", 0.089, [(-1.38, -1.74, -1.58, -1.76, 0.240)], mat, thick=0.011))
    # Twin long ramjet side ducts running mid-body all the way to the tail
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    r = 0.089
    for side in (-1.0, 1.0):
        x_in, x_out = side * (r + 0.004), side * (r + 0.072)
        z_t, z_b = 0.026, -0.050
        y_f, y_a = 0.22, -1.76
        vf = [bm.verts.new(p) for p in ((x_in, y_f, z_t), (x_out * 0.94, y_f - 0.03, z_t * 0.85), (x_out, y_f - 0.08, z_b * 0.85), (x_in, y_f - 0.08, z_b))]
        vm = [bm.verts.new(p) for p in ((x_in, y_a + 0.14, z_t), (x_out, y_a + 0.14, z_t * 0.85), (x_out, y_a + 0.14, z_b * 0.85), (x_in, y_a + 0.14, z_b))]
        va = [bm.verts.new(p) for p in ((x_in, y_a, z_t * 0.45), (x_in + side * 0.02, y_a, z_t * 0.35), (x_in + side * 0.02, y_a, z_b * 0.35), (x_in, y_a, z_b * 0.45))]
        for i in range(4):
            ni = (i + 1) % 4
            for face_v, uv_v in (((vf[i], vf[ni], vm[ni], vm[i]), (0.86, 0.36)), ((vm[i], vm[ni], va[ni], va[i]), (0.86, 0.25))):
                f = bm.faces.new(face_v)
                f.smooth = True
                for lp in f.loops:
                    lp[uv].uv = uv_v
        for face_v in (vf, list(reversed(va))):
            f = bm.faces.new(face_v)
            for lp in f.loops:
                lp[uv].uv = (0.86, 0.06)
    objs.append(make_obj("Meteor_RamjetDucts", bm, mat))
    return objs


def b_mica_ng(mat: bpy.types.Material) -> list[bpy.types.Object]:
    objs = [build_fuselage("MICA_Body", 3.10, 0.160, 0.44, "ogive", mat, boat_tail=0.84)]
    objs.append(build_fin_set("MICA_Fins", 0.080, [
        (0.95, -0.68, 0.72, -0.68, 0.060),    # Long mid-body strakes
        (-0.98, -1.44, -1.24, -1.46, 0.175),  # Trapezoidal aft control fins
    ], mat, thick=0.010))
    return objs


def b_r37m(mat: bpy.types.Material) -> list[bpy.types.Object]:
    objs = [build_fuselage("R37M_Body", 4.06, 0.380, 0.85, "ogive", mat, boat_tail=0.84)]
    objs.append(build_fin_set("R37M_Strakes", 0.190, [(0.80, -0.95, 0.55, -0.95, 0.145)], mat, thick=0.015))
    # Folding aft cruciform fins (DrawArg 25)
    for k in range(4):
        rot = Matrix.Rotation(math.radians(45 + k * 90), 3, "Y")
        bm_f = bmesh.new()
        uv_f = bm_f.loops.layers.uv.new("UVMap")
        add_airfoil_fin(bm_f, uv_f, rot, 0.20, -0.20, 0.0, -0.20, 0.0, 0.175, 0.014)
        piv = rot @ Vector((0, -1.78, 0.185))
        f_obj = make_obj(f"R37M_Fin_{k}", bm_f, mat, location=(piv.x, -1.78, piv.z))
        axis = (rot @ Vector((1, 0, 0))).normalized()
        animate_rot_quat(f_obj, f"25_R37M_Fin_{k}", 100, Quaternion(axis, math.radians(82.0)), 200, Quaternion((1, 0, 0, 0)))
        objs.append(f_obj)
    return objs


def b_aam4b(mat: bpy.types.Material) -> list[bpy.types.Object]:
    objs = [build_fuselage("AAM4B_Body", 3.67, 0.203, 0.66, "ogive", mat, boat_tail=0.84)]
    objs.append(build_fin_set("AAM4B_Fins", 0.1015, [
        (0.28, -0.45, -0.05, -0.45, 0.265),
        (-1.42, -1.78, -1.62, -1.80, 0.215),
    ], mat, thick=0.011))
    return objs


def b_aim260(mat: bpy.types.Material) -> list[bpy.types.Object]:
    objs = [build_fuselage("AIM260_Body", 3.66, 0.178, 0.74, "ogive", mat, boat_tail=0.84)]
    objs.append(build_fin_set("AIM260_Fins", 0.089, [
        (0.65, -0.75, 0.45, -0.75, 0.025),
        (-1.42, -1.78, -1.62, -1.78, 0.145),
    ], mat, thick=0.010))
    return objs


def b_aim174b(mat: bpy.types.Material) -> list[bpy.types.Object]:
    objs = [build_fuselage("AIM174B_Body", 5.03, 0.343, 0.96, "ogive", mat, boat_tail=0.86)]
    objs.append(build_fin_set("AIM174B_Fins", 0.1715, [
        (0.90, -1.45, 0.65, -1.45, 0.145),
        (-1.95, -2.42, -2.18, -2.44, 0.350),
    ], mat, thick=0.015))
    return objs


def b_pl17(mat: bpy.types.Material) -> list[bpy.types.Object]:
    objs = [build_fuselage("PL17_Body", 6.00, 0.260, 0.95, "ogive", mat, boat_tail=0.84)]
    objs.append(build_fin_set("PL17_Fins", 0.130, [
        (0.45, -1.35, 0.20, -1.35, 0.048),
        (-2.55, -2.92, -2.74, -2.94, 0.190),
    ], mat, thick=0.012))
    return objs


AAMS = [
    ("ng_iris_t",    "iris_t",     (0.5, 3.0, 0.5), b_iris_t),
    ("ng_r77_grid",  "r77_grid",   (0.7, 3.8, 0.7), b_r77_grid),
    ("ng_r77m",      "east_ru_cn", (0.7, 3.8, 0.7), b_r77m),
    ("ng_pl12a",     "pl12_15",    (0.8, 4.0, 0.8), b_pl12a),
    ("ng_pl15",      "pl12_15",    (0.6, 4.1, 0.6), lambda m: b_pl15(m, False)),
    ("ng_pl15e",     "pl12_15",    (0.6, 4.1, 0.6), lambda m: b_pl15(m, True)),
    ("ng_python5",   "python5",    (0.7, 3.2, 0.7), b_python5),
    ("ng_r74m2",     "r74m2",      (0.6, 3.0, 0.6), b_r74m2),
    ("ng_aim9x_b3",  "aim9x_b3",   (0.4, 3.1, 0.4), b_aim9x_b3),
    ("ng_aim54e",    "aim54e",     (1.0, 4.1, 1.0), b_aim54e),
    ("ng_meteor",    "meteor",     (0.7, 3.7, 0.7), b_meteor),
    ("ng_mica_ng",   "french_mica",(0.6, 3.2, 0.6), b_mica_ng),
    ("ng_r37m",      "east_ru_cn", (0.8, 4.2, 0.8), b_r37m),
    ("ng_aam4b",     "pl12_15",    (0.8, 3.8, 0.8), b_aam4b),
    ("ng_aim260",    "us_bvr",     (0.5, 3.7, 0.5), b_aim260),
    ("ng_aim174b",   "usn_174b",   (1.1, 5.1, 1.1), b_aim174b),
    ("ng_pl17_long", "pl12_15",    (0.7, 6.1, 0.7), b_pl17),
]


def add_box_helper(name: str, size_xyz: tuple[float, float, float], special_type: str) -> None:
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0))
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = size_xyz
    bpy.ops.object.transform_apply(scale=True)
    if hasattr(obj, "EDMProps"):
        obj.EDMProps.SPECIAL_TYPE = special_type


def render_showcase() -> None:
    clear_scene()
    themes = sorted({t for _, t, _, _ in AAMS})
    mats = {t: create_preview_material(t) for t in themes}
    bpy.context.scene.frame_set(200)
    cols = [
        ("ng_iris_t", -4.2), ("ng_aim9x_b3", -3.4), ("ng_r74m2", -2.6), ("ng_python5", -1.8),
        ("ng_mica_ng", -1.0), ("ng_meteor", -0.2), ("ng_r77_grid", 0.6), ("ng_r77m", 1.4),
        ("ng_pl12a", 2.2), ("ng_pl15", 3.0), ("ng_aam4b", 3.8), ("ng_aim54e", 4.7), ("ng_r37m", 5.7),
    ]
    spec_map = {n: (t, fn) for n, t, _, fn in AAMS}
    for n, x_pos in cols:
        t, fn = spec_map[n]
        objs = fn(mats[t])
        bpy.context.view_layer.update()
        for o in objs:
            if o.animation_data and o.animation_data.action:
                o.rotation_quaternion = o.rotation_quaternion.copy()
                o.animation_data_clear()
            o.location.x += x_pos

    bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 0, -0.60))
    floor = bpy.context.active_object
    fm = bpy.data.materials.new("Floor")
    fm.use_nodes = True
    fm.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.045, 0.05, 0.06, 1.0)
    floor.data.materials.append(fm)
    world = bpy.context.scene.world or bpy.data.worlds.new("World")
    bpy.context.scene.world = world
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.025, 0.03, 0.04, 1.0)
    tgt = Vector((0.6, 0.0, 0.0))
    for loc, en in (((5.0, 5.5, 6.0), 2200), ((-5.5, 2.5, 4.0), 1100), ((0.5, -6.5, 3.5), 1100)):
        bpy.ops.object.light_add(type="AREA", location=loc)
        l = bpy.context.active_object
        l.data.energy, l.data.size = en, 4.5
        l.rotation_euler = (tgt - l.location).to_track_quat("-Z", "Y").to_euler()
    bpy.ops.object.camera_add(location=(2.8, 6.6, 4.0))
    cam = bpy.context.active_object
    cam.data.lens = 34.0
    cam.rotation_euler = (tgt - cam.location).to_track_quat("-Z", "Y").to_euler()
    bpy.context.scene.camera = cam
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.samples = 40
    sc.cycles.use_denoising = True
    sc.render.resolution_x, sc.render.resolution_y = 1920, 1080
    sc.render.filepath = str(PREVIEW_OUT)
    bpy.ops.render.render(write_still=True)
    print(f"[OK] Rendered {PREVIEW_OUT}")


def main() -> None:
    addon_utils.enable("io_scene_edm", default_set=True)
    SHAPES_DIR.mkdir(parents=True, exist_ok=True)
    bpy.context.scene.frame_start = 0
    bpy.context.scene.frame_end = 200
    for name, theme, bbox, fn in AAMS:
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
    render_showcase()


if __name__ == "__main__":
    main()
