-- NextGen Heavy Arsenal: Ballistic, Anti-Ship, SEAD, Bunker-Busters, Stealth Cruise, Drones, KEKA Troll & Special AAMs
-- Uses physically calibrated Mach-indexed polars (polar_profiles.lua) + DrawArg 25 (wing fold) & DrawArg 407 (propeller spin).

local polar = dofile(current_mod_path .. "/Database/polar_profiles.lua")

local function deep_copy(orig)
    if type(orig) ~= "table" then return orig end
    local copy = {}
    for k, v in pairs(orig) do
        copy[deep_copy(k)] = deep_copy(v)
    end
    return copy
end

-- Base Air-to-Surface / Ballistic / SEAD / Supersonic template (anti_rad_missile.sch)
local BASE_AS_TEMPLATE = {
    category = CAT_MISSILES,
    caliber = 0.254,
    mass = 450.0,
    model = "ng_kh31_ramjet",
    sounderName = "Weapons/Missile",
    targeting_data = { fm_type = -1 },
    type_name = "missile",
    wsTypeOfWeapon = { wsType_Weapon, wsType_Missile, wsType_AS_Missile, WSTYPE_PLACEHOLDER },

    Escort = 0,
    Head_Type = 5,
    sigma = { 4, 4, 4 },
    M = 450.0,
    H_max = 35000,
    H_min = 1,
    H_min_t = 0,
    Diam = 254,
    Cx_pil = 2.4,
    D_max = 180000,
    D_min = 1500,
    Head_Form = 1,
    Life_Time = 900,
    Nr_max = 12,
    v_min = 120,
    v_mid = 320,
    Mach_max = 1.2,
    t_b = 0.2,
    t_acc = 2.5,
    t_marsh = 120.0,
    Range_max = 250000,
    Fi_start = 1.2,
    Fi_rak = 3.14152,
    Fi_excort = 1.5,
    Fi_search = 1.5,
    OmViz_max = 0.4,
    PN_gain = 4,
    Reflection = 0.02,
    SeekerGen = 4,
    KillDistance = 0,
    X_back = -2.2,
    Y_back = 0,
    Z_back = 0,
    ccm_k0 = 0.05,
    hoj = 0,
    loft = 0,
    nozzle_exit_area = 0.015,
    scheme = "schemes/missiles/anti_rad_missile.sch",
    class_name = "wAmmunitionSelfHoming",

    controller = { boost_start = 0, march_start = 1.5 },
    exhaust = { 0.7, 0.7, 0.7, 0.04 },

    boost = {
        custom_smoke_dissipation_factor = 0.2,
        fuel_mass = 25.0,
        impulse = 235,
        nozzle_exit_area = 0.015,
        nozzle_orientationXYZ = { { 0, 0, 0 } },
        nozzle_position = { { -2.2, 0, 0 } },
        smoke_color = { 0.85, 0.85, 0.85 },
        smoke_transparency = 0.10,
        tail_width = 0.40,
        work_time = 2.0,
    },

    march = {
        custom_smoke_dissipation_factor = 0.1,
        fuel_mass = 120.0,
        impulse = 300,
        nozzle_exit_area = 0.015,
        nozzle_orientationXYZ = { { 0, 0, 0 } },
        nozzle_position = { { -2.2, 0, 0 } },
        smoke_color = { 0.85, 0.85, 0.85 },
        smoke_opacity_type = 1,
        smoke_transparency = 0.04,
        tail_width = 0.25,
        work_time = 120.0,
    },

    actuator = {
        D = 200, T1 = 0.005, T2 = 0.01, Tf = 0.01,
        fin_stall = 1, max_delta = 0.35, max_omega = 5.0, sim_count = 4,
    },

    autopilot = {
        Areq_limit = 12, K_heading_hor = 0.5, K_heading_ver = 0.3, K_loft = 2.8,
        Kconv = 3, Kd = 0.24, Ki = 0.01, Knv = 0.0024, Kout = 1, Krx = 2, Kx = 0.04,
        PN_dist_data = { 15000, 1, 5000, 1 },
        alg = 0, bang_bang = 0, delay = 1.0,
        fins_limit = 0.35, fins_limit_x = 0.087,
        loft_active_by_default = 0,
        max_pitch_cmd = 0.55, max_signal_Fi = 0.25,
        min_a_conv_approach_vel = 80, min_horiz_time = 2,
        null_roll = 0.785398, op_time = 900, rotate_fins_output = 0, x_channel_delay = 1,
    },

    fm = deep_copy(polar.FM_HYPERSONIC),

    seeker = {
        FOV = 2.09, abs_err_val = 2, aim_sigma = 3, aim_y_offset = 1.5,
        ang_err_val = 0.00014, blind_rad_val = 1, calc_aim_dist = 500000,
        delay = 1.2, err_correct_time = 2,
        guide_to_last_pos = true, keep_aim_time = 5,
        lock_manual_target_types_only = 0,
        max_w_LOS = 0.35, op_time = 900, pos_memory_time = 300,
        sens_far_dist = 150000, sens_near_dist = 80,
    },

    proximity_fuze = { arm_delay = 1.5, radius = 6 },
    warhead = {
        caliber = 254, concrete_factors = { 2.0, 2.0, 1.5 }, concrete_obj_factor = 2.0,
        cumulative_factor = 1.5, cumulative_thickness = 0.25, expl_mass = 120.0, fantom = 1,
        mass = 120.0, obj_factors = { 2.0, 2.0 }, other_factors = { 1.5, 1.5, 1.5 }, piercing_mass = 35.0,
    },
    warhead_air = {
        caliber = 254, concrete_factors = { 1, 1, 1 }, concrete_obj_factor = 0,
        cumulative_factor = 0, cumulative_thickness = 0, expl_mass = 120.0, fantom = 1,
        mass = 120.0, obj_factors = { 1, 1 }, other_factors = { 1, 1, 1 }, piercing_mass = 20.0,
    },
}

-- Folding-wing Cruise, Glide, Drone & Sea-Skimmer Template (sat_cruise_missile.sch)
local BASE_CRUISE_FOLDING = {
    category = CAT_MISSILES,
    caliber = 0.480,
    mass = 1300.0,
    model = "ng_stealth_cruise",
    sounderName = "Weapons/Missile",
    targeting_data = { fm_type = -1 },
    type_name = "missile",
    wsTypeOfWeapon = { wsType_Weapon, wsType_Missile, wsType_AS_Missile, WSTYPE_PLACEHOLDER },

    Escort = 0, Head_Type = 5, Head_Form = 0, sigma = { 10, 10, 10 }, M = 1300.0,
    H_max = 15000, H_min = -1, H_min_t = 0, Diam = 480, Cx_pil = 6.0,
    D_max = 560000, D_min = 3000, Life_Time = 1800, Nr_max = 8,
    v_min = 140, v_mid = 235, Mach_max = 0.95, t_b = 0, t_acc = 4, t_marsh = 1800,
    Range_max = 560000, Fi_start = 0.7, Fi_rak = 3.14152, Fi_excort = 0.7,
    Fi_search = 99.9, OmViz_max = 99.9, Reflection = 0.04, KillDistance = 0,
    X_back = -2.55, Y_back = 0, Z_back = 0,
    scheme = "schemes/missiles/sat_cruise_missile.sch",
    class_name = "wAmmunitionSelfHoming",
    play_booster_animation = { val = 0 },
    booster_animation = { start_val = 0 },
    encyclopediaAnimation = { args = { [25] = 1 } },

    controller = { boost_start = 0, march_start = 0.8 },
    boost = {
        boost_factor = 0, boost_time = 0, custom_smoke_dissipation_factor = 0,
        fuel_mass = 0, impulse = 0, nozzle_orientationXYZ = { { 0, 0, 0 } },
        nozzle_position = { { 0, 0, 0 } }, smoke_color = { 0, 0, 0 },
        smoke_transparency = 0, tail_width = 0, work_time = 0,
    },
    march = {
        custom_smoke_dissipation_factor = 0.2, fuel_mass = 280, impulse = 3000,
        max_thrust = 3200, min_fuel_rate = 0.005, min_thrust = -100,
        nozzle_orientationXYZ = { { 0, 0, 0 } }, nozzle_position = { { -2.4, 0, 0 } },
        smoke_color = { 0.6, 0.6, 0.6 }, smoke_transparency = 0.02,
        tail_width = 0.35, thrust_Tau = 0.0017, work_time = 9999,
    },
    control_block = {
        can_update_target_pos = 1, default_cruise_height = 60, obj_sensor = 0,
        seeker_activation_dist = 18000, turn_before_point_reach = 1,
        turn_hor_N = 1.4, turn_max_calc_angle_deg = 90, turn_point_trigger_dist = 250, use_horiz_dist = 1,
    },
    cruise_autopilot = {
        Kd_eng = 0, Kd_hor = 0, Kd_ver = 0, Kd_ver_st1 = 0.015, Kd_ver_st2 = 5e-05,
        Ki_eng = 0.003, Kii_ver = 0.2, Kp_eng = 265, Kp_hor_err = 260, Kp_hor_err_croll = 0.06,
        Kp_ver = 8.5, Kp_ver_st1 = 0.009, Kp_ver_st2 = 0.00018,
        alg_calc_time = 1.5, alg_div_k = 2, alg_max_sin_climb = 0.8,
        alg_points_num = 7, alg_section_temp_points = 3, alg_tmp_point_vel_k = 1.5,
        alg_vel_k = 6, auto_terrain_following = 1, auto_terrain_following_height = 75,
        delay = 1, eng_max_thrust = 3500, eng_min_thrust = -120, estimated_N_max = 6,
        finsLimit = 0.78, max_roll = 0.8, max_start_y_vel = 35, no_alg_vel_k = 10, stab_vel = 230,
    },
    final_autopilot = {
        J_Angle_K = 0.20, J_Angle_W = 0.7, J_Diff_K = 0.4, J_FinAngle_K = 0.34,
        J_Int_K = 0.001, J_Power_K = 2.0, J_Trigger_Vert = 1, K = 72, Kg = 4, Ki = 0,
        delay = 0, finsLimit = 0.78, hKd = 0.005, hKp_err = 120, hKp_err_croll = 0.04,
        max_roll = 0.8, useJumpByDefault = 1,
    },
    fm = deep_copy(polar.FM_CRUISE_STEALTH),
    seeker = { can_update_target_pos = 1, coalition = 2, coalition_rnd_coeff = 5 },
    warhead = {
        caliber = 480, concrete_factors = { 4, 1, 8 }, concrete_obj_factor = 4,
        cumulative_factor = 0, cumulative_thickness = 0, default_fuze_delay = 0,
        expl_mass = 450, fantom = 1, is_htp = true, mass = 450,
        obj_factors = { 2, 1 }, other_factors = { 1.5, 1.5, 1.5 }, piercing_mass = 90,
    },
    warhead_air = {
        caliber = 480, concrete_factors = { 1, 1, 1 }, concrete_obj_factor = 0,
        cumulative_factor = 0, cumulative_thickness = 0, default_fuze_delay = 0,
        expl_mass = 450, fantom = 1, is_htp = true, mass = 450,
        obj_factors = { 1, 1 }, other_factors = { 1, 1, 1 }, piercing_mass = 40,
    },
}

