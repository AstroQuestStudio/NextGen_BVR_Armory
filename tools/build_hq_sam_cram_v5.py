"""Blender 5.2 AAA Hard-Surface Rebuild of Ground Air Defenses (C-RAM, Iron Dome 5x4, EL/M-2084, IRIS-T SLM 8x8, TRML-4D,
SAMP/T, Pantsir-SM, Patriot M903, THAAD HEMTT, S-400 5P85SM2, KEKA Spaceport Pad) + Tomahawk/THAAD/40N6/GMLRS Missiles.
All built natively +X Forward, +Z Up for DCS World EDM with proper connectors and DrawArgs 0, 1, 11, 23, 25.
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
OUT_DIR = Path(r"C:\Users\trufa\.gemini\antigravity\brain\d63eda09-3e0f-4368-acac-466f620a5bd4")
PREVIEW_HQ_SAM = OUT_DIR / "preview_hq_sam_v5.png"
PREVIEW_HQ_CLOSEUP = OUT_DIR / "preview_hq_cram_irondome_closeup.png"

# UV Zone Presets for the 2K Vehicle Atlas (gen_sam_textures_v5.py)
UV_HULL    = (0.04, 0.46, 0.54, 0.96)
UV_RADOME  = (0.52, 0.73, 0.54, 0.96)
UV_AESA    = (0.77, 0.98, 0.54, 0.96)
UV_TREAD   = (0.02, 0.23, 0.04, 0.46)
UV_RIM     = (0.26, 0.48, 0.26, 0.48)
UV_METAL   = (0.52, 0.72, 0.28, 0.40)
UV_AMMO    = (0.52, 0.72, 0.42, 0.49)
UV_GLASS   = (0.78, 0.96, 0.28, 0.46)
UV_LOUVER  = (0.52, 0.72, 0.02, 0.22)
UV_HAZARD  = (0.78, 0.98, 0.02, 0.14)
UV_LIGHT   = (0.78, 0.86, 0.18, 0.24)


def clear_scene() -> None:
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for col in (bpy.data.meshes, bpy.data.materials, bpy.data.actions):
        for item in list(col):
            if item.users == 0:
                col.remove(item)


def load_theme_images(theme: str):
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
    a, n, r = load_theme_images(theme)
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
    a, n, r = load_theme_images(theme)
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
    key_euler(emp, action_name, [(0, (0, 0, -math.pi)), (50, (0, 0, -math.pi * 0.5)), (100, (0, 0, 0)), (150, (0, 0, math.pi * 0.5)), (200, (0, 0, math.pi))])


def add_gun_elevation(emp: bpy.types.Object, action_name: str, min_deg: float = -15.0, max_deg: float = 85.0) -> None:
    key_euler(emp, action_name, [(0, (0, math.radians(-min_deg), 0)), (100, (0, 0, 0)), (200, (0, math.radians(-max_deg), 0))])


def map_face_uv(f: bmesh.types.BMFace, uv, zone: tuple[float, float, float, float]) -> None:
    u0, u1, v0, v1 = zone
    coords = [(u0, v0), (u1, v0), (u1, v1), (u0, v1)]
    for i, lp in enumerate(f.loops):
        lp[uv].uv = coords[i % 4]


def add_bevel_box(bm: bmesh.types.BMesh, uv, center: tuple[float, float, float], size: tuple[float, float, float], zone=UV_HULL, rot_euler=(0.0, 0.0, 0.0), bevel: float = 0.025) -> None:
    ret = bmesh.ops.create_cube(bm, size=1.0)
    verts = ret["verts"]
    for v in verts:
        v.co.x *= size[0]
        v.co.y *= size[1]
        v.co.z *= size[2]
    edges = list({e for v in verts for e in v.link_edges})
    if bevel > 0.002 and min(size) > bevel * 2.5:
        bres = bmesh.ops.bevel(bm, geom=edges, offset=bevel, segments=1, affect="EDGES")
        bverts = list({v for f in bres["faces"] for v in f.verts} | set(verts))
    else:
        bverts = verts
    # Remove orphaned
    valid_verts = [v for v in bverts if v.is_valid]
    m = Matrix.Translation(center) @ Euler(rot_euler, "XYZ").to_matrix().to_4x4()
    for v in valid_verts:
        v.co = m @ v.co
    for f in bm.faces:
        if any(v in valid_verts for v in f.verts):
            if any(lp[uv].uv.length == 0 for lp in f.loops):
                map_face_uv(f, uv, zone)


def add_cyl(bm: bmesh.types.BMesh, uv, p0: Vector, p1: Vector, r0: float, r1: float | None = None, segs: int = 20, zone=UV_HULL, smooth: bool = True) -> None:
    if r1 is None:
        r1 = r0
    axis = (p1 - p0).normalized()
    ref = Vector((0, 0, 1)) if abs(axis.z) < 0.9 else Vector((1, 0, 0))
    u = axis.cross(ref).normalized()
    w = axis.cross(u).normalized()
    ring0 = [bm.verts.new(p0 + (u * math.cos(2 * math.pi * i / segs) + w * math.sin(2 * math.pi * i / segs)) * r0) for i in range(segs)]
    ring1 = [bm.verts.new(p1 + (u * math.cos(2 * math.pi * i / segs) + w * math.sin(2 * math.pi * i / segs)) * r1) for i in range(segs)]
    u0, u1, v0, v1 = zone
    for i in range(segs):
        ni = (i + 1) % segs
        f = bm.faces.new((ring0[i], ring0[ni], ring1[ni], ring1[i]))
        f.smooth = smooth
        ua = u0 + (i / segs) * (u1 - u0)
        ub = u0 + ((i + 1) / segs) * (u1 - u0)
        for lp, uvc in zip(f.loops, ((ua, v0), (ub, v0), (ub, v1), (ua, v1))):
            lp[uv].uv = uvc
    for f in (bm.faces.new(list(reversed(ring0))), bm.faces.new(ring1)):
        map_face_uv(f, uv, zone)


def add_strut(bm: bmesh.types.BMesh, uv, p0: tuple[float, float, float], p1: tuple[float, float, float], radius: float = 0.04, zone=UV_METAL) -> None:
    add_cyl(bm, uv, Vector(p0), Vector(p1), radius, radius, 10, zone, True)


def add_wheel_hq(bm: bmesh.types.BMesh, uv, x: float, y: float, z_hub: float, radius: float = 0.56, width: float = 0.36) -> None:
    """Detailed off-road military tire with beveled shoulder, recessed steel dish rim & hub cap."""
    hw = width * 0.5
    segs = 24
    # Profile across Y: outer sidewall -> shoulder -> tread -> shoulder -> inner sidewall -> rim dish
    prof = [
        (y - hw * 0.85, radius * 0.86),
        (y - hw,        radius),
        (y + hw,        radius),
        (y + hw * 0.85, radius * 0.86),
    ]
    rings = [[bm.verts.new((x + r * math.cos(2 * math.pi * i / segs), yy, z_hub + r * math.sin(2 * math.pi * i / segs))) for i in range(segs)] for yy, r in prof]
    u0, u1, v0, v1 = UV_TREAD
    for k in range(len(rings) - 1):
        r0, r1 = rings[k], rings[k + 1]
        for i in range(segs):
            ni = (i + 1) % segs
            f = bm.faces.new((r0[i], r0[ni], r1[ni], r1[i]))
            f.smooth = True
            va = v0 + (i / segs) * (v1 - v0)
            vb = v0 + ((i + 1) / segs) * (v1 - v0)
            for lp, uvc in zip(f.loops, ((u0, va), (u0, vb), (u1, vb), (u1, va))):
                lp[uv].uv = uvc
    # Steel dish rim & hub cap mapped circularly to UV_RIM (black rubber outer sidewall + center bolted dish!)
    u0, u1, v0, v1 = UV_RIM
    uc, vc = 0.5 * (u0 + u1), 0.5 * (v0 + v1)
    ur, vr = 0.46 * (u1 - u0), 0.46 * (v1 - v0)
    for sign, r_face in ((-1, rings[0]), (1, rings[-1])):
        add_cyl(bm, uv, Vector((x, y + sign * hw * 0.84, z_hub)), Vector((x, y + sign * hw * 0.62, z_hub)), radius * 0.56, radius * 0.50, 20, UV_RIM, True)
        add_cyl(bm, uv, Vector((x, y + sign * hw * 0.62, z_hub)), Vector((x, y + sign * hw * 0.96, z_hub)), radius * 0.24, radius * 0.20, 14, UV_METAL, True)
        f_cap = bm.faces.new(list(reversed(r_face)) if sign < 0 else r_face)
        for lp in f_cap.loops:
            dx = (lp.vert.co.x - x) / max(0.01, radius)
            dz = (lp.vert.co.z - z_hub) / max(0.01, radius)
            lp[uv].uv = (uc + dx * ur, vc + dz * vr)


def add_heavy_8x8_truck(bm: bmesh.types.BMesh, uv, length: float = 8.8, width: float = 2.52, wheel_xs=(3.2, 1.45, -1.85, -3.35), twin_cab: bool = False) -> None:
    """Shared AAA 8x8 MAN HX / KamAZ / HEMTT / MAZ chassis with frame rails, cab glass, headlights, fenders & jacks."""
    # Twin longitudinal I-beam rails + crossmembers
    for ry in (-0.52, 0.52):
        add_bevel_box(bm, uv, (0.0, ry, 0.92), (length, 0.18, 0.28), UV_METAL, bevel=0.02)
    add_bevel_box(bm, uv, (0.0, 0.0, 1.08), (length * 0.96, width * 0.78, 0.14), UV_HULL, bevel=0.02)
    # Heavy front bumper + tow hooks + headlights
    bx = length * 0.50 + 0.08
    add_bevel_box(bm, uv, (bx, 0.0, 0.92), (0.28, width * 0.96, 0.34), UV_METAL, bevel=0.03)
    for ly in (-width * 0.36, width * 0.36):
        add_bevel_box(bm, uv, (bx + 0.14, ly, 0.92), (0.04, 0.22, 0.14), UV_LIGHT, bevel=0.0)
        add_bevel_box(bm, uv, (-length * 0.50 - 0.02, ly, 0.92), (0.04, 0.20, 0.12), UV_HAZARD, bevel=0.0)
    # Cab geometry
    cx = length * 0.36
    if twin_cab:
        # S-400 MAZ/BAZ twin side-by-side nose cabs separated by central cooling grille!
        for sy in (-0.72, 0.72):
            add_bevel_box(bm, uv, (cx, sy, 1.85), (2.30, 0.88, 1.45), UV_HULL, bevel=0.06)
            add_bevel_box(bm, uv, (cx + 1.15, sy, 2.08), (0.05, 0.68, 0.52), UV_GLASS, rot_euler=(0, math.radians(-10), 0), bevel=0.0)
        add_bevel_box(bm, uv, (cx + 0.15, 0.0, 1.68), (1.95, 0.54, 1.05), UV_LOUVER, bevel=0.04)
    else:
        # Modern armored MAN HX / KamAZ / HEMTT cabover with sloped armored windshield + radiator grille + roof hatch
        add_bevel_box(bm, uv, (cx, 0.0, 1.88), (2.25, width * 0.94, 1.48), UV_HULL, bevel=0.08)
        # Windshield upper sloped nose
        add_bevel_box(bm, uv, (cx + 1.06, 0.0, 2.18), (0.14, width * 0.82, 0.52), UV_GLASS, rot_euler=(0, math.radians(-14), 0), bevel=0.01)
        # Front radiator cooling louvers
        add_bevel_box(bm, uv, (cx + 1.13, 0.0, 1.54), (0.05, width * 0.58, 0.42), UV_LOUVER, bevel=0.01)
        # Side cab windows + mirror arms + twin roof hatches
        for sy in (-1.0, 1.0):
            add_bevel_box(bm, uv, (cx + 0.18, sy * (width * 0.47), 2.16), (0.85, 0.04, 0.46), UV_GLASS, bevel=0.0)
            add_bevel_box(bm, uv, (cx + 0.92, sy * (width * 0.55), 2.04), (0.12, 0.16, 0.34), UV_METAL, bevel=0.01)
        add_bevel_box(bm, uv, (cx - 0.15, 0.35, 2.65), (0.55, 0.55, 0.08), UV_HULL, bevel=0.01)
    # 8 Wheels + Wheel-arch Mudguards + Axles
    for wx in wheel_xs:
        add_cyl(bm, uv, Vector((wx, -width * 0.42, 0.56)), Vector((wx, width * 0.42, 0.56)), 0.12, 0.12, 12, UV_METAL, True)
        for wy in (-width * 0.45, width * 0.45):
            add_wheel_hq(bm, uv, wx, wy, 0.56, 0.56, 0.36)
            add_bevel_box(bm, uv, (wx, wy, 1.18), (1.28, 0.42, 0.06), UV_HULL, bevel=0.01)
    # 4 Hydraulic stabilizer jacks lowered to ground (z=0.02..1.05)
    for sx in (-length * 0.42, 0.25):
        for sy in (-width * 0.56, width * 0.56):
            add_cyl(bm, uv, Vector((sx, sy, 0.10)), Vector((sx, sy, 1.05)), 0.08, 0.09, 12, UV_METAL, True)
            add_cyl(bm, uv, Vector((sx, sy, 0.02)), Vector((sx, sy, 0.10)), 0.24, 0.22, 14, UV_HULL, True)


# =========================================================================
# HQ GROUND AIR DEFENSES (Photo-Faithful Rework!)
# =========================================================================
def g_hq_cram_centurion(mat: bpy.types.Material) -> list[bpy.types.Object]:
    """Photo-faithful Centurion C-RAM from Wikimedia #00, #04, #10, #11:
    Gooseneck step-deck trailer + louvered generator + slotted U-barbette + ammo drum + 20mm link chute + FLIR + R2-D2 dome + A-frame 6-barrel Vulcan."""
    objs = []
    bm_h = bmesh.new()
    uv_h = bm_h.loops.layers.uv.new("UVMap")
    # Step-frame flatbed trailer: raised front gooseneck (-3.1..-1.2, z=1.18) + lower main deck (-1.2..2.7, z=0.82)
    add_bevel_box(bm_h, uv_h, (-2.15, 0.0, 1.18), (2.10, 2.30, 0.22), UV_METAL, bevel=0.02)
    add_bevel_box(bm_h, uv_h, (0.75, 0.0, 0.82), (4.10, 2.38, 0.26), UV_HULL, bevel=0.03)
    # Louvered generator + HVAC chiller cabinets on front & rear decks (#02, #10)
    add_bevel_box(bm_h, uv_h, (-2.10, 0.0, 1.85), (1.65, 1.98, 1.15), UV_HULL, bevel=0.04)
    add_bevel_box(bm_h, uv_h, (-2.10, 1.00, 1.85), (1.15, 0.04, 0.78), UV_LOUVER, bevel=0.01)
    add_bevel_box(bm_h, uv_h, (-2.10, -1.00, 1.85), (1.15, 0.04, 0.78), UV_LOUVER, bevel=0.01)
    add_bevel_box(bm_h, uv_h, (-0.55, 0.0, 1.48), (1.15, 1.92, 1.08), UV_HULL, bevel=0.04)
    # Exhaust stacks
    add_cyl(bm_h, uv_h, Vector((-2.75, 0.72, 2.40)), Vector((-2.75, 0.72, 2.95)), 0.06, 0.06, 12, UV_METAL)
    # Tandem rear wheels (#10) + 4 hydraulic leveling outriggers
    for wx in (-2.55, -1.55):
        for wy in (-1.08, 1.08):
            add_wheel_hq(bm_h, uv_h, wx, wy, 0.46, 0.46, 0.28)
    for sx in (-2.85, 2.45):
        for sy in (-1.38, 1.38):
            add_cyl(bm_h, uv_h, Vector((sx, sy, 0.08)), Vector((sx, sy, 0.92)), 0.07, 0.08, 12, UV_METAL)
            add_cyl(bm_h, uv_h, Vector((sx, sy, 0.02)), Vector((sx, sy, 0.08)), 0.22, 0.20, 14, UV_HULL)
    objs.append(make_obj("CRAM_StepTrailer", bm_h, mat))

    # Turret Azimuth (Arg 0) + Center Connector
    emp_az = make_empty("Empty_CRAM_Az", (1.35, 0.0, 0.96))
    add_turret_azimuth(emp_az, "0_CRAM_Az")
    objs.append(emp_az)
    objs.append(make_empty("CENTER_TOWER", (1.35, 0.0, 0.96), special_type="CONNECTOR"))

    # Ribbed & Slotted U-Barbette + Cylindrical 20mm Ammo Drum (#00, #04)
    bm_b = bmesh.new()
    uv_b = bm_b.loops.layers.uv.new("UVMap")
    add_cyl(bm_b, uv_b, Vector((0, 0, 0)), Vector((0, 0, 0.36)), 0.88, 0.84, 28, UV_HULL)
    # Slotted twin side arms built from front/rear vertical posts + cross rungs (#04!)
    for sy in (-0.64, 0.64):
        add_bevel_box(bm_b, uv_b, (0.26, sy, 0.82), (0.24, 0.24, 1.02), UV_HULL, bevel=0.02)
        add_bevel_box(bm_b, uv_b, (-0.24, sy, 0.82), (0.24, 0.24, 1.02), UV_HULL, bevel=0.02)
        add_bevel_box(bm_b, uv_b, (0.0, sy, 1.24), (0.76, 0.24, 0.22), UV_HULL, bevel=0.02)
        add_bevel_box(bm_b, uv_b, (0.0, sy, 0.44), (0.76, 0.24, 0.18), UV_HULL, bevel=0.02)
    # Rear electronics cabinet & under-cradle cylindrical ammo drum
    add_bevel_box(bm_b, uv_b, (-0.54, 0.0, 0.72), (0.42, 1.08, 0.86), UV_HULL, bevel=0.03)
    add_cyl(bm_b, uv_b, Vector((0.18, -0.34, 0.56)), Vector((0.18, 0.34, 0.56)), 0.32, 0.32, 20, UV_METAL)
    objs.append(make_obj("CRAM_SlottedBarbette", bm_b, mat, parent=emp_az))

    # Elevating Cradle (Arg 1): White R2-D2 Ku-band dome, FLIR pod, 20mm curved feed chute, A-frame cradle (#00, #04)
    emp_el = make_empty("Empty_CRAM_El", (0.0, 0.0, 1.16), parent=emp_az)
    add_gun_elevation(emp_el, "1_CRAM_El", -15.0, 85.0)
    objs.append(emp_el)

    bm_c = bmesh.new()
    uv_c = bm_c.loops.layers.uv.new("UVMap")
    # Receiver block + underside brass ammo link chute
    add_bevel_box(bm_c, uv_c, (0.14, 0.0, 0.02), (0.96, 0.78, 0.58), UV_METAL, bevel=0.03)
    add_bevel_box(bm_c, uv_c, (0.42, -0.26, -0.36), (0.42, 0.18, 0.44), UV_AMMO, rot_euler=(0.35, 0.2, 0), bevel=0.01)
    # Iconic R2-D2 white radome cylinder + dark sealing collar + stepped dome (#00, #04)
    add_cyl(bm_c, uv_c, Vector((0.02, 0, 0.24)), Vector((0.02, 0, 0.34)), 0.49, 0.47, 28, UV_METAL)
    add_cyl(bm_c, uv_c, Vector((0.02, 0, 0.34)), Vector((0.02, 0, 1.50)), 0.45, 0.44, 28, UV_RADOME)
    ret_s = bmesh.ops.create_uvsphere(bm_c, u_segments=28, v_segments=14, radius=0.45)
    for v in ret_s["verts"]:
        v.co += Vector((0.02, 0.0, 1.50))
    for f in bm_c.faces:
        if all(v.co.z > 1.48 for v in f.verts):
            f.smooth = True
            map_face_uv(f, uv_c, UV_RADOME)
    # Forward-right FLIR optronic box + glass aperture (#00, #06)
    add_bevel_box(bm_c, uv_c, (0.58, 0.44, 0.46), (0.52, 0.34, 0.42), UV_RADOME, bevel=0.02)
    add_cyl(bm_c, uv_c, Vector((0.84, 0.44, 0.46)), Vector((0.90, 0.44, 0.46)), 0.12, 0.11, 16, UV_GLASS)
    # Triangle steel tubular gun cradle A-frame (#00, #04)
    for sy in (-0.28, 0.28):
        add_strut(bm_c, uv_c, (0.55, sy, 0.24), (1.92, sy * 0.42, 0.05), 0.032, UV_METAL)
        add_strut(bm_c, uv_c, (0.55, sy, -0.24), (1.92, sy * 0.42, -0.09), 0.032, UV_METAL)
    objs.append(make_obj("CRAM_RadomeAndCradle", bm_c, mat, parent=emp_el))

    # Spinning 6-barrel 20mm Vulcan (Arg 23)
    emp_sp = make_empty("Empty_CRAM_Spin", (0.56, 0.0, -0.02), parent=emp_el)
    key_euler(emp_sp, "23_CRAM_Spin", [(100, (0, 0, 0)), (150, (math.pi, 0, 0)), (200, (2 * math.pi, 0, 0))])
    objs.append(emp_sp)

    bm_g = bmesh.new()
    uv_g = bm_g.loops.layers.uv.new("UVMap")
    for k in range(6):
        ang = k * (math.pi / 3.0)
        add_cyl(bm_g, uv_g, Vector((0.0, 0.062 * math.cos(ang), 0.062 * math.sin(ang))), Vector((2.05, 0.062 * math.cos(ang), 0.062 * math.sin(ang))), 0.017, 0.016, 10, UV_METAL)
    for cx in (0.45, 1.35, 1.88):
        add_cyl(bm_g, uv_g, Vector((cx, 0, 0)), Vector((cx + 0.09, 0, 0)), 0.098, 0.098, 18, UV_METAL)
    objs.append(make_obj("CRAM_6Barrels", bm_g, mat, parent=emp_sp))

    objs.append(make_empty("POINT_GUN_01", (2.64, 0.0, -0.02), parent=emp_el, special_type="CONNECTOR"))
    objs.append(make_empty("POINT_SIGHT_01", (0.92, 0.44, 0.46), parent=emp_el, special_type="CONNECTOR"))
    return objs


def g_hq_iron_dome_ln(mat: bpy.types.Material) -> list[bpy.types.Object]:
    """Photo-faithful Iron Dome 20-Cell MFR Launcher from #00, #01, #03, #04:
    Flat open I-beam frame + 4 corner jacks + rear generator + tall folding mast + tilting 5x4 corrugated cell cage."""
    objs = []
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    # Open I-beam skid platform + cross ribs + 4 corner hydraulic jack pads
    for sy in (-1.12, 1.12):
        add_bevel_box(bm, uv, (0.0, sy, 0.36), (4.90, 0.22, 0.24), UV_HULL, bevel=0.02)
    for sx in (-2.2, -0.8, 0.8, 2.2):
        add_bevel_box(bm, uv, (sx, 0.0, 0.36), (0.20, 2.28, 0.20), UV_HULL, bevel=0.02)
        for sy in (-1.28, 1.28):
            if sx in (-2.2, 2.2):
                add_cyl(bm, uv, Vector((sx, sy, 0.08)), Vector((sx, sy, 0.68)), 0.08, 0.09, 12, UV_METAL)
                add_cyl(bm, uv, Vector((sx, sy, 0.02)), Vector((sx, sy, 0.08)), 0.22, 0.20, 14, UV_HULL)
    # Rear generator & electronics cabinet + tall mast antenna (#03!)
    add_bevel_box(bm, uv, (-1.65, 0.0, 1.05), (1.10, 1.96, 1.18), UV_HULL, bevel=0.04)
    add_bevel_box(bm, uv, (-1.65, 0.99, 1.05), (0.72, 0.04, 0.74), UV_LOUVER, bevel=0.01)
    add_cyl(bm, uv, Vector((-1.95, -0.78, 1.62)), Vector((-1.95, -0.78, 4.95)), 0.045, 0.025, 10, UV_METAL)
    objs.append(make_obj("IDome_SkidChassis", bm, mat))

    emp_az = make_empty("Empty_IDome_Az", (0.55, 0.0, 0.48))
    add_turret_azimuth(emp_az, "0_IDome_Az")
    objs.append(emp_az)
    objs.append(make_empty("CENTER_TOWER", (0.55, 0.0, 0.48), special_type="CONNECTOR"))

    # A-frame tilt trunnion stanchions + hydraulic lift rams + Elevated 5x4 Rectangular Corrugated Cage (#00, #03)
    bm_tr = bmesh.new()
    uv_tr = bm_tr.loops.layers.uv.new("UVMap")
    for sy in (-1.12, 1.12):
        add_strut(bm_tr, uv_tr, (-0.55, sy, 0.0), (0.0, sy, 1.48), 0.085, UV_HULL)
        add_strut(bm_tr, uv_tr, (0.55, sy, 0.0), (0.0, sy, 1.48), 0.085, UV_HULL)
        add_strut(bm_tr, uv_tr, (-0.95, sy * 0.85, 0.05), (-0.18, sy * 0.85, 1.15), 0.055, UV_METAL)
    objs.append(make_obj("IDome_TrunnionRams", bm_tr, mat, parent=emp_az))

    emp_el = make_empty("Empty_IDome_Pod", (0.0, 0.0, 1.48), rotation_euler=(0.0, math.radians(-58.0), 0.0), parent=emp_az)
    objs.append(emp_el)

    bm_pod = bmesh.new()
    uv_p = bm_pod.loops.layers.uv.new("UVMap")
    # Outer ribbed rectangular box frame with recessed open cell lattice front/rear!
    for sz in (-0.86, 0.86):
        add_bevel_box(bm_pod, uv_p, (0.0, 0.0, sz), (2.45, 2.26, 0.10), UV_HULL, bevel=0.015)
    for sy in (-1.08, 1.08):
        add_bevel_box(bm_pod, uv_p, (0.0, sy, 0.0), (2.45, 0.10, 1.78), UV_HULL, bevel=0.015)
    # 3 Circumferential stiffening ribs around pod (#00, #03)
    for rx in (-0.95, 0.0, 0.95):
        add_bevel_box(bm_pod, uv_p, (rx, 0.0, 0.0), (0.14, 2.34, 1.88), UV_HULL, bevel=0.02)
    # Internal horizontal/vertical cell dividers + 20 recessed square dark throats + missile caps
    for r_i in range(5):
        zz = (r_i - 2) * 0.42
        add_bevel_box(bm_pod, uv_p, (0.0, 0.0, zz), (2.42, 2.18, 0.045), UV_METAL, bevel=0.0)
    for c_i in range(6):
        yy = (c_i - 2.5) * 0.42
        add_bevel_box(bm_pod, uv_p, (0.0, yy, 0.0), (2.42, 0.045, 1.72), UV_METAL, bevel=0.0)
    idx = 0
    for row in range(4):
        for col in range(5):
            idx += 1
            yy = (col - 2) * 0.42
            zz = (row - 1.5) * 0.42
            add_cyl(bm_pod, uv_p, Vector((-1.18, yy, zz)), Vector((1.16, yy, zz)), 0.155, 0.155, 16, UV_HULL)
            add_cyl(bm_pod, uv_p, Vector((1.16, yy, zz)), Vector((1.24, yy, zz)), 0.135, 0.115, 14, UV_RADOME)
            objs.append(make_empty(f"POINT_MISSILE_{idx:02d}", (1.30, yy, zz), parent=emp_el, special_type="CONNECTOR"))
    objs.append(make_obj("IDome_5x4Cage", bm_pod, mat, parent=emp_el))
    objs.append(make_empty("POINT_SIGHT_01", (1.32, 0.0, 0.95), parent=emp_el, special_type="CONNECTOR"))
    return objs


def g_hq_iron_dome_radar(mat: bpy.types.Material) -> list[bpy.types.Object]:
    """EL/M-2084 MMR Radar on heavy 4-leg tandem flatbed trailer (#10, #13)."""
    objs = []
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    add_bevel_box(bm, uv, (0.0, 0.0, 0.95), (6.60, 2.38, 0.28), UV_HULL, bevel=0.03)
    add_bevel_box(bm, uv, (-2.15, 0.0, 1.72), (1.85, 2.10, 1.25), UV_HULL, bevel=0.04)
    add_bevel_box(bm, uv, (-2.15, 1.06, 1.72), (1.20, 0.04, 0.80), UV_LOUVER, bevel=0.01)
    for wx in (2.25, 1.10, -2.25):
        for wy in (-1.08, 1.08):
            add_wheel_hq(bm, uv, wx, wy, 0.50, 0.50, 0.30)
    for sx in (-2.9, 2.9):
        for sy in (-1.35, 1.35):
            add_cyl(bm, uv, Vector((sx, sy, 0.08)), Vector((sx, sy, 0.95)), 0.07, 0.08, 12, UV_METAL)
            add_cyl(bm, uv, Vector((sx, sy, 0.02)), Vector((sx, sy, 0.08)), 0.22, 0.20, 14, UV_HULL)
    objs.append(make_obj("MMR_Trailer", bm, mat))

    emp_rot = make_empty("Empty_MMR_Rot", (0.45, 0.0, 1.15))
    key_euler(emp_rot, "11_MMR_Rot", [(100, (0, 0, 0)), (150, (0, 0, math.pi)), (200, (0, 0, 2 * math.pi))])
    objs.append(emp_rot)

    bm_a = bmesh.new()
    uv_a = bm_a.loops.layers.uv.new("UVMap")
    add_cyl(bm_a, uv_a, Vector((0, 0, 0)), Vector((0, 0, 1.15)), 0.55, 0.48, 24, UV_METAL)
    add_bevel_box(bm_a, uv_a, (-0.35, 0.0, 1.45), (0.95, 1.45, 0.95), UV_HULL, bevel=0.03)
    # Tilted broad S-Band AESA array + recessed front dipole face
    add_bevel_box(bm_a, uv_a, (0.28, 0.0, 2.35), (0.42, 2.65, 2.35), UV_HULL, rot_euler=(0, math.radians(-18), 0), bevel=0.08)
    add_bevel_box(bm_a, uv_a, (0.48, 0.0, 2.42), (0.08, 2.38, 2.08), UV_AESA, rot_euler=(0, math.radians(-18), 0), bevel=0.02)
    objs.append(make_obj("MMR_AESAPanel", bm_a, mat, parent=emp_rot))
    return objs


def g_hq_irist_slm_ln(mat: bpy.types.Material) -> list[bpy.types.Object]:
    """Photo-faithful Diehl IRIS-T SLM 8-Cell Square Ribbed Vertical Launcher on MAN HX 8x8 (#01, #02, #03)."""
    objs = []
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    add_heavy_8x8_truck(bm, uv, 8.80, 2.52, (3.15, 1.45, -1.75, -3.25))
    # Mid-deck generator & comms shelter + twin tall dipole masts (#02, #03!)
    add_bevel_box(bm, uv, (0.15, 0.0, 1.85), (2.75, 2.25, 1.38), UV_HULL, bevel=0.04)
    add_bevel_box(bm, uv, (0.15, 1.14, 1.85), (1.45, 0.04, 0.78), UV_LOUVER, bevel=0.01)
    for my in (-0.85, 0.85):
        add_cyl(bm, uv, Vector((0.85, my, 2.50)), Vector((0.85, my, 5.85)), 0.045, 0.028, 10, UV_METAL)
        add_cyl(bm, uv, Vector((0.85, my, 5.85)), Vector((0.85, my, 6.25)), 0.14, 0.14, 14, UV_RADOME)
    objs.append(make_obj("IRIST_MAN_HX", bm, mat))

    emp_tur = make_empty("Empty_IRIST_VLS", (-2.65, 0.0, 1.25))
    objs.append(emp_tur)
    objs.append(make_empty("CENTER_TOWER", (-2.65, 0.0, 1.25), special_type="CONNECTOR"))

    bm_v = bmesh.new()
    uv_v = bm_v.loops.layers.uv.new("UVMap")
    # Blast-deflector base box + 8 SQUARE ribbed canisters (2 rows x 4 cols)
    add_bevel_box(bm_v, uv_v, (0.0, 0.0, 0.45), (1.35, 2.40, 0.85), UV_METAL, bevel=0.03)
    idx = 0
    for c in range(2):
        for r in range(4):
            idx += 1
            xx = (c - 0.5) * 0.56
            yy = (r - 1.5) * 0.56
            add_bevel_box(bm_v, uv_v, (xx, yy, 2.55), (0.48, 0.48, 4.45), UV_HULL, bevel=0.025)
            for rz in (1.15, 2.25, 3.35, 4.45):
                add_bevel_box(bm_v, uv_v, (xx, yy, rz), (0.52, 0.52, 0.08), UV_METAL, bevel=0.01)
            add_bevel_box(bm_v, uv_v, (xx, yy, 4.80), (0.42, 0.42, 0.06), UV_AESA, bevel=0.01)
            objs.append(make_empty(f"POINT_MISSILE_{idx:02d}", (xx, yy, 4.86), rotation_euler=(0.0, math.radians(-90.0), 0.0), parent=emp_tur, special_type="CONNECTOR"))
    objs.append(make_obj("IRIST_8SquareVLS", bm_v, mat, parent=emp_tur))
    objs.append(make_empty("POINT_SIGHT_01", (1.2, 0.0, 3.2), special_type="CONNECTOR"))
    return objs


def g_hq_trml_4d_radar(mat: bpy.types.Material) -> list[bpy.types.Object]:
    """Hensoldt TRML-4D AESA Radar on MAN HX 8x8 (#05, #06, #07)."""
    objs = []
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    add_heavy_8x8_truck(bm, uv, 8.80, 2.52, (3.15, 1.45, -1.75, -3.25))
    add_bevel_box(bm, uv, (-0.85, 0.0, 1.88), (4.65, 2.30, 1.48), UV_HULL, bevel=0.04)
    add_bevel_box(bm, uv, (-0.85, 1.16, 1.88), (2.20, 0.04, 0.84), UV_LOUVER, bevel=0.01)
    objs.append(make_obj("TRML_MAN_HX", bm, mat))

    emp_rot = make_empty("Empty_TRML_Rot", (-1.55, 0.0, 2.85))
    key_euler(emp_rot, "11_TRML_Rot", [(100, (0, 0, 0)), (150, (0, 0, math.pi)), (200, (0, 0, 2 * math.pi))])
    objs.append(emp_rot)

    bm_r = bmesh.new()
    uv_r = bm_r.loops.layers.uv.new("UVMap")
    add_bevel_box(bm_r, uv_r, (-0.25, 0.0, 0.72), (1.35, 1.25, 1.25), UV_HULL, bevel=0.04)
    add_bevel_box(bm_r, uv_r, (0.28, 0.0, 2.25), (0.48, 2.15, 1.95), UV_HULL, rot_euler=(0, math.radians(-16), 0), bevel=0.06)
    add_bevel_box(bm_r, uv_r, (0.50, 0.0, 2.30), (0.08, 1.92, 1.72), UV_AESA, rot_euler=(0, math.radians(-16), 0), bevel=0.02)
    objs.append(make_obj("TRML_AESAFace", bm_r, mat, parent=emp_rot))
    return objs


def g_hq_sampt_aster30(mat: bpy.types.Material) -> list[bpy.types.Object]:
    """Eurosam SAMP/T Mamba 8-Cell Vertical Cylindrical Launcher on 8x8 Carrier."""
    objs = []
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    add_heavy_8x8_truck(bm, uv, 9.00, 2.52, (3.25, 1.50, -1.80, -3.35))
    add_bevel_box(bm, uv, (0.20, 0.0, 1.82), (2.80, 2.22, 1.32), UV_HULL, bevel=0.04)
    objs.append(make_obj("SAMPT_Chassis", bm, mat))

    emp_tur = make_empty("Empty_SAMPT_VLS", (-2.65, 0.0, 1.25))
    objs.append(emp_tur)
    objs.append(make_empty("CENTER_TOWER", (-2.65, 0.0, 1.25), special_type="CONNECTOR"))

    bm_v = bmesh.new()
    uv_v = bm_v.loops.layers.uv.new("UVMap")
    add_bevel_box(bm_v, uv_v, (0.0, 0.0, 0.45), (1.45, 2.44, 0.85), UV_METAL, bevel=0.03)
    idx = 0
    for c in range(2):
        for r in range(4):
            idx += 1
            xx = (c - 0.5) * 0.62
            yy = (r - 1.5) * 0.60
            add_cyl(bm_v, uv_v, Vector((xx, yy, 0.40)), Vector((xx, yy, 5.45)), 0.25, 0.25, 20, UV_HULL)
            for rz in (1.40, 2.90, 4.40, 5.42):
                add_cyl(bm_v, uv_v, Vector((xx, yy, rz)), Vector((xx, yy, rz + 0.08)), 0.27, 0.27, 20, UV_METAL)
            add_cyl(bm_v, uv_v, Vector((xx, yy, 5.45)), Vector((xx, yy, 5.50)), 0.22, 0.22, 16, UV_AESA)
            objs.append(make_empty(f"POINT_MISSILE_{idx:02d}", (xx, yy, 5.54), rotation_euler=(0.0, math.radians(-90.0), 0.0), parent=emp_tur, special_type="CONNECTOR"))
    objs.append(make_obj("SAMPT_8Cylinders", bm_v, mat, parent=emp_tur))
    objs.append(make_empty("POINT_SIGHT_01", (1.2, 0.0, 3.2), special_type="CONNECTOR"))
    return objs


def g_hq_pantsir_sm(mat: bpy.types.Material) -> list[bpy.types.Object]:
    """Photo-faithful Pantsir-SM 96K6 from #00, #02, #04, #05:
    KamAZ-6560 8x8 + rear twin spare tires + turret with angled tan front tracking radar, Janus top SR, 2x twin 30mm 2A38M guns & 12 tapered 57E6M tubes."""
    objs = []
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    add_heavy_8x8_truck(bm, uv, 9.40, 2.56, (3.40, 1.60, -1.75, -3.30))
    # Twin upright spare tires behind cab (#00, #02)
    add_wheel_hq(bm, uv, 1.50, 0.56, 2.02, 0.54, 0.34)
    add_wheel_hq(bm, uv, 1.50, -0.56, 2.02, 0.54, 0.34)
    # Armored equipment body module
    add_bevel_box(bm, uv, (-1.15, 0.0, 1.85), (4.65, 2.40, 1.32), UV_HULL, bevel=0.04)
    add_bevel_box(bm, uv, (-1.15, 1.21, 1.85), (2.80, 0.04, 0.78), UV_LOUVER, bevel=0.01)
    objs.append(make_obj("Pantsir_KamAZ6560", bm, mat))

    emp_az = make_empty("Empty_Pantsir_Az", (-1.55, 0.0, 2.52))
    add_turret_azimuth(emp_az, "0_Pantsir_Az")
    objs.append(emp_az)
    objs.append(make_empty("CENTER_TOWER", (-1.55, 0.0, 2.52), special_type="CONNECTOR"))

    bm_t = bmesh.new()
    uv_t = bm_t.loops.layers.uv.new("UVMap")
    add_bevel_box(bm_t, uv_t, (0.0, 0.0, 0.72), (2.35, 1.68, 1.40), UV_HULL, bevel=0.06)
    # Iconic inclined circular tan tracking phased-array radar dome on turret front (#02, #04!)
    add_cyl(bm_t, uv_t, Vector((1.05, 0.0, 0.85)), Vector((1.42, 0.0, 1.05)), 0.52, 0.50, 28, UV_RADOME)
    # EO/IR sight ball beside trunnion
    add_cyl(bm_t, uv_t, Vector((0.88, 0.62, 1.38)), Vector((1.12, 0.62, 1.38)), 0.22, 0.20, 18, UV_GLASS)
    objs.append(make_obj("Pantsir_Turret", bm_t, mat, parent=emp_az))

    # Top Janus dual-sided S-band Search Radar (Arg 11)
    emp_sr = make_empty("Empty_Pantsir_SR", (-0.65, 0.0, 1.56), parent=emp_az)
    key_euler(emp_sr, "11_Pantsir_SR", [(100, (0, 0, 0)), (150, (0, 0, math.pi)), (200, (0, 0, 2 * math.pi))])
    objs.append(emp_sr)
    bm_sr = bmesh.new()
    uv_sr = bm_sr.loops.layers.uv.new("UVMap")
    add_cyl(bm_sr, uv_sr, Vector((0, 0, -0.20)), Vector((0, 0, 0.30)), 0.28, 0.24, 16, UV_METAL)
    add_bevel_box(bm_sr, uv_sr, (0.0, 0.0, 0.62), (0.38, 2.05, 0.85), UV_AESA, rot_euler=(0, math.radians(-12), 0), bevel=0.04)
    objs.append(make_obj("Pantsir_JanusSR", bm_sr, mat, parent=emp_sr))

    # Elevating Weapon Arms (Arg 1): 12x 57E6M tubes + Twin-Barrel 30mm 2A38M guns (#04)
    emp_el = make_empty("Empty_Pantsir_El", (0.15, 0.0, 0.82), parent=emp_az)
    add_gun_elevation(emp_el, "1_Pantsir_El", -5.0, 82.0)
    objs.append(emp_el)

    bm_ar = bmesh.new()
    uv_ar = bm_ar.loops.layers.uv.new("UVMap")
    idx = 0
    for side_y in (-1.28, 1.28):
        add_bevel_box(bm_ar, uv_ar, (-0.1, side_y * 0.85, 0.12), (0.95, 0.28, 0.65), UV_METAL, bevel=0.02)
        for r in range(3):
            for c in range(2):
                idx += 1
                yy = side_y + (c - 0.5) * 0.25 * (1 if side_y > 0 else -1)
                zz = (r - 1.0) * 0.27 + 0.30
                add_cyl(bm_ar, uv_ar, Vector((-1.62, yy, zz)), Vector((1.72, yy, zz)), 0.115, 0.105, 16, UV_HULL)
                add_cyl(bm_ar, uv_ar, Vector((1.72, yy, zz)), Vector((1.78, yy, zz)), 0.095, 0.095, 14, UV_RADOME)
                objs.append(make_empty(f"POINT_MISSILE_{idx:02d}", (1.82, yy, zz), parent=emp_el, special_type="CONNECTOR"))
        # Dual 30mm 2A38M barrels + perforated jackets (#04)
        gy = side_y * 0.68
        for gz in (-0.18, -0.04):
            add_cyl(bm_ar, uv_ar, Vector((0.0, gy, gz)), Vector((2.32, gy, gz)), 0.026, 0.022, 12, UV_METAL)
        add_bevel_box(bm_ar, uv_ar, (0.65, gy, -0.11), (0.85, 0.12, 0.26), UV_HULL, bevel=0.01)
    objs.append(make_obj("Pantsir_PodsAnd2A38M", bm_ar, mat, parent=emp_el))
    objs.append(make_empty("POINT_GUN_01", (2.38, -0.87, -0.11), parent=emp_el, special_type="CONNECTOR"))
    objs.append(make_empty("POINT_GUN_02", (2.38, 0.87, -0.11), parent=emp_el, special_type="CONNECTOR"))
    objs.append(make_empty("POINT_SIGHT_01", (1.16, 0.62, 1.38), parent=emp_az, special_type="CONNECTOR"))
    return objs


def g_hq_patriot_pac3(mat: bpy.types.Material) -> list[bpy.types.Object]:
    """Photo-faithful Patriot M903 PAC-3 MSE 16-Cell Quad-Pack from #03, #04, #05."""
    objs = []
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    add_bevel_box(bm, uv, (0.0, 0.0, 0.84), (6.50, 2.48, 0.30), UV_HULL, bevel=0.03)
    add_bevel_box(bm, uv, (2.25, 0.0, 1.48), (1.40, 1.85, 0.98), UV_HULL, bevel=0.04)
    add_bevel_box(bm, uv, (2.25, 0.94, 1.48), (0.95, 0.04, 0.64), UV_LOUVER, bevel=0.01)
    for wx in (-1.55, -2.65):
        for wy in (-1.12, 1.12):
            add_wheel_hq(bm, uv, wx, wy, 0.50, 0.50, 0.30)
    for sx in (-2.95, 2.95):
        for sy in (-1.42, 1.42):
            add_cyl(bm, uv, Vector((sx, sy, 0.08)), Vector((sx, sy, 0.90)), 0.08, 0.09, 12, UV_METAL)
            add_cyl(bm, uv, Vector((sx, sy, 0.02)), Vector((sx, sy, 0.08)), 0.24, 0.22, 14, UV_HULL)
    objs.append(make_obj("Patriot_M903Trailer", bm, mat))

    emp_az = make_empty("Empty_Pat_Az", (-1.10, 0.0, 1.00))
    add_turret_azimuth(emp_az, "0_Pat_Az")
    objs.append(emp_az)
    objs.append(make_empty("CENTER_TOWER", (-1.10, 0.0, 1.00), special_type="CONNECTOR"))

    # Turret base + mast antenna + hydraulic lift rams (#03, #05)
    bm_tr = bmesh.new()
    uv_tr = bm_tr.loops.layers.uv.new("UVMap")
    add_cyl(bm_tr, uv_tr, Vector((0, 0, 0)), Vector((0, 0, 0.42)), 0.82, 0.78, 24, UV_METAL)
    add_cyl(bm_tr, uv_tr, Vector((-0.65, 1.05, 0.2)), Vector((-0.65, 1.05, 4.95)), 0.04, 0.025, 10, UV_METAL)
    for sy in (-0.65, 0.65):
        add_strut(bm_tr, uv_tr, (-0.15, sy, 0.35), (0.35, sy, 2.05), 0.075, UV_METAL)
    objs.append(make_obj("Patriot_LiftFrame", bm_tr, mat, parent=emp_az))

    emp_el = make_empty("Empty_Pat_Pod", (-0.30, 0.0, 2.28), rotation_euler=(0.0, math.radians(-38.0), 0.0), parent=emp_az)
    objs.append(emp_el)
    bm_p = bmesh.new()
    uv_p = bm_p.loops.layers.uv.new("UVMap")
    # 4 Ribbed Rectangular Quad-Pack Canisters + Crosshatch Frangible End-Caps (#03!)
    for c in range(2):
        for r in range(2):
            yy = (c - 0.5) * 1.14
            zz = (r - 0.5) * 0.96
            add_bevel_box(bm_p, uv_p, (0.0, yy, zz), (5.25, 0.96, 0.80), UV_HULL, bevel=0.025)
            for rx in (-2.0, -0.7, 0.7, 2.0):
                add_bevel_box(bm_p, uv_p, (rx, yy, zz), (0.14, 1.02, 0.86), UV_METAL, bevel=0.01)
            add_bevel_box(bm_p, uv_p, (2.64, yy, zz), (0.06, 0.88, 0.72), UV_AESA, bevel=0.01)
    idx = 0
    for c in range(4):
        for r in range(4):
            idx += 1
            objs.append(make_empty(f"POINT_MISSILE_{idx:02d}", (2.70, (c - 1.5) * 0.54, (r - 1.5) * 0.44), parent=emp_el, special_type="CONNECTOR"))
    objs.append(make_obj("Patriot_16CellQuadPack", bm_p, mat, parent=emp_el))
    objs.append(make_empty("POINT_SIGHT_01", (1.2, 0.0, 3.2), parent=emp_az, special_type="CONNECTOR"))
    return objs


def g_hq_thaad_ln(mat: bpy.types.Material) -> list[bpy.types.Object]:
    """Photo-faithful THAAD 8-Tube HEMTT M1120 Launcher from #06, #07, #08."""
    objs = []
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    add_heavy_8x8_truck(bm, uv, 9.60, 2.48, (3.45, 1.75, -1.85, -3.45))
    # Rear pivot trunnion stanchions + twin hydraulic elevating cylinders under rack (#06, #07)
    for sy in (-1.12, 1.12):
        add_bevel_box(bm, uv, (-3.45, sy, 1.48), (0.55, 0.22, 0.72), UV_HULL, bevel=0.02)
        add_strut(bm, uv, (-0.85, sy * 0.75, 1.15), (-2.15, sy * 0.75, 2.85), 0.075, UV_METAL)
    objs.append(make_obj("THAAD_HEMTT", bm, mat))

    emp_tur = make_empty("Empty_THAAD_El", (-3.35, 0.0, 1.65), rotation_euler=(0.0, math.radians(-78.0), 0.0))
    objs.append(emp_tur)
    objs.append(make_empty("CENTER_TOWER", (-3.35, 0.0, 1.65), special_type="CONNECTOR"))

    bm_t = bmesh.new()
    uv_t = bm_t.loops.layers.uv.new("UVMap")
    # Open tan painted steel skeleton truss + 4 transverse tube-clamping bulkheads (#06, #07, #08!)
    for sy in (-1.18, 1.18):
        add_bevel_box(bm_t, uv_t, (2.95, sy, 0.0), (6.10, 0.14, 0.36), UV_HULL, bevel=0.015)
    for cx in (0.15, 1.95, 3.85, 5.65):
        add_bevel_box(bm_t, uv_t, (cx, 0.0, 0.0), (0.18, 2.38, 1.08), UV_HULL, bevel=0.015)
    idx = 0
    for row in range(2):
        for col in range(4):
            idx += 1
            yy = (col - 1.5) * 0.56
            zz = (row - 0.5) * 0.52
            add_cyl(bm_t, uv_t, Vector((0.05, yy, zz)), Vector((6.35, yy, zz)), 0.23, 0.23, 20, UV_HULL)
            add_cyl(bm_t, uv_t, Vector((6.35, yy, zz)), Vector((6.42, yy, zz)), 0.20, 0.20, 16, UV_RADOME)
            objs.append(make_empty(f"POINT_MISSILE_{idx:02d}", (6.46, yy, zz), parent=emp_tur, special_type="CONNECTOR"))
    objs.append(make_obj("THAAD_8TubeRack", bm_t, mat, parent=emp_tur))
    objs.append(make_empty("POINT_SIGHT_01", (2.0, 0.0, 3.0), special_type="CONNECTOR"))
    return objs


def g_hq_s400_tel(mat: bpy.types.Material) -> list[bpy.types.Object]:
    """Photo-faithful S-400 Triumf 5P85SM2 4-Tube Heavy TEL from #09:
    Twin side-by-side cab noses + center grille + 4 huge vertical ribbed olive canisters with red stiffening rings!"""
    objs = []
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    add_heavy_8x8_truck(bm, uv, 10.40, 2.75, (3.85, 1.85, -2.05, -3.75), twin_cab=True)
    add_bevel_box(bm, uv, (-0.85, 0.0, 1.55), (5.60, 2.30, 0.72), UV_HULL, bevel=0.03)
    objs.append(make_obj("S400_MAZ543", bm, mat))

    emp_tur = make_empty("Empty_S400_VLS", (-3.45, 0.0, 1.35))
    objs.append(emp_tur)
    objs.append(make_empty("CENTER_TOWER", (-3.45, 0.0, 1.35), special_type="CONNECTOR"))

    bm_t = bmesh.new()
    uv_t = bm_t.loops.layers.uv.new("UVMap")
    add_bevel_box(bm_t, uv_t, (0.0, 0.0, 0.45), (1.35, 2.65, 0.85), UV_METAL, bevel=0.03)
    for i in range(4):
        yy = (i - 1.5) * 0.70
        add_cyl(bm_t, uv_t, Vector((0.0, yy, 0.20)), Vector((0.0, yy, 7.80)), 0.34, 0.34, 24, UV_HULL)
        for rz in (1.40, 3.20, 5.00, 6.80, 7.65):
            add_cyl(bm_t, uv_t, Vector((0.0, yy, rz)), Vector((0.0, yy, rz + 0.14)), 0.36, 0.36, 24, UV_RADOME)  # Red-ring zone!
        add_cyl(bm_t, uv_t, Vector((0.0, yy, 7.80)), Vector((0.0, yy, 7.86)), 0.30, 0.30, 20, UV_AESA)
        objs.append(make_empty(f"POINT_MISSILE_{i + 1:02d}", (0.0, yy, 7.90), rotation_euler=(0.0, math.radians(-90.0), 0.0), parent=emp_tur, special_type="CONNECTOR"))
    objs.append(make_obj("S400_4Tubes", bm_t, mat, parent=emp_tur))
    objs.append(make_empty("POINT_SIGHT_01", (2.0, 0.0, 3.2), special_type="CONNECTOR"))
    return objs


def g_hq_keka_launcher(mat: bpy.types.Material) -> list[bpy.types.Object]:
    """KEKA Aerospace Savanna Spaceport Mobile Rig (Troll Pad!)."""
    objs = []
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    add_bevel_box(bm, uv, (0.0, 0.0, 0.56), (4.10, 1.95, 0.20), UV_HULL, bevel=0.02)
    add_bevel_box(bm, uv, (-1.15, 0.58, 0.88), (0.72, 0.52, 0.44), UV_HAZARD, bevel=0.02)  # Car battery ignition crate
    add_bevel_box(bm, uv, (-1.15, -0.58, 0.86), (0.68, 0.50, 0.40), UV_LOUVER, bevel=0.02)
    for wy in (-1.02, 1.02):
        add_wheel_hq(bm, uv, -0.45, wy, 0.44, 0.44, 0.28)
    objs.append(make_obj("KEKA_SpaceportTrailer", bm, mat))

    emp_az = make_empty("Empty_KEKA_Az", (0.20, 0.0, 0.68))
    add_turret_azimuth(emp_az, "0_KEKA_Az")
    objs.append(emp_az)
    objs.append(make_empty("CENTER_TOWER", (0.20, 0.0, 0.68), special_type="CONNECTOR"))

    emp_el = make_empty("Empty_KEKA_Boom", (0.0, 0.0, 1.05), rotation_euler=(0.0, math.radians(-58.0), 0.0), parent=emp_az)
    objs.append(emp_el)
    bm_r = bmesh.new()
    uv_r = bm_r.loops.layers.uv.new("UVMap")
    # Welded lattice rail truss + corrugated blast deflector shield + launch shoes
    add_bevel_box(bm_r, uv_r, (0.25, 0.0, 0.0), (4.80, 0.28, 0.16), UV_RADOME, bevel=0.01)
    add_bevel_box(bm_r, uv_r, (-2.25, 0.0, 0.28), (0.08, 0.88, 0.72), UV_LOUVER, bevel=0.01)
    for x0 in (-1.6, -0.4, 0.8, 2.0):
        add_strut(bm_r, uv_r, (x0, -0.14, 0.0), (x0 + 0.6, 0.0, -0.22), 0.03, UV_METAL)
        add_strut(bm_r, uv_r, (x0, 0.14, 0.0), (x0 + 0.6, 0.0, -0.22), 0.03, UV_METAL)
    objs.append(make_obj("KEKA_TrussRail", bm_r, mat, parent=emp_el))
    objs.append(make_empty("POINT_MISSILE_01", (1.65, 0.0, 0.34), parent=emp_el, special_type="CONNECTOR"))
    objs.append(make_empty("POINT_SIGHT_01", (1.20, 0.0, 0.90), parent=emp_el, special_type="CONNECTOR"))
    return objs


# =========================================================================
# NEW BACKLOG & SAM MISSILES (Native +X Forward!)
# =========================================================================
def m_tomahawk_v(mat: bpy.types.Material) -> list[bpy.types.Object]:
    """BGM-109 Tomahawk Block V from #06, #07, #09: hemispherical blunt nose, dorsal/ventral belly turbofan scoop, straight wings (Arg 25) & cruciform tail."""
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    L, r = 6.25, 0.260
    prof = [(-3.12, 0.006), (-3.02, 0.19), (-2.60, r), (2.78, r)]
    for i in range(1, 10):
        a = (i / 10.0) * (math.pi * 0.5)
        prof.append((2.78 + math.sin(a) * 0.34, max(0.006, r * math.cos(a))))
    rings = [[bm.verts.new((x, rad * math.cos(2 * math.pi * i / 32), rad * math.sin(2 * math.pi * i / 32))) for i in range(32)] for x, rad in prof]
    for idx in range(len(rings) - 1):
        r0, r1 = rings[idx], rings[idx + 1]
        for i in range(32):
            ni = (i + 1) % 32
            f = bm.faces.new((r0[i], r0[ni], r1[ni], r1[i])); f.smooth = True
            map_face_uv(f, uv, UV_RADOME if idx >= 3 else UV_HULL)
    bm.faces.new(rings[-1]); bm.faces.new(list(reversed(rings[0])))
    # Ventral turbofan intake scoop (#07, #09)
    add_bevel_box(bm, uv, (-1.85, 0.0, -0.26), (1.15, 0.20, 0.16), UV_METAL, bevel=0.02)
    # 4 Tail fins
    for k in range(4):
        rot = Matrix.Rotation(math.radians(k * 90.0), 3, "X")
        p = [rot @ Vector((-2.45, 0, r * 0.9)), rot @ Vector((-2.85, 0, r + 0.34)), rot @ Vector((-3.08, 0, r + 0.34)), rot @ Vector((-3.00, 0, r * 0.9))]
        vs = [bm.verts.new(pt) for pt in p]
        f = bm.faces.new(vs); map_face_uv(f, uv, UV_HAZARD)
    objs = [make_obj("Tomahawk_Body", bm, mat)]
    # Straight folding mid-wings (DrawArg 25)
    for side, sn in ((-1.0, "L"), (1.0, "R")):
        bm_w = bmesh.new(); uv_w = bm_w.loops.layers.uv.new("UVMap")
        add_bevel_box(bm_w, uv_w, (0.0, side * 0.68, 0.0), (0.34, 1.36, 0.028), UV_RADOME, bevel=0.008)
        w_obj = make_obj(f"Tomahawk_Wing_{sn}", bm_w, mat, location=(0.25, side * 0.18, -0.02))
        key_euler(w_obj, f"25_Tomahawk_Wing_{sn}", [(100, (0, 0, side * math.radians(-86.0))), (200, (0, 0, 0))])
        objs.append(w_obj)
    return objs


def m_sam_thaad(mat: bpy.types.Material) -> list[bpy.types.Object]:
    """Exact THAAD Missile from #09 Blueprint (6.17m): flared tail skirt + booster + stepped cone Kill-Vehicle."""
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    prof = [(-3.08, 0.24), (-2.65, 0.17), (-0.75, 0.17), (0.80, 0.185), (1.35, 0.13), (3.08, 0.015)]
    rings = [[bm.verts.new((x, r * math.cos(2 * math.pi * i / 32), r * math.sin(2 * math.pi * i / 32))) for i in range(32)] for x, r in prof]
    for idx in range(len(rings) - 1):
        r0, r1 = rings[idx], rings[idx + 1]
        for i in range(32):
            ni = (i + 1) % 32
            f = bm.faces.new((r0[i], r0[ni], r1[ni], r1[i])); f.smooth = True
            map_face_uv(f, uv, UV_RADOME if idx >= 3 else UV_HULL)
    bm.faces.new(rings[-1]); bm.faces.new(list(reversed(rings[0])))
    return [make_obj("THAAD_KineticDart", bm, mat)]


def m_sam_40n6(mat: bpy.types.Material) -> list[bpy.types.Object]:
    """Massive 7.5m S-400 40N6 / SM-3 IIA long-range ABM missile."""
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    prof = [(-3.75, 0.22), (-3.65, 0.26), (1.85, 0.26), (2.75, 0.16), (3.75, 0.01)]
    rings = [[bm.verts.new((x, r * math.cos(2 * math.pi * i / 32), r * math.sin(2 * math.pi * i / 32))) for i in range(32)] for x, r in prof]
    for idx in range(len(rings) - 1):
        r0, r1 = rings[idx], rings[idx + 1]
        for i in range(32):
            ni = (i + 1) % 32
            f = bm.faces.new((r0[i], r0[ni], r1[ni], r1[i])); f.smooth = True
            map_face_uv(f, uv, UV_RADOME if idx >= 2 else UV_HULL)
    bm.faces.new(rings[-1]); bm.faces.new(list(reversed(rings[0])))
    for k in range(4):
        rot = Matrix.Rotation(math.radians(45 + k * 90), 3, "X")
        add_bevel_box(bm, uv, tuple(rot @ Vector((-3.30, 0, 0.38))), (0.85, 0.02, 0.42), UV_METAL, rot_euler=(math.radians(45 + k * 90), 0, 0), bevel=0.0)
    return [make_obj("S400_40N6_ABM", bm, mat)]


def m_gmlrs_m31(mat: bpy.types.Material) -> list[bpy.types.Object]:
    """M31A2 / ER-GMLRS Precision Artillery Rocket (3.94m x 0.227m)."""
    bm = bmesh.new()
    uv = bm.loops.layers.uv.new("UVMap")
    prof = [(-1.97, 0.09), (-1.85, 0.114), (1.42, 0.114), (1.85, 0.04), (1.97, 0.008)]
    rings = [[bm.verts.new((x, r * math.cos(2 * math.pi * i / 28), r * math.sin(2 * math.pi * i / 28))) for i in range(28)] for x, r in prof]
    for idx in range(len(rings) - 1):
        r0, r1 = rings[idx], rings[idx + 1]
        for i in range(28):
            ni = (i + 1) % 28
            f = bm.faces.new((r0[i], r0[ni], r1[ni], r1[i])); f.smooth = True
            map_face_uv(f, uv, UV_RADOME if idx >= 2 else UV_HULL)
    bm.faces.new(rings[-1]); bm.faces.new(list(reversed(rings[0])))
    for k in range(4):
        rot = Matrix.Rotation(math.radians(45 + k * 90), 3, "X")
        add_bevel_box(bm, uv, tuple(rot @ Vector((1.22, 0, 0.15))), (0.22, 0.012, 0.10), UV_METAL, rot_euler=(math.radians(45 + k * 90), 0, 0), bevel=0.0)
        add_bevel_box(bm, uv, tuple(rot @ Vector((-1.72, 0, 0.18))), (0.36, 0.014, 0.18), UV_METAL, rot_euler=(math.radians(45 + k * 90), 0, 0), bevel=0.0)
    return [make_obj("GMLRS_M31_Body", bm, mat)]


HQ_MODELS = [
    ("ng_cram_centurion",  "hq_cram",       (7.0, 3.2, 4.8),   g_hq_cram_centurion,   "sam"),
    ("ng_iron_dome_ln",    "hq_irondome",   (5.6, 3.2, 5.2),   g_hq_iron_dome_ln,     "sam"),
    ("ng_iron_dome_radar", "hq_irondome",   (7.2, 3.2, 4.8),   g_hq_iron_dome_radar,  "sam"),
    ("ng_irist_slm_ln",    "hq_nato_sam",   (9.4, 3.0, 6.4),   g_hq_irist_slm_ln,     "sam"),
    ("ng_trml_4d_radar",   "hq_nato_sam",   (9.2, 3.0, 6.0),   g_hq_trml_4d_radar,    "sam"),
    ("ng_sampt_aster30",   "hq_nato_sam",   (9.4, 3.0, 6.4),   g_hq_sampt_aster30,    "sam"),
    ("ng_pantsir_sm",      "hq_russia_sam", (9.8, 3.4, 5.2),   g_hq_pantsir_sm,       "sam"),
    ("ng_patriot_pac3_ln", "hq_nato_sam",   (7.2, 3.2, 5.6),   g_hq_patriot_pac3,     "sam"),
    ("ng_thaad_ln",        "hq_thaad_tan",  (10.0, 3.2, 6.6),  g_hq_thaad_ln,         "sam"),
    ("ng_s400_tel",        "hq_russia_sam", (10.8, 3.4, 8.2),  g_hq_s400_tel,         "sam"),
    ("ng_keka_launcher",   "hq_keka_rig",   (5.2, 2.5, 4.8),   g_hq_keka_launcher,    "sam"),
    ("ng_tomahawk_v",      "hq_cram",       (6.4, 2.9, 0.9),   m_tomahawk_v,          "msl"),
    ("ng_sam_thaad",       "hq_thaad_tan",  (6.3, 0.7, 0.7),   m_sam_thaad,           "msl"),
    ("ng_sam_40n6",        "hq_russia_sam", (7.6, 1.0, 1.0),   m_sam_40n6,            "msl"),
    ("ng_gmlrs_m31",       "hq_thaad_tan",  (4.0, 0.6, 0.6),   m_gmlrs_m31,           "msl"),
]


def add_box_helper(name: str, size_xyz: tuple[float, float, float], special_type: str) -> None:
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0))
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = size_xyz
    bpy.ops.object.transform_apply(scale=True)
    if hasattr(obj, "EDMProps"):
        obj.EDMProps.SPECIAL_TYPE = special_type


