# 🐧 JTuxDriver: The Ultimate Tux Droid Controller

[![Java](https://img.shields.io/badge/Java-8%2B-orange)](https://www.java.com)
[![Maven](https://img.shields.io/badge/Maven-Built-blue)](https://maven.apache.org)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-lightgrey)]()
[![Status](https://img.shields.io/badge/Status-Revived-%2300ff00)]()

**Welcome to the resurrection of the Tux Droid!** 
This project brings the classic Linux mascot robot back to life on **modern Windows (10/11)** and **Linux (Ubuntu/Debian)** systems. No more old dependencies, no more broken Python scripts — just pure, fast Java power.

---

## 🚀 Super Easy Quick Start (المميزات)

### 🪟 Windows Users (One-Click!)

1. **Download** this repository (or `git clone`)
2. **Double-click** `START_WINDOWS.bat`
3. Wait for automatic setup (first time downloads Maven ~10MB)
4. **Done!** 🎉 The Interactive Console will open

> **Requirements:** Java 8+ (the script will tell you if it's missing)

### 🐧 Linux/Ubuntu Users (One-Command!)

1. Open Terminal
2. Navigate to the project folder
3. Run:
   ```bash
   chmod +x START_LINUX.sh && ./START_LINUX.sh
   ```
4. Follow the prompts (it will install missing packages automatically)
5. **Done!** 🎉

> **Requirements:** The script auto-installs: `openjdk-11-jdk`, `maven`, `espeak`, `libhidapi`

---

## ✨ Features (المميزات)

*   **⚡ Cross-Platform:** Single codebase runs on Windows and Linux
*   **🗣️ Text-to-Speech (TTS):** 
    *   **Windows:** Uses native PowerShell Speech Synthesis (No setup needed!)
    *   **Linux:** Uses `espeak` for lightweight speech
*   **🕺 Animation Engine:** Full control over:
    *   **Eyes:** Open, close, blink
    *   **Mouth:** Move while talking
    *   **Wings:** Flap up/down
    *   **Spin:** Rotate left/right
    *   **LED:** Color and intensity control
*   **🎵 Audio Player:** Play MP3 files directly through Tux Droid or PC speakers
*   **⌨️ Interactive Mode:** Control the robot with simple text commands
*   **🔌 Plug & Play:** Automatically detects the USB Dongle
*   **🎭 52 Cinematic Combos:** Pre-programmed animations and routines

---

## 🎮 Commands (الأوامر)

Once the application is running, you'll see an interactive menu. Or use these commands:

### Interactive Menu Options
| Option | Description |
| :--- | :--- |
| `1` | Show Top 10 Cinematic Combos |
| `2` | Show All 50 Combos |
| `3` | Basic Controls (Eyes, Wings, Spin...) |
| `4` | Diagnostics |
| `5` | Music Player Menu |

### Command-Line Arguments
```bash
# Run interactive mode (default)
java -jar target/jtuxdriver-1.0-SNAPSHOT.jar

# Or with explicit flag
java -jar target/jtuxdriver-1.0-SNAPSHOT.jar --interactive

# Single commands
java -jar target/jtuxdriver-1.0-SNAPSHOT.jar --flap
java -jar target/jtuxdriver-1.0-SNAPSHOT.jar --eyes true
java -jar target/jtuxdriver-1.0-SNAPSHOT.jar --spin left --val 100
java -jar target/jtuxdriver-1.0-SNAPSHOT.jar --say "Hello World"
java -jar target/jtuxdriver-1.0-SNAPSHOT.jar --combo 6
java -jar target/jtuxdriver-1.0-SNAPSHOT.jar --play assets/audio/billie.mp3

# Debug mode (see raw USB data)
java -jar target/jtuxdriver-1.0-SNAPSHOT.jar --debug
```

### Available Flags
| Flag | Description | Example |
| :--- | :--- | :--- |
| `--interactive, -i` | Force interactive mode | `-i` |
| `--flap` | Flap wings | `--flap` |
| `--eyes <bool>` | Open/close eyes | `--eyes true` |
| `--blink <n>` | Blink N times | `--blink 3` |
| `--mouth <bool>` | Open/close mouth | `--mouth true` |
| `--talk <n>` | Move mouth N times | `--talk 5` |
| `--spin <dir>` | Spin left/right | `--spin left` |
| `--val <n>` | Duration for spin | `--val 100` |
| `--led <color>` | Set LED color (0-255) | `--led 2` |
| `--intensity <n>` | LED intensity (0-255) | `--intensity 255` |
| `--say <text>` | Speak text | `--say "Hello"` |
| `--combo <id>` | Run combo (1-52) | `--combo 6` |
| `--play <file>` | Play MP3 file | `--play song.mp3` |
| `--list, -l` | Check device connection | `-l` |
| `--debug, -d` | Debug HID input | `-d` |

---

## 🛠️ Troubleshooting (حل المشاكل)

### Windows Issues

**"Java is not installed"**
- Download from: https://adoptium.net/ (Recommended)
- Or: https://www.oracle.com/java/technologies/downloads/

**"Build failed"**
- Close any running TuxDroid applications
- Delete the `target` folder and try again

**"Device not found"**
- Make sure the Tux Droid USB dongle is plugged in
- Try a different USB port

### Linux Issues

**"Permission denied" for USB**
```bash
# The script should do this automatically, but if not:
sudo bash -c 'echo "SUBSYSTEM==\"usb\", ATTR{idVendor}==\"03eb\", ATTR{idProduct}==\"ff07\", MODE=\"0666\"" > /etc/udev/rules.d/99-tuxdroid.rules'
sudo udevadm control --reload-rules
sudo udevadm trigger
# Log out and back in
```

**"espeak not found"**
```bash
sudo apt install espeak
```

**"libhidapi not found"**
```bash
sudo apt install libhidapi-hidraw0 libhidapi-dev
```

---

## 🏗️ Developer Info (للمطورين)

### Project Structure
```
├── START_WINDOWS.bat      # Easy Windows launcher
├── START_LINUX.sh         # Easy Linux launcher
├── src/                   # Java source code
│   └── main/java/com/kowalski7cc/jtuxdriver/
│       ├── cli/           # Command-line interface
│       │   ├── Main.java
│       │   └── InteractiveMode.java
│       ├── core/          # USB/HID transport
│       ├── AudioPlayer.java
│       ├── TTS.java
│       ├── TuxDroid.java
│       └── TuxCombos.java
├── assets/audio/          # Audio files for dancing
├── scripts/               # Additional scripts
└── pom.xml               # Maven build file
```

### Building Manually
```bash
# Using Maven
mvn clean package

# Or using the portable Maven (Windows)
tools\maven\bin\mvn.cmd clean package
```

### Dependencies
- **hid4java** - USB HID communication
- **JLayer** - MP3 decoding
- **Picocli** - Command-line argument parsing
- **JUnit 5** - Testing

---

## 📋 Changelog

### v3.0 (Current)
- ✅ Unified codebase for Windows and Linux
- ✅ Easy one-click launchers
- ✅ Auto-install missing dependencies (Linux)
- ✅ Fixed `--interactive` flag
- ✅ Improved audio player with fallback
- ✅ Better error handling and messages
- ✅ 64-bit Linux support

### v2.0
- Added Interactive Menu mode
- 52 Cinematic Combos
- Music player with dancing

### v1.0
- Initial release
- Basic USB HID communication

---

## 👨‍💻 Author & Credits

**Developed & Revived by:** Scayar  
**Email:** scayar.exe@gmail.com  
**Powered by:** AI Assistant 🤖  

*   Original Hardware by **Kysoh** (Legacy)
*   This driver is an open-source modernization effort

> *"Tux Droid Never Dies!"* 🐧💙

---

## 📄 License

This project is licensed under the GNU Lesser General Public License v3.0 - see the [docs/LICENSE](docs/LICENSE) file for details.
