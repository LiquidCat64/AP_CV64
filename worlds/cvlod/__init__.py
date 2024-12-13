import os
import typing
import settings
import base64
import logging

from BaseClasses import Item, Region, Tutorial, ItemClassification
from .items import CVLoDItem, filler_item_names, get_item_info, get_item_names_to_ids, get_item_counts
from .locations import CVLoDLocation, get_location_info, verify_locations, get_location_names_to_ids, base_id
from .entrances import verify_entrances, get_warp_entrances
from .options import CVLoDOptions, CharacterStages, DraculasCondition, SubWeaponShuffle
from .stages import get_locations_from_stage, get_normal_stage_exits, vanilla_stage_order, \
    shuffle_stages, generate_warps, get_region_names
from .regions import get_region_info
from .rules import CVLoDRules
from .data import iname, rname, ename
from worlds.AutoWorld import WebWorld, World
from .aesthetics import randomize_lighting, shuffle_sub_weapons, randomize_music, get_start_inventory_data,\
    get_location_data, randomize_shop_prices, get_loading_zone_bytes,  get_countdown_numbers,\
    randomize_fountain_puzzle, randomize_charnel_prize_coffin
from .rom import RomData, write_patch, get_base_rom_path, CVLoDProcedurePatch, CVLOD_US_HASH
from .client import CastlevaniaLoDClient


