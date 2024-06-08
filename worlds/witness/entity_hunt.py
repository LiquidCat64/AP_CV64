from collections import defaultdict
from logging import debug
from pprint import pformat
from typing import TYPE_CHECKING, Dict, List, Set, Tuple

from .data import static_logic as static_witness_logic

if TYPE_CHECKING:
    from . import WitnessPlayerLogic, WitnessWorld


class EntityHuntPicker:
    def __init__(self, player_logic: "WitnessPlayerLogic", world: "WitnessWorld", pre_picked_entities: Set[str]):
        self.player_logic = player_logic
        self.player_options = world.options
        self.player_name = world.player_name
        self.random = world.random

        self.PRE_PICKED_HUNT_ENTITIES = pre_picked_entities.copy()
        self.HUNT_ENTITIES = set()

        self.ALL_ELIGIBLE_PANELS, self.ELIGIBLE_PANELS_BY_AREA = self._get_eligible_panels()

    def pick_panel_hunt_panels(self) -> Set[str]:
        self.HUNT_ENTITIES = self.PRE_PICKED_HUNT_ENTITIES.copy()

        self._pick_all_hunt_panels()
        self._replace_unfair_hunt_panels_with_good_hunt_panels()
        self._log_results()

        return self.HUNT_ENTITIES

    def _get_eligible_panels(self) -> Tuple[List[str], Dict[str, Set[str]]]:
        disallowed_entities_for_panel_hunt = {
            "0x03629",  # Tutorial Gate Open, which is the panel that is locked by panel hunt
            "0x03505",  # Tutorial Gate Close (same thing)
            "0x3352F",  # Gate EP (same thing)
            "0x00CDB",  # Challenge Reallocating
            "0x0051F",  # Challenge Reallocating
            "0x00524",  # Challenge Reallocating
            "0x00CD4",  # Challenge Reallocating
            "0x00CB9",  # Challenge May Be Unsolvable
            "0x00CA1",  # Challenge May Be Unsolvable
            "0x00C80",  # Challenge May Be Unsolvable
            "0x00C68",  # Challenge May Be Unsolvable
            "0x00C59",  # Challenge May Be Unsolvable
            "0x00C22",  # Challenge May Be Unsolvable
            "0x0A3A8",  # Reset PP
            "0x0A3B9",  # Reset PP
            "0x0A3BB",  # Reset PP
            "0x0A3AD",  # Reset PP
        }

        all_eligible_panels = [
            entity_hex for entity_hex, entity_obj in static_witness_logic.ENTITIES_BY_HEX.items()
            if entity_obj["entityType"] == "Panel" and self.player_logic.solvability_guaranteed(entity_hex)
            and not (
                # Due to an edge case, Discards have to be on in disable_non_randomized even if Discard Shuffle is off.
                # However, I don't think they should be hunt panels in this case.
                self.player_options.disable_non_randomized_puzzles
                and not self.player_options.shuffle_discarded_panels
                and entity_obj["locationType"] == "Discard"
            )
            and entity_hex not in disallowed_entities_for_panel_hunt
            and entity_hex not in self.HUNT_ENTITIES
        ]

        eligible_panels_by_area = defaultdict(set)
        for eligible_panel in all_eligible_panels:
            associated_area = static_witness_logic.ENTITIES_BY_HEX[eligible_panel]["area"]["name"]
            eligible_panels_by_area[associated_area].add(eligible_panel)

        return all_eligible_panels, eligible_panels_by_area

    def _get_percentage_of_hunt_panels_by_area(self):
        contributing_percentage_per_area = dict()
        for area, eligible_panels in self.ELIGIBLE_PANELS_BY_AREA.items():
            amount_of_already_chosen_panels = len(self.ELIGIBLE_PANELS_BY_AREA[area] & self.HUNT_ENTITIES)
            current_percentage = amount_of_already_chosen_panels / len(self.HUNT_ENTITIES)
            contributing_percentage_per_area[area] = current_percentage

        return contributing_percentage_per_area

    def _get_next_random_batch(self, amount: int, same_area_discouragement: float) -> List[str]:
        """
        Pick the next batch of hunt panels.
        Areas that already have a lot of hunt panels in them will be discouraged from getting more.
        The strength of this effect is controlled by the same_area_discouragement factor from the player's options.
        """

        percentage_of_hunt_panels_by_area = self._get_percentage_of_hunt_panels_by_area()

        max_percentage = max(percentage_of_hunt_panels_by_area.values())
        if max_percentage == 0:
            allowance_per_area = {area: 1 for area in percentage_of_hunt_panels_by_area}
        else:
            allowance_per_area = {
                area: (max_percentage - current_percentage) / max_percentage
                for area, current_percentage in percentage_of_hunt_panels_by_area.items()
            }
            # use same_area_discouragement as lerp factor
            allowance_per_area = {
                area: (1.0 - same_area_discouragement) + (weight * same_area_discouragement)
                for area, weight in allowance_per_area.items()
            }

        assert min(allowance_per_area.values()) >= 0, (f"Somehow, an area had a negative weight when picking"
                                                       f" hunt panels: {allowance_per_area}")

        remaining_panels, remaining_panels_weights = [], []
        for area, eligible_panels in self.ELIGIBLE_PANELS_BY_AREA.items():
            for panel in eligible_panels - self.HUNT_ENTITIES:
                remaining_panels.append(panel)
                remaining_panels_weights.append(allowance_per_area[area])

        # I don't think this can ever happen, but let's be safe
        if sum(remaining_panels_weights) == 0:
            remaining_panels_weights = [1] * len(remaining_panels_weights)

        return self.random.choices(remaining_panels, weights=remaining_panels_weights, k=amount)

    def _pick_all_hunt_panels(self):
        total_panels = self.player_options.panel_hunt_total.value
        same_area_discouragement = self.player_options.panel_hunt_discourage_same_area_factor / 100

        # If we're using random picking, just choose all the panels now and return
        if not same_area_discouragement:
            hunt_panels = self.random.choices(self.ALL_ELIGIBLE_PANELS, k=total_panels - len(self.HUNT_ENTITIES))
            self.HUNT_ENTITIES.update(hunt_panels)
            return

        # If we're discouraging panels from the same area being picked, we have to pick panels one at a time
        # For higher total counts, we do them in small batches for performance
        batch_size = max(1, total_panels // 20)

        while len(self.HUNT_ENTITIES) < total_panels:
            actual_amount_to_pick = min(batch_size, total_panels - len(self.HUNT_ENTITIES))

            self.HUNT_ENTITIES.update(self._get_next_random_batch(actual_amount_to_pick, same_area_discouragement))

    def _replace_unfair_hunt_panels_with_good_hunt_panels(self):
        """
        Replace some of the connected panels with the one you're guaranteed to be able to see & solve first
        """

        replacements = {
            "0x18488": "0x00609",  # Replace Swamp Sliding Bridge Underwater with Swamp Sliding Bridge Above Water
            "0x03676": "0x03678",  # Replace Quarry Upper Ramp Control with Lower Ramp Control
            "0x03675": "0x03679",  # Replace Quarry Upper Lift Control with Lower Lift Control
        }

        if self.player_options.shuffle_doors < 2:
            replacements.update({
                "0x334DC": "0x334DB",  # In door shuffle, the Shadows Timer Panels are disconnected
                "0x17CBC": "0x2700B",  # In door shuffle, the Laser Timer Panels are disconnected
            })

        for bad_entitiy, good_entity in replacements.items():
            # If the bad entity was picked as a hunt entity ...
            if bad_entitiy not in self.HUNT_ENTITIES:
                continue

            # ... and the good entity was not ...
            if good_entity in self.HUNT_ENTITIES or good_entity not in self.ALL_ELIGIBLE_PANELS:
                continue

            # ... replace the bad entity with the good entity.
            self.HUNT_ENTITIES.remove(bad_entitiy)
            self.HUNT_ENTITIES.add(good_entity)

    def _log_results(self):
        final_percentage_of_hunt_panels_by_area = self._get_percentage_of_hunt_panels_by_area()

        sorted_area_percentages_dict = dict(sorted(final_percentage_of_hunt_panels_by_area.items(), key=lambda x: x[1]))
        sorted_area_percentages_dict = {
            area: str(percentage) + (" (maxed)" if self.ELIGIBLE_PANELS_BY_AREA[area] <= self.HUNT_ENTITIES else "")
            for area, percentage in sorted_area_percentages_dict.items()
        }
        player_name = self.player_name
        discouragemenet_factor = self.player_options.panel_hunt_discourage_same_area_factor
        debug(
            f'Final area percentages for player "{player_name}" ({discouragemenet_factor} discouragement):\n'
            f"{pformat(sorted_area_percentages_dict)}"
        )
