"""Blender 5.2 Studio Card Renderer for ALL 79 EDM Shapes in NextGen_BVR_Armory.
Renders 960x540 Cycles studio-lit hero cards into docs/renders/<shape>.png
for every air-to-air missile, strike/glide/cruise weapon, drone, SAM interceptor,
KEKA payload, and Ground Air Defense vehicle.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import bmesh
import bpy
from mathutils import Euler, Matrix, Vector

REPO_ROOT = Path(r"C:\Users\trufa\NextGen_BVR_Armory")
TOOLS_DIR = REPO_ROOT / "tools"
MOD_DIR = REPO_ROOT / "mod"
TEX_DIR = MOD_DIR / "Textures" / "NextGen_BVR_Armory"
SHAPES_DIR = MOD_DIR / "Shapes"
RENDERS_DIR = REPO_ROOT / "docs" / "renders"

sys.path.insert(0, str(TOOLS_DIR))
import build_mega_aam_rework as m_aam
import build_mega_arsenal_v3 as m_v3
import build_sam_cram_and_backlog_v4 as m_v4
import build_hq_sam_cram_v5 as m_v5
import build_missile_rework_v6 as m_v6


def clear_scene() -> None:
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for col in (bpy.data.meshes, bpy.data.materials, bpy.data.actions, bpy.data.lights, bpy.data.cameras):
        for item in list(col):
            if item.users == 0:
                col.remove(item)


def load_preview_mat(theme: str) -> bpy.types.Material:
    mat = bpy.data.materials.new(f"CardMat_{theme}")
    mat.use_nodes = True
    nt = mat.node_tree
    bsdf = nt.nodes.get("Principled BSDF")
    alb = TEX_DIR / f"ng_{theme}_albedo.png"
    nrm = TEX_DIR / f"ng_{theme}_normal.png"
    rmt = TEX_DIR / f"ng_{theme}_roughmet.png"
    if alb.exists():
        ta = nt.nodes.new("ShaderNodeTexImage")
        ta.image = bpy.data.images.load(str(alb), check_existing=True)
        nt.links.new(ta.outputs["Color"], bsdf.inputs["Base Color"])
    if rmt.exists():
        tr = nt.nodes.new("ShaderNodeTexImage")
        tr.image = bpy.data.images.load(str(rmt), check_existing=True)
        tr.image.colorspace_settings.name = "Non-Color"
        sep = nt.nodes.new("ShaderNodeSeparateColor")
        nt.links.new(tr.outputs["Color"], sep.inputs["Color"])
        nt.links.new(sep.outputs["Green"], bsdf.inputs["Roughness"])
        nt.links.new(sep.outputs["Blue"], bsdf.inputs["Metallic"])
    if nrm.exists():
        tn = nt.nodes.new("ShaderNodeTexImage")
        tn.image = bpy.data.images.load(str(nrm), check_existing=True)
        tn.image.colorspace_settings.name = "Non-Color"
        nmap = nt.nodes.new("ShaderNodeNormalMap")
        nmap.inputs["Strength"].default_value = 1.0
        nt.links.new(tn.outputs["Color"], nmap.inputs["Color"])
        nt.links.new(nmap.outputs["Normal"], bsdf.inputs["Normal"])
    return mat


def _box(bm, uv, center, size, rot=(0.0, 0.0, 0.0), uv_box=(0.1, 0.9, 0.1, 0.9), bevel=0.0):
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
    valid = [v for v in bverts if v.is_valid]
    m = Matrix.Translation(center) @ Euler(rot, "XYZ").to_matrix().to_4x4()
    for v in valid:
        v.co = m @ v.co
    u0, u1, v0, v1 = uv_box
    coords = [(u0, v0), (u1, v0), (u1, v1), (u0, v1)]
    for f in bm.faces:
        if any(v in valid for v in f.verts) and all(lp[uv].uv.length == 0 for lp in f.loops):
            for i, lp in enumerate(f.loops):
                lp[uv].uv = coords[i % 4]


def _revolve_x(bm, uv, profile_xr: list[tuple[float, float]], segs: int = 28):
    rings = [
        [bm.verts.new((x, r * math.cos(2 * math.pi * i / segs), r * math.sin(2 * math.pi * i / segs))) for i in range(segs)]
        for x, r in profile_xr
    ]
    xmin, xmax = profile_xr[0][0], profile_xr[-1][0]
    span = max(0.01, xmax - xmin)
    for k in range(len(rings) - 1):
        u0 = 0.05 + 0.90 * ((profile_xr[k][0] - xmin) / span)
        u1 = 0.05 + 0.90 * ((profile_xr[k + 1][0] - xmin) / span)
        r0, r1 = rings[k], rings[k + 1]
        for i in range(segs):
            ni = (i + 1) % segs
            f = bm.faces.new((r0[i], r0[ni], r1[ni], r1[i]))
            f.smooth = True
            va = 0.1 + 0.8 * (i / segs)
            vb = 0.1 + 0.8 * ((i + 1) / segs)
            for lp, uvc in zip(f.loops, ((u0, va), (u0, vb), (u1, vb), (u1, va))):
                lp[uv].uv = uvc
    bm.faces.new(rings[-1])
    bm.faces.new(list(reversed(rings[0])))


def _fins_x(bm, uv, x_center: float, r_body: float, chord: float, span: float, count: int = 4, angle_offset: float = 45.0, sweep_deg: float = 0.0):
    for k in range(count):
        ang = math.radians(angle_offset + k * (360.0 / count))
        r_mid = r_body + span * 0.40
        _box(
            bm, uv,
            (x_center, math.cos(ang) * r_mid, math.sin(ang) * r_mid),
            (chord, span, 0.014),
            rot=(ang, math.radians(sweep_deg), 0.0),
            uv_box=(0.76, 0.96, 0.15, 0.85),
        )


def _mk(name: str, bm: bmesh.types.BMesh, mat: bpy.types.Material):
    mesh = bpy.data.meshes.new(name)
    bm.to_mesh(mesh)
    bm.free()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(obj)
    obj.data.materials.append(mat)
    return [obj]


# ---------- Clean procedural studio rebuilders for the 15 v1/v2 shapes ----------
def leg_aim120a(mat):
    bm = bmesh.new(); uv = bm.loops.layers.uv.new("UVMap")
    _revolve_x(bm, uv, [(-1.83, 0.072), (-1.70, 0.089), (1.35, 0.089), (1.68, 0.045), (1.83, 0.004)])
    _fins_x(bm, uv, 0.10, 0.089, 0.44, 0.24, 4, 45)
    _fins_x(bm, uv, -1.52, 0.089, 0.40, 0.22, 4, 45)
    return _mk("AIM120A", bm, mat)


def leg_aim120cd(mat):
    bm = bmesh.new(); uv = bm.loops.layers.uv.new("UVMap")
    _revolve_x(bm, uv, [(-1.83, 0.072), (-1.70, 0.089), (1.35, 0.089), (1.68, 0.045), (1.83, 0.004)])
    _fins_x(bm, uv, 0.15, 0.089, 0.36, 0.16, 4, 45)
    _fins_x(bm, uv, -1.55, 0.089, 0.32, 0.15, 4, 45)
    return _mk("AIM120CD", bm, mat)


def leg_asraam(mat):
    bm = bmesh.new(); uv = bm.loops.layers.uv.new("UVMap")
    _revolve_x(bm, uv, [(-1.45, 0.068), (-1.35, 0.083), (1.26, 0.083), (1.40, 0.045), (1.45, 0.008)])
    _fins_x(bm, uv, -1.24, 0.083, 0.28, 0.15, 4, 45)
    return _mk("ASRAAM", bm, mat)


def leg_peregrine(mat):
    bm = bmesh.new(); uv = bm.loops.layers.uv.new("UVMap")
    _revolve_x(bm, uv, [(-0.90, 0.05), (-0.82, 0.06), (0.65, 0.06), (0.85, 0.025), (0.90, 0.004)])
    _fins_x(bm, uv, 0.05, 0.06, 0.35, 0.09, 4, 45)
    _fins_x(bm, uv, -0.72, 0.06, 0.20, 0.12, 4, 45)
    return _mk("Peregrine", bm, mat)


def leg_guided_rocket(mat):
    bm = bmesh.new(); uv = bm.loops.layers.uv.new("UVMap")
    _revolve_x(bm, uv, [(-0.88, 0.032), (-0.75, 0.035), (0.72, 0.035), (0.86, 0.018), (0.88, 0.005)])
    _fins_x(bm, uv, 0.42, 0.035, 0.14, 0.055, 4, 45)
    _fins_x(bm, uv, -0.76, 0.035, 0.16, 0.075, 4, 0)
    return _mk("GuidedRocket", bm, mat)


def leg_atgm_quad(mat):
    bm = bmesh.new(); uv = bm.loops.layers.uv.new("UVMap")
    _revolve_x(bm, uv, [(-0.90, 0.075), (-0.80, 0.089), (0.76, 0.089), (0.88, 0.05), (0.90, 0.012)])
    _fins_x(bm, uv, 0.15, 0.089, 0.85, 0.025, 4, 45)
    _fins_x(bm, uv, -0.70, 0.089, 0.26, 0.15, 4, 45)
    return _mk("ATGM_Quad", bm, mat)


def leg_aasm_hammer(mat):
    bm = bmesh.new(); uv = bm.loops.layers.uv.new("UVMap")
    _revolve_x(bm, uv, [(-1.55, 0.09), (-1.40, 0.12), (-0.70, 0.136), (0.95, 0.136), (1.35, 0.075), (1.55, 0.015)])
    _fins_x(bm, uv, 1.05, 0.11, 0.28, 0.08, 4, 45)
    _fins_x(bm, uv, -1.18, 0.12, 0.48, 0.36, 4, 45)
    return _mk("AASM_Hammer", bm, mat)


def leg_durandal(mat):
    bm = bmesh.new(); uv = bm.loops.layers.uv.new("UVMap")
    _revolve_x(bm, uv, [(-1.25, 0.095), (-0.85, 0.112), (0.85, 0.112), (1.15, 0.045), (1.25, 0.005)])
    _fins_x(bm, uv, -0.95, 0.112, 0.32, 0.12, 4, 45)
    return _mk("Durandal", bm, mat)


def leg_glide_sdb(mat):
    bm = bmesh.new(); uv = bm.loops.layers.uv.new("UVMap")
    _box(bm, uv, (0.0, 0.0, 0.0), (1.65, 0.19, 0.17), bevel=0.04)
    _box(bm, uv, (0.85, 0.0, 0.0), (0.36, 0.16, 0.14), bevel=0.04)
    # Deployed diamond back wings
    for sy in (-1.0, 1.0):
        _box(bm, uv, (-0.05, sy * 0.44, 0.09), (0.24, 0.85, 0.022), rot=(0, 0, sy * math.radians(-22)))
    _fins_x(bm, uv, -0.72, 0.08, 0.20, 0.12, 4, 45)
    return _mk("GlideSDB", bm, mat)


def leg_umpb_d30(mat):
    bm = bmesh.new(); uv = bm.loops.layers.uv.new("UVMap")
    _revolve_x(bm, uv, [(-1.42, 0.09), (-1.15, 0.15), (1.05, 0.15), (1.35, 0.06), (1.42, 0.008)])
    for sy in (-1.0, 1.0):
        _box(bm, uv, (0.08, sy * 0.56, 0.16), (0.30, 1.12, 0.025), rot=(0, 0, sy * math.radians(-20)))
    _fins_x(bm, uv, -1.20, 0.14, 0.28, 0.18, 4, 45)
    return _mk("UMPB_D30", bm, mat)


def leg_heavy_umpk(mat):
    bm = bmesh.new(); uv = bm.loops.layers.uv.new("UVMap")
    _revolve_x(bm, uv, [(-1.24, 0.08), (-0.78, 0.20), (0.72, 0.20), (1.12, 0.10), (1.24, 0.01)])
    _box(bm, uv, (0.0, 0.0, 0.23), (1.75, 0.22, 0.09), bevel=0.015)
    for sy in (-1.0, 1.0):
        _box(bm, uv, (0.10, sy * 0.68, 0.26), (0.32, 1.35, 0.025), rot=(0, 0, sy * math.radians(-24)))
    _fins_x(bm, uv, -1.02, 0.14, 0.34, 0.20, 4, 45)
    return _mk("HeavyUMPK", bm, mat)


def leg_brahmos(mat):
    bm = bmesh.new(); uv = bm.loops.layers.uv.new("UVMap")
    _revolve_x(bm, uv, [(-4.10, 0.24), (-3.80, 0.335), (3.45, 0.335), (3.65, 0.28), (4.10, 0.015)])
    _fins_x(bm, uv, 0.40, 0.335, 0.85, 0.42, 4, 45)
    _fins_x(bm, uv, -3.55, 0.335, 0.72, 0.46, 4, 45)
    return _mk("BrahMos", bm, mat)


def leg_kh31(mat):
    bm = bmesh.new(); uv = bm.loops.layers.uv.new("UVMap")
    _revolve_x(bm, uv, [(-2.35, 0.14), (-2.10, 0.18), (1.85, 0.18), (2.22, 0.08), (2.35, 0.008)])
    for k in range(4):
        ang = math.radians(45 + k * 90)
        _box(bm, uv, (-0.15, math.cos(ang) * 0.22, math.sin(ang) * 0.22), (2.10, 0.11, 0.11), bevel=0.02)
    _fins_x(bm, uv, -0.35, 0.18, 0.55, 0.24, 4, 45)
    _fins_x(bm, uv, -2.05, 0.18, 0.42, 0.26, 4, 45)
    return _mk("Kh31", bm, mat)


def leg_hypersonic(mat):
    bm = bmesh.new(); uv = bm.loops.layers.uv.new("UVMap")
    _revolve_x(bm, uv, [(-3.25, 0.19), (-2.90, 0.24), (1.20, 0.24), (2.35, 0.14), (3.25, 0.008)])
    _fins_x(bm, uv, -2.85, 0.24, 0.65, 0.28, 4, 45)
    return _mk("Hypersonic", bm, mat)


def leg_loitering_x(mat):
    bm = bmesh.new(); uv = bm.loops.layers.uv.new("UVMap")
    _revolve_x(bm, uv, [(-0.82, 0.05), (-0.70, 0.075), (0.62, 0.075), (0.82, 0.01)])
    _fins_x(bm, uv, 0.18, 0.075, 0.24, 0.48, 4, 45)
    _fins_x(bm, uv, -0.58, 0.075, 0.22, 0.44, 4, 45)
    return _mk("LoiteringX", bm, mat)


LEGACY_15 = [
    ("ng_aim120a",        "us_bvr",          leg_aim120a),
    ("ng_aim120cd",       "us_bvr",          leg_aim120cd),
    ("ng_asraam_sleek",   "us_bvr",          leg_asraam),
    ("ng_peregrine",      "us_bvr",          leg_peregrine),
    ("ng_guided_rocket",  "us_bvr",          leg_guided_rocket),
    ("ng_atgm_quad",      "helo_atgm",       leg_atgm_quad),
    ("ng_aasm_hammer",    "aasm_hammer",     leg_aasm_hammer),
    ("ng_durandal_runway","durandal_cbu",    leg_durandal),
    ("ng_glide_sdb",      "glide_bomb",      leg_glide_sdb),
    ("ng_umpb_d30",       "umpb_pab",        leg_umpb_d30),
    ("ng_heavy_umpk",     "heavy_bomb",      leg_heavy_umpk),
    ("ng_brahmos_intake", "ramjet_heavy",    leg_brahmos),
    ("ng_kh31_ramjet",    "ramjet_heavy",    leg_kh31),
    ("ng_hypersonic",     "hypersonic_blk",  leg_hypersonic),
    ("ng_loitering_x",    "loitering_olive", leg_loitering_x),
]


def gather_all_79():
    registry: dict[str, tuple[str, object, str, int]] = {}
    # Order: v1/v2 legacy -> AAMS -> Arsenal v3 -> V4 backlog -> HQ v5 (later overrides earlier!)
    for name, theme, fn in LEGACY_15:
        registry[name] = (theme, fn, "x", 200)
    for name, theme, _, fn in m_aam.AAMS:
        registry[name] = (theme, fn, "y_to_x", 200)
    for name, theme, _, fn in m_v3.ARSENAL_MODELS:
        registry[name] = (theme, fn, "y_to_x", 200)
    for name, theme, _, fn, grp in m_v4.MODELS_V4:
        registry[name] = (theme, fn, "x", 145 if grp == "sam" else 200)
    for name, theme, _, fn, grp in m_v5.HQ_MODELS:
        registry[name] = (theme, fn, "x", 135 if grp == "sam" else 200)
    for name, theme, _, fn in m_v6.WAVE6_MODELS:
        registry[name] = (theme, fn, "x", 200)
    return registry


def scene_world_bounds() -> tuple[Vector, Vector]:
    bpy.context.view_layer.update()
    pts = []
    for o in bpy.context.scene.objects:
        if o.type == "MESH":
            for corner in o.bound_box:
                pts.append(o.matrix_world @ Vector(corner))
    if not pts:
        return Vector((-1, -1, -1)), Vector((1, 1, 1))
    mn = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
    mx = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
    return mn, mx


def render_card(name: str, theme: str, fn, axis_mode: str, frame: int, out_path: Path) -> None:
    clear_scene()
    bpy.context.scene.frame_start = 0
    bpy.context.scene.frame_end = 200
    bpy.context.scene.frame_set(frame)

    mat = load_preview_mat(theme)
    objs = fn(mat)
    if axis_mode == "y_to_x":
        root = bpy.data.objects.new("CardRoot", None)
        bpy.context.scene.collection.objects.link(root)
        root.rotation_euler = (0.0, 0.0, -math.pi * 0.5)
        for o in objs:
            if o.parent is None:
                o.parent = root
    bpy.context.view_layer.update()

    mn, mx = scene_world_bounds()
    center = 0.5 * (mn + mx)
    diag = (mx - mn).length
    is_ground = (mx.z - mn.z) > 1.8 or diag > 8.0 and (mx.y - mn.y) > 1.8 and min(o.location.z for o in objs if o.type == "MESH") >= -0.2
    # Place ground plane cleanly beneath bottom of bounding box
    floor_z = (mn.z - 0.02) if mn.z > -0.15 else (mn.z - max(0.25, diag * 0.08))

    bpy.ops.mesh.primitive_plane_add(size=max(30.0, diag * 8.0), location=(center.x, center.y, floor_z))
    floor = bpy.context.active_object
    fm = bpy.data.materials.new("CardFloor")
    fm.use_nodes = True
    fm.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.055, 0.062, 0.072, 1.0)
    fm.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.55
    floor.data.materials.append(fm)

    world = bpy.context.scene.world or bpy.data.worlds.new("World")
    bpy.context.scene.world = world
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.032, 0.038, 0.048, 1.0)

    # Studio 3-point lighting scaled cleanly by diag^2
    dist = max(1.8, diag * 1.45)
    base_e = (dist ** 2) * 28.0
    for (dx, dy, dz), mult in (((0.9, -1.1, 1.15), 1.0), ((-1.1, 0.7, 0.75), 0.45), ((0.2, 1.2, 0.65), 0.35)):
        bpy.ops.object.light_add(type="AREA", location=center + Vector((dx * dist, dy * dist, dz * dist)))
        l = bpy.context.active_object
        l.data.energy = base_e * mult
        l.data.size = max(1.0, diag * 0.7)
        l.rotation_euler = (center - l.location).to_track_quat("-Z", "Y").to_euler()

    # Hero 3/4 view fitting projected bounding box cleanly at <=78% of 960x540 frustum!
    cam_dir = Vector((0.72, -0.92, 0.44)).normalized()
    right = Vector((0, 0, 1)).cross(cam_dir).normalized()
    up = cam_dir.cross(right).normalized()
    corners = [Vector((x, y, z)) for x in (mn.x, mx.x) for y in (mn.y, mx.y) for z in (mn.z, mx.z)]
    half_w = max(abs((c - center).dot(right)) for c in corners)
    half_h = max(abs((c - center).dot(up)) for c in corners)
    half_d = max(abs((c - center).dot(cam_dir)) for c in corners)
    lens_mm = 36.0
    sensor_w = 36.0
    sensor_h = sensor_w * (540.0 / 960.0)
    dist_w = (half_w / 0.39) * (lens_mm / sensor_w) + half_d
    dist_h = (half_h / 0.39) * (lens_mm / sensor_h) + half_d
    cam_dist = max(1.3, dist_w, dist_h)

    bpy.ops.object.camera_add(location=center + cam_dir * cam_dist)
    cam = bpy.context.active_object
    cam.data.lens = lens_mm
    cam.rotation_euler = (center - cam.location).to_track_quat("-Z", "Y").to_euler()
    bpy.context.scene.camera = cam

    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.samples = 18
    sc.cycles.use_denoising = True
    sc.render.resolution_x, sc.render.resolution_y = 960, 540
    sc.render.filepath = str(out_path)
    bpy.ops.render.render(write_still=True)


def main() -> None:
    RENDERS_DIR.mkdir(parents=True, exist_ok=True)
    reg = gather_all_79()
    expected = sorted(p.stem for p in SHAPES_DIR.glob("*.edm"))
    missing = [s for s in expected if s not in reg]
    if missing:
        raise RuntimeError(f"Unmapped EDM shapes: {missing}")

    # Support optional "--only-v6" or "--only-fixed" to fast-rerender modified groups
    only_v6 = "--only-v6" in sys.argv
    only_fixed = "--only-fixed" in sys.argv
    v6_set = {n for n, _, _, _ in m_v6.WAVE6_MODELS}
    fixed_set = v6_set | {n for n, _, _, _, g in m_v5.HQ_MODELS if g == "sam"}
    targets = [s for s in expected if (s in v6_set if only_v6 else (s in fixed_set if only_fixed else True))]
    total = len(targets)
    for idx, shape in enumerate(targets, 1):
        out = RENDERS_DIR / f"{shape}.png"
        theme, fn, axis_mode, frame = reg[shape]
        render_card(shape, theme, fn, axis_mode, frame, out)
        print(f"[{idx:02d}/{total}] Rendered {out.name} ({out.stat().st_size} B)")


if __name__ == "__main__":
    main()
