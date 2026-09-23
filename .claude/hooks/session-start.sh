#!/bin/bash
set -euo pipefail

# Only needed for Claude Code on the web / remote sessions.
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

# libreoffice-core is preinstalled in this environment, but the actual
# application components (Writer/Calc/Impress) are not. Without them,
# `soffice --convert-to pdf` fails on every file ("source file could not
# be loaded"), which breaks docx/xlsx/pptx -> PDF preview rendering.
if ! dpkg -s libreoffice-writer >/dev/null 2>&1; then
  apt-get update -qq
  apt-get install -y -qq libreoffice-writer libreoffice-calc libreoffice-impress
fi

# scripts/build.js (generates working/*.docx) depends on the npm "docx" package.
if [ -f "$CLAUDE_PROJECT_DIR/package.json" ]; then
  (cd "$CLAUDE_PROJECT_DIR" && npm install --no-audit --no-fund)
fi
