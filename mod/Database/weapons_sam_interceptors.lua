-- NextGen Ground-Launched SAM Interceptors & KEKA Aerospace Surface Rockets
-- Registers wsType_SA_Missile interceptors for Iron Dome, IRIS-T SLM, SAMP/T Aster-30, Patriot PAC-3 MSE, Pantsir-SM & KEKA Pad.

local polar = dofile(current_mod_path .. "/Database/polar_profiles.lua")

local function deep_copy(orig)
    if type(orig) ~= "table" then return orig end
    local copy = {}
    for k, v in pairs(orig) do
        copy[deep_copy(k)] = deep_copy(v)
    end
    return copy
end

local BASE_SAM_MISSILE = {
    category = CAT_MISSILES,
    caliber = 0.160,
    mass = 90.0,
    model = "ng_sam_tamir",
    sounderName = "Weapons/Missile",
    targeting_data = { fm_type = -1 },
    type_name = "missile",
    wsTypeOfWeapon = { wsType_Weapon, wsType_Missile, wsType_SA_Missile, WSTYPE_PLACEHOLDER },

    Escort = 1,
    Head_Type = 2, -- Active RF / dual datalink
    sigma = { 4, 4, 4 },
    M = 90.0,
    H_max = 25000,
    H_min = 1,
    H_min_t = 1,
    Diam = 160,
    Cx_pil = 2.0,
    D_max = 70000,
    D_min = 400,
    Head_Form = 1,
    Life_Time = 90,
    Nr_max = 45,
    v_min = 80,
    v_mid = 650,
    Mach_max = 3.2,
    t_b = 0.0,
    t_acc = 3.5,
    t_marsh = 6.0,
    Range_max = 70000,
    Fi_start = 3.14152,
    Fi_rak = 3.14152,
    Fi_excort = 2.6,
    Fi_search = 99.9,
    OmViz_max = 99.9,
    PN_gain = 5.0,
    Reflection = 0.012,
    SeekerGen = 4,
    KillDistance = 12,
    X_back = -1.45,
    Y_back = 0,
    Z_back = 0,
    ccm_k0 = 0.04,
    hoj = 1,
    loft = 1,
    supersonic_A_coef_skew = 0.15,
    nozzle_exit_area = 0.014,
    scheme = "schemes/missiles/aa_missile_amraam2.sch",
    class_name = "wAmmunitionSelfHoming",

    controller = { boost_start = 0, march_start = 2.8 },
    exhaust = { 0.85, 0.85, 0.85, 0.35 },

    boost = {
        custom_smoke_dissipation_factor = 0.2,
        fuel_mass = 22.0,
        impulse = 255,
        nozzle_exit_area = 0.014,
        nozzle_orientationXYZ = { { 0, 0, 0 } },
        nozzle_position = { { -1.45, 0, 0 } },
        smoke_color = { 0.95, 0.95, 0.95 },
        smoke_transparency = 0.75,
        tail_width = 0.38,
        work_time = 2.8,
    },
    march = {
        custom_smoke_dissipation_factor = 0.2,
        fuel_mass = 18.0,
        impulse = 248,
        nozzle_exit_area = 0.014,
        nozzle_orientationXYZ = { { 0, 0, 0 } },
        nozzle_position = { { -1.45, 0, 0 } },
        smoke_color = { 0.90, 0.90, 0.90 },
        smoke_transparency = 0.25,
        tail_width = 0.25,
        work_time = 5.5,
    },

    active_radar_lock_dist = 25000,
    go_to_active_by_default = 1,

    actuator = {
        D = 280, T1 = 0.002, T2 = 0.005, Tf = 0.005,
        fin_stall = 1, max_delta = 0.35, max_omega = 12.0, sim_count = 4,
    },

    autopilot = {
        Ka = 18, Kd = 190, Knav = 5, Krx = 2, Kx = 0.1, T1 = 309, Tc = 0.05, Tf = 0.08,
        accel_coeffs = { 0, 12.0, -1.2, -0.25, 24, 0.00017 },
        cmd_delay = 0.35, dV0 = 420, delay = 0.15,
        fins_limit = 0.35, fins_limit_x = 0.087, gload_limit = 45,
        loft_active = 1, loft_factor = 4.5, loft_off_range = 12000, loft_sin = 0.50,
        null_roll = 0.785398, op_time = 120,
    },

    fm = deep_copy(polar.FM_AAM_WVR),

    seeker = {
        FOV = 2.4, abs_err_val = 1.0, aim_sigma = 1.5, aim_y_offset = 0.0,
        ang_err_val = 0.0001, blind_rad_val = 1, calc_aim_dist = 200000,
        delay = 0.25, err_correct_time = 1.0, guide_to_last_pos = true, keep_aim_time = 5,
        lock_manual_target_types_only = 0, max_w_LOS = 0.85, op_time = 120,
        pos_memory_time = 60, sens_far_dist = 80000, sens_near_dist = 60,
    },

    proximity_fuze = { arm_delay = 0.4, radius = 14 },
    warhead = {
        caliber = 160, concrete_factors = { 1, 1, 1 }, concrete_obj_factor = 0,
        cumulative_factor = 0, cumulative_thickness = 0, expl_mass = 14.0, fantom = 1,
        mass = 14.0, obj_factors = { 1, 1 }, other_factors = { 1, 1, 1 }, piercing_mass = 5.0,
    },
    warhead_air = {
        caliber = 160, concrete_factors = { 1, 1, 1 }, concrete_obj_factor = 0,
        cumulative_factor = 0, cumulative_thickness = 0, expl_mass = 14.0, fantom = 1,
        mass = 14.0, obj_factors = { 1, 1 }, other_factors = { 1, 1, 1 }, piercing_mass = 5.0,
    },
}

