<p align="center">
  <img src="https://img.shields.io/badge/ScayTux-v3.0-cyan?style=for-the-badge&logo=linux&logoColor=white" alt="ScayTux v3.0">
  <img src="https://img.shields.io/badge/Java-8%2B-orange?style=for-the-badge&logo=openjdk&logoColor=white" alt="Java 8+">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-blue?style=for-the-badge" alt="Platform">
  <img src="https://img.shields.io/badge/100-Combos-green?style=for-the-badge" alt="100 Combos">
  <img src="https://img.shields.io/badge/License-LGPL--3.0-green?style=for-the-badge" alt="License">
</p>

<h1 align="center">🐧 ScayTux</h1>
<h3 align="center">The Ultimate Tux Droid Controller</h3>

<p align="center">
  <strong>Bring your Tux Droid back to life on modern Windows 10/11 & Linux systems!</strong>
</p>

<p align="center">
  <a href="https://tuxdroid.com"><img src="https://img.shields.io/badge/Website-Tuxdroid.com-FF6A00?style=flat-square&logo=globe&logoColor=white" alt="Website"></a>
  <a href="https://github.com/Scayar/ScayTux"><img src="https://img.shields.io/badge/GitHub-Scayar%2FScayTux-black?style=flat-square&logo=github" alt="GitHub"></a>
  <a href="https://buymeacoffee.com/scayar"><img src="https://img.shields.io/badge/Support-Buy%20Me%20a%20Coffee-yellow?style=flat-square&logo=buy-me-a-coffee&logoColor=black" alt="Support"></a>
</p>

---

## 🌐 Website

