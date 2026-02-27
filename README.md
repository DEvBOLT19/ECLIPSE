# ECLIPSE ⚔️

**ECLIPSE** is a **2D top-down action-adventure game** inspired by classic GBA titles like Pokémon and Hollow Knight.
The game follows **BOLT**, a calm and observant boy, on a journey to uncover the truth behind the mysterious disappearance of his village and confront dark forces threatening the kingdom.

Built entirely in **Python using Pygame**, ECLIPSE combines **exploration, combat, time travel, and story-driven cutscenes** for an immersive experience.

---

## 🌟 Features

- **Pokémon-style top-down movement**
- **Interactive NPCs** and companion system
- **Story-driven cutscenes** with dialogue boxes and scripted events
- **Time-travel mechanics** affecting past and present maps
- **Weapons, power-ups, and inventory system**
- **Mini-bosses and multi-phase final boss fights**
- **Dynamic maps**: village, city, castle, and their past versions
- **Emotional story arc**: confront a cursed father, uncover secrets, and restore villagers

---

## 🎮 Story Overview

BOLT trains as a swordsman in a quiet village under the kingdom’s rule.
Returning from practice one day, he discovers **the village completely abandoned**.

- Explore the city, meet companions like **Kiro**, and gain allies
- Discover the **Forgotten Swordsman** and recover your **Father’s Blade**
- Face the king’s daughter and a corrupted father
- Travel through **time** to solve puzzles and unlock hidden events
- Restore the kingdom and villagers while gaining new abilities

> Every decision, mission, and battle shapes BOLT’s journey toward uncovering the full truth.

---

## 🗂 Folder Structure

```text
ECLIPSE/
├─ assets/        # Sprites, tiles, music, and sound effects
├─ maps/          # CSV or JSON map layouts
├─ scripts/       # Game logic and mechanics
├─ story_scenes/  # Modular cutscenes and story events
├─ save_data/     # Save files for player progress
├─ README.md      # Project information
└─ requirements.txt
```

---

## ⚡ Controls

| Key | Action |
|-----|--------|
| Arrow Keys | Move BOLT |
| Space | Interact / Advance Dialogue / Trigger objectives |
| T | Time travel (unlocks in Chapter 6) |
| Enter | Toggle Menu |
| Esc | Quit Game |

---

## 🛠 Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/ECLIPSE.git
   cd ECLIPSE
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the game**

   ```bash
   python scripts/main.py
   ```

---

## 📦 Dependencies

- Python 3.10+
- Pygame

Install Pygame directly (optional):

```bash
pip install pygame
```

---

## 🎨 Assets

- Player sprites, NPCs, tiles, and items are located in `assets/`.
- Background music and SFX support the story experience.
- Assets are organized for straightforward expansion and modding.

---

## 📝 Contributing

Team BOLT welcomes contributions:

1. Fork the repository
2. Create a new branch (`feature/your-feature`)
3. Commit your changes with clear messages
4. Submit a pull request describing your additions

We encourage adding new story missions, cutscenes, and boss mechanics.

---

## ✅ Current Game Flow

- Chapter-based story progression from village mystery to final boss ending
- City/castle exploration, companion unlock, and time-travel reveal chapter
- Father curse boss fight and two-phase final queen battle
- Normal ending and true ending based on key item completion
- Auto-save to `save_data/save1.json` for chapter, location, timeline, and inventory state
