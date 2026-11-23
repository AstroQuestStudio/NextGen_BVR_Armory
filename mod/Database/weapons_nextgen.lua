-- NextGen BVR & WVR Air-to-Air Weapon Definitions (DCS World 2.9+ Modular API)
-- Uses physically calibrated Mach-indexed polars (polar_profiles.lua) + dual-stage boost/march propulsion.

local polar = dofile(current_mod_path .. "/Database/polar_profiles.lua")

local function deep_copy(orig)
    if type(orig) ~= "table" then return orig end
    local copy = {}
    for k, v in pairs(orig) do
        copy[deep_copy(k)] = deep_copy(v)
    end
    return copy
end

-- Authentic AIM-120C / aa_missile_amraam2.sch template
local BASE_BVR_TEMPLATE = {
    category = CAT_AIR_TO_AIR,
    caliber = 0.178,
    mass = 161.5,
    model = "ng_aim120cd",
    sounderName = "Weapons/Missile",
    targeting_data = { fm_type = -1 },
    type_name = "missile",
    wsTypeOfWeapon = { wsType_Weapon, wsType_Missile, wsType_AA_Missile, WSTYPE_PLACEHOLDER },

    Escort = 1,
    Head_Type = 2,
    sigma = { 4, 4, 4 },
    M = 161.5,
    H_max = 26000,
    H_min = 1,
    H_min_t = 1,
    Diam = 178,
    Cx_pil = 2.2,
    D_max = 105000,
    D_min = 700,
    Head_Form = 1,
    Life_Time = 140,
    Nr_max = 40,
    v_min = 140,
    v_mid = 780,
    Mach_max = 4.2,
    t_b = 0.1,
    t_acc = 3.0,
    t_marsh = 6.5,
    Range_max = 120000,
    Fi_start = 0.88,
    Fi_rak = 3.14152,
    Fi_excort = 1.05,
    Fi_search = 1.05,
    OmViz_max = 0.52,
    PN_gain = 4.5,
    Reflection = 0.02,
    SeekerGen = 4,
    KillDistance = 15,
    X_back = -1.8,
    Y_back = 0,
    Z_back = 0,
    ccm_k0 = 0.06,
    hoj = 1,
    loft = 1,
    loft_factor = 4.5,
    supersonic_A_coef_skew = 0.12,
    nozzle_exit_area = 0.0132,
    scheme = "schemes/missiles/aa_missile_amraam2.sch",
    class_name = "wAmmunitionSelfHoming",

    controller = { boost_start = 0, march_start = 0.4 },
    exhaust = { 0.8, 0.8, 0.8, 0.04 },

    boost = {
        custom_smoke_dissipation_factor = 0.2,
        fuel_mass = 24.0,
        impulse = 245,
        nozzle_exit_area = 0.0132,
        nozzle_orientationXYZ = { { 0, 0, 0 } },
        nozzle_position = { { -1.8, 0, 0 } },
        smoke_color = { 0.85, 0.85, 0.85 },
        smoke_transparency = 0.06,
        tail_width = 0.35,
        work_time = 2.8,
    },

    march = {
        custom_smoke_dissipation_factor = 0.2,
        fuel_mass = 36.0,
        impulse = 248,
        nozzle_exit_area = 0.0132,
        nozzle_orientationXYZ = { { 0, 0, 0 } },
        nozzle_position = { { -1.8, 0, 0 } },
        smoke_color = { 0.85, 0.85, 0.85 },
        smoke_opacity_type = 1,
        smoke_transparency = 0.02,
        tail_width = 0.22,
        work_time = 7.5,
    },

    active_radar_lock_dist = 22000,
    go_to_active_by_default = 1,

    actuator = {
        D = 250, T1 = 0.002, T2 = 0.006, Tf = 0.005,
        fin_stall = 1, max_delta = 0.35, max_omega = 7.5, sim_count = 4,
    },

    autopilot = {
        Ka = 16, Kd = 180, Knav = 4, Krx = 2, Kx = 0.1, T1 = 309, Tc = 0.06, Tf = 0.1,
        accel_coeffs = { 0, 11.5, -1.2, -0.25, 24, 0.00016926 },
        cmd_delay = 0.8, dV0 = 393, delay = 0.2,
        fins_limit = 0.34, fins_limit_x = 0.087, gload_limit = 40,
        loft_active = 1, loft_factor = 4.5, loft_off_range = 15000, loft_sin = 0.50,
        null_roll = 0.785398, op_time = 140,
    },

    fm = deep_copy(polar.FM_AAM_BVR),

    seeker = {
        FOV = 1.57, abs_err_val = 1.5, aim_sigma = 2.0, aim_y_offset = 0.0,
        ang_err_val = 0.0001, blind_rad_val = 1, calc_aim_dist = 180000,
        delay = 0.5, err_correct_time = 1.5, guide_to_last_pos = true, keep_aim_time = 5,
        lock_manual_target_types_only = 0, max_w_LOS = 0.55, op_time = 140,
        pos_memory_time = 60, sens_far_dist = 80000, sens_near_dist = 120,
    },

    proximity_fuze = { arm_delay = 0.8, radius = 15 },
    warhead = {
        caliber = 178, concrete_factors = { 1, 1, 1 }, concrete_obj_factor = 0,
        cumulative_factor = 0, cumulative_thickness = 0, expl_mass = 20.0, fantom = 1,
        mass = 20.0, obj_factors = { 1, 1 }, other_factors = { 1, 1, 1 }, piercing_mass = 5.0,
    },
    warhead_air = {
        caliber = 178, concrete_factors = { 1, 1, 1 }, concrete_obj_factor = 0,
        cumulative_factor = 0, cumulative_thickness = 0, expl_mass = 20.0, fantom = 1,
        mass = 20.0, obj_factors = { 1, 1 }, other_factors = { 1, 1, 1 }, piercing_mass = 5.0,
    },
}