local sam_missiles = {}

local function reg_sam(spec)
    local w = deep_copy(BASE_SAM_MISSILE)
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
    w.D_min = spec.d_min or 400
    w.H_max = spec.h_max or 25000
    w.Life_Time = spec.life_time or 110
    w.Nr_max = spec.g_limit or 45
    w.autopilot.gload_limit = spec.g_limit or 45
    w.KillDistance = spec.kill_dist or 12
    w.proximity_fuze.radius = spec.kill_dist or 12
    w.ccm_k0 = spec.ccm or 0.03

    polar.apply_polar(w, spec.polar, spec.caliber, spec.mass, spec.length)

    local back = -(spec.length * 0.5)
    w.X_back = back
    w.boost.fuel_mass = spec.boost_fuel
    w.boost.impulse = spec.boost_isp or 255
    w.boost.work_time = spec.boost_time
    w.boost.nozzle_position = { { back + 0.04, 0, 0 } }
    w.controller.march_start = spec.boost_time

    w.march.fuel_mass = spec.march_fuel
    w.march.impulse = spec.march_isp or 248
    w.march.work_time = spec.march_time
    w.march.nozzle_position = { { back + 0.04, 0, 0 } }
    w.t_acc = spec.boost_time
    w.t_marsh = spec.march_time

    if spec.troll then
        w.boost.smoke_transparency = 1.0
        w.boost.tail_width = 1.25
        w.boost.smoke_color = { 0.92, 0.78, 0.58 }
        w.march.smoke_transparency = 0.95
        w.march.tail_width = 1.1
        w.seeker.aim_sigma = 18.0
        w.fm.finsTau = 0.30
    end

    w.warhead.caliber = math.floor(spec.caliber * 1000)
    w.warhead.expl_mass = spec.warhead
    w.warhead.mass = spec.warhead
    w.warhead_air.caliber = math.floor(spec.caliber * 1000)
    w.warhead_air.expl_mass = spec.warhead
    w.warhead_air.mass = spec.warhead

    w.shape_table_data = {
        { name = spec.id, file = spec.shape, life = 1, fire = { 0, 1 }, username = spec.display_name, index = WSTYPE_PLACEHOLDER },
    }

    local reg = declare_weapon(w)
    sam_missiles[spec.id] = reg
    return reg
end

