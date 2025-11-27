#!/bin/bash
# Package BirthCode for Client Distribution
# This script creates a clean ZIP file for your client

echo "Creating client package for BirthCode..."

# Define the output ZIP name
OUTPUT_ZIP="birthcode-client-package.zip"

# Remove old package if exists
rm -f "$OUTPUT_ZIP"

# Create ZIP with only necessary files
zip -r "$OUTPUT_ZIP" \
  main.py \
  requirements.txt \
  Dockerfile \
  docker-compose.yml \
  .dockerignore \
  run-windows.bat \
  DOCKER_SETUP.md \
  README.md \
  .env.example \
  ai/ \
  calc/ \
  ui/ \
  fonts/ \
  images/ \
  -x "*.pyc" \
  -x "*__pycache__*" \
  -x "*.git*" \
  -x "*.venv*" \
  -x "*venv/*" \
  -x "*.env" \
  -x "*tests/*" \
  -x "*docs/*" \
  -x "*.spec" \
  -x "*build/*" \
  -x "*dist/*" \
  -x "*.md" "!README.md" "!DOCKER_SETUP.md"

echo "✓ Package created: $OUTPUT_ZIP"
echo ""
echo "Contents:"
unzip -l "$OUTPUT_ZIP" | head -30
echo ""
echo "Package size:"
ls -lh "$OUTPUT_ZIP"
echo ""
echo "Ready to send to your client!"
