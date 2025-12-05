# 🐧 TUX Droid AI Control

A complete IoT automation system for controlling TUX Droid via Telegram Bot and REST API.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![Telegram](https://img.shields.io/badge/Telegram-Bot-blue.svg)
![License](https://img.shields.io/badge/License-GPL--2.0-red.svg)

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the System](#running-the-system)
- [API Documentation](#api-documentation)
- [Telegram Bot Usage](#telegram-bot-usage)
- [Adding New Actions](#adding-new-actions)
- [Development](#development)
- [Troubleshooting](#troubleshooting)

## 🎯 Overview

TUX Droid AI Control is a modern, modular system that allows you to control a TUX Droid robot via:

- **Telegram Bot**: User-friendly interface with button menus
- **REST API**: HTTP endpoints for programmatic control
- **Mock Driver**: Development mode without hardware

The system is designed to be:
- 📚 **Educational**: Clean code, well-documented, easy to understand
- 🔧 **Modular**: Separated concerns, easy to extend
- 🛡️ **Robust**: Error handling, logging, graceful degradation
- 🚀 **Production-ready**: Proper project structure, configuration management

## 🏗️ Architecture

```
┌─────────────────┐     HTTP      ┌─────────────────┐     USB      ┌─────────────┐
│   Telegram Bot  │ ──────────▶  │   FastAPI API   │ ──────────▶  │  TUX Droid  │
│   (Windows/Any) │              │    (Ubuntu)     │              │  (Hardware) │
└─────────────────┘              └─────────────────┘              └─────────────┘
                                        │
                                        ▼
                                 ┌─────────────────┐
                                 │  TUX Controller │
                                 │                 │
                                 │  ┌───────────┐  │
                                 │  │  Driver   │  │
                                 │  │(Mock/Real)│  │
                                 │  └───────────┘  │
                                 └─────────────────┘
```

### Project Structure

```
tux-droid-ai-control/
├── backend/                 # FastAPI REST API
│   ├── main.py             # API entry point
│   ├── routes/             # API endpoints
│   │   ├── tux_routes.py   # TUX control routes
│   │   └── health.py       # Health check routes
│   ├── schemas/            # Pydantic models
│   │   └── tux_schemas.py  # Request/response schemas
│   └── nlp_parser.py       # NLP placeholder (future)
│
├── bot/                     # Telegram Bot
│   ├── main.py             # Bot entry point
│   ├── handlers.py         # Command handlers
│   ├── keyboards.py        # Button layouts
│   └── api_client.py       # API client
│
├── tux/                     # TUX Control Layer
│   ├── controller.py       # High-level controller
│   ├── actions.py          # Action types & mapping
│   └── driver.py           # Hardware driver interface
│
├── stubs/                   # Mock Implementations
│   └── mock_driver.py      # Mock TUX driver
│
├── config/                  # Configuration
│   ├── settings.py         # Settings management
│   └── env.example         # Environment template
│
├── tests/                   # Test Suite
│   ├── test_backend.py     # API tests
│   └── test_bot.py         # Bot tests
│
├── requirements.txt         # Dependencies
└── README.md               # This file
```

## ✨ Features

### TUX Control Actions

| Category | Actions |
|----------|---------|
| 👀 **Eyes** | Blink, Open, Close |
| 👄 **Mouth** | Move, Open, Close |
| 🐧 **Wings** | Wave, Raise, Lower |
| 🔄 **Spin** | Left, Right (various angles) |
| 💡 **LEDs** | On, Off, Toggle, Pulse |
| 🔊 **Sound** | Play, Mute, Unmute |
| 😴 **Sleep** | Normal, Quick, Deep, Wake |

### Operation Modes

- **DEV Mode**: Uses mock driver, simulates TUX actions with logging
- **PROD Mode**: Uses real hardware driver via USB

## 📦 Requirements

### Software

- Python 3.10 or higher
- pip (Python package manager)

### Hardware (PROD Mode Only)

- TUX Droid connected via USB
- Ubuntu Linux (recommended for USB driver)
- libtuxdriver or compatible driver

## 🚀 Installation

### 1. Clone/Copy the Project

```bash
# Navigate to project directory
cd tux-droid-ai-control
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Linux/macOS)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
# Copy example configuration
cp config/env.example .env

# Edit .env with your settings
# (See Configuration section below)
```

## ⚙️ Configuration

Create a `.env` file in the project root:

```env
# Telegram Bot Token (from @BotFather)
TELEGRAM_BOT_TOKEN=your_bot_token_here

# Backend API URL
BACKEND_API_URL=http://localhost:8000

# API Server Settings
API_HOST=0.0.0.0
API_PORT=8000

# TUX Mode: DEV (mock) or PROD (real hardware)
TUX_MODE=DEV

# USB Device Path (PROD mode only)
TUX_DEVICE_PATH=/dev/ttyUSB0

# Logging Level
LOG_LEVEL=INFO
```

### Getting a Telegram Bot Token

1. Open Telegram and search for `@BotFather`
2. Send `/newbot` command
3. Follow instructions to create your bot
4. Copy the token provided

## 🏃 Running the System

### Start Backend API (Ubuntu)

```bash
# From project root
cd tux-droid-ai-control

# Activate virtual environment
source venv/bin/activate

# Run the API server
python -m backend.main

# Or with uvicorn directly
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at:
- API: `http://localhost:8000`
- Docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Start Telegram Bot

```bash
# From project root (can be on Windows or Ubuntu)
cd tux-droid-ai-control

# Activate virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Run the bot
python -m bot.main
```

### Running Both Together (Ubuntu)

```bash
# Terminal 1 - Backend
uvicorn backend.main:app --host 0.0.0.0 --port 8000

# Terminal 2 - Bot
python -m bot.main
```

## 📡 API Documentation

### Endpoints Overview

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API info |
| `/health` | GET | Health check |
| `/status` | GET | TUX status |
| `/tux/eyes` | POST | Eye control |
| `/tux/mouth` | POST | Mouth control |
| `/tux/wings` | POST | Wing control |
| `/tux/spin` | POST | Spin control |
| `/tux/leds` | POST | LED control |
| `/tux/sound` | POST | Sound control |
| `/tux/sleep` | POST | Sleep control |
| `/tux/speak` | POST | TTS (placeholder) |
| `/tux/custom` | POST | Custom actions |
| `/tux/connect` | POST | Connect to TUX |
| `/tux/disconnect` | POST | Disconnect from TUX |

### Example Requests

#### Blink Eyes
```bash
curl -X POST http://localhost:8000/tux/eyes \
  -H "Content-Type: application/json" \
  -d '{"action": "blink", "count": 3}'
```

#### Wave Wings
```bash
curl -X POST http://localhost:8000/tux/wings \
  -H "Content-Type: application/json" \
  -d '{"action": "wave", "count": 5, "speed": 4}'
```

#### Spin Left
```bash
curl -X POST http://localhost:8000/tux/spin \
  -H "Content-Type: application/json" \
  -d '{"action": "left", "angle": 4, "speed": 3}'
```

#### Toggle LEDs
```bash
curl -X POST http://localhost:8000/tux/leds \
  -H "Content-Type: application/json" \
  -d '{"action": "toggle", "count": 5, "delay": 25}'
```

## 🤖 Telegram Bot Usage

### Commands

| Command | Description |
|---------|-------------|
| `/start` | Start bot and show main menu |
| `/menu` | Show main menu |
| `/status` | Check TUX status |
| `/help` | Show help message |

### Quick Actions (Text)

- `👀 Blink` - Blink eyes once
- `🐧 Wave` - Wave wings once
- `💡 Toggle` - Toggle LEDs
- `↩️ Spin Left` - Spin left 90°
- `↪️ Spin Right` - Spin right 90°

### Menu Navigation

1. Use `/start` to see the main menu
2. Click category buttons (Eyes, Mouth, Wings, etc.)
3. Click action buttons to control TUX
4. Use "Back to Menu" to return

## 🔧 Adding New Actions

### 1. Add to Actions Module

Edit `tux/actions.py`:

```python
class ActionType(str, Enum):
    # ... existing actions ...
    MY_NEW_ACTION = "my_new_action"

# Add firmware command code
FIRMWARE_COMMANDS = {
    # ... existing commands ...
    ActionType.MY_NEW_ACTION: 0xXX,  # Your command code
}
```

### 2. Add to Controller

Edit `tux/controller.py`:

```python
def my_new_action(self, param1: int = 1) -> Dict[str, Any]:
    """Description of your new action."""
    logger.info(f"Performing new action with param1={param1}")
    return self._execute(TuxAction(ActionType.MY_NEW_ACTION, {"param1": param1}))
```

### 3. Add API Endpoint

Edit `backend/routes/tux_routes.py`:

```python
@router.post("/my-action")
async def my_new_action(request: MyActionRequest, controller=Depends(get_tux_controller)):
    result = controller.my_new_action(param1=request.param1)
    return create_response(result)
```

### 4. Add Bot Button (Optional)

Edit `bot/keyboards.py` and `bot/handlers.py` to add new buttons.

## 🧪 Development

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_backend.py -v
```

### Mock Mode

In DEV mode, the mock driver:
- Logs all actions to console
- Maintains simulated state
- Provides visual feedback (emojis)
- No hardware required

### Logging

Set `LOG_LEVEL` in `.env`:
- `DEBUG` - Detailed information
- `INFO` - General information (default)
- `WARNING` - Warnings only
- `ERROR` - Errors only

## ❓ Troubleshooting

### Bot Not Responding

1. Check `TELEGRAM_BOT_TOKEN` is correct
2. Ensure backend API is running
3. Check `BACKEND_API_URL` points to correct address

### API Connection Error

1. Verify API is running: `curl http://localhost:8000/health`
2. Check firewall settings
3. Verify network connectivity between bot and API

### TUX Not Responding (PROD Mode)

1. Check USB connection
2. Verify device path: `ls /dev/ttyUSB*`
3. Check permissions: `sudo chmod 666 /dev/ttyUSB0`
4. Verify TUX driver is installed

### Common Errors

| Error | Solution |
|-------|----------|
| "Token not configured" | Set `TELEGRAM_BOT_TOKEN` in `.env` |
| "Connection refused" | Start backend API first |
| "Device not found" | Check USB connection and device path |
| "Permission denied" | Add user to `dialout` group or use sudo |

## 📄 License

This project is licensed under the GPL-2.0 License - see the LICENSE file for details.

## 🙏 Acknowledgments

- TUX Droid firmware team
- FastAPI framework
- python-telegram-bot library

---

**Made with ❤️ for TUX Droid enthusiasts**

