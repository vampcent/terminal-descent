import random
from player import Player, CLASS_ABILITIES
from enemy import Enemy, BURN_IMMUNE, BURN_WEAK
from loot import get_equipped_set, SETS

def apply_status(target, effect, value, max_stacks):
    if not hasattr(target, 'status_effects'):
        target.status_effects = {}
    current = target.status_effects.get(effect, {})
    stacks = min(current.get('stacks', 0) + 1, max_stacks)
    target.status_effects[effect] = {
        'stacks': stacks,
        'value': value,
        'turns': current.get('turns', 0) + 5 if effect == 'poison' else current.get('turns', 0) + 3,
    }
    print(f"  {effect.upper()} applied! ({stacks} stack(s))")

def apply_burn(enemy, stacks=2, ignore_immune=False):
    if enemy.name in BURN_IMMUNE and not ignore_immune:
        print(f"  {enemy.name} is immune to burn! The flask fizzles out.")
        return False
    multiplier = 2 if enemy.name in BURN_WEAK else 1
    value = 10 * multiplier
    for _ in range(stacks):
        apply_status(enemy, 'burn', value, 3)
    if multiplier == 2:
        print(f"  {enemy.name} is weak to fire! The flames spread violently!")
    return True

def tick_statuses(target, eternal_inferno=False):
    if not hasattr(target, 'status_effects'):
        return
    expired = []
    for effect, data in list(target.status_effects.items()):
        if effect == 'poison':
            dmg = int(data['value'] * data['stacks'])
            target.hp -= dmg
            print(f"  Poison deals {dmg} damage! ({data['stacks']} stack(s))")
        elif effect == 'burn':
            dmg = int(data['value'] * data['stacks'])
            target.hp -= dmg
            print(f"  Burn deals {dmg} damage! ({data['stacks']} stack(s))")
        data['turns'] -= 1
        if data['turns'] <= 0 and not (effect == 'burn' and eternal_inferno):
            expired.append(effect)
    for effect in expired:
        del target.status_effects[effect]
        print(f"  {effect.upper()} has worn off.")

ABILITIES = {
    "Power Strike":  {"cost": 15, "type": "damage",  "multiplier": 2.0, "status": None},
    "Shield Bash":   {"cost": 25, "type": "damage",  "multiplier": 1.0, "status": ("atk_down", 5, 3)},
    "War Cry":       {"cost": 40, "type": "buff",    "multiplier": 0,   "status": ("atk_up", 5, 3)},
    "Backstab":      {"cost": 15, "type": "damage",  "multiplier": 2.5, "status": None},
    "Smoke Bomb":    {"cost": 25, "type": "buff",    "multiplier": 0,   "status": ("spd_up", 0, 2)},
    "Poison Blade":  {"cost": 40, "type": "damage",  "multiplier": 1.0, "status": ("poison", 0, 5)},
    "Fireball":      {"cost": 15, "type": "damage",  "multiplier": 2.0, "status": None},
    "Frost Nova":    {"cost": 25, "type": "damage",  "multiplier": 1.0, "status": ("def_down", 3, 3)},
    "Arcane Burst":  {"cost": 40, "type": "double",  "multiplier": 1.0, "status": None},
}

def get_active_set_bonus(player):
    set_name, set_data = get_equipped_set(player)
    if set_data:
        return set_data["bonus"]
    return None

def use_ability(player, enemy, ability, set_bonus=None):
    data = ABILITIES.get(ability)
    if not data:
        print("  Unknown ability!")
        return False

    cost = data["cost"]

    # forbidden mastery — 80% mp cost reduction
    if set_bonus == "forbidden_mastery":
        cost = max(1, int(cost * 0.2))

    if player.mp < cost:
        print("  Not enough MP!")
        return False
    player.mp -= cost

    atype = data["type"]
    mult  = data["multiplier"]
    status = data["status"]

    def do_hit(multiplier):
        dmg = enemy.take_damage(int(player.atk * multiplier))
        # on hit weapon effects
        weapon = player.equipped.get("weapon")
        if weapon:
            handle_on_hit(player, enemy, weapon, set_bonus)
        return dmg

    if atype == "damage":
        dmg = do_hit(mult)
        print(f"  {ability}! You deal {dmg} damage!")
        # forbidden mastery 15% double hit
        if set_bonus == "forbidden_mastery" and random.randint(1,100) <= 15:
            dmg2 = do_hit(mult)
            print(f"  Forbidden Mastery! The spell echoes for {dmg2} extra damage!")

    elif atype == "double":
        dmg1 = do_hit(mult)
        dmg2 = do_hit(mult)
        print(f"  {ability}! Two hits for {dmg1} and {dmg2} damage!")
        if set_bonus == "forbidden_mastery" and random.randint(1,100) <= 15:
            dmg3 = do_hit(mult)
            print(f"  Forbidden Mastery! A third strike for {dmg3} damage!")

    elif atype == "buff":
        print(f"  {ability}!")

    if status:
        effect, value, max_stacks = status
        if effect == "poison":
            value = int(player.atk * 0.20)
        elif effect == "spd_up":
            value = player.spd
        apply_status(enemy if effect in ("atk_down", "def_down", "poison") else player, effect, value, max_stacks)

    return True

