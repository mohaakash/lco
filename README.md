# LCO Project

A Python-based application for Elemental Analysis and Report Generation using Kepler-style astrology PDFs.

## Features

*   **PDF Extraction**: Automatically extracts planetary data from Page 3 of Kepler-style PDF reports.
*   **Elemental Analysis**: Calculates the distribution of Fire, Earth, Air, and Water elements based on planetary positions.
*   **AI-Powered Reports**: Generates personalized daily routines and detailed elemental reports using Google Gemini AI.
*   **GUI**: User-friendly interface built with PyQt6 for easy interaction.

## Setup

1.  **Create a virtual environment:**
    ```bash
    python -m venv .venv
    ```

2.  **Activate the virtual environment:**
    *   **Linux/macOS:**
        ```bash
        source .venv/bin/activate
        ```
    *   **Windows:**
        ```bash
        .venv\Scripts\activate
        ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configuration:**
    *   Create a `.env` file in the root directory.
    *   Add your Google Gemini API key:
        ```env
        GEMINI_API_KEY=your_api_key_here
        ```

## Usage

To run the main application, execute the following command:

```bash
python main.py
```

### Generating a Report
1.  Launch the application.
2.  Click "Upload PDF" and select a Kepler-style PDF file (must contain Page 3 with planetary data).
3.  The application will extract the data and display the Elemental Analysis.
4.  Click "Generate Report" to create a detailed PDF report with AI-generated insights.

## Dependencies

*   `PyQt6`: For the Graphical User Interface.
*   `pymupdf`: For PDF text extraction.
*   `google-generativeai`: For interacting with the Gemini API.
*   `python-dotenv`: For managing environment variables.
*   `PyPDF2`: For PDF manipulation.