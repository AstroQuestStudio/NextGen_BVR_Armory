-- NextGen Tactical Expansion: Rockets, ATGMs, UMPK/UMPB/PAB/SPICE/JDAM-ER Glide Bombs, ASMs & WVR/BVR Sub-Variants
-- Uses physically calibrated Mach-indexed polars (polar_profiles.lua) + DrawArg 25 wing fold.

local polar = dofile(current_mod_path .. "/Database/polar_profiles.lua")

local function deep_copy(orig)
    if type(orig) ~= "table" then return orig end
    local copy = {}
    for k, v in pairs(orig) do
        copy[deep_copy(k)] = deep_copy(v)
    end
    return copy
end

local BASE_TACTICAL = {
    category = CAT_MISSILES,
    caliber = 0.178,
    mass = 150.0,
    model = "ng_atgm_quad",
    sounderName = "Weapons/Missile",
    targeting_data = { fm_type = -1 },
    type_name = "missile",
    wsTypeOfWeapon = { wsType_Weapon, wsType_Missile, wsType_AS_Missile, WSTYPE_PLACEHOLDER },
    Escort = 0, Head_Type = 4, sigma = { 3, 3, 3 }, M = 150.0,
    H_max = 18000, H_min = 1, H_min_t = 0, Diam = 178, Cx_pil = 1.8,
    D_max = 45000, D_min = 400, Head_Form = 1, Life_Time = 180, Nr_max = 22,
    v_min = 90, v_mid = 480, Mach_max = 2.5, t_b = 0.2, t_acc = 2.0, t_marsh = 12.0,
    Range_max = 60000, Fi_start = 1.0, Fi_rak = 3.14152, Fi_excort = 1.2, Fi_search = 1.2,
    OmViz_max = 0.6, PN_gain = 4, Reflection = 0.03, SeekerGen = 4, KillDistance = 0,
    X_back = -1.2, Y_back = 0, Z_back = 0, ccm_k0 = 0.06, hoj = 0, loft = 0,
    nozzle_exit_area = 0.012, scheme = "schemes/missiles/anti_rad_missile.sch",
    class_name = "wAmmunitionSelfHoming",
    controller = { boost_start = 0, march_start = 0.8 },
    exhaust = { 0.8, 0.8, 0.8, 0.05 },
    boost = {
        custom_smoke_dissipation_factor = 0.2, fuel_mass = 8.0, impulse = 220,
        nozzle_exit_area = 0.012, nozzle_orientationXYZ = { { 0, 0, 0 } },
        nozzle_position = { { -1.2, 0, 0 } }, smoke_color = { 0.8, 0.8, 0.8 },
        smoke_transparency = 0.1, tail_width = 0.25, work_time = 0.8,
    },
    march = {
        custom_smoke_dissipation_factor = 0.2, fuel_mass = 35.0, impulse = 250,
        nozzle_exit_area = 0.012, nozzle_orientationXYZ = { { 0, 0, 0 } },
        nozzle_position = { { -1.2, 0, 0 } }, smoke_color = { 0.8, 0.8, 0.8 },
        smoke_opacity_type = 1, smoke_transparency = 0.04, tail_width = 0.2, work_time = 10.0,
    },
    actuator = { D = 220, T1 = 0.004, T2 = 0.008, Tf = 0.008, fin_stall = 1, max_delta = 0.35, max_omega = 6.0, sim_count = 4 },
    autopilot = {
        Areq_limit = 18, K_heading_hor = 0.5, K_heading_ver = 0.3, K_loft = 2.0,
        Kconv = 3, Kd = 0.24, Ki = 0.01, Knv = 0.0024, Kout = 1, Krx = 2, Kx = 0.04,
        PN_dist_data = { 10000, 1, 3000, 1 }, alg = 0, bang_bang = 0, delay = 0.5,
        fins_limit = 0.35, fins_limit_x = 0.087, loft_active_by_default = 0,
        max_pitch_cmd = 0.55, max_signal_Fi = 0.25, min_a_conv_approach_vel = 60, min_horiz_time = 1,
        null_roll = 0.785398, op_time = 180, rotate_fins_output = 0, x_channel_delay = 0.5,
    },
    fm = deep_copy(polar.FM_AAM_BVR),
    seeker = {
        FOV = 2.09, abs_err_val = 2, aim_sigma = 3, aim_y_offset = 1.0,
        ang_err_val = 0.00014, blind_rad_val = 1, calc_aim_dist = 300000,
        delay = 0.8, err_correct_time = 1.5, guide_to_last_pos = true, keep_aim_time = 5,
        lock_manual_target_types_only = 0, max_w_LOS = 0.5, op_time = 180, pos_memory_time = 180,
        sens_far_dist = 90000, sens_near_dist = 50,
    },
    proximity_fuze = { arm_delay = 1.0, radius = 6 },
    warhead = {
        caliber = 178, concrete_factors = { 2.0, 2.0, 1.5 }, concrete_obj_factor = 1.5,
        cumulative_factor = 2.0, cumulative_thickness = 0.4, expl_mass = 30.0, fantom = 1,
        mass = 30.0, obj_factors = { 2.0, 2.0 }, other_factors = { 1.5, 1.5, 1.5 }, piercing_mass = 10.0,
    },
    warhead_air = {
        caliber = 178, concrete_factors = { 1, 1, 1 }, concrete_obj_factor = 0,
        cumulative_factor = 0, cumulative_thickness = 0, expl_mass = 30.0, fantom = 1,
        mass = 30.0, obj_factors = { 1, 1 }, other_factors = { 1, 1, 1 }, piercing_mass = 8.0,
    },
}

