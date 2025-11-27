# Use Python 3.11 with Debian Bookworm for Qt6 support
FROM python:3.11-bookworm

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    DISPLAY=:0

# Install system dependencies for PyQt6 and WeasyPrint
RUN apt-get update && apt-get install -y \
    # Qt6 dependencies
    libqt6core6 \
    libqt6gui6 \
    libqt6widgets6 \
    libqt6network6 \
    libqt6printsupport6 \
    qt6-qpa-plugins \
    # X11 and display dependencies
    libxcb-xinerama0 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-randr0 \
    libxcb-render-util0 \
    libxcb-shape0 \
    libxcb-cursor0 \
    libxkbcommon-x11-0 \
    libxkbcommon0 \
    libdbus-1-3 \
    libgl1 \
    libglib2.0-0 \
    # WeasyPrint dependencies
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info \
    # PDF processing
    libmupdf-dev \
    # Fonts
    fonts-liberation \
    fonts-dejavu-core \
    # Utilities
    xauth \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create directory for X11 socket
RUN mkdir -p /tmp/.X11-unix

# Set the entrypoint
CMD ["python", "main.py"]
