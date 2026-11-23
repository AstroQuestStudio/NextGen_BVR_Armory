-- NextGen BVR & WVR Air-to-Air Weapon Definitions (DCS World 2.9+ Modular API)
-- Includes baseline & sub-variant BVR/WVR missiles with folding-fin DrawArg 25 where applicable.

local function deep_copy(orig)
    if type(orig) ~= "table" then return orig end
    local copy = {}
    for k, v in pairs(orig) do
        copy[deep_copy(k)] = deep_copy(v)
    end
    return copy
end

-- Base supersonic active-radar BVR template derived from AIM-120C/D (aa_missile_amraam2.sch)
local BASE_BVR_TEMPLATE = {
    category = CAT_AIR_TO_AIR,
    caliber = 0.178,
    mass = 152.0,
    model = "ng_aim120cd",
    sounderName = "Weapons/Missile",
    targeting_data = { fm_type = -1 },
    type_name = "missile",
    wsTypeOfWeapon = { wsType_Weapon, wsType_Missile, wsType_AA_Missile, WSTYPE_PLACEHOLDER },

    Escort = 1,
    Head_Type = 2, -- Active Radar
    sigma = { 5, 5, 5 },
    M = 152.0,
    H_max = 20000,
    H_min = 1,
    H_min_t = 1,
    Diam = 178,
    Cx_pil = 1.9,
    D_max = 105000,
    D_min = 700,
    Head_Form = 0,
    Life_Time = 110,
    Nr_max = 40,
    v_min = 140,
    v_mid = 800,
    Mach_max = 4.0,
    t_b = 0,
    t_acc = 4.0,
    t_marsh = 7.0,
    Range_max = 110000,
    Fi_start = 0.5,
    Fi_rak = 3.14152,
    Fi_excort = 1.05,
    Fi_search = 0.9,
    OmViz_max = 0.52,
    PN_gain = 4.5,
    Reflection = 0.015,
    SeekerGen = 4,
    KillDistance = 15,
    X_back = -1.8,
    Y_back = 0,
    Z_back = 0,
    ccm_k0 = 0.1,
    hoj = 1,
    loft = 1,
    supersonic_A_coef_skew = 0.17,
    nozzle_exit_area = 0.014,
    scheme = "schemes/missiles/aa_missile_amraam2.sch",
    class_name = "wAmmunitionSelfHoming",

    controller = {
        boost_start = 0,
        march_start = 0.2,
    },
    exhaust = { 0.8, 0.8, 0.8, 0.04 },

    boost = {
        custom_smoke_dissipation_factor = 0.2,
        fuel_mass = 0,
        impulse = 1,
        nozzle_exit_area = 0.014,
        nozzle_orientationXYZ = { { 0, 0, 0 } },
        nozzle_position = { { -1.75, 0, 0 } },
        smoke_color = { 0.85, 0.85, 0.85 },
        smoke_transparency = 0.05,
        tail_width = 0.2,
        work_time = 0.2,
    },

    march = {
        custom_smoke_dissipation_factor = 0.2,
        fuel_mass = 52.0,
        impulse = 250,
        nozzle_exit_area = 0.014,
        nozzle_orientationXYZ = { { 0, 0, 0 } },
        nozzle_position = { { -1.75, 0, 0 } },
        smoke_color = { 0.85, 0.85, 0.85 },
        smoke_opacity_type = 1,
        smoke_transparency = 0.02,
        tail_width = 0.2,
        work_time = 10.0,
    },

    active_radar_lock_dist = 20000,
    go_to_active_by_default = 1,

    actuator = {
        D = 260,
        T1 = 0.004,
        T2 = 0.008,
        Tf = 0.008,
        fin_stall = 1,
        max_delta = 0.35,
        max_omega = 8.0,
        sim_count = 4,
    },

    autopilot = {
        K_loft = 5.0,
        Kconv = 3.2,
        Kd = 0.024,
        Kd_loft = 0.5,
        Ki = 0.001,
        Knv = 0.0012,
        Kout = 1,
        Krx = 1.6,
        Kx = 0.04,
        PN_coeffs = {
            4,
            10000, 0.4,
            25000, 0.8,
            45000, 1.0,
            80000, 0.8,
        },
        PN_dist_data = {
            15000, 1,
            5000, 1,
        },
        alg = 0,
        bang_bang = 0,
        delay = 0.6,
        fins_limit = 0.35,
        fins_limit_x = 0.087,
        loft_active_by_default = 1,
        max_A_loft = 4.0,
        max_pitch_cmd = 0.52,
        max_signal_Fi = 0.22,
        min_a_conv_approach_vel = 150,
        min_horiz_time = 2,
        null_roll = 0.785398,
        op_time = 120,
        rotate_fins_output = 0,
        target_angle_loft = 0.35,
        x_channel_delay = 0.4,
    },

    fm = {
        A1trim = { 16, 16, 16, 16, 16, 17, 18, 20, 21, 21, 22, 22, 23, 23, 24, 24, 24, 25, 25, 25, 25, 25, 25, 25, 25, 25 },
        A2trim = { 16, 16, 16, 16, 16, 17, 18, 20, 21, 21, 22, 22, 23, 23, 24, 24, 24, 25, 25, 25, 25, 25, 25, 25, 25, 25 },
        Cx0 = { 0.36, 0.36, 0.36, 0.36, 0.40, 0.56, 0.68, 0.65, 0.60, 0.56, 0.52, 0.48, 0.45, 0.42, 0.40, 0.38, 0.36, 0.35, 0.34, 0.33, 0.32, 0.31, 0.30, 0.29, 0.28, 0.27 },
        CxB = { 0.014, 0.014, 0.014, 0.014, 0.016, 0.028, 0.058, 0.065, 0.060, 0.055, 0.050, 0.045, 0.040, 0.036, 0.033, 0.030, 0.028, 0.026, 0.024, 0.022, 0.020, 0.019, 0.018, 0.017, 0.016, 0.015 },
        Cya = { 1.15, 1.15, 1.15, 1.15, 1.18, 1.38, 1.42, 1.35, 1.25, 1.14, 1.05, 0.98, 0.92, 0.87, 0.82, 0.78, 0.74, 0.71, 0.68, 0.65, 0.62, 0.60, 0.58, 0.56, 0.54, 0.52 },
        Cza = { 1.15, 1.15, 1.15, 1.15, 1.18, 1.38, 1.42, 1.35, 1.25, 1.14, 1.05, 0.98, 0.92, 0.87, 0.82, 0.78, 0.74, 0.71, 0.68, 0.65, 0.62, 0.60, 0.58, 0.56, 0.54, 0.52 },
        Ix = 2.0,
        Iy = 190.0,
        Iz = 190.0,
        K1 = { 0.005, 0.005, 0.005, 0.005, 0.005, 0.0048, 0.0044, 0.0040, 0.0036, 0.0033, 0.0030, 0.0028, 0.0026, 0.0024, 0.0023, 0.0022, 0.0021, 0.0020, 0.0019, 0.0018, 0.0017, 0.0016, 0.0015, 0.0014, 0.0013, 0.0012 },
        K2 = { 0.005, 0.005, 0.005, 0.005, 0.005, 0.0048, 0.0044, 0.0040, 0.0036, 0.0033, 0.0030, 0.0028, 0.0026, 0.0024, 0.0023, 0.0022, 0.0021, 0.0020, 0.0019, 0.0018, 0.0017, 0.0016, 0.0015, 0.0014, 0.0013, 0.0012 },
        L = 0.178,
        Mxd = 20.0,
        Mxw = -50.0,
        Mya = { -0.50, -0.50, -0.50, -0.50, -0.55, -0.68, -0.70, -0.64, -0.56, -0.48, -0.42, -0.37, -0.33, -0.30, -0.27, -0.25, -0.23, -0.22, -0.21, -0.20, -0.19, -0.18, -0.17, -0.16, -0.15, -0.15 },
        Myw = { -2.0, -2.0, -2.0, -2.0, -2.2, -2.6, -2.8, -2.7, -2.5, -2.4, -2.3, -2.2, -2.1, -2.0, -1.9, -1.9, -1.8, -1.8, -1.7, -1.7, -1.6, -1.6, -1.6, -1.5, -1.5, -1.5 },
        Mza = { -0.50, -0.50, -0.50, -0.50, -0.55, -0.68, -0.70, -0.64, -0.56, -0.48, -0.42, -0.37, -0.33, -0.30, -0.27, -0.25, -0.23, -0.22, -0.21, -0.20, -0.19, -0.18, -0.17, -0.16, -0.15, -0.15 },
        Mzw = { -2.0, -2.0, -2.0, -2.0, -2.2, -2.6, -2.8, -2.7, -2.5, -2.4, -2.3, -2.2, -2.1, -2.0, -1.9, -1.9, -1.8, -1.8, -1.7, -1.7, -1.6, -1.6, -1.6, -1.5, -1.5, -1.5 },
        S = 0.025,
        caliber = 0.178,
        delta_max = 0.35,
        draw_fins_conv = { 1.570796, 1, 1 },
        fins_part_val = 0,
        fins_stall = 1,
        mass = 152.0,
        model_roll = 0.785398,
        rotated_fins_inp = 0,
        table_degree_values = 1,
        table_scale = 0.2,
        tail_first = 0,
        wind_sigma = 0,
        wind_time = 0,
    },

    seeker = {
        FOV = 1.57,
        abs_err_val = 1.5,
        aim_sigma = 2.0,
        aim_y_offset = 0.0,
        ang_err_val = 0.0001,
        blind_rad_val = 1,
        calc_aim_dist = 150000,
        delay = 0.5,
        err_correct_time = 1.5,
        guide_to_last_pos = true,
        keep_aim_time = 5,
        lock_manual_target_types_only = 0,
        max_w_LOS = 0.5,
        op_time = 120,
        pos_memory_time = 60,
        sens_far_dist = 80000,
        sens_near_dist = 150,
    },

    proximity_fuze = {
        arm_delay = 0.8,
        radius = 15,
    },

    warhead = {
        caliber = 178,
        concrete_factors = { 1, 1, 1 },
        concrete_obj_factor = 0,
        cumulative_factor = 0,
        cumulative_thickness = 0,
        expl_mass = 20.0,
        fantom = 1,
        mass = 20.0,
        obj_factors = { 1, 1 },
        other_factors = { 1, 1, 1 },
        piercing_mass = 5.0,
    },

    warhead_air = {
        caliber = 178,
        concrete_factors = { 1, 1, 1 },
        concrete_obj_factor = 0,
        cumulative_factor = 0,
        cumulative_thickness = 0,
        expl_mass = 20.0,
        fantom = 1,
        mass = 20.0,
        obj_factors = { 1, 1 },
        other_factors = { 1, 1, 1 },
        piercing_mass = 5.0,
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
    w.fm.caliber = spec.caliber
    w.fm.L = spec.caliber
    w.fm.S = math.pi * (spec.caliber * 0.5) * (spec.caliber * 0.5)
    w.mass = spec.mass
    w.M = spec.mass
    w.fm.mass = spec.mass
    w.Mach_max = spec.mach_max
    w.Range_max = spec.range_max
    w.D_max = spec.range_max
    w.Life_Time = spec.life_time or 140
    w.Nr_max = spec.g_limit or 40
    w.autopilot.Areq_limit = spec.g_limit or 40
    w.autopilot.op_time = w.Life_Time
    w.seeker.op_time = w.Life_Time
    w.march.fuel_mass = spec.fuel_mass
    w.march.impulse = spec.impulse
    w.march.work_time = spec.burn_time
    w.t_marsh = spec.burn_time
    w.active_radar_lock_dist = spec.pitbull_dist or 20000
    w.Head_Type = spec.head_type or 2
    w.ccm_k0 = spec.ccm or 0.08
    w.warhead.caliber = math.floor(spec.caliber * 1000)
    w.warhead.expl_mass = spec.warhead_mass
    w.warhead.mass = spec.warhead_mass
    w.warhead_air.caliber = math.floor(spec.caliber * 1000)
    w.warhead_air.expl_mass = spec.warhead_mass
    w.warhead_air.mass = spec.warhead_mass

    local back = -(spec.length * 0.5)
    w.X_back = back
    w.boost.nozzle_position = { { back + 0.05, 0, 0 } }
    w.march.nozzle_position = { { back + 0.05, 0, 0 } }

    if spec.head_type == 1 then
        w.autopilot.loft_active_by_default = 0
        w.loft = 0
        w.hoj = 0
        w.seeker.sens_far_dist = 35000
        w.seeker.FOV = 2.4
    else
        w.autopilot.loft_active_by_default = spec.loft ~= nil and spec.loft or 1
        w.loft = spec.loft ~= nil and spec.loft or 1
        w.seeker.sens_far_dist = spec.range_max * 0.75
    end

    if FOLDING_AAM_SHAPES[spec.shape] then
        w.encyclopediaAnimation = { args = { [25] = 1 } }
    end

    w.shape_table_data = {
        {
            name = spec.id,
            file = spec.shape,
            life = 1,
            fire = { 0, 1 },
            username = spec.display_name,
            index = WSTYPE_PLACEHOLDER,
        },
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
        Elements = {
            {
                ShapeName = spec.shape,
            },
        },
    })

    return spec.clsid
end

local specs = {
    -- US / NATO / Allied BVR
    { id = "NG_AIM_120A",    clsid = "{NEXTGEN_AIM_120A}",    faction = "nato_bvr",   shape = "ng_aim120a",  caliber = 0.178, length = 3.66, display_name = "AIM-120A AMRAAM (NextGen)",       short_name = "AIM-120A",  mass = 152.0, mach_max = 4.0, range_max = 75000,  fuel_mass = 45.0,  impulse = 240, burn_time = 7.0,  warhead_mass = 22.0, ccm = 0.12, g_limit = 40, picture = "aim120c.png" },
    { id = "NG_AIM_120C5",   clsid = "{NEXTGEN_AIM_120C5}",   faction = "nato_bvr",   shape = "ng_aim120cd", caliber = 0.178, length = 3.66, display_name = "AIM-120C-5 AMRAAM (NextGen)",     short_name = "AIM120C5",  mass = 157.0, mach_max = 4.1, range_max = 105000, fuel_mass = 52.0,  impulse = 248, burn_time = 8.2,  warhead_mass = 20.0, ccm = 0.07, g_limit = 42, picture = "aim120c.png" },
    { id = "NG_AIM_120C7",   clsid = "{NEXTGEN_AIM_120C7}",   faction = "nato_bvr",   shape = "ng_aim120cd", caliber = 0.178, length = 3.66, display_name = "AIM-120C-7 AMRAAM (NextGen)",     short_name = "AIM120C7",  mass = 161.5, mach_max = 4.2, range_max = 120000, fuel_mass = 56.0,  impulse = 250, burn_time = 9.0,  warhead_mass = 20.0, ccm = 0.05, g_limit = 42, picture = "aim120c.png" },
    { id = "NG_AIM_120C8",   clsid = "{NEXTGEN_AIM_120C8}",   faction = "nato_bvr",   shape = "ng_aim120cd", caliber = 0.178, length = 3.66, display_name = "AIM-120C-8 / D Export (NextGen)", short_name = "AIM120C8",  mass = 161.5, mach_max = 4.3, range_max = 150000, fuel_mass = 62.0,  impulse = 254, burn_time = 10.5, warhead_mass = 20.0, ccm = 0.03, g_limit = 44, picture = "aim120c.png", life_time = 175 },
    { id = "NG_AIM_120D3",   clsid = "{NEXTGEN_AIM_120D3}",   faction = "nato_bvr",   shape = "ng_aim120cd", caliber = 0.178, length = 3.66, display_name = "AIM-120D-3 AMRAAM (NextGen)",     short_name = "AIM120D3",  mass = 161.5, mach_max = 4.5, range_max = 180000, fuel_mass = 66.0,  impulse = 255, burn_time = 12.0, warhead_mass = 20.0, ccm = 0.02, g_limit = 45, picture = "aim120c.png", life_time = 200 },
    { id = "NG_AIM_260",     clsid = "{NEXTGEN_AIM_260}",     faction = "nato_bvr",   shape = "ng_aim260",   caliber = 0.178, length = 3.66, display_name = "AIM-260A JATM (NextGen)",         short_name = "AIM-260A",  mass = 168.0, mach_max = 5.2, range_max = 260000, fuel_mass = 82.0,  impulse = 265, burn_time = 15.0, warhead_mass = 22.0, ccm = 0.01, g_limit = 50, picture = "aim120c.png", life_time = 240 },
    { id = "NG_AIM_174B",    clsid = "{NEXTGEN_AIM_174B}",    faction = "nato_bvr",   shape = "ng_aim174b",  caliber = 0.343, length = 5.03, display_name = "AIM-174B Gunslinger (NextGen)",   short_name = "AIM-174B",  mass = 860.0, mach_max = 5.5, range_max = 380000, fuel_mass = 430.0, impulse = 270, burn_time = 22.0, warhead_mass = 60.0, ccm = 0.01, g_limit = 32, picture = "aim54.png",   life_time = 320 },
    { id = "NG_AIM_54C_PLUS",clsid = "{NEXTGEN_AIM_54C_PLUS}",faction = "nato_bvr",   shape = "ng_aim54e",   caliber = 0.380, length = 3.96, display_name = "AIM-54C+ Sea Phoenix (NextGen)",  short_name = "AIM54C+",   mass = 465.0, mach_max = 4.6, range_max = 185000, fuel_mass = 170.0, impulse = 250, burn_time = 22.0, warhead_mass = 60.0, ccm = 0.05, g_limit = 22, picture = "aim54.png",   life_time = 200 },
    { id = "NG_AAM_4B",      clsid = "{NEXTGEN_AAM_4B}",      faction = "nato_bvr",   shape = "ng_aam4b",    caliber = 0.203, length = 3.67, display_name = "Mitsubishi AAM-4B AESA (NextGen)",short_name = "AAM-4B",    mass = 222.0, mach_max = 4.5, range_max = 120000, fuel_mass = 78.0,  impulse = 252, burn_time = 10.0, warhead_mass = 24.0, ccm = 0.03, g_limit = 42, picture = "aim120c.png", life_time = 160 },
    { id = "NG_I_DERBY_ER",  clsid = "{NEXTGEN_I_DERBY_ER}",  faction = "nato_bvr",   shape = "ng_pl12a",    caliber = 0.160, length = 3.62, display_name = "Rafael I-Derby ER (NextGen)",     short_name = "Derby-ER",  mass = 118.0, mach_max = 4.2, range_max = 100000, fuel_mass = 46.0,  impulse = 250, burn_time = 9.0,  warhead_mass = 23.0, ccm = 0.04, g_limit = 45, picture = "aim120c.png", life_time = 150 },
    { id = "NG_METEOR",      clsid = "{NEXTGEN_METEOR}",      faction = "nato_bvr",   shape = "ng_meteor",   caliber = 0.178, length = 3.65, display_name = "MBDA Meteor Ramjet (NextGen)",    short_name = "Meteor",    mass = 190.0, mach_max = 4.8, range_max = 220000, fuel_mass = 95.0,  impulse = 420, burn_time = 35.0, warhead_mass = 24.0, ccm = 0.01, g_limit = 45, picture = "aim120c.png", life_time = 260 },

    -- European / French / NATO WVR
    { id = "NG_MICA_RF",     clsid = "{NEXTGEN_MICA_RF}",     faction = "french_all", shape = "ng_mica_ng",  caliber = 0.160, length = 3.10, display_name = "MBDA MICA EM/RF (NextGen)",       short_name = "MICA-RF",   mass = 112.0, mach_max = 4.0, range_max = 80000,  fuel_mass = 40.0,  impulse = 245, burn_time = 6.5,  warhead_mass = 12.0, ccm = 0.05, g_limit = 50, head_type = 2, picture = "aim120c.png", life_time = 110 },
    { id = "NG_MICA_IR",     clsid = "{NEXTGEN_MICA_IR}",     faction = "french_all", shape = "ng_mica_ng",  caliber = 0.160, length = 3.10, display_name = "MBDA MICA IR (NextGen)",          short_name = "MICA-IR",   mass = 112.0, mach_max = 4.0, range_max = 60000,  fuel_mass = 40.0,  impulse = 245, burn_time = 6.5,  warhead_mass = 12.0, ccm = 0.04, g_limit = 50, head_type = 1, picture = "aim9x.png",   life_time = 100 },
    { id = "NG_MICA_NG_EM",  clsid = "{NEXTGEN_MICA_NG_EM}",  faction = "french_all", shape = "ng_mica_ng",  caliber = 0.160, length = 3.10, display_name = "MICA NG RF Dual-Pulse (NextGen)", short_name = "MICA-NGR",  mass = 115.0, mach_max = 4.2, range_max = 105000, fuel_mass = 48.0,  impulse = 258, burn_time = 9.0,  warhead_mass = 12.0, ccm = 0.02, g_limit = 50, head_type = 2, picture = "aim120c.png", life_time = 135 },
    { id = "NG_MICA_NG_IR",  clsid = "{NEXTGEN_MICA_NG_IR}",  faction = "french_all", shape = "ng_mica_ng",  caliber = 0.160, length = 3.10, display_name = "MICA NG IR Matrix (NextGen)",     short_name = "MICA-NGI",  mass = 115.0, mach_max = 4.2, range_max = 80000,  fuel_mass = 48.0,  impulse = 258, burn_time = 9.0,  warhead_mass = 12.0, ccm = 0.02, g_limit = 50, head_type = 1, picture = "aim9x.png",   life_time = 120 },
    { id = "NG_IRIS_T",      clsid = "{NEXTGEN_IRIS_T}",      faction = "nato_wvr",   shape = "ng_iris_t",   caliber = 0.127, length = 2.94, display_name = "IRIS-T IIR TVC (NextGen)",        short_name = "IRIS-T",    mass = 87.4,  mach_max = 3.2, range_max = 28000,  fuel_mass = 30.0,  impulse = 245, burn_time = 4.8,  warhead_mass = 11.4, ccm = 0.02, g_limit = 60, head_type = 1, picture = "aim9x.png",   life_time = 65 },
    { id = "NG_IRIS_T_SL",   clsid = "{NEXTGEN_IRIS_T_SL}",   faction = "nato_wvr",   shape = "ng_iris_t",   caliber = 0.152, length = 3.30, display_name = "IRIS-T SL Extended (NextGen)",    short_name = "IRIST-SL",  mass = 118.0, mach_max = 3.8, range_max = 45000,  fuel_mass = 44.0,  impulse = 250, burn_time = 7.5,  warhead_mass = 11.4, ccm = 0.02, g_limit = 50, head_type = 1, picture = "aim9x.png",   life_time = 90 },
    { id = "NG_AAM_5B",      clsid = "{NEXTGEN_AAM_5B}",      faction = "nato_wvr",   shape = "ng_iris_t",   caliber = 0.130, length = 3.10, display_name = "Mitsubishi AAM-5B IIR (NextGen)", short_name = "AAM-5B",    mass = 95.0,  mach_max = 3.5, range_max = 35000,  fuel_mass = 34.0,  impulse = 248, burn_time = 5.2,  warhead_mass = 11.0, ccm = 0.02, g_limit = 55, head_type = 1, picture = "aim9x.png",   life_time = 75 },
    { id = "NG_PYTHON_4",    clsid = "{NEXTGEN_PYTHON_4}",    faction = "nato_wvr",   shape = "ng_python5",  caliber = 0.160, length = 3.00, display_name = "Rafael Python-4 WVR (NextGen)",   short_name = "Python-4",  mass = 105.0, mach_max = 3.5, range_max = 18000,  fuel_mass = 30.0,  impulse = 235, burn_time = 4.5,  warhead_mass = 11.0, ccm = 0.05, g_limit = 50, head_type = 1, picture = "aim9x.png",   life_time = 55 },

    -- East / China / Russia BVR
    { id = "NG_PL_12A",      clsid = "{NEXTGEN_PL_12A}",      faction = "east_bvr",   shape = "ng_pl12a",    caliber = 0.203, length = 3.93, display_name = "PL-12A / SD-10A Improved (NG)",   short_name = "PL-12A",    mass = 199.0, mach_max = 4.4, range_max = 110000, fuel_mass = 70.0,  impulse = 250, burn_time = 9.0,  warhead_mass = 22.0, ccm = 0.04, g_limit = 40, picture = "r77.png",     life_time = 150 },
    { id = "NG_PL_15",       clsid = "{NEXTGEN_PL_15}",       faction = "east_bvr",   shape = "ng_pl15",     caliber = 0.203, length = 4.00, display_name = "PL-15 AESA BVR (NextGen)",        short_name = "PL-15",     mass = 210.0, mach_max = 5.0, range_max = 220000, fuel_mass = 96.0,  impulse = 262, burn_time = 14.0, warhead_mass = 24.0, ccm = 0.02, g_limit = 40, picture = "r77.png",     life_time = 210 },
    { id = "NG_PL_15E",      clsid = "{NEXTGEN_PL_15E}",      faction = "east_bvr",   shape = "ng_pl15e",    caliber = 0.203, length = 4.00, display_name = "PL-15E Fold-Fin Export (NextGen)",short_name = "PL-15E",    mass = 205.0, mach_max = 4.8, range_max = 160000, fuel_mass = 80.0,  impulse = 258, burn_time = 12.0, warhead_mass = 22.0, ccm = 0.03, g_limit = 40, picture = "r77.png",     life_time = 180 },
    { id = "NG_R_77_1",      clsid = "{NEXTGEN_R_77_1}",      faction = "east_bvr",   shape = "ng_r77_grid", caliber = 0.200, length = 3.71, display_name = "R-77-1 / RVV-SD Grid-Fin (NG)",   short_name = "R-77-1",    mass = 190.0, mach_max = 4.5, range_max = 110000, fuel_mass = 68.0,  impulse = 250, burn_time = 9.0,  warhead_mass = 22.5, ccm = 0.04, g_limit = 40, picture = "r77.png",     life_time = 145 },
    { id = "NG_R_77M",       clsid = "{NEXTGEN_R_77M}",       faction = "east_bvr",   shape = "ng_r77m",     caliber = 0.200, length = 3.71, display_name = "R-77M Izdeliye 180 (NextGen)",    short_name = "R-77M",     mass = 195.0, mach_max = 5.0, range_max = 190000, fuel_mass = 88.0,  impulse = 260, burn_time = 13.0, warhead_mass = 22.5, ccm = 0.02, g_limit = 42, picture = "r77.png",     life_time = 195 },
    { id = "NG_R_37M",       clsid = "{NEXTGEN_R_37M}",       faction = "east_bvr",   shape = "ng_r37m",     caliber = 0.380, length = 4.06, display_name = "R-37M RVV-BD Long-Range (NG)",    short_name = "R-37M",     mass = 510.0, mach_max = 6.0, range_max = 320000, fuel_mass = 260.0, impulse = 270, burn_time = 18.0, warhead_mass = 60.0, ccm = 0.02, g_limit = 30, picture = "r33.png",     life_time = 280 },
    { id = "NG_KS_172",      clsid = "{NEXTGEN_KS_172}",      faction = "east_bvr",   shape = "ng_r37m",     caliber = 0.400, length = 6.01, display_name = "KS-172 AAM-L AWACS-Killer (NG)",  short_name = "KS-172",    mass = 750.0, mach_max = 5.5, range_max = 400000, fuel_mass = 380.0, impulse = 272, burn_time = 24.0, warhead_mass = 50.0, ccm = 0.02, g_limit = 25, picture = "r33.png",     life_time = 340 },
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

-- Cross-compatible loadouts so European and Russian aircraft also get Meteor & IRIS-T
table.insert(registered_clsids.french_all, "{NEXTGEN_METEOR}")
table.insert(registered_clsids.nato_bvr,   "{NEXTGEN_METEOR}")

return registered_clsids
