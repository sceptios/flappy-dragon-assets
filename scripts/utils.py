import os
from yamlreader import load_yaml

GAME_STRINGS = {}
SKILLS = {}
DRAGONS = {}
EGGS = {}
ROYALS = {}
THEMES = {}
WORLDS = {}
AUGMENTS = {}


class Data:
    CONTROLS = ["Tap", "RTap", "Hold", "RHold", "GoToTap", "Follow"]
    RARITIES = ["Common", "Uncommon", "Rare", "Epic", "Legendary", "Mythic", "All"]
    TYPES = ["Western", "Leviathan", "Feathered", "Eastern", "Mountain", "Fairy", "Cosmic", "All"]
    SKILL_CONDITIONS = [
        "WhenInitializingGameplayCamera",
        "WhenScoring",
        "WhenEatingRoyal",
        "WhenGettingCrown",
        "WhenGettingTreasure",
        "WhenDestroyingTowers",
        "WhenDying",
        "WhenFlapping",
        "WhenGettingPowerUp",
        "WhileUsingPowerUp",
        "WhenCalculatingPowerUpChances",
        "WhenCalculatingPowerUpPower",
        "WhenCalculatingTileChances",
        "WhenCalculatingRiftChances",
        "ResetsWhenChangingTheme",
        "WhenColliding",
        "WhenPickingUpSomething",
        "WhenSpinning",
        "WhenGettingStellarDonut",
        "WhenGettingMysteryEgg",
        "WhenEnteringRift",
        "WhenPickingUpPowerupUp",
    ]
    EGG_CATEGORIES = ["Rarity", "Type", "Season", "Powerup", "Subtype"]


def punctuate(descs):
    for lang in descs:
        if lang not in ["ja", "zh", "zh-CN", "ko"] and descs[lang][-1] not in [".", "?", "!", chr(0xBF), chr(0xA1)]:
            descs[lang] += "."
    return descs


class Skill:
    def __init__(self, filepath, *args, **kwargs):
        super().__init__(*args, **kwargs)
        json_data = load_yaml(filepath)

        self.guid = json_data["_guid"]

        cooldown = {
            "min": json_data["minValueCooldown"],
            "max": json_data["maxValueCooldown"],
        }
        primary_value = {
            "min": json_data["minValuePrimary"],
            "max": json_data["maxValuePrimary"],
            "prefix": json_data["prefixValuePrimary"],
            "suffix": json_data["suffixValuePrimary"],
        }
        secondary_value = {
            "min": json_data["minValueSecondary"],
            "max": json_data["maxValueSecondary"],
            "prefix": json_data["prefixValueSecondary"],
            "suffix": json_data["suffixValueSecondary"],
        }
        activation_conditions = []
        condition_raw = json_data["activateCondition"]
        for index in range(len(Data.SKILL_CONDITIONS)):
            if condition_raw & (2 << index):
                activation_conditions.append(Data.SKILL_CONDITIONS[index])

        self.data = {
            "name": GAME_STRINGS[json_data["localizedName"]["mTerm"]],
            "is_active_skill": bool(json_data["isActive"]),
            "cooldown": cooldown,
            "activation_conditions": activation_conditions,
            "increased_royal_appearence": bool(json_data["increaseRoyalAppearenceChance"]),
            "increased_chest_appearence": bool(json_data["increaseChestAppearenceChance"]),
            "increased_egg_appearence": bool(json_data["increaseEggAppearenceChance"]),
            "increased_powerup_appearence": bool(json_data["increasePowerUpAppearenceChance"]),
            "increased_portal_appearence": bool(json_data["increasePortalAppearenceChance"]),
            "increased_donut_appearence": bool(json_data["increaseStellarDonutAppearenceChance"]),
            "PRIMARY_VALUE": primary_value,
            "SECONDARY_VALUE": secondary_value,
            "description": punctuate(GAME_STRINGS[json_data["localizedDescription"]["mTerm"]]),
        }


