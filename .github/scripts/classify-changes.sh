#!/usr/bin/env bash
# Copyright (c) 2026 Eddie Aftandilian.
# Licensed under the BSD 3-Clause License (see LICENSE file).
set -euo pipefail

# Reads changed paths, one per line, on stdin and writes code=true to
# $GITHUB_OUTPUT when any of them can affect the build or tests.
#
# Only documentation, the license, and agent skills are skipped. Agent skills
# are repository automation assets with their own tests. Other extensions,
# including .txt, are code: test data and CMake build files use .txt.
CODE_FILES=$(grep -vE '(\.md$|^LICENSE$|^\.agents/skills/)' | grep -v '^$' || true)
if [[ -n "$CODE_FILES" ]]; then
  echo "code=true" >> "$GITHUB_OUTPUT"
else
  echo "code=false" >> "$GITHUB_OUTPUT"
fi