local BASE_FOLDING_GLIDE = {
    category = CAT_MISSILES,
    caliber = 0.300,
    mass = 250.0,
    model = "ng_umpb_d30",
    sounderName = "Weapons/Missile",
    targeting_data = { fm_type = -1 },
    type_name = "missile",
    wsTypeOfWeapon = { wsType_Weapon, wsType_Missile, wsType_AS_Missile, WSTYPE_PLACEHOLDER },
    Escort = 0, Head_Type = 5, Head_Form = 0, sigma = { 8, 8, 8 }, M = 250.0,
    H_max = 15000, H_min = -1, H_min_t = 0, Diam = 300, Cx_pil = 4.5,
    D_max = 110000, D_min = 1500, Life_Time = 900, Nr_max = 8,
    v_min = 120, v_mid = 215, Mach_max = 0.95, t_b = 0, t_acc = 3, t_marsh = 600,
    Range_max = 110000, Fi_start = 0.9, Fi_rak = 3.14152, Fi_excort = 0.9, Fi_search = 99.9,
    OmViz_max = 99.9, Reflection = 0.04, KillDistance = 0,
    X_back = -1.4, Y_back = 0, Z_back = 0,
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
        custom_smoke_dissipation_factor = 0.1, fuel_mass = 40.0, impulse = 2200,
        max_thrust = 900, min_fuel_rate = 0.002, min_thrust = -50,
        nozzle_orientationXYZ = { { 0, 0, 0 } }, nozzle_position = { { -1.4, 0, 0 } },
        smoke_color = { 0.7, 0.7, 0.7 }, smoke_transparency = 0.01,
        tail_width = 0.15, thrust_Tau = 0.002, work_time = 600.0,
    },
    control_block = {
        can_update_target_pos = 1, default_cruise_height = 80, obj_sensor = 0,
        seeker_activation_dist = 12000, turn_before_point_reach = 1,
        turn_hor_N = 1.4, turn_max_calc_angle_deg = 90, turn_point_trigger_dist = 200, use_horiz_dist = 1,
    },
    cruise_autopilot = {
        Kd_eng = 0, Kd_hor = 0, Kd_ver = 0, Kd_ver_st1 = 0.015, Kd_ver_st2 = 5e-05,
        Ki_eng = 0.003, Kii_ver = 0.2, Kp_eng = 220, Kp_hor_err = 240, Kp_hor_err_croll = 0.06,
        Kp_ver = 8.0, Kp_ver_st1 = 0.009, Kp_ver_st2 = 0.00018,
        alg_calc_time = 1.5, alg_div_k = 2, alg_max_sin_climb = 0.8,
        alg_points_num = 7, alg_section_temp_points = 3, alg_tmp_point_vel_k = 1.5,
        alg_vel_k = 6, auto_terrain_following = 1, auto_terrain_following_height = 100,
        delay = 1, eng_max_thrust = 1400, eng_min_thrust = -100, estimated_N_max = 6,
        finsLimit = 0.78, max_roll = 0.8, max_start_y_vel = 35, no_alg_vel_k = 10, stab_vel = 210,
    },
    final_autopilot = {
        J_Angle_K = 0.22, J_Angle_W = 0.7, J_Diff_K = 0.4, J_FinAngle_K = 0.35,
        J_Int_K = 0.001, J_Power_K = 2.0, J_Trigger_Vert = 1, K = 75, Kg = 4, Ki = 0,
        delay = 0, finsLimit = 0.78, hKd = 0.005, hKp_err = 120, hKp_err_croll = 0.04,
        max_roll = 0.8, useJumpByDefault = 1,
    },
    fm = deep_copy(polar.FM_GLIDE_BOMB),
    seeker = { can_update_target_pos = 1, coalition = 2, coalition_rnd_coeff = 5 },
    warhead = {
        caliber = 300, concrete_factors = { 3.5, 1.5, 5.0 }, concrete_obj_factor = 3.5,
        cumulative_factor = 0, cumulative_thickness = 0, default_fuze_delay = 0,
        expl_mass = 120.0, fantom = 1, is_htp = true, mass = 120.0,
        obj_factors = { 2.0, 1.5 }, other_factors = { 1.5, 1.5, 1.5 }, piercing_mass = 40.0,
    },
    warhead_air = {
        caliber = 300, concrete_factors = { 1, 1, 1 }, concrete_obj_factor = 0,
        cumulative_factor = 0, cumulative_thickness = 0, default_fuze_delay = 0,
        expl_mass = 120.0, fantom = 1, is_htp = true, mass = 120.0,
        obj_factors = { 1, 1 }, other_factors = { 1, 1, 1 }, piercing_mass = 20.0,
    },
}

local FOLDING_SHAPES = {
    ng_heavy_umpk     = true,
    ng_umpb_d30       = true,
    ng_stealth_cruise = true,
    ng_jassm_taurus   = true,
    ng_glide_sdb      = true,
    ng_spice_glide    = true,
    ng_kh35u          = true,
    ng_nsm_jsm        = true,
    ng_kalibr_3m54    = true,
    ng_javelin_top    = true,
    ng_loitering_x    = true,
    ng_tomahawk_v     = true,
}

local tac_attrs = {}

local function register_tac(spec)
    local is_folding = (spec.role ~= "aam") and FOLDING_SHAPES[spec.shape] and (spec.role ~= "ag")
    local w = deep_copy(is_folding and BASE_FOLDING_GLIDE or BASE_TACTICAL)

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
    w.Life_Time = spec.life_time or 600
    w.march.fuel_mass = spec.fuel_mass
    w.march.impulse = spec.impulse
    w.march.work_time = spec.burn_time
    w.t_marsh = spec.burn_time
    w.warhead.caliber = math.floor(spec.caliber * 1000)
    w.warhead.expl_mass = spec.warhead_mass
    w.warhead.mass = spec.warhead_mass
    w.warhead_air.caliber = math.floor(spec.caliber * 1000)
    w.warhead_air.expl_mass = spec.warhead_mass
    w.warhead_air.mass = spec.warhead_mass

    local default_polar = is_folding and ((spec.role == "cruise") and "FM_CRUISE_STEALTH" or "FM_GLIDE_BOMB") or ((spec.role == "aam") and ((spec.head_type == 1) and "FM_AAM_WVR" or "FM_AAM_BVR") or "FM_AAM_BVR")
    polar.apply_polar(w, spec.polar or default_polar, spec.caliber, spec.mass, spec.length)

    local back = -(spec.length * 0.5)
    w.X_back = back
    w.boost.nozzle_position = { { back + 0.05, 0, 0 } }
    w.march.nozzle_position = { { back + 0.05, 0, 0 } }

    if is_folding then
        w.fm.wingsDeplDelay = 1.0
        w.fm.wingsDeplProcTime = 2.5
        if spec.role == "cruise" then
            w.march.max_thrust = 3000
            w.cruise_autopilot.stab_vel = 230
        elseif spec.role == "loiter" then
            w.encyclopediaAnimation = { args = { [25] = 1, [407] = 0.35 } }
            w.cruise_autopilot.stab_vel = 65
            w.v_min = 35
            w.v_mid = 65
        end
    else
        w.autopilot.op_time = w.Life_Time
        w.seeker.op_time = w.Life_Time
        if spec.role == "aam" then
            w.category = CAT_AIR_TO_AIR
            w.wsTypeOfWeapon = { wsType_Weapon, wsType_Missile, wsType_AA_Missile, WSTYPE_PLACEHOLDER }
            w.scheme = "schemes/missiles/aa_missile_amraam2.sch"
            w.Head_Type = spec.head_type or 2
            w.proximity_fuze.radius = 15
        end
        if spec.shape == "ng_durandal_runway" then
            w.encyclopediaAnimation = { args = { [0] = 1 } }
        elseif spec.shape == "ng_atgm_quad" or spec.shape == "ng_javelin_top" then
            w.encyclopediaAnimation = { args = { [25] = 1 } }
        end
    end

    w.shape_table_data = {
        { name = spec.id, file = spec.shape, life = 1, fire = { 0, 1 }, username = spec.display_name, index = WSTYPE_PLACEHOLDER },
    }

    local registered = declare_weapon(w)
    tac_attrs[spec.id] = registered.wsTypeOfWeapon
    declare_loadout({
        category = (spec.role == "aam") and CAT_AIR_TO_AIR or CAT_MISSILES,
        CLSID = spec.clsid,
        Picture = spec.picture or "agm65d.png",
        displayName = _(spec.display_name),
        Weight = spec.mass,
        Cx_pil = 0.0018,
        attribute = registered.wsTypeOfWeapon,
        Elements = { { ShapeName = spec.shape } },
    })
    return spec.clsid
end

