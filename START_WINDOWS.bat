@echo off
chcp 65001 >nul 2>&1
setlocal enabledelayedexpansion
title 🐧 TuxDroid Controller - Windows

:: Set colors (works on Windows 10+)
for /f "tokens=*" %%a in ('echo prompt $E^| cmd') do set "ESC=%%a"

echo.
echo %ESC%[96m╔═══════════════════════════════════════════════════════════╗%ESC%[0m
echo %ESC%[96m║       🐧 TUXDROID ULTIMATE CONTROLLER - WINDOWS 🐧        ║%ESC%[0m
echo %ESC%[96m╚═══════════════════════════════════════════════════════════╝%ESC%[0m
echo.

:: Navigate to script directory
cd /d "%~dp0"

:: ═══════════════════════════════════════════════════════════════
:: STEP 1: Check Java
:: ═══════════════════════════════════════════════════════════════
echo %ESC%[33m[1/4]%ESC%[0m Checking Java...

where java >nul 2>&1
if %errorlevel% neq 0 (
    echo %ESC%[91m[ERROR]%ESC%[0m Java is NOT installed!
    echo.
    echo %ESC%[93mPlease install Java 8 or higher:%ESC%[0m
    echo   Option 1: https://adoptium.net/
    echo   Option 2: https://www.oracle.com/java/technologies/downloads/
    echo.
    echo After installing, restart this script.
    pause
    exit /b 1
)

:: Get Java version
for /f "tokens=3" %%v in ('java -version 2^>^&1 ^| findstr /i "version"') do (
    set "JAVA_VER=%%~v"
)
echo %ESC%[92m[OK]%ESC%[0m Java found: %JAVA_VER%

:: ═══════════════════════════════════════════════════════════════
:: STEP 2: Setup Maven (Portable)
:: ═══════════════════════════════════════════════════════════════
echo.
echo %ESC%[33m[2/4]%ESC%[0m Setting up Maven...

set "MVN_CMD="

:: Check for global Maven first
where mvn >nul 2>&1
if %errorlevel% equ 0 (
    echo %ESC%[92m[OK]%ESC%[0m Using system Maven
    set "MVN_CMD=mvn"
    goto :maven_ready
)

:: Check for local portable Maven
if exist "tools\maven\bin\mvn.cmd" (
    echo %ESC%[92m[OK]%ESC%[0m Using local portable Maven
    set "MVN_CMD=tools\maven\bin\mvn.cmd"
    goto :maven_ready
)

:: Download portable Maven
echo %ESC%[93m[INFO]%ESC%[0m Downloading portable Maven (one-time setup)...
echo       This may take 1-2 minutes...
echo.

:: Create tools directory if it doesn't exist
if not exist "tools" mkdir tools

:: Download Maven using PowerShell
powershell -ExecutionPolicy Bypass -Command ^
    "$ProgressPreference = 'SilentlyContinue'; " ^
    "$url = 'https://archive.apache.org/dist/maven/maven-3/3.9.6/binaries/apache-maven-3.9.6-bin.zip'; " ^
    "$zip = 'tools\maven.zip'; " ^
    "Write-Host 'Downloading...'; " ^
    "Invoke-WebRequest -Uri $url -OutFile $zip; " ^
    "Write-Host 'Extracting...'; " ^
    "Expand-Archive -Path $zip -DestinationPath 'tools' -Force; " ^
    "if (Test-Path 'tools\maven') { Remove-Item 'tools\maven' -Recurse -Force }; " ^
    "Rename-Item 'tools\apache-maven-3.9.6' 'tools\maven'; " ^
    "Remove-Item $zip; " ^
    "Write-Host 'Done!'"

if not exist "tools\maven\bin\mvn.cmd" (
    echo %ESC%[91m[ERROR]%ESC%[0m Failed to download Maven!
    echo Please check your internet connection and try again.
    pause
    exit /b 1
)

echo %ESC%[92m[OK]%ESC%[0m Maven installed successfully
set "MVN_CMD=tools\maven\bin\mvn.cmd"

:maven_ready

:: ═══════════════════════════════════════════════════════════════
:: STEP 3: Build Project
:: ═══════════════════════════════════════════════════════════════
echo.
echo %ESC%[33m[3/4]%ESC%[0m Building project...

:: Check if JAR already exists and is recent (skip rebuild)
if exist "target\jtuxdriver-1.0-SNAPSHOT.jar" (
    echo %ESC%[92m[OK]%ESC%[0m JAR file found, skipping build
    echo       ^(Delete target folder to force rebuild^)
    goto :build_done
)

:: Run Maven build
echo %ESC%[93m[INFO]%ESC%[0m Running Maven build... please wait...
call %MVN_CMD% package -DskipTests -q

if %errorlevel% neq 0 (
    echo.
    echo %ESC%[91m[ERROR]%ESC%[0m Build failed!
    echo.
    echo %ESC%[93mTrying to fix common issues...%ESC%[0m
    
    :: Try to kill any Java process that might lock files
    taskkill /f /im java.exe >nul 2>&1
    
    :: Clean and rebuild
    echo Cleaning and rebuilding...
    if exist "target" rmdir /s /q "target" >nul 2>&1
    call %MVN_CMD% package -DskipTests -q
    
    if %errorlevel% neq 0 (
        echo %ESC%[91m[ERROR]%ESC%[0m Build still failed!
        echo Run this for details: %MVN_CMD% package -e
        pause
        exit /b 1
    )
)

echo %ESC%[92m[OK]%ESC%[0m Build successful!

:build_done

:: ═══════════════════════════════════════════════════════════════
:: STEP 4: Run Application
:: ═══════════════════════════════════════════════════════════════
echo.
echo %ESC%[33m[4/4]%ESC%[0m Starting TuxDroid Controller...
echo.
echo %ESC%[96m═══════════════════════════════════════════════════════════%ESC%[0m
echo.

:: Run with native access enabled (required for hid4java)
java --enable-native-access=ALL-UNNAMED -jar "target\jtuxdriver-1.0-SNAPSHOT.jar" %*

echo.
echo %ESC%[96m═══════════════════════════════════════════════════════════%ESC%[0m
echo %ESC%[92m[INFO]%ESC%[0m Application closed.
echo.
pause

