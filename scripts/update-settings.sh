#!/bin/bash
# update-settings.sh - Update project settings.json with verified LLM models
# Usage: bash update-settings.sh [--settings <path>]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"
DATA_DIR="$BASE_DIR/data"
MODELS_FILE="$DATA_DIR/models.json"
TEST_RESULTS_FILE="$DATA_DIR/test-results.json"

# Parse arguments
SETTINGS_PATH="${FREELLM_SETTINGS:-$PWD/settings.json}"  # default: settings.json in the current project
while [[ $# -gt 0 ]]; do
    case $1 in
        --settings)
            SETTINGS_PATH="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Resolve settings path to absolute
if [[ "$SETTINGS_PATH" != /* ]]; then
    SETTINGS_PATH="$BASE_DIR/$SETTINGS_PATH"
fi

echo "=== Update Settings.json ==="
echo "Settings file: $SETTINGS_PATH"
echo ""

# Check if models file exists
if [ ! -f "$MODELS_FILE" ]; then
    echo "❌ Models file not found: $MODELS_FILE"
    echo "Run gather-llm-apis.sh first to populate models data"
    exit 1
fi

# Check if settings file exists
if [ ! -f "$SETTINGS_PATH" ]; then
    echo "Settings file not found. Creating new file..."
    
    # Create initial settings structure
    mkdir -p "$(dirname "$SETTINGS_PATH")"
    
    cat > "$SETTINGS_PATH" << 'EOF'
{
  "version": "1.0.0",
  "models": {},
  "settings": {
    "default_model": null,
    "api_keys": {},
    "rate_limits": {
      "requests_per_minute": 60,
      "requests_per_day": 10000
    },
    "cache": {
      "enabled": true,
      "ttl": 3600
    },
    "logging": {
      "level": "info",
      "save_responses": false
    }
  }
}
EOF
    
    echo "Created new settings file: $SETTINGS_PATH"
fi

# Read existing settings
echo "Reading existing settings..."
EXISTING_SETTINGS=$(cat "$SETTINGS_PATH")

# Create backup
BACKUP_PATH="${SETTINGS_PATH}.backup.$(date +%Y%m%d_%H%M%S)"
cp "$SETTINGS_PATH" "$BACKUP_PATH"
echo "Backup created: $BACKUP_PATH"

# Extract verified models (those with reliability score >= 7)
echo ""
echo "Extracting verified models from test results..."

# Get working models
WORKING_MODELS=$(jq -s 'map(.test | select(.reliability_score >= 7) | .model) | unique | .[]' "$TEST_RESULTS_FILE" 2>/dev/null || echo "")

# If no test results, use all models
if [ -z "$WORKING_MODELS" ] || [ "$WORKING_MODELS" = "null" ]; then
    echo "No test results found. Using all models from data/models.json"
    WORKING_MODELS=$(jq -r '.models[].name' "$MODELS_FILE" 2>/dev/null || jq -r '.[].models[]?.name' "$MODELS_FILE" 2>/dev/null || echo "")
fi

# Process each working model
echo ""
echo "Processing verified models..."

# Create new settings structure
NEW_SETTINGS=$(cat "$SETTINGS_PATH")

# Add model configurations
echo "Adding model configurations..."

# Get all working model info
for model_name in $WORKING_MODELS; do
    echo "  - $model_name"
    
    # Find model info
    MODEL_INFO=$(jq --arg name "$model_name" '.[] | select(.models[]?.name == $name or .name == $name)' "$MODELS_FILE" 2>/dev/null | head -1)
    
    if [ -n "$MODEL_INFO" ]; then
        provider=$(echo "$MODEL_INFO" | jq -r '.provider // "Unknown"')
        base_url=$(echo "$MODEL_INFO" | jq -r '.base_url // ""')
        context=$(echo "$MODEL_INFO" | jq -r '.context_length // 8192')
        auth=$(echo "$MODEL_INFO" | jq -r '.auth // "api_key"')
        
        # Get rate limits
        rpm=$(echo "$MODEL_INFO" | jq -r '.rate_limits.requests_per_minute // 60')
        rpd=$(echo "$MODEL_INFO" | jq -r '.rate_limits.requests_per_day // 10000')
        
        # Update model configuration
        NEW_SETTINGS=$(echo "$NEW_SETTINGS" | jq --arg model "$model_name" \
            --arg provider "$provider" \
            --arg url "$base_url" \
            --arg context "$context" \
            --arg auth "$auth" \
            --arg rpm "$rpm" \
            --arg rpd "$rpd" \
            '.models[$model] = {
                "provider": $provider,
                "base_url": $url,
                "context_length": ($context | tonumber),
                "max_output": 8192,
                "auth": $auth,
                "rate_limits": {
                    "requests_per_minute": ($rpm | tonumber),
                    "requests_per_day": ($rpd | tonumber)
                },
                "verified": true,
                "added_at": "'$(date -Iseconds)'"
            }')
    fi
done

# Set default model to first working model
DEFAULT_MODEL=$(echo "$WORKING_MODELS" | head -1)
if [ -n "$DEFAULT_MODEL" ]; then
    NEW_SETTINGS=$(echo "$NEW_SETTINGS" | jq --arg model "$DEFAULT_MODEL" '.settings.default_model = $model')
fi

# Save updated settings
echo "$NEW_SETTINGS" | jq '.' > "$SETTINGS_PATH"

echo ""
echo "Settings updated successfully!"
echo ""
echo "Summary:"
echo "  - Total verified models: $(echo "$WORKING_MODELS" | wc -l)"
echo "  - Default model: $DEFAULT_MODEL"
echo ""
echo "Settings file: $SETTINGS_PATH"
echo "Backup: $BACKUP_PATH"
echo ""
echo "To restore previous settings:"
echo "  cp $BACKUP_PATH $SETTINGS_PATH"
