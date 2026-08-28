# ⚡ CyberSurge 3D

<div align="center">

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)
![Ursina Engine](https://img.shields.io/badge/engine-Ursina%208.3-cyan.svg)
![Framerate](https://img.shields.io/badge/framerate-60%20FPS%20Locked-brightgreen.svg)
![Theme](https://img.shields.io/badge/theme-Dark%20Synthwave-magenta.svg)

A high-speed, dark-themed 3D endless runner game built in Python with the **Ursina Engine**.

</div>

---

## 🎮 Gameplay & Overview

In **CyberSurge 3D**, you pilot a high-tech hovercraft accelerating down an infinite procedural neon grid in deep space. Dodge laser hurdles, slide under high barriers, evade moving cyber-drones, and gather energy crystals to rack up massive score multipliers!

### 🕹️ Controls

| Key | Action |
| :--- | :--- |
| **`A` / `D`** or **`←` / `→`** | Steer & shift lanes (Left / Center / Right) |
| **`W` / `Space` / `↑`** | **Jump** over low laser hurdles |
| **`S` / `↓`** | **Slide / Dive** under overhead barriers |
| **`E` / `Left Shift`** | Activate **Hyperdrive Boost** (Invincibility & Mach speed) |
| **`Esc`** | Pause / resume game |
| **`Space` / `R`** | Instant retry on Game Over |

---

## 🚀 Installation & Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/your-username/derun3.git
cd derun3
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch the game
```bash
python main.py
```

---

## ✨ Features

- 🏎️ **Smooth 3D Flight Physics**: Dynamic banking rolls, jump arcs, and slide-crouching with real-time responsive camera tracking.
- 🌌 **Infinite Procedural Track & Dynamic Biomes**: Seamlessly traverses through multiple visual biomes (*Neon Metropolis*, *Solar Flare*, *Cyber Toxic*, *Deep Void*) with batch-combined mesh generation for maximum performance.
- 🔒 **Rock-Solid 60 FPS**: Clock-mode frame limiting and hardware VSync eliminate stutter, frame drops, and tearing.
- 💎 **Powerups & Pickups**:
  - **Energy Crystals**: Build up combo multiplier chains (up to **8x**).
  - **Shield Matrix**: Absorbs lethal impacts and grants invulnerability buffers.
  - **Magnetic Flux**: Pulls distant shards directly into your craft.
  - **Hyperdrive Boost**: Smashes through obstacles with screen shake and particle bursts.
- 🎨 **Garage / Ship Customization**: Select between multiple hovercraft skins (*Neon Blade*, *Solar Phantom*, *Toxic Viper*, *Dark Matter*).
- 🏆 **Local High Scores**: Automatically saves all-time high scores, runs played, and total distance in `scores.json`.

---

## 📁 Project Structure

```
derun3/
├── main.py              # Main entrypoint, game loop, and 60 FPS clock configuration
├── game/
│   ├── config.py        # Core constants, biome palettes, and vehicle skins
│   ├── player.py        # 3D Hovercraft player entity, physics, and banking roll
│   ├── track.py         # Procedural track generator, segment pooling & mesh combining
│   ├── obstacles.py     # Laser hurdles, high barriers, drones, and pylon hazards
│   ├── collectibles.py  # Energy crystals, shields, magnets, and boost pickups
│   ├── fx.py            # Camera shake trauma system and particle bursts
│   ├── ui.py            # HUD, start menu, pause overlay, and game over screens
│   └── highscores.py    # Local high score and run persistence
├── requirements.txt     # Python package dependencies
├── .gitignore           # Standard Python & engine ignore rules
├── LICENSE              # MIT Open Source License
└── README.md            # Project documentation
```

---

## 📄 License

Distributed under the [MIT License](LICENSE).
