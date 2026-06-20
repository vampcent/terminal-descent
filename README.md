# Terminal Descent

A text-based roguelike dungeon crawler RPG playable entirely in your terminal, built in Python.

Descend through an endless dungeon, floor by floor. Fight enemies, collect loot, build your character and survive as long as you can. There is no escape. The only way out is death.

---

## Features

- **Three playable classes** — Warrior, Rogue, and Mage, each with unique stats and abilities
- **Endless dungeon** — floors go on forever, enemies scale endlessly with depth
- **Turn-based combat** — attack, use class abilities and consume items
- **RPG progression** — gain XP, level up, and watch your stats grow with every fight
- **Loot system** — weapons, armour, boots, rings, and consumables drop from enemies
- **Equipment slots** — equip and swap gear to shape your build
- **Boss encounters** — a powerful boss awaits every 10 floors cleared
- **Tavern hub** — clear a full floor to earn a rest; spend gold on healing and supplies before descending
- **Permadeath** — when you die, it's over. How deep can you go?

---

## Getting Started

### Requirements

- Python 3.8+
- [colorama](https://pypi.org/project/colorama/) for coloured terminal output

### Installation

```bash
git clone https://github.com/YOUR_USERNAME/terminal-descent.git
cd terminal-descent
pip install -r requirements.txt
python main.py
```

---

## How to Play

1. Create your hero - choose a name and class
2. Fight your way through every room on the floor
3. Clear the entire floor to unlock the tavern
4. Visit the tavern to rest, restock, and spend your gold
5. Descend to the next floor and repeat
6. Every 10 floors, face a boss - defeat it or die trying
7. There is no win condition. Descend until you fall.

---

## Project Structure

```
terminal_descent/
├── main.py          # Entry point and game loop
├── game.py          # Core game state and floor logic
├── player.py        # Player class — stats, levelling, inventory
├── enemy.py         # Enemy class and scaling enemy tables
├── combat.py        # Turn-based combat loop
├── loot.py          # Loot tables and item drops
├── tavern.py        # Tavern menu and shop logic
├── display.py       # All terminal output and formatting
└── data/
    ├── enemies.json # Enemy definitions
    └── items.json   # Item and loot definitions
```

---

## Roadmap

- [ ] More classes (Paladin, Ranger, Necromancer)
- [ ] Passive skill trees per class
- [ ] Procedurally generated room descriptions
- [ ] Shrine rooms with risk/reward choices

---

## Built With

- Python 3
- colorama

---

*A personal project built to learn Python, OOP, and game logic - and to have something fun to play in the terminal.*
