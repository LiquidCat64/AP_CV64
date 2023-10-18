"""
Parses the WitnessLogic.txt logic file into useful data structures.
This is the heart of the randomization.

In WitnessLogic.txt we have regions defined with their connections:

Region Name (Short name) - Connected Region 1 - Connection Requirement 1 - Connected Region 2...

And then panels in that region with the hex code used in the game
previous panels that are required to turn them on, as well as the symbols they require:

0x##### (Panel Name) - Required Panels - Required Items

On __init__, the base logic is read and all panels are given Location IDs.
When the world has parsed its options, a second function is called to finalize the logic.
"""

import copy
from typing import cast
from logging import warning

from worlds.AutoWorld import World
from .static_logic import StaticWitnessLogic, DoorItemDefinition, ItemCategory, ProgressiveItemDefinition
from .utils import *
from .Options import is_option_enabled, get_option_value, the_witness_options


class WitnessPlayerLogic:
    """WITNESS LOGIC CLASS"""

    def reduce_req_within_region(self, panel_hex: str):
        """
        Panels in this game often only turn on when other panels are solved.
        Those other panels may have different item requirements.
        It would be slow to recursively check solvability each time.
        This is why we reduce the item dependencies within the region.
        Panels outside of the same region will still be checked manually.
        """

        if panel_hex in self.COMPLETELY_DISABLED_ENTITIES or panel_hex in self.IRRELEVANT_BUT_NOT_DISABLED_ENTITIES:
            return frozenset()

        check_obj = self.REFERENCE_LOGIC.ENTITIES_BY_HEX[panel_hex]

        these_items = frozenset({frozenset()})

        if check_obj["id"]:
            these_items = self.DEPENDENT_REQUIREMENTS_BY_HEX[panel_hex]["items"]

        these_items = frozenset({
            subset.intersection(self.THEORETICAL_ITEMS_NO_MULTI)
            for subset in these_items
        })

        for subset in these_items:
            self.PROG_ITEMS_ACTUALLY_IN_THE_GAME_NO_MULTI.update(subset)

        these_panels = self.DEPENDENT_REQUIREMENTS_BY_HEX[panel_hex]["panels"]

        if panel_hex in self.DOOR_ITEMS_BY_ID:
            door_items = frozenset({frozenset([item]) for item in self.DOOR_ITEMS_BY_ID[panel_hex]})

            all_options = set()

            for dependentItem in door_items:
                self.PROG_ITEMS_ACTUALLY_IN_THE_GAME_NO_MULTI.update(dependentItem)
                for items_option in these_items:
                    all_options.add(items_option.union(dependentItem))

            # 0x28A0D depends on another entity for *non-power* reasons -> This dependency needs to be preserved...
            if panel_hex != "0x28A0D":
                return frozenset(all_options)
            # ...except in Expert, where that dependency doesn't exist, but now there *is* a power dependency.
            # In the future, it would be wise to make a distinction between "power dependencies" and other dependencies.
            if any("0x28998" in option for option in these_panels):
                return frozenset(all_options)

            these_items = all_options

        disabled_eps = {eHex for eHex in self.COMPLETELY_DISABLED_ENTITIES
                        if StaticWitnessLogic.ENTITIES_BY_HEX[eHex]["entityType"] == "EP"}

        these_panels = frozenset({panels - disabled_eps
                                  for panels in these_panels})

        if these_panels == frozenset({frozenset()}):
            return these_items

        all_options = set()

        for option in these_panels:
            dependent_items_for_option = frozenset({frozenset()})

            for option_panel in option:
                dep_obj = self.REFERENCE_LOGIC.ENTITIES_BY_HEX.get(option_panel)

                if option_panel in self.COMPLETELY_DISABLED_ENTITIES:
                    new_items = frozenset()
                elif option_panel in {"7 Lasers", "11 Lasers", "PP2 Weirdness", "Theater to Tunnels"}:
                    new_items = frozenset({frozenset([option_panel])})
                # If a panel turns on when a panel in a different region turns on,
                # the latter panel will be an "event panel", unless it ends up being
                # a location itself. This prevents generation failures.
                elif dep_obj["region"]["name"] != check_obj["region"]["name"]:
                    new_items = frozenset({frozenset([option_panel])})
                    self.EVENT_PANELS_FROM_PANELS.add(option_panel)
                elif option_panel in self.ALWAYS_EVENT_NAMES_BY_HEX.keys():
                    new_items = frozenset({frozenset([option_panel])})
                    self.EVENT_PANELS_FROM_PANELS.add(option_panel)
                else:
                    new_items = self.reduce_req_within_region(option_panel)

                updated_items = set()

                for items_option in dependent_items_for_option:
                    for items_option2 in new_items:
                        updated_items.add(items_option.union(items_option2))

                dependent_items_for_option = updated_items

            for items_option in these_items:
                for dependentItem in dependent_items_for_option:
                    all_options.add(items_option.union(dependentItem))

        return frozenset(all_options)

    def make_single_adjustment(self, adj_type: str, line: str):
        from . import StaticWitnessItems
        """Makes a single logic adjustment based on additional logic file"""

        if adj_type == "Items":
            line_split = line.split(" - ")
            item_name = line_split[0]

            if item_name not in StaticWitnessItems.item_data:
                raise RuntimeError("Item \"" + item_name + "\" does not exist.")

            self.THEORETICAL_ITEMS.add(item_name)
            if isinstance(StaticWitnessLogic.all_items[item_name], ProgressiveItemDefinition):
                self.THEORETICAL_ITEMS_NO_MULTI.update(cast(ProgressiveItemDefinition,
                                                            StaticWitnessLogic.all_items[item_name]).child_item_names)
            else:
                self.THEORETICAL_ITEMS_NO_MULTI.add(item_name)

            if StaticWitnessLogic.all_items[item_name].category in [ItemCategory.DOOR, ItemCategory.LASER]:
                panel_hexes = cast(DoorItemDefinition, StaticWitnessLogic.all_items[item_name]).panel_id_hexes
                for panel_hex in panel_hexes:
                    self.DOOR_ITEMS_BY_ID.setdefault(panel_hex, []).append(item_name)

            return

        if adj_type == "Remove Items":
            item_name = line

            self.THEORETICAL_ITEMS.discard(item_name)
            if isinstance(StaticWitnessLogic.all_items[item_name], ProgressiveItemDefinition):
                self.THEORETICAL_ITEMS_NO_MULTI\
                    .difference_update(cast(ProgressiveItemDefinition,
                                            StaticWitnessLogic.all_items[item_name]).child_item_names)
            else:
                self.THEORETICAL_ITEMS_NO_MULTI.discard(item_name)

            if StaticWitnessLogic.all_items[item_name].category in [ItemCategory.DOOR, ItemCategory.LASER]:
                panel_hexes = cast(DoorItemDefinition, StaticWitnessLogic.all_items[item_name]).panel_id_hexes
                for panel_hex in panel_hexes:
                    if panel_hex in self.DOOR_ITEMS_BY_ID and item_name in self.DOOR_ITEMS_BY_ID[panel_hex]:
                        self.DOOR_ITEMS_BY_ID[panel_hex].remove(item_name)

        if adj_type == "Starting Inventory":
            self.STARTING_INVENTORY.add(line)

        if adj_type == "Event Items":
            line_split = line.split(" - ")
            hex_set = line_split[1].split(",")

            for hex_code in hex_set:
                self.ALWAYS_EVENT_NAMES_BY_HEX[hex_code] = line_split[0]

            to_remove = set()

            for hex_code, event_name in self.ALWAYS_EVENT_NAMES_BY_HEX.items():
                if hex_code not in hex_set and event_name == line_split[0]:
                    to_remove.add(hex_code)

            for remove in to_remove:
                del self.ALWAYS_EVENT_NAMES_BY_HEX[remove]

            return

        if adj_type == "Requirement Changes":
            line_split = line.split(" - ")

            requirement = {
                "panels": parse_lambda(line_split[1]),
            }

            if len(line_split) > 2:
                required_items = parse_lambda(line_split[2])
                items_actually_in_the_game = [item_name for item_name, item_definition
                                              in StaticWitnessLogic.all_items.items()
                                              if item_definition.category is ItemCategory.SYMBOL]
                required_items = frozenset(
                    subset.intersection(items_actually_in_the_game)
                    for subset in required_items
                )

                requirement["items"] = required_items

            self.DEPENDENT_REQUIREMENTS_BY_HEX[line_split[0]] = requirement

            return

        if adj_type == "Disabled Locations":
            panel_hex = line[:7]

            self.COMPLETELY_DISABLED_ENTITIES.add(panel_hex)

            return

        if adj_type == "Irrelevant Locations":
            panel_hex = line[:7]

            self.IRRELEVANT_BUT_NOT_DISABLED_ENTITIES.add(panel_hex)

            return

        if adj_type == "Region Changes":
            new_region_and_options = define_new_region(line + ":")
            
            self.CONNECTIONS_BY_REGION_NAME[new_region_and_options[0]["name"]] = new_region_and_options[1]

            return

        if adj_type == "New Connections":
            line_split = line.split(" - ")
            source_region = line_split[0]
            target_region = line_split[1]
            panel_set_string = line_split[2]

            for connection in self.CONNECTIONS_BY_REGION_NAME[source_region]:
                if connection[0] == target_region:
                    self.CONNECTIONS_BY_REGION_NAME[source_region].remove(connection)

                    if panel_set_string == "TrueOneWay":
                        self.CONNECTIONS_BY_REGION_NAME[source_region].add(
                            (target_region, frozenset({frozenset(["TrueOneWay"])}))
                        )
                    else:
                        new_lambda = connection[1] | parse_lambda(panel_set_string)
                        self.CONNECTIONS_BY_REGION_NAME[source_region].add((target_region, new_lambda))
                    break
            else:  # Execute if loop did not break. TIL this is a thing you can do!
                new_conn = (target_region, parse_lambda(panel_set_string))
                self.CONNECTIONS_BY_REGION_NAME[source_region].add(new_conn)

        if adj_type == "Added Locations":
            if "0x" in line:
                line = StaticWitnessLogic.ENTITIES_BY_HEX[line]["checkName"]
            self.ADDED_CHECKS.add(line)

    def make_options_adjustments(self, world: World):
        """Makes logic adjustments based on options"""
        adjustment_linesets_in_order = []

        # Postgame

        doors = get_option_value(world, "shuffle_doors") >= 2
        lasers = is_option_enabled(world, "shuffle_lasers")
        early_caves = get_option_value(world, "early_caves") > 0
        victory = get_option_value(world, "victory_condition")
        mnt_lasers = get_option_value(world, "mountain_lasers")
        chal_lasers = get_option_value(world, "challenge_lasers")

        mountain_enterable_from_top = victory == 0 or victory == 1 or (victory == 3 and chal_lasers > mnt_lasers)

        if not is_option_enabled(world, "shuffle_postgame"):
            if not (early_caves or doors):
                adjustment_linesets_in_order.append(get_caves_exclusion_list())
                if not victory == 1:
                    adjustment_linesets_in_order.append(get_path_to_challenge_exclusion_list())
                    adjustment_linesets_in_order.append(get_challenge_vault_box_exclusion_list())
                    adjustment_linesets_in_order.append(get_beyond_challenge_exclusion_list())

            if not ((doors or early_caves) and (victory == 0 or (victory == 2 and mnt_lasers > chal_lasers))):
                adjustment_linesets_in_order.append(get_beyond_challenge_exclusion_list())
                if not victory == 1:
                    adjustment_linesets_in_order.append(get_challenge_vault_box_exclusion_list())

            if not(doors or mountain_enterable_from_top):
                adjustment_linesets_in_order.append(get_mountain_lower_exclusion_list())

            if not mountain_enterable_from_top:
                adjustment_linesets_in_order.append(get_mountain_upper_exclusion_list())

            if not ((victory == 0 and doors) or victory == 1 or (victory == 2 and mnt_lasers > chal_lasers and doors)):
                if doors:
                    adjustment_linesets_in_order.append(get_bottom_floor_discard_exclusion_list())
                else:
                    adjustment_linesets_in_order.append(get_bottom_floor_discard_nondoors_exclusion_list())

        # Exclude Discards / Vaults

        if not is_option_enabled(world, "shuffle_discarded_panels"):
            # In disable_non_randomized, the discards are needed for alternate activation triggers, UNLESS both
            # (remote) doors and lasers are shuffled.
            if not is_option_enabled(world, "disable_non_randomized_puzzles") or (doors and lasers):
                adjustment_linesets_in_order.append(get_discard_exclusion_list())

            if doors:
                adjustment_linesets_in_order.append(get_bottom_floor_discard_exclusion_list())

        if not is_option_enabled(world, "shuffle_vault_boxes"):
            adjustment_linesets_in_order.append(get_vault_exclusion_list())
            if not victory == 1:
                adjustment_linesets_in_order.append(get_challenge_vault_box_exclusion_list())

        # Victory Condition

        if get_option_value(world, "victory_condition") == 0:
            self.VICTORY_LOCATION = "0x3D9A9"
        elif get_option_value(world, "victory_condition") == 1:
            self.VICTORY_LOCATION = "0x0356B"
        elif get_option_value(world, "victory_condition") == 2:
            self.VICTORY_LOCATION = "0x09F7F"
        elif get_option_value(world, "victory_condition") == 3:
            self.VICTORY_LOCATION = "0xFFF00"

        if get_option_value(world, "challenge_lasers") <= 7:
            adjustment_linesets_in_order.append([
                "Requirement Changes:",
                "0xFFF00 - 11 Lasers - True",
            ])

        if is_option_enabled(world, "disable_non_randomized_puzzles"):
            adjustment_linesets_in_order.append(get_disable_unrandomized_list())

        if is_option_enabled(world, "shuffle_symbols") or "shuffle_symbols" not in the_witness_options.keys():
            adjustment_linesets_in_order.append(get_symbol_shuffle_list())

        if get_option_value(world, "EP_difficulty") == 0:
            adjustment_linesets_in_order.append(get_ep_easy())
        elif get_option_value(world, "EP_difficulty") == 1:
            adjustment_linesets_in_order.append(get_ep_no_eclipse())

        if get_option_value(world, "door_groupings") == 1:
            if get_option_value(world, "shuffle_doors") == 1:
                adjustment_linesets_in_order.append(get_simple_panels())
            elif get_option_value(world, "shuffle_doors") == 2:
                adjustment_linesets_in_order.append(get_simple_doors())
            elif get_option_value(world, "shuffle_doors") == 3:
                adjustment_linesets_in_order.append(get_simple_doors())
                adjustment_linesets_in_order.append(get_simple_additional_panels())
        else:
            if get_option_value(world, "shuffle_doors") == 1:
                adjustment_linesets_in_order.append(get_complex_door_panels())
                adjustment_linesets_in_order.append(get_complex_additional_panels())
            elif get_option_value(world, "shuffle_doors") == 2:
                adjustment_linesets_in_order.append(get_complex_doors())
            elif get_option_value(world, "shuffle_doors") == 3:
                adjustment_linesets_in_order.append(get_complex_doors())
                adjustment_linesets_in_order.append(get_complex_additional_panels())

        if is_option_enabled(world, "shuffle_boat"):
            adjustment_linesets_in_order.append(get_boat())

        if get_option_value(world, "early_caves") == 2:
            adjustment_linesets_in_order.append(get_early_caves_start_list())

        if get_option_value(world, "early_caves") == 1 and not doors:
            adjustment_linesets_in_order.append(get_early_caves_list())

        if is_option_enabled(world, "elevators_come_to_you"):
            adjustment_linesets_in_order.append(get_elevators_come_to_you())

        for item in self.YAML_ADDED_ITEMS:
            adjustment_linesets_in_order.append(["Items:", item])

        if is_option_enabled(world, "shuffle_lasers"):
            adjustment_linesets_in_order.append(get_laser_shuffle())

        if get_option_value(world, "shuffle_EPs") != 2:
            adjustment_linesets_in_order.append(["Disabled Locations:"] + get_ep_obelisks()[1:])

        if get_option_value(world, "shuffle_EPs") == 0:
            adjustment_linesets_in_order.append(["Irrelevant Locations:"] + get_ep_all_individual()[1:])

        yaml_disabled_eps = []

        for yaml_disabled_location in self.YAML_DISABLED_LOCATIONS:
            if yaml_disabled_location not in StaticWitnessLogic.ENTITIES_BY_NAME:
                continue

            loc_obj = StaticWitnessLogic.ENTITIES_BY_NAME[yaml_disabled_location]

            if loc_obj["entityType"] == "EP" and get_option_value(world, "shuffle_EPs") != 0:
                yaml_disabled_eps.append(loc_obj["checkHex"])

            if loc_obj["entityType"] in {"EP", "General", "Vault", "Discard"}:
                self.EXCLUDED_LOCATIONS.add(loc_obj["checkHex"])

        adjustment_linesets_in_order.append(["Disabled Locations:"] + yaml_disabled_eps)

        for adjustment_lineset in adjustment_linesets_in_order:
            current_adjustment_type = None

            for line in adjustment_lineset:
                if len(line) == 0:
                    continue

                if line[-1] == ":":
                    current_adjustment_type = line[:-1]
                    continue

                self.make_single_adjustment(current_adjustment_type, line)

        for entity_id in self.COMPLETELY_DISABLED_ENTITIES:
            if entity_id in self.DOOR_ITEMS_BY_ID:
                del self.DOOR_ITEMS_BY_ID[entity_id]

    def make_dependency_reduced_checklist(self):
        """
        Turns dependent check set into semi-independent check set
        """

        for check_hex in self.DEPENDENT_REQUIREMENTS_BY_HEX.keys():
            indep_requirement = self.reduce_req_within_region(check_hex)

            self.REQUIREMENTS_BY_HEX[check_hex] = indep_requirement

        for item in self.PROG_ITEMS_ACTUALLY_IN_THE_GAME_NO_MULTI:
            if item not in self.THEORETICAL_ITEMS:
                progressive_item_name = StaticWitnessLogic.get_parent_progressive_item(item)
                self.PROG_ITEMS_ACTUALLY_IN_THE_GAME.add(progressive_item_name)
                child_items = cast(ProgressiveItemDefinition,
                                   StaticWitnessLogic.all_items[progressive_item_name]).child_item_names
                multi_list = [child_item for child_item in child_items
                              if child_item in self.PROG_ITEMS_ACTUALLY_IN_THE_GAME_NO_MULTI]
                self.MULTI_AMOUNTS[item] = multi_list.index(item) + 1
                self.MULTI_LISTS[progressive_item_name] = multi_list
            else:
                self.PROG_ITEMS_ACTUALLY_IN_THE_GAME.add(item)

    def make_event_item_pair(self, panel: str):
        """
        Makes a pair of an event panel and its event item
        """
        action = " Opened" if StaticWitnessLogic.ENTITIES_BY_HEX[panel]["entityType"] == "Door" else " Solved"

        name = StaticWitnessLogic.ENTITIES_BY_HEX[panel]["checkName"] + action
        if panel not in self.EVENT_ITEM_NAMES:
            if StaticWitnessLogic.ENTITIES_BY_HEX[panel]["entityType"] == "EP":
                obelisk = StaticWitnessLogic.ENTITIES_BY_HEX[StaticWitnessLogic.EP_TO_OBELISK_SIDE[panel]]["checkName"]

                self.EVENT_ITEM_NAMES[panel] = obelisk + " - " + StaticWitnessLogic.ENTITIES_BY_HEX[panel]["checkName"]

            else:
                warning("Panel \"" + name + "\" does not have an associated event name.")
                self.EVENT_ITEM_NAMES[panel] = name + " Event"
        pair = (name, self.EVENT_ITEM_NAMES[panel])
        return pair

    def make_event_panel_lists(self):
        """
        Special event panel data structures
        """

        self.ALWAYS_EVENT_NAMES_BY_HEX[self.VICTORY_LOCATION] = "Victory"

        for region_name, connections in self.CONNECTIONS_BY_REGION_NAME.items():
            for connection in connections:
                for panel_req in connection[1]:
                    for panel in panel_req:
                        if panel == "TrueOneWay":
                            continue

                        if self.REFERENCE_LOGIC.ENTITIES_BY_HEX[panel]["region"]["name"] != region_name:
                            if panel not in self.COMPLETELY_DISABLED_ENTITIES:
                                self.EVENT_PANELS_FROM_REGIONS.add(panel)

        self.EVENT_PANELS.update(self.EVENT_PANELS_FROM_PANELS)
        self.EVENT_PANELS.update(self.EVENT_PANELS_FROM_REGIONS)

        self.EVENT_PANELS -= self.COMPLETELY_DISABLED_ENTITIES

        for always_hex, always_item in self.ALWAYS_EVENT_NAMES_BY_HEX.items():
            if always_hex in self.COMPLETELY_DISABLED_ENTITIES:
                continue
            self.ALWAYS_EVENT_HEX_CODES.add(always_hex)
            self.EVENT_PANELS.add(always_hex)
            self.EVENT_ITEM_NAMES[always_hex] = always_item

        for panel in self.EVENT_PANELS:
            pair = self.make_event_item_pair(panel)
            self.EVENT_ITEM_PAIRS[pair[0]] = pair[1]

    def __init__(self, world: World, disabled_locations: Set[str], start_inv: Dict[str, int]):
        self.YAML_DISABLED_LOCATIONS = disabled_locations
        self.YAML_ADDED_ITEMS = start_inv

        self.EVENT_PANELS_FROM_PANELS = set()
        self.EVENT_PANELS_FROM_REGIONS = set()

        self.IRRELEVANT_BUT_NOT_DISABLED_ENTITIES = set()

        self.THEORETICAL_ITEMS = set()
        self.THEORETICAL_ITEMS_NO_MULTI = set()
        self.MULTI_AMOUNTS = dict()
        self.MULTI_LISTS = dict()
        self.PROG_ITEMS_ACTUALLY_IN_THE_GAME_NO_MULTI = set()
        self.PROG_ITEMS_ACTUALLY_IN_THE_GAME = set()
        self.DOOR_ITEMS_BY_ID: Dict[str, List[str]] = {}
        self.STARTING_INVENTORY = set()

        self.DIFFICULTY = get_option_value(world, "puzzle_randomization")

        if self.DIFFICULTY == 0:
            self.REFERENCE_LOGIC = StaticWitnessLogic.sigma_normal
        elif self.DIFFICULTY == 1:
            self.REFERENCE_LOGIC = StaticWitnessLogic.sigma_expert
        elif self.DIFFICULTY == 2:
            self.REFERENCE_LOGIC = StaticWitnessLogic.vanilla

        self.CONNECTIONS_BY_REGION_NAME = copy.copy(self.REFERENCE_LOGIC.STATIC_CONNECTIONS_BY_REGION_NAME)
        self.DEPENDENT_REQUIREMENTS_BY_HEX = copy.copy(self.REFERENCE_LOGIC.STATIC_DEPENDENT_REQUIREMENTS_BY_HEX)
        self.REQUIREMENTS_BY_HEX = dict()

        # Determining which panels need to be events is a difficult process.
        # At the end, we will have EVENT_ITEM_PAIRS for all the necessary ones.
        self.EVENT_PANELS = set()
        self.EVENT_ITEM_PAIRS = dict()
        self.ALWAYS_EVENT_HEX_CODES = set()
        self.COMPLETELY_DISABLED_ENTITIES = set()
        self.PRECOMPLETED_LOCATIONS = set()
        self.EXCLUDED_LOCATIONS = set()
        self.ADDED_CHECKS = set()
        self.VICTORY_LOCATION = "0x0356B"
        self.EVENT_ITEM_NAMES = {
            "0xFFD00": "Main Island Reached Independently",
            "0xFFD01": "Inside Quarry Reached Independently",
            "0x09D9B": "Monastery Shutters Open",
            "0x193A6": "Monastery Laser Panel Activates",
            "0x00037": "Monastery Branch Panels Activate",
            "0x0A079": "Access to Bunker Laser",
            "0x0A3B5": "Door to Tutorial Discard Opens",
            "0x00139": "Keep Hedges 1 Knowledge",
            "0x019DC": "Keep Hedges 2 Knowledge",
            "0x019E7": "Keep Hedges 3 Knowledge",
            "0x01A0F": "Keep Hedges 4 Knowledge",
            "0x033EA": "Pressure Plates 1 Knowledge",
            "0x01BE9": "Pressure Plates 2 Knowledge",
            "0x01CD3": "Pressure Plates 3 Knowledge",
            "0x01D3F": "Pressure Plates 4 Knowledge",
            "0x09F7F": "Mountain Access",
            "0x0367C": "Quarry Laser Stoneworks Requirement Met",
            "0x009A1": "Swamp Between Bridges Far 1 Activates",
            "0x00006": "Swamp Cyan Water Drains",
            "0x00990": "Swamp Between Bridges Near Row 1 Activates",
            "0x0A8DC": "Intro 6 Activates",
            "0x0000A": "Swamp Beyond Rotating Bridge 1 Access",
            "0x09E86": "Mountain Floor 2 Blue Bridge Access",
            "0x09ED8": "Mountain Floor 2 Yellow Bridge Access",
            "0x0A3D0": "Quarry Laser Boathouse Requirement Met",
            "0x00596": "Swamp Red Water Drains",
            "0x00E3A": "Swamp Purple Water Drains",
            "0x0343A": "Door to Symmetry Island Powers On",
            "0xFFF00": "Mountain Bottom Floor Discard Turns On",
            "0x17CA6": "All Boat Panels Turn On",
            "0x17CDF": "All Boat Panels Turn On",
            "0x09DB8": "All Boat Panels Turn On",
            "0x17C95": "All Boat Panels Turn On",
            "0x0A054": "Couch EP solvable",
            "0x03BB0": "Town Church Lattice Vision From Outside",
            "0x28AC1": "Town Wooden Rooftop Turns On",
            "0x28A69": "Town Tower 1st Door Opens",
            "0x28ACC": "Town Tower 2nd Door Opens",
            "0x28AD9": "Town Tower 3rd Door Opens",
            "0x28B39": "Town Tower 4th Door Opens",
            "0x014E8": "Quarry Stoneworks Lift Control Powers On",
            "0x03675": "Quarry Stoneworks Ramp Moving",
            "0x03679": "Quarry Stoneworks Lift Moving",
            "0x2FAF6": "Tutorial Gate Secret Solution Knowledge",
            "0x079DF": "Town Tall Hexagonal Turns On",
            "0x17DA2": "Right Orange Bridge Fully Extended",
            "0x19B24": "Shadows Intro Patterns Visible",
            "0x2700B": "Open Door to Treehouse Laser House",
            "0x00055": "Orchard Apple Trees 4 Turns On",
            "0x17DDB": "Left Orange Bridge Fully Extended",
            "0x03535": "Shipwreck Video Pattern Knowledge",
            "0x03542": "Mountain Video Pattern Knowledge",
            "0x0339E": "Desert Video Pattern Knowledge",
            "0x03481": "Tutorial Video Pattern Knowledge",
            "0x03702": "Jungle Video Pattern Knowledge",
            "0x0356B": "Challenge Video Pattern Knowledge",
            "0x0A15F": "Desert Laser Panel Shutters Open (1)",
            "0x012D7": "Desert Laser Panel Shutters Open (2)",
            "0x03613": "Treehouse Orange Bridge 13 Turns On",
            "0x17DEC": "Treehouse Laser House Access Requirement",
            "0x03C08": "Town Church Entry Opens",
            "0x17D02": "Windmill Blades Spinning",
            "0x0A0C9": "Cargo Box EP completable",
            "0x09E39": "Pink Light Bridge Extended",
            "0x17CC4": "Rails EP available",
            "0x2896A": "Bridge Underside EP available",
            "0x00064": "First Tunnel EP visible",
            "0x03553": "Tutorial Video EPs availble",
            "0x17C79": "Bunker Glass Room solutions visible",
            "0x275FF": "Stoneworks Light EPs available",
            "0x17E2B": "Remaining Purple Sand EPs available",
            "0x03852": "Ramp EPs requirement",
            "0x334D8": "RGB panels & EPs solvable",
            "0x03750": "Left Garden EP available",
            "0x03C0C": "RGB Flowers EP requirement",
            "0x01CD5": "Pressure Plates 3 EP requirement",
            "0x3865F": "Ramp EPs access requirement",
            "0x1C31A": "Challenge Completion Requirement 1",
            "0x1C319": "Challenge Completion Requirement 2",
            "0x09E7B": "Mountain Floor 1 Exit Door Requirement 1",
            "0x09E6B": "Mountain Floor 1 Exit Door Requirement 2",
            "0x09F6E": "Mountain Floor 1 Exit Door Requirement 3",
            "0x09EAF": "Mountain Floor 1 Exit Door Requirement 4",
        }

        self.ALWAYS_EVENT_NAMES_BY_HEX = {
            "0x00509": "Symmetry Laser Activation",
            "0x012FB": "Desert Laser Activation",
            "0x09F98": "Desert Laser Redirection",
            "0x01539": "Quarry Laser Activation",
            "0x181B3": "Shadows Laser Activation",
            "0x014BB": "Keep Laser Activation",
            "0x17C65": "Monastery Laser Activation",
            "0x032F9": "Town Laser Activation",
            "0x00274": "Jungle Laser Activation",
            "0x0C2B2": "Bunker Laser Activation",
            "0x00BF6": "Swamp Laser Activation",
            "0x028A4": "Treehouse Laser Activation",
        }

        self.make_options_adjustments(world)
        self.make_dependency_reduced_checklist()
        self.make_event_panel_lists()