local tac_specs = {
    -- 1. Guided Rockets (8)
    { id = "NG_APKWS_HE",      clsid = "{NEXTGEN_APKWS_HE}",      role = "ag",     shape = "ng_guided_rocket",   caliber = 0.070, length = 1.75, display_name = "APKWS II 70mm Laser HE (NextGen)",    short_name = "APKWS-HE", mass = 15.0,   mach_max = 2.2, range_max = 12000,  fuel_mass = 3.5,   impulse = 220, burn_time = 2.0,   warhead_mass = 4.5,   picture = "hydra.png" },
    { id = "NG_APKWS_AP",      clsid = "{NEXTGEN_APKWS_AP}",      role = "ag",     shape = "ng_guided_rocket",   caliber = 0.070, length = 1.75, display_name = "APKWS II 70mm Laser AP (NextGen)",    short_name = "APKWS-AP", mass = 16.0,   mach_max = 2.2, range_max = 12000,  fuel_mass = 3.5,   impulse = 220, burn_time = 2.0,   warhead_mass = 4.0,   picture = "hydra.png" },
    { id = "NG_AGR_20_FALCO",  clsid = "{NEXTGEN_AGR20_FALCO}",   role = "aam",    shape = "ng_guided_rocket",   caliber = 0.070, length = 1.87, display_name = "AGR-20 FALCO Counter-Drone AAM (NG)", short_name = "FALCO",    mass = 15.0,   mach_max = 2.4, range_max = 14000,  fuel_mass = 3.8,   impulse = 225, burn_time = 2.2,   warhead_mass = 4.2,   picture = "hydra.png", head_type = 1 },
    { id = "NG_CIRIT_70MM",    clsid = "{NEXTGEN_CIRIT_70MM}",    role = "ag",     shape = "ng_guided_rocket",   caliber = 0.070, length = 1.90, display_name = "Roketsan CIRIT 70mm Laser (NG)",      short_name = "CIRIT",    mass = 15.0,   mach_max = 2.2, range_max = 10000,  fuel_mass = 3.5,   impulse = 220, burn_time = 2.0,   warhead_mass = 4.5,   picture = "hydra.png" },
    { id = "NG_ZUNI_LASER",    clsid = "{NEXTGEN_ZUNI_LASER}",    role = "ag",     shape = "ng_guided_rocket",   caliber = 0.127, length = 2.80, display_name = "Zuni 127mm Laser-Guided (NextGen)",   short_name = "Zuni-L",   mass = 58.0,   mach_max = 2.4, range_max = 18000,  fuel_mass = 14.0,  impulse = 230, burn_time = 3.0,   warhead_mass = 22.0,  picture = "zuni.png" },
    { id = "NG_S8_CORR",       clsid = "{NEXTGEN_S8_CORR}",       role = "ag",     shape = "ng_guided_rocket",   caliber = 0.080, length = 1.65, display_name = "S-8KOR 80mm Laser Rocket (NextGen)",  short_name = "S-8KOR",   mass = 15.5,   mach_max = 2.1, range_max = 10000,  fuel_mass = 3.8,   impulse = 220, burn_time = 1.8,   warhead_mass = 4.2,   picture = "s8.png" },
    { id = "NG_S13_DF",        clsid = "{NEXTGEN_S13_DF}",        role = "ag",     shape = "ng_guided_rocket",   caliber = 0.122, length = 2.90, display_name = "S-13DF 122mm Thermobaric (NextGen)",  short_name = "S-13DF",   mass = 68.0,   mach_max = 2.3, range_max = 14000,  fuel_mass = 16.0,  impulse = 230, burn_time = 2.5,   warhead_mass = 32.0,  picture = "s13.png" },
    { id = "NG_CRV7_PG",       clsid = "{NEXTGEN_CRV7_PG}",       role = "ag",     shape = "ng_guided_rocket",   caliber = 0.070, length = 1.75, display_name = "CRV7-PG High-Velocity (NextGen)",     short_name = "CRV7-PG",  mass = 14.5,   mach_max = 3.0, range_max = 15000,  fuel_mass = 4.0,   impulse = 245, burn_time = 2.2,   warhead_mass = 4.5,   picture = "hydra.png" },

    -- 2. ATGMs, Tacticals & Close Air Support (15)
    { id = "NG_JAGM",          clsid = "{NEXTGEN_JAGM}",          role = "ag",     shape = "ng_atgm_quad",       caliber = 0.178, length = 1.80, display_name = "AGM-179 JAGM Tri-Mode (NextGen)",     short_name = "JAGM",     mass = 49.0,   mach_max = 1.8, range_max = 28000,  fuel_mass = 12.0,  impulse = 235, burn_time = 5.0,   warhead_mass = 9.0,   picture = "agm114.png" },
    { id = "NG_BRIMSTONE_2",   clsid = "{NEXTGEN_BRIMSTONE_2}",   role = "ag",     shape = "ng_atgm_quad",       caliber = 0.180, length = 1.80, display_name = "MBDA Brimstone 2 MMW (NextGen)",      short_name = "Brimst-2", mass = 50.0,   mach_max = 1.8, range_max = 60000,  fuel_mass = 14.0,  impulse = 240, burn_time = 6.5,   warhead_mass = 8.5,   picture = "agm114.png" },
    { id = "NG_BRIMSTONE_3",   clsid = "{NEXTGEN_BRIMSTONE_3}",   role = "ag",     shape = "ng_atgm_quad",       caliber = 0.180, length = 1.80, display_name = "MBDA Brimstone 3 Tri-Mode (NextGen)", short_name = "Brimst-3", mass = 52.0,   mach_max = 2.0, range_max = 75000,  fuel_mass = 16.0,  impulse = 246, burn_time = 8.0,   warhead_mass = 9.0,   picture = "agm114.png" },
    { id = "NG_SPIKE_NLOS",    clsid = "{NEXTGEN_SPIKE_NLOS}",    role = "ag",     shape = "ng_atgm_quad",       caliber = 0.170, length = 1.67, display_name = "Spike NLOS 32km EO/IR (NextGen)",     short_name = "Spike-N",  mass = 71.0,   mach_max = 1.2, range_max = 32000,  fuel_mass = 18.0,  impulse = 250, burn_time = 45.0,  warhead_mass = 12.0,  picture = "agm65d.png" },
    { id = "NG_SPIKE_LR2",     clsid = "{NEXTGEN_SPIKE_LR2}",     role = "ag",     shape = "ng_javelin_top",     caliber = 0.130, length = 1.20, display_name = "Rafael Spike-LR2 Air-Pod (NextGen)",  short_name = "SpikeLR2", mass = 13.0,   mach_max = 1.1, range_max = 10000,  fuel_mass = 3.2,   impulse = 225, burn_time = 12.0,  warhead_mass = 4.0,   picture = "agm114.png" },
    { id = "NG_FGM_148F_JAV",  clsid = "{NEXTGEN_FGM148F_JAV}",   role = "ag",     shape = "ng_javelin_top",     caliber = 0.127, length = 1.25, display_name = "FGM-148F Javelin Air-Mount (NG)",     short_name = "JavelinF", mass = 15.9,   mach_max = 1.1, range_max = 6000,   fuel_mass = 3.5,   impulse = 220, burn_time = 8.0,   warhead_mass = 8.4,   picture = "agm114.png" },
    { id = "NG_AKERON_MP",     clsid = "{NEXTGEN_AKERON_MP}",     role = "ag",     shape = "ng_javelin_top",     caliber = 0.140, length = 1.30, display_name = "MBDA AKERON MP Pod-ATGM (NextGen)",   short_name = "AkeronMP", mass = 15.0,   mach_max = 1.2, range_max = 8000,   fuel_mass = 3.6,   impulse = 225, burn_time = 10.0,  warhead_mass = 5.0,   picture = "agm114.png" },
    { id = "NG_AKERON_LP",     clsid = "{NEXTGEN_AKERON_LP}",     role = "ag",     shape = "ng_atgm_quad",       caliber = 0.165, length = 1.80, display_name = "MBDA Akeron LP (NextGen)",            short_name = "AkeronLP", mass = 38.0,   mach_max = 1.4, range_max = 22000,  fuel_mass = 10.0,  impulse = 240, burn_time = 18.0,  warhead_mass = 8.0,   picture = "agm65d.png" },
    { id = "NG_VIKHR_M",       clsid = "{NEXTGEN_VIKHR_M}",       role = "ag",     shape = "ng_atgm_quad",       caliber = 0.130, length = 2.75, display_name = "9K121M Vikhr-M Tandem (NextGen)",     short_name = "Vikhr-M",  mass = 45.0,   mach_max = 2.0, range_max = 12000,  fuel_mass = 11.0,  impulse = 230, burn_time = 4.5,   warhead_mass = 12.0,  picture = "vikhr.png" },
    { id = "NG_HERMES_A",      clsid = "{NEXTGEN_HERMES_A}",      role = "ag",     shape = "ng_atgm_quad",       caliber = 0.210, length = 3.20, display_name = "Hermes-A Long-Range ATGM (NextGen)",  short_name = "Hermes-A", mass = 110.0,  mach_max = 3.0, range_max = 100000, fuel_mass = 38.0,  impulse = 250, burn_time = 14.0,  warhead_mass = 28.0,  picture = "agm65d.png" },
    { id = "NG_KH_38MLE",      clsid = "{NEXTGEN_KH_38MLE}",      role = "ag",     shape = "ng_kh38_grom",       caliber = 0.310, length = 4.20, display_name = "Kh-38MLE Laser Tact-ASM (NextGen)",   short_name = "Kh38MLE",  mass = 520.0,  mach_max = 2.2, range_max = 45000,  fuel_mass = 145.0, impulse = 245, burn_time = 12.0,  warhead_mass = 250.0, picture = "agm65d.png" },
    { id = "NG_KH_38MTE",      clsid = "{NEXTGEN_KH_38MTE}",      role = "ag",     shape = "ng_kh38_grom",       caliber = 0.310, length = 4.20, display_name = "Kh-38MTE IIR Imaging ASM (NextGen)", short_name = "Kh38MTE",  mass = 520.0,  mach_max = 2.2, range_max = 45000,  fuel_mass = 145.0, impulse = 245, burn_time = 12.0,  warhead_mass = 250.0, picture = "agm65d.png" },
    { id = "NG_GROM_E1",       clsid = "{NEXTGEN_GROM_E1}",       role = "ag",     shape = "ng_kh38_grom",       caliber = 0.310, length = 4.20, display_name = "Grom-E1 Powered Glide-ASM (NextGen)", short_name = "Grom-E1",  mass = 594.0,  mach_max = 1.6, range_max = 120000, fuel_mass = 160.0, impulse = 255, burn_time = 22.0,  warhead_mass = 315.0, picture = "agm65d.png" },
    { id = "NG_LMUR_305",      clsid = "{NEXTGEN_LMUR_305}",      role = "ag",     shape = "ng_kh38_grom",       caliber = 0.200, length = 1.95, display_name = "LMUR / Izdeliye 305 EO-ASM (NextGen)",short_name = "LMUR-305", mass = 105.0,  mach_max = 1.1, range_max = 18000,  fuel_mass = 28.0,  impulse = 245, burn_time = 35.0,  warhead_mass = 25.0,  picture = "agm65d.png" },
    { id = "NG_DELILAH",       clsid = "{NEXTGEN_DELILAH}",       role = "cruise", shape = "ng_kalibr_3m54",     caliber = 0.330, length = 2.71, display_name = "IMI Delilah Stand-Off Loiter (NG)",   short_name = "Delilah",  mass = 187.0,  mach_max = 0.85,range_max = 250000, fuel_mass = 62.0,  impulse = 2800,burn_time = 700.0, warhead_mass = 30.0,  picture = "agm84d.png", life_time = 1400 },

    -- 3. Folding Glide Bombs (UMPK / UMPB-PAB / SPICE / GLSDB / JDAM-ER / SDB) & Retarded Bombs (21)
    { id = "NG_UMPB_D30SN",    clsid = "{NEXTGEN_UMPB_D30SN}",    role = "glide",  shape = "ng_umpb_d30",        caliber = 0.300, length = 2.85, display_name = "UMPB D-30SN Glide (PAB / NextGen)",   short_name = "UMPB-D30", mass = 250.0,  mach_max = 0.95,range_max = 110000, fuel_mass = 15.0,  impulse = 2200,burn_time = 300.0, warhead_mass = 100.0, picture = "fab500.png" },
    { id = "NG_UMPB_5R",       clsid = "{NEXTGEN_UMPB_5R}",       role = "glide",  shape = "ng_umpb_d30",        caliber = 0.340, length = 3.20, display_name = "UMPB-5R Powered Long-Glide (NextGen)",short_name = "UMPB-5R",  mass = 380.0,  mach_max = 0.95,range_max = 160000, fuel_mass = 35.0,  impulse = 2500,burn_time = 450.0, warhead_mass = 160.0, picture = "fab500.png" },
    { id = "NG_PBK_500U_DREL", clsid = "{NEXTGEN_PBK_500U_DREL}", role = "glide",  shape = "ng_umpb_d30",        caliber = 0.360, length = 3.10, display_name = "PBK-500U Drel Cluster Glide (NG)",    short_name = "PBK-500U", mass = 540.0,  mach_max = 0.92,range_max = 55000,  fuel_mass = 4.0,   impulse = 1800,burn_time = 240.0, warhead_mass = 320.0, picture = "fab500.png" },
    { id = "NG_FAB_250_UMPK",  clsid = "{NEXTGEN_FAB_250_UMPK}",  role = "glide",  shape = "ng_heavy_umpk",      caliber = 0.325, length = 2.15, display_name = "FAB-250 M-62 UMPK Glide (NextGen)",   short_name = "FAB250G",  mass = 275.0,  mach_max = 0.95,range_max = 60000,  fuel_mass = 3.0,   impulse = 1800,burn_time = 240.0, warhead_mass = 100.0, picture = "fab500.png" },
    { id = "NG_FAB_500_UMPK",  clsid = "{NEXTGEN_FAB_500_UMPK}",  role = "glide",  shape = "ng_heavy_umpk",      caliber = 0.400, length = 2.47, display_name = "FAB-500 M-62 UMPK Glide (NextGen)",   short_name = "FAB500G",  mass = 520.0,  mach_max = 0.95,range_max = 65000,  fuel_mass = 4.0,   impulse = 1800,burn_time = 260.0, warhead_mass = 230.0, picture = "fab500.png" },
    { id = "NG_FAB_1500_UMPK", clsid = "{NEXTGEN_FAB_1500_UMPK}", role = "glide",  shape = "ng_heavy_umpk",      caliber = 0.630, length = 2.80, display_name = "FAB-1500 M-54 UMPK Glide (NextGen)",  short_name = "FAB1500G", mass = 1550.0, mach_max = 0.95,range_max = 75000,  fuel_mass = 5.0,   impulse = 1800,burn_time = 300.0, warhead_mass = 675.0, picture = "fab500.png" },
    { id = "NG_FAB_3000_UMPK", clsid = "{NEXTGEN_FAB_3000_UMPK}", role = "glide",  shape = "ng_heavy_umpk",      caliber = 0.820, length = 3.30, display_name = "FAB-3000 M-54 UMPK Heavy (NextGen)",  short_name = "FAB3000G", mass = 3050.0, mach_max = 0.92,range_max = 60000,  fuel_mass = 6.0,   impulse = 1800,burn_time = 280.0, warhead_mass = 1400.0,picture = "fab500.png" },
    { id = "NG_SPICE_250",     clsid = "{NEXTGEN_SPICE_250}",     role = "glide",  shape = "ng_spice_glide",     caliber = 0.180, length = 2.05, display_name = "Rafael SPICE-250 Stand-Off (NextGen)",short_name = "SPICE250", mass = 113.0,  mach_max = 0.95,range_max = 100000, fuel_mass = 3.0,   impulse = 1800,burn_time = 260.0, warhead_mass = 75.0,  picture = "gbu38.png" },
    { id = "NG_SPICE_1000",    clsid = "{NEXTGEN_SPICE_1000}",    role = "glide",  shape = "ng_spice_glide",     caliber = 0.360, length = 3.60, display_name = "Rafael SPICE-1000 Winged (NextGen)",  short_name = "SPICE1K",  mass = 520.0,  mach_max = 0.95,range_max = 125000, fuel_mass = 4.0,   impulse = 1800,burn_time = 320.0, warhead_mass = 240.0, picture = "gbu38.png" },
    { id = "NG_SPICE_2000",    clsid = "{NEXTGEN_SPICE_2000}",    role = "glide",  shape = "ng_spice_glide",     caliber = 0.460, length = 4.20, display_name = "Rafael SPICE-2000 EO/GPS (NextGen)",  short_name = "SPICE2K",  mass = 990.0,  mach_max = 0.95,range_max = 75000,  fuel_mass = 4.0,   impulse = 1800,burn_time = 280.0, warhead_mass = 450.0, picture = "gbu31.png" },
    { id = "NG_GBU_38_ER",     clsid = "{NEXTGEN_GBU_38_ER}",     role = "glide",  shape = "ng_umpb_d30",        caliber = 0.273, length = 2.38, display_name = "GBU-38/B JDAM-ER 500lb Wing (NG)",     short_name = "GBU38-ER", mass = 270.0,  mach_max = 0.95,range_max = 75000,  fuel_mass = 3.0,   impulse = 1800,burn_time = 280.0, warhead_mass = 90.0,  picture = "gbu38.png" },
    { id = "NG_GBU_62_QS_ER",  clsid = "{NEXTGEN_GBU_62_QS_ER}",  role = "glide",  shape = "ng_umpb_d30",        caliber = 0.457, length = 3.88, display_name = "GBU-62(V)1/B QuickStrike-ER (NG)",    short_name = "GBU62-ER", mass = 950.0,  mach_max = 0.95,range_max = 80000,  fuel_mass = 4.0,   impulse = 1800,burn_time = 300.0, warhead_mass = 440.0, picture = "gbu31.png" },
    { id = "NG_GBU_64_JDAM_ER",clsid = "{NEXTGEN_GBU_64_JDAMER}", role = "glide",  shape = "ng_umpb_d30",        caliber = 0.457, length = 3.88, display_name = "GBU-64/B JDAM-ER Winged (NextGen)",   short_name = "JDAM-ER",  mass = 950.0,  mach_max = 0.95,range_max = 75000,  fuel_mass = 4.0,   impulse = 1800,burn_time = 300.0, warhead_mass = 430.0, picture = "gbu31.png" },
    { id = "NG_BLU_109_NG",    clsid = "{NEXTGEN_BLU_109_NG}",    role = "glide",  shape = "ng_heavy_umpk",      caliber = 0.370, length = 3.80, display_name = "GBU-31(V)3 Penetrator Wing (NG)",   short_name = "BLU-109N", mass = 950.0,  mach_max = 0.95,range_max = 55000,  fuel_mass = 4.0,   impulse = 1800,burn_time = 240.0, warhead_mass = 420.0, picture = "gbu31.png" },
    { id = "NG_GBU_39_B",      clsid = "{NEXTGEN_GBU_39_B}",      role = "glide",  shape = "ng_glide_sdb",       caliber = 0.190, length = 1.80, display_name = "GBU-39B/B Laser SDB (NextGen)",      short_name = "GBU-39B",  mass = 130.0,  mach_max = 0.95,range_max = 110000, fuel_mass = 2.0,   impulse = 1800,burn_time = 320.0, warhead_mass = 93.0,  picture = "gbu38.png" },
    { id = "NG_GLSDB",         clsid = "{NEXTGEN_GLSDB}",         role = "glide",  shape = "ng_glide_sdb",       caliber = 0.227, length = 3.90, display_name = "GLSDB Boosted Precision SDB (NG)",    short_name = "GLSDB",    mass = 270.0,  mach_max = 1.6, range_max = 150000, fuel_mass = 65.0,  impulse = 2600,burn_time = 450.0, warhead_mass = 93.0,  picture = "gbu38.png" },
    { id = "NG_SWITCHBLADE_3", clsid = "{NEXTGEN_SWITCHBLADE_3}", role = "loiter", shape = "ng_loitering_x",     caliber = 0.080, length = 0.65, display_name = "Switchblade 300 Air-Tube (NextGen)",  short_name = "SB-300",   mass = 2.5,    mach_max = 0.22,range_max = 15000,  fuel_mass = 0.5,   impulse = 1800,burn_time = 300.0, warhead_mass = 1.0,   picture = "gbu38.png" },
    { id = "NG_DURANDAL_NG",   clsid = "{NEXTGEN_DURANDAL_NG}",   role = "ag",     shape = "ng_durandal_runway", caliber = 0.223, length = 2.50, display_name = "BLU-107/B Durandal NG (NextGen)",     short_name = "Durandal", mass = 219.0,  mach_max = 1.3, range_max = 18000,  fuel_mass = 22.0,  impulse = 230, burn_time = 3.5,   warhead_mass = 100.0, picture = "mk82.png" },
    { id = "NG_ODAB_500_NG",   clsid = "{NEXTGEN_ODAB_500_NG}",   role = "ag",     shape = "ng_durandal_runway", caliber = 0.500, length = 2.38, display_name = "ODAB-500PMV Thermobaric (NextGen)",   short_name = "ODAB-500", mass = 525.0,  mach_max = 1.0, range_max = 35000,  fuel_mass = 1.0,   impulse = 40,  burn_time = 1.0,   warhead_mass = 380.0, picture = "fab500.png" },
    { id = "NG_CBU_105_NG",    clsid = "{NEXTGEN_CBU_105_NG}",    role = "ag",     shape = "ng_durandal_runway", caliber = 0.400, length = 2.34, display_name = "CBU-105 WCMD SFW NG (NextGen)",      short_name = "CBU-105N", mass = 430.0,  mach_max = 1.0, range_max = 38000,  fuel_mass = 1.0,   impulse = 40,  burn_time = 1.0,   warhead_mass = 220.0, picture = "cbu97.png" },

    -- 4. Heavy Supersonic Anti-Ship & Folding Cruise (8)
    { id = "NG_BRAHMOS_A",     clsid = "{NEXTGEN_BRAHMOS_A}",     role = "ag",     shape = "ng_brahmos_intake",  caliber = 0.670, length = 8.20, display_name = "BrahMos-A Supersonic (NextGen)",      short_name = "BrahMos",  mass = 2500.0, mach_max = 3.0, range_max = 450000, fuel_mass = 850.0, impulse = 320, burn_time = 140.0, warhead_mass = 300.0, picture = "agm84d.png", life_time = 900, polar = "FM_AAM_ULTRA" },
    { id = "NG_BRAHMOS_NG",    clsid = "{NEXTGEN_BRAHMOS_NG}",    role = "ag",     shape = "ng_brahmos_intake",  caliber = 0.500, length = 6.00, display_name = "BrahMos-NG Light Mach 3.5 (NextGen)",short_name = "BrahmsNG", mass = 1260.0, mach_max = 3.5, range_max = 300000, fuel_mass = 460.0, impulse = 320, burn_time = 95.0,  warhead_mass = 220.0, picture = "agm84d.png", life_time = 800, polar = "FM_AAM_ULTRA" },
    { id = "NG_ONIKS_A",       clsid = "{NEXTGEN_ONIKS_A}",       role = "ag",     shape = "ng_brahmos_intake",  caliber = 0.670, length = 8.00, display_name = "P-800 Oniks Air-Launched (NextGen)",  short_name = "Oniks-A",  mass = 2500.0, mach_max = 2.8, range_max = 400000, fuel_mass = 820.0, impulse = 310, burn_time = 130.0, warhead_mass = 300.0, picture = "agm84d.png", life_time = 900, polar = "FM_AAM_ULTRA" },
    { id = "NG_ASM_3",         clsid = "{NEXTGEN_ASM_3}",         role = "ag",     shape = "ng_kh31_ramjet",     caliber = 0.350, length = 6.00, display_name = "Mitsubishi ASM-3 Ramjet (NextGen)",   short_name = "ASM-3",    mass = 900.0,  mach_max = 3.2, range_max = 220000, fuel_mass = 300.0, impulse = 300, burn_time = 80.0,  warhead_mass = 200.0, picture = "agm84d.png", life_time = 600, polar = "FM_AAM_ULTRA" },
    { id = "NG_YJ_12",         clsid = "{NEXTGEN_YJ_12}",         role = "ag",     shape = "ng_kh31_ramjet",     caliber = 0.700, length = 6.30, display_name = "YJ-12 Supersonic ASM (NextGen)",      short_name = "YJ-12",    mass = 2000.0, mach_max = 3.5, range_max = 400000, fuel_mass = 680.0, impulse = 310, burn_time = 110.0, warhead_mass = 300.0, picture = "agm84d.png", life_time = 800, polar = "FM_AAM_ULTRA" },
    { id = "NG_KH_59MK2",      clsid = "{NEXTGEN_KH_59MK2}",      role = "cruise", shape = "ng_jassm_taurus",    caliber = 0.400, length = 4.20, display_name = "Kh-59MK2 Stealth Cruise (NextGen)",   short_name = "Kh59MK2",  mass = 770.0,  mach_max = 0.95,range_max = 290000, fuel_mass = 200.0, impulse = 2800,burn_time = 600.0, warhead_mass = 320.0, picture = "agm154.png", life_time = 1200 },
    { id = "NG_SOM_B2",        clsid = "{NEXTGEN_SOM_B2}",        role = "cruise", shape = "ng_jassm_taurus",    caliber = 0.420, length = 5.00, display_name = "TUBITAK SOM-B2 Deep-Pen Cruise (NG)", short_name = "SOM-B2",   mass = 620.0,  mach_max = 0.92,range_max = 250000, fuel_mass = 165.0, impulse = 2850,burn_time = 580.0, warhead_mass = 230.0, picture = "agm154.png", life_time = 1200 },
    { id = "NG_RBS_15_MK4",    clsid = "{NEXTGEN_RBS_15_MK4}",    role = "cruise", shape = "ng_nsm_jsm",         caliber = 0.500, length = 4.35, display_name = "RBS-15F Mk4 Gungnir (NextGen)",       short_name = "RBS15-4",  mass = 650.0,  mach_max = 0.95,range_max = 300000, fuel_mass = 180.0, impulse = 2800,burn_time = 650.0, warhead_mass = 200.0, picture = "agm84d.png", life_time = 1200 },

    -- 5. Special Air-to-Air Interceptors (6)
    { id = "NG_AIM_54E",       clsid = "{NEXTGEN_AIM_54E}",       role = "aam", shape = "ng_aim54e",       caliber = 0.380, length = 3.96, display_name = "AIM-54E Sea Phoenix (NextGen)",       short_name = "AIM-54E", mass = 460.0, mach_max = 5.0, range_max = 220000, fuel_mass = 180.0, impulse = 255, burn_time = 24.0, warhead_mass = 60.0,  picture = "aim54.png",   life_time = 220, polar = "FM_AAM_ULTRA" },
    { id = "NG_ASRAAM_BLK6",   clsid = "{NEXTGEN_ASRAAM_BLK6}",   role = "aam", shape = "ng_asraam_sleek", caliber = 0.166, length = 2.90, display_name = "MBDA ASRAAM Block 6 (NextGen)",       short_name = "ASRAAM6", mass = 88.0,  mach_max = 3.8, range_max = 50000,  fuel_mass = 32.0,  impulse = 250, burn_time = 5.5,  warhead_mass = 10.0,  picture = "aim9x.png",   head_type = 1, life_time = 85 },
    { id = "NG_R_74M2",        clsid = "{NEXTGEN_R_74M2}",        role = "aam", shape = "ng_r74m2",        caliber = 0.170, length = 2.90, display_name = "R-74M2 (K-74M2) WVR (NextGen)",       short_name = "R-74M2",  mass = 105.0, mach_max = 3.2, range_max = 40000,  fuel_mass = 35.0,  impulse = 242, burn_time = 5.5,  warhead_mass = 8.0,   picture = "r73.png",     head_type = 1, life_time = 75 },
    { id = "NG_PL_10E",        clsid = "{NEXTGEN_PL_10E}",        role = "aam", shape = "ng_python5",      caliber = 0.160, length = 3.00, display_name = "PL-10E HOBS WVR (NextGen)",           short_name = "PL-10E",  mass = 105.0, mach_max = 4.0, range_max = 35000,  fuel_mass = 34.0,  impulse = 245, burn_time = 5.2,  warhead_mass = 10.0,  picture = "aim9x.png",   head_type = 1, life_time = 75 },
    { id = "NG_MAGIC_3",       clsid = "{NEXTGEN_MAGIC_3}",       role = "aam", shape = "ng_asraam_sleek", caliber = 0.157, length = 2.85, display_name = "Matra Magic III NG (NextGen)",        short_name = "Magic-3", mass = 92.0,  mach_max = 3.5, range_max = 38000,  fuel_mass = 32.0,  impulse = 245, burn_time = 5.0,  warhead_mass = 12.5,  picture = "magic.png",   head_type = 1, life_time = 75 },
    { id = "NG_SKY_SWORD_2C",  clsid = "{NEXTGEN_SKY_SWORD_2C}",  role = "aam", shape = "ng_aim120cd",     caliber = 0.190, length = 3.60, display_name = "TC-2C Sky Sword II BVR (NextGen)",    short_name = "TC-2C",   mass = 184.0, mach_max = 4.8, range_max = 110000, fuel_mass = 62.0,  impulse = 250, burn_time = 8.5,  warhead_mass = 22.0,  picture = "aim120c.png", life_time = 150 },

    -- 6. v5 Backlog ATGM, Light Naval, Dual-Mode Maverick & Micro Smart Glide (+16)
    { id = "NG_KORNET_EM",     clsid = "{NEXTGEN_KORNET_EM}",     role = "ag",     shape = "ng_atgm_quad",    caliber = 0.152, length = 1.20, display_name = "9M133 Kornet-EM 10km Tandem (NG)",   short_name = "KornetEM",mass = 33.0,  mach_max = 1.1, range_max = 10000,  fuel_mass = 8.0,   impulse = 225, burn_time = 14.0, warhead_mass = 7.0,  picture = "vikhr.png" },
    { id = "NG_PARS_3_LR",     clsid = "{NEXTGEN_PARS_3_LR}",     role = "ag",     shape = "ng_atgm_quad",    caliber = 0.159, length = 1.60, display_name = "MBDA PARS 3 LR Fire-Forget (NG)",     short_name = "PARS3-LR",mass = 49.0,  mach_max = 1.2, range_max = 8000,   fuel_mass = 11.0,  impulse = 230, burn_time = 10.0, warhead_mass = 9.0,  picture = "agm114.png" },
    { id = "NG_HJ_10",         clsid = "{NEXTGEN_HJ_10}",         role = "ag",     shape = "ng_atgm_quad",    caliber = 0.170, length = 1.85, display_name = "Norinco HJ-10 Heavy NLOS ATGM",       short_name = "HJ-10",   mass = 105.0, mach_max = 1.0, range_max = 15000,  fuel_mass = 28.0,  impulse = 235, burn_time = 24.0, warhead_mass = 18.0, picture = "agm114.png" },
    { id = "NG_HJ_12",         clsid = "{NEXTGEN_HJ_12}",         role = "ag",     shape = "ng_javelin_top",  caliber = 0.135, length = 1.25, display_name = "Norinco HJ-12 Top-Attack Pod (NG)",   short_name = "HJ-12",   mass = 17.0,  mach_max = 1.1, range_max = 5000,   fuel_mass = 3.8,   impulse = 220, burn_time = 8.0,  warhead_mass = 7.5,  picture = "agm114.png" },
    { id = "NG_UMTAS_L",       clsid = "{NEXTGEN_UMTAS_L}",       role = "ag",     shape = "ng_atgm_quad",    caliber = 0.160, length = 1.75, display_name = "Roketsan L-UMTAS Laser ATGM (NG)",    short_name = "L-UMTAS", mass = 37.5,  mach_max = 1.2, range_max = 16000,  fuel_mass = 10.0,  impulse = 235, burn_time = 16.0, warhead_mass = 8.0,  picture = "agm114.png" },
    { id = "NG_OMTAS",         clsid = "{NEXTGEN_OMTAS}",         role = "ag",     shape = "ng_javelin_top",  caliber = 0.160, length = 1.80, display_name = "Roketsan OMTAS IIR Pod-ATGM (NG)",    short_name = "OMTAS",   mass = 35.0,  mach_max = 1.1, range_max = 6000,   fuel_mass = 8.0,   impulse = 225, burn_time = 10.0, warhead_mass = 8.0,  picture = "agm114.png" },
    { id = "NG_STUGNA_P_AIR",  clsid = "{NEXTGEN_STUGNA_P}",      role = "ag",     shape = "ng_javelin_top",  caliber = 0.130, length = 1.36, display_name = "Stugna-P / Skif Air Laser ATGM",      short_name = "StugnaP", mass = 16.0,  mach_max = 1.1, range_max = 6000,   fuel_mass = 4.0,   impulse = 225, burn_time = 11.0, warhead_mass = 6.5,  picture = "vikhr.png" },
    { id = "NG_AGM_65E2",      clsid = "{NEXTGEN_AGM_65E2}",      role = "ag",     shape = "ng_kh38_grom",    caliber = 0.305, length = 2.49, display_name = "AGM-65E2/L Laser Maverick (NG)",      short_name = "AGM65E2", mass = 293.0, mach_max = 1.4, range_max = 28000,  fuel_mass = 75.0,  impulse = 238, burn_time = 7.0,  warhead_mass = 136.0,picture = "agm65d.png" },
    { id = "NG_SEA_VENOM",     clsid = "{NEXTGEN_SEA_VENOM}",     role = "cruise", shape = "ng_exocet_am39",  caliber = 0.200, length = 2.50, display_name = "MBDA Sea Venom / ANL Anti-Ship",      short_name = "SeaVenom",mass = 120.0, mach_max = 0.90,range_max = 45000,  fuel_mass = 28.0,  impulse = 2600,burn_time = 180.0,warhead_mass = 30.0, picture = "agm84d.png", life_time = 500 },
    { id = "NG_MARTE_ER",      clsid = "{NEXTGEN_MARTE_ER}",      role = "cruise", shape = "ng_kh35u",        caliber = 0.316, length = 3.60, display_name = "MBDA Marte ER 100km Turbojet (NG)",   short_name = "Marte-ER",mass = 340.0, mach_max = 0.92,range_max = 110000, fuel_mass = 90.0,  impulse = 2800,burn_time = 450.0,warhead_mass = 75.0, picture = "agm84d.png", life_time = 900 },
    { id = "NG_TESEO_MK2E",    clsid = "{NEXTGEN_TESEO_MK2E}",    role = "cruise", shape = "ng_tomahawk_v",   caliber = 0.460, length = 5.05, display_name = "MBDA Teseo Mk2/E Otomat AShM (NG)",    short_name = "Teseo2E", mass = 700.0, mach_max = 0.95,range_max = 350000, fuel_mass = 200.0, impulse = 3000,burn_time = 1100.0,warhead_mass = 180.0,picture = "agm84d.png", life_time = 1600 },
    { id = "NG_PENGUIN_MK3",   clsid = "{NEXTGEN_PENGUIN_MK3}",   role = "cruise", shape = "ng_nsm_jsm",      caliber = 0.280, length = 3.18, display_name = "Kongsberg Penguin Mk 3 IIR AShM",     short_name = "Penguin3",mass = 370.0, mach_max = 0.90,range_max = 55000,  fuel_mass = 85.0,  impulse = 250, burn_time = 24.0, warhead_mass = 120.0,picture = "agm84d.png", life_time = 600 },
    { id = "NG_BLUE_SPEAR",    clsid = "{NEXTGEN_BLUE_SPEAR}",    role = "cruise", shape = "ng_nsm_jsm",      caliber = 0.380, length = 5.00, display_name = "Blue Spear 5G Sea-Skimmer (NG)",      short_name = "BlueSpr", mass = 950.0, mach_max = 0.94,range_max = 290000, fuel_mass = 260.0, impulse = 2900,burn_time = 950.0,warhead_mass = 200.0,picture = "agm84d.png", life_time = 1500 },
    { id = "NG_MAM_L",         clsid = "{NEXTGEN_MAM_L}",         role = "glide",  shape = "ng_glide_sdb",    caliber = 0.160, length = 1.00, display_name = "Roketsan MAM-L Smart Glide (NG)",     short_name = "MAM-L",   mass = 22.0,  mach_max = 0.85,range_max = 18000,  fuel_mass = 1.0,   impulse = 1600,burn_time = 180.0,warhead_mass = 10.0, picture = "gbu38.png" },
    { id = "NG_MAM_T",         clsid = "{NEXTGEN_MAM_T}",         role = "glide",  shape = "ng_glide_sdb",    caliber = 0.230, length = 1.40, display_name = "Roketsan MAM-T 95kg Smart Glide",     short_name = "MAM-T",   mass = 94.0,  mach_max = 0.90,range_max = 45000,  fuel_mass = 2.0,   impulse = 1800,burn_time = 240.0,warhead_mass = 45.0, picture = "gbu38.png" },
    { id = "NG_TOLUN_SDB",     clsid = "{NEXTGEN_TOLUN_SDB}",     role = "glide",  shape = "ng_glide_sdb",    caliber = 0.170, length = 1.80, display_name = "ASELSAN Tolun GPS/IIR SDB (NG)",      short_name = "Tolun",   mass = 139.0, mach_max = 0.95,range_max = 102000, fuel_mass = 2.5,   impulse = 1800,burn_time = 300.0,warhead_mass = 95.0, picture = "gbu38.png" },
}

