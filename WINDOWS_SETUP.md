# BirthCode - Windows Setup Guide

## Quick Start

This package contains everything you need to run BirthCode on Windows using Docker.

## Prerequisites

1. **Docker Desktop for Windows**
   - Download from: https://www.docker.com/products/docker-desktop/
   - Install and ensure it's running

2. **VcXsrv X Server** (for GUI display)
   - Download from: https://sourceforge.net/projects/vcxsrv/
   - Install VcXsrv

## Setup Instructions

### Step 1: Extract the Files

Extract the `birthcode-windows.zip` file to a folder on your Windows PC (e.g., `C:\BirthCode\`)

### Step 2: Configure VcXsrv

1. Run **XLaunch** from the Start Menu
2. Use these settings:
   - ✅ **Multiple windows**
   - ✅ **Display number: 0**
   - ✅ **Start no client**
   - ✅ **Disable access control** (CRITICAL!)
3. **IMPORTANT**: Allow VcXsrv through Windows Firewall when prompted
   - Or manually add a firewall rule for `vcxsrv.exe`

### Step 3: Start Docker Desktop

Make sure Docker Desktop is running before proceeding.

### Step 4: Run the Application

1. Navigate to the extracted folder
2. Double-click `run-windows.bat`
3. The script will:
   - Check for VcXsrv
   - Build the Docker image (first time only - may take a few minutes)
   - Start the application

### Step 5: First-Time Setup (Optional)

If you want to use AI features:
1. Copy `.env.example` to `.env`
2. Edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your-api-key-here
   ```

## Troubleshooting

### Application Won't Start

1. **Check VcXsrv is running**
   ```cmd
   tasklist | findstr vcxsrv
   ```

2. **Verify "Disable access control" is enabled in VcXsrv**
   - Restart VcXsrv with this setting if needed

3. **Check Windows Firewall**
   - Allow `vcxsrv.exe` through firewall
   - Allow `Docker Desktop` through firewall

4. **Restart sequence**
   - Close VcXsrv
   - Restart Docker Desktop
   - Start VcXsrv with correct settings
   - Run `run-windows.bat` again

### Docker Build Fails

1. Ensure Docker Desktop is running
2. Check your internet connection (needed to download dependencies)
3. Try restarting Docker Desktop

### Display Connection Error

If you see `qt.qpa.xcb: could not connect to display`:
- Ensure VcXsrv is running with "Disable access control" checked
- Check Windows Firewall settings
- Try restarting both VcXsrv and Docker Desktop

## What's Included

- ✅ Application source code
- ✅ Docker configuration files
- ✅ Windows batch script for easy launching
- ✅ All required fonts and images
- ✅ Documentation

## Need Help?

For detailed Docker setup instructions, see `DOCKER_SETUP.md` in the extracted folder.

For general application usage, see `README.md`.

---

**Note**: The first time you run the application, Docker will need to download the base image and install dependencies. This may take 5-10 minutes depending on your internet connection. Subsequent runs will be much faster!