def handle_on_hit(player, enemy, weapon, set_bonus=None):
    on_hit = weapon.get("on_hit")
    if not on_hit:
        return

    if on_hit == "poison_half":
        if not hasattr(player, 'poison_half_counter'):
            player.poison_half_counter = 0
        player.poison_half_counter += 1
        if player.poison_half_counter >= 2:
            player.poison_half_counter = 0
            poison_val = int(player.atk * 0.20)
            apply_status(enemy, 'poison', poison_val, 5)
            print(f"  Spider Fang Blade drips poison!")

    elif on_hit == "def_down":
        apply_status(enemy, 'def_down', 3, 3)
        print(f"  Banewraith Blade corrodes the enemy's armour!")

    elif on_hit == "poison_stack":
        poison_val = int(player.atk * 0.20)
        apply_status(enemy, 'poison', poison_val, 5)
        print(f"  Corruption Staff seeps poison!")

    elif on_hit == "self_damage_10":
        if random.randint(1, 100) <= 10:
            dmg = max(1, int(player.hp * 0.05))
            player.hp -= dmg
            print(f"  The Rusty Halberd cuts you for {dmg} damage!")

    elif on_hit == "spd_up_0.1":
        increment = 0.1
        if set_bonus == "mind_ascendant":
            increment = 0.2
        player.base_spd += increment
        player.spd = player.base_spd
        print(f"  Blade of the Elder Mind sharpens your reflexes! SPD +{increment:.1f}")

    elif on_hit == "burn_stack":
        eternal = set_bonus == "eternal_inferno"
        apply_burn(enemy, stacks=1, ignore_immune=eternal)
        print(f"  The Eternal Flame Blade ignites the enemy!")

    elif on_hit == "instant_kill_1":
        chance = 5 if set_bonus == "void_incarnate" else 1
        if random.randint(1, 100) <= chance:
            enemy.hp = 0
            print(f"  The Blade of the Abyss tears through reality! Instant kill!")

def handle_on_kill(player, enemy, set_bonus=None):
    weapon = player.equipped.get("weapon")
    if weapon and weapon.get("on_kill") == "atk_up_2":
        player.base_atk += 2
        player.atk = player.base_atk
        print(f"  Souldrainer feeds on the kill! ATK permanently +2!")

    # reapers pact set bonus
    if set_bonus == "reapers_pact":
        if player.hp <= int(player.max_hp * 0.30):
            player.base_atk += 2
            player.atk = player.base_atk
            print(f"  Reaper's Pact! ATK permanently +2!")

def handle_accessory_on_kill(player):
    accessory = player.equipped.get("accessory")
    if not accessory:
        return
    special = accessory.get("special", "")
    if special == "hp_restore_5_on_kill":
        restore = int(player.max_hp * 0.05)
        player.hp = min(player.hp + restore, player.max_hp)
        print(f"  Amulet of the Wild restores {restore} HP!")
    elif special == "hp_restore_15_on_kill":
        restore = int(player.max_hp * 0.15)
        player.hp = min(player.hp + restore, player.max_hp)
        print(f"  Shield of Eternal Night restores {restore} HP!")

