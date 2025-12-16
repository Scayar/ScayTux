#!/bin/bash
# ═══════════════════════════════════════════════════════════════
#  🐧 SCAYTUX - THE ULTIMATE TUX DROID CONTROLLER
#  Author: Scayar
#  GitHub: https://github.com/Scayar
#  Email:  Scayar.exe@gmail.com
# ═══════════════════════════════════════════════════════════════

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
PURPLE='\033[0;35m'
DIM='\033[2m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Navigate to script directory
cd "$(dirname "$0")"
PROJECT_DIR=$(pwd)

echo ""
echo -e "${CYAN}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║            🐧 SCAYTUX - TUX DROID CONTROLLER 🐧           ║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${DIM}              Made with ${RED}♥${DIM} by ${CYAN}Scayar${NC}"
echo -e "${DIM}              github.com/Scayar${NC}"
echo ""

# ═══════════════════════════════════════════════════════════════
# Helper Functions
# ═══════════════════════════════════════════════════════════════

log_step() {
    echo -e "${YELLOW}[$1]${NC} $2"
}

log_ok() {
    echo -e "${GREEN}[OK]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

# ═══════════════════════════════════════════════════════════════
# STEP 1: Check and Install Dependencies
# ═══════════════════════════════════════════════════════════════
log_step "1/5" "Checking dependencies..."

MISSING_DEPS=""

# Check Java
if ! command -v java &> /dev/null; then
    MISSING_DEPS="$MISSING_DEPS openjdk-11-jdk"
    log_error "Java not found"
else
    JAVA_VER=$(java -version 2>&1 | head -n 1)
    log_ok "Java found: $JAVA_VER"
fi

# Check Maven
if ! command -v mvn &> /dev/null; then
    MISSING_DEPS="$MISSING_DEPS maven"
    log_error "Maven not found"
else
    log_ok "Maven found"
fi

# Check espeak (for TTS)
if ! command -v espeak &> /dev/null && ! command -v espeak-ng &> /dev/null; then
    MISSING_DEPS="$MISSING_DEPS espeak"
    log_info "espeak not found (optional, for text-to-speech)"
fi

# Check libhidapi (for USB HID)
HIDAPI_FOUND=false
for lib in /usr/lib/libhidapi*.so* /usr/lib/*/libhidapi*.so* /usr/local/lib/libhidapi*.so*; do
    if [ -f "$lib" ]; then
        HIDAPI_FOUND=true
        break
    fi
done

if [ "$HIDAPI_FOUND" = false ]; then
    MISSING_DEPS="$MISSING_DEPS libhidapi-hidraw0 libhidapi-dev"
    log_error "libhidapi not found"
else
    log_ok "libhidapi found"
fi

# Install missing dependencies
if [ -n "$MISSING_DEPS" ]; then
    echo ""
    log_info "Missing packages:$MISSING_DEPS"
    echo ""
    read -p "Install missing packages? (requires sudo) [Y/n]: " -n 1 -r
    echo ""
    
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        log_info "Installing packages..."
        sudo apt-get update -qq
        sudo apt-get install -y $MISSING_DEPS
        
        if [ $? -ne 0 ]; then
            log_error "Failed to install some packages"
            log_info "Try manually: sudo apt-get install$MISSING_DEPS"
        else
            log_ok "Packages installed successfully"
        fi
    fi
fi

# ═══════════════════════════════════════════════════════════════
# STEP 2: Setup udev Rules (USB Permissions)
# ═══════════════════════════════════════════════════════════════
echo ""
log_step "2/5" "Checking USB permissions..."

UDEV_RULE_FILE="/etc/udev/rules.d/99-tuxdroid.rules"
UDEV_RULE='SUBSYSTEM=="usb", ATTR{idVendor}=="03eb", ATTR{idProduct}=="ff07", MODE="0666", GROUP="plugdev"'

if [ -f "$UDEV_RULE_FILE" ]; then
    log_ok "udev rules already configured"
else
    log_info "Setting up udev rules for TuxDroid USB access..."
    echo ""
    read -p "Setup USB permissions? (requires sudo, one-time) [Y/n]: " -n 1 -r
    echo ""
    
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        echo "$UDEV_RULE" | sudo tee "$UDEV_RULE_FILE" > /dev/null
        
        # Also add HID rule
        echo 'KERNEL=="hidraw*", ATTR{idVendor}=="03eb", ATTR{idProduct}=="ff07", MODE="0666", GROUP="plugdev"' | sudo tee -a "$UDEV_RULE_FILE" > /dev/null
        
        sudo udevadm control --reload-rules
        sudo udevadm trigger
        
        # Add user to plugdev group if not already
        if ! groups | grep -q plugdev; then
            sudo usermod -aG plugdev $USER
            log_info "Added $USER to plugdev group"
            log_info "You may need to log out and back in for group changes to take effect"
        fi
        
        log_ok "udev rules configured"
    fi
fi

# ═══════════════════════════════════════════════════════════════
# STEP 3: Create libhidapi symlink if needed
# ═══════════════════════════════════════════════════════════════
echo ""
log_step "3/5" "Checking library symlinks..."

# Detect architecture
ARCH=$(uname -m)
if [ "$ARCH" = "x86_64" ]; then
    LIB_PATH="/usr/lib/x86_64-linux-gnu"
elif [ "$ARCH" = "i686" ] || [ "$ARCH" = "i386" ]; then
    LIB_PATH="/usr/lib/i386-linux-gnu"
elif [ "$ARCH" = "aarch64" ]; then
    LIB_PATH="/usr/lib/aarch64-linux-gnu"
else
    LIB_PATH="/usr/lib"
fi

# Check for libhidapi.so symlink
if [ ! -L "$LIB_PATH/libhidapi.so" ] && [ -f "$LIB_PATH/libhidapi-hidraw.so.0" ]; then
    log_info "Creating libhidapi symlink..."
    sudo ln -sf "$LIB_PATH/libhidapi-hidraw.so.0" "$LIB_PATH/libhidapi.so" 2>/dev/null
    if [ $? -eq 0 ]; then
        log_ok "Symlink created"
    fi
else
    log_ok "Library paths OK"
fi

# ═══════════════════════════════════════════════════════════════
# STEP 4: Build Project
# ═══════════════════════════════════════════════════════════════
echo ""
log_step "4/5" "Building project..."

JAR_FILE="target/ScayTux.jar"

if [ -f "$JAR_FILE" ]; then
    log_ok "JAR file found, skipping build"
    log_info "(Delete target/ folder to force rebuild)"
else
    log_info "Running Maven build... please wait..."
    mvn package -DskipTests -q
    
    if [ $? -ne 0 ]; then
        log_error "Build failed!"
        log_info "Try running: mvn package -e  (for detailed errors)"
        exit 1
    fi
    
    log_ok "Build successful!"
fi

# ═══════════════════════════════════════════════════════════════
# STEP 5: Detect Audio Device
# ═══════════════════════════════════════════════════════════════
echo ""
log_step "5/5" "Detecting audio device..."

# Try to find TuxDroid USB Audio device
if command -v aplay &> /dev/null; then
    AUDIO_CARD=$(aplay -l 2>/dev/null | grep -i "USB" | grep -i "card" | head -n 1 | awk '{print $2}' | tr -d ':')
    
    if [ -n "$AUDIO_CARD" ]; then
        export TUX_AUDIO_DEV="plughw:$AUDIO_CARD,0"
        log_ok "Found USB Audio at Card #$AUDIO_CARD"
    else
        export TUX_AUDIO_DEV="default"
        log_info "No USB Audio found, using default device"
    fi
else
    export TUX_AUDIO_DEV="default"
fi

# ═══════════════════════════════════════════════════════════════
# Run Application
# ═══════════════════════════════════════════════════════════════
echo ""
echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
echo ""

# Kill any stuck audio processes from previous runs
killall -9 mpg123 2>/dev/null
killall -9 aplay 2>/dev/null

# Set JNA library path for current architecture
export JNA_LIBRARY_PATH="$LIB_PATH"

# Run the application
java -Djna.library.path="$LIB_PATH" \
     -Dtux.audio.dev="$TUX_AUDIO_DEV" \
     -jar "$JAR_FILE" "$@"

echo ""
echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}[INFO]${NC} ScayTux closed."
echo -e "${DIM}       Made with ${RED}♥${DIM} by ${CYAN}Scayar${DIM} - github.com/Scayar${NC}"
echo ""
