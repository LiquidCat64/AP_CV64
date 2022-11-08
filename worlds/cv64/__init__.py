import os
import typing
# import math
import threading

from BaseClasses import Item, MultiWorld, Tutorial, ItemClassification
from .Items import CV64Item, ItemData, item_table, junk_table
from .Locations import CV64Location, all_locations, setup_locations
from .Options import cv64_options
from .Regions import create_regions, connect_regions
from .Levels import level_list
from .Rules import set_rules
from .Names import ItemName, LocationName
from ..AutoWorld import WebWorld, World
from .Rom import LocalRom, patch_rom, get_base_rom_path, CV64DeltaPatch, rom_item_bytes
# import math


class CV64Web(WebWorld):
    theme = "stone"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Castlevania 64 randomizer connected to an Archipelago Multiworld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Liquid Cat"]
    )

    tutorials = "Insert setup webpage here"


class CV64World(World):
    """
    Castlevania for the Nintendo 64 is the first 3D game in the franchise. As either whip-wielding Belmont descendant
    Reinhardt Schneider or powerful sorceress Carrie Fernandez, brave many terrifying traps and foes as you make your
    way to Dracula's chamber and stop his rule of terror.
    """
    game: str = "Castlevania 64"
    option_definitions = cv64_options
    topology_present = False
    data_version = 0
    # hint_blacklist = {}
    remote_items = False

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = all_locations

    active_level_list: typing.List[str]
    villa_cc_ids = [2, 3]
    active_warp_list: typing.List[str]
    web = CV64Web()

    def __init__(self, world: MultiWorld, player: int):
        self.rom_name_available_event = threading.Event()
        super().__init__(world, player)

    @classmethod
    def stage_assert_generate(cls, world):
        rom_file = get_base_rom_path()
        if not os.path.exists(rom_file):
            raise FileNotFoundError(rom_file)

    def _get_slot_data(self):
        return {
            "death_link": self.multiworld.death_link[self.player].value,
            "active_levels": self.active_level_list,
            "active_warps": self.active_warp_list
        }

    def create_regions(self):
        location_table = setup_locations(self.multiworld, self.player)
        create_regions(self.multiworld, self.player, location_table)

    def create_item(self, name: str, force_non_progression=False) -> Item:
        data = item_table[name]

        if force_non_progression:
            classification = ItemClassification.filler
        elif data.progression:
            classification = ItemClassification.progression
        else:
            classification = ItemClassification.filler

        created_item = CV64Item(name, classification, data.code, self.player)
        if name in rom_item_bytes:
            created_item.item_byte = rom_item_bytes[name]

        return created_item

    def lookup_table(self):
        pass

    def _create_items(self, name: str):
        data = item_table[name]
        return [self.create_item(name)] * data.quantity

    def set_rules(self):
        set_rules(self.multiworld, self.player)

    def generate_basic(self):
        itempool: typing.List[CV64Item] = []

        # Levels
        total_required_locations = 212

        # number_of_specials = 0
        self.multiworld.get_location(LocationName.the_end, self.player).place_locked_item(self.create_item(ItemName.victory))

        self.multiworld.get_location(LocationName.forest_boss_one, self.player)\
            .place_locked_item(self.create_item(ItemName.bone_mom_one))
        self.multiworld.get_location(LocationName.forest_boss_two, self.player)\
            .place_locked_item(self.create_item(ItemName.forest_weretiger))
        self.multiworld.get_location(LocationName.forest_boss_three, self.player)\
            .place_locked_item(self.create_item(ItemName.bone_mom_two))
        self.multiworld.get_location(LocationName.cw_boss, self.player)\
            .place_locked_item(self.create_item(ItemName.w_dragons))
        self.multiworld.get_location(LocationName.villa_boss, self.player)\
            .place_locked_item(self.create_item(ItemName.vamp_couple))
        self.multiworld.get_location(LocationName.cc_boss_one, self.player)\
            .place_locked_item(self.create_item(ItemName.behemoth))
        self.multiworld.get_location(LocationName.cc_boss_two, self.player)\
            .place_locked_item(self.create_item(ItemName.rosamilla))
        self.multiworld.get_location(LocationName.dt_boss_one, self.player)\
            .place_locked_item(self.create_item(ItemName.werejaguar))
        self.multiworld.get_location(LocationName.dt_boss_two, self.player)\
            .place_locked_item(self.create_item(ItemName.werewolf))
        self.multiworld.get_location(LocationName.dt_boss_three, self.player)\
            .place_locked_item(self.create_item(ItemName.werebull))
        self.multiworld.get_location(LocationName.dt_boss_four, self.player)\
            .place_locked_item(self.create_item(ItemName.weretiger))
        self.multiworld.get_location(LocationName.roc_boss, self.player)\
            .place_locked_item(self.create_item(ItemName.deathtrice))

        number_of_special1s = self.multiworld.total_special1s[self.player].value
        number_of_special2s = self.multiworld.total_special2s[self.player].value

        itempool += [self.create_item(ItemName.special_one) for _ in range(number_of_special1s)]
        itempool += [self.create_item(ItemName.roast_chicken) for _ in range(21)]
        itempool += [self.create_item(ItemName.roast_beef) for _ in range(24)]
        itempool += [self.create_item(ItemName.healing_kit) for _ in range(4)]
        itempool += [self.create_item(ItemName.purifying) for _ in range(14)]
        itempool += [self.create_item(ItemName.cure_ampoule) for _ in range(5)]
        itempool += [self.create_item(ItemName.powerup) for _ in range(10)]
        itempool += [self.create_item(ItemName.magical_nitro) for _ in range(2)]
        itempool += [self.create_item(ItemName.mandragora) for _ in range(2)]
        itempool += [self.create_item(ItemName.sun_card) for _ in range(9)]
        itempool += [self.create_item(ItemName.moon_card) for _ in range(8)]
        itempool += [self.create_item(ItemName.left_tower_key)]
        itempool += [self.create_item(ItemName.storeroom_key)]
        itempool += [self.create_item(ItemName.archives_key)]
        itempool += [self.create_item(ItemName.garden_key)]
        itempool += [self.create_item(ItemName.copper_key)]
        itempool += [self.create_item(ItemName.chamber_key)]
        itempool += [self.create_item(ItemName.execution_key)]
        itempool += [self.create_item(ItemName.science_key_one)]
        itempool += [self.create_item(ItemName.science_key_two)]
        itempool += [self.create_item(ItemName.science_key_three)]
        itempool += [self.create_item(ItemName.clocktower_key_one)]
        itempool += [self.create_item(ItemName.clocktower_key_two)]
        itempool += [self.create_item(ItemName.clocktower_key_three)]

        if self.multiworld.draculas_condition[self.player].value == 3:
            itempool += [self.create_item(ItemName.special_two) for _ in range(number_of_special2s)]

        if self.multiworld.carrie_logic[self.player]:
            itempool += [self.create_item(ItemName.roast_beef)]
            itempool += [self.create_item(ItemName.moon_card)]
            total_required_locations += 2

        if self.multiworld.lizard_generator_items[self.player]:
            itempool += [self.create_item(ItemName.powerup)]
            itempool += [self.create_item(ItemName.sun_card)]
            total_required_locations += 6

        total_junk_count = total_required_locations - len(itempool)

        junk_pool = []
        for item_name in self.multiworld.random.choices(list(junk_table.keys()), k=total_junk_count):
            junk_pool += [self.create_item(item_name)]

        itempool += junk_pool

        self.active_level_list = level_list.copy()
        self.active_warp_list = self.multiworld.random.sample(self.active_level_list, 7)

        if self.multiworld.stage_shuffle[self.player]:
            self.active_level_list.remove(LocationName.villa)
            self.active_level_list.remove(LocationName.castle_center)
            self.active_level_list.remove(LocationName.castle_keep)
            self.multiworld.random.shuffle(self.active_level_list)
            self.villa_cc_ids = self.multiworld.random.sample(range(0, 6), 2)
            if self.villa_cc_ids[0] < self.villa_cc_ids[1]:
                self.active_level_list.insert(self.villa_cc_ids[0], LocationName.villa)
                self.active_level_list.insert(self.villa_cc_ids[1] + 2, LocationName.castle_center)
            else:
                self.active_level_list.insert(self.villa_cc_ids[1], LocationName.castle_center)
                self.active_level_list.insert(self.villa_cc_ids[0] + 4, LocationName.villa)
            self.active_level_list.append(LocationName.castle_keep)

        if self.multiworld.warp_shuffle[self.player].value == 0:
            new_list = self.active_level_list.copy()
            for warp in self.active_level_list:
                if warp not in self.active_warp_list:
                    new_list.remove(warp)
            self.active_warp_list = new_list
        elif self.multiworld.warp_shuffle[self.player].value == 2:
            new_list = level_list.copy()
            for warp in level_list:
                if warp not in self.active_warp_list:
                    new_list.remove(warp)
            self.active_warp_list = new_list

        connect_regions(self.multiworld, self.player, self.active_level_list, self.active_warp_list)

        self.multiworld.itempool += itempool

    def generate_output(self, output_directory: str):
        try:
            world = self.multiworld
            player = self.player

            rom = LocalRom(get_base_rom_path())

            offsets_to_ids = {}
            for location_name in self.location_name_to_id:
                loc = self.multiworld.get_location(location_name, self.player)
                if loc.item.name in rom_item_bytes or loc.item.game != "Castlevania 64":
                    if loc.item.player == self.player:
                        offsets_to_ids[loc.rom_offset] = loc.item.item_byte
                        if loc.loc_type == "npc":
                            if 0x19 < offsets_to_ids[loc.rom_offset] < 0x1D:
                                offsets_to_ids[loc.rom_offset] += 0x0D
                            elif offsets_to_ids[loc.rom_offset] > 0x1C:
                                offsets_to_ids[loc.rom_offset] -= 0x03
                    else:
                        if loc.item.classification == ItemClassification.progression:
                            offsets_to_ids[loc.rom_offset] = 0x11
                        else:
                            offsets_to_ids[loc.rom_offset] = 0x12

            patch_rom(self.multiworld, rom, self.player, offsets_to_ids, self.active_level_list, self.active_warp_list)

            outfilepname = f'_P{player}'
            outfilepname += f"_{world.player_name[player].replace(' ', '_')}" \
                if world.player_name[player] != 'Player%d' % player else ''

            rompath = os.path.join(output_directory, f'AP_{world.seed_name}{outfilepname}.sfc')
            rom.write_to_file(rompath)
            self.rom_name = rom.name

            patch = CV64DeltaPatch(os.path.splitext(rompath)[0]+CV64DeltaPatch.patch_file_ending, player=player,
                                   player_name=world.player_name[player], patched_path=rompath)
            patch.write()
        except:
            raise
        finally:
            if os.path.exists(rompath):
                os.unlink(rompath)
            self.rom_name_available_event.set()  # make sure threading continues and errors are collected

    def write_spoiler(self, spoiler_handle: typing.TextIO):
        stagecounts = {"Main": 1, "Reinhardt": 1, "Carrie": 1}
        spoiler_handle.write("\n")
        header_text = "Castlevania 64 stage order:\n"
        header_text = header_text.format(self.multiworld.player_name[self.player])
        spoiler_handle.write(header_text)
        for x in range(len(self.active_level_list)):
            if self.active_level_list[x - 1] == LocationName.villa or self.active_level_list[x - 1] \
                    == LocationName.castle_center or self.active_level_list[x - 2] == LocationName.castle_center:
                stagetype = "Reinhardt"
            elif self.active_level_list[x - 2] == LocationName.villa or self.active_level_list[x - 3] \
                    == LocationName.castle_center or self.active_level_list[x - 4] == LocationName.castle_center:
                stagetype = "Carrie"
            else:
                stagetype = "Main"

            if stagetype == "Reinhardt":
                text = "{0} Stage {1}:\t{2}\n"
            else:
                text = "{0} Stage {1}:\t\t{2}\n"
            text = text.format(stagetype, stagecounts[stagetype], self.active_level_list[x])
            spoiler_handle.writelines(text)
            stagecounts[stagetype] += 1

        spoiler_handle.writelines("\nStart Warp:\t" + self.active_level_list[0])
        for x in range(len(self.active_warp_list)):
            text = "\nWarp {0}:\t{1}"
            text = text.format(x + 1, self.active_warp_list[x])
            spoiler_handle.writelines(text)

    def fill_slot_data(self) -> dict:
        slot_data = self._get_slot_data()
        for option_name in cv64_options:
            option = getattr(self.multiworld, option_name)[self.player]
            slot_data[option_name] = option.value

        return slot_data

    def modify_multidata(self, multidata: dict):
        import base64
        # wait for self.rom_name to be available.
        self.rom_name_available_event.wait()
        rom_name = getattr(self, "rom_name", None)
        # we skip in case of error, so that the original error in the output thread is the one that gets raised
        if rom_name:
            new_name = base64.b64encode(bytes(self.rom_name)).decode()
            multidata["connect_names"][new_name] = multidata["connect_names"][self.multiworld.player_name[self.player]]