class Dragon:
    def __init__(self, filepath, *args, **kwargs):
        super().__init__(*args, **kwargs)
        json_data = load_yaml(filepath)

        self.guid = json_data["_guid"]
        self.enabled = bool(json_data["m_Enabled"])

        self.data = {
            "name": json_data["name"],
            "type": Data.TYPES[json_data["type"]],
            "rarity": Data.RARITIES[json_data["rarity"]],
            "control": Data.CONTROLS[json_data["controlType"]],
            "breeding_eggs": [i["guid"] for i in json_data["breedingEggs"]],
            "speed": json_data["horizontalSpeed"],
            "force": json_data["verticalSpeed"],
            "weight": json_data["gravity"],
            "description": punctuate(GAME_STRINGS[json_data["localizedDescription"]["mTerm"]]),
            "skill": SKILLS[json_data["skill"]["guid"]].data,
        }

    def convert_breeding_eggs(self):
        self.data["breeding_eggs"] = [EGGS[guid].data["name"]["en"][:-4] for guid in self.data["breeding_eggs"]]

    def __lt__(self, other):
        return self.data["name"] < other.data["name"]


class Egg:
    def __init__(self, filepath, *args, **kwargs):
        super().__init__(*args, **kwargs)
        json_data = load_yaml(filepath)

        self.guid = json_data["_guid"]
        self.enabled = bool(json_data["m_Enabled"])

        self.data = {
            "name": GAME_STRINGS[json_data["nameKey"]],
            "description": GAME_STRINGS[json_data["descriptionKey"]],
            "incubation_time": json_data["incubationTime"],
            "category": Data.EGG_CATEGORIES[json_data["eggSubtype"]],
            "rarity_pool": Data.RARITIES[json_data["rarityPool"]],
            "type_pool": Data.TYPES[json_data["typePool"]],
            "custom_pool": [DRAGONS[i["guid"]].data["name"] for i in json_data["customDragonPool"]],
            "contains_dragon_heart": bool(json_data["containsDragonHeart"]),
            "contains_evil_mushroom": bool(json_data["containsEvilMushroom"]),
            "contains_fairy_dust": bool(json_data["containsFairyDust"]),
            "contains_dragon_eye": bool(json_data["containsDragonEye"]),
            "contains_dragon_chilli": bool(json_data["containsDragonChilli"]),
            "contains_thunder_cloud": bool(json_data["containsThunderCloud"]),
            "contains_sands_of_time": bool(json_data["containsSandsOfTime"]),
            "contains_cosmic_stars": bool(json_data["containsCosmicStars"]),
            "contains_lucky_charm": bool(json_data["containsLuckyCharm"]),
            "contains_curved_spoon": bool(json_data["containsCurvedSpoon"]),
            "contains_magic_snowflake": bool(json_data["containsMagicSnowflake"]),
            "contains_spooky_ghost": bool(json_data["containsSpookyGhost"]),
        }
        if self.data["custom_pool"]:
            self.data["type_pool"] = Data.TYPES[-1]

    def __lt__(self, other):
        return self.data["name"]["en"] < other.data["name"]["en"]


class Royal:
    def __init__(self, filepath, *args, **kwargs):
        super().__init__(*args, **kwargs)
        json_data = load_yaml(filepath)

        self.guid = json_data["_guid"]

        self.data = {"name": json_data["name"], "can_sleep": bool(json_data["canSleep"])}


class Theme:
    def __init__(self, filepath, *args, **kwargs):
        super().__init__(*args, **kwargs)
        json_data = load_yaml(filepath)

        self.guid = json_data["_guid"]

        self.data = {
            "name": json_data["name"],
            "is_night": bool(json_data["isNight"]),
            "has_rain": bool(json_data["hasRain"]),
            "has_snow": bool(json_data["hasSnow"]),
        }


class World:
    def __init__(self, filepath, *args, **kwargs):
        super().__init__(*args, **kwargs)
        json_data = load_yaml(filepath)

        self.guid = json_data["_guid"]

        self.data = {
            "name": GAME_STRINGS[json_data["localizedNameKey"]],
            "description": punctuate(GAME_STRINGS[json_data["localizedDescriptionKey"]]),
            "tower_spacing": {
                "horizontal": {
                    "initial": json_data["spacingCurve"]["m_Curve"][0]["value"],
                    "final": json_data["spacingCurve"]["m_Curve"][1]["value"],
                },
                "vertical": {
                    "initial": json_data["closureCurve"]["m_Curve"][0]["value"],
                    "final": json_data["closureCurve"]["m_Curve"][1]["value"],
                },
            },
            "aristocrats": [ROYALS[i["guid"]].data for i in json_data["royals"]],
            "themes": [THEMES[i["guid"]].data for i in json_data["themes"]],
        }

    def __lt__(self, other):
        return self.data["name"]["en"] < other.data["name"]["en"]


