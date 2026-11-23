declare_plugin("NextGen_BVR_Armory", {
    installed     = true,
    dirName       = current_mod_path,
    displayName   = _("Next-Gen BVR, Strategic & Air Defense Armory"),
    shortName     = "NextGen_BVR_Armory",
    state         = "installed",
    developerName = "DCS-Modding AI Lab",
    version       = "3.0.0",
    info          = _("NextGen Armory v3.0: Calibrated Mach-indexed DCS polars + 170+ air/ground weapons, KEKA Aerospace Troposphere troll rockets, and animated Surface Air Defenses (Centurion C-RAM, Iron Dome 20-cell + EL/M-2084, IRIS-T SLM, SAMP/T Aster 30, Pantsir-SM, Patriot PAC-3 MSE & KEKA Pad)."),
})

mount_vfs_model_path(current_mod_path .. "/Shapes")
mount_vfs_texture_path(current_mod_path .. "/Textures/NextGen_BVR_Armory")

-- 1. Load Air-to-Air, Heavy Air-to-Ground, Tactical & Ground SAM Interceptors
local nextgen_clsids = dofile(current_mod_path .. "/Database/weapons_nextgen.lua")
local ag_clsids      = dofile(current_mod_path .. "/Database/weapons_arsenal_ag.lua")
local tac_clsids     = dofile(current_mod_path .. "/Database/weapons_tactical_30.lua")
local sam_weapons    = dofile(current_mod_path .. "/Database/weapons_sam_interceptors.lua")

-- 2. Register Surface Air Defense Launchers, Radars & C-RAM
local register_air_defenses = dofile(current_mod_path .. "/Database/units_air_defense.lua")
if register_air_defenses and sam_weapons then
    register_air_defenses(sam_weapons)
end

if ag_clsids then
    for _, c in ipairs(ag_clsids.nato_aam) do table.insert(nextgen_clsids.nato_bvr, c) end
    for _, c in ipairs(ag_clsids.east_aam) do table.insert(nextgen_clsids.east_bvr, c) end
    for _, c in ipairs(ag_clsids.wvr_aam)  do table.insert(nextgen_clsids.nato_wvr, c) end
    nextgen_clsids.ag_all = ag_clsids.ag_all
end

if tac_clsids then
    for _, c in ipairs(tac_clsids.nato_bvr)   do table.insert(nextgen_clsids.nato_bvr, c) end
    for _, c in ipairs(tac_clsids.nato_wvr)   do table.insert(nextgen_clsids.nato_wvr, c) end
    for _, c in ipairs(tac_clsids.french_all) do table.insert(nextgen_clsids.french_all, c) end
    for _, c in ipairs(tac_clsids.east_bvr)   do table.insert(nextgen_clsids.east_bvr, c) end
    for _, c in ipairs(tac_clsids.ag_all)     do table.insert(nextgen_clsids.ag_all, c) end
end

-- Attach new CLSIDs to existing aircraft pylons in memory (never modifies DCS install files)
local function attach_clsids_to_compatible_pylons(clsid_map)
    if not db or not db.Units or not db.Units.Planes or not db.Units.Planes.Plane then
        return
    end

    local anchor_to_new = {
        -- NATO BVR (AIM-120C / AIM-120B anchors)
        ["{4088557F-5176-48F4-9B17-01B976F64952}"] = clsid_map.nato_bvr,
        ["{444BA8AE-82A7-4345-842E-76154EF5B543}"] = clsid_map.nato_bvr,
        ["{C8E06185-7CD6-4C90-959F-044679E90751}"] = clsid_map.nato_bvr,
        -- NATO WVR (AIM-9X / AIM-9M anchors)
        ["{5CE2FF2A-645A-4197-B48D-8720AC69394F}"] = clsid_map.nato_wvr,
        ["{6CEB49FC-DED8-4DED-B053-E1F033FF72D3}"] = clsid_map.nato_wvr,
        -- French MICA / Magic / Super 530D anchors
        ["{FC23864E-3B80-48E3-9C03-3DA8B229622E}"] = clsid_map.french_all,
        ["{MMagicII}"]                             = clsid_map.french_all,
        ["{Matra_S530D}"]                          = clsid_map.french_all,
        -- Eastern / Russian / Chinese BVR anchors (R-77 / SD-10 / R-27ER)
        ["{B4C01D60-A8A3-4237-BD72-CA7655BC0F93}"] = clsid_map.east_bvr,
        ["{E8069896-8435-4B90-95C0-01A03AE6E400}"] = clsid_map.east_bvr,
        ["{D55F6732-C75B-424A-B8AD-1D85A94D6547}"] = clsid_map.east_bvr,
        -- Air-to-Ground / SEAD / Cruise / Glide Bomb anchors
        ["{B06DD79A-F21E-4EB9-8E4B-53543A40A906}"] = clsid_map.ag_all,
        ["{F16A4DE0-116C-4A71-97F0-2CF85B0313EC}"] = clsid_map.ag_all,
        ["{BCE4E030-38E9-423E-98ED-24BE3DA87C32}"] = clsid_map.ag_all,
        ["{DB769D48-67D7-42ED-A2BE-108D586C8812}"] = clsid_map.ag_all,
        ["{GBU-38}"]                               = clsid_map.ag_all,
        ["{AGM-154C}"]                             = clsid_map.ag_all,
    }

    for _, plane in pairs(db.Units.Planes.Plane) do
        if plane.Pylons then
            for _, pylon in pairs(plane.Pylons) do
                if pylon.Launchers then
                    local existing = {}
                    for _, launcher in pairs(pylon.Launchers) do
                        if launcher.CLSID then
                            existing[launcher.CLSID] = true
                        end
                    end
                    for anchor, new_list in pairs(anchor_to_new) do
                        if existing[anchor] then
                            for _, new_clsid in ipairs(new_list) do
                                if not existing[new_clsid] then
                                    table.insert(pylon.Launchers, { CLSID = new_clsid })
                                    existing[new_clsid] = true
                                end
                            end
                        end
                    end
                end
            end
        end
    end
end

if nextgen_clsids then
    attach_clsids_to_compatible_pylons(nextgen_clsids)
end

plugin_done()