local tac_clsids = {
    ag_all     = {},
    nato_wvr   = {},
    nato_bvr   = {},
    french_all = {},
    east_bvr   = {},
}

for _, spec in ipairs(tac_specs) do
    local clsid = register_tac(spec)
    if spec.role == "aam" then
        if spec.id == "NG_R_74M2" or spec.id == "NG_PL_10E" then
            table.insert(tac_clsids.east_bvr, clsid)
        elseif spec.id == "NG_MAGIC_3" then
            table.insert(tac_clsids.french_all, clsid)
        elseif spec.id == "NG_AIM_54E" or spec.id == "NG_SKY_SWORD_2C" then
            table.insert(tac_clsids.nato_bvr, clsid)
        else
            table.insert(tac_clsids.nato_wvr, clsid)
        end
    else
        table.insert(tac_clsids.ag_all, clsid)
    end
end

-- Multi-Ejector Racks (3x UMPB D-30SN, 4x SPICE-250, 4x FGM-148F Javelin)
declare_loadout({
    category = CAT_MISSILES,
    CLSID = "{NEXTGEN_UMPB_D30_3X}",
    Picture = "fab500.png",
    displayName = _("3x UMPB D-30SN Glide Rack (PAB / NextGen)"),
    Weight = 790.0,
    Cx_pil = 0.0036,
    Count = 3,
    attribute = tac_attrs["NG_UMPB_D30SN"],
    Elements = {
        { ShapeName = "ng_umpb_d30", Position = { 0, -0.14,  0.00 } },
        { ShapeName = "ng_umpb_d30", Position = { 0, -0.34, -0.22 } },
        { ShapeName = "ng_umpb_d30", Position = { 0, -0.34,  0.22 } },
    },
})
table.insert(tac_clsids.ag_all, "{NEXTGEN_UMPB_D30_3X}")