local FOLDING_SHAPES = {
    ng_stealth_cruise = true,
    ng_jassm_taurus   = true,
    ng_glide_sdb      = true,
    ng_loitering_x    = true,
    ng_umpb_d30       = true,
    ng_heavy_umpk     = true,
    ng_kh35u          = true,
    ng_nsm_jsm        = true,
    ng_kh22_32        = true,
    ng_kh58ushke      = true,
    ng_spear_ew       = true,
    ng_gbu57_mop      = true,
    ng_spice_glide    = true,
    ng_kalibr_3m54    = true,
    ng_javelin_top    = true,
    ng_tomahawk_v     = true,
}

local PROP_SHAPES = {
    ng_loitering_x = true,
    ng_shahed_136  = true,
    ng_harop       = true,
}

local registered_attrs = {}

local function register_as(spec)
    local is_folding = (spec.role ~= "aam") and FOLDING_SHAPES[spec.shape]
    local is_cruise_mode = (spec.role == "cruise") or (spec.role == "glide") or (spec.role == "loiter")
    local use_cruise_scheme = is_cruise_mode or (is_folding and (spec.role ~= "sead") and (spec.role ~= "supersonic_ship"))
    local w = deep_copy(use_cruise_scheme and BASE_CRUISE_FOLDING or BASE_AS_TEMPLATE)

    w.name = spec.id
    w.user_name = _(spec.display_name)
    w.displayName = _(spec.display_name)
    w.display_name = _(spec.display_name)
    w.display_name_short = spec.short_name
    w.model = spec.shape
    w.caliber = spec.caliber
    w.Diam = math.floor(spec.caliber * 1000)
    w.mass = spec.mass
    w.M = spec.mass
    w.Mach_max = spec.mach_max
    w.Range_max = spec.range_max
    w.D_max = spec.range_max
    w.Life_Time = spec.life_time or 900
    w.warhead.caliber = math.floor(spec.caliber * 1000)
    w.warhead.expl_mass = spec.warhead_mass
    w.warhead.mass = spec.warhead_mass
    w.warhead_air.caliber = math.floor(spec.caliber * 1000)
    w.warhead_air.expl_mass = spec.warhead_mass
    w.warhead_air.mass = spec.warhead_mass

    local default_polar = "FM_HYPERSONIC"
    if use_cruise_scheme then
        default_polar = (spec.role == "loiter") and "FM_LOITER_DRONE" or ((spec.role == "glide") and "FM_GLIDE_BOMB" or "FM_CRUISE_STEALTH")
    elseif spec.role == "aam" then
        default_polar = (spec.head_type == 1) and "FM_AAM_WVR" or "FM_AAM_ULTRA"
    end
    polar.apply_polar(w, spec.polar or default_polar, spec.caliber, spec.mass, spec.length)

    local back = -(spec.length * 0.5)
    w.X_back = back
    w.boost.nozzle_position = { { back + 0.06, 0, 0 } }
    w.march.nozzle_position = { { back + 0.06, 0, 0 } }

    if use_cruise_scheme then
        w.march.fuel_mass = spec.fuel_mass
        w.march.impulse = spec.impulse
        w.march.work_time = spec.burn_time
        w.t_marsh = spec.burn_time
        w.fm.wingsDeplDelay = (spec.role == "loiter") and 0.4 or 1.0
        w.fm.wingsDeplProcTime = (spec.role == "loiter") and 1.2 or 2.5
        if PROP_SHAPES[spec.shape] then
            if FOLDING_SHAPES[spec.shape] then
                w.encyclopediaAnimation = { args = { [25] = 1, [407] = 0.35 } }
            else
                w.encyclopediaAnimation = { args = { [407] = 0.35 } }
            end
            w.cruise_autopilot.stab_vel = (spec.shape == "ng_shahed_136") and 52 or 85
            w.v_min = 40
            w.v_mid = w.cruise_autopilot.stab_vel
        elseif spec.role == "loiter" then
            -- Jet drones (Palianytsia, Shahed-238, Peklo)
            w.cruise_autopilot.stab_vel = 195
            w.v_min = 95
            w.v_mid = 195
        end
        if spec.role == "glide" then
            w.march.max_thrust = 400
            w.cruise_autopilot.stab_vel = 210
        end
        if spec.penetrator then
            w.warhead.concrete_factors = { 8.0, 2.0, 15.0 }
            w.warhead.concrete_obj_factor = 8.0
            w.warhead.piercing_mass = spec.warhead_mass * 0.55
        end
    else
        local b_frac = spec.boost_frac or 0.30
        w.boost.fuel_mass = spec.fuel_mass * b_frac
        w.boost.impulse = 250
        w.boost.work_time = math.max(1.8, spec.burn_time * 0.25)
        w.controller.march_start = w.boost.work_time
        w.march.fuel_mass = spec.fuel_mass * (1.0 - b_frac)
        w.march.impulse = spec.impulse
        w.march.work_time = math.max(2.5, spec.burn_time * 0.75)
        w.t_acc = w.boost.work_time
        w.t_marsh = w.march.work_time
        w.autopilot.op_time = w.Life_Time
        w.seeker.op_time = w.Life_Time
        if FOLDING_SHAPES[spec.shape] then
            w.encyclopediaAnimation = { args = { [25] = 1 } }
        end
        if spec.loft then
            w.loft = 1
            w.autopilot.loft_active_by_default = 1
        end
        if spec.troll then
            w.boost.smoke_transparency = 1.0
            w.boost.tail_width = 1.25
            w.boost.smoke_color = { 0.94, 0.78, 0.56 }
            w.march.smoke_transparency = 0.95
            w.march.tail_width = 1.1
            w.seeker.aim_sigma = 16.0
        end
        if spec.role == "aam" then
            w.category = CAT_AIR_TO_AIR
            w.wsTypeOfWeapon = { wsType_Weapon, wsType_Missile, wsType_AA_Missile, WSTYPE_PLACEHOLDER }
            w.scheme = "schemes/missiles/aa_missile_amraam2.sch"
            w.Head_Type = spec.head_type or 2
            w.proximity_fuze.radius = 15
        end
    end

    w.shape_table_data = {
        { name = spec.id, file = spec.shape, life = 1, fire = { 0, 1 }, username = spec.display_name, index = WSTYPE_PLACEHOLDER },
    }

    local registered = declare_weapon(w)
    registered_attrs[spec.id] = registered.wsTypeOfWeapon
    declare_loadout({
        category = (spec.role == "aam") and CAT_AIR_TO_AIR or CAT_MISSILES,
        CLSID = spec.clsid,
        Picture = spec.picture or "agm88.png",
        displayName = _(spec.display_name),
        Weight = spec.mass,
        Cx_pil = 0.0022,
        attribute = registered.wsTypeOfWeapon,
        Elements = { { ShapeName = spec.shape } },
    })
    return spec.clsid
end