class CVLoDSettings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the CVLoD US rom"""
        copy_to = "Castlevania - Legacy of Darkness (USA).z64"
        description = "CVLoD (USA) ROM File"
        md5s = [CVLOD_US_HASH]

    rom_file: RomFile = RomFile(RomFile.copy_to)


class CVLoDWeb(WebWorld):
    theme = "stone"

    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Archipleago Castlevania 64 randomizer on your computer and connecting it to a "
        "multiworld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Liquid Cat"]
    )]


class CVLoDWorld(World):
    """
    Castlevania: Legacy of Darkness is an expanded "director's cut" edition of Castlevania 64, featuring new characters,
    new and heavily altered stages, new bosses, and more. In addition to Reinhardt and Carrie from the prior game, you
    can now play as Cornell, a man-beast who sets out on a quest to rescue his sister, and Henry, a gun-toting knight
    tasked by the church to rescue kidnapped children.
    """
    game = "Castlevania - Legacy of Darkness"
    item_name_groups = {
        "Bomb": {iname.nitro, iname.mandragora},
        "Ingredient": {iname.nitro, iname.mandragora},
        "Crest": {iname.crest_a, iname.crest_b},
    }
    location_name_groups = {stage: set(get_locations_from_stage(stage)) for stage in vanilla_stage_order}
    options_dataclass = CVLoDOptions
    options: CVLoDOptions
    settings: typing.ClassVar[CVLoDSettings]
    topology_present = True

    item_name_to_id = get_item_names_to_ids()
    location_name_to_id = get_location_names_to_ids()

    active_stage_exits: typing.Dict[str, typing.Dict]
    active_stage_list: typing.List[str]
    active_warp_list: typing.List[str]

    # Default values to possibly be updated in generate_early
    reinhardt_stages: bool = True
    carrie_stages: bool = True
    branching_stages: bool = False
    starting_stage: str = rname.forest_of_silence
    total_s1s: int = 7
    s1s_per_warp: int = 1
    total_s2s: int = 0
    required_s2s: int = 0
    drac_condition: int = 0

    auth: bytearray

    web = CVLoDWeb()

    def generate_early(self) -> None:
        # Generate the player's unique authentication
        self.auth = bytearray(self.random.getrandbits(8) for _ in range(16))

        # If there are more S1s needed to unlock the whole warp menu than there are S1s in total, drop S1s per warp to
        # something manageable.
        #if self.s1s_per_warp * 7 > self.total_s1s:
        #    self.s1s_per_warp = self.total_s1s // 7
        #    logging.warning(f"[{self.multiworld.player_name[self.player]}] Too many required Special1s "
        #                    f"({self.options.special1s_per_warp.value * 7}) for Special1s Per Warp setting: "
        #                    f"{self.options.special1s_per_warp.value} with Total Special1s setting: "
        #                    f"{self.options.total_special1s.value}. Lowering Special1s Per Warp to: "
        #                    f"{self.s1s_per_warp}")
        #    self.options.special1s_per_warp.value = self.s1s_per_warp

        # Set the total and required Special2s to 1 if the drac condition is the Crystal, to the specified YAML numbers
        # if it's Specials, or to 0 if it's None or Bosses. The boss totals will be figured out later.
        #if self.drac_condition == DraculasCondition.option_crystal:
        #    self.total_s2s = 1
        #    self.required_s2s = 1
        #elif self.drac_condition == DraculasCondition.option_specials:
        #    self.total_s2s = self.options.total_special2s.value
        #    self.required_s2s = int(self.options.percent_special2s_required.value / 100 * self.total_s2s)

        # Enable/disable character stages and branching paths accordingly
        #if self.options.character_stages == CharacterStages.option_reinhardt_only:
        #    self.carrie_stages = False
        #elif self.options.character_stages == CharacterStages.option_carrie_only:
        #    self.reinhardt_stages = False
        #elif self.options.character_stages == CharacterStages.option_both:
        #    self.branching_stages = True

        self.active_stage_exits = get_normal_stage_exits(self)

        stage_1_blacklist = []

        # Prevent Clock Tower from being Stage 1 if more than 4 S1s are needed to warp out of it.
        if self.s1s_per_warp > 4 and not self.options.multi_hit_breakables:
            stage_1_blacklist.append(rname.clock_tower)

        # Shuffle the stages if the option is on.
        #if self.options.stage_shuffle:
        #    self.active_stage_exits, self.starting_stage, self.active_stage_list = \
        #        shuffle_stages(self, stage_1_blacklist)
        #else:
        self.active_stage_list = [stage for stage in vanilla_stage_order if stage in self.active_stage_exits]

        # Create a list of warps from the active stage list. They are in a random order by default and will never
        # include the starting stage.
        # self.active_warp_list = generate_warps(self)

    def create_regions(self) -> None:
        # Add the Menu Region.
        created_regions = [Region("Menu", self.player, self.multiworld)]

        # Add every stage Region by checking to see if that stage is active.
        created_regions.extend([Region(name, self.player, self.multiworld)
                                for name in get_region_names(self.active_stage_exits)])

        # Add the Renon's shop Region if shopsanity is on.
        #if self.options.shopsanity:
        #    created_regions.append(Region(rname.renon, self.player, self.multiworld))

        # Add the Dracula's chamber (the end) Region.
        created_regions.append(Region(rname.ck_drac_chamber, self.player, self.multiworld))

        # Set up the Regions correctly.
        self.multiworld.regions.extend(created_regions)

        # Add the warp Entrances to the Menu Region (the one always at the start of the Region list).
        # created_regions[0].add_exits(get_warp_entrances(self.active_warp_list))
        created_regions[0].add_exits({rname.fl_start: "Start stage"})

        for reg in created_regions:

            # Add the Entrances to all the Regions.
            ent_names = get_region_info(reg.name, "entrances")
            if ent_names is not None:
                reg.add_exits(verify_entrances(self.options, ent_names, self.active_stage_exits))

            # Add the Locations to all the Regions.
            loc_names = get_region_info(reg.name, "locations")
            if loc_names is None:
                continue
            verified_locs, events = verify_locations(self.options, loc_names)
            reg.add_locations(verified_locs, CVLoDLocation)

            # Place event Items on all of their associated Locations.
            for event_loc, event_item in events.items():
                self.get_location(event_loc).place_locked_item(self.create_item(event_item, "progression"))
                # If we're looking at a boss kill trophy, increment the total S2s and, if we're not already at the
                # set number of required bosses, the total required number. This way, we can prevent gen failures
                # should the player set more bosses required than there are total.
                #if event_item == iname.trophy:
                #    self.total_s2s += 1
                #    if self.required_s2s < self.options.bosses_required.value:
                #        self.required_s2s += 1

        # If Dracula's Condition is Bosses and there are less calculated required S2s than the value specified by the
        # player (meaning there weren't enough bosses to reach the player's setting), throw a warning and lower the
        # option value.
        #if self.options.draculas_condition == DraculasCondition.option_bosses and self.required_s2s < \
        #        self.options.bosses_required.value:
        #    logging.warning(f"[{self.multiworld.player_name[self.player]}] Not enough bosses for Bosses Required "
        #                    f"setting: {self.options.bosses_required.value}. Lowering to: {self.required_s2s}")
        #    self.options.bosses_required.value = self.required_s2s

    def create_item(self, name: str, force_classification=None) -> Item:
        if force_classification is not None:
            classification = getattr(ItemClassification, force_classification)
        else:
            classification = getattr(ItemClassification, get_item_info(name, "default classification"))

        code = get_item_info(name, "code")
        if code is not None:
            code += base_id

        created_item = CVLoDItem(name, classification, code, self.player)

        return created_item

    def create_items(self) -> None:
        item_counts = get_item_counts(self)

        # Set up the items correctly
        self.multiworld.itempool += [self.create_item(item, classification) for classification in item_counts for item
                                     in item_counts[classification] for _ in range(item_counts[classification][item])]

    def set_rules(self) -> None:
        # Set all the Entrance rules properly.
        CVLoDRules(self).set_cvlod_rules()

    def generate_output(self, output_directory: str) -> None:
        active_locations = self.multiworld.get_locations(self.player)

        # Location data and shop names, descriptions, and colors
        offset_data, shop_name_list, shop_colors_list, shop_desc_list = \
            get_location_data(self, active_locations)
        # Shop prices
        #if self.options.shop_prices:
        #    offset_data.update(randomize_shop_prices(self))
        # Map lighting
        #if self.options.map_lighting:
        #    offset_data.update(randomize_lighting(self))
        # Sub-weapons
        if self.options.sub_weapon_shuffle == SubWeaponShuffle.option_own_pool:
            offset_data.update(shuffle_sub_weapons(self))
        # Music
        #if self.options.background_music:
        #    offset_data.update(randomize_music(self))
        # Loading zones
        # offset_data.update(get_loading_zone_bytes(self.options, self.starting_stage, self.active_stage_exits))
        # Countdown
        if self.options.countdown:
            offset_data.update(get_countdown_numbers(self.options, active_locations))
        # Start Inventory
        offset_data.update(get_start_inventory_data(self.player, self.options,
                                                    self.multiworld.precollected_items[self.player]))
        # Forest Charnel prize coffin
        offset_data.update(randomize_charnel_prize_coffin(self))
        # Villa fountain puzzle
        offset_data.update(randomize_fountain_puzzle(self))

        patch = CVLoDProcedurePatch(player=self.player, player_name=self.multiworld.player_name[self.player])
        write_patch(self, patch, offset_data, shop_name_list, shop_desc_list, shop_colors_list, active_locations)

        rom_path = os.path.join(output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}"
                                                  f"{patch.patch_file_ending}")

        patch.write(rom_path)

    def get_filler_item_name(self) -> str:
        return self.random.choice(filler_item_names)

    #def extend_hint_information(self, hint_data: typing.Dict[int, typing.Dict[int, str]]):
        # Attach each location's stage's position to its hint information if Stage Shuffle is on.
    #    if not self.options.stage_shuffle:
    #        return

    #    stage_pos_data = {}
    #    for loc in list(self.multiworld.get_locations(self.player)):
    #        stage = get_region_info(loc.parent_region.name, "stage")
    #        if stage is not None and loc.address is not None:
    #            num = str(self.active_stage_exits[stage]["position"]).zfill(2)
    #            path = self.active_stage_exits[stage]["path"]
    #            stage_pos_data[loc.address] = f"Stage {num}"
    #            if path != " ":
    #                stage_pos_data[loc.address] += path
    #    hint_data[self.player] = stage_pos_data

    def modify_multidata(self, multidata: typing.Dict[str, typing.Any]):
        # Put the player's unique authentication in connect_names.
        multidata["connect_names"][base64.b64encode(self.auth).decode("ascii")] = \
            multidata["connect_names"][self.multiworld.player_name[self.player]]

    #def write_spoiler(self, spoiler_handle: typing.TextIO) -> None:
        # Write the stage order to the spoiler log
    #    spoiler_handle.write(f"\nCastlevania 64 stage & warp orders for {self.multiworld.player_name[self.player]}:\n")
    #    for stage in self.active_stage_list:
    #        num = str(self.active_stage_exits[stage]["position"]).zfill(2)
    #        path = self.active_stage_exits[stage]["path"]
    #        spoiler_handle.writelines(f"Stage {num}{path}:\t{stage}\n")

        # Write the warp order to the spoiler log
    #    spoiler_handle.writelines(f"\nStart :\t{self.active_stage_list[0]}\n")
    #    for i in range(1, len(self.active_warp_list)):
    #        spoiler_handle.writelines(f"Warp {i}:\t{self.active_warp_list[i]}\n")
