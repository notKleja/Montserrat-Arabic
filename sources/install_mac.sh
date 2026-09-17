#!/bin/bash
# Install the OTFs on macOS so Figma Desktop picks up the new build.
# Figma fetches local fonts via http://127.0.0.1:<port>/figma/font-file?file=<path> and its
# Chromium HTTP cache keys on the path only, so a replaced file at the same path stays stale.
# We therefore (1) version the installed filename and (2) purge that cache and fontd's registry.
set -euo pipefail
cd "$(dirname "$0")/.."
VER=$(python3 -c "from fontTools.ttLib import TTFont; print('%.3f' % TTFont('fonts/OTF/Drahim-Regular.otf')['head'].fontRevision)")
FIGMA="$HOME/Library/Application Support/Figma"

osascript -e 'tell application "Figma" to quit' 2>/dev/null || true
sleep 2
rm -f "$HOME"/Library/Fonts/Drahim-*.otf
for w in Regular Medium SemiBold Bold; do cp "fonts/OTF/Drahim-$w.otf" "$HOME/Library/Fonts/Drahim-$w-$VER.otf"; done
killall fontd 2>/dev/null || true
rm -f "$FIGMA/font_cache.json"
rm -rf "$FIGMA"/DesktopProfile/v*/Cache/Cache_Data "$FIGMA"/DesktopBeta/Profile/v*/Cache/Cache_Data
open -a Figma
echo "installed Drahim $VER; in open Figma files re-apply the font on existing text layers to force re-layout"