def use_item(player, enemy=None):
    consumables = [item for item in player.inventory if item["slot"] == "consumable"]
    if not consumables:
        print("  No items to use!")
        return
    print("\n  Choose an item:")
    for i, item in enumerate(consumables, 1):
        print(f"  {i}. {item['name']} — {item['desc']}")
    choice = input("\n  > ").strip()
    if not choice.isdigit() or not (1 <= int(choice) <= len(consumables)):
        print("  Invalid choice, no item used.")
        return
    item = consumables[int(choice) - 1]

    if "hp" in item["bonus"]:
        restore = int(player.max_hp * item["bonus"]["hp"])
        player.hp = min(player.hp + restore, player.max_hp)
        print(f"  Used {item['name']}! Restored {restore} HP.")
    if "mp" in item["bonus"]:
        restore = int(player.max_mp * item["bonus"]["mp"])
        player.mp = min(player.mp + restore, player.max_mp)
        print(f"  Used {item['name']}! Restored {restore} MP.")
    if "hp_set" in item["bonus"]:
        player.hp = max(1, int(player.max_hp * item["bonus"]["hp_set"]))
        print(f"  You drink the {item['name']}... your vision goes red.")
    if "atk_up" in item["bonus"]:
        apply_status(player, 'atk_up', item["bonus"]["atk_up"], 3)
        print(f"  Used {item['name']}! ATK increased!")
    if "def_up" in item["bonus"]:
        apply_status(player, 'def_up', item["bonus"]["def_up"], 3)
        print(f"  Used {item['name']}! DEF increased!")
    if "spd_up" in item["bonus"]:
        apply_status(player, 'spd_up', item["bonus"]["spd_up"], 3)
        print(f"  Used {item['name']}! SPD increased!")
    if "poison" in item["bonus"] and enemy:
        poison_val = int(player.atk * 0.20)
        for _ in range(2):
            apply_status(enemy, 'poison', poison_val, 5)
        print(f"  Used {item['name']}! Enemy poisoned!")
    if "burn" in item["bonus"] and enemy:
        apply_burn(enemy, stacks=2)
    if "def_down" in item["bonus"] and enemy:
        for _ in range(2):
            apply_status(enemy, 'def_down', item["bonus"]["def_down"], 3)
        print(f"  Used {item['name']}! Enemy defence reduced!")

    player.inventory.remove(item)

