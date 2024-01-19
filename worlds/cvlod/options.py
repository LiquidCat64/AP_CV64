from dataclasses import dataclass
from Options import Choice, DefaultOnToggle, Range, Toggle, PerGameCommonOptions


class CharacterStages(Choice):
    """Whether to include Reinhardt-only stages, Carrie-only stages, or both."""
    display_name = "Character Stages"
    option_both = 0
    option_both_no_branches = 1
    option_reinhardt_only = 2
    option_carrie_only = 3
    default = 0


class StageShuffle(Toggle):
    """Shuffles which stages appear in which stage slots. Villa and Castle Center will never appear in any character
    stage slots if all character stages are included; they can only be somewhere on the main path.
    Castle Keep will always be at the end of the line."""
    display_name = "Stage Shuffle"


class StartingStage(Choice):
    """Which stage to start at if Stage Shuffle is turned on."""
    display_name = "Starting Stage"
    option_forest_of_silence = 0
    option_castle_wall = 1
    option_villa = 2
    option_tunnel = 3
    option_underground_waterway = 4
    option_castle_center = 5
    option_duel_tower = 6
    option_tower_of_execution = 7
    option_tower_of_science = 8
    option_tower_of_sorcery = 9
    option_room_of_clocks = 10
    option_clock_tower = 11
    option_mystery = 12
    default = 12


class WarpOrder(Choice):
    """Arranges the warps in the warp menu in whichever stage order chosen,
    thus changing the order they are unlocked in."""
    display_name = "Warp Order"
    option_seed_stage_order = 0
    option_vanilla_stage_order = 1
    option_randomized_order = 2
    default = 0


class SubWeaponShuffle(Choice):
    """Shuffles all sub-weapons in the game within their own pool or in the main item pool."""
    display_name = "Sub-weapon Shuffle"
    option_off = 0
    option_own_pool = 1
    option_anywhere = 2
    default = 0


class SpareKeys(Choice):
    """Puts an additional copy of every key item in the pool for every key item that there is to ensure fewer specific
    locations are required. Chance gives each key item a 50% chance of having a duplicate instead of guaranteeing one
    for all of them."""
    display_name = "Spare Keys"
    option_off = 0
    option_on = 1
    option_chance = 2
    default = 0


class HardItemPool(Toggle):
    """Replaces some items in the item pool with less valuable ones, to make the item pool sort of resemble Hard Mode
    in the PAL version."""
    display_name = "Hard Item Pool"


class Special1sPerWarp(Range):
    """Sets how many Special1 jewels are needed per warp menu option unlock."""
    range_start = 1
    range_end = 10
    default = 1
    display_name = "Special1s Per Warp"


class TotalSpecial1s(Range):
    """Sets how many Speical1 jewels are in the pool in total. This cannot be less than Special1s Per Warp x 7."""
    range_start = 1
    range_end = 70
    default = 7
    display_name = "Total Special1s"


class DraculasCondition(Choice):
    """Sets the requirement for unlocking and opening the door to Dracula's chamber.
    None: No requirement. Door is unlocked from the start.
    Crystal: Activate the big crystal in Castle Center's basement. Neither boss afterwards has to be defeated.
    Bosses: Kill a specified number of bosses with health bars and claim their Trophies.
    Specials: Find a specified number of Special2 jewels shuffled in the main item pool."""
    display_name = "Dracula's Condition"
    option_none = 0
    option_crystal = 1
    option_bosses = 2
    option_specials = 3
    default = 1


class PercentSpecial2sRequired(Range):
    """Percentage of Special2s required to enter Dracula's chamber when Dracula's Condition is Special2s."""
    range_start = 10
    range_end = 100
    default = 100
    display_name = "Percent Special2s Required"


class TotalSpecial2s(Range):
    """How many Speical2 jewels are in the pool in total when Dracula's Condition is Special2s."""
    range_start = 1
    range_end = 70
    default = 10
    display_name = "Total Special2s"