**[Tuxdroid.com](https://tuxdroid.com)** — Full documentation, installation guides, 100 combos list, Telegram setup, TTS guide, troubleshooting, and more!

---

## 📋 Table of Contents

- [Website](#-website)
- [Overview](#-overview)
- [Features](#-features)
- [Hardware Requirements](#-hardware-requirements)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [First Run](#-first-run)
- [Usage](#-usage)
- [Commands Reference](#-commands-reference)
- [100 Combos (Full List)](#-100-combos-full-list)
- [Telegram Remote Control](#-telegram-remote-control)
- [Text-to-Speech & Audio](#-text-to-speech--audio)
- [Project Structure](#-project-structure)
- [Manual Build](#-manual-build)
- [Dependencies](#-dependencies)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [Author](#-author)
- [License](#-license)

---

## 🌟 Overview

**ScayTux** is a modern, cross-platform Java application that resurrects the classic **Tux Droid** robot for modern operating systems. No more outdated Python scripts or broken dependencies — pure Java power with 100 cinematic animations, Telegram bot, TTS, and a beautiful interactive CLI.

**What is Tux Droid?** A Linux mascot robot from ~2007 — a wireless USB-connected penguin figure that spins, flaps wings, blinks LED eyes, and speaks. The original software is abandoned; ScayTux brings it back to life on modern systems.

📚 **Learn more about Tux Droid:**
- [Wikipedia: Tux Droid](https://en.wikipedia.org/wiki/Tux_Droid) — Overview, specs, history
- [Ars Technica review (2008)](https://arstechnica.com/gadgets/2008/03/tux-droid-review/) — Make a penguin do your bidding
- [LWN.net (2006)](https://lwn.net/Articles/195808/) — Tux Droid brings Tux the penguin alive
- [eLinux.org](https://elinux.org/Tux_Droid) — Technical documentation

```
  ███████╗ ██████╗ █████╗ ██╗   ██╗████████╗██╗   ██╗██╗  ██╗
  ██╔════╝██╔════╝██╔══██╗╚██╗ ██╔╝╚══██╔══╝██║   ██║╚██╗██╔╝
  ███████╗██║     ███████║ ╚████╔╝    ██║   ██║   ██║ ╚███╔╝ 
  ╚════██║██║     ██╔══██║  ╚██╔╝     ██║   ██║   ██║ ██╔██╗ 
  ███████║╚██████╗██║  ██║   ██║      ██║   ╚██████╔╝██╔╝ ██╗
  ╚══════╝ ╚═════╝╚═╝  ╚═╝   ╚═╝      ╚═╝    ╚═════╝ ╚═╝  ╚═╝
```

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| ⚡ **Cross-Platform** | Single codebase for Windows 10/11 and Linux (Ubuntu/Debian) |
| 📱 **Telegram Remote** | Control your Tux from anywhere via inline-keyboard Telegram Bot |
| 🎭 **100 Combos** | 90 animation combos + 10 music+dance combos |
| 🗣️ **Text-to-Speech** | Windows: PowerShell • Linux: espeak with multiple voices |
| 🎵 **Music Player** | Play MP3s through Tux with synchronized dancing |
| 🔌 **Plug & Play** | Auto-detects USB dongle (VID: 0x03eb, PID: 0xFF07) |
| ⌨️ **Interactive CLI** | Beautiful ANSI-colored menu system |
| 🦅 **Full Motor Control** | Eyes, Mouth, Wings, Spin, LED with smooth animations |

---

## 🔧 Hardware Requirements

| Item | Description |
|------|-------------|
| **Tux Droid** | The penguin robot (with batteries) |
| **USB Dongle** | "Fishtank" dongle (VID: 0x03eb, PID: 0xFF07) |
| **USB Cable** | Connect dongle to your computer |

---

## 🚀 Quick Start

### Windows (One-Click)

```bash
git clone https://github.com/Scayar/ScayTux
cd ScayTux
START_WINDOWS.bat
```

> **Automatic**: Installs portable Maven, builds project, launches Interactive Mode.

### Linux (One-Command)

```bash
git clone https://github.com/Scayar/ScayTux
cd ScayTux
chmod +x START_LINUX.sh && ./START_LINUX.sh
```

> **Automatic**: Installs OpenJDK, Maven, espeak, libhidapi, configures udev rules.

### Manual Build (Any Platform)

```bash
git clone https://github.com/Scayar/ScayTux
cd ScayTux
mvn clean package -DskipTests
java -jar target/ScayTux.jar
```

---

## 📦 Installation

### Prerequisites

| Platform | Requirement | How to Install |
|----------|-------------|----------------|
| **All** | Java 8+ | [Adoptium](https://adoptium.net/) or [Oracle JDK](https://www.oracle.com/java/technologies/downloads/) |
| **All** | Maven 3.6+ | Auto-installed by launcher scripts |
| **Linux** | libhidapi | `sudo apt install libhidapi-hidraw0 libhidapi-dev` |
| **Linux** | espeak (TTS) | `sudo apt install espeak` |

### Linux USB Permissions

The launcher script auto-configures this. For manual setup:

```bash
# Create udev rule
sudo bash -c 'cat > /etc/udev/rules.d/99-tuxdroid.rules << EOF
SUBSYSTEM=="usb", ATTR{idVendor}=="03eb", ATTR{idProduct}=="ff07", MODE="0666", GROUP="plugdev"
KERNEL=="hidraw*", ATTR{idVendor}=="03eb", ATTR{idProduct}=="ff07", MODE="0666", GROUP="plugdev"
EOF'

sudo udevadm control --reload-rules
sudo udevadm trigger
sudo usermod -aG plugdev $USER
# Log out and back in
```

---

## 🎬 First Run

1. **Plug in** the Tux Droid USB dongle.
2. **Run** `START_WINDOWS.bat` (Windows) or `./START_LINUX.sh` (Linux).
3. **Choose** from the main menu:
   - `1` — Interactive Menu (browse and run 100 combos)
   - `2` — Manual/REPL Mode (type commands freely)
   - `3` — Telegram Control (set up remote control)
   - `4` — Exit

---

## 🎮 Usage

### Interactive Mode (Default)

```bash
java -jar target/ScayTux.jar
```

### Command-Line Mode

```bash
# Basic controls
java -jar target/ScayTux.jar --flap
java -jar target/ScayTux.jar --eyes true
java -jar target/ScayTux.jar --blink 5
java -jar target/ScayTux.jar --spin left --val 100

# Text-to-Speech
java -jar target/ScayTux.jar --say "Hello World"

# Play music with dance
java -jar target/ScayTux.jar --play assets/audio/billie.mp3

# Run combo (1-100)
java -jar target/ScayTux.jar --combo 14

# List devices
java -jar target/ScayTux.jar --list

# Debug mode
java -jar target/ScayTux.jar --debug
```

---

## 📚 Commands Reference

### CLI Arguments

| Flag | Description | Example |
|------|-------------|---------|
| `-i, --interactive` | Force interactive mode | `-i` |
| `--flap` | Flap wings | `--flap` |
| `--eyes <bool>` | Open (true) or close (false) eyes | `--eyes true` |
| `--blink <n>` | Blink eyes N times | `--blink 5` |
| `--mouth <bool>` | Open or close mouth | `--mouth true` |
| `--talk <n>` | Move mouth N times | `--talk 10` |
| `--spin <dir>` | Spin left or right | `--spin left` |
| `--val <n>` | Duration/loops for spin | `--val 100` |
| `--led <color>` | LED: 1=Red, 2=Blue, 3=Yellow | `--led 2` |
| `--intensity <n>` | LED intensity (0-255) | `--intensity 255` |
| `--say <text>` | Speak with TTS | `--say "Hello"` |
| `--combo <id>` | Run combo **1-100** | `--combo 49` |
| `--play <file>` | Play MP3 and dance | `--play song.mp3` |
| `-l, --list` | Check USB connection | `-l` |
| `-d, --debug` | Debug HID monitor | `-d` |
| `--spin-doctor` | Motor diagnostic | `--spin-doctor` |

---

## 🎭 100 Combos (Full List)

### Animation Combos (1-90)

| ID | Name | ID | Name | ID | Name |
|----|------|----|------|----|------|
| 1 | Royal Entrance | 31 | Ninja Silent | 61 | Weatherman |
| 2 | Bird Flex | 32 | Wake Ninja | 62 | Fitness Coach |
| 3 | Brain Loading | 33 | JumpScare | 63 | Alarm Clock |
| 4 | Sleep Mode | 34 | Sad Apology | 64 | Moonwalk |
| 5 | Hacker Alert | 35 | Switch OFF | 65 | Karate Chop |
| 6 | Police Mode | 36 | Magic Portal | 66 | News Anchor |
| 7 | Shy Bird | 37 | Taunting | 67 | Evil Villain |
| 8 | Laugh Mode | 38 | Game Won | 68 | Cheerleader |
| 9 | Kiss | 39 | Game Lost | 69 | Ghostly Haunt |
| 10 | Bird Crying | 40 | Loading 100% | 70 | Cowboy Duel |
| ... | ... | ... | ... | ... | ... |
| 51 | Disco Fever | 71 | Science Lab | 81 | Space Explorer |
| 52 | Morning Stretch | 72 | Royal Wave | 82 | Chef Kiss |
| 53 | Pirate Captain | 73 | Breakdance | 83 | Drill Sergeant |
| 54 | Opera Singer | 74 | Sneezing Fit | 84 | Morse Code |
| 55 | Counting Sheep | 75 | Photo Pose | 85 | Surfer Dude |
| 56 | Thunder Storm | 76 | Hypnotize | 86 | Orchestra Conductor |
| 57 | Zen Meditation | 77 | Traffic Cop | 87 | Spy Mode |
| 58 | Rocket Launch | 78 | Submarine | 88 | Fortune Teller |
| 59 | Penguin Walk | 79 | Birthday Party | 89 | Heavyweight Champ |
| 60 | Time Bomb | 80 | Mime Artist | 90 | Penguin Shuffle |

> **Browse all 100**: Run interactive mode → "Show All 100 Combos" • Or visit [tuxdroid.com/docs/combos](https://tuxdroid.com/docs/combos)

### Music + Dance Combos (91-100)

| ID | Name | Song File |
|----|------|-----------|
| 91 | Michael Jackson | billie.mp3 |
| 92 | Chicken Dance | chicken.mp3 |
| 93 | Syrian Dabkah | Suirian dabkah.mp3 |
| 94 | Crazy Mode | crazy.mp3 |
| 95 | Say My Name | Say My Name.mp3 |
| 96 | Robot Rock | robot-rock.mp3 *(add to assets/audio/)* |
| 97 | Macarena | macarena.mp3 *(add to assets/audio/)* |
| 98 | Egyptian Walk | egyptian.mp3 *(add to assets/audio/)* |
| 99 | Cha Cha Slide | cha-cha.mp3 *(add to assets/audio/)* |
| 100 | Tux Anthem | tux-anthem.mp3 *(add to assets/audio/)* |

Place MP3 files in `assets/audio/` to enable music combos 91-100.

---

## 📱 Telegram Remote Control

Control your Tux Droid from anywhere!

### Setup (Step by Step)

1. **Create Bot**: Message [@BotFather](https://t.me/BotFather) on Telegram → `/newbot` → Follow prompts → Copy the **bot token**.
2. **Get Chat ID**: Message [@userinfobot](https://t.me/userinfobot) → `/start` → Copy your **Chat ID**.
3. **Configure ScayTux**:
   - Copy `telegram_config.example.json` to `telegram_config.json`
   - Edit `telegram_config.json` and add your `botToken` and `chatId`
   - Or run ScayTux → `3. Telegram Control` → `1. Configure Bot` and enter them interactively
4. **Start Bot**: Run ScayTux → `3. Telegram Control` → `2. Start Bot`

### Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | Show main menu |
| `/connect` | Connect to Tux Droid |
| `/flap` | Flap wings |
| `/blink` | Blink eyes |
| `/dance` | Dance animation |
| `/say <text>` | Make Tux speak |
| `/combo1` to `/combo100` | Run any combo |
| `/stop` | Stop music |

---

## 🗣️ Text-to-Speech & Audio

- **Windows**: Uses PowerShell (native SAPI voice)
- **Linux**: Uses espeak (`sudo apt install espeak`)
- **Voices**: NORMAL, WHISPER, ANGRY, SAD, CUTE, ROBOT, ANNOUNCER
- **Audio**: MP3 playback via JLayer; place files in `assets/audio/`

---

## 📁 Project Structure

```
ScayTux/
├── START_WINDOWS.bat         # Windows launcher
├── START_LINUX.sh            # Linux launcher
├── pom.xml                   # Maven config
├── telegram_config.example.json  # Template (copy to telegram_config.json)
├── telegram_config.json      # Your config (gitignored - add token here)
│
├── src/main/java/.../jtuxdriver/
│   ├── cli/                  # Main, InteractiveMode, Debug
│   ├── core/                 # HidTransport, UsbTransport
│   ├── telegram/             # TelegramController, TelegramManager
│   ├── TuxDroid.java         # Tux control API
│   ├── TuxCombos.java        # 100 combo implementations
│   ├── Command.java          # USB packet factory
│   ├── AudioPlayer.java      # MP3 player
│   ├── TTS.java              # Text-to-Speech
│   └── USBDefines.java       # USB constants
│
├── assets/audio/             # MP3 files (billie.mp3, chicken.mp3, etc.)
├── docs/                     # COMMAND_REFERENCE.md, LICENSE
└── website/                  # Tuxdroid.com (Next.js)
    ├── src/app/              # Pages
    ├── src/components/      # UI components
    └── public/images/       # Logo, assets
```

---

## 🔨 Manual Build

```bash
# Build JAR
mvn clean package -DskipTests

# Run
java -jar target/ScayTux.jar

# Run with options
java -jar target/ScayTux.jar --combo 14 --say "Hello"
```

---

## 📦 Dependencies

| Library | Purpose |
|---------|---------|
| [hid4java](https://github.com/gary-rowe/hid4java) | USB HID |
| [Picocli](https://picocli.info/) | CLI parsing |
| [JLayer](http://www.javazoom.net/javalayer/) | MP3 |
| [TelegramBots](https://github.com/rubenlagus/TelegramBots) | Telegram API |
| [Gson](https://github.com/google/gson) | JSON config |

---

## 🔧 Troubleshooting

### Windows

| Issue | Solution |
|-------|----------|
| "Java is not installed" | Download from [Adoptium](https://adoptium.net/) |
| Maven download/rename fails | Delete `tools/` folder and retry, or [install Maven manually](https://maven.apache.org/download.cgi) |
| "Build failed" | Delete `target/` and retry |
| "Device not found" | Try different USB port; replug dongle |
| No audio from Tux | Check Windows mixer for "TuxDroid-Audio" |

### Linux

| Issue | Solution |
|-------|----------|
| USB "Permission denied" | Run launcher (auto udev) or add udev rules manually |
| "espeak not found" | `sudo apt install espeak` |
| "libhidapi not found" | `sudo apt install libhidapi-hidraw0 libhidapi-dev` |

### Common

| Issue | Solution |
|-------|----------|
| Tux not responding | Unplug → wait 5s → replug |
| Spin stutters | Use `--val 100` or higher |
| Telegram bot not connecting | Check token, chat ID, internet, firewall |

**More help**: [tuxdroid.com/docs/troubleshooting](https://tuxdroid.com/docs/troubleshooting)

---

## 🤝 Contributing

1. Fork the repository
2. Create a branch (`git checkout -b feature/amazing`)
3. Commit (`git commit -m 'Add amazing feature'`)
4. Push (`git push origin feature/amazing`)
5. Open a Pull Request

---

## 👨‍💻 Author

| | |
|---|---|
| **Name** | Scayar |
| **GitHub** | [github.com/Scayar](https://github.com/Scayar) |
| **Website** | [Tuxdroid.com](https://tuxdroid.com) |
| **Telegram** | [@im_scayar](https://t.me/im_scayar) |
| **Support** | [Buy Me a Coffee ☕](https://buymeacoffee.com/scayar) |

---

## ❤️ Support

- ⭐ **Star** this repository
- ☕ [**Buy me a coffee**](https://buymeacoffee.com/scayar)
- 📢 **Share** with other Tux Droid owners
- 🐛 **Report bugs** via [GitHub Issues](https://github.com/Scayar/ScayTux/issues)

---

## 📄 License

**GNU Lesser General Public License v3.0 (LGPL-3.0)** — see [docs/LICENSE](docs/LICENSE).

---

<p align="center">
  <strong>Made with ♥ by Scayar</strong><br>
  <em>"Tux Droid Never Dies!"</em> 🐧💙
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Tux%20Droid-Resurrected-success?style=for-the-badge" alt="Tux Droid Resurrected">
</p>