declare_loadout({
    category = CAT_MISSILES,
    CLSID = "{NEXTGEN_SPICE_250_4X}",
    Picture = "gbu38.png",
    displayName = _("4x Rafael SPICE-250 Smart Rack (NextGen)"),
    Weight = 510.0,
    Cx_pil = 0.0034,
    Count = 4,
    attribute = tac_attrs["NG_SPICE_250"],
    Elements = {
        { ShapeName = "ng_spice_glide", Position = { 0, -0.14, -0.16 } },
        { ShapeName = "ng_spice_glide", Position = { 0, -0.14,  0.16 } },
        { ShapeName = "ng_spice_glide", Position = { 0, -0.34, -0.16 } },
        { ShapeName = "ng_spice_glide", Position = { 0, -0.34,  0.16 } },
    },
})
table.insert(tac_clsids.ag_all, "{NEXTGEN_SPICE_250_4X}")

declare_loadout({
    category = CAT_MISSILES,
    CLSID = "{NEXTGEN_JAVELIN_4X}",
    Picture = "agm114.png",
    displayName = _("4x FGM-148F Javelin Air Quad-Pod (NextGen)"),
    Weight = 85.0,
    Cx_pil = 0.0024,
    Count = 4,
    attribute = tac_attrs["NG_FGM_148F_JAV"],
    Elements = {
        { ShapeName = "ng_javelin_top", Position = { 0, -0.12, -0.14 } },
        { ShapeName = "ng_javelin_top", Position = { 0, -0.12,  0.14 } },
        { ShapeName = "ng_javelin_top", Position = { 0, -0.30, -0.14 } },
        { ShapeName = "ng_javelin_top", Position = { 0, -0.30,  0.14 } },
    },
})
table.insert(tac_clsids.ag_all, "{NEXTGEN_JAVELIN_4X}")

declare_loadout({
    category = CAT_MISSILES,
    CLSID = "{NEXTGEN_TOLUN_4X}",
    Picture = "gbu38.png",
    displayName = _("4x ASELSAN Tolun Smart SDB Rack (NextGen)"),
    Weight = 580.0,
    Cx_pil = 0.0034,
    Count = 4,
    attribute = tac_attrs["NG_TOLUN_SDB"],
    Elements = {
        { ShapeName = "ng_glide_sdb", Position = { 0, -0.14, -0.16 } },
        { ShapeName = "ng_glide_sdb", Position = { 0, -0.14,  0.16 } },
        { ShapeName = "ng_glide_sdb", Position = { 0, -0.34, -0.16 } },
        { ShapeName = "ng_glide_sdb", Position = { 0, -0.34,  0.16 } },
    },
})
table.insert(tac_clsids.ag_all, "{NEXTGEN_TOLUN_4X}")

return tac_clsids
