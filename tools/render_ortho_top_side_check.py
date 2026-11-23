"""Render calibrated orthographic TOP (+Z) and SIDE (+X) silhouette sheets + Folded vs Deployed audit."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

import bpy
from mathutils import Vector


SCRATCH_DIR = Path(__file__).resolve().parent
OUT_DIR = SCRATCH_DIR.parent

AAM_SCRIPT = SCRATCH_DIR / "build_mega_aam_rework.py"
ARS_SCRIPT = SCRATCH_DIR / "build_mega_arsenal_v3.py"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def freeze_and_place(objs: list[bpy.types.Object], x_off: float, y_off: float, z_off: float = 0.0, rot_z_90: bool = False) -> None:
    bpy.context.view_layer.update()
    for o in objs:
        if o.animation_data and o.animation_data.action:
            if o.rotation_mode == "QUATERNION":
                o.rotation_quaternion = o.rotation_quaternion.copy()
            else:
                o.rotation_euler = o.rotation_euler.copy()
            o.animation_data_clear()
        if rot_z_90:
            # Rotate around Y axis to show SIDE view looking from +Z? No, camera sits on +Z looking down!
            # So rotating weapon 90 deg around Y puts its Z-vertical side facing +Z!
            o.rotation_mode = "XYZ"
            # Wait: for children/rotated fins, create parent empty!
            pass
        o.location.x += x_off
        o.location.y += y_off
        o.location.z += z_off


def parent_and_place(objs: list[bpy.types.Object], label: str, x_off: float, y_off: float, roll_90_for_side: bool = False) -> None:
    bpy.context.view_layer.update()
    empty = bpy.data.objects.new(f"Root_{label}", None)
    bpy.context.collection.objects.link(empty)
    for o in objs:
        if o.animation_data and o.animation_data.action:
            if o.rotation_mode == "QUATERNION":
                o.rotation_quaternion = o.rotation_quaternion.copy()
            else:
                o.rotation_euler = o.rotation_euler.copy()
            o.animation_data_clear()
        o.parent = empty
    if roll_90_for_side:
        empty.rotation_euler = (0.0, 1.5707963, 0.0)
    empty.location = (x_off, y_off, 0.0)


def setup_ortho_scene(ortho_scale: float, center_xy: tuple[float, float], out_path: Path) -> None:
    # Neutral light grey drafting background for crisp silhouette readability
    world = bpy.context.scene.world or bpy.data.worlds.new("World")
    bpy.context.scene.world = world
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.76, 0.78, 0.81, 1.0)
    world.node_tree.nodes["Background"].inputs["Strength"].default_value = 1.0

    # Soft studio lighting from above + angled rim so white & dark missiles both pop cleanly
    for loc, en in (((0.0, 0.0, 20.0), 4500), ((10.0, 12.0, 14.0), 3000), ((-10.0, -8.0, 12.0), 2200)):
        bpy.ops.object.light_add(type="AREA", location=loc)
        l = bpy.context.active_object
        l.data.energy, l.data.size = en, 14.0
        tgt = Vector((center_xy[0], center_xy[1], 0.0))
        l.rotation_euler = (tgt - l.location).to_track_quat("-Z", "Y").to_euler()

    bpy.ops.object.camera_add(location=(center_xy[0], center_xy[1], 25.0))
    cam = bpy.context.active_object
    cam.data.type = "ORTHO"
    cam.data.ortho_scale = ortho_scale
    cam.rotation_euler = (0.0, 0.0, 0.0)
    bpy.context.scene.camera = cam

    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.samples = 24
    sc.cycles.use_denoising = True
    sc.render.resolution_x = 2400
    sc.render.resolution_y = 1440
    sc.render.filepath = str(out_path)


def render_top_side_sheet(
    mod,
    items: list[tuple[str, str, tuple, object]],
    spacing: float,
    row_sep: float,
    ortho_scale: float,
    out_path: Path,
) -> None:
    mod.clear_scene()
    themes = sorted({t for _, t, _, _ in items})
    mats = {t: mod.create_preview_material(t) for t in themes}
    bpy.context.scene.frame_set(200)

    n = len(items)
    x_start = -0.5 * (n - 1) * spacing

    # Top row = Orthographic TOP (+Z), Bottom row = Orthographic SIDE (rolled 90 deg around Y)
    for idx, (name, theme, _, fn) in enumerate(items):
        x = x_start + idx * spacing
        objs_top = fn(mats[theme])
        parent_and_place(objs_top, f"{name}_TOP", x, row_sep * 0.5, roll_90_for_side=False)
        objs_side = fn(mats[theme])
        parent_and_place(objs_side, f"{name}_SIDE", x, -row_sep * 0.5, roll_90_for_side=True)

    setup_ortho_scene(ortho_scale, (0.0, 0.0), out_path)
    bpy.ops.render.render(write_still=True)
    print(f"[OK] Rendered ortho sheet {out_path}")


def render_folded_vs_deployed(aam_mod, ars_mod, out_path: Path) -> None:
    ars_mod.clear_scene()
    folding_items = [
        ("ng_pl15e",          aam_mod, "pl12_15",     lambda m: aam_mod.b_pl15(m, True)),
        ("ng_r77_grid",       aam_mod, "r77_grid",    aam_mod.b_r77_grid),
        ("ng_r37m",           aam_mod, "east_ru_cn",  aam_mod.b_r37m),
        ("ng_kh35u",          ars_mod, "kh35_uran",   ars_mod.b_kh35u),
        ("ng_nsm_jsm",        ars_mod, "stealth_dark",ars_mod.b_nsm_jsm),
        ("ng_kh22_32",        ars_mod, "kh22_32",     ars_mod.b_kh22_32),
        ("ng_kh58ushke",      ars_mod, "kh58_sead",   ars_mod.b_kh58ushke),
        ("ng_spear_ew",       ars_mod, "glide_bomb",  ars_mod.b_spear_ew),
        ("ng_gbu57_mop",      ars_mod, "gbu57_mop",   ars_mod.b_gbu57_mop),
        ("ng_spice_glide",    ars_mod, "spice_eo",    ars_mod.b_spice_glide),
        ("ng_stealth_cruise", ars_mod, "scalp_new",   ars_mod.b_scalp_blunt),
        ("ng_jassm_taurus",   ars_mod, "taurus_new",  ars_mod.b_taurus_new),
    ]

    mats = {}
    for _, mod, theme, _ in folding_items:
        if (mod, theme) not in mats:
            mats[(mod, theme)] = mod.create_preview_material(theme)

    spacing = 2.4
    x_start = -0.5 * (len(folding_items) - 1) * spacing

    # Frame 100 = Folded (top row, y=+6.2)
    bpy.context.scene.frame_set(100)
    for idx, (name, mod, theme, fn) in enumerate(folding_items):
        objs = fn(mats[(mod, theme)])
        parent_and_place(objs, f"{name}_FOLDED", x_start + idx * spacing, 6.2, roll_90_for_side=False)

    # Frame 200 = Deployed (bottom row, y=-6.2)
    bpy.context.scene.frame_set(200)
    for idx, (name, mod, theme, fn) in enumerate(folding_items):
        objs = fn(mats[(mod, theme)])
        parent_and_place(objs, f"{name}_DEPLOYED", x_start + idx * spacing, -6.2, roll_90_for_side=False)

    setup_ortho_scene(31.0, (0.0, 0.0), out_path)
    bpy.ops.render.render(write_still=True)
    print(f"[OK] Rendered folded vs deployed {out_path}")


def main() -> None:
    aam_mod = load_module(AAM_SCRIPT, "build_mega_aam_rework")
    ars_mod = load_module(ARS_SCRIPT, "build_mega_arsenal_v3")
    bpy.context.scene.frame_start = 0
    bpy.context.scene.frame_end = 200

    render_top_side_sheet(
        aam_mod,
        aam_mod.AAMS,
        spacing=1.15,
        row_sep=7.2,
        ortho_scale=21.5,
        out_path=OUT_DIR / "ortho_aam_top_side.png",
    )
    render_top_side_sheet(
        ars_mod,
        ars_mod.ARSENAL_MODELS,
        spacing=2.35,
        row_sep=13.0,
        ortho_scale=44.0,
        out_path=OUT_DIR / "ortho_arsenal_top_side.png",
    )
    render_folded_vs_deployed(
        aam_mod,
        ars_mod,
        out_path=OUT_DIR / "ortho_folded_vs_deployed.png",
    )


if __name__ == "__main__":
    main()