local ag_specs = {
    -- 1. Ballistic & Hypersonic Aeroballistic (13)
    { id = "NG_KH_47M2_KINZHAL", clsid = "{NEXTGEN_KH47M2_KINZHAL}", role = "sead",   polar = "FM_HYPERSONIC", shape = "ng_kinzhal",         caliber = 1.050, length = 7.40, display_name = "Kh-47M2 Kinzhal Mach 10 (NextGen)",   short_name = "Kinzhal",  mass = 4300.0, mach_max = 9.5, range_max = 1500000, fuel_mass = 2400.0, impulse = 290, burn_time = 65.0,  warhead_mass = 480.0, picture = "agm88.png", loft = true, life_time = 1200 },
    { id = "NG_AGM_183A_ARRW",   clsid = "{NEXTGEN_AGM183A_ARRW}",   role = "sead",   polar = "FM_HYPERSONIC", shape = "ng_arrw",            caliber = 0.720, length = 6.50, display_name = "AGM-183A ARRW Hypersonic (NG)",       short_name = "ARRW",     mass = 3100.0, mach_max = 8.5, range_max = 1600000, fuel_mass = 1800.0, impulse = 295, burn_time = 55.0,  warhead_mass = 350.0, picture = "agm88.png", loft = true, life_time = 1200 },
    { id = "NG_DF_17",           clsid = "{NEXTGEN_DF_17}",          role = "sead",   polar = "FM_HYPERSONIC", shape = "ng_df17_waverider",  caliber = 0.850, length = 7.80, display_name = "DF-17 Air-Drop Waverider HGV (NG)",   short_name = "DF-17",    mass = 3400.0, mach_max = 9.2, range_max = 1800000, fuel_mass = 1950.0, impulse = 295, burn_time = 60.0,  warhead_mass = 380.0, picture = "agm88.png", loft = true, life_time = 1400 },
    { id = "NG_DF_21D",          clsid = "{NEXTGEN_DF_21D}",         role = "sead",   polar = "FM_HYPERSONIC", shape = "ng_kinzhal",         caliber = 1.000, length = 8.20, display_name = "DF-21D ASBM Carrier-Killer (NextGen)",short_name = "DF-21D",   mass = 4400.0, mach_max = 9.5, range_max = 1500000, fuel_mass = 2400.0, impulse = 290, burn_time = 65.0,  warhead_mass = 600.0, picture = "agm88.png", loft = true, life_time = 1400 },
    { id = "NG_YJ_21",           clsid = "{NEXTGEN_YJ_21}",          role = "sead",   polar = "FM_HYPERSONIC", shape = "ng_kinzhal",         caliber = 0.850, length = 7.00, display_name = "YJ-21 Eagle Strike Ballistic (NG)",   short_name = "YJ-21",    mass = 3600.0, mach_max = 8.0, range_max = 1000000, fuel_mass = 1900.0, impulse = 285, burn_time = 55.0,  warhead_mass = 400.0, picture = "agm88.png", loft = true, life_time = 1000 },
    { id = "NG_9M723_ISKANDER",  clsid = "{NEXTGEN_9M723_ISKANDER}", role = "sead",   polar = "FM_HYPERSONIC", shape = "ng_iskander_atacms", caliber = 0.720, length = 6.20, display_name = "9M723 Iskander-M Air-Launch (NG)",    short_name = "Iskander", mass = 3200.0, mach_max = 6.2, range_max = 500000,  fuel_mass = 1650.0, impulse = 278, burn_time = 35.0,  warhead_mass = 480.0, picture = "agm88.png", loft = true, life_time = 900 },
    { id = "NG_ATACMS_IVA",      clsid = "{NEXTGEN_ATACMS_IVA}",     role = "sead",   polar = "FM_HYPERSONIC", shape = "ng_prsm_atacms",     caliber = 0.610, length = 3.98, display_name = "MGM-168 ATACMS Block IVA Air (NG)",   short_name = "ATACMS4A", mass = 1670.0, mach_max = 4.5, range_max = 300000,  fuel_mass = 820.0,  impulse = 268, burn_time = 24.0,  warhead_mass = 227.0, picture = "agm88.png", loft = true, life_time = 700 },
    { id = "NG_PRSM_INC1",       clsid = "{NEXTGEN_PRSM_INC1}",      role = "sead",   polar = "FM_HYPERSONIC", shape = "ng_prsm_atacms",     caliber = 0.430, length = 4.00, display_name = "PrSM Increment 1 Hypersonic (NG)",    short_name = "PrSM-1",   mass = 980.0,  mach_max = 5.8, range_max = 500000,  fuel_mass = 520.0,  impulse = 275, burn_time = 26.0,  warhead_mass = 120.0, picture = "agm88.png", loft = true, life_time = 850 },
    { id = "NG_IAI_RAMPAGE",     clsid = "{NEXTGEN_IAI_RAMPAGE}",    role = "sead",   polar = "FM_HYPERSONIC", shape = "ng_rampage_lora",    caliber = 0.306, length = 4.70, display_name = "IAI Rampage Aero-Ballistic (NG)",     short_name = "Rampage",  mass = 570.0,  mach_max = 4.2, range_max = 250000,  fuel_mass = 240.0,  impulse = 265, burn_time = 24.0,  warhead_mass = 150.0, picture = "agm88.png", loft = true },
    { id = "NG_AIR_LORA",        clsid = "{NEXTGEN_AIR_LORA}",       role = "sead",   polar = "FM_HYPERSONIC", shape = "ng_rampage_lora",    caliber = 0.624, length = 5.20, display_name = "IAI Air LORA Long-Range (NextGen)",   short_name = "AirLORA",  mass = 1600.0, mach_max = 5.0, range_max = 430000,  fuel_mass = 760.0,  impulse = 275, burn_time = 40.0,  warhead_mass = 570.0, picture = "agm88.png", loft = true },
    { id = "NG_KH_15S",          clsid = "{NEXTGEN_KH_15S}",         role = "sead",   polar = "FM_HYPERSONIC", shape = "ng_rampage_lora",    caliber = 0.455, length = 4.78, display_name = "Kh-15S Raduga Mach 5 ASM (NextGen)",  short_name = "Kh-15S",   mass = 1200.0, mach_max = 5.0, range_max = 300000,  fuel_mass = 580.0,  impulse = 270, burn_time = 32.0,  warhead_mass = 150.0, picture = "agm88.png", loft = true },
    { id = "NG_FATH_360",        clsid = "{NEXTGEN_FATH_360}",       role = "sead",   polar = "FM_HYPERSONIC", shape = "ng_rampage_lora",    caliber = 0.368, length = 5.17, display_name = "Fath-360 Guided Tact-Ballistic (NG)", short_name = "Fath-360", mass = 787.0,  mach_max = 4.0, range_max = 120000,  fuel_mass = 310.0,  impulse = 258, burn_time = 18.0,  warhead_mass = 150.0, picture = "agm88.png", loft = true },
    { id = "NG_KHEIBAR_SHEKAN",  clsid = "{NEXTGEN_KHEIBAR_SHEKAN}", role = "sead",   polar = "FM_HYPERSONIC", shape = "ng_df17_waverider",  caliber = 0.780, length = 6.80, display_name = "Kheibar Shekan MaRV Ballistic (NG)",  short_name = "Kheibar",  mass = 2800.0, mach_max = 6.5, range_max = 1450000, fuel_mass = 1450.0, impulse = 280, burn_time = 45.0,  warhead_mass = 500.0, picture = "agm88.png", loft = true, life_time = 1300 },

    -- 2. KEKA Aerospace Troll Rockets (Air-Launched) (3)
    { id = "NG_KEKA_TROPO4",     clsid = "{NEXTGEN_KEKA_TROPO4}",    role = "sead",   polar = "FM_KEKA_TROLL", shape = "ng_keka_tropo5",     caliber = 0.240, length = 3.20, display_name = "KEKA Troposphere-4 DIY (Troll!)",     short_name = "KEKA-T4",  mass = 135.0,  mach_max = 2.7, range_max = 25000,   fuel_mass = 52.0,   impulse = 215, burn_time = 7.0,   warhead_mass = 30.0,  picture = "hydra.png", loft = true, troll = true },
    { id = "NG_KEKA_TROPO5_AIR", clsid = "{NEXTGEN_KEKA_TROPO5_AIR}",role = "sead",   polar = "FM_KEKA_TROLL", shape = "ng_keka_tropo5",     caliber = 0.280, length = 3.60, display_name = "KEKA Troposphere-5 Viral Cat (Troll!)",short_name= "KEKA-T5",  mass = 195.0,  mach_max = 3.0, range_max = 45000,   fuel_mass = 80.0,   impulse = 222, burn_time = 9.0,   warhead_mass = 55.0,  picture = "hydra.png", loft = true, troll = true },
    { id = "NG_KEKA_TROPO6_AIR", clsid = "{NEXTGEN_KEKA_TROPO6_AIR}",role = "sead",   polar = "FM_KEKA_TROLL", shape = "ng_keka_tropo6",     caliber = 0.340, length = 5.20, display_name = "KEKA Troposphere-6 Strap-On (Troll!)",short_name = "KEKA-T6",  mass = 440.0,  mach_max = 4.4, range_max = 120000,  fuel_mass = 210.0,  impulse = 235, burn_time = 16.0,  warhead_mass = 140.0, picture = "zuni.png",  loft = true, troll = true },

    -- 3. Anti-Ship & Naval Missiles (18)
    { id = "NG_EXOCET_B2",       clsid = "{NEXTGEN_EXOCET_B2}",      role = "sead",            polar = "FM_HYPERSONIC",     shape = "ng_exocet_am39", caliber = 0.350, length = 4.69, display_name = "Exocet AM39 Block 2 Mod 2 (NG)",   short_name = "AM39-B2",  mass = 655.0,  mach_max = 0.93, range_max = 70000,   fuel_mass = 140.0, impulse = 250,  burn_time = 110.0, warhead_mass = 165.0, picture = "agm84d.png" },
    { id = "NG_EXOCET_B3",       clsid = "{NEXTGEN_EXOCET_B3}",      role = "sead",            polar = "FM_HYPERSONIC",     shape = "ng_exocet_am39", caliber = 0.350, length = 4.70, display_name = "Exocet AM39 Block 3 (NextGen)",     short_name = "AM39-B3",  mass = 670.0,  mach_max = 0.95, range_max = 180000,  fuel_mass = 180.0, impulse = 310,  burn_time = 200.0, warhead_mass = 165.0, picture = "agm84d.png" },
    { id = "NG_AGM_84N_HARPOON", clsid = "{NEXTGEN_AGM84N_HARPOON}", role = "sead",            polar = "FM_CRUISE_STEALTH", shape = "ng_exocet_am39", caliber = 0.343, length = 3.85, display_name = "AGM-84N Harpoon Block II+ (NG)",    short_name = "Harpoon+", mass = 528.0,  mach_max = 0.85, range_max = 280000,  fuel_mass = 145.0, impulse = 320,  burn_time = 240.0, warhead_mass = 221.0, picture = "agm84d.png" },
    { id = "NG_AGM_84K_SLAMER",  clsid = "{NEXTGEN_AGM84K_SLAMER}",  role = "cruise",          polar = "FM_CRUISE_STEALTH", shape = "ng_exocet_am39", caliber = 0.343, length = 4.37, display_name = "AGM-84K SLAM-ERATA Cruise (NG)",   short_name = "SLAM-ER",  mass = 675.0,  mach_max = 0.95, range_max = 270000,  fuel_mass = 185.0, impulse = 2900, burn_time = 700.0, warhead_mass = 221.0, picture = "agm84d.png", life_time = 1300 },
    { id = "NG_KH_35U",          clsid = "{NEXTGEN_KH_35U}",         role = "cruise",          polar = "FM_CRUISE_STEALTH", shape = "ng_kh35u",       caliber = 0.420, length = 3.85, display_name = "Kh-35U Uran-U ASM (NextGen)",       short_name = "Kh-35U",   mass = 550.0,  mach_max = 0.92, range_max = 260000,  fuel_mass = 140.0, impulse = 2800, burn_time = 650.0, warhead_mass = 145.0, picture = "agm84d.png", life_time = 1200 },
    { id = "NG_KH_35UE",         clsid = "{NEXTGEN_KH_35UE}",        role = "cruise",          polar = "FM_CRUISE_STEALTH", shape = "ng_kh35u",       caliber = 0.420, length = 3.85, display_name = "Kh-35UE Export Sea-Skimmer (NG)",  short_name = "Kh-35UE",  mass = 550.0,  mach_max = 0.92, range_max = 260000,  fuel_mass = 140.0, impulse = 2800, burn_time = 650.0, warhead_mass = 145.0, picture = "agm84d.png", life_time = 1200 },
    { id = "NG_NSM",             clsid = "{NEXTGEN_NSM}",            role = "cruise",          polar = "FM_CRUISE_STEALTH", shape = "ng_nsm_jsm",     caliber = 0.340, length = 3.96, display_name = "Naval Strike Missile / JSM (NG)",   short_name = "NSM/JSM",  mass = 410.0,  mach_max = 0.95, range_max = 250000,  fuel_mass = 110.0, impulse = 2800, burn_time = 600.0, warhead_mass = 125.0, picture = "agm84d.png", life_time = 1200 },
    { id = "NG_ATMACA",          clsid = "{NEXTGEN_ATMACA}",         role = "cruise",          polar = "FM_CRUISE_STEALTH", shape = "ng_kh35u",       caliber = 0.350, length = 5.20, display_name = "Roketsan Atmaca Sea-Skimmer (NG)",  short_name = "Atmaca",   mass = 750.0,  mach_max = 0.90, range_max = 250000,  fuel_mass = 195.0, impulse = 2850, burn_time = 650.0, warhead_mass = 220.0, picture = "agm84d.png", life_time = 1200 },
    { id = "NG_GABRIEL_V",       clsid = "{NEXTGEN_GABRIEL_V}",      role = "cruise",          polar = "FM_CRUISE_STEALTH", shape = "ng_nsm_jsm",     caliber = 0.380, length = 5.50, display_name = "IAI Gabriel V / Blue Spear (NG)",   short_name = "Gab-V",    mass = 1250.0, mach_max = 0.92, range_max = 290000,  fuel_mass = 310.0, impulse = 2950, burn_time = 750.0, warhead_mass = 240.0, picture = "agm84d.png", life_time = 1350 },
    { id = "NG_ICE_BREAKER",     clsid = "{NEXTGEN_ICE_BREAKER}",    role = "cruise",          polar = "FM_CRUISE_STEALTH", shape = "ng_nsm_jsm",     caliber = 0.350, length = 4.00, display_name = "Rafael Ice Breaker 300km (NG)",     short_name = "IceBrk",   mass = 400.0,  mach_max = 0.95, range_max = 300000,  fuel_mass = 120.0, impulse = 2900, burn_time = 700.0, warhead_mass = 113.0, picture = "agm84d.png", life_time = 1300 },
    { id = "NG_CAKIR",           clsid = "{NEXTGEN_CAKIR}",          role = "cruise",          polar = "FM_CRUISE_STEALTH", shape = "ng_nsm_jsm",     caliber = 0.275, length = 3.30, display_name = "Roketsan Cakir Stealth Cruise (NG)",short_name = "Cakir",    mass = 275.0,  mach_max = 0.85, range_max = 150000,  fuel_mass = 75.0,  impulse = 2750, burn_time = 450.0, warhead_mass = 70.0,  picture = "agm84d.png", life_time = 900 },
    { id = "NG_KALIBR_3M54",     clsid = "{NEXTGEN_KALIBR_3M54}",    role = "cruise",          polar = "FM_CRUISE_STEALTH", shape = "ng_kalibr_3m54", caliber = 0.533, length = 6.20, display_name = "3M54 / 3M14 Kalibr Air-Launch (NG)",short_name = "Kalibr",   mass = 1570.0, mach_max = 2.9,  range_max = 660000,  fuel_mass = 480.0, impulse = 3100, burn_time = 1100.0,warhead_mass = 400.0, picture = "agm84d.png", life_time = 2000 },
    { id = "NG_HSIUNG_FENG_3",   clsid = "{NEXTGEN_HSIUNG_FENG_3}",  role = "supersonic_ship", polar = "FM_AAM_ULTRA",      shape = "ng_kh31_ramjet", caliber = 0.460, length = 6.10, display_name = "Hsiung Feng III Ramjet ASM (NG)",   short_name = "HF-3",     mass = 1400.0, mach_max = 3.0,  range_max = 300000,  fuel_mass = 500.0, impulse = 310,  burn_time = 110.0, warhead_mass = 225.0, picture = "agm84d.png" },
    { id = "NG_KH_22N",          clsid = "{NEXTGEN_KH_22N}",         role = "supersonic_ship", polar = "FM_HYPERSONIC",     shape = "ng_kh22_32",     caliber = 0.920, length = 11.65,display_name = "Kh-22N Burya Mach 4.6 ASM (NG)",    short_name = "Kh-22N",   mass = 5820.0, mach_max = 4.6,  range_max = 600000,  fuel_mass = 3000.0,impulse = 310,  burn_time = 120.0, warhead_mass = 960.0, picture = "agm84d.png", loft = true, life_time = 1200 },
    { id = "NG_KH_32",           clsid = "{NEXTGEN_KH_32}",          role = "supersonic_ship", polar = "FM_HYPERSONIC",     shape = "ng_kh22_32",     caliber = 0.920, length = 11.65,display_name = "Kh-32 Deep-Strike Cruise (NextGen)",short_name = "Kh-32",    mass = 5800.0, mach_max = 4.6,  range_max = 1000000, fuel_mass = 3200.0,impulse = 320,  burn_time = 160.0, warhead_mass = 500.0, picture = "agm84d.png", loft = true, life_time = 1400 },
    { id = "NG_ZIRCON",          clsid = "{NEXTGEN_ZIRCON}",         role = "supersonic_ship", polar = "FM_HYPERSONIC",     shape = "ng_zircon",      caliber = 0.600, length = 8.50, display_name = "3M22 Tsirkon Scramjet Mach 9 (NG)",short_name = "3M22-Zrc", mass = 2800.0, mach_max = 8.8,  range_max = 1000000, fuel_mass = 1350.0,impulse = 410,  burn_time = 180.0, warhead_mass = 350.0, picture = "agm88.png",  loft = true, life_time = 1200 },
    { id = "NG_HALO_HYPER",      clsid = "{NEXTGEN_HALO_HYPER}",     role = "supersonic_ship", polar = "FM_HYPERSONIC",     shape = "ng_zircon",      caliber = 0.440, length = 6.20, display_name = "HALO Hypersonic Mach 6+ ASM (NG)", short_name = "HALO-M6",  mass = 1450.0, mach_max = 6.2,  range_max = 450000,  fuel_mass = 580.0, impulse = 320,  burn_time = 65.0,  warhead_mass = 320.0, picture = "agm88.png" },
    { id = "NG_YJ_83K",          clsid = "{NEXTGEN_YJ_83K}",         role = "cruise",          polar = "FM_CRUISE_STEALTH", shape = "ng_kh35u",       caliber = 0.360, length = 5.15, display_name = "YJ-83K Air-Launched ASM (NextGen)", short_name = "YJ-83K",   mass = 715.0,  mach_max = 0.90, range_max = 230000,  fuel_mass = 190.0, impulse = 2800, burn_time = 600.0, warhead_mass = 190.0, picture = "agm84d.png", life_time = 1100 },
    { id = "NG_YJ_18A",          clsid = "{NEXTGEN_YJ_18A}",         role = "cruise",          polar = "FM_CRUISE_STEALTH", shape = "ng_kh35u",       caliber = 0.533, length = 6.20, display_name = "YJ-18A Dual-Stage ASM (NextGen)",   short_name = "YJ-18A",   mass = 1600.0, mach_max = 2.8,  range_max = 540000,  fuel_mass = 520.0, impulse = 2900, burn_time = 900.0, warhead_mass = 300.0, picture = "agm84d.png", life_time = 1500 },

    -- 4. SEAD / Anti-Radiation Missiles (15)
    { id = "NG_AARGM_ER",        clsid = "{NEXTGEN_AARGM_ER}",       role = "sead",   polar = "FM_AAM_ULTRA",      shape = "ng_aargm_er",    caliber = 0.292, length = 4.17, display_name = "AGM-88G AARGM-ER (NextGen)",        short_name = "AARGM-ER", mass = 467.0, mach_max = 4.0, range_max = 280000, fuel_mass = 175.0, impulse = 255, burn_time = 22.0,  warhead_mass = 70.0,  picture = "agm88.png", loft = true },
    { id = "NG_AGM_88E_AARGM",   clsid = "{NEXTGEN_AGM88E_AARGM}",   role = "sead",   polar = "FM_AAM_BVR",        shape = "ng_aargm_er",    caliber = 0.254, length = 4.17, display_name = "AGM-88E AARGM Dual-Seeker (NG)",    short_name = "AGM-88E",  mass = 361.0, mach_max = 3.2, range_max = 150000, fuel_mass = 130.0, impulse = 250, burn_time = 16.0,  warhead_mass = 68.0,  picture = "agm88.png", loft = true },
    { id = "NG_AGM_122_SIDEARM", clsid = "{NEXTGEN_AGM122_SIDEARM}", role = "sead",   polar = "FM_AAM_WVR",        shape = "ng_aim9x_b3",    caliber = 0.127, length = 2.87, display_name = "AGM-122 Sidearm Helo-SEAD (NG)",    short_name = "Sidearm",  mass = 88.0,  mach_max = 2.5, range_max = 22000,  fuel_mass = 26.0,  impulse = 235, burn_time = 4.0,   warhead_mass = 10.0,  picture = "agm88.png" },
    { id = "NG_KH_58USHKE",      clsid = "{NEXTGEN_KH_58USHKE}",     role = "sead",   polar = "FM_AAM_ULTRA",      shape = "ng_kh58ushke",   caliber = 0.380, length = 4.19, display_name = "Kh-58UShKE Folding-Fin SEAD (NG)",  short_name = "Kh58UShKE",mass = 650.0, mach_max = 3.6, range_max = 245000, fuel_mass = 245.0, impulse = 265, burn_time = 26.0,  warhead_mass = 149.0, picture = "agm88.png", loft = true },
    { id = "NG_ALARM",           clsid = "{NEXTGEN_ALARM}",          role = "sead",   polar = "FM_AAM_BVR",        shape = "ng_alarm_sead",  caliber = 0.230, length = 4.24, display_name = "MBDA ALARM Loiter-SEAD (NextGen)",  short_name = "ALARM",    mass = 268.0, mach_max = 2.4, range_max = 93000,  fuel_mass = 82.0,  impulse = 240, burn_time = 16.0,  warhead_mass = 55.0,  picture = "agm88.png", loft = true },
    { id = "NG_ALARM_NG",        clsid = "{NEXTGEN_ALARM_NG}",       role = "sead",   polar = "FM_AAM_BVR",        shape = "ng_alarm_sead",  caliber = 0.230, length = 4.24, display_name = "MBDA ALARM-NG Active SEAD (NG)",    short_name = "ALARM-NG", mass = 275.0, mach_max = 2.8, range_max = 135000, fuel_mass = 95.0,  impulse = 250, burn_time = 20.0,  warhead_mass = 55.0,  picture = "agm88.png", loft = true },
    { id = "NG_ARMAT",           clsid = "{NEXTGEN_ARMAT}",          role = "sead",   polar = "FM_AAM_ULTRA",      shape = "ng_aargm_er",    caliber = 0.400, length = 4.15, display_name = "Matra ARMAT Anti-Radar (NextGen)",  short_name = "ARMAT",    mass = 550.0, mach_max = 2.8, range_max = 120000, fuel_mass = 180.0, impulse = 250, burn_time = 18.0,  warhead_mass = 150.0, picture = "agm88.png", loft = true },
    { id = "NG_RUDRAM_1",        clsid = "{NEXTGEN_RUDRAM_1}",       role = "sead",   polar = "FM_AAM_ULTRA",      shape = "ng_rudram_arm",  caliber = 0.360, length = 5.50, display_name = "DRDO Rudram-1 NGARM SEAD (NextGen)",short_name = "Rudram-1", mass = 600.0, mach_max = 2.5, range_max = 150000, fuel_mass = 210.0, impulse = 255, burn_time = 22.0,  warhead_mass = 120.0, picture = "agm88.png", loft = true },
    { id = "NG_RUDRAM_2",        clsid = "{NEXTGEN_RUDRAM_2}",       role = "sead",   polar = "FM_HYPERSONIC",     shape = "ng_rudram_arm",  caliber = 0.400, length = 5.50, display_name = "DRDO Rudram-2 Mach 5.5 ARM (NG)",   short_name = "Rudram-2", mass = 750.0, mach_max = 5.5, range_max = 350000, fuel_mass = 360.0, impulse = 275, burn_time = 35.0,  warhead_mass = 200.0, picture = "agm88.png", loft = true },
    { id = "NG_CM_102",          clsid = "{NEXTGEN_CM_102}",         role = "sead",   polar = "FM_AAM_ULTRA",      shape = "ng_rudram_arm",  caliber = 0.350, length = 4.80, display_name = "CM-102 Anti-Radiation (NextGen)",   short_name = "CM-102",   mass = 520.0, mach_max = 3.5, range_max = 100000, fuel_mass = 180.0, impulse = 255, burn_time = 18.0,  warhead_mass = 80.0,  picture = "agm88.png", loft = true },
    { id = "NG_YJ_91",           clsid = "{NEXTGEN_YJ_91}",          role = "sead",   polar = "FM_AAM_ULTRA",      shape = "ng_kh31_ramjet", caliber = 0.360, length = 4.70, display_name = "YJ-91 Anti-Radar Ramjet (NextGen)", short_name = "YJ-91",    mass = 600.0, mach_max = 3.5, range_max = 150000, fuel_mass = 200.0, impulse = 268, burn_time = 28.0,  warhead_mass = 90.0,  picture = "agm88.png" },
    { id = "NG_SPEAR_EW",        clsid = "{NEXTGEN_SPEAR_EW}",       role = "cruise", polar = "FM_CRUISE_STEALTH", shape = "ng_spear_ew",    caliber = 0.180, length = 1.80, display_name = "MBDA SPEAR-EW Stand-In Jammer (NG)",short_name = "SPEAR-EW", mass = 92.0,  mach_max = 0.95,range_max = 140000, fuel_mass = 26.0,  impulse = 2500,burn_time = 420.0, warhead_mass = 15.0,  picture = "gbu38.png", life_time = 900 },
    { id = "NG_LD_10",           clsid = "{NEXTGEN_LD_10}",          role = "sead",   polar = "FM_AAM_BVR",        shape = "ng_pl12a",       caliber = 0.203, length = 3.93, display_name = "LD-10 Anti-Radiation (NextGen)",    short_name = "LD-10",    mass = 200.0, mach_max = 4.0, range_max = 80000,  fuel_mass = 70.0,  impulse = 250, burn_time = 10.0,  warhead_mass = 25.0,  picture = "agm88.png" },
    { id = "NG_MAR_1",           clsid = "{NEXTGEN_MAR_1}",          role = "sead",   polar = "FM_AAM_BVR",        shape = "ng_alarm_sead",  caliber = 0.230, length = 4.00, display_name = "Mectron MAR-1 SEAD (NextGen)",      short_name = "MAR-1",    mass = 274.0, mach_max = 2.2, range_max = 100000, fuel_mass = 88.0,  impulse = 240, burn_time = 15.0,  warhead_mass = 90.0,  picture = "agm88.png" },
    { id = "NG_KH_31PM",         clsid = "{NEXTGEN_KH_31PM}",        role = "sead",   polar = "FM_AAM_ULTRA",      shape = "ng_kh31_ramjet", caliber = 0.360, length = 4.70, display_name = "Kh-31PM Anti-Radar (NextGen)",      short_name = "Kh-31PM",  mass = 610.0, mach_max = 3.5, range_max = 250000, fuel_mass = 220.0, impulse = 270, burn_time = 35.0,  warhead_mass = 90.0,  picture = "agm88.png" },

    -- 5. Stealth Cruise, Deep Penetrators & Glide Bombs (14)
    { id = "NG_GBU_57A_MOP",     clsid = "{NEXTGEN_GBU57A_MOP}",     role = "glide",  polar = "FM_GLIDE_BOMB",     shape = "ng_gbu57_mop",     caliber = 0.800, length = 6.20, display_name = "GBU-57A/B MOP 30,000lb Bunker (NG)",short_name = "GBU-57",   mass = 13600.0,mach_max = 1.2, range_max = 45000,   fuel_mass = 2.0,   impulse = 1800, burn_time = 180.0, warhead_mass = 2400.0,picture = "gbu31.png", penetrator = true },
    { id = "NG_SCALP_EG",        clsid = "{NEXTGEN_SCALP_EG}",       role = "cruise", polar = "FM_CRUISE_STEALTH", shape = "ng_stealth_cruise",caliber = 0.480, length = 5.10, display_name = "SCALP-EG / Storm Shadow (NextGen)",short_name = "SCALP-EG", mass = 1300.0, mach_max = 0.95,range_max = 560000,  fuel_mass = 280.0, impulse = 3000, burn_time = 900.0, warhead_mass = 450.0, picture = "agm154.png",penetrator = true, life_time = 1800 },
    { id = "NG_TAURUS",          clsid = "{NEXTGEN_TAURUS}",         role = "cruise", polar = "FM_CRUISE_STEALTH", shape = "ng_jassm_taurus",  caliber = 0.510, length = 5.10, display_name = "TAURUS KEPD 350 (NextGen)",         short_name = "TAURUS",   mass = 1400.0, mach_max = 0.95,range_max = 500000,  fuel_mass = 300.0, impulse = 3000, burn_time = 900.0, warhead_mass = 481.0, picture = "agm154.png",penetrator = true, life_time = 1800 },
    { id = "NG_JASSM_ER",        clsid = "{NEXTGEN_JASSM_ER}",       role = "cruise", polar = "FM_CRUISE_STEALTH", shape = "ng_jassm_taurus",  caliber = 0.450, length = 4.27, display_name = "AGM-158B JASSM-ER (NextGen)",       short_name = "JASSM-ER", mass = 1020.0, mach_max = 0.92,range_max = 925000,  fuel_mass = 260.0, impulse = 3200, burn_time = 1200.0,warhead_mass = 450.0, picture = "agm154.png",life_time = 2400 },
    { id = "NG_JASSM_XR",        clsid = "{NEXTGEN_JASSM_XR}",       role = "cruise", polar = "FM_CRUISE_STEALTH", shape = "ng_jassm_taurus",  caliber = 0.520, length = 5.40, display_name = "AGM-158D JASSM-XR Ultra (NextGen)", short_name = "JASSM-XR", mass = 2200.0, mach_max = 0.92,range_max = 1850000, fuel_mass = 950.0, impulse = 3400, burn_time = 2400.0,warhead_mass = 450.0, picture = "agm154.png",life_time = 3600 },
    { id = "NG_LRASM",           clsid = "{NEXTGEN_LRASM}",          role = "cruise", polar = "FM_CRUISE_STEALTH", shape = "ng_jassm_taurus",  caliber = 0.450, length = 4.27, display_name = "AGM-158C LRASM (NextGen)",          short_name = "LRASM",    mass = 1100.0, mach_max = 0.92,range_max = 550000,  fuel_mass = 260.0, impulse = 3200, burn_time = 900.0, warhead_mass = 454.0, picture = "agm84d.png",life_time = 2000 },
    { id = "NG_SOM_J",           clsid = "{NEXTGEN_SOM_J}",          role = "cruise", polar = "FM_CRUISE_STEALTH", shape = "ng_jassm_taurus",  caliber = 0.340, length = 3.90, display_name = "TUBITAK SOM-J F-35 Bay Cruise (NG)",short_name = "SOM-J",    mass = 540.0,  mach_max = 0.92,range_max = 275000,  fuel_mass = 140.0, impulse = 2900, burn_time = 650.0, warhead_mass = 140.0, picture = "agm154.png",life_time = 1200 },
    { id = "NG_KH_69",           clsid = "{NEXTGEN_KH_69}",          role = "cruise", polar = "FM_CRUISE_STEALTH", shape = "ng_jassm_taurus",  caliber = 0.400, length = 4.19, display_name = "Kh-69 Stealth Cruise (NextGen)",    short_name = "Kh-69",    mass = 770.0,  mach_max = 0.95,range_max = 290000,  fuel_mass = 180.0, impulse = 2800, burn_time = 600.0, warhead_mass = 310.0, picture = "agm154.png",life_time = 1200 },
    { id = "NG_KH_50",           clsid = "{NEXTGEN_KH_50}",          role = "cruise", polar = "FM_CRUISE_STEALTH", shape = "ng_stealth_cruise",caliber = 0.560, length = 6.00, display_name = "Kh-50 Compact ALCM (NextGen)",      short_name = "Kh-50",    mass = 1600.0, mach_max = 0.94,range_max = 1500000, fuel_mass = 620.0, impulse = 3300, burn_time = 1800.0,warhead_mass = 450.0, picture = "agm154.png",life_time = 2800 },
    { id = "NG_KH_101",          clsid = "{NEXTGEN_KH_101}",         role = "cruise", polar = "FM_CRUISE_STEALTH", shape = "ng_stealth_cruise",caliber = 0.742, length = 7.45, display_name = "Kh-101 Strategic ALCM (NextGen)",   short_name = "Kh-101",   mass = 2400.0, mach_max = 0.92,range_max = 2500000, fuel_mass = 1050.0,impulse = 3400, burn_time = 2400.0,warhead_mass = 450.0, picture = "agm154.png",life_time = 3600 },
    { id = "NG_GBU_53",          clsid = "{NEXTGEN_GBU_53}",         role = "glide",  polar = "FM_GLIDE_BOMB",     shape = "ng_glide_sdb",     caliber = 0.180, length = 1.76, display_name = "GBU-53/B StormBreaker (NextGen)",   short_name = "GBU-53",   mass = 93.0,   mach_max = 0.95,range_max = 110000,  fuel_mass = 2.0,   impulse = 200,  burn_time = 2.0,   warhead_mass = 48.0,  picture = "gbu38.png" },
    { id = "NG_JSOW_ER",         clsid = "{NEXTGEN_JSOW_ER}",        role = "cruise", polar = "FM_GLIDE_BOMB",     shape = "ng_glide_sdb",     caliber = 0.330, length = 4.10, display_name = "AGM-154C-1 JSOW-ER (NextGen)",      short_name = "JSOW-ER",  mass = 495.0,  mach_max = 0.95,range_max = 560000,  fuel_mass = 90.0,  impulse = 2600, burn_time = 400.0, warhead_mass = 225.0, picture = "agm154.png" },
    { id = "NG_SPEAR_3",         clsid = "{NEXTGEN_SPEAR_3}",        role = "cruise", polar = "FM_CRUISE_STEALTH", shape = "ng_glide_sdb",     caliber = 0.180, length = 1.80, display_name = "MBDA SPEAR 3 (NextGen)",            short_name = "SPEAR-3",  mass = 90.0,   mach_max = 0.95,range_max = 140000,  fuel_mass = 22.0,  impulse = 2400, burn_time = 320.0, warhead_mass = 40.0,  picture = "gbu38.png" },
    { id = "NG_MALD_J",          clsid = "{NEXTGEN_MALD_J}",         role = "cruise", polar = "FM_CRUISE_STEALTH", shape = "ng_glide_sdb",     caliber = 0.180, length = 2.84, display_name = "ADM-160 MALD-J Decoy (NextGen)",    short_name = "MALD-J",   mass = 115.0,  mach_max = 0.91,range_max = 920000,  fuel_mass = 45.0,  impulse = 3000, burn_time = 1200.0,warhead_mass = 5.0,   picture = "agm154.png",life_time = 1800 },

    -- 6. AASM Hammer Sub-Variants (3)
    { id = "NG_AASM_250",        clsid = "{NEXTGEN_AASM_250}",       role = "sead",   polar = "FM_GLIDE_BOMB", shape = "ng_aasm_hammer", caliber = 0.273, length = 3.10, display_name = "AASM-250 Hammer (NextGen)",       short_name = "AASM-250", mass = 340.0,  mach_max = 1.15, range_max = 75000, fuel_mass = 28.0, impulse = 225, burn_time = 8.0,  warhead_mass = 120.0, picture = "gbu38.png" },
    { id = "NG_AASM_500",        clsid = "{NEXTGEN_AASM_500}",       role = "sead",   polar = "FM_GLIDE_BOMB", shape = "ng_aasm_hammer", caliber = 0.320, length = 3.35, display_name = "AASM-500 Hammer Heavy (NextGen)", short_name = "AASM-500", mass = 540.0,  mach_max = 1.10, range_max = 72000, fuel_mass = 40.0, impulse = 228, burn_time = 9.0,  warhead_mass = 230.0, picture = "gbu38.png" },
    { id = "NG_AASM_1000",       clsid = "{NEXTGEN_AASM_1000}",      role = "sead",   polar = "FM_GLIDE_BOMB", shape = "ng_aasm_hammer", caliber = 0.360, length = 3.60, display_name = "AASM-1000 Hammer (NextGen)",      short_name = "AASM-1T",  mass = 1050.0, mach_max = 1.05, range_max = 70000, fuel_mass = 55.0, impulse = 230, burn_time = 10.0, warhead_mass = 450.0, picture = "gbu31.png" },

    -- 7. Loitering Munitions / One-Way Attack & Jet Drones (16)
    { id = "NG_SHAHED_136",      clsid = "{NEXTGEN_SHAHED_136}",     role = "loiter", polar = "FM_LOITER_DRONE", shape = "ng_shahed_136",     caliber = 0.320, length = 3.50, display_name = "Shahed-136 / Geran-2 Delta (NG)",   short_name = "Shahed136",mass = 200.0, mach_max = 0.25, range_max = 1800000, fuel_mass = 55.0, impulse = 3600, burn_time = 3600.0,warhead_mass = 50.0, picture = "gbu38.png", life_time = 3600 },
    { id = "NG_SHAHED_131",      clsid = "{NEXTGEN_SHAHED_131}",     role = "loiter", polar = "FM_LOITER_DRONE", shape = "ng_shahed_136",     caliber = 0.240, length = 2.60, display_name = "Shahed-131 / Geran-1 Mini-Delta",   short_name = "Shahed131",mass = 135.0, mach_max = 0.24, range_max = 900000,  fuel_mass = 35.0, impulse = 3400, burn_time = 2400.0,warhead_mass = 20.0, picture = "gbu38.png", life_time = 2400 },
    { id = "NG_SHAHED_238",      clsid = "{NEXTGEN_SHAHED_238}",     role = "loiter", polar = "FM_CRUISE_STEALTH",shape = "ng_shahed_238",     caliber = 0.340, length = 3.50, display_name = "Shahed-238 / Geran-3 Turbojet (NG)",short_name = "Shahed238",mass = 260.0, mach_max = 0.72, range_max = 800000,  fuel_mass = 75.0, impulse = 2800, burn_time = 1500.0,warhead_mass = 50.0, picture = "agm154.png",life_time = 1800 },
    { id = "NG_PALIANYTSIA",     clsid = "{NEXTGEN_PALIANYTSIA}",    role = "loiter", polar = "FM_CRUISE_STEALTH",shape = "ng_palianytsia_jet",caliber = 0.320, length = 3.40, display_name = "Palianytsia Turbojet Drone (NG)",   short_name = "Palynytsa",mass = 320.0, mach_max = 0.75, range_max = 700000,  fuel_mass = 90.0, impulse = 2900, burn_time = 1400.0,warhead_mass = 65.0, picture = "agm154.png",life_time = 1800 },
    { id = "NG_PEKLO",           clsid = "{NEXTGEN_PEKLO}",          role = "loiter", polar = "FM_CRUISE_STEALTH",shape = "ng_palianytsia_jet",caliber = 0.280, length = 2.80, display_name = "Peklo Jet Drone-Missile (NextGen)", short_name = "Peklo",    mass = 220.0, mach_max = 0.70, range_max = 700000,  fuel_mass = 68.0, impulse = 2900, burn_time = 1300.0,warhead_mass = 45.0, picture = "agm154.png",life_time = 1700 },
    { id = "NG_AQ_400_SCYTHE",   clsid = "{NEXTGEN_AQ_400_SCYTHE}",  role = "loiter", polar = "FM_LOITER_DRONE", shape = "ng_palianytsia_jet",caliber = 0.300, length = 3.00, display_name = "AQ-400 Scythe Long-Range Drone",   short_name = "AQ-400",   mass = 150.0, mach_max = 0.28, range_max = 750000,  fuel_mass = 42.0, impulse = 3200, burn_time = 2400.0,warhead_mass = 42.0, picture = "gbu38.png", life_time = 2400 },
    { id = "NG_HAROP_AIR",       clsid = "{NEXTGEN_HAROP_AIR}",      role = "loiter", polar = "FM_LOITER_DRONE", shape = "ng_harop",          caliber = 0.280, length = 2.50, display_name = "IAI Harop SEAD Drone (NextGen)",    short_name = "Harop",    mass = 135.0, mach_max = 0.45, range_max = 200000,  fuel_mass = 35.0, impulse = 2600, burn_time = 900.0, warhead_mass = 23.0, picture = "gbu38.png", life_time = 1500 },
    { id = "NG_HARPY_NG",        clsid = "{NEXTGEN_HARPY_NG}",       role = "loiter", polar = "FM_LOITER_DRONE", shape = "ng_harop",          caliber = 0.280, length = 2.70, display_name = "IAI Harpy NG Anti-Radar Drone",     short_name = "Harpy-NG", mass = 160.0, mach_max = 0.42, range_max = 500000,  fuel_mass = 48.0, impulse = 2800, burn_time = 1600.0,warhead_mass = 32.0, picture = "gbu38.png", life_time = 2000 },
    { id = "NG_ALTIUS_600M",     clsid = "{NEXTGEN_ALTIUS_600M}",    role = "loiter", polar = "FM_LOITER_DRONE", shape = "ng_harop",          caliber = 0.140, length = 1.60, display_name = "ALTIUS-600M Tube Loiterer (NG)",    short_name = "ALTIUS6",  mass = 12.2,  mach_max = 0.25, range_max = 440000,  fuel_mass = 3.5,  impulse = 3200, burn_time = 1800.0,warhead_mass = 3.2,  picture = "gbu38.png", life_time = 2000 },
    { id = "NG_LANCET_AIR",      clsid = "{NEXTGEN_LANCET_AIR}",     role = "loiter", polar = "FM_LOITER_DRONE", shape = "ng_loitering_x",    caliber = 0.150, length = 1.65, display_name = "Lancet-3 Air-Launched (NextGen)",   short_name = "Lancet-3", mass = 18.0,  mach_max = 0.35, range_max = 65000,   fuel_mass = 4.0,  impulse = 2200, burn_time = 600.0, warhead_mass = 5.0,  picture = "gbu38.png", life_time = 900 },
    { id = "NG_LANCET_3M",       clsid = "{NEXTGEN_LANCET_3M}",      role = "loiter", polar = "FM_LOITER_DRONE", shape = "ng_loitering_x",    caliber = 0.160, length = 1.75, display_name = "Lancet-3M Izdeliye-51M (NextGen)",  short_name = "Lancet-3M",mass = 22.0,  mach_max = 0.38, range_max = 80000,   fuel_mass = 5.5,  impulse = 2400, burn_time = 720.0, warhead_mass = 8.0,  picture = "gbu38.png", life_time = 1000 },
    { id = "NG_KUB_BLA",         clsid = "{NEXTGEN_KUB_BLA}",        role = "loiter", polar = "FM_LOITER_DRONE", shape = "ng_shahed_136",     caliber = 0.140, length = 1.21, display_name = "ZALA KUB-BLA Loitering Delta (NG)", short_name = "KUB-BLA",  mass = 14.0,  mach_max = 0.25, range_max = 40000,   fuel_mass = 2.5,  impulse = 2000, burn_time = 600.0, warhead_mass = 3.0,  picture = "gbu38.png", life_time = 900 },
    { id = "NG_HERO_120",        clsid = "{NEXTGEN_HERO_120}",       role = "loiter", polar = "FM_LOITER_DRONE", shape = "ng_loitering_x",    caliber = 0.140, length = 1.50, display_name = "UVision HERO-120 Anti-Armor (NG)",  short_name = "HERO-120", mass = 18.0,  mach_max = 0.32, range_max = 60000,   fuel_mass = 3.5,  impulse = 2300, burn_time = 720.0, warhead_mass = 4.5,  picture = "gbu38.png", life_time = 1000 },
    { id = "NG_HERO_400EC",      clsid = "{NEXTGEN_HERO_400EC}",     role = "loiter", polar = "FM_LOITER_DRONE", shape = "ng_loitering_x",    caliber = 0.200, length = 2.10, display_name = "UVision HERO-400EC Long-Endurance",  short_name = "HERO-400", mass = 50.0,  mach_max = 0.35, range_max = 150000,  fuel_mass = 10.0, impulse = 2500, burn_time = 1200.0,warhead_mass = 10.0, picture = "gbu38.png", life_time = 1600 },
    { id = "NG_WARMATE",         clsid = "{NEXTGEN_WARMATE}",        role = "loiter", polar = "FM_LOITER_DRONE", shape = "ng_loitering_x",    caliber = 0.110, length = 1.10, display_name = "WB Electronics Warmate 2 (NG)",     short_name = "Warmate",  mass = 8.5,   mach_max = 0.28, range_max = 35000,   fuel_mass = 1.8,  impulse = 2000, burn_time = 480.0, warhead_mass = 2.0,  picture = "gbu38.png", life_time = 700 },
    { id = "NG_SWARM_GLIDER",    clsid = "{NEXTGEN_SWARM_GLIDER}",   role = "loiter", polar = "FM_LOITER_DRONE", shape = "ng_loitering_x",    caliber = 0.120, length = 1.25, display_name = "Switchblade 600 / FPV Drone (NG)",  short_name = "SB-600",   mass = 15.0,  mach_max = 0.38, range_max = 50000,   fuel_mass = 3.0,  impulse = 2100, burn_time = 450.0, warhead_mass = 4.5,  picture = "gbu38.png", life_time = 700 },

    -- 8. Special / Experimental AAMs (4)
    { id = "NG_PL_17",           clsid = "{NEXTGEN_PL_17}",          role = "aam", polar = "FM_AAM_ULTRA", shape = "ng_pl17_long", caliber = 0.260, length = 6.00, display_name = "PL-17 AWACS-Killer (NextGen)",     short_name = "PL-17",    mass = 450.0, mach_max = 5.5, range_max = 350000, fuel_mass = 210.0, impulse = 265, burn_time = 16.0, warhead_mass = 45.0, picture = "aim120c.png", life_time = 260 },
    { id = "NG_PYTHON_5",        clsid = "{NEXTGEN_PYTHON_5}",       role = "aam", polar = "FM_AAM_WVR",   shape = "ng_python5",   caliber = 0.160, length = 3.10, display_name = "Rafael Python-5 (NextGen)",        short_name = "Python-5", mass = 105.0, mach_max = 4.0, range_max = 35000,  fuel_mass = 34.0,  impulse = 240, burn_time = 5.2,  warhead_mass = 11.0, picture = "aim9x.png",   head_type = 1, life_time = 70 },
    { id = "NG_AIM_9X_BLK3",     clsid = "{NEXTGEN_AIM_9X_BLK3}",    role = "aam", polar = "FM_AAM_WVR",   shape = "ng_aim9x_b3",  caliber = 0.127, length = 3.02, display_name = "AIM-9X Block III LOAL (NextGen)",  short_name = "AIM-9X3",  mass = 88.0,  mach_max = 3.4, range_max = 45000,  fuel_mass = 31.0,  impulse = 245, burn_time = 5.5,  warhead_mass = 10.0, picture = "aim9x.png",   head_type = 1, life_time = 80 },
    { id = "NG_PEREGRINE",       clsid = "{NEXTGEN_PEREGRINE}",      role = "aam", polar = "FM_AAM_BVR",   shape = "ng_peregrine", caliber = 0.120, length = 1.80, display_name = "Raytheon Peregrine Mini-BVR (NG)", short_name = "Peregrn",  mass = 68.0,  mach_max = 4.2, range_max = 90000,  fuel_mass = 28.0,  impulse = 252, burn_time = 7.0,  warhead_mass = 9.0,  picture = "aim120c.png", life_time = 120 },

    -- 9. v5 Backlog Cruise, Precision Artillery, MRBMs, Anti-Ship, SEAD, Drones & KEKA Njiwa-1 (+32)
    { id = "NG_BGM109_BLK5",     clsid = "{NEXTGEN_BGM109_BLK5}",    role = "cruise", polar = "FM_CRUISE_STEALTH", shape = "ng_tomahawk_v",      caliber = 0.520, length = 6.25, display_name = "BGM-109 Tomahawk Block V MST (NG)",short_name = "BGM109-V", mass = 1510.0, mach_max = 0.90, range_max = 1600000, fuel_mass = 450.0, impulse = 3200, burn_time = 1800.0, warhead_mass = 450.0, picture = "agm84d.png", life_time = 3200 },
    { id = "NG_BGM109_BLK4",     clsid = "{NEXTGEN_BGM109_BLK4}",    role = "cruise", polar = "FM_CRUISE_STEALTH", shape = "ng_tomahawk_v",      caliber = 0.520, length = 6.25, display_name = "BGM-109E Tactical Tomahawk IV",    short_name = "BGM109-4", mass = 1480.0, mach_max = 0.88, range_max = 1500000, fuel_mass = 430.0, impulse = 3100, burn_time = 1700.0, warhead_mass = 450.0, picture = "agm84d.png", life_time = 3000 },
    { id = "NG_M31A2_GMLRS",     clsid = "{NEXTGEN_M31A2_GMLRS}",    role = "ballistic", polar = "FM_HYPERSONIC", shape = "ng_gmlrs_m31",      caliber = 0.227, length = 3.94, display_name = "M31A2 GMLRS Unitary Air-Launch",   short_name = "M31A2",    mass = 302.0,  mach_max = 2.6,  range_max = 85000,   fuel_mass = 95.0,  impulse = 245,  burn_time = 8.0,    warhead_mass = 91.0,  picture = "hydra.png" },
    { id = "NG_ER_GMLRS",        clsid = "{NEXTGEN_ER_GMLRS}",       role = "ballistic", polar = "FM_HYPERSONIC", shape = "ng_gmlrs_m31",      caliber = 0.254, length = 4.10, display_name = "ER-GMLRS 150km Precision Rocket",  short_name = "ER-GMLRS", mass = 360.0,  mach_max = 3.2,  range_max = 150000,  fuel_mass = 135.0, impulse = 255,  burn_time = 11.0,   warhead_mass = 91.0,  picture = "hydra.png" },
    { id = "NG_TORNADO_S_9M544", clsid = "{NEXTGEN_TORNADO_9M544}",  role = "ballistic", polar = "FM_HYPERSONIC", shape = "ng_gmlrs_m31",      caliber = 0.300, length = 7.60, display_name = "Tornado-S 9M544 300mm Guided (NG)",short_name = "9M544",    mass = 828.0,  mach_max = 3.5,  range_max = 120000,  fuel_mass = 320.0, impulse = 250,  burn_time = 12.0,   warhead_mass = 240.0, picture = "hydra.png" },
    { id = "NG_TRG_230",         clsid = "{NEXTGEN_TRG_230}",        role = "ballistic", polar = "FM_HYPERSONIC", shape = "ng_gmlrs_m31",      caliber = 0.230, length = 3.40, display_name = "Roketsan TRG-230 Laser-GPS (NG)",  short_name = "TRG-230",  mass = 215.0,  mach_max = 2.5,  range_max = 70000,   fuel_mass = 78.0,  impulse = 240,  burn_time = 7.5,    warhead_mass = 42.0,  picture = "hydra.png" },
    { id = "NG_TRG_300_KAPLAN",  clsid = "{NEXTGEN_TRG_300}",        role = "ballistic", polar = "FM_HYPERSONIC", shape = "ng_gmlrs_m31",      caliber = 0.300, length = 5.24, display_name = "Roketsan TRG-300 Kaplan Blk II",   short_name = "TRG-300",  mass = 585.0,  mach_max = 3.6,  range_max = 120000,  fuel_mass = 240.0, impulse = 252,  burn_time = 11.0,   warhead_mass = 105.0, picture = "hydra.png" },
    { id = "NG_TAYFUN",          clsid = "{NEXTGEN_TAYFUN}",         role = "ballistic", polar = "FM_HYPERSONIC", shape = "ng_iskander_atacms",caliber = 0.610, length = 6.50, display_name = "Roketsan Tayfun Hypersonic MRBM",  short_name = "Tayfun",   mass = 2300.0, mach_max = 6.5,  range_max = 560000,  fuel_mass = 1100.0,impulse = 265,  burn_time = 38.0,   warhead_mass = 470.0, picture = "agm88.png" },
    { id = "NG_BORA_KHAN",       clsid = "{NEXTGEN_BORA_KHAN}",      role = "ballistic", polar = "FM_HYPERSONIC", shape = "ng_iskander_atacms",caliber = 0.610, length = 6.10, display_name = "Roketsan Bora / Khan TBM (NG)",    short_name = "Bora-TBM", mass = 2500.0, mach_max = 5.0,  range_max = 280000,  fuel_mass = 1100.0,impulse = 258,  burn_time = 30.0,   warhead_mass = 470.0, picture = "agm88.png" },
    { id = "NG_HYUNMOO_4",       clsid = "{NEXTGEN_HYUNMOO_4}",      role = "ballistic", polar = "FM_HYPERSONIC", shape = "ng_iskander_atacms",caliber = 0.720, length = 7.40, display_name = "Hyunmoo-IV 2-Ton Bunker-Buster",   short_name = "Hyunmoo4", mass = 4200.0, mach_max = 7.0,  range_max = 800000,  fuel_mass = 1800.0,impulse = 268,  burn_time = 45.0,   warhead_mass = 2000.0,picture = "gbu31.png", penetrator = true },
    { id = "NG_PRALAY",          clsid = "{NEXTGEN_PRALAY}",         role = "ballistic", polar = "FM_HYPERSONIC", shape = "ng_iskander_atacms",caliber = 0.650, length = 6.80, display_name = "DRDO Pralay Quasi-Ballistic (NG)", short_name = "Pralay",   mass = 5000.0, mach_max = 6.0,  range_max = 500000,  fuel_mass = 2200.0,impulse = 262,  burn_time = 36.0,   warhead_mass = 700.0, picture = "agm88.png" },
    { id = "NG_KN_23",           clsid = "{NEXTGEN_KN_23}",          role = "ballistic", polar = "FM_HYPERSONIC", shape = "ng_iskander_atacms",caliber = 0.920, length = 7.50, display_name = "KN-23 Quasi-Ballistic SRBM (NG)",  short_name = "KN-23",    mass = 3400.0, mach_max = 6.2,  range_max = 600000,  fuel_mass = 1500.0,impulse = 264,  burn_time = 40.0,   warhead_mass = 500.0, picture = "agm88.png" },
    { id = "NG_FATEH_313",       clsid = "{NEXTGEN_FATEH_313}",      role = "ballistic", polar = "FM_HYPERSONIC", shape = "ng_rampage_lora",   caliber = 0.610, length = 8.80, display_name = "Fateh-313 Composite Precision",    short_name = "Fateh313", mass = 3450.0, mach_max = 4.8,  range_max = 500000,  fuel_mass = 1600.0,impulse = 258,  burn_time = 34.0,   warhead_mass = 500.0, picture = "agm88.png" },
    { id = "NG_ZOLFAGHAR",       clsid = "{NEXTGEN_ZOLFAGHAR}",      role = "ballistic", polar = "FM_HYPERSONIC", shape = "ng_iskander_atacms",caliber = 0.680, length = 10.30,display_name = "Zolfaghar 700km Tactical SRBM",    short_name = "Zolfaghr", mass = 4600.0, mach_max = 5.8,  range_max = 700000,  fuel_mass = 2100.0,impulse = 260,  burn_time = 42.0,   warhead_mass = 580.0, picture = "agm88.png" },
    { id = "NG_ROCKS_ALBM",      clsid = "{NEXTGEN_ROCKS_ALBM}",     role = "ballistic", polar = "FM_HYPERSONIC", shape = "ng_rampage_lora",   caliber = 0.420, length = 4.70, display_name = "Rafael ROCKS Supersonic ALBM (NG)",short_name = "ROCKS",    mass = 1200.0, mach_max = 4.8,  range_max = 300000,  fuel_mass = 480.0, impulse = 262,  burn_time = 24.0,   warhead_mass = 400.0, picture = "agm88.png", penetrator = true },
    { id = "NG_KD_88",           clsid = "{NEXTGEN_KD_88}",          role = "cruise",    polar = "FM_CRUISE_STEALTH", shape = "ng_kalibr_3m54",  caliber = 0.360, length = 4.50, display_name = "KD-88 / TL-7 Stand-Off ASM (NG)",  short_name = "KD-88",    mass = 720.0,  mach_max = 0.90, range_max = 200000,  fuel_mass = 200.0, impulse = 2800, burn_time = 650.0,  warhead_mass = 190.0, picture = "agm84d.png", life_time = 1200 },
    { id = "NG_CM_400AKG",       clsid = "{NEXTGEN_CM_400AKG}",      role = "ballistic", polar = "FM_HYPERSONIC", shape = "ng_kinzhal",        caliber = 0.400, length = 5.10, display_name = "CM-400AKG Hypersonic ASM (NG)",    short_name = "CM-400",   mass = 910.0,  mach_max = 5.0,  range_max = 240000,  fuel_mass = 380.0, impulse = 264,  burn_time = 20.0,   warhead_mass = 200.0, picture = "agm88.png" },
    { id = "NG_AGM_78D",         clsid = "{NEXTGEN_AGM_78D}",        role = "sead",      polar = "FM_AAM_ULTRA",  shape = "ng_sam_40n6",       caliber = 0.343, length = 4.57, display_name = "AGM-78D Standard ARM SEAD (NG)",   short_name = "AGM-78D",  mass = 620.0,  mach_max = 2.5,  range_max = 90000,   fuel_mass = 240.0, impulse = 250,  burn_time = 18.0,   warhead_mass = 97.0,  picture = "agm88.png" },
    { id = "NG_KH_25MPU",        clsid = "{NEXTGEN_KH_25MPU}",       role = "sead",      polar = "FM_AAM_BVR",    shape = "ng_kh58ushke",      caliber = 0.275, length = 4.19, display_name = "Kh-25MPU Passive Anti-Radar (NG)", short_name = "Kh-25MPU", mass = 320.0,  mach_max = 2.4,  range_max = 40000,   fuel_mass = 110.0, impulse = 242,  burn_time = 12.0,   warhead_mass = 89.0,  picture = "agm88.png" },
    { id = "NG_KH_28",           clsid = "{NEXTGEN_KH_28}",          role = "sead",      polar = "FM_AAM_ULTRA",  shape = "ng_kh58ushke",      caliber = 0.430, length = 6.00, display_name = "Kh-28 Heavy Anti-Radar (NextGen)", short_name = "Kh-28",    mass = 715.0,  mach_max = 3.0,  range_max = 110000,  fuel_mass = 290.0, impulse = 255,  burn_time = 22.0,   warhead_mass = 155.0, picture = "agm88.png" },
    { id = "NG_YJ_62",           clsid = "{NEXTGEN_YJ_62}",          role = "cruise",    polar = "FM_CRUISE_STEALTH", shape = "ng_tomahawk_v",   caliber = 0.540, length = 6.10, display_name = "YJ-62 / C-602 Long-Range AShM",    short_name = "YJ-62",    mass = 1350.0, mach_max = 0.90, range_max = 400000,  fuel_mass = 380.0, impulse = 3000, burn_time = 1200.0, warhead_mass = 300.0, picture = "agm84d.png", life_time = 1600 },
    { id = "NG_C_802A",          clsid = "{NEXTGEN_C_802A}",         role = "cruise",    polar = "FM_CRUISE_STEALTH", shape = "ng_kh35u",        caliber = 0.360, length = 5.14, display_name = "C-802A Sea-Skimmer AShM (NG)",     short_name = "C-802A",   mass = 682.0,  mach_max = 0.90, range_max = 180000,  fuel_mass = 195.0, impulse = 2800, burn_time = 650.0,  warhead_mass = 165.0, picture = "agm84d.png", life_time = 1200 },
    { id = "NG_HAESEONG",        clsid = "{NEXTGEN_HAESEONG}",       role = "cruise",    polar = "FM_CRUISE_STEALTH", shape = "ng_kh35u",        caliber = 0.340, length = 4.80, display_name = "SSM-700K Haeseong Sea Star (NG)",  short_name = "Haeseong", mass = 718.0,  mach_max = 0.90, range_max = 180000,  fuel_mass = 200.0, impulse = 2850, burn_time = 650.0,  warhead_mass = 250.0, picture = "agm84d.png", life_time = 1200 },
    { id = "NG_HSIUNG_FENG_2",   clsid = "{NEXTGEN_HF_2}",           role = "cruise",    polar = "FM_CRUISE_STEALTH", shape = "ng_exocet_am39",  caliber = 0.340, length = 4.80, display_name = "HF-2 Hsiung Feng II AShM (NG)",    short_name = "HF-2",     mass = 685.0,  mach_max = 0.85, range_max = 160000,  fuel_mass = 180.0, impulse = 2750, burn_time = 580.0,  warhead_mass = 180.0, picture = "agm84d.png", life_time = 1100 },
    { id = "NG_EXOCET_MM40_3C",  clsid = "{NEXTGEN_MM40_B3C}",       role = "cruise",    polar = "FM_CRUISE_STEALTH", shape = "ng_exocet_am39",  caliber = 0.350, length = 5.80, display_name = "Exocet MM40 Blk 3c Coherent (NG)", short_name = "MM40-3c",  mass = 780.0,  mach_max = 0.93, range_max = 200000,  fuel_mass = 220.0, impulse = 2900, burn_time = 700.0,  warhead_mass = 165.0, picture = "agm84d.png", life_time = 1200 },
    { id = "NG_ALTIUS_700M",     clsid = "{NEXTGEN_ALTIUS_700M}",    role = "loiter",    polar = "FM_LOITER_DRONE",   shape = "ng_harop",        caliber = 0.200, length = 2.10, display_name = "Anduril ALTIUS-700M Loiter (NG)",  short_name = "ALTIUS7",  mass = 30.0,   mach_max = 0.30, range_max = 160000,  fuel_mass = 9.0,   impulse = 2800, burn_time = 1600.0, warhead_mass = 15.0,  picture = "gbu38.png", life_time = 1800 },
    { id = "NG_HERO_30",         clsid = "{NEXTGEN_HERO_30}",        role = "loiter",    polar = "FM_LOITER_DRONE",   shape = "ng_loitering_x",  caliber = 0.100, length = 0.95, display_name = "UVision HERO-30 Tube Loiterer",    short_name = "HERO-30",  mass = 3.5,    mach_max = 0.25, range_max = 15000,   fuel_mass = 0.8,   impulse = 1900, burn_time = 450.0,  warhead_mass = 0.8,   picture = "gbu38.png", life_time = 600 },
    { id = "NG_GREEN_DRAGON",    clsid = "{NEXTGEN_GREEN_DRAGON}",   role = "loiter",    polar = "FM_LOITER_DRONE",   shape = "ng_loitering_x",  caliber = 0.140, length = 1.60, display_name = "IAI Green Dragon Tactical Drone",  short_name = "GrnDrgn",  mass = 15.0,   mach_max = 0.28, range_max = 40000,   fuel_mass = 3.5,   impulse = 2200, burn_time = 720.0,  warhead_mass = 3.0,   picture = "gbu38.png", life_time = 1000 },
    { id = "NG_KARGU_3",         clsid = "{NEXTGEN_KARGU_3}",        role = "loiter",    polar = "FM_LOITER_DRONE",   shape = "ng_loitering_x",  caliber = 0.120, length = 0.85, display_name = "STM Kargu-3 Precision Loiterer",   short_name = "Kargu-3",  mass = 7.5,    mach_max = 0.22, range_max = 15000,   fuel_mass = 1.5,   impulse = 1800, burn_time = 500.0,  warhead_mass = 1.8,   picture = "gbu38.png", life_time = 700 },
    { id = "NG_RAM_II",          clsid = "{NEXTGEN_RAM_II}",         role = "loiter",    polar = "FM_LOITER_DRONE",   shape = "ng_loitering_x",  caliber = 0.150, length = 1.55, display_name = "RAM II Loitering Munition (NG)",   short_name = "RAM-II",   mass = 16.0,   mach_max = 0.30, range_max = 45000,   fuel_mass = 3.8,   impulse = 2200, burn_time = 650.0,  warhead_mass = 4.0,   picture = "gbu38.png", life_time = 900 },
    { id = "NG_ORBITER_1K",      clsid = "{NEXTGEN_ORBITER_1K}",     role = "loiter",    polar = "FM_LOITER_DRONE",   shape = "ng_harop",        caliber = 0.160, length = 1.70, display_name = "Orbiter 1K Kingfisher Drone (NG)", short_name = "Orbt-1K",  mass = 13.0,   mach_max = 0.26, range_max = 100000,  fuel_mass = 3.2,   impulse = 2600, burn_time = 1200.0, warhead_mass = 2.5,   picture = "gbu38.png", life_time = 1500 },
    { id = "NG_KEKA_NJIWA1",     clsid = "{NEXTGEN_KEKA_NJIWA1}",    role = "ballistic", polar = "FM_KEKA_TROLL",   shape = "ng_keka_tropo6",  caliber = 0.420, length = 6.20, display_name = "KEKA Njiwa-1 MicroSat Booster!",   short_name = "Njiwa-1",  mass = 820.0,  mach_max = 5.0,  range_max = 500000,  fuel_mass = 420.0, impulse = 250,  burn_time = 24.0,   warhead_mass = 150.0, picture = "hydra.png", troll = true },
}

