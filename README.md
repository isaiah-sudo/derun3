# ⚡ CyberSurge 3D

<div align="center">

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)
![Ursina Engine](https://img.shields.io/badge/engine-Ursina%208.3-cyan.svg)
![Framerate](https://img.shields.io/badge/framerate-60%20FPS%20Locked-brightgreen.svg)
![Theme](https://img.shields.io/badge/theme-Dark%20Synthwave-magenta.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-blueviolet.svg)

A high-speed, dark-themed 3D endless runner game built in Python with the **Ursina Engine**.

</div>

---

## 🎮 Game Modes

CyberSurge 3D features **two distinct game modes** selectable directly on the title screen:

### 1. 🏎️ **CLASSIC MODE (CRUISE)**
- **Balanced Acceleration**: Steady, controlled speed scaling.
- **Top Speed**: ~`85 KM/H`.
- **Standard Powerups**: Standard timers and single-layer shields.
- **Combo Cap**: Up to `8x` multiplier.

### 2. 🔥 **OVERDRIVE MODE (HYPER-SURGE)**
- **Extreme Speed Growth**: Over **4x faster acceleration**, scaling up to blistering top speeds of **`175+ KM/H`**!
- **Stacking Powerups**:
  - 🛡️ **Shield Stacking**: Pick up multiple shields to build up extra shield charges (`Shield x2`, `Shield x3`, `Shield x4`). Each hit deflects and consumes only 1 charge!
  - ⚡ **Hyperdrive Boost Stacking**: Multiple boost pickups stack duration and multiply top speed (with camera FOV warping up to `96`!).
  - 🧲 **Magnetic Flux Stacking**: Stacks magnetic duration and expands the suction radius up to `32m` across all lanes!
  - 💎 **Mega Combos**: Build combo multipliers up to **`32x`** for exponential scoring!
- **Dedicated Leaderboard**: Tracks separate high scores for Classic and Overdrive modes.

---

## 🕹️ Controls

| Key | Action |
| :--- | :--- |
| **`A` / `D`** or **`←` / `→`** | Steer & shift lanes (Left / Center / Right) |
| **`W` / `Space` / `↑`** | **Jump** over low laser hurdles |
| **`S` / `↓`** | **Slide / Dive** under overhead barriers |
| **`E` / `Left Shift`** | Activate **Hyperdrive Boost** |
| **`Tab` / `M`** | Toggle Game Mode on the Title Screen |
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

## 📦 Build Standalone Windows EXE

You can package the entire game into a standalone `.exe` without needing Python installed on the target machine:

### Option A: 1-Click Batch Script
Double click **`build_exe.bat`** (or run `.\build_exe.bat` in your terminal).

### Option B: Python Build Script
```bash
python build_exe.py
```

The output executable and asset folder will be generated at:
```
dist/CyberSurge3D/CyberSurge3D.exe
```

---

## 📄 License

Distributed under the [MIT License](LICENSE).
