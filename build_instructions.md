# Build Instructions for Windows

This guide explains how to build the standalone `.exe` for the LCO application on Windows.

## Prerequisites

1.  **Windows Machine**: You must perform these steps on a Windows computer.
2.  **Python 3.10+**: Ensure Python is installed and added to your PATH.
3.  **GTK3 Runtime**: Required for PDF generation (WeasyPrint).
    *   Download and install the [GTK3 Runtime for Windows](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases).
    *   **Important**: During installation, ensure "Set up PATH environment variable" is checked.

## Setup

1.  **Clone/Copy the Repository**: Get the code onto your Windows machine.
2.  **Create a Virtual Environment**:
    ```powershell
    python -m venv .venv
    .venv\Scripts\activate
    ```
3.  **Install Dependencies**:
    ```powershell
    pip install -r requirements.txt
    pip install pyinstaller
    ```

## Building the Executable

1.  **Run PyInstaller**:
    Use the provided `lco.spec` file to build the application.
    ```powershell
    pyinstaller lco.spec
    ```

2.  **Locate the Output**:
    *   The build artifacts will be in the `dist/` folder.
    *   You will find a folder named `LCO_App` inside `dist/`.
    *   The main executable is `dist/LCO_App/LCO_App.exe`.

## Distribution

*   To distribute the application, zip the entire `dist/LCO_App` folder.
*   Send the zip file to your client.
*   They just need to unzip it and run `LCO_App.exe`.

## Troubleshooting

*   **PDF Generation Fails**: If the PDF generation fails, it's almost always because the GTK3 libraries are not found. Ensure the GTK3 Runtime is installed and its `bin` folder is in the system PATH.
*   **Missing Images/Templates**: If images or templates are missing, check the `datas` section in `lco.spec` and ensure the paths are correct relative to where you run the command.