class Augment:
    def __init__(self, filepath, *args, **kwargs):
        super().__init__(*args, **kwargs)
        json_data = load_yaml(filepath)

        self.guid = json_data["_guid"]

        primary_value = {
            "value": json_data["valuePrimary"],
            "prefix": json_data["prefixValuePrimary"],
            "suffix": json_data["suffixValuePrimary"],
        }
        secondary_value = {
            "value": json_data["valueSecondary"],
            "prefix": json_data["prefixValueSecondary"],
            "suffix": json_data["suffixValueSecondary"],
        }

        self.data = {
            "name": GAME_STRINGS[json_data["localizedNameKey"]],
            "is_stackable": bool(json_data["isStackable"]),
            "PRIMARY_VALUE": primary_value,
            "SECONDARY_VALUE": secondary_value,
            "description": punctuate(GAME_STRINGS[json_data["localizedDescriptionKey"]]),
        }

    def __lt__(self, other):
        return self.data["name"]["en"] < other.data["name"]["en"]


def load_data(base_dir):
    languages = []
    json_data = load_yaml(os.path.join(base_dir, "I2Languages.asset"))["mSource"]
    for item in json_data["mLanguages"]:
        languages.append(item["Code"])
    for item in json_data["mTerms"]:
        GAME_STRINGS[item["Term"]] = {}
        for index, data in enumerate(item["Languages"]):
            if isinstance(data, str):
                data = data.strip()
            GAME_STRINGS[item["Term"]][languages[index]] = data

    FILE_NAMES = {"dragons": [], "skills": [], "eggs": [], "royals": [], "themes": [], "worlds": [], "augments": []}
    for filename in os.listdir(os.path.join(base_dir, "MonoBehaviour")):
        if filename.endswith(".asset"):
            if filename.startswith("Dragon_"):
                FILE_NAMES["dragons"].append(os.path.join(base_dir, "MonoBehaviour", filename))
            elif filename.startswith("Skill_"):
                FILE_NAMES["skills"].append(os.path.join(base_dir, "MonoBehaviour", filename))
            elif filename.startswith("Egg_"):
                FILE_NAMES["eggs"].append(os.path.join(base_dir, "MonoBehaviour", filename))
            elif filename.startswith("Royal_"):
                FILE_NAMES["royals"].append(os.path.join(base_dir, "MonoBehaviour", filename))
            elif filename.startswith("Theme_"):
                FILE_NAMES["themes"].append(os.path.join(base_dir, "MonoBehaviour", filename))
            elif filename.startswith("World_"):
                FILE_NAMES["worlds"].append(os.path.join(base_dir, "MonoBehaviour", filename))
            elif filename.startswith("DimensionalAugment_"):
                FILE_NAMES["augments"].append(os.path.join(base_dir, "MonoBehaviour", filename))

    for filename in FILE_NAMES["skills"]:
        skill = Skill(filename)
        SKILLS[skill.guid] = skill

    for filename in FILE_NAMES["dragons"]:
        dragon = Dragon(filename)
        DRAGONS[dragon.guid] = dragon

    for filename in FILE_NAMES["eggs"]:
        egg = Egg(filename)
        EGGS[egg.guid] = egg

    for dragon in DRAGONS.values():
        dragon.convert_breeding_eggs()

    for filename in FILE_NAMES["royals"]:
        royal = Royal(filename)
        ROYALS[royal.guid] = royal

    for filename in FILE_NAMES["themes"]:
        theme = Theme(filename)
        THEMES[theme.guid] = theme

    for filename in FILE_NAMES["worlds"]:
        world = World(filename)
        WORLDS[world.guid] = world

    for filename in FILE_NAMES["augments"]:
        augment = Augment(filename)
        AUGMENTS[augment.guid] = augment