local FOLDING_AAM_SHAPES = {
    ng_pl15e    = true,
    ng_r77_grid = true,
    ng_r37m     = true,
}

local function register_missile(spec)
    local w = deep_copy(BASE_BVR_TEMPLATE)

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
    w.Life_Time = spec.life_time or 140
    w.Nr_max = spec.g_limit or 40
    w.autopilot.gload_limit = spec.g_limit or 40
    w.autopilot.op_time = w.Life_Time
    w.seeker.op_time = w.Life_Time
    w.active_radar_lock_dist = spec.pitbull_dist or 22000
    w.Head_Type = spec.head_type or 2
    w.ccm_k0 = spec.ccm or 0.06
    w.warhead.caliber = math.floor(spec.caliber * 1000)
    w.warhead.expl_mass = spec.warhead_mass
    w.warhead.mass = spec.warhead_mass
    w.warhead_air.caliber = math.floor(spec.caliber * 1000)
    w.warhead_air.expl_mass = spec.warhead_mass
    w.warhead_air.mass = spec.warhead_mass

    polar.apply_polar(w, spec.polar or "FM_AAM_BVR", spec.caliber, spec.mass, spec.length)

    -- Two-stage propulsion split (initial boost + sustained/dual-pulse/ramjet march)
    local back = -(spec.length * 0.5)
    w.X_back = back
    local boost_frac = spec.boost_frac or 0.38
    w.boost.fuel_mass = spec.fuel_mass * boost_frac
    w.boost.impulse = spec.boost_isp or 245
    w.boost.work_time = math.max(1.8, spec.burn_time * 0.30)
    w.boost.nozzle_position = { { back + 0.05, 0, 0 } }
    w.controller.march_start = w.boost.work_time

    w.march.fuel_mass = spec.fuel_mass * (1.0 - boost_frac)
    w.march.impulse = spec.impulse
    w.march.work_time = math.max(2.5, spec.burn_time * 0.70)
    w.march.nozzle_position = { { back + 0.05, 0, 0 } }
    w.t_acc = w.boost.work_time
    w.t_marsh = w.march.work_time

    if spec.head_type == 1 then
        w.autopilot.loft_active = 0
        w.loft = 0
        w.hoj = 0
        w.actuator.max_omega = 12.0
        w.seeker.sens_far_dist = 35000
        w.seeker.FOV = 2.4
    else
        local use_loft = spec.loft ~= nil and spec.loft or 1
        w.autopilot.loft_active = use_loft
        w.loft = use_loft
        w.seeker.sens_far_dist = spec.range_max * 0.75
    end

    if FOLDING_AAM_SHAPES[spec.shape] then
        w.encyclopediaAnimation = { args = { [25] = 1 } }
    end

    w.shape_table_data = {
        { name = spec.id, file = spec.shape, life = 1, fire = { 0, 1 }, username = spec.display_name, index = WSTYPE_PLACEHOLDER },
    }

    local registered = declare_weapon(w)
    declare_loadout({
        category = CAT_AIR_TO_AIR,
        CLSID = spec.clsid,
        Picture = spec.picture or "aim120c.png",
        displayName = _(spec.display_name),
        Weight = spec.mass,
        Cx_pil = 0.0019,
        attribute = registered.wsTypeOfWeapon,
        Elements = { { ShapeName = spec.shape } },
    })

    return spec.clsid