class BossesRequired(Range):
    """Sets how many bosses need to be defeated to enter Dracula's chamber. Only applies if Dracula's Chamber Condition
    is set to Bosses. Completely disabling the Renon and/or Vincent fights will decrease this number if above 14."""
    range_start = 1
    range_end = 16
    default = 14
    display_name = "Bosses Required"


class CarrieLogic(Toggle):
    """Adds the 2 checks inside Underground Waterway's crawlspace to the pool. If you are not yet certain that you
    (and everyone else if racing the same seed) will be playing as Carrie, don't enable this. Can be combined with
    Glitch Logic to include Carrie-only tricks."""
    display_name = "Carrie Logic"


class HardLogic(Toggle):
    """Properly considers sequence break tricks in logic (i.e. Left Tower skip). Can be combined with Carrie Logic to
    include Carrie-only skips. See the FAQ for a full list of tricks and glitches that may be logically required."""
    display_name = "Hard Logic"


class MultiHitBreakables(Toggle):
    """Adds the items that drop from the objects that break in three hits to the pool. There are 17 of these throughout
    the game adding up to 74 checks in total. The game will be modified to remember exactly which of their items you've
    picked up instead of simply whether they were broken or not."""
    display_name = "Multi-hit Breakables"


class EmptyBreakables(Toggle):
    """Adds 9 check locations in the form of breakables that normally have nothing (i.e. many Forest coffins, the candle
    in the Villa foyer that drops nothing, etc.) and some additional Red Jewels and/or moneybags into the item pool to
    compensate."""
    display_name = "Empty Breakables"


class LizardLockerItems(Toggle):
    """Adds the 6 items inside Castle Center 2F's Lizard-man generators to the pool. Picking up all of these can be a
    very time-consuming and luck-based process, so they are excluded by default."""
    display_name = "Lizard Locker Items"


class Shopsanity(Toggle):
    """Adds 7 one-time purchases from Renon's shop into the location pool. After buying an item from a slot, it will
    revert to whatever it is in the vanilla game."""
    display_name = "Shopsanity"


class ShopPrices(Choice):
    """Randomizes the amount of gold each item costs in Renon's shop.
    Use the below options to control how much or little an item can cost."""
    display_name = "Shop Prices"
    option_vanilla = 0
    option_randomized = 1
    default = 0


class MinimumGoldPrice(Range):
    """The lowest amount of gold an item can cost in Renon's shop, divided by 100.
    Only applies if shop prices are randomized."""
    display_name = "Minimum Gold Price"
    range_start = 1
    range_end = 50
    default = 2


class MaximumGoldPrice(Range):
    """The highest amount of gold an item can cost in Renon's shop, divided by 100.
    Only applies if shop prices are randomized."""
    display_name = "Maximum Gold Price"
    range_start = 1
    range_end = 50
    default = 30


class PostBehemothBoss(Choice):
    """Sets which boss is fought in the vampire triplets' room
    in Castle Center by which characters after defeating Behemoth."""
    display_name = "Post-Behemoth Boss"
    option_vanilla = 0
    option_inverted = 1
    option_always_rosa = 2
    option_always_camilla = 3
    default = 0


class RoomOfClocksBoss(Choice):
    """Sets which boss is fought at Room of Clocks by which characters."""
    display_name = "Room of Clocks Boss"
    option_vanilla = 0
    option_inverted = 1
    option_always_death = 2
    option_always_actrise = 3
    default = 0


class RenonFightCondition(Choice):
    """Sets the condition on which the Renon fight will trigger.
    Vanilla = after spending more than 30,000 gold in his shop."""
    display_name = "Renon Fight Condition"
    option_never = 0
    option_spend_30k = 1
    option_always = 2
    default = 0


class VincentFightCondition(Choice):
    """Sets the condition on which the vampire Vincent fight will trigger.
    Vanilla = after 16 or more in-game days pass."""
    display_name = "Vincent Fight Condition"
    option_never = 0
    option_wait_16_days = 1
    option_always = 2
    default = 0


