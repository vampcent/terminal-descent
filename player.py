CLASS_STATS = {
    "Warrior": {"max_hp": 120, "max_mp": 40,  "atk": 7,  "def": 5, "spd": 4},
    "Rogue":   {"max_hp": 80,  "max_mp": 50,  "atk": 9,  "def": 3, "spd": 8},
    "Mage":    {"max_hp": 60,  "max_mp": 100, "atk": 12, "def": 2, "spd": 5},
}

CLASS_ABILITIES = {
    "Warrior": ["Power Strike", "Shield Bash", "War Cry"],
    "Rogue":   ["Backstab", "Smoke Bomb", "Poison Blade"],
    "Mage":    ["Fireball", "Frost Nova", "Arcane Burst"],
}

class Player:
    def __init__(self, name, char_class):
        self.name = name
        self.char_class = char_class

        stats = CLASS_STATS[char_class]

        self.max_hp = stats["max_hp"]
        self.hp = stats["max_hp"]
        self.max_mp = stats["max_mp"]
        self.mp = stats["max_mp"]

        self.base_atk = stats["atk"]
        self.atk = stats["atk"]
        self.base_defense = stats["def"]
        self.defense = stats["def"]
        self.base_spd = stats["spd"]
        self.spd = stats["spd"]

        self.level = 1
        self.xp = 0
        self.xp_next = 100
        self.gold = 0
        self.inventory = []
        self.status_effects = {}
        self.equipped = {
            "weapon": None,
            "armor": None,
            "boots": None,
            "ring": None,
            "accessory": None,
        }

    def level_up(self):
        self.level += 1
        self.xp_next = int(self.xp_next * 1.5)
        self.max_hp += 10
        self.max_mp += 8
        self.base_atk += 1
        self.atk = self.base_atk
        self.base_defense += 1
        self.defense = self.base_defense
        self.base_spd += 1
        self.spd = self.base_spd
        self.hp = self.max_hp
        self.mp = self.max_mp
        print(f"\n*** LEVEL UP! You are now level {self.level}! ***")
        print(f"  HP: +10 | MP: +8 | ATK: +1 | DEF: +1 | SPD: +1")

    def gain_xp(self, amount):
        self.xp += amount
        print(f"  You gained {amount} XP!")
        while self.xp >= self.xp_next:
            self.xp -= self.xp_next
            self.level_up()

    def take_damage(self, amount):
        damage = max(1, amount - self.defense)
        self.hp -= damage
        return damage

    def show_stats(self):
        print(f"\n  {self.name} the {self.char_class} — Level {self.level}")
        print(f"  HP:  {self.hp}/{self.max_hp}")
        print(f"  MP:  {self.mp}/{self.max_mp}")
        print(f"  ATK: {self.atk}  DEF: {self.defense}  SPD: {self.spd}")
        print(f"  XP:  {self.xp}/{self.xp_next}")
        print(f"  Gold: {self.gold}g")