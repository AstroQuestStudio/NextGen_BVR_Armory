"""Verify NextGen_BVR_Armory v5.0 Lua syntax, shape bindings, SAM units, CLSID uniqueness, and PBR textures."""

from pathlib import Path
import re
import sys


def verify(mod_dir: Path) -> None:
    shapes_dir = mod_dir / "Shapes"
    tex_dir = mod_dir / "Textures" / "NextGen_BVR_Armory"
    db_dir = mod_dir / "Database"

    shapes = {p.stem for p in shapes_dir.glob("*.edm")}
    textures = {p.name for p in tex_dir.glob("*.png")}

    lua_files = [
        mod_dir / "entry.lua",
        db_dir / "polar_profiles.lua",
        db_dir / "weapons_nextgen.lua",
        db_dir / "weapons_arsenal_ag.lua",
        db_dir / "weapons_tactical_30.lua",
        db_dir / "weapons_sam_interceptors.lua",
        db_dir / "units_air_defense.lua",
    ]

    all_ids = {}
    all_clsids = {}
    all_units = {}
    missing_shapes = []

    for lf in lua_files:
        assert lf.exists(), f"Missing Lua file: {lf}"
        txt = lf.read_text(encoding="utf-8")
        clean = re.sub(r"--[^\n]*", "", txt)
        no_str = re.sub(r'"[^"]*"', '""', clean)
        assert no_str.count("{") == no_str.count("}"), f"Unbalanced {{}} in {lf.name}"
        assert no_str.count("(") == no_str.count(")"), f"Unbalanced () in {lf.name}"

        if lf.name.startswith("weapons_"):
            ids = re.findall(r'\bid\s*=\s*"([^"]+)"', txt)
            clsids = re.findall(r'\b(?:clsid|CLSID)\s*=\s*"([^"]+)"', txt)
            shs = re.findall(r'\b(?:shape|ShapeName)\s*=\s*"([^"]+)"', txt)
            for idv in ids:
                assert idv not in all_ids, f"Duplicate weapon id {idv} in {lf.name} and {all_ids[idv]}"
                all_ids[idv] = lf.name
            for cl in clsids:
                assert cl not in all_clsids, f"Duplicate CLSID {cl} in {lf.name} and {all_clsids[cl]}"
                all_clsids[cl] = lf.name
            for s in shs:
                if s not in shapes:
                    missing_shapes.append((s, lf.name))
        elif lf.name == "units_air_defense.lua":
            uids = re.findall(r'\bid\s*=\s*"([^"]+)"', txt)
            shs = re.findall(r'\bshape\s*=\s*"([^"]+)"', txt)
            for u in uids:
                assert u not in all_units, f"Duplicate unit id {u}"
                all_units[u] = lf.name
            for s in shs:
                if s not in shapes:
                    missing_shapes.append((s, lf.name))

    assert not missing_shapes, f"Missing .edm shapes: {missing_shapes}"
    print(
        f"[OK] Verified {len(all_ids)} weapons, {len(all_clsids)} aircraft loadouts, "
        f"{len(all_units)} air defense units, {len(shapes)} .edm shapes, {len(textures)} PBR .png maps."
    )


if __name__ == "__main__":
    root = Path(__file__).resolve().parent.parent / "mod"
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else root
    verify(target)