class BadEndingCondition(Choice):
    """Sets the condition on which the currently-controlled character's Bad Ending will trigger.
    Vanilla = after defeating vampire Vincent."""
    display_name = "Bad Ending Condition"
    option_never = 0
    option_defeat_vincent = 1
    option_always = 2
    default = 0


class IncreaseItemLimit(DefaultOnToggle):
    """Increases the holding limit of usable items from 10 to 99 of each item."""
    display_name = "Increase Item Limit"


class NerfHealingItems(Toggle):
    """Decreases the amount of health healed by Roast Chickens to 25%, Roast Beefs to 50%, and Healing Kits to 80%."""
    display_name = "Nerf Healing Items"


class LoadingZoneHeals(DefaultOnToggle):
    """Whether end-of-level loading zones restore health and cure status aliments or not.
    Recommended off for those looking for more of a survival horror experience!"""


class InvisibleItems(Choice):
    """Sets which items are visible in their locations and which are invisible until picked up. 'Chance' gives each item
    a 50/50 chance of being visible or invisible."""
    display_name = "Invisible Items"
    option_vanilla = 0
    option_reveal_all = 1
    option_hide_all = 2
    option_chance = 3
    default = 0


class DropPreviousSubWeapon(Toggle):
    """When picking up a sub-weapon, the one you had before will drop behind you, so it can be taken back if desired."""
    display_name = "Drop Previous Sub-weapon"


class PermanentPowerUps(Toggle):
    """Replaces PowerUps with PermaUps, which upgrade your B weapon level permanently after receiving them even after
    death. To compensate, only two will be in the pool overall, and they will not drop from any enemy or projectile."""
    display_name = "Permanent PowerUps"


class IceTrapPercentage(Range):
    """Replaces a percentage of junk items with Ice Traps."""
    display_name = "Ice Trap Percentage"
    range_start = 0
    range_end = 100
    default = 0


class IceTrapAppearance(Choice):
    """Changes the appearance of ice traps as freestanding items."""
    display_name = "Ice Trap Appearance"
    option_major_only = 0
    option_junk_only = 1
    option_anything = 2
    default = 0


class DisableTimeRestrictions(Toggle):
    """Disables the time restriction on every event and door that requires the current time to be something specific
     (sun/moon doors, meeting Rosa, and the Villa fountain). The Villa coffin is not affected by this."""
    display_name = "Disable Time Requirements"


class SkipGondolas(Toggle):
    """Makes jumping on and activating a gondola in Tunnel instantly teleport you to the other station, thereby skipping
    the entire three-minute wait to ride the gondolas. The item normally at the gondola transfer point will be moved to
    instead be near the red gondola at its station."""
    display_name = "Skip Gondolas"


class SkipWaterwayBlocks(Toggle):
    """Opens the door to the third switch in Underground Waterway from the start so that the jumping across floating
    brick platforms won't have to be done."""
    display_name = "Skip Waterway Blocks"


class Countdown(Choice):
    """Displays, below the HUD clock, the number of unobtained progression-marked items or locations remaining in the
    stage you're currently in."""
    display_name = "Countdown"
    option_none = 0
    option_majors = 1
    option_all_locations = 2
    default = 0


class PantherDash(Choice):
    """Hold C-right at any time to sprint way faster. Any sequence breaks that might be possible with it are NOT
    considered in logic on any setting and any boss fights with boss health meters, if started, are expected to be
    finished before leaving their arenas if Dracula's Condition is bosses. Jumpless will prevent jumping while moving at
    the increased speed to make it impossible to cheat logic with it."""
    display_name = "Panther Dash"
    option_off = 0
    option_on = 1
    option_jumpless = 2
    default = 0


class IncreaseShimmySpeed(Toggle):
    """Increases the speed at which characters shimmy left and right while hanging on ledges."""
    display_name = "Increase Shimmy Speed"


class FallGuard(Toggle):
    """Removes fall damage from landing hard. Note that falling for too long will still result in instant death."""
    display_name = "Fall Guard"


