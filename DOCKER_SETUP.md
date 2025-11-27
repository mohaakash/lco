# Docker Setup Guide for BirthCode

This guide explains how to run the BirthCode application using Docker on Windows.

## Prerequisites

### 1. Docker Desktop
- Download and install Docker Desktop for Windows from: https://www.docker.com/products/docker-desktop
- Make sure Docker Desktop is running before proceeding

### 2. VcXsrv X Server (Required for GUI)
Since this is a GUI application (PyQt6), you need an X Server to display the interface on Windows.

**Download and Install:**
1. Download VcXsrv from: https://sourceforge.net/projects/vcxsrv/
2. Install VcXsrv with default settings

**Configure and Run:**
1. Launch "XLaunch" from the Start Menu
2. Follow the configuration wizard:
   - **Display settings**: Select "Multiple windows"
   - **Display number**: 0
   - **Client startup**: Select "Start no client"
   - **Extra settings**: **IMPORTANT** - Check "Disable access control"
3. Click "Finish" to start the X Server
4. VcXsrv will run in the system tray

> **Note**: You need to start VcXsrv every time before running the application.

## Quick Start

### Option 1: Using the Batch Script (Recommended)

1. Open the project folder
2. Double-click `run-windows.bat`
3. The script will:
   - Check if Docker is running
   - Check if VcXsrv is running
   - Build the Docker image (first time only)
   - Start the application

### Option 2: Manual Docker Commands

1. Open Command Prompt or PowerShell in the project directory

2. Build the Docker image:
   ```cmd
   docker-compose build
   ```

3. Get your host IP address:
   ```cmd
   ipconfig
   ```
   Look for "IPv4 Address" (usually something like 192.168.x.x)

4. Run the container:
   ```cmd
   docker-compose run --rm -e DISPLAY=<YOUR_IP>:0.0 birthcode-app
   ```
   Replace `<YOUR_IP>` with your actual IP address

## Configuration

### Setting up Gemini API Key

The application uses Google Gemini AI for report generation. To configure your API key:

1. **Option A - Using Settings Dialog (Recommended)**:
   - Run the application
   - Click the "Settings" button in the Personal Details form
   - Enter your Gemini API key
   - Click "Save"
   - The key will be saved in the Docker container's persistent storage

2. **Option B - Using Environment File**:
   - Create a `.env` file in the project root (if it doesn't exist)
   - Add your API key:
     ```
     GEMINI_API_KEY=your_api_key_here
     ```
   - The Docker container will automatically load this file

## Troubleshooting

### Application window doesn't appear

1. **Check VcXsrv is running**:
   - Look for the VcXsrv icon in the system tray
   - If not running, launch XLaunch again

2. **Verify "Disable access control" is checked**:
   - Close VcXsrv
   - Run XLaunch again and make sure to check "Disable access control"

3. **Check Windows Firewall**:
   - Windows Firewall might block X11 connections
   - Allow VcXsrv through the firewall when prompted

4. **Restart Docker Desktop**:
   - Sometimes Docker needs a restart
   - Right-click Docker Desktop icon → Restart

### "Docker is not running" error

1. Start Docker Desktop from the Start Menu
2. Wait for Docker to fully start (whale icon in system tray)
3. Try running the application again

### Build errors

1. Make sure you have a stable internet connection
2. Try rebuilding with:
   ```cmd
   docker-compose build --no-cache
   ```

### Application crashes or errors

1. Check the console output for error messages
2. Make sure all required files are present in the project directory
3. Verify the `.env` file has the correct API key

## File Structure

```
lco/
├── Dockerfile              # Docker image definition
├── docker-compose.yml      # Docker Compose configuration
├── .dockerignore          # Files to exclude from Docker image
├── run-windows.bat        # Windows launcher script
├── DOCKER_SETUP.md        # This file
├── main.py                # Application entry point
├── requirements.txt       # Python dependencies
├── fonts/                 # Application fonts
├── images/                # Application images
├── ai/                    # AI integration code
├── calc/                  # Element calculator
└── ui/                    # User interface components
```

## Updating the Application

If you receive updates to the application:

1. Replace the project files with the new version
2. Rebuild the Docker image:
   ```cmd
   docker-compose build --no-cache
   ```
3. Run the application as usual

## Uninstalling

To completely remove the application:

1. Remove Docker containers and images:
   ```cmd
   docker-compose down --rmi all
   ```

2. Delete the project folder

3. (Optional) Uninstall VcXsrv if you don't need it for other applications

## Support

For issues or questions:
- Check the troubleshooting section above
- Review Docker Desktop logs
- Check VcXsrv is configured correctly

## Technical Notes

- The application runs in a Linux container with PyQt6
- X11 forwarding is used to display the GUI on Windows
- All Python dependencies are installed automatically
- The container uses Python 3.11
- WeasyPrint is used for PDF generation
