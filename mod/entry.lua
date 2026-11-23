declare_plugin("NextGen_BVR_Armory", {
    installed     = true,
    dirName       = current_mod_path,
    displayName   = _("Next-Gen BVR, Strategic & Air Defense Armory"),
    shortName     = "NextGen_BVR_Armory",
    state         = "installed",
    developerName = "DCS-Modding AI Lab",
    version       = "6.0.0",
    info          = _("NextGen Armory v6.0: Calibrated Mach-indexed DCS polars + 262 air/ground/naval/ABM/drone weapons (Shahed-238 Jet, Tomahawk Blk V, GMLRS, PrSM/ATACMS, DF-17, THAAD, S-400 40N6, KEKA Njiwa-1) + 11 high-detail animated SAM & C-RAM vehicles."),
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
        -- NATO BVR (AIM-120C / AIM-120B verified across F-16C, FA-18C, F-15C, F-15E, F-14, Eurofighter, etc.)
        ["{C8E06185-7CD6-4C90-959F-044679E90751}"] = clsid_map.nato_bvr, -- AIM-120C
        ["{444BA8AE-82A7-4345-842E-76154EFCCA46}"] = clsid_map.nato_bvr, -- AIM-120B (F-16C / F-15E)
        ["{40EF17B7-F508-45de-8566-6FFECC0C1AB8}"] = clsid_map.nato_bvr, -- AIM-120B (F-15C / FA-18C)
        ["LAU-115_2*LAU-127_AIM-120C"]           = clsid_map.nato_bvr, -- FA-18C twin AMRAAM
        ["{LAU-115 - AIM-120C}"]                  = clsid_map.nato_bvr, -- FA-18C LAU-115 AMRAAM
        ["{LAU-115 - AIM-120C_R}"]                = clsid_map.nato_bvr,
        -- NATO WVR (AIM-9X / AIM-9M)
        ["{5CE2FF2A-645A-4197-B48D-8720AC69394F}"] = clsid_map.nato_wvr, -- AIM-9X
        ["{6CEB49FC-DED8-4DED-B053-E1F033FF72D3}"] = clsid_map.nato_wvr, -- AIM-9M
        ["{9BFD8C90-F7AE-4e90-833B-BFD0CED0E536}"] = clsid_map.nato_wvr, -- AIM-9M (F-15C / F-16C)
        ["LAU-115_LAU-127_AIM-9X"]                = clsid_map.nato_wvr, -- FA-18C AIM-9X
        -- French M-2000C Magic II & Super 530D
        ["{MMagicII}"]                             = clsid_map.french_all,
        ["{Matra_S530D}"]                          = clsid_map.french_all,
        -- Eastern / Russian / Chinese BVR & WVR (R-77 / R-27ER / R-73 / JF-17 SD-10 / PL-5EII)
        ["{B4C01D60-A8A3-4237-BD72-CA7655BC0FE9}"] = clsid_map.east_bvr, -- R-77 (J-11A / MiG-29S)
        ["{E8069896-8435-4B90-95C0-01A03AE6E400}"] = clsid_map.east_bvr, -- R-27ER (Su-27 / Su-33 / J-11A / MiG-29)
        ["{FBC29BFE-3D24-4C64-B81D-941239D12249}"] = clsid_map.east_bvr, -- R-73 (Su-27 / Su-33 / J-11A / MiG-29)
        ["DIS_SD-10"]                              = clsid_map.east_bvr, -- JF-17 SD-10
        ["DIS_PL-5EII"]                            = clsid_map.nato_wvr, -- JF-17 PL-5EII
        -- Air-to-Ground / SEAD / Cruise / Glide Bomb anchors
        ["{B06DD79A-F21E-4EB9-BD9D-AB3844618C93}"] = clsid_map.ag_all,   -- AGM-88C HARM (F-16C / FA-18C)
        ["{F16A4DE0-116C-4A71-97F0-2CF85B0313EC}"] = clsid_map.ag_all,   -- AGM-84 / Harpoon
        ["{BCE4E030-38E9-423E-98ED-24BE3DA87C32}"] = clsid_map.ag_all,   -- Mk-82
        ["{DB769D48-67D7-42ED-A2BE-108D566C8B1E}"] = clsid_map.ag_all,   -- GBU-12
        ["{GBU-38}"]                               = clsid_map.ag_all,   -- GBU-38 JDAM
        ["{GBU-31}"]                               = clsid_map.ag_all,   -- GBU-31 JDAM
        ["{AGM-154A}"]                             = clsid_map.ag_all,   -- AGM-154A JSOW
        ["DIS_LD-10"]                              = clsid_map.ag_all,   -- JF-17 LD-10
        ["DIS_C-802AK"]                            = clsid_map.ag_all,   -- JF-17 C-802AK
        ["{FAB_250_DUAL_L}"]                       = clsid_map.ag_all,   -- Ru Flanker A-G
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

if log and log.write then
    log.write("NextGen_BVR_Armory", log.INFO, "Loaded v6.0.0: 262 weapons, 11 air defense units, 81 EDM shapes")
end

plugin_done()
