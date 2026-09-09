#!/bin/bash
# test-apis.sh - Wrapper for test-apis.py
#
# Usage:
#   bash scripts/test-apis.sh                      # test all providers
#   bash scripts/test-apis.sh --limit 5            # first 5 only
#   bash scripts/test-apis.sh --provider Groq      # test specific provider
#   bash scripts/test-apis.sh --context-limit long # only long context test
#
# Environment: Set your API keys with:
#   export GROQ_API_KEY="gsk-..."
#   export GEMINI_API_KEY="..."
#   etc.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$SCRIPT_DIR/test-apis.py" "$@"