local ag_clsids = {
    ag_all   = {},
    east_aam = {},
    nato_aam = {},
    wvr_aam  = {},
}

for _, spec in ipairs(ag_specs) do
    local clsid = register_as(spec)
    if spec.role == "aam" then
        if spec.id == "NG_PL_17" then
            table.insert(ag_clsids.east_aam, clsid)
        elseif spec.id == "NG_PEREGRINE" then
            table.insert(ag_clsids.nato_aam, clsid)
        else
            table.insert(ag_clsids.wvr_aam, clsid)
        end
    else
        table.insert(ag_clsids.ag_all, clsid)
    end
end

-- Multi-rack loadouts (including Twin KEKA Troposphere Rack!)
local multi_racks = {
    {
        clsid = "{NEXTGEN_GBU_53_4X}",
        category = CAT_MISSILES,
        attr_id = "NG_GBU_53",
        display_name = "4x GBU-53/B StormBreaker Rack (NextGen)",
        weight = 420.0,
        picture = "gbu38.png",
        shape = "ng_glide_sdb",
        offsets = { {-0.14, -0.14, 0}, {0.14, -0.14, 0}, {-0.14, -0.32, 0}, {0.14, -0.32, 0} },
        target_list = ag_clsids.ag_all,
    },
    {
        clsid = "{NEXTGEN_SPEAR_3_3X}",
        category = CAT_MISSILES,
        attr_id = "NG_SPEAR_3",
        display_name = "3x MBDA SPEAR 3 Rack (NextGen)",
        weight = 315.0,
        picture = "gbu38.png",
        shape = "ng_glide_sdb",
        offsets = { {0, -0.12, 0}, {-0.16, -0.26, 0}, {0.16, -0.26, 0} },
        target_list = ag_clsids.ag_all,
    },
    {
        clsid = "{NEXTGEN_SPEAR_EW_3X}",
        category = CAT_MISSILES,
        attr_id = "NG_SPEAR_EW",
        display_name = "3x MBDA SPEAR-EW Jammer Rack (NextGen)",
        weight = 320.0,
        picture = "gbu38.png",
        shape = "ng_spear_ew",
        offsets = { {0, -0.12, 0}, {-0.16, -0.26, 0}, {0.16, -0.26, 0} },
        target_list = ag_clsids.ag_all,
    },
    {
        clsid = "{NEXTGEN_LANCET_3X}",
        category = CAT_MISSILES,
        attr_id = "NG_LANCET_AIR",
        display_name = "3x Lancet-3 Drone Pod (NextGen)",
        weight = 75.0,
        picture = "gbu38.png",
        shape = "ng_loitering_x",
        offsets = { {0, -0.10, 0}, {-0.18, -0.26, 0}, {0.18, -0.26, 0} },
        target_list = ag_clsids.ag_all,
    },
    {
        clsid = "{NEXTGEN_KEKA_2X}",
        category = CAT_MISSILES,
        attr_id = "NG_KEKA_TROPO5_AIR",
        display_name = "2x KEKA Troposphere-5 Twin Pod (Troll!)",
        weight = 430.0,
        picture = "hydra.png",
        shape = "ng_keka_tropo5",
        offsets = { {-0.24, -0.24, 0}, {0.24, -0.24, 0} },
        target_list = ag_clsids.ag_all,
    },
    {
        clsid = "{NEXTGEN_PEREGRINE_2X}",
        category = CAT_AIR_TO_AIR,
        attr_id = "NG_PEREGRINE",
        display_name = "2x Raytheon Peregrine Twin-Rack (NextGen)",
        weight = 165.0,
        picture = "aim120c.png",
        shape = "ng_peregrine",
        offsets = { {-0.13, -0.14, 0}, {0.13, -0.14, 0} },
        target_list = ag_clsids.nato_aam,
    },
    {
        clsid = "{NEXTGEN_TOMAHAWK_2X}",
        category = CAT_MISSILES,
        attr_id = "NG_BGM109_BLK5",
        display_name = "2x BGM-109 Tomahawk Block V Heavy Rack (NG)",
        weight = 3100.0,
        picture = "agm84d.png",
        shape = "ng_tomahawk_v",
        offsets = { {-0.38, -0.35, 0}, {0.38, -0.35, 0} },
        target_list = ag_clsids.ag_all,
    },
    {
        clsid = "{NEXTGEN_GMLRS_6X}",
        category = CAT_MISSILES,
        attr_id = "NG_ER_GMLRS",
        display_name = "6x ER-GMLRS Air-Launched Pod (NextGen)",
        weight = 2250.0,
        picture = "hydra.png",
        shape = "ng_gmlrs_m31",
        offsets = { {-0.30, -0.18, 0}, {0.0, -0.18, 0}, {0.30, -0.18, 0}, {-0.30, -0.45, 0}, {0.0, -0.45, 0}, {0.30, -0.45, 0} },
        target_list = ag_clsids.ag_all,
    },
}

for _, rack in ipairs(multi_racks) do
    local elements = {}
    for _, pos in ipairs(rack.offsets) do
        table.insert(elements, { ShapeName = rack.shape, Position = { 0, pos[2], pos[1] } })
    end
    declare_loadout({
        category = rack.category,
        CLSID = rack.clsid,
        Picture = rack.picture,
        displayName = _(rack.display_name),
        Weight = rack.weight,
        Cx_pil = 0.0032,
        Count = #rack.offsets,
        attribute = registered_attrs[rack.attr_id],
        Elements = elements,
    })
    table.insert(rack.target_list, rack.clsid)
end

return ag_clsids
