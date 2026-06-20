import random

ENEMY_DATA = {
    # The Forest (floors 1-10)
    "Dire Wolf":       {"hp": 28, "atk": 8,  "def": 1, "xp": 20,  "gold": (2, 8)},
    "Goblin Scout":    {"hp": 22, "atk": 7,  "def": 1, "xp": 15,  "gold": (1, 6)},
    "Hornet Swarm":    {"hp": 18, "atk": 9,  "def": 0, "xp": 18,  "gold": (0, 4)},
    "Forest Troll":    {"hp": 38, "atk": 8,  "def": 2, "xp": 25,  "gold": (3, 10)},
    "Rabid Bear":      {"hp": 35, "atk": 9,  "def": 1, "xp": 22,  "gold": (2, 8)},

    # The Mines (floors 11-20)
    "Cave Troll":      {"hp": 45, "atk": 11, "def": 2, "xp": 45,  "gold": (6, 15)},
    "Giant Spider":    {"hp": 38, "atk": 12, "def": 1, "xp": 40,  "gold": (4, 12)},
    "Kobold Miner":    {"hp": 35, "atk": 11, "def": 2, "xp": 35,  "gold": (5, 14)},
    "Rock Golem":      {"hp": 55, "atk": 10, "def": 3, "xp": 50,  "gold": (8, 18)},
    "Swarm of Bats":   {"hp": 30, "atk": 12, "def": 0, "xp": 30,  "gold": (2, 8)},

    # The Crypt (floors 21-30)
    "Skeleton Warrior":{"hp": 50, "atk": 14, "def": 2, "xp": 70,  "gold": (10, 22)},
    "Zombie":          {"hp": 55, "atk": 13, "def": 2, "xp": 60,  "gold": (8, 18)},
    "Ghost":           {"hp": 40, "atk": 15, "def": 1, "xp": 65,  "gold": (9, 20)},
    "Mummy":           {"hp": 60, "atk": 14, "def": 2, "xp": 75,  "gold": (12, 25)},
    "Ghoul":           {"hp": 45, "atk": 15, "def": 1, "xp": 68,  "gold": (10, 22)},

    # The Ruined Castle (floors 31-40)
    "Cursed Knight":   {"hp": 65, "atk": 17, "def": 2, "xp": 100, "gold": (15, 30)},
    "Gargoyle":        {"hp": 60, "atk": 17, "def": 3, "xp": 95,  "gold": (14, 28)},
    "Banshee":         {"hp": 55, "atk": 18, "def": 1, "xp": 105, "gold": (16, 32)},
    "Wraith":          {"hp": 58, "atk": 18, "def": 1, "xp": 100, "gold": (15, 30)},
    "Dark Archer":     {"hp": 52, "atk": 18, "def": 1, "xp": 98,  "gold": (14, 28)},

    # The Dark Mage School (floors 41-50)
    "Apprentice Mage": {"hp": 60, "atk": 20, "def": 1, "xp": 130, "gold": (20, 40)},
    "Arcane Golem":    {"hp": 80, "atk": 19, "def": 3, "xp": 145, "gold": (25, 45)},
    "Spell Wraith":    {"hp": 60, "atk": 21, "def": 1, "xp": 135, "gold": (22, 42)},
    "Corrupted Scholar":{"hp": 68,"atk": 20, "def": 2, "xp": 140, "gold": (24, 44)},
    "Living Tome":     {"hp": 55, "atk": 21, "def": 1, "xp": 128, "gold": (20, 38)},

    # The Underdark (floors 51-60)
    "Dark Elf Assassin":{"hp": 72,"atk": 22, "def": 2, "xp": 175, "gold": (30, 55)},
    "Mind Flayer":     {"hp": 78, "atk": 23, "def": 2, "xp": 180, "gold": (32, 58)},
    "Cave Kraken":     {"hp": 95, "atk": 21, "def": 3, "xp": 185, "gold": (35, 60)},
    "Duergar Warrior": {"hp": 82, "atk": 22, "def": 3, "xp": 170, "gold": (28, 52)},
    "Fungal Horror":   {"hp": 88, "atk": 21, "def": 2, "xp": 165, "gold": (26, 50)},

    # The Core (floors 61-70)
    "Lava Elemental":  {"hp": 95,  "atk": 25, "def": 2, "xp": 220, "gold": (40, 70)},
    "Demon Grunt":     {"hp": 90,  "atk": 24, "def": 2, "xp": 215, "gold": (38, 68)},
    "Fire Drake":      {"hp": 110, "atk": 26, "def": 2, "xp": 230, "gold": (42, 75)},
    "Ash Wraith":      {"hp": 82,  "atk": 26, "def": 1, "xp": 225, "gold": (40, 72)},
    "Infernal Knight": {"hp": 115, "atk": 23, "def": 3, "xp": 235, "gold": (45, 80)},

    # The Abyss (floors 71+)
    "Void Wraith":     {"hp": 105, "atk": 29, "def": 2, "xp": 300, "gold": (55, 90)},
    "Soul Eater":      {"hp": 115, "atk": 28, "def": 2, "xp": 310, "gold": (58, 95)},
    "Abyssal Titan":   {"hp": 140, "atk": 30, "def": 3, "xp": 320, "gold": (60, 100)},
    "Nightmare":       {"hp": 110, "atk": 31, "def": 1, "xp": 315, "gold": (57, 92)},
    "The Undying":     {"hp": 130, "atk": 32, "def": 2, "xp": 330, "gold": (62, 105)},
}

