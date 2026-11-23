-- NextGen Air Defense Ground Units (DCS World 2.9+ Modular Tech Vehicles)
-- Uses authentic GT/WS/LN architecture verified from HEMTT_C-RAM_Phalanx, CHAP_TorM2, NASAMS & Patriot:
-- Centurion C-RAM, Iron Dome (20-cell Tamir + EL/M-2084), IRIS-T SLM, SAMP/T Aster-30 B1NT, Pantsir-SM, Patriot PAC-3 MSE & KEKA Pad!

local function make_radar_channel(opts)
    return {
        LN = {
            {
                ECM_K = opts.ecm_k or 0.35,
                beamWidth = opts.beam_width or math.rad(120),
                distanceMax = opts.dist_max,
                distanceMin = opts.dist_min or 100,
                frequencyRange = opts.freq or { 2000000000, 4000000000 },
                max_number_of_missiles_channels = opts.channels or 1,
                max_trg_alt = opts.max_alt or 25000,
                min_trg_alt = opts.min_alt or 2,
                reactionTime = opts.reaction or 1.0,
                reflection_limit = opts.refl_limit or 0.008,
                type = opts.ln_type or 102,
            },
        },
        angles = { { math.pi, -math.pi, math.rad(-5), math.rad(82) } },
        pos = opts.pos or { 0, 3.0, 0 },
        omegaY = 3.0,
        omegaZ = 3.0,
        pidY = { p = 80, i = 1.0, d = 10, inn = 10 },
        pidZ = { p = 80, i = 1.0, d = 10, inn = 10 },
    }
end

local function make_missile_br(count)
    local br = {}
    for i = 1, count do
        table.insert(br, { connector_name = string.format("POINT_MISSILE_%02d", i) })
    end
    return br
end

local function base_vehicle_skeleton(spec)
    local GT = {}
    GT_t.ws = 0
    GT.Name = spec.id
    GT.DisplayName = _(spec.display_name)
    GT.DisplayNameShort = spec.short_name
    GT.type = spec.id
    GT.Rate = spec.rate or 20
    GT.category = "Air Defence"
    GT.tags = spec.tags or { "Air Defence", "SAM SHORAD" }
    GT.MaxSpeed = spec.max_speed or 0
    GT.Crew = 0
    GT.DetectionRange = spec.det_range
    GT.ThreatRange = spec.threat_range
    GT.ThreatRangeMin = spec.threat_min or 100
    GT.airWeaponDist = spec.threat_range
    GT.IR_emission_coeff = 0.08
    GT.EPLRS = true
    GT.Waypoint_Custom_Panel = true
    GT.enablePlayerCanDrive = false
    GT.swing_on_run = false
    GT.swapped_names = true
    GT.defaultStartAlarmState = 2
    GT.mapclasskey = spec.mapclass or "P0091000087"
    GT.Countries = { "USA", "Israel", "France", "Germany", "UK", "Ukraine", "Russia", "China", "Combined Joint Task Forces Blue", "Combined Joint Task Forces Red" }

    GT.chassis = {
        life = spec.life or 6,
    }

    GT.armour_scheme = {
        hull_azimuth = { {} },
        hull_elevation = { {} },
        turret_azimuth = { {} },
        turret_elevation = { {} },
    }

    GT.sensor = {
        height = spec.sensor_height or 4.0,
        max_alt_finding_target = spec.max_alt or 25000,
        max_range_finding_target = spec.det_range,
        min_alt_finding_target = 0,
        min_range_finding_target = 0,
    }

    GT.Sensors = spec.sensors
    GT.animation_arguments = spec.anim_args or {}
    GT.radar_rotation_period = spec.radar_period or 1.5

    GT.shape_table_data = {
        {
            file = spec.shape,
            life = spec.life or 6,
            username = spec.id,
            name = spec.id,
            classname = "lLandVehicle",
            positioning = "BYNORMAL",
        },
    }

    GT.visual = {
        shape = spec.shape,
        shape_dstr = spec.shape,
        fire_size = 0.8,
        fire_pos = { 0, 1.2, 0 },
        fire_time = 400,
        max_time_agony = 60,
        min_time_agony = 5,
        agony_explosion_size = 5,
    }

    GT.snd = {
        radarRotation = "GndTech/RadarRotation",
    }

    GT.attribute = spec.attribute
    GT.WS = spec.ws
    add_surface_unit(GT)