def choose_ability(player, enemy, set_bonus=None):
    abilities = CLASS_ABILITIES[player.char_class]
    print("\n  Choose an ability:")
    for i, ab in enumerate(abilities, 1):
        cost = ABILITIES[ab]["cost"]
        if set_bonus == "forbidden_mastery":
            cost = max(1, int(cost * 0.2))
        mp_note = "" if player.mp >= cost else " (not enough MP)"
        print(f"  {i}. {ab} ({cost} MP){mp_note}")
    choice = input("\n  > ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(abilities):
        ability = abilities[int(choice) - 1]
        use_ability(player, enemy, ability, set_bonus)
    else:
        print("  Invalid choice, you hesitate!")

def show_turn_header(player, enemy, set_bonus=None):
    abilities = CLASS_ABILITIES[player.char_class]
    consumables = [item for item in player.inventory if item["slot"] == "consumable"]

    print(f"\n  {'='*40}")
    print(f"  {enemy.name}")
    print(f"  HP: {enemy.hp}/{enemy.max_hp}")
    print(f"  {'='*40}")
    print(f"\n  {player.name} | HP: {player.hp}/{player.max_hp} | MP: {player.mp}/{player.max_mp}")

    if set_bonus:
        print(f"  Set Bonus: {set_bonus.replace('_', ' ').title()}")

    print(f"\n  Abilities:")
    for ab in abilities:
        cost = ABILITIES[ab]["cost"]
        if set_bonus == "forbidden_mastery":
            cost = max(1, int(cost * 0.2))
        mp_note = "" if player.mp >= cost else " (not enough MP)"
        print(f"    - {ab} ({cost} MP){mp_note}")

    if consumables:
        print(f"\n  Inventory:")
        for item in consumables:
            print(f"    - {item['name']} — {item['desc']}")
    else:
        print(f"\n  Inventory: empty")

    print(f"\n  What will you do?")
    print(f"  1. Attack")
    print(f"  2. Ability")
    print(f"  3. Use Item")
    print(f"  4. Attack + Use Item")
    print(f"  5. Ability + Use Item")

def combat(player, enemy):
    print(f"\n  A {enemy.name} appears!")
    print(f"  HP: {enemy.hp} | ATK: {enemy.atk} | DEF: {enemy.defense}\n")

    set_bonus = get_active_set_bonus(player)
    eternal_inferno = set_bonus == "eternal_inferno"
    first_hit_blocked = False

    # igris oathbound shield — block first hit
    accessory = player.equipped.get("accessory")
    if accessory and accessory.get("special") == "block_first_hit":
        first_hit_blocked = True

    while player.hp > 0 and enemy.is_alive():

        tick_statuses(enemy, eternal_inferno=eternal_inferno)
        if not enemy.is_alive():
            break

        if 'def_down' in enemy.status_effects:
            reduction = enemy.status_effects['def_down']['value'] * enemy.status_effects['def_down']['stacks']
            enemy.defense = max(0, int(enemy.base_defense - reduction))
        else:
            enemy.defense = enemy.base_defense

        bonus_atk = 0
        bonus_def = 0
        bonus_spd = 0
        if player.status_effects:
            if 'atk_up' in player.status_effects:
                bonus_atk = player.status_effects['atk_up']['value'] * player.status_effects['atk_up']['stacks']
            if 'def_up' in player.status_effects:
                bonus_def = player.status_effects['def_up']['value'] * player.status_effects['def_up']['stacks']
            if 'spd_up' in player.status_effects:
                bonus_spd = player.status_effects['spd_up']['value'] * player.status_effects['spd_up']['stacks']

        player.atk = int(player.base_atk + bonus_atk)
        player.defense = int(player.base_defense + bonus_def)
        player.spd = int(player.base_spd + bonus_spd)

        # last stand set bonus — double ATK and DEF below 20% HP
        if set_bonus == "last_stand" and player.hp <= int(player.max_hp * 0.20):
            player.atk *= 2
            player.defense *= 2
            print(f"  Last Stand! ATK and DEF doubled!")

        show_turn_header(player, enemy, set_bonus)
        action = input("\n  > ").strip()

        if action == "1":
            dmg = enemy.take_damage(player.atk)
            print(f"  You attack for {dmg} damage!")
            handle_on_hit(player, enemy, player.equipped.get("weapon", {}), set_bonus)

        elif action == "2":
            choose_ability(player, enemy, set_bonus)

        elif action == "3":
            use_item(player, enemy)

        elif action == "4":
            dmg = enemy.take_damage(player.atk)
            print(f"  You attack for {dmg} damage!")
            handle_on_hit(player, enemy, player.equipped.get("weapon", {}), set_bonus)
            if not enemy.is_alive():
                break
            use_item(player, enemy)

        elif action == "5":
            choose_ability(player, enemy, set_bonus)
            if not enemy.is_alive():
                break
            use_item(player, enemy)

        else:
            print("  Invalid choice, you hesitate!")

        if not enemy.is_alive():
            handle_on_kill(player, enemy, set_bonus)
            handle_accessory_on_kill(player)
            break

        tick_statuses(player)
        print(f"\n  --- {enemy.name}'s turn ---")

        enemy_atk = enemy.atk
        if 'atk_down' in enemy.status_effects:
            reduction = enemy.status_effects['atk_down']['value'] * enemy.status_effects['atk_down']['stacks']
            enemy_atk = max(1, int(enemy.atk - reduction))

        # fire resist ring — 10% less damage from burn immune enemies
        ring = player.equipped.get("ring")
        if ring and ring.get("special") == "fire_resist_10" and enemy.name in BURN_IMMUNE:
            enemy_atk = int(enemy_atk * 0.9)

        # unyielding stone set bonus — 20% chance to take 0 damage
        if set_bonus == "unyielding_stone" and random.randint(1, 100) <= 20:
            print(f"  Unyielding Stone! You absorb the hit!")
        elif first_hit_blocked:
            print(f"  Igris's Oathbound Shield blocks the attack!")
            first_hit_blocked = False
        else:
            evade_chance = max(0, (player.spd / (player.spd + enemy.atk)) * 100 - 20)

            # evasion bonuses from equipment
            armor = player.equipped.get("armor")
            boots = player.equipped.get("boots")
            if armor and armor.get("special") == "evasion_10":
                evade_chance += 10
            if boots and boots.get("special") == "evasion_5":
                evade_chance += 5

            if random.randint(1, 100) <= evade_chance:
                print(f"  You dodge the {enemy.name}'s attack!")
            else:
                # burn resist accessory
                dmg = player.take_damage(enemy_atk)
                accessory = player.equipped.get("accessory")
                if accessory and accessory.get("special") == "burn_resist_50":
                    dmg = int(dmg * 0.5)
                    player.hp += int(dmg * 0.5)
                # deathless shroud check
                if player.hp <= 0:
                    armor = player.equipped.get("armor")
                    if armor and armor.get("special") == "death_save" and not armor.get("used"):
                        player.hp = 1
                        armor["used"] = True
                        print(f"  The Deathless Shroud saves you! It crumbles to dust.")
                        player.equipped["armor"] = None
                    else:
                        print(f"  {enemy.name} hits you for {dmg} damage!")
                        break
                else:
                    print(f"  {enemy.name} hits you for {dmg} damage!")

                # reflect damage — shield of the deep earth
                accessory = player.equipped.get("accessory")
                if accessory and accessory.get("special") == "reflect_10":
                    reflect = max(1, int(dmg * 0.1))
                    enemy.hp -= reflect
                    print(f"  Reflected {reflect} damage!")

    if player.hp <= 0:
        print(f"\n  You have been defeated by {enemy.name}...")
        return "dead"
    else:
        print(f"\n  You defeated {enemy.name}!")
        player.gain_xp(enemy.xp)
        player.gold += enemy.gold
        print(f"  +{enemy.xp} XP | +{enemy.gold} gold")

        # void incarnate — 5% skip next combat
        if set_bonus == "void_incarnate" and random.randint(1, 100) <= 15:
            print(f"  Void Incarnate! The next combat will be skipped.")
            player.skip_next_combat = True

        return "victory"