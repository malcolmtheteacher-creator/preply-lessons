#!/bin/bash
# Build script for Malcolm's Lessons website
#
# This script:
# 1. Rebuilds the mind map (.itmz) file from the lesson index
#
# Usage:
#   ./build.sh
#
# The mind map is saved to: ../Assets/Malcolm_Lessons_Map.itmz

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🔨 Building Malcolm's Lessons..."
echo ""

# Build mind map
echo "📖 Building mind map..."
python3 build_mindmap.py

echo ""
echo "✅ Build complete!"
echo ""
echo "Files updated:"
echo "  • ../Assets/Malcolm_Lessons_Map.itmz"