BOSS_DATA = {
    10:  {"name": "Gobzo, the Wolf Tamer",             "hp": 160, "atk": 13, "def": 3, "xp": 150, "gold": (20, 40)},
    20:  {"name": "Grak, the Deep Foreman",            "hp": 230, "atk": 18, "def": 4, "xp": 280, "gold": (40, 70)},
    30:  {"name": "Seraphine, the Undying Countess",   "hp": 290, "atk": 22, "def": 3, "xp": 380, "gold": (60, 100)},
    40:  {"name": "Commander Igris, Oathbound Warrior","hp": 350, "atk": 27, "def": 5, "xp": 500, "gold": (80, 130)},
    50:  {"name": "Headmaster Voss, the Corrupted",    "hp": 420, "atk": 32, "def": 4, "xp": 620, "gold": (100, 160)},
    60:  {"name": "Zyx'ara, the Elder Mind",           "hp": 490, "atk": 35, "def": 4, "xp": 750, "gold": (130, 200)},
    70:  {"name": "Ignarath, the Eternal Flame",       "hp": 580, "atk": 39, "def": 5, "xp": 900, "gold": (160, 250)},
}

ZONE_POOLS = {
    (1,  10): ["Dire Wolf", "Goblin Scout", "Hornet Swarm", "Forest Troll", "Rabid Bear"],
    (11, 20): ["Cave Troll", "Giant Spider", "Kobold Miner", "Rock Golem", "Swarm of Bats"],
    (21, 30): ["Skeleton Warrior", "Zombie", "Ghost", "Mummy", "Ghoul"],
    (31, 40): ["Cursed Knight", "Gargoyle", "Banshee", "Wraith", "Dark Archer"],
    (41, 50): ["Apprentice Mage", "Arcane Golem", "Spell Wraith", "Corrupted Scholar", "Living Tome"],
    (51, 60): ["Dark Elf Assassin", "Mind Flayer", "Cave Kraken", "Duergar Warrior", "Fungal Horror"],
    (61, 70): ["Lava Elemental", "Demon Grunt", "Fire Drake", "Ash Wraith", "Infernal Knight"],
    (71, 999):["Void Wraith", "Soul Eater", "Abyssal Titan", "Nightmare", "The Undying"],
}

class Enemy:
    def __init__(self, name, hp, atk, defense, xp, gold):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.atk = atk
        self.defense = defense
        self.xp = xp
        self.gold = random.randint(*gold)
        self.is_boss = False

    def take_damage(self, amount):
        damage = max(1, amount - self.defense)
        self.hp -= damage
        return damage

    def is_alive(self):
        return self.hp > 0


def get_enemy_pool(floor):
    for (min_floor, max_floor), enemies in ZONE_POOLS.items():
        if min_floor <= floor <= max_floor:
            return enemies
    return ZONE_POOLS[(71, 999)]


def spawn_enemy(floor):
    pool = get_enemy_pool(floor)
    name = random.choice(pool)
    data = ENEMY_DATA[name]
    return Enemy(name, data["hp"], data["atk"], data["def"], data["xp"], data["gold"])


def spawn_boss(floor):
    if floor in BOSS_DATA:
        data = BOSS_DATA[floor]
    else:
        last = BOSS_DATA[70]
        scale = 1 + (floor - 70) * 0.1
        data = {
            "name": f"Abyssal Lord (Floor {floor})",
            "hp":   int(last["hp"]  * scale),
            "atk":  int(last["atk"] * scale),
            "def":  last["def"],
            "xp":   int(last["xp"]  * scale),
            "gold": (int(last["gold"][0] * scale), int(last["gold"][1] * scale)),
        }
    enemy = Enemy(data["name"], data["hp"], data["atk"], data["def"], data["xp"], data["gold"])
    enemy.is_boss = True
    return enemy