end

local function register_air_defenses(sam_weapons)
    -- =====================================================================
    -- 1. Centurion C-RAM (Land-Based Phalanx 20mm CIWS)
    -- =====================================================================
    base_vehicle_skeleton({
        id = "NG_CRAM_Centurion",
        display_name = "Centurion C-RAM Phalanx CIWS (NextGen)",
        short_name = "C-RAM",
        shape = "ng_cram_centurion",
        det_range = 14000,
        threat_range = 2500,
        threat_min = 50,
        max_alt = 4000,
        radar_period = 1.0,
        sensors = { RADAR = "C_RAM_Phalanx" },
        mapclass = "SPAAA_RAD_Truck",
        tags = { "Air Defence", "SP AAA" },
        attribute = {
            wsType_Ground, wsType_SAM, wsType_Gun, WSTYPE_PLACEHOLDER,
            "AA_flak", "SAM TR", "Mobile AAA", "C-RAM", "Datalink",
            "All", "Ground Units", "Vehicles", "Ground vehicles",
            "NonAndLightArmoredUnits", "NonArmoredUnits",
            "Air Defence", "SAM related", "SAM elements", "Armed Air Defence",
            "Rocket Attack Valid AirDefence", "AAA",
        },
        ws = {
            maxTargetDetectionRange = 14000,
            radar_type = 104,
            searchRadarFrequencies = { { 12000000000, 18000000000 } },
            searchRadarMaxElevation = math.rad(82),
            {
                center = "CENTER_TOWER",
                pointer = "POINT_SIGHT_01",
                drawArgument1 = 0,
                drawArgument2 = 1,
                reference_angle_Y = 0,
                reference_angle_Z = 0,
                omegaY = 2.6,
                omegaZ = 2.2,
                pidY = { p = 120, i = 2.0, d = 10, inn = 12 },
                pidZ = { p = 120, i = 2.0, d = 10, inn = 12 },
                angles = { { math.pi, -math.pi, math.rad(-15), math.rad(85) } },
                LN = {
                    {
                        type = 3,
                        reactionTime = 0.25,
                        reflection_limit = 0.008,
                        distanceMin = 50,
                        distanceMax = 2500,
                        max_trg_alt = 3500,
                        min_trg_alt = 0,
                        beamWidth = math.rad(180),
                        createMuzzleFlashEffect = true,
                        fireAnimationArgument = 23,
                        useTargetAccelInSight = true,
                        sensor = {},
                        BR = { { connector_name = "POINT_GUN_01" } },
                        PL = {
                            {
                                ammo_capacity = 1550,
                                portionAmmoCapacity = 1550,
                                reload_time = 120,
                                shot_delay = 0.0133, -- 4,500 RPM
                                switch_on_delay = 0.01,
                                shell_name = { "M246_20_HE_gr" },
                                shell_display_name = "20mm M246 HE-IT C-RAM",
                            },
                        },
                    },
                },
            },
        },
    })

    -- =====================================================================
    -- 2. Iron Dome MFR 20-Cell Tamir Launcher (Multi-Channel Anti-Rocket/Cruise/Air)
    -- =====================================================================
    local id_ws = {
        maxTargetDetectionRange = 75000,
        radar_type = 104,
        searchRadarFrequencies = { { 2000000000, 4000000000 } },
        searchRadarMaxElevation = math.rad(75),
    }
    for _ = 1, 4 do
        table.insert(id_ws, make_radar_channel({ dist_max = 75000, reaction = 0.9, refl_limit = 0.006, max_alt = 15000 }))
    end
    table.insert(id_ws, {
        center = "CENTER_TOWER",
        pointer = "POINT_SIGHT_01",
        drawArgument1 = 0,
        omegaY = 1.4,
        pidY = { p = 40, i = 0.5, d = 8, inn = 8 },
        angles = { { math.pi, -math.pi, math.rad(10), math.rad(80) } },
        LN = {
            {
                type = 4,
                reactionTime = 1.0,
                reflection_limit = 0.006,
                distanceMin = 400,
                distanceMax = 70000,
                max_trg_alt = 12000,
                min_trg_alt = 5,
                depends_on_unit = { { { "self", 1 } }, { { "self", 2 } }, { { "self", 3 } }, { { "self", 4 } }, { { "NG_IronDome_ELM2084" } } },
                sensor = {},
                BR = make_missile_br(20),
                PL = {
                    {
                        type_ammunition = sam_weapons["NG_SAM_TAMIR"].wsTypeOfWeapon,
                        name_ammunition = sam_weapons["NG_SAM_TAMIR"].user_name,
                        ammo_capacity = 20,
                        portionAmmoCapacity = 20,
                        reload_time = 600,
                        shot_delay = 0.45,
                    },
                },
            },
        },
    })
    base_vehicle_skeleton({
        id = "NG_IronDome_Launcher",
        display_name = "Iron Dome 20-Cell Tamir Launcher (NextGen)",
        short_name = "IronDome",
        shape = "ng_iron_dome_ln",
        det_range = 75000,
        threat_range = 70000,
        threat_min = 400,
        max_alt = 12000,
        sensors = { RADAR = "Tor 9A331" },
        tags = { "Air Defence", "SAM SHORAD" },
        attribute = {
            wsType_Ground, wsType_SAM, wsType_Miss, WSTYPE_PLACEHOLDER,
            "AA_missile", "SR SAM", "SAM SR", "SAM TR", "C-RAM", "Datalink",
            "All", "Ground Units", "Vehicles", "Ground vehicles",
            "NonAndLightArmoredUnits", "NonArmoredUnits",
            "Air Defence", "SAM related", "SAM elements", "Armed Air Defence",
        },
        ws = id_ws,
    })

    -- =====================================================================
    -- 3. IAI EL/M-2084 MMR S-Band AESA Search Radar
    -- =====================================================================
    base_vehicle_skeleton({
        id = "NG_IronDome_ELM2084",
        display_name = "EL/M-2084 MMR Iron Dome Radar (NextGen)",
        short_name = "ELM-2084",
        shape = "ng_iron_dome_radar",
        det_range = 250000,
        threat_range = 0,
        max_alt = 40000,
        max_speed = 65.0,
        radar_period = 1.6,
        anim_args = { locator_rotation = 11 },
        sensors = { RADAR = "NASAMS_Radar_MPQ64F1" },
        tags = { "Air Defence", "SAM SR" },
        mapclass = "P0091000083",
        attribute = {
            wsType_Ground, wsType_SAM, wsType_Radar, WSTYPE_PLACEHOLDER,
            "SAM SR", "EWR", "Datalink", "All", "Ground Units", "Vehicles",
            "Ground vehicles", "NonAndLightArmoredUnits", "NonArmoredUnits",
            "Air Defence", "SAM related", "SAM elements",
        },
        ws = {
            maxTargetDetectionRange = 250000,
            radar_type = 101,
            searchRadarFrequencies = { { 2000000000, 4000000000 } },
            searchRadarMaxElevation = math.rad(70),
            make_radar_channel({ ln_type = 101, dist_max = 250000, reaction = 1.5, refl_limit = 0.005, max_alt = 40000 }),
            make_radar_channel({ ln_type = 101, dist_max = 250000, reaction = 1.5, refl_limit = 0.005, max_alt = 40000 }),
        },
    })

    -- =====================================================================
    -- 4. Diehl IRIS-T SLM 8-Cell VLS Battery Truck
    -- =====================================================================
    local ir_ws = {
        maxTargetDetectionRange = 60000,
        radar_type = 104,
        searchRadarFrequencies = { { 4000000000, 8000000000 } },
    }
    for _ = 1, 3 do
        table.insert(ir_ws, make_radar_channel({ dist_max = 60000, reaction = 1.1, refl_limit = 0.01, max_alt = 20000 }))
    end
    table.insert(ir_ws, {
        center = "CENTER_TOWER",
        pointer = "POINT_SIGHT_01",
        angles = { { math.pi, -math.pi, 0, math.rad(90) } },
        LN = {
            {
                type = 4,
                reactionTime = 1.2,
                reflection_limit = 0.01,
                distanceMin = 400,
                distanceMax = 45000,
                max_trg_alt = 20000,
                min_trg_alt = 5,
                depends_on_unit = { { { "self", 1 } }, { { "self", 2 } }, { { "self", 3 } }, { { "NG_TRML_4D_Radar" } } },
                sensor = {},
                BR = make_missile_br(8),
                PL = {
                    {
                        type_ammunition = sam_weapons["NG_SAM_IRIST_SLM"].wsTypeOfWeapon,
                        name_ammunition = sam_weapons["NG_SAM_IRIST_SLM"].user_name,
                        ammo_capacity = 8,
                        portionAmmoCapacity = 8,
                        reload_time = 480,
                        shot_delay = 0.6,
                    },
                },
            },
        },
    })
    base_vehicle_skeleton({
        id = "NG_IRIST_SLM_Launcher",
        display_name = "IRIS-T SLM 8-Cell VLS Truck (NextGen)",
        short_name = "IRIS-TSLM",
        shape = "ng_irist_slm_ln",
        det_range = 60000,
        threat_range = 45000,
        threat_min = 400,
        max_alt = 20000,
        max_speed = 70.0,
        sensors = { RADAR = "Tor 9A331" },
        tags = { "Air Defence", "SAM SHORAD" },
        attribute = {
            wsType_Ground, wsType_SAM, wsType_Miss, WSTYPE_PLACEHOLDER,
            "AA_missile", "MR SAM", "SAM SR", "SAM TR", "Datalink",
            "All", "Ground Units", "Vehicles", "Ground vehicles",
            "NonAndLightArmoredUnits", "NonArmoredUnits",
            "Air Defence", "SAM related", "SAM elements", "Armed Air Defence",
        },
        ws = ir_ws,
    })

    -- =====================================================================
    -- 5. Eurosam SAMP/T Aster 30 B1NT 8-Cell VLS
    -- =====================================================================
    local st_ws = {
        maxTargetDetectionRange = 180000,
        radar_type = 102,
        searchRadarFrequencies = { { 4000000000, 12000000000 } },
    }
    for _ = 1, 4 do
        table.insert(st_ws, make_radar_channel({ dist_max = 180000, reaction = 1.5, refl_limit = 0.01, max_alt = 30000 }))
    end
    table.insert(st_ws, {
        center = "CENTER_TOWER",
        pointer = "POINT_SIGHT_01",
        angles = { { math.pi, -math.pi, 0, math.rad(90) } },
        LN = {
            {
                type = 4,
                reactionTime = 1.5,
                reflection_limit = 0.01,
                distanceMin = 1200,
                distanceMax = 150000,
                max_trg_alt = 25000,
                min_trg_alt = 10,
                depends_on_unit = { { { "self", 1 } }, { { "self", 2 } }, { { "self", 3 } }, { { "self", 4 } } },
                sensor = {},
                BR = make_missile_br(8),
                PL = {
                    {
                        type_ammunition = sam_weapons["NG_SAM_ASTER30"].wsTypeOfWeapon,
                        name_ammunition = sam_weapons["NG_SAM_ASTER30"].user_name,
                        ammo_capacity = 8,
                        portionAmmoCapacity = 8,
                        reload_time = 600,
                        shot_delay = 0.7,
                    },
                },
            },
        },
    })
    base_vehicle_skeleton({
        id = "NG_SAMPT_Aster30_Launcher",
        display_name = "SAMP/T Aster 30 B1NT 8-Cell VLS (NextGen)",
        short_name = "SAMP/T",
        shape = "ng_sampt_aster30",
        det_range = 180000,
        threat_range = 150000,
        threat_min = 1200,
        max_alt = 30000,
        max_speed = 70.0,
        sensors = { RADAR = "Patriot str" },
        tags = { "Air Defence", "SAM" },
        attribute = {
            wsType_Ground, wsType_SAM, wsType_Miss, WSTYPE_PLACEHOLDER,
            "AA_missile", "LR SAM", "SAM SR", "SAM TR", "Datalink",
            "All", "Ground Units", "Vehicles", "Ground vehicles",
            "NonAndLightArmoredUnits", "NonArmoredUnits",
            "Air Defence", "SAM related", "SAM elements", "Armed Air Defence",
        },
        ws = st_ws,
    })

    -- =====================================================================
    -- 6. Pantsir-SM (96K6 Hybrid 12x 57E6M + Twin 30mm 2A38M SPAAGM)
    -- =====================================================================
    base_vehicle_skeleton({
        id = "NG_Pantsir_SM",
        display_name = "Pantsir-SM 96K6 SPAAGM (NextGen)",
        short_name = "PantsirSM",
        shape = "ng_pantsir_sm",
        det_range = 45000,
        threat_range = 32000,
        threat_min = 200,
        max_alt = 18000,
        max_speed = 75.0,
        radar_period = 1.8,
        anim_args = { locator_rotation = 11 },
        sensors = { RADAR = "Tor 9A331" },
        tags = { "Air Defence", "SAM SHORAD" },
        attribute = {
            wsType_Ground, wsType_SAM, wsType_MissGun, WSTYPE_PLACEHOLDER,
            "AA_missile", "AA_flak", "SR SAM", "SAM SR", "SAM TR", "C-RAM",
            "All", "Ground Units", "Vehicles", "Ground vehicles",
            "NonAndLightArmoredUnits", "NonArmoredUnits",
            "Air Defence", "SAM related", "SAM elements", "Armed Air Defence",
            "Rocket Attack Valid AirDefence", "AAA",
        },
        ws = {
            maxTargetDetectionRange = 45000,
            radar_type = 104,
            searchRadarFrequencies = { { 2000000000, 18000000000 } },
            make_radar_channel({ dist_max = 45000, reaction = 0.8, refl_limit = 0.008, max_alt = 18000 }),
            make_radar_channel({ dist_max = 45000, reaction = 0.8, refl_limit = 0.008, max_alt = 18000 }),
            {
                center = "CENTER_TOWER",
                pointer = "POINT_SIGHT_01",
                drawArgument1 = 0,
                drawArgument2 = 1,
                omegaY = 1.6,
                omegaZ = 1.4,
                pidY = { p = 90, i = 1.5, d = 9, inn = 10 },
                pidZ = { p = 90, i = 1.5, d = 9, inn = 10 },
                angles = { { math.pi, -math.pi, math.rad(-5), math.rad(82) } },
                LN = {
                    {
                        type = 4,
                        reactionTime = 1.0,
                        reflection_limit = 0.008,
                        distanceMin = 600,
                        distanceMax = 32000,
                        max_trg_alt = 18000,
                        min_trg_alt = 5,
                        depends_on_unit = { { { "self", 1 } }, { { "self", 2 } } },
                        sensor = {},
                        BR = make_missile_br(12),
                        PL = {
                            {
                                type_ammunition = sam_weapons["NG_SAM_57E6M"].wsTypeOfWeapon,
                                name_ammunition = sam_weapons["NG_SAM_57E6M"].user_name,
                                ammo_capacity = 12,
                                portionAmmoCapacity = 12,
                                reload_time = 600,
                                shot_delay = 0.5,
                            },
                        },
                    },
                    {
                        type = 3,
                        reactionTime = 0.4,
                        reflection_limit = 0.008,
                        distanceMin = 100,
                        distanceMax = 4000,
                        max_trg_alt = 3000,
                        min_trg_alt = 0,
                        createMuzzleFlashEffect = true,
                        useTargetAccelInSight = true,
                        sensor = {},
                        BR = {
                            { connector_name = "POINT_GUN_01" },
                            { connector_name = "POINT_GUN_02" },
                        },
                        PL = {
                            {
                                ammo_capacity = 1400,
                                portionAmmoCapacity = 1400,
                                reload_time = 240,
                                shot_delay = 0.024, -- Dual 30mm 2A38M 2500 rpm combined
                                shell_name = { "2A38_30_AP", "2A38_30_HE" },
                            },
                        },
                    },
                },
            },
        },
    })

    -- =====================================================================
    -- 7. Patriot M903 PAC-3 MSE 16-Cell Quad-Pack ABM Launcher
    -- =====================================================================
    local pat_ws = {
        maxTargetDetectionRange = 160000,
        radar_type = 102,
        searchRadarFrequencies = { { 4480000000, 5450000000 } },
    }
    for _ = 1, 4 do
        table.insert(pat_ws, make_radar_channel({ dist_max = 160000, reaction = 1.8, refl_limit = 0.01, max_alt = 35000 }))
    end
    table.insert(pat_ws, {
        center = "CENTER_TOWER",
        drawArgument1 = 0,
        omegaY = 0.7,
        pidY = { p = 20, i = 0.2, d = 6, inn = 6 },
        angles = { { math.pi, -math.pi, 0, math.rad(85) } },
        LN = {
            {
                type = 4,
                reactionTime = 1.8,
                reflection_limit = 0.01,
                distanceMin = 1000,
                distanceMax = 120000,
                max_trg_alt = 35000,
                min_trg_alt = 15,
                depends_on_unit = { { { "self", 1 } }, { { "self", 2 } }, { { "self", 3 } }, { { "self", 4 } }, { { "Patriot str" } } },
                sensor = {},
                BR = make_missile_br(16),
                PL = {
                    {
                        type_ammunition = sam_weapons["NG_SAM_PAC3_MSE"].wsTypeOfWeapon,
                        name_ammunition = sam_weapons["NG_SAM_PAC3_MSE"].user_name,
                        ammo_capacity = 16,
                        portionAmmoCapacity = 16,
                        reload_time = 900,
                        shot_delay = 0.6,
                    },
                },
            },
        },
    })
    base_vehicle_skeleton({
        id = "NG_Patriot_PAC3_MSE_LN",
        display_name = "Patriot M903 PAC-3 MSE 16-Cell (NextGen)",
        short_name = "M903-PAC3",
        shape = "ng_patriot_pac3_ln",
        det_range = 160000,
        threat_range = 120000,
        threat_min = 1000,
        max_alt = 35000,
        sensors = { RADAR = "Patriot str" },
        tags = { "Air Defence", "SAM" },
        attribute = {
            wsType_Ground, wsType_SAM, wsType_Miss, WSTYPE_PLACEHOLDER,
            "AA_missile", "LR SAM", "SAM SR", "SAM TR", "Datalink",
            "All", "Ground Units", "Vehicles", "Ground vehicles",
            "NonAndLightArmoredUnits", "NonArmoredUnits",
            "Air Defence", "SAM related", "SAM elements", "Armed Air Defence",
        },
        ws = pat_ws,
    })

    -- =====================================================================
    -- 8. KEKA Aerospace Mobile Launch Rail ("Troposphere Pad" Troll SAM!)
    -- =====================================================================
    base_vehicle_skeleton({
        id = "NG_KEKA_LaunchPad",
        display_name = "KEKA Aerospace Troposphere Pad (Troll SAM!)",
        short_name = "KEKA-Pad",
        shape = "ng_keka_launcher",
        det_range = 80000,
        threat_range = 95000,
        threat_min = 600,
        max_alt = 35000,
        max_speed = 35.0,
        sensors = { RADAR = "Tor 9A331" },
        tags = { "Air Defence", "SAM SHORAD" },
        attribute = {
            wsType_Ground, wsType_SAM, wsType_Miss, WSTYPE_PLACEHOLDER,
            "AA_missile", "MR SAM", "SAM SR", "SAM TR",
            "All", "Ground Units", "Vehicles", "Ground vehicles",
            "NonAndLightArmoredUnits", "NonArmoredUnits",
            "Air Defence", "SAM related", "SAM elements", "Armed Air Defence",
        },
        ws = {
            maxTargetDetectionRange = 80000,
            radar_type = 104,
            make_radar_channel({ dist_max = 80000, reaction = 2.2, refl_limit = 0.02, max_alt = 35000 }),
            {
                center = "CENTER_TOWER",
                pointer = "POINT_SIGHT_01",
                drawArgument1 = 0,
                omegaY = 0.65,
                pidY = { p = 15, i = 0.1, d = 4, inn = 5 },
                angles = { { math.pi, -math.pi, 0, math.rad(85) } },
                LN = {
                    {
                        type = 4,
                        reactionTime = 2.2,
                        reflection_limit = 0.02,
                        distanceMin = 600,
                        distanceMax = 95000,
                        max_trg_alt = 35000,
                        min_trg_alt = 20,
                        depends_on_unit = { { { "self", 1 } } },
                        sensor = {},
                        BR = { { connector_name = "POINT_MISSILE_01" } },
                        PL = {
                            {
                                type_ammunition = sam_weapons["NG_SAM_KEKA_T6"].wsTypeOfWeapon,
                                name_ammunition = sam_weapons["NG_SAM_KEKA_T6"].user_name,
                                ammo_capacity = 4,
                                portionAmmoCapacity = 1,
                                reload_time = 12,
                                shot_delay = 1.5,
                            },
                        },
                    },
                },
            },
        },
    })

    -- =====================================================================
    -- 9. Hensoldt TRML-4D C-Band AESA Search & Track Radar (IRIS-T SLM)
    -- =====================================================================
    base_vehicle_skeleton({
        id = "NG_TRML_4D_Radar",
        display_name = "TRML-4D AESA Air Surveillance Radar (NextGen)",
        short_name = "TRML-4D",
        shape = "ng_trml_4d_radar",
        det_range = 250000,
        threat_range = 0,
        max_alt = 40000,
        max_speed = 70.0,
        radar_period = 1.4,
        anim_args = { locator_rotation = 11 },
        sensors = { RADAR = "NASAMS_Radar_MPQ64F1" },
        tags = { "Air Defence", "SAM SR" },
        mapclass = "P0091000083",
        attribute = {
            wsType_Ground, wsType_SAM, wsType_Radar, WSTYPE_PLACEHOLDER,
            "SAM SR", "EWR", "Datalink", "All", "Ground Units", "Vehicles",
            "Ground vehicles", "NonAndLightArmoredUnits", "NonArmoredUnits",
            "Air Defence", "SAM related", "SAM elements",
        },
        ws = {
            maxTargetDetectionRange = 250000,
            radar_type = 101,
            searchRadarFrequencies = { { 4000000000, 8000000000 } },
            searchRadarMaxElevation = math.rad(70),
            make_radar_channel({ ln_type = 101, dist_max = 250000, reaction = 1.2, refl_limit = 0.005, max_alt = 40000 }),
            make_radar_channel({ ln_type = 101, dist_max = 250000, reaction = 1.2, refl_limit = 0.005, max_alt = 40000 }),
        },
    })

    -- =====================================================================
    -- 10. THAAD 8-Tube HEMTT Exo-Atmospheric ABM Launcher
    -- =====================================================================
    local thaad_ws = {
        maxTargetDetectionRange = 240000,
        radar_type = 102,
        searchRadarFrequencies = { { 8000000000, 12000000000 } },
    }
    for _ = 1, 4 do
        table.insert(thaad_ws, make_radar_channel({ dist_max = 240000, reaction = 2.0, refl_limit = 0.008, max_alt = 150000 }))
    end
    table.insert(thaad_ws, {
        center = "CENTER_TOWER",
        pointer = "POINT_SIGHT_01",
        angles = { { math.pi, -math.pi, 0, math.rad(88) } },
        LN = {
            {
                type = 4,
                reactionTime = 2.0,
                reflection_limit = 0.008,
                distanceMin = 5000,
                distanceMax = 200000,
                max_trg_alt = 150000,
                min_trg_alt = 500,
                depends_on_unit = { { { "self", 1 } }, { { "self", 2 } }, { { "self", 3 } }, { { "self", 4 } }, { { "Patriot str" } } },
                sensor = {},
                BR = make_missile_br(8),
                PL = {
                    {
                        type_ammunition = sam_weapons["NG_SAM_THAAD"].wsTypeOfWeapon,
                        name_ammunition = sam_weapons["NG_SAM_THAAD"].user_name,
                        ammo_capacity = 8,
                        portionAmmoCapacity = 8,
                        reload_time = 1200,
                        shot_delay = 1.0,
                    },
                },
            },
        },
    })
    base_vehicle_skeleton({
        id = "NG_THAAD_Launcher",
        display_name = "THAAD M1120 8-Tube Exo-ABM TEL (NextGen)",
        short_name = "THAAD",
        shape = "ng_thaad_ln",
        det_range = 240000,
        threat_range = 200000,
        threat_min = 5000,
        max_alt = 150000,
        max_speed = 65.0,
        sensors = { RADAR = "Patriot str" },
        tags = { "Air Defence", "SAM" },
        attribute = {
            wsType_Ground, wsType_SAM, wsType_Miss, WSTYPE_PLACEHOLDER,
            "AA_missile", "LR SAM", "SAM SR", "SAM TR", "Datalink",
            "All", "Ground Units", "Vehicles", "Ground vehicles",
            "NonAndLightArmoredUnits", "NonArmoredUnits",
            "Air Defence", "SAM related", "SAM elements", "Armed Air Defence",
        },
        ws = thaad_ws,
    })

    -- =====================================================================
    -- 11. S-400 Triumf 5P85SM2 4-Tube 40N6 Long-Range ABM TEL
    -- =====================================================================
    local s400_ws = {
        maxTargetDetectionRange = 400000,
        radar_type = 102,
        searchRadarFrequencies = { { 2000000000, 4000000000 } },
    }
    for _ = 1, 4 do
        table.insert(s400_ws, make_radar_channel({ dist_max = 400000, reaction = 2.0, refl_limit = 0.01, max_alt = 35000 }))
    end
    table.insert(s400_ws, {
        center = "CENTER_TOWER",
        pointer = "POINT_SIGHT_01",
        angles = { { math.pi, -math.pi, 0, math.rad(90) } },
        LN = {
            {
                type = 4,
                reactionTime = 2.0,
                reflection_limit = 0.01,
                distanceMin = 5000,
                distanceMax = 380000,
                max_trg_alt = 35000,
                min_trg_alt = 10,
                depends_on_unit = { { { "self", 1 } }, { { "self", 2 } }, { { "self", 3 } }, { { "self", 4 } } },
                sensor = {},
                BR = make_missile_br(4),
                PL = {
                    {
                        type_ammunition = sam_weapons["NG_SAM_40N6"].wsTypeOfWeapon,
                        name_ammunition = sam_weapons["NG_SAM_40N6"].user_name,
                        ammo_capacity = 4,
                        portionAmmoCapacity = 4,
                        reload_time = 1400,
                        shot_delay = 1.2,
                    },
                },
            },
        },
    })
    base_vehicle_skeleton({
        id = "NG_S400_TEL",
        display_name = "S-400 Triumf 5P85SM2 40N6 TEL (NextGen)",
        short_name = "S-400-TEL",
        shape = "ng_s400_tel",
        det_range = 400000,
        threat_range = 380000,
        threat_min = 5000,
        max_alt = 35000,
        max_speed = 60.0,
        sensors = { RADAR = "Tor 9A331" },
        tags = { "Air Defence", "SAM" },
        attribute = {
            wsType_Ground, wsType_SAM, wsType_Miss, WSTYPE_PLACEHOLDER,
            "AA_missile", "LR SAM", "SAM SR", "SAM TR", "Datalink",
            "All", "Ground Units", "Vehicles", "Ground vehicles",
            "NonAndLightArmoredUnits", "NonArmoredUnits",
            "Air Defence", "SAM related", "SAM elements", "Armed Air Defence",
        },
        ws = s400_ws,
    })
end

return register_air_defenses
