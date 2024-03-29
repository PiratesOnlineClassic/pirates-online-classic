from direct.directnotify import DirectNotifyGlobal
from pirates.movement.AnimationMixer import AnimationMixer


class BipedAnimationMixer(AnimationMixer):
    NA_INDEX = -1
    IDLE_INDEX = 0
    INPLACE_INDEX_0 = 1
    INPLACE_INDEX_1 = 2
    MOTION_INDEX = 3
    INMOTION_INDEX_0 = 4
    INMOTION_INDEX_1 = 5
    INMOTION_INDEX_2 = 6
    MOVIE_INDEX = 7
    LOOP = {
        'NA': NA_INDEX,
        'IDLE': IDLE_INDEX,
        'MOTION': MOTION_INDEX}
    ACTION = {
        'NA': NA_INDEX,
        'INPLACE_0': INPLACE_INDEX_0,
        'INPLACE_1': INPLACE_INDEX_1,
        'INMOTION_0': INMOTION_INDEX_0,
        'INMOTION_1': INMOTION_INDEX_1,
        'INMOTION_2': INMOTION_INDEX_2,
        'MOVIE': MOVIE_INDEX}
    notify = DirectNotifyGlobal.directNotify.newCategory('BipedAnimationMixer')
    sectionNames = [
        'legs',
        'torso',
        'head']
    sectionNameIds = dict(zip(sectionNames, range(len(sectionNames))))
    partNameLists = dict(zip(sectionNames, [
        [
            'legs'],
        [
            'torso'],
        [
            'head']]))
    AnimRankings = {
        'idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'idle_centered': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'idle_handhip': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'idle_handhip_from_idle': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'idle_flex': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'idle_arm_scratch': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'idle_butt_scratch': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'idle_head_scratch': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'idle_head_scratch_side': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'kraken_struggle_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'kraken_fight_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'map_head_into_look_left': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'map_head_outof_look_left': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'map_head_look_left_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'map_look_arm_right': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'map_look_arm_left': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'map_look_boot_left': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'map_look_boot_right': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'map_look_pant_right': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'idle_B_shiftWeight': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'idle_sit': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'idle_sit_alt': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'emote_anger': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'emote_celebrate': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'emote_coin_flip': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'emote_clap': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'emote_dance_jig': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'emote_fear': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'emote_flex': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'emote_laugh': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'emote_no': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'emote_sad': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'emote_smile': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'emote_thriller': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'emote_wave': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'emote_wink': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'emote_yawn': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'emote_yes': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'look_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'look_idle_2': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'walk': (LOOP['MOTION'], LOOP['MOTION'], LOOP['MOTION']),
        'walk_back_diagonal_left': (LOOP['MOTION'], LOOP['MOTION'], LOOP['MOTION']),
        'walk_back_diagonal_right': (LOOP['MOTION'], LOOP['MOTION'], LOOP['MOTION']),
        'turn_left': (LOOP['MOTION'], LOOP['MOTION'], LOOP['MOTION']),
        'turn_right': (LOOP['MOTION'], LOOP['MOTION'], LOOP['MOTION']),
        'spin_left': (LOOP['MOTION'], LOOP['MOTION'], LOOP['MOTION']),
        'spin_right': (LOOP['MOTION'], LOOP['MOTION'], LOOP['MOTION']),
        'run': (LOOP['MOTION'], LOOP['MOTION'], LOOP['MOTION']),
        'march': (LOOP['MOTION'], LOOP['MOTION'], LOOP['MOTION']),
        'left_face': (LOOP['MOTION'], LOOP['MOTION'], LOOP['MOTION']),
        'strafe_left': (LOOP['MOTION'], LOOP['MOTION'], LOOP['MOTION']),
        'strafe_right': (LOOP['MOTION'], LOOP['MOTION'], LOOP['MOTION']),
        'run_diagonal_left': (LOOP['MOTION'], LOOP['MOTION'], LOOP['MOTION']),
        'run_diagonal_right': (LOOP['MOTION'], LOOP['MOTION'], LOOP['MOTION']),
        'run_with_weapon': (LOOP['MOTION'], LOOP['MOTION'], LOOP['MOTION']),
        'jump': (ACTION['INMOTION_0'], ACTION['INMOTION_0'], ACTION['INMOTION_0']),
        'fall_ground': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'stock_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'stock_sleep': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'stock_sleep_to_idle': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'swim': (LOOP['MOTION'], LOOP['MOTION'], LOOP['MOTION']),
        'swim_left': (LOOP['MOTION'], LOOP['MOTION'], LOOP['MOTION']),
        'swim_right': (LOOP['MOTION'], LOOP['MOTION'], LOOP['MOTION']),
        'swim_left_diagonal': (LOOP['MOTION'], LOOP['MOTION'], LOOP['MOTION']),
        'swim_right_diagonal': (LOOP['MOTION'], LOOP['MOTION'], LOOP['MOTION']),
        'swim_back': (LOOP['MOTION'], LOOP['MOTION'], LOOP['MOTION']),
        'swim_back_diagonal_left': (LOOP['MOTION'], LOOP['MOTION'], LOOP['MOTION']),
        'swim_back_diagonal_right': (LOOP['MOTION'], LOOP['MOTION'], LOOP['MOTION']),
        'wheel': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'semi_conscious_loop': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'semi_conscious_standup': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'attention': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'sit': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'sit_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'teleport': (ACTION['MOVIE'], ACTION['MOVIE'], ACTION['MOVIE']),
        'coin_flip_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'coin_flip_look_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'coin_flip_old_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'drink_potion': (ACTION['INPLACE_1'], ACTION['INMOTION_2'], ACTION['INMOTION_2']),
        'search_low': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'search_med': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'searching': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'chant_a_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'chant_b_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'jump_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'summon_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'axe_chop_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'axe_chop_look_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'bar_wipe': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'bar_wipe_into_look': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'bar_wipe_look_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'bar_wipe_outof_look': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'bar_talk01_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'bar_talk01_into_look': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'bar_talk01_look_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'bar_talk01_outof_look': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'bar_talk02_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'bar_talk02_into_look': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'bar_talk02_look_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'bar_talk02_outof_look': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'bar_talk03_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'bar_write_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'bar_write_into_look': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'bar_write_look_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'bar_write_outof_look': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'barrel_hide_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'barrel_hide_into_look': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'barrel_hide_look_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'barrel_hide_outof_look': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'sit_hanginglegs_outof_look': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'sit_hanginglegs_look_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'sit_hanginglegs_into_look': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'sit_hanginglegs_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'sit_sleep_outof_look': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'sit_sleep_look_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'sit_sleep_into_look': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'sit_sleep_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'sleep_outof_look': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'sleep_into_look': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'sleep_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'sleep_sick_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'sleep_sick_into_look': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'sleep_sick_look_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'sleep_sick_outof_look': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'tatoo_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'tatoo_into_look': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'tatoo_look_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'tatoo_outof_look': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'tatoo_receive_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'tatoo_receive_into_look': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'tatoo_receive_look_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'tatoo_receive_outof_look': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'stir_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'stir_into_look': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'stir_look_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'stir_outof_look': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'sow_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'sow_into_look': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'sow_look_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'sow_outof_look': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'patient_work_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'doctor_work_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'doctor_work_into_look': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'doctor_work_look_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'doctor_work_outof_look': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'primp_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'primp_into_look': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'primp_look_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'primp_outof_look': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'lute_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'lute_into_look': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'lute_look_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'lute_outof_look': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'loom_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'loom_into_look': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'loom_look_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'loom_outof_look': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'crazy_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'crazy_look_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'flute_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'flute_look_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'look_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'roar_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'handdig_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'moaning_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'searching_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'repairfloor_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'repairfloor_into': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'repairfloor_outof': (ACTION['INPLACE_0'], ACTION['INPLACE_0'], ACTION['INPLACE_0']),
        'screenshot_pose': (ACTION['INPLACE_1'], ACTION['INMOTION_2'], ACTION['INMOTION_2']),
        'friend_pose': (ACTION['INPLACE_1'], ACTION['INMOTION_2'], ACTION['INMOTION_2']),
        'wheel_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'kneel': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'kneel_fromidle': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'boxing_fromidle': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'boxing_hit_head_right': (ACTION['INPLACE_0'], ACTION['INMOTION_1'], ACTION['INMOTION_1']),
        'boxing_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'boxing_idle_alt': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'boxing_kick': (ACTION['INPLACE_1'], ACTION['INMOTION_2'], ACTION['INMOTION_2']),
        'boxing_punch': (ACTION['INPLACE_1'], ACTION['INMOTION_2'], ACTION['INMOTION_2']),
        'boxing_haymaker': (ACTION['INPLACE_1'], ACTION['INMOTION_2'], ACTION['INMOTION_2']),
        'wand_cast_start': (ACTION['INPLACE_1'], ACTION['INMOTION_2'], ACTION['INMOTION_2']),
        'wand_cast_fire': (ACTION['INPLACE_1'], ACTION['INMOTION_2'], ACTION['INMOTION_2']),
        'wand_cast_idle': (LOOP['IDLE'], LOOP['MOTION'], LOOP['MOTION']),
        'wand_hurt': (ACTION['INPLACE_0'], ACTION['INMOTION_1'], ACTION['INMOTION_1']),
        'wand_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'wandCast': (ACTION['INPLACE_1'], ACTION['INMOTION_2'], ACTION['INMOTION_2']),
        'wandneutral': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'voodoo_draw': (ACTION['INPLACE_1'], ACTION['INMOTION_2'], ACTION['INMOTION_2']),
        'voodoo_doll_hurt': (ACTION['INPLACE_0'], ACTION['INMOTION_1'], ACTION['INMOTION_1']),
        'voodoo_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'voodoo_tune': (ACTION['INPLACE_1'], ACTION['INMOTION_2'], ACTION['INMOTION_2']),
        'voodoo_strafe_left': (LOOP['MOTION'], LOOP['MOTION'], LOOP['MOTION']),
        'voodoo_strafe_right': (LOOP['MOTION'], LOOP['MOTION'], LOOP['MOTION']),
        'voodoo_swarm': (ACTION['INPLACE_1'], ACTION['INMOTION_2'], ACTION['INMOTION_2']),
        'voodoo_walk': (LOOP['MOTION'], LOOP['MOTION'], LOOP['MOTION']),
        'voodoo_doll_poke': (ACTION['INPLACE_1'], ACTION['INMOTION_2'], ACTION['INMOTION_2']),
        'bomb_throw': (ACTION['INPLACE_1'], ACTION['INMOTION_2'], ACTION['INMOTION_2']),
        'bomb_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'bomb_hurt': (ACTION['INPLACE_0'], ACTION['INMOTION_1'], ACTION['INMOTION_1']),
        'bomb_draw': (ACTION['INPLACE_1'], ACTION['INMOTION_2'], ACTION['INMOTION_2']),
        'bomb_charge': (ACTION['INPLACE_1'], ACTION['INMOTION_2'], ACTION['INMOTION_2']),
        'bomb_charge_loop': (ACTION['INPLACE_1'], ACTION['INMOTION_2'], ACTION['INMOTION_2']),
        'bomb_charge_throw': (ACTION['INPLACE_1'], ACTION['INMOTION_2'], ACTION['INMOTION_2']),
        'bigbomb_throw': (ACTION['INPLACE_1'], ACTION['INMOTION_2'], ACTION['INMOTION_2']),
        'bigbomb_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'bigbomb_draw': (ACTION['INPLACE_1'], ACTION['INMOTION_2'], ACTION['INMOTION_2']),
        'bigbomb_walk': (LOOP['MOTION'], LOOP['MOTION'], LOOP['MOTION']),
        'bigbomb_walk_back': (LOOP['MOTION'], LOOP['MOTION'], LOOP['MOTION']),
        'bigbomb_walk_back_left': (LOOP['MOTION'], LOOP['MOTION'], LOOP['MOTION']),
        'bigbomb_walk_back_right': (LOOP['MOTION'], LOOP['MOTION'], LOOP['MOTION']),
        'bigbomb_walk_left': (LOOP['MOTION'], LOOP['MOTION'], LOOP['MOTION']),
        'bigbomb_walk_left_diagonal': (LOOP['MOTION'], LOOP['MOTION'], LOOP['MOTION']),
        'bigbomb_walk_right': (LOOP['MOTION'], LOOP['MOTION'], LOOP['MOTION']),
        'bigbomb_walk_right_diagonal': (LOOP['MOTION'], LOOP['MOTION'], LOOP['MOTION']),
        'bigbomb_charge': (ACTION['INPLACE_1'], ACTION['INMOTION_2'], ACTION['INMOTION_2']),
        'bigbomb_charge_loop': (ACTION['INPLACE_1'], ACTION['INMOTION_2'], ACTION['INMOTION_2']),
        'bigbomb_charge_throw': (ACTION['INPLACE_1'], ACTION['INMOTION_2'], ACTION['INMOTION_2']),
        'gun_draw': (ACTION['INPLACE_1'], ACTION['INMOTION_2'], ACTION['INMOTION_2']),
        'gun_fire': (ACTION['INPLACE_1'], ACTION['INMOTION_2'], ACTION['INMOTION_2']),
        'gun_hurt': (ACTION['INPLACE_0'], ACTION['INMOTION_1'], ACTION['INMOTION_1']),
        'gun_reload': (ACTION['INPLACE_1'], ACTION['INMOTION_2'], ACTION['INMOTION_2']),
        'gun_pointedup_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'gun_putaway': (ACTION['INPLACE_1'], ACTION['INMOTION_2'], ACTION['INMOTION_2']),
        'gun_aim_idle': (ACTION['INPLACE_1'], ACTION['INMOTION_2'], ACTION['INMOTION_2']),
        'bayonet_drill': (ACTION['INPLACE_1'], ACTION['INMOTION_2'], ACTION['INMOTION_2']),
        'bayonet_attackA': (ACTION['INPLACE_1'], ACTION['INMOTION_2'], ACTION['INMOTION_2']),
        'bayonet_attackB': (ACTION['INPLACE_1'], ACTION['INMOTION_2'], ACTION['INMOTION_2']),
        'bayonet_attackC': (ACTION['INPLACE_1'], ACTION['INMOTION_2'], ACTION['INMOTION_2']),
        'bayonet_idle_to_fight_idle': (ACTION['INPLACE_1'], ACTION['INMOTION_2'], ACTION['INMOTION_2']),
        'bayonet_attack_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'bayonet_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'bayonet_run': (LOOP['MOTION'], LOOP['MOTION'], LOOP['MOTION']),
        'bayonet_walk': (LOOP['MOTION'], LOOP['MOTION'], LOOP['MOTION']),
        'bayonet_attack_walk': (LOOP['MOTION'], LOOP['MOTION'], LOOP['MOTION']),
        'sword_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'sword_draw': (ACTION['INPLACE_1'], ACTION['INMOTION_2'], ACTION['INMOTION_2']),
        'sword_putaway': (ACTION['INPLACE_1'], ACTION['INMOTION_2'], ACTION['INMOTION_2']),
        'sword_slash': (ACTION['INPLACE_1'], ACTION['INMOTION_2'], ACTION['INMOTION_2']),
        'sword_comboA': (ACTION['INPLACE_1'], ACTION['INMOTION_2'], ACTION['INMOTION_2']),
        'sword_thrust': (ACTION['INPLACE_1'], ACTION['INMOTION_2'], ACTION['INMOTION_2']),
        'sword_roll_thrust': (ACTION['INPLACE_1'], ACTION['INMOTION_2'], ACTION['INMOTION_2']),
        'sword_cleave': (ACTION['INPLACE_1'], ACTION['INMOTION_2'], ACTION['INMOTION_2']),
        'sword_lunge': (ACTION['INPLACE_1'], ACTION['INMOTION_2'], ACTION['INMOTION_2']),
        'sword_hit': (ACTION['INPLACE_0'], ACTION['INMOTION_1'], ACTION['INMOTION_1']),
        'cutlass_attention': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'cutlass_combo': (ACTION['INPLACE_1'], ACTION['INMOTION_2'], ACTION['INMOTION_2']),
        'cutlass_hurt': (ACTION['INPLACE_0'], ACTION['INMOTION_1'], ACTION['INMOTION_1']),
        'cutlass_taunt': (ACTION['INPLACE_1'], ACTION['INMOTION_2'], ACTION['INMOTION_2']),
        'cutlass_bladestorm': (ACTION['INPLACE_1'], ACTION['INMOTION_2'], ACTION['INMOTION_2']),
        'cutlass_sweep': (ACTION['INPLACE_1'], ACTION['INMOTION_2'], ACTION['INMOTION_2']),
        'cutlass_headbutt': (ACTION['INPLACE_1'], ACTION['INMOTION_2'], ACTION['INMOTION_2']),
        'cutlass_kick': (ACTION['INPLACE_1'], ACTION['INMOTION_2'], ACTION['INMOTION_2']),
        'cutlass_walk_navy': (LOOP['MOTION'], LOOP['MOTION'], LOOP['MOTION']),
        'dagger_combo': (ACTION['INPLACE_1'], ACTION['INMOTION_2'], ACTION['INMOTION_2']),
        'knife_throw': (ACTION['INPLACE_1'], ACTION['INMOTION_2'], ACTION['INMOTION_2']),
        'dagger_asp': (ACTION['INPLACE_1'], ACTION['INMOTION_2'], ACTION['INMOTION_2']),
        'dagger_hurt': (ACTION['INPLACE_0'], ACTION['INMOTION_1'], ACTION['INMOTION_1']),
        'dagger_throw_sand': (ACTION['INPLACE_1'], ACTION['INMOTION_2'], ACTION['INMOTION_2']),
        'dagger_vipers_nest': (ACTION['INPLACE_1'], ACTION['INMOTION_2'], ACTION['INMOTION_2']),
        'foil_coup': (ACTION['INPLACE_1'], ACTION['INMOTION_2'], ACTION['INMOTION_2']),
        'foil_hack': (ACTION['INPLACE_1'], ACTION['INMOTION_2'], ACTION['INMOTION_2']),
        'foil_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'foil_slash': (ACTION['INPLACE_1'], ACTION['INMOTION_2'], ACTION['INMOTION_2']),
        'foil_thrust': (ACTION['INPLACE_1'], ACTION['INMOTION_2'], ACTION['INMOTION_2']),
        'foil_kick': (ACTION['INPLACE_1'], ACTION['INMOTION_2'], ACTION['INMOTION_2']),
        'sword_advance': (LOOP['MOTION'], LOOP['MOTION'], LOOP['MOTION']),
        'dualcutlass_comboA': (ACTION['INPLACE_1'], ACTION['INMOTION_2'], ACTION['INMOTION_2']),
        'dualcutlass_comboB': (ACTION['INPLACE_1'], ACTION['INMOTION_2'], ACTION['INMOTION_2']),
        'dualcutlass_draw': (ACTION['INPLACE_1'], ACTION['INMOTION_2'], ACTION['INMOTION_2']),
        'dualcutlass_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'dualcutlass_hurt': (ACTION['INPLACE_0'], ACTION['INMOTION_1'], ACTION['INMOTION_1']),
        'dualcutlass_walk': (LOOP['MOTION'], LOOP['MOTION'], LOOP['MOTION']),
        'shovel': (LOOP['MOTION'], LOOP['MOTION'], LOOP['MOTION']),
        'blacksmith_work_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'blacksmith_work_look_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'blacksmith_work_into_look': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'blacksmith_work_outof_look': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'shovel_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'shovel_idle_into_dig': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'fishing_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'fishing_pole_cast': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'fishing_pole_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'fishing_drawpole': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'chest_walk': (LOOP['MOTION'], LOOP['MOTION'], LOOP['MOTION']),
        'chest_strafe_left': (LOOP['MOTION'], LOOP['MOTION'], LOOP['MOTION']),
        'chest_strafe_right': (LOOP['MOTION'], LOOP['MOTION'], LOOP['MOTION']),
        'chest_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'chest_putdown': (ACTION['INPLACE_0'], ACTION['INMOTION_1'], ACTION['INMOTION_1']),
        'chest_kneel_to_steal': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'chest_steal': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'into_deal': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'deal': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'deal_left': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'deal_right': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'deal_idle': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'cards_bad_tell': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'cards_bet': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'cards_cheat': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'cards_check': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'cards_good_tell': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'cards_hide': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'cards_hide_hit': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'cards_hide_idle': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'cards_pick_up': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'cards_pick_up_idle': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'cards_set_down': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'cards_set_down_lose': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'cards_set_down_win': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'cards_set_down_win_show': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'cards_blackjack_hit': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'cards_blackjack_stay': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'sweep': (LOOP['MOTION'], LOOP['MOTION'], LOOP['MOTION']),
        'sweep_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'sweep_look_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'sweep_into_look': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'sweep_outof_look': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'rigging_climb': (LOOP['MOTION'], LOOP['MOTION'], LOOP['MOTION']),
        'tread_water': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'tread_water_into_teleport': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),
        'rope_grab': (ACTION['INMOTION_2'], ACTION['INMOTION_2'], ACTION['INMOTION_2']),
        'rope_grab_from_idle': (ACTION['INMOTION_2'], ACTION['INMOTION_2'], ACTION['INMOTION_2']),
        'rope_board': (ACTION['MOVIE'], ACTION['MOVIE'], ACTION['MOVIE']),
        'rope_dismount': (ACTION['MOVIE'], ACTION['MOVIE'], ACTION['MOVIE']),
        'swing_aboard': (ACTION['MOVIE'], ACTION['MOVIE'], ACTION['MOVIE']),
        'intro': (LOOP['MOTION'], LOOP['MOTION'], LOOP['MOTION']),
        'jail_dropinto': (ACTION['MOVIE'], ACTION['MOVIE'], ACTION['MOVIE']),
        'jail_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'jail_standup': (ACTION['MOVIE'], ACTION['MOVIE'], ACTION['MOVIE']),
        'death': (ACTION['MOVIE'], ACTION['MOVIE'], ACTION['MOVIE']),
        'death2': (ACTION['MOVIE'], ACTION['MOVIE'], ACTION['MOVIE']),
        'death3': (ACTION['MOVIE'], ACTION['MOVIE'], ACTION['MOVIE']),
        'death4': (ACTION['MOVIE'], ACTION['MOVIE'], ACTION['MOVIE']),
        'kick_door': (ACTION['INMOTION_2'], ACTION['INMOTION_2'], ACTION['INMOTION_2']),
        'kick_door_loop': (LOOP['IDLE'], LOOP['MOTION'], LOOP['MOTION']),
        'board': (ACTION['MOVIE'], ACTION['MOVIE'], ACTION['MOVIE']),
        'tentacle_squeeze': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'tentacle_idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'sand_in_eyes': (ACTION['INPLACE_0'], ACTION['INMOTION_1'], ACTION['INMOTION_1']),
        'sand_in_eyes_holdweapon_noswing': (ACTION['INPLACE_0'], ACTION['INMOTION_1'], ACTION['INMOTION_1']),
        'sand_in_eyes_wWeapon': (ACTION['INPLACE_0'], ACTION['INMOTION_1'], ACTION['INMOTION_1']),
        'bomb_receive': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'dagger_receive': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'doll_receive': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'staff_receive': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        '0_tut_act_1_1_1_jail': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        '0_tut_act_1_1_2_jail': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'tut_1_1_5_a_idle_dan': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        'tut_1_1_5_b_dan': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        '1_tut_act_1_1_5_a_dan': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        '1_tut_act_1_1_5_c_dan': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        '0_tut_act_1_2_dock': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        '1_tut_act_1_2_dock': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        '0_tut_act_1_2_b_dock': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        '1_tut_act_1_2_b_dock': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        '0_tut_act_1_3_jr_a': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        '0_tut_act_1_3_jr_b': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        '1_tut_act_1_3_jr_a': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        '1_tut_act_1_3_jr_b': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        '2_tut_act_1_3_jr_a': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        '2_tut_act_1_3_jr_b': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        '3_tut_act_1_3_jr_a': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        '3_tut_act_1_3_jr_b': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        '0_tut_act_2_1_wt': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        '0_tut_act_2_1_b_wt': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        '0_tut_act_2_3_es': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        '0_tut_act_2_4_cb_a': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        '0_tut_act_2_4_cb_b': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        '0_tut_act_2_4_cb_c': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        '0_tut_act_2_2_td': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        '1_tut_act_2_2_td': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        '2_tut_act_2_2_td': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        '3_tut_act_2_2_td': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        '4_tut_act_2_2_td': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        '5_tut_act_2_2_td': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        '0_tut_act_2_5_js': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        '1_tut_act_2_5_js': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        '0_tut_act_3_1_bp': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        '1_tut_act_3_1_bp': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        '2_tut_act_3_1_bp': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        '3_tut_act_3_1_bp': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        '4_tut_act_3_1_bp': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        '0_tut_act_3_2_js': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),
        '1_tut_act_3_2_js': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE'])}