class BackgroundMusic(Choice):
    """Randomizes or disables the music heard throughout the game. Randomized music is split into two pools: songs that
    loop and songs that don't."""
    display_name = "Background Music"
    option_normal = 0
    option_disabled = 1
    option_randomized = 2
    default = 0


class MapLighting(Choice):
    """Randomizes the lighting color RGB values on every map during every time of day to be literally anything.
    The colors and/or shading of the following things are affected: fog, maps, player, enemies, and some objects."""
    display_name = "Map Lighting"
    option_normal = 0
    option_randomized = 1
    default = 0


class WindowColorR(Range):
    """The red color value for the text windows during gameplay."""
    display_name = "Window Color R"
    range_start = 0
    range_end = 15
    default = 10


class WindowColorG(Range):
    """The green color value for the text windows during gameplay."""
    display_name = "Window Color G"
    range_start = 0
    range_end = 15
    default = 10


class WindowColorB(Range):
    """The blue color value for the text windows during gameplay."""
    display_name = "Window Color B"
    range_start = 0
    range_end = 15
    default = 10


class WindowColorA(Range):
    """The alpha value for the text windows during gameplay."""
    display_name = "Window Color A"
    range_start = 0
    range_end = 15
    default = 6


class DeathLink(Choice):
    """When you die, everyone dies. Of course the reverse is true too.
    explosive: Makes received DeathLinks kill you via the Magical Nitro explosion rather than the normal death
    animation."""
    display_name = "DeathLink"
    option_off = 0
    alias_no = 0
    alias_true = 1
    alias_yes = 1
    option_on = 1
    option_explosive = 2


@dataclass
class CVLoDOptions(PerGameCommonOptions):
    # character_stages: CharacterStages
    # stage_shuffle: StageShuffle
    # starting_stage: StartingStage
    # custom_stage_order: CustomStageOrder
    # warp_order: WarpOrder
    sub_weapon_shuffle: SubWeaponShuffle
    spare_keys: SpareKeys
    # hard_item_pool: HardItemPool
    # special1s_per_warp: Special1sPerWarp
    # total_special1s: TotalSpecial1s
    # draculas_condition: DraculasCondition
    # percent_special2s_required: PercentSpecial2sRequired
    # total_special2s: TotalSpecial2s
    # bosses_required: BossesRequired
    carrie_logic: CarrieLogic
    hard_logic: HardLogic
    multi_hit_breakables: MultiHitBreakables
    # empty_breakables: EmptyBreakables
    # lizard_locker_items: LizardLockerItems
    # shopsanity: Shopsanity
    # shop_prices: ShopPrices
    # minimum_gold_price: MinimumGoldPrice
    # maximum_gold_price: MaximumGoldPrice
    # post_behemoth_boss: PostBehemothBoss
    # room_of_clocks_boss: RoomOfClocksBoss
    # renon_fight_condition: RenonFightCondition
    # vincent_fight_condition: VincentFightCondition
    # bad_ending_condition: BadEndingCondition
    increase_item_limit: IncreaseItemLimit
    # nerf_healing_items: NerfHealingItems
    # loading_zone_heals: LoadingZoneHeals
    # invisible_items: InvisibleItems
    # drop_previous_sub_weapon: DropPreviousSubWeapon
    # permanent_powerups: PermanentPowerUps
    # ice_trap_percentage: IceTrapPercentage
    # ice_trap_appearance: IceTrapAppearance
    # disable_time_restrictions: DisableTimeRestrictions
    # skip_gondolas: SkipGondolas
    # skip_waterway_blocks: SkipWaterwayBlocks
    # countdown: Countdown
    # panther_dash: PantherDash
    # increase_shimmy_speed: IncreaseShimmySpeed
    # background_music: BackgroundMusic
    # map_lighting: MapLighting
    # fall_guard: FallGuard
    window_color_r: WindowColorR
    window_color_g: WindowColorG
    window_color_b: WindowColorB
    window_color_a: WindowColorA
    # death_link: DeathLink
