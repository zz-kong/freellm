#!/bin/bash
# verify_setup.sh - Verify the Free LLM API Discovery setup

echo "=== Free LLM API Discovery Setup Verification ==="
echo ""

# Check directories
echo "Checking directories..."
for dir in data docs logs models tests scripts; do
    if [ -d "$dir" ]; then
        echo "  ✅ $dir/"
    else
        echo "  ❌ $dir/ (missing)"
    fi
done

# Check scripts
echo ""
echo "Checking scripts..."
for script in gather-llm-apis.sh test-apis.sh publish-docs.sh update-settings.sh; do
    if [ -f "scripts/$script" ]; then
        echo "  ✅ scripts/$script"
    else
        echo "  ❌ scripts/$script (missing)"
    fi
done

# Check data files
echo ""
echo "Checking data files..."
if [ -f "data/models.json" ]; then
    echo "  ✅ data/models.json ($(jq 'length' data/models.json) providers)"
else
    echo "  ❌ data/models.json (missing)"
fi

# Check documentation
echo ""
echo "Checking documentation..."
if [ -f "docs/models.md" ]; then
    echo "  ✅ docs/models.md"
else
    echo "  ❌ docs/models.md (missing)"
fi

# Check settings
echo ""
echo "Checking settings..."
if [ -f "settings.json" ]; then
    echo "  ✅ settings.json"
else
    echo "  ❌ settings.json (missing)"
fi

# Check dependencies
echo ""
echo "Checking dependencies..."
if command -v jq &> /dev/null; then
    echo "  ✅ jq $(jq --version)"
else
    echo "  ❌ jq (not found - install with: pkg install jq)"
fi

if command -v curl &> /dev/null; then
    echo "  ✅ curl $(curl --version | head -1)"
else
    echo "  ⚠️  curl (not found - required for API testing)"
fi

echo ""
echo "=== Verification Complete ==="
echo ""
echo "Next steps:"
echo "1. Run: bash scripts/gather-llm-apis.sh --force"
echo "2. View: cat docs/models.md | head -80"
echo "3. Test: bash scripts/test-apis.sh --limit 3"
echo ""
echo "Documentation:"
echo "  - README.md - Project overview"
echo "  - SETUP_SUMMARY.md - Quick start guide"
echo "  - COMPLETE_SUMMARY.md - Full documentation"