local specs = {
    { id = "NG_SAM_TAMIR",      shape = "ng_sam_tamir",     polar = "FM_AAM_WVR",    caliber = 0.160, length = 3.00, display_name = "Tamir Iron Dome Interceptor (NG)",  short_name = "Tamir",    mass = 90.0,  mach_max = 2.8, range_max = 70000,  d_min = 350, h_max = 12000, boost_fuel = 22.0, boost_time = 2.5, march_fuel = 18.0, march_time = 6.5,  warhead = 12.0, g_limit = 48, kill_dist = 10, life_time = 85 },
    { id = "NG_SAM_IRIST_SLM",  shape = "ng_sam_irist_slm", polar = "FM_AAM_BVR",    caliber = 0.152, length = 4.00, display_name = "IRIS-T SLM Interceptor (NextGen)", short_name = "IRIST-SLM",mass = 120.0, mach_max = 3.5, range_max = 45000,  d_min = 400, h_max = 20000, boost_fuel = 32.0, boost_time = 3.2, march_fuel = 24.0, march_time = 7.5,  warhead = 12.0, g_limit = 55, kill_dist = 12, life_time = 95 },
    { id = "NG_SAM_ASTER30",    shape = "ng_sam_aster30",   polar = "FM_AAM_ULTRA",  caliber = 0.180, length = 4.90, display_name = "MBDA Aster 30 B1NT ABM (NextGen)", short_name = "Aster-30", mass = 450.0, mach_max = 4.5, range_max = 150000, d_min = 1200,h_max = 25000, boost_fuel = 160.0,boost_time = 3.8, march_fuel = 65.0, march_time = 11.0, warhead = 20.0, g_limit = 60, kill_dist = 14, life_time = 160 },
    { id = "NG_SAM_PAC3_MSE",   shape = "ng_sam_pac3_mse",  polar = "FM_AAM_ULTRA",  caliber = 0.255, length = 5.20, display_name = "MIM-104F PAC-3 MSE HTK (NextGen)", short_name = "PAC3-MSE", mass = 365.0, mach_max = 5.0, range_max = 120000, d_min = 1000,h_max = 35000, boost_fuel = 125.0,boost_time = 4.2, march_fuel = 55.0, march_time = 9.5,  warhead = 24.0, g_limit = 55, kill_dist = 8,  life_time = 140 },
    { id = "NG_SAM_57E6M",      shape = "ng_sam_tamir",     polar = "FM_AAM_BVR",    caliber = 0.170, length = 3.20, display_name = "57E6M Pantsir-SM HyperSAM (NG)",   short_name = "57E6M",    mass = 94.0,  mach_max = 5.2, range_max = 32000,  d_min = 600, h_max = 18000, boost_fuel = 36.0, boost_time = 2.2, march_fuel = 12.0, march_time = 4.0,  warhead = 20.0, g_limit = 38, kill_dist = 10, life_time = 65 },
    { id = "NG_SAM_KEKA_T5",    shape = "ng_keka_tropo5",   polar = "FM_KEKA_TROLL", caliber = 0.280, length = 3.60, display_name = "KEKA Troposphere-5 (Troll SAM!)",  short_name = "KEKA-T5",  mass = 180.0, mach_max = 2.9, range_max = 35000,  d_min = 400, h_max = 18000, boost_fuel = 65.0, boost_time = 4.5, march_fuel = 25.0, march_time = 6.0,  warhead = 45.0, g_limit = 18, kill_dist = 20, life_time = 90,  troll = true },
    { id = "NG_SAM_KEKA_T6",    shape = "ng_keka_tropo6",   polar = "FM_KEKA_TROLL", caliber = 0.340, length = 5.20, display_name = "KEKA Troposphere-6 Booster (Troll!)",short_name = "KEKA-T6", mass = 420.0, mach_max = 4.2, range_max = 95000,  d_min = 600, h_max = 35000, boost_fuel = 180.0,boost_time = 6.5, march_fuel = 70.0, march_time = 10.0, warhead = 110.0,g_limit = 16, kill_dist = 28, life_time = 150, troll = true },
}

for _, sp in ipairs(specs) do
    reg_sam(sp)
end

return sam_missiles
