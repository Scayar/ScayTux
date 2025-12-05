# 🐧 TUX Droid - Ubuntu Setup Guide

Complete guide to set up and run TUX Droid AI Control on Ubuntu with real hardware.

## Quick Start (Copy & Paste)

```bash
# === STEP 1: Clone and Setup ===
git clone https://github.com/Scayar/ScayTux.git
cd ScayTux
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# === STEP 2: Configure .env ===
cp config/env.example .env

# Edit .env and add your Telegram token + set PROD mode:
nano .env
# Change these lines:
#   TELEGRAM_BOT_TOKEN=your_token_here
#   TUX_MODE=PROD
#   TUX_DEVICE_PATH=/dev/ttyUSB0

# === STEP 3: USB Permissions (IMPORTANT!) ===
# Add yourself to dialout group:
sudo usermod -a -G dialout $USER

# Temporarily set device permissions (until reboot):
sudo chmod 666 /dev/ttyUSB0

# === STEP 4: Run Diagnostic ===
python -m scripts.diagnose

# === STEP 5: Run the System ===
# Terminal 1 - Backend API:
source venv/bin/activate
python -m backend.main

# Terminal 2 - Telegram Bot:
source venv/bin/activate
python -m bot.main
```

---

## Detailed Steps

### 1. Check if TUX Dongle is Detected

```bash
# List USB devices
lsusb

# Look for FTDI or TUX-related device
lsusb | grep -i ftdi
lsusb | grep -i serial

# Check serial devices
ls -la /dev/ttyUSB*
ls -la /dev/ttyACM*
```

Expected output:
```
crw-rw---- 1 root dialout 188, 0 Dec  5 10:00 /dev/ttyUSB0
```

### 2. Fix USB Permissions

**Option A: Add User to dialout Group (Permanent)**
```bash
# Add user to dialout group
sudo usermod -a -G dialout $USER

# IMPORTANT: Logout and login again for changes to take effect!
# Or reboot:
sudo reboot
```

**Option B: Change Device Permissions (Temporary)**
```bash
# Quick fix (resets on reboot)
sudo chmod 666 /dev/ttyUSB0
```

**Option C: Create udev Rule (Permanent, Recommended)**
```bash
# Create udev rule for TUX dongle
sudo nano /etc/udev/rules.d/99-tuxdroid.rules
```

Add this line (adjust VID/PID if needed):
```
SUBSYSTEM=="tty", ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6001", MODE="0666", GROUP="dialout"
```

Then reload rules:
```bash
sudo udevadm control --reload-rules
sudo udevadm trigger
```

### 3. Verify Python Environment

```bash
# Check Python version (need 3.10+)
python3 --version

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Verify serial library
python3 -c "import serial; print('pyserial OK')"
```

### 4. Configure Environment

```bash
# Copy example config
cp config/env.example .env

# Edit configuration
nano .env
```

Set these values in `.env`:
```env
# Your Telegram Bot Token
TELEGRAM_BOT_TOKEN=8327028798:AAHdMLu8lQcaUPVFw6FxhiDdl--M2n5NP4E

# Set to PROD for real hardware
TUX_MODE=PROD

# USB device path (check with: ls /dev/ttyUSB*)
TUX_DEVICE_PATH=/dev/ttyUSB0

# Enable debug logging for troubleshooting
LOG_LEVEL=DEBUG
```

### 5. Run Diagnostic Tool

```bash
# Activate virtual environment
source venv/bin/activate

# Run full diagnostic
python -m scripts.diagnose
```

This will check:
- Python packages installed
- USB devices detected
- Serial permissions
- TUX driver connection

### 6. Run the System

**Terminal 1 - Backend API:**
```bash
cd ~/ScayTux
source venv/bin/activate
python -m backend.main
```

You should see:
```
╔══════════════════════════════════════════════════════════════╗
║              TUX CONTROLLER INITIALIZATION                   ║
╚══════════════════════════════════════════════════════════════╝
🔧 MODE: PRODUCTION (Real Hardware)
   Device path: /dev/ttyUSB0
📡 Attempting to connect to TUX Droid...
✅ TUX Droid connected successfully!
```

**Terminal 2 - Telegram Bot:**
```bash
cd ~/ScayTux
source venv/bin/activate
python -m bot.main
```

### 7. Test from Telegram

1. Open Telegram
2. Find your bot
3. Send `/start`
4. Click action buttons
5. Watch the backend logs for commands being sent

---

## Troubleshooting

### Problem: "Permission denied" on /dev/ttyUSB0

```bash
# Quick fix
sudo chmod 666 /dev/ttyUSB0

# Permanent fix
sudo usermod -a -G dialout $USER
# Then logout/login
```

### Problem: No /dev/ttyUSB* device found

```bash
# Check if dongle is recognized
lsusb

# Check kernel messages
dmesg | tail -20

# Look for USB serial in kernel
dmesg | grep -i usb
dmesg | grep -i tty
```

### Problem: "pyserial not installed"

```bash
source venv/bin/activate
pip install pyserial pyusb
```

### Problem: Commands sent but TUX doesn't respond

1. Check logs for command bytes being sent
2. Verify baudrate (should be 115200)
3. Try different TUX_DEVICE_PATH
4. Run diagnostic: `python -m scripts.diagnose`

### Problem: Backend connects but Bot doesn't work

1. Check Telegram token in `.env`
2. Check BACKEND_API_URL in `.env`
3. Ensure backend is running on port 8000
4. Check firewall: `sudo ufw allow 8000`

---

## Useful Commands

```bash
# Monitor USB devices
watch -n 1 "ls -la /dev/ttyUSB*"

# View backend logs
journalctl -f -u tuxdroid  # if using systemd

# Test serial manually
screen /dev/ttyUSB0 115200

# Check what's using the serial port
lsof /dev/ttyUSB0

# Kill process using serial port
fuser -k /dev/ttyUSB0
```

---

## Running as a Service (Optional)

Create systemd service for auto-start:

```bash
sudo nano /etc/systemd/system/tuxdroid-api.service
```

```ini
[Unit]
Description=TUX Droid API Server
After=network.target

[Service]
Type=simple
User=YOUR_USERNAME
WorkingDirectory=/home/YOUR_USERNAME/ScayTux
Environment=PATH=/home/YOUR_USERNAME/ScayTux/venv/bin
ExecStart=/home/YOUR_USERNAME/ScayTux/venv/bin/python -m backend.main
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable tuxdroid-api
sudo systemctl start tuxdroid-api
sudo systemctl status tuxdroid-api
```

---

## Need Help?

1. Run diagnostic: `python -m scripts.diagnose`
2. Check logs with `LOG_LEVEL=DEBUG`
3. Open an issue on GitHub with diagnostic output