def render_hq_showcase(items: list[tuple[str, str, object, tuple[float, float]]], out_path: Path, cam_loc, cam_tgt, lens=32.0) -> None:
    clear_scene()
    mats = {t: create_preview_material(t) for _, t, _, _ in items}
    bpy.context.scene.frame_set(135)
    for name, theme, fn, (xp, yp) in items:
        objs = fn(mats[theme])
        bpy.context.view_layer.update()
        for o in objs:
            if o.animation_data and o.animation_data.action:
                o.rotation_euler = o.rotation_euler.copy()
                o.animation_data_clear()
        for o in objs:
            if o.parent is None:
                o.location.x += xp
                o.location.y += yp

    bpy.ops.mesh.primitive_plane_add(size=160, location=(0, 0, 0))
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
    for loc, en in (((22.0, -22.0, 26.0), 18000), ((-22.0, 14.0, 16.0), 8000), ((0.0, 26.0, 14.0), 6000)):
        bpy.ops.object.light_add(type="AREA", location=loc)
        l = bpy.context.active_object
        l.data.energy, l.data.size = en, 14.0
        l.rotation_euler = (tgt - l.location).to_track_quat("-Z", "Y").to_euler()
    bpy.ops.object.camera_add(location=cam_loc)
    cam = bpy.context.active_object
    cam.data.lens = lens
    cam.rotation_euler = (tgt - cam.location).to_track_quat("-Z", "Y").to_euler()
    bpy.context.scene.camera = cam
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.samples = 36
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
    for name, theme, bbox, fn, _ in HQ_MODELS:
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

    sam_grid = [
        ("ng_cram_centurion",  "hq_cram",       g_hq_cram_centurion,  (-16, 8)),
        ("ng_iron_dome_ln",    "hq_irondome",   g_hq_iron_dome_ln,    (-7, 8)),
        ("ng_iron_dome_radar", "hq_irondome",   g_hq_iron_dome_radar, (2, 8)),
        ("ng_irist_slm_ln",    "hq_nato_sam",   g_hq_irist_slm_ln,    (12, 8)),
        ("ng_trml_4d_radar",   "hq_nato_sam",   g_hq_trml_4d_radar,   (22, 8)),
        ("ng_sampt_aster30",   "hq_nato_sam",   g_hq_sampt_aster30,   (-16, -6)),
        ("ng_pantsir_sm",      "hq_russia_sam", g_hq_pantsir_sm,      (-5, -6)),
        ("ng_patriot_pac3_ln", "hq_nato_sam",   g_hq_patriot_pac3,    (5, -6)),
        ("ng_thaad_ln",        "hq_thaad_tan",  g_hq_thaad_ln,        (15, -6)),
        ("ng_s400_tel",        "hq_russia_sam", g_hq_s400_tel,        (26, -6)),
        ("ng_keka_launcher",   "hq_keka_rig",   g_hq_keka_launcher,   (-5, -18)),
    ]
    render_hq_showcase(sam_grid, PREVIEW_HQ_SAM, (26.0, -32.0, 18.0), (2.0, -2.0, 2.0), lens=28.0)

    closeup = [
        ("ng_cram_centurion", "hq_cram",       g_hq_cram_centurion, (-5.5, 0.0)),
        ("ng_iron_dome_ln",   "hq_irondome",   g_hq_iron_dome_ln,   (2.5, 0.0)),
        ("ng_pantsir_sm",     "hq_russia_sam", g_hq_pantsir_sm,     (11.5, 0.0)),
    ]
    render_hq_showcase(closeup, PREVIEW_HQ_CLOSEUP, (10.0, -14.0, 6.2), (2.5, 0.0, 1.8), lens=36.0)

    # Render orthographic-like comparison strip of the 4 new v5 missiles (deployed at frame 200 -> Tomahawk wings open!)
    clear_scene()
    msl_items = [
        ("ng_tomahawk_v", "hq_cram",       m_tomahawk_v, (0.0,  2.4, 1.0)),
        ("ng_sam_thaad",  "hq_thaad_tan",  m_sam_thaad,  (0.0,  0.8, 1.0)),
        ("ng_sam_40n6",   "hq_russia_sam", m_sam_40n6,   (0.0, -0.8, 1.0)),
        ("ng_gmlrs_m31",  "hq_thaad_tan",  m_gmlrs_m31,  (0.0, -2.4, 1.0)),
    ]
    mats_m = {t: create_preview_material(t) for _, t, _, _ in msl_items}
    bpy.context.scene.frame_set(200)
    for name, theme, fn, (xp, yp, zp) in msl_items:
        objs = fn(mats_m[theme])
        bpy.context.view_layer.update()
        for o in objs:
            if o.animation_data and o.animation_data.action:
                o.rotation_euler = o.rotation_euler.copy()
                o.animation_data_clear()
        for o in objs:
            o.location.x += xp
            o.location.y += yp
            o.location.z += zp
    bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 0, 0))
    fl = bpy.context.active_object
    fmm = bpy.data.materials.new("MFloor"); fmm.use_nodes = True
    fmm.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.045, 0.05, 0.06, 1.0)
    fl.data.materials.append(fmm)
    for loc, en in (((4.0, -6.0, 9.0), 4000), ((-5.0, 5.0, 7.0), 2500)):
        bpy.ops.object.light_add(type="AREA", location=loc)
        la = bpy.context.active_object
        la.data.energy, la.data.size = en, 8.0
        la.rotation_euler = (Vector((0, 0, 1.0)) - la.location).to_track_quat("-Z", "Y").to_euler()
    bpy.ops.object.camera_add(location=(0.2, 0.0, 11.5))
    cm = bpy.context.active_object
    cm.data.type = "ORTHO"; cm.data.ortho_scale = 9.2
    cm.rotation_euler = (0.0, 0.0, 0.0)
    bpy.context.scene.camera = cm
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"; sc.cycles.samples = 32; sc.cycles.use_denoising = True
    sc.render.resolution_x, sc.render.resolution_y = 1920, 1080
    sc.render.filepath = str(OUT_DIR / "preview_missiles_v5_ortho.png")
    bpy.ops.render.render(write_still=True)
    print(f"[OK] Rendered {OUT_DIR / 'preview_missiles_v5_ortho.png'}")


if __name__ == "__main__":
    main()