end

local specs = {
    -- US / NATO / Allied BVR
    { id = "NG_AIM_120A",    clsid = "{NEXTGEN_AIM_120A}",    faction = "nato_bvr",   polar = "FM_AAM_BVR",   shape = "ng_aim120a",       caliber = 0.178, length = 3.66, display_name = "AIM-120A AMRAAM (NextGen)",       short_name = "AIM-120A", mass = 152.0, mach_max = 4.0, range_max = 75000,  fuel_mass = 45.0,  impulse = 240, burn_time = 7.0,  warhead_mass = 22.0, ccm = 0.12, g_limit = 40, picture = "aim120c.png" },
    { id = "NG_AIM_120C5",   clsid = "{NEXTGEN_AIM_120C5}",   faction = "nato_bvr",   polar = "FM_AAM_BVR",   shape = "ng_aim120cd",      caliber = 0.178, length = 3.66, display_name = "AIM-120C-5 AMRAAM (NextGen)",     short_name = "AIM120C5", mass = 157.0, mach_max = 4.1, range_max = 105000, fuel_mass = 52.0,  impulse = 248, burn_time = 8.2,  warhead_mass = 20.0, ccm = 0.07, g_limit = 42, picture = "aim120c.png" },
    { id = "NG_AIM_120C7",   clsid = "{NEXTGEN_AIM_120C7}",   faction = "nato_bvr",   polar = "FM_AAM_BVR",   shape = "ng_aim120cd",      caliber = 0.178, length = 3.66, display_name = "AIM-120C-7 AMRAAM (NextGen)",     short_name = "AIM120C7", mass = 161.5, mach_max = 4.2, range_max = 120000, fuel_mass = 56.0,  impulse = 250, burn_time = 9.0,  warhead_mass = 20.0, ccm = 0.05, g_limit = 42, picture = "aim120c.png" },
    { id = "NG_AIM_120C8",   clsid = "{NEXTGEN_AIM_120C8}",   faction = "nato_bvr",   polar = "FM_AAM_BVR",   shape = "ng_aim120cd",      caliber = 0.178, length = 3.66, display_name = "AIM-120C-8 / D Export (NextGen)", short_name = "AIM120C8", mass = 161.5, mach_max = 4.3, range_max = 150000, fuel_mass = 62.0,  impulse = 254, burn_time = 10.5, warhead_mass = 20.0, ccm = 0.03, g_limit = 44, picture = "aim120c.png", life_time = 175 },
    { id = "NG_AIM_120D3",   clsid = "{NEXTGEN_AIM_120D3}",   faction = "nato_bvr",   polar = "FM_AAM_BVR",   shape = "ng_aim120cd",      caliber = 0.178, length = 3.66, display_name = "AIM-120D-3 AMRAAM (NextGen)",     short_name = "AIM120D3", mass = 161.5, mach_max = 4.5, range_max = 180000, fuel_mass = 66.0,  impulse = 255, burn_time = 12.0, warhead_mass = 20.0, ccm = 0.02, g_limit = 45, picture = "aim120c.png", life_time = 200 },
    { id = "NG_AIM_260",     clsid = "{NEXTGEN_AIM_260}",     faction = "nato_bvr",   polar = "FM_AAM_ULTRA", shape = "ng_aim260",        caliber = 0.178, length = 3.66, display_name = "AIM-260A JATM (NextGen)",         short_name = "AIM-260A", mass = 168.0, mach_max = 5.2, range_max = 260000, fuel_mass = 82.0,  impulse = 265, burn_time = 15.0, warhead_mass = 22.0, ccm = 0.01, g_limit = 50, picture = "aim120c.png", life_time = 240 },
    { id = "NG_AIM_174B",    clsid = "{NEXTGEN_AIM_174B}",    faction = "nato_bvr",   polar = "FM_AAM_ULTRA", shape = "ng_aim174b",       caliber = 0.343, length = 5.03, display_name = "AIM-174B Gunslinger (NextGen)",   short_name = "AIM-174B", mass = 860.0, mach_max = 5.5, range_max = 380000, fuel_mass = 430.0, impulse = 270, burn_time = 22.0, warhead_mass = 60.0, ccm = 0.01, g_limit = 32, picture = "aim54.png",   life_time = 320 },
    { id = "NG_AIM_54C_PLUS",clsid = "{NEXTGEN_AIM_54C_PLUS}",faction = "nato_bvr",   polar = "FM_AAM_ULTRA", shape = "ng_aim54e",        caliber = 0.380, length = 3.96, display_name = "AIM-54C+ Sea Phoenix (NextGen)",  short_name = "AIM54C+",  mass = 465.0, mach_max = 4.6, range_max = 185000, fuel_mass = 170.0, impulse = 250, burn_time = 22.0, warhead_mass = 60.0, ccm = 0.05, g_limit = 22, picture = "aim54.png",   life_time = 200 },
    { id = "NG_AAM_4B",      clsid = "{NEXTGEN_AAM_4B}",      faction = "nato_bvr",   polar = "FM_AAM_BVR",   shape = "ng_aam4b",         caliber = 0.203, length = 3.67, display_name = "Mitsubishi AAM-4B AESA (NextGen)",short_name = "AAM-4B",   mass = 222.0, mach_max = 4.5, range_max = 120000, fuel_mass = 78.0,  impulse = 252, burn_time = 10.0, warhead_mass = 24.0, ccm = 0.03, g_limit = 42, picture = "aim120c.png", life_time = 160 },
    { id = "NG_I_DERBY_ER",  clsid = "{NEXTGEN_I_DERBY_ER}",  faction = "nato_bvr",   polar = "FM_AAM_BVR",   shape = "ng_pl12a",         caliber = 0.160, length = 3.62, display_name = "Rafael I-Derby ER (NextGen)",     short_name = "Derby-ER", mass = 118.0, mach_max = 4.2, range_max = 100000, fuel_mass = 46.0,  impulse = 250, burn_time = 9.0,  warhead_mass = 23.0, ccm = 0.04, g_limit = 45, picture = "aim120c.png", life_time = 150 },
    { id = "NG_METEOR",      clsid = "{NEXTGEN_METEOR}",      faction = "nato_bvr",   polar = "FM_AAM_ULTRA", shape = "ng_meteor",        caliber = 0.178, length = 3.65, display_name = "MBDA Meteor Ramjet (NextGen)",    short_name = "Meteor",   mass = 190.0, mach_max = 4.8, range_max = 220000, fuel_mass = 95.0,  impulse = 460, burn_time = 38.0, warhead_mass = 24.0, ccm = 0.01, g_limit = 45, picture = "aim120c.png", boost_frac = 0.24, life_time = 260 },
    { id = "NG_ASTRA_MK1",   clsid = "{NEXTGEN_ASTRA_MK1}",   faction = "nato_bvr",   polar = "FM_AAM_BVR",   shape = "ng_gokdogan_astra",caliber = 0.178, length = 3.60, display_name = "DRDO Astra Mk 1 BVR (NextGen)",   short_name = "Astra-1",  mass = 154.0, mach_max = 4.5, range_max = 110000, fuel_mass = 52.0,  impulse = 250, burn_time = 9.0,  warhead_mass = 15.0, ccm = 0.04, g_limit = 40, picture = "aim120c.png", life_time = 150 },
    { id = "NG_ASTRA_MK2",   clsid = "{NEXTGEN_ASTRA_MK2}",   faction = "nato_bvr",   polar = "FM_AAM_BVR",   shape = "ng_gokdogan_astra",caliber = 0.178, length = 3.80, display_name = "DRDO Astra Mk 2 Dual-Pulse (NG)", short_name = "Astra-2",  mass = 165.0, mach_max = 4.6, range_max = 160000, fuel_mass = 66.0,  impulse = 256, burn_time = 12.0, warhead_mass = 15.0, ccm = 0.03, g_limit = 42, picture = "aim120c.png", life_time = 185 },
    { id = "NG_ASTRA_MK3",   clsid = "{NEXTGEN_ASTRA_MK3}",   faction = "nato_bvr",   polar = "FM_AAM_ULTRA", shape = "ng_meteor",        caliber = 0.178, length = 3.84, display_name = "Astra Mk 3 / Gandiva SFDR (NG)",  short_name = "Astra-3",  mass = 185.0, mach_max = 5.0, range_max = 300000, fuel_mass = 92.0,  impulse = 440, burn_time = 34.0, warhead_mass = 18.0, ccm = 0.02, g_limit = 42, picture = "aim120c.png", boost_frac = 0.24, life_time = 270 },
    { id = "NG_GOKDOGAN",    clsid = "{NEXTGEN_GOKDOGAN}",    faction = "nato_bvr",   polar = "FM_AAM_BVR",   shape = "ng_gokdogan_astra",caliber = 0.178, length = 3.70, display_name = "TUBITAK Gokdogan BVR (NextGen)",  short_name = "Gokdogan", mass = 160.0, mach_max = 4.2, range_max = 100000, fuel_mass = 50.0,  impulse = 248, burn_time = 8.5,  warhead_mass = 20.0, ccm = 0.04, g_limit = 40, picture = "aim120c.png", life_time = 145 },
    { id = "NG_R_DARTER",    clsid = "{NEXTGEN_R_DARTER}",    faction = "nato_bvr",   polar = "FM_AAM_BVR",   shape = "ng_pl12a",         caliber = 0.160, length = 3.62, display_name = "Denel R-Darter BVR (NextGen)",    short_name = "R-Darter", mass = 120.0, mach_max = 4.0, range_max = 75000,  fuel_mass = 40.0,  impulse = 244, burn_time = 7.5,  warhead_mass = 18.0, ccm = 0.06, g_limit = 40, picture = "aim120c.png" },

    -- European / French / Allied WVR
    { id = "NG_MICA_RF",     clsid = "{NEXTGEN_MICA_RF}",     faction = "french_all", polar = "FM_AAM_WVR",   shape = "ng_mica_ng",       caliber = 0.160, length = 3.10, display_name = "MBDA MICA EM/RF (NextGen)",       short_name = "MICA-RF",  mass = 112.0, mach_max = 4.0, range_max = 80000,  fuel_mass = 40.0,  impulse = 245, burn_time = 6.5,  warhead_mass = 12.0, ccm = 0.05, g_limit = 50, head_type = 2, picture = "aim120c.png", life_time = 110 },
    { id = "NG_MICA_IR",     clsid = "{NEXTGEN_MICA_IR}",     faction = "french_all", polar = "FM_AAM_WVR",   shape = "ng_mica_ng",       caliber = 0.160, length = 3.10, display_name = "MBDA MICA IR (NextGen)",          short_name = "MICA-IR",  mass = 112.0, mach_max = 4.0, range_max = 60000,  fuel_mass = 40.0,  impulse = 245, burn_time = 6.5,  warhead_mass = 12.0, ccm = 0.04, g_limit = 50, head_type = 1, picture = "aim9x.png",   life_time = 100 },
    { id = "NG_MICA_NG_EM",  clsid = "{NEXTGEN_MICA_NG_EM}",  faction = "french_all", polar = "FM_AAM_WVR",   shape = "ng_mica_ng",       caliber = 0.160, length = 3.10, display_name = "MICA NG RF Dual-Pulse (NextGen)", short_name = "MICA-NGR", mass = 115.0, mach_max = 4.2, range_max = 105000, fuel_mass = 48.0,  impulse = 258, burn_time = 9.0,  warhead_mass = 12.0, ccm = 0.02, g_limit = 50, head_type = 2, picture = "aim120c.png", life_time = 135 },
    { id = "NG_MICA_NG_IR",  clsid = "{NEXTGEN_MICA_NG_IR}",  faction = "french_all", polar = "FM_AAM_WVR",   shape = "ng_mica_ng",       caliber = 0.160, length = 3.10, display_name = "MICA NG IR Matrix (NextGen)",     short_name = "MICA-NGI", mass = 115.0, mach_max = 4.2, range_max = 80000,  fuel_mass = 48.0,  impulse = 258, burn_time = 9.0,  warhead_mass = 12.0, ccm = 0.02, g_limit = 50, head_type = 1, picture = "aim9x.png",   life_time = 120 },
    { id = "NG_IRIS_T",      clsid = "{NEXTGEN_IRIS_T}",      faction = "nato_wvr",   polar = "FM_AAM_WVR",   shape = "ng_iris_t",        caliber = 0.127, length = 2.94, display_name = "IRIS-T IIR TVC (NextGen)",        short_name = "IRIS-T",   mass = 87.4,  mach_max = 3.2, range_max = 28000,  fuel_mass = 30.0,  impulse = 245, burn_time = 4.8,  warhead_mass = 11.4, ccm = 0.02, g_limit = 60, head_type = 1, picture = "aim9x.png",   life_time = 65 },
    { id = "NG_IRIS_T_SL",   clsid = "{NEXTGEN_IRIS_T_SL}",   faction = "nato_wvr",   polar = "FM_AAM_WVR",   shape = "ng_sam_irist_slm", caliber = 0.152, length = 4.00, display_name = "IRIS-T SL Extended (NextGen)",    short_name = "IRIST-SL", mass = 118.0, mach_max = 3.8, range_max = 45000,  fuel_mass = 44.0,  impulse = 250, burn_time = 7.5,  warhead_mass = 11.4, ccm = 0.02, g_limit = 50, head_type = 1, picture = "aim9x.png",   life_time = 90 },
    { id = "NG_AAM_5B",      clsid = "{NEXTGEN_AAM_5B}",      faction = "nato_wvr",   polar = "FM_AAM_WVR",   shape = "ng_iris_t",        caliber = 0.130, length = 3.10, display_name = "Mitsubishi AAM-5B IIR (NextGen)", short_name = "AAM-5B",   mass = 95.0,  mach_max = 3.5, range_max = 35000,  fuel_mass = 34.0,  impulse = 248, burn_time = 5.2,  warhead_mass = 11.0, ccm = 0.02, g_limit = 55, head_type = 1, picture = "aim9x.png",   life_time = 75 },
    { id = "NG_PYTHON_4",    clsid = "{NEXTGEN_PYTHON_4}",    faction = "nato_wvr",   polar = "FM_AAM_WVR",   shape = "ng_python5",       caliber = 0.160, length = 3.00, display_name = "Rafael Python-4 WVR (NextGen)",   short_name = "Python-4", mass = 105.0, mach_max = 3.5, range_max = 18000,  fuel_mass = 30.0,  impulse = 235, burn_time = 4.5,  warhead_mass = 11.0, ccm = 0.05, g_limit = 50, head_type = 1, picture = "aim9x.png",   life_time = 55 },
    { id = "NG_BOZDOGAN",    clsid = "{NEXTGEN_BOZDOGAN}",    faction = "nato_wvr",   polar = "FM_AAM_WVR",   shape = "ng_aim9x_b3",      caliber = 0.160, length = 3.00, display_name = "TUBITAK Bozdogan WVR (NextGen)",  short_name = "Bozdogan", mass = 102.0, mach_max = 3.8, range_max = 30000,  fuel_mass = 34.0,  impulse = 246, burn_time = 5.0,  warhead_mass = 11.0, ccm = 0.03, g_limit = 55, head_type = 1, picture = "aim9x.png",   life_time = 70 },
    { id = "NG_A_DARTER",    clsid = "{NEXTGEN_A_DARTER}",    faction = "nato_wvr",   polar = "FM_AAM_WVR",   shape = "ng_iris_t",        caliber = 0.166, length = 2.98, display_name = "Denel A-Darter 5th-Gen IIR (NG)", short_name = "A-Darter", mass = 93.0,  mach_max = 3.5, range_max = 26000,  fuel_mass = 32.0,  impulse = 246, burn_time = 4.8,  warhead_mass = 10.0, ccm = 0.03, g_limit = 55, head_type = 1, picture = "aim9x.png",   life_time = 65 },
    { id = "NG_TC1_SKYSWORD",clsid = "{NEXTGEN_TC1_SKYSWORD}",faction = "nato_wvr",   polar = "FM_AAM_WVR",   shape = "ng_python5",       caliber = 0.127, length = 2.87, display_name = "TC-1 Sky Sword I WVR (NextGen)",  short_name = "TC-1",     mass = 89.0,  mach_max = 3.2, range_max = 18000,  fuel_mass = 28.0,  impulse = 238, burn_time = 4.5,  warhead_mass = 10.0, ccm = 0.06, g_limit = 45, head_type = 1, picture = "aim9x.png",   life_time = 55 },

    -- East / China / Russia BVR & WVR
    { id = "NG_PL_12A",      clsid = "{NEXTGEN_PL_12A}",      faction = "east_bvr",   polar = "FM_AAM_BVR",   shape = "ng_pl12a",         caliber = 0.203, length = 3.93, display_name = "PL-12A / SD-10A Improved (NG)",   short_name = "PL-12A",   mass = 199.0, mach_max = 4.4, range_max = 110000, fuel_mass = 70.0,  impulse = 250, burn_time = 9.0,  warhead_mass = 22.0, ccm = 0.04, g_limit = 40, picture = "r77.png",     life_time = 150 },
    { id = "NG_PL_15",       clsid = "{NEXTGEN_PL_15}",       faction = "east_bvr",   polar = "FM_AAM_BVR",   shape = "ng_pl15",          caliber = 0.203, length = 4.00, display_name = "PL-15 AESA BVR (NextGen)",        short_name = "PL-15",    mass = 210.0, mach_max = 5.0, range_max = 220000, fuel_mass = 96.0,  impulse = 262, burn_time = 14.0, warhead_mass = 24.0, ccm = 0.02, g_limit = 40, picture = "r77.png",     life_time = 210 },
    { id = "NG_PL_15E",      clsid = "{NEXTGEN_PL_15E}",      faction = "east_bvr",   polar = "FM_AAM_BVR",   shape = "ng_pl15e",         caliber = 0.203, length = 4.00, display_name = "PL-15E Fold-Fin Export (NextGen)",short_name = "PL-15E",   mass = 205.0, mach_max = 4.8, range_max = 160000, fuel_mass = 80.0,  impulse = 258, burn_time = 12.0, warhead_mass = 22.0, ccm = 0.03, g_limit = 40, picture = "r77.png",     life_time = 180 },
    { id = "NG_R_77_1",      clsid = "{NEXTGEN_R_77_1}",      faction = "east_bvr",   polar = "FM_AAM_BVR",   shape = "ng_r77_grid",      caliber = 0.200, length = 3.71, display_name = "R-77-1 / RVV-SD Grid-Fin (NG)",   short_name = "R-77-1",   mass = 190.0, mach_max = 4.5, range_max = 110000, fuel_mass = 68.0,  impulse = 250, burn_time = 9.0,  warhead_mass = 22.5, ccm = 0.04, g_limit = 40, picture = "r77.png",     life_time = 145 },
    { id = "NG_R_77M",       clsid = "{NEXTGEN_R_77M}",       faction = "east_bvr",   polar = "FM_AAM_BVR",   shape = "ng_r77m",          caliber = 0.200, length = 3.71, display_name = "R-77M Izdeliye 180 (NextGen)",    short_name = "R-77M",    mass = 195.0, mach_max = 5.0, range_max = 190000, fuel_mass = 88.0,  impulse = 260, burn_time = 13.0, warhead_mass = 22.5, ccm = 0.02, g_limit = 42, picture = "r77.png",     life_time = 195 },
    { id = "NG_RVV_MD2",     clsid = "{NEXTGEN_RVV_MD2}",     faction = "east_bvr",   polar = "FM_AAM_WVR",   shape = "ng_r74m2",         caliber = 0.170, length = 2.95, display_name = "RVV-MD2 Internal-Bay WVR (NG)",   short_name = "RVV-MD2",  mass = 108.0, mach_max = 3.4, range_max = 50000,  fuel_mass = 38.0,  impulse = 248, burn_time = 6.0,  warhead_mass = 8.0,  ccm = 0.02, g_limit = 50, head_type = 1, picture = "r73.png", life_time = 85 },
    { id = "NG_R_37M",       clsid = "{NEXTGEN_R_37M}",       faction = "east_bvr",   polar = "FM_AAM_ULTRA", shape = "ng_r37m",          caliber = 0.380, length = 4.06, display_name = "R-37M RVV-BD Long-Range (NG)",    short_name = "R-37M",    mass = 510.0, mach_max = 6.0, range_max = 320000, fuel_mass = 260.0, impulse = 270, burn_time = 18.0, warhead_mass = 60.0, ccm = 0.02, g_limit = 30, picture = "r33.png",     life_time = 280 },
    { id = "NG_KS_172",      clsid = "{NEXTGEN_KS_172}",      faction = "east_bvr",   polar = "FM_AAM_ULTRA", shape = "ng_r37m",          caliber = 0.400, length = 6.01, display_name = "KS-172 AAM-L AWACS-Killer (NG)",  short_name = "KS-172",   mass = 750.0, mach_max = 5.5, range_max = 400000, fuel_mass = 380.0, impulse = 272, burn_time = 24.0, warhead_mass = 50.0, ccm = 0.02, g_limit = 25, picture = "r33.png",     life_time = 340 },
}

local registered_clsids = {
    nato_bvr   = {},
    nato_wvr   = {},
    french_all = {},
    east_bvr   = {},
}

for _, spec in ipairs(specs) do
    local clsid = register_missile(spec)
    table.insert(registered_clsids[spec.faction], clsid)
end

table.insert(registered_clsids.french_all, "{NEXTGEN_METEOR}")
table.insert(registered_clsids.nato_bvr,   "{NEXTGEN_METEOR}")

return registered_clsids
