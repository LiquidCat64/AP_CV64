from .data import lname, rname, ename
from typing import List, Union

# # #    KEY    # # #
# "stage" = What stage the Region is a part of. The Region and its corresponding Locations and Entrances will only be
#           put in if its stage is active.
# "locations" = The Locations to add to that Region when putting in said Region (provided their add conditions pass).
# "entrances" = The Entrances to add to that Region when putting in said Region (provided their add conditions pass).
region_info = {
    "Menu": {},

    rname.fl_start: {"stage": rname.foggy_lake,
                     "locations": [lname.fld_forecast_port,
                                   lname.fld_forecast_starboard,
                                   lname.fld_foremast_lower,
                                   lname.fld_stairs_port,
                                   lname.fld_stairs_starboard,
                                   lname.fld_net_port,
                                   lname.fld_net_starboard,
                                   lname.fld_mainmast_base,
                                   lname.fld_near_door,
                                   lname.fld_near_block_l,
                                   lname.fld_near_block_r,
                                   lname.fld_above_door,
                                   lname.fld_stern_port,
                                   lname.fld_stern_starboard,
                                   lname.fld_poop_port_crates,
                                   lname.fld_poop_starboard_crates,
                                   lname.fld_mainmast_top,
                                   lname.fld_jiggermast,
                                   lname.fld_foremast_upper_port,
                                   lname.fld_foremast_upper_starboard],
                     "entrances": [ename.fl_to_below]},

    rname.fl_middle: {"stage": rname.foggy_lake,
                      "locations": [lname.flb_hallway_l,
                                    lname.flb_hallway_r,
                                    lname.flb_tall_crates,
                                    lname.flb_short_crates_l,
                                    lname.flb_short_crates_r],
                      "entrances": [ename.fl_from_below,
                                    ename.fl_sink]},

    rname.fl_end: {"stage": rname.foggy_lake,
                   "locations": [lname.flp_pier_l,
                                 lname.flp_pier_m,
                                 lname.flp_pier_r,
                                 lname.flp_statue_l,
                                 lname.flp_statue_r],
                   "entrances": [ename.fl_end]},

    rname.forest_start: {"stage": rname.forest_of_silence,
                         "locations": [lname.forest_pier_center,
                                       lname.forest_pier_end],
                         "entrances": [ename.forest_king_skeleton_1]},

    rname.forest_half_1: {"stage": rname.forest_of_silence,
                          "locations": [lname.forest_sypha_ne,
                                        lname.forest_sypha_se,
                                        lname.forest_sypha_nw,
                                        lname.forest_sypha_sw,
                                        lname.forest_flea_trail,
                                        lname.forest_leap,
                                        lname.forest_descent,
                                        lname.forest_tunnel,
                                        lname.forest_child_ledge],
                          "entrances": [ename.forest_dbridge_gate]},

    rname.forest_half_2: {"stage": rname.forest_of_silence,
                          "locations": [lname.forest_charnel_1,
                                        lname.forest_charnel_2,
                                        lname.forest_charnel_3,
                                        lname.forest_pike,
                                        lname.forest_werewolf_pit,
                                        lname.forest_end_gate],
                          "entrances": [ename.forest_reverse_leap,
                                        ename.forest_final_switch]},

    rname.forest_end: {"stage": rname.forest_of_silence,
                       "locations": [lname.forest_skelly_mouth],
                       "entrances": [ename.forest_end]},

    rname.cw_start: {"stage": rname.castle_wall,
                     "locations": [lname.cwr_bottom,
                                   lname.cwr_top,
                                   lname.cw_dragon_sw,
                                   # lname.cw_boss,
                                   lname.cw_save_slab1,
                                   lname.cw_save_slab2,
                                   lname.cw_save_slab3,
                                   lname.cw_save_slab4,
                                   lname.cw_save_slab5,
                                   lname.cw_rrampart,
                                   lname.cw_lrampart,
                                   lname.cw_pillar,
                                   lname.cw_shelf,
                                   lname.cw_shelf_torch],
                     "entrances": [ename.cw_lt_door,
                                   ename.villa_warp]},

    rname.cw_exit: {"stage": rname.castle_wall,
                    "locations": [lname.cw_ground_left,
                                  lname.cw_ground_middle,
                                  lname.cw_ground_right]},

    rname.cw_ltower: {"stage": rname.castle_wall,
                      "locations": [lname.cwl_bottom,
                                    lname.cwl_bridge,
                                    lname.cw_drac_sw,
                                    lname.cw_drac_slab1,
                                    lname.cw_drac_slab2,
                                    lname.cw_drac_slab3,
                                    lname.cw_drac_slab4,
                                    lname.cw_drac_slab5],
                      "entrances": [ename.cw_portcullis_c,
                                    ename.cw_end]},

    rname.villa_start: {"stage": rname.villa,
                        "locations": [lname.villafy_outer_gate_l,
                                      lname.villafy_outer_gate_r,
                                      lname.villafy_inner_gate],
                        "entrances": [ename.villa_dog_gates]},

    rname.villa_entrance: {"stage": rname.villa,
                           "locations": [lname.villafy_gate_marker,
                                         lname.villafy_villa_marker,
                                         lname.villafo_front_r,
                                         lname.villafo_front_l,
                                         lname.villafo_mid_l,
                                         lname.villafo_mid_r,
                                         lname.villafo_rear_r,
                                         lname.villafo_rear_l,
                                         lname.villafo_pot_r,
                                         lname.villafo_pot_l,
                                         lname.villafo_sofa,
                                         lname.villafo_chandelier1,
                                         lname.villafo_chandelier2,
                                         lname.villafo_chandelier3,
                                         lname.villafo_chandelier4,
                                         lname.villafo_chandelier5],
                           "entrances": [ename.villa_snipe_dogs,
                                         ename.villa_fountain_pillar,
                                         ename.villa_into_servant_door,
                                         ename.villa_to_rose_garden]},

    rname.villa_fountain: {"stage": rname.villa,
                           "locations": [lname.villafy_fountain_fl,
                                         lname.villafy_fountain_fr,
                                         lname.villafy_fountain_ml,
                                         lname.villafy_fountain_mr,
                                         lname.villafy_fountain_rl,
                                         lname.villafy_fountain_rr],
                           "entrances": [ename.villa_fountain_shine]},

    rname.villa_fountain_top: {"stage": rname.villa,
                               "locations": [lname.villafy_fountain_shine]},

    rname.villa_living: {"stage": rname.villa,
                         "locations": [lname.villafo_6am_roses,
                                       lname.villala_hallway_stairs,
                                       lname.villala_hallway_l,
                                       lname.villala_hallway_r,
                                       lname.villala_vincent,
                                       lname.villala_slivingroom_table_l,
                                       lname.villala_slivingroom_table_r,
                                       lname.villala_slivingroom_mirror,
                                       lname.villala_diningroom_roses,
                                       lname.villala_llivingroom_pot_r,
                                       lname.villala_llivingroom_pot_l,
                                       lname.villala_llivingroom_painting,
                                       lname.villala_llivingroom_light,
                                       lname.villala_llivingroom_lion,
                                       lname.villala_exit_knight],
                         "entrances": [ename.villa_from_rose_garden,
                                       ename.villa_to_storeroom,
                                       ename.villa_to_archives,
                                       ename.villa_rescue_henry,
                                       # ename.villa_renon,
                                       ename.villa_to_main_maze_gate]},

    rname.villa_storeroom: {"stage": rname.villa,
                            "locations": [lname.villala_storeroom_l,
                                          lname.villala_storeroom_r,
                                          lname.villala_storeroom_s],
                            "entrances": [ename.villa_from_storeroom]},

    rname.villa_archives: {"stage": rname.villa,
                           "locations": [lname.villala_archives_table,
                                         lname.villala_archives_rear]},

    rname.villa_mary_reward: {"stage": rname.villa,
                              "locations": [lname.villala_mary]},

    rname.villa_maze_f: {"stage": rname.villa,
                         "locations": [lname.villam_malus_torch,
                                       lname.villam_malus_bush,
                                       lname.villam_fplatform,
                                       lname.villam_frankieturf_l,
                                       lname.villam_frankieturf_r,
                                       lname.villam_frankieturf_ru],
                         "entrances": [ename.villa_from_main_maze_gate,
                                       ename.villa_copper_door,
                                       ename.villa_front_rose_doors]},

    rname.villa_maze_r: {"stage": rname.villa,
                         "locations": [lname.villam_hole_de,
                                       lname.villam_child_de,
                                       lname.villam_rplatform_f,
                                       lname.villam_rplatform_r,
                                       lname.villam_rplatform_de,
                                       lname.villam_exit_de,
                                       lname.villam_serv_path_l,
                                       lname.villam_serv_path_sl,
                                       lname.villam_serv_path_sr],
                         "entrances": [ename.villa_from_rear_maze_gate,
                                       ename.villa_thorn_fence,
                                       ename.villa_copper_skip_e,
                                       ename.villa_copper_skip_i,
                                       ename.villa_rear_rose_doors]},

    rname.villa_fgarden: {"stage": rname.villa,
                          "locations": [lname.villam_fgarden_f,
                                        lname.villam_fgarden_mf,
                                        lname.villam_fgarden_mr,
                                        lname.villam_fgarden_r]},

    rname.villa_servants: {"stage": rname.villa,
                           "locations": [lname.villafo_serv_ent],
                           "entrances": [ename.villa_out_of_servant_door,
                                         ename.villa_to_rear_maze_gate]},

    rname.villa_crypt_e: {"stage": rname.villa,
                          "locations": [lname.villam_crypt_ent,
                                        lname.villam_crypt_upstream],
                          "entrances": [ename.villa_bridge_door,
                                        ename.villa_crest_door]},

    rname.villa_crypt_i: {"stage": rname.villa,
                          "locations": [lname.villac_ent_l,
                                        lname.villac_ent_r,
                                        lname.villac_wall_l,
                                        lname.villac_wall_r,
                                        lname.villac_coffin_l,
                                        lname.villac_coffin_r,
                                        lname.the_end]},

    rname.tunnel_start: {"stage": rname.tunnel,
                         "locations": [lname.tunnel_landing,
                                       lname.tunnel_landing_rc,
                                       lname.tunnel_stone_alcove_r,
                                       lname.tunnel_stone_alcove_l,
                                       lname.tunnel_twin_arrows,
                                       lname.tunnel_arrows_rock1,
                                       lname.tunnel_arrows_rock2,
                                       lname.tunnel_arrows_rock3,
                                       lname.tunnel_arrows_rock4,
                                       lname.tunnel_arrows_rock5,
                                       lname.tunnel_lonesome_bucket,
                                       lname.tunnel_lbucket_mdoor_l,
                                       lname.tunnel_lbucket_quag,
                                       lname.tunnel_bucket_quag_rock1,
                                       lname.tunnel_bucket_quag_rock2,
                                       lname.tunnel_bucket_quag_rock3,
                                       lname.tunnel_lbucket_albert,
                                       lname.tunnel_albert_camp,
                                       lname.tunnel_albert_quag,
                                       lname.tunnel_gondola_rc_sdoor_l,
                                       lname.tunnel_gondola_rc_sdoor_m,
                                       lname.tunnel_gondola_rc_sdoor_r,
                                       lname.tunnel_gondola_rc,
                                       lname.tunnel_rgondola_station,
                                       lname.tunnel_gondola_transfer],
                         "entrances": [ename.tunnel_start_renon,
                                       ename.tunnel_gondolas]},

    rname.tunnel_end: {"stage": rname.tunnel,
                       "locations": [lname.tunnel_corpse_bucket_quag,
                                     lname.tunnel_corpse_bucket_mdoor_l,
                                     lname.tunnel_corpse_bucket_mdoor_r,
                                     lname.tunnel_shovel_quag_start,
                                     lname.tunnel_exit_quag_start,
                                     lname.tunnel_shovel_quag_end,
                                     lname.tunnel_exit_quag_end,
                                     lname.tunnel_shovel,
                                     lname.tunnel_shovel_save,
                                     lname.tunnel_shovel_mdoor_l,
                                     lname.tunnel_shovel_mdoor_r,
                                     lname.tunnel_shovel_sdoor_l,
                                     lname.tunnel_shovel_sdoor_m,
                                     lname.tunnel_shovel_sdoor_r],
                       "entrances": [ename.tunnel_end_renon,
                                     ename.tunnel_end]},

    rname.uw_main: {"stage": rname.underground_waterway,
                    "locations": [lname.uw_near_ent,
                                  lname.uw_across_ent,
                                  lname.uw_first_ledge1,
                                  lname.uw_first_ledge2,
                                  lname.uw_first_ledge3,
                                  lname.uw_first_ledge4,
                                  lname.uw_first_ledge5,
                                  lname.uw_first_ledge6,
                                  lname.uw_poison_parkour,
                                  lname.uw_boss,
                                  lname.uw_waterfall_alcove,
                                  lname.uw_carrie1,
                                  lname.uw_carrie2,
                                  lname.uw_bricks_save,
                                  lname.uw_above_skel_ledge,
                                  lname.uw_in_skel_ledge1,
                                  lname.uw_in_skel_ledge2,
                                  lname.uw_in_skel_ledge3],
                    "entrances": [ename.uw_final_waterfall,
                                  ename.uw_renon]},

    rname.uw_end: {"stage": rname.underground_waterway,
                   "entrances": [ename.uw_waterfall_skip,
                                 ename.uw_end]},

    rname.cc_main: {"stage": rname.castle_center,
                    "locations": [lname.ccb_skel_hallway_ent,
                                  lname.ccb_skel_hallway_jun,
                                  lname.ccb_skel_hallway_tc,
                                  lname.ccb_skel_hallway_ba,
                                  lname.ccb_behemoth_l_ff,
                                  lname.ccb_behemoth_l_mf,
                                  lname.ccb_behemoth_l_mr,
                                  lname.ccb_behemoth_l_fr,
                                  lname.ccb_behemoth_r_ff,
                                  lname.ccb_behemoth_r_mf,
                                  lname.ccb_behemoth_r_mr,
                                  lname.ccb_behemoth_r_fr,
                                  lname.ccb_behemoth_crate1,
                                  lname.ccb_behemoth_crate2,
                                  lname.ccb_behemoth_crate3,
                                  lname.ccb_behemoth_crate4,
                                  lname.ccb_behemoth_crate5,
                                  lname.ccelv_near_machine,
                                  lname.ccelv_atop_machine,
                                  lname.ccelv_stand1,
                                  lname.ccelv_stand2,
                                  lname.ccelv_stand3,
                                  lname.ccelv_pipes,
                                  lname.ccelv_switch,
                                  lname.ccelv_staircase,
                                  lname.ccff_redcarpet_knight,
                                  lname.ccff_gears_side,
                                  lname.ccff_gears_mid,
                                  lname.ccff_gears_corner,
                                  lname.ccff_lizard_knight,
                                  lname.ccff_lizard_near_knight,
                                  lname.ccff_lizard_pit,
                                  lname.ccff_lizard_corner,
                                  lname.ccff_lizard_locker_nfr,
                                  lname.ccff_lizard_locker_nmr,
                                  lname.ccff_lizard_locker_nml,
                                  lname.ccff_lizard_locker_nfl,
                                  lname.ccff_lizard_locker_fl,
                                  lname.ccff_lizard_locker_fr,
                                  lname.ccff_lizard_slab1,
                                  lname.ccff_lizard_slab2,
                                  lname.ccff_lizard_slab3,
                                  lname.ccff_lizard_slab4,
                                  lname.ccll_brokenstairs_floor,
                                  lname.ccll_brokenstairs_knight,
                                  lname.ccll_brokenstairs_save,
                                  lname.ccll_glassknight_l,
                                  lname.ccll_glassknight_r,
                                  lname.ccll_butlers_door,
                                  lname.ccll_butlers_side,
                                  lname.ccll_cwhall_butlerflames_past,
                                  lname.ccll_cwhall_flamethrower,
                                  lname.ccll_cwhall_cwflames,
                                  lname.ccll_heinrich,
                                  lname.ccia_nitro_crates,
                                  lname.ccia_nitro_shelf_h,
                                  lname.ccia_stairs_knight,
                                  lname.ccia_maids_vase,
                                  lname.ccia_maids_outer,
                                  lname.ccia_maids_inner,
                                  lname.ccia_inventions_maids,
                                  lname.ccia_inventions_crusher,
                                  lname.ccia_inventions_famicart,
                                  lname.ccia_inventions_zeppelin,
                                  lname.ccia_inventions_round,
                                  lname.ccia_nitrohall_flamethrower,
                                  lname.ccia_nitrohall_torch,
                                  lname.ccia_nitro_shelf_i],
                    "entrances": [ename.cc_tc_door,
                                  ename.cc_lower_wall,
                                  ename.cc_renon,
                                  ename.cc_upper_wall]},

    rname.cc_torture_chamber: {"stage": rname.castle_center,
                               "locations": [lname.ccb_mandrag_shelf_l,
                                             lname.ccb_mandrag_shelf_r,
                                             lname.ccb_torture_rack,
                                             lname.ccb_torture_rafters]},

    rname.cc_library: {"stage": rname.castle_center,
                       "locations": [lname.ccll_cwhall_wall,
                                     lname.ccl_bookcase]},

    rname.cc_crystal: {"stage": rname.castle_center,
                       "locations": [lname.cc_behind_the_seal,
                                     lname.cc_boss_one,
                                     lname.cc_boss_two],
                       "entrances": [ename.cc_elevator]},

    rname.cc_elev_top: {"stage": rname.castle_center,
                        "entrances": [ename.cc_exit_r,
                                      ename.cc_exit_c]},

    rname.dt_main: {"stage": rname.duel_tower,
                    "locations": [lname.dt_boss_one,
                                  lname.dt_boss_two,
                                  lname.dt_ibridge_l,
                                  lname.dt_ibridge_r,
                                  lname.dt_stones_start,
                                  lname.dt_stones_end,
                                  lname.dt_werebull_arena,
                                  lname.dt_boss_three,
                                  lname.dt_boss_four],
                    "entrances": [ename.dt_start,
                                  ename.dt_end]},

    rname.toe_main: {"stage": rname.tower_of_execution,
                     "locations": [lname.toe_ledge1,
                                   lname.toe_ledge2,
                                   lname.toe_ledge3,
                                   lname.toe_ledge4,
                                   lname.toe_ledge5,
                                   lname.toe_midsavespikes_r,
                                   lname.toe_midsavespikes_l,
                                   lname.toe_elec_grate,
                                   lname.toe_ibridge,
                                   lname.toe_top],
                     "entrances": [ename.toe_start,
                                   ename.toe_gate,
                                   ename.toe_gate_skip,
                                   ename.toe_end]},

    rname.toe_ledge: {"stage": rname.tower_of_execution,
                      "locations": [lname.toe_keygate_l,
                                    lname.toe_keygate_r]},

    rname.tosci_start: {"stage": rname.tower_of_science,
                        "locations": [lname.tosci_elevator,
                                      lname.tosci_plain_sr,
                                      lname.tosci_stairs_sr],
                        "entrances": [ename.tosci_start,
                                      ename.tosci_key1_door,
                                      ename.tosci_to_key2_door]},

    rname.tosci_three_doors: {"stage": rname.tower_of_science,
                              "locations": [lname.tosci_three_door_hall]},

    rname.tosci_conveyors: {"stage": rname.tower_of_science,
                            "locations": [lname.tosci_ibridge_t,
                                          lname.tosci_ibridge_b1,
                                          lname.tosci_ibridge_b2,
                                          lname.tosci_ibridge_b3,
                                          lname.tosci_ibridge_b4,
                                          lname.tosci_ibridge_b5,
                                          lname.tosci_ibridge_b6,
                                          lname.tosci_conveyor_sr,
                                          lname.tosci_exit],
                            "entrances": [ename.tosci_from_key2_door,
                                          ename.tosci_key3_door,
                                          ename.tosci_end]},

    rname.tosci_key3: {"stage": rname.tower_of_science,
                       "locations": [lname.tosci_key3_r,
                                     lname.tosci_key3_m,
                                     lname.tosci_key3_l]},

    rname.tosor_main: {"stage": rname.tower_of_sorcery,
                       "locations": [lname.tosor_stained_tower,
                                     lname.tosor_savepoint,
                                     lname.tosor_trickshot,
                                     lname.tosor_yellow_bubble,
                                     lname.tosor_blue_platforms,
                                     lname.tosor_side_isle,
                                     lname.tosor_ibridge],
                       "entrances": [ename.tosor_start,
                                     ename.tosor_end]},

    rname.roc_main: {"stage": rname.room_of_clocks,
                     "locations": [lname.roc_ent_l,
                                   lname.roc_ent_r,
                                   lname.roc_elev_r,
                                   lname.roc_elev_l,
                                   lname.roc_cont_r,
                                   lname.roc_cont_l,
                                   lname.roc_exit,
                                   lname.roc_boss],
                     "entrances": [ename.roc_gate]},

    rname.ct_start: {"stage": rname.clock_tower,
                     "locations": [lname.ct_gearclimb_battery_slab1,
                                   lname.ct_gearclimb_battery_slab2,
                                   lname.ct_gearclimb_battery_slab3,
                                   lname.ct_gearclimb_side,
                                   lname.ct_gearclimb_corner,
                                   lname.ct_gearclimb_door_slab1,
                                   lname.ct_gearclimb_door_slab2,
                                   lname.ct_gearclimb_door_slab3],
                     "entrances": [ename.ct_to_door1]},

    rname.ct_middle: {"stage": rname.clock_tower,
                      "locations": [lname.ct_bp_chasm_fl,
                                    lname.ct_bp_chasm_fr,
                                    lname.ct_bp_chasm_rl,
                                    lname.ct_bp_chasm_k],
                      "entrances": [ename.ct_from_door1,
                                    ename.ct_to_door2]},

    rname.ct_end: {"stage": rname.clock_tower,
                   "locations": [lname.ct_finalroom_door_slab1,
                                 lname.ct_finalroom_door_slab2,
                                 lname.ct_finalroom_fl,
                                 lname.ct_finalroom_fr,
                                 lname.ct_finalroom_rl,
                                 lname.ct_finalroom_rr,
                                 lname.ct_finalroom_platform,
                                 lname.ct_finalroom_renon_slab1,
                                 lname.ct_finalroom_renon_slab2,
                                 lname.ct_finalroom_renon_slab3,
                                 lname.ct_finalroom_renon_slab4,
                                 lname.ct_finalroom_renon_slab5,
                                 lname.ct_finalroom_renon_slab6,
                                 lname.ct_finalroom_renon_slab7,
                                 lname.ct_finalroom_renon_slab8],
                   "entrances": [ename.ct_from_door2,
                                 ename.ct_renon,
                                 ename.ct_door_3]},

    rname.ck_main: {"stage": rname.castle_keep,
                    "locations": [lname.ck_boss_one,
                                  lname.ck_boss_two,
                                  lname.ck_flame_l,
                                  lname.ck_flame_r,
                                  lname.ck_behind_drac,
                                  lname.ck_cube],
                    "entrances": [ename.ck_slope_jump]},

    rname.renon: {"locations": [lname.renon1,
                                lname.renon2,
                                lname.renon3,
                                lname.renon4,
                                lname.renon5,
                                lname.renon6,
                                lname.renon7]},

    rname.ck_drac_chamber: {"locations": [lname.the_end]}
}


def get_region_info(region: str, info: str) -> Union[str, List[str], None]:
    return region_info[region].get(info, None)
