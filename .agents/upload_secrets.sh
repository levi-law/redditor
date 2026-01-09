#!/bin/bash
# Upload secrets from secrets.env to GitHub repository
# Usage: ./upload_secrets.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SECRETS_FILE="$SCRIPT_DIR/secrets.env"
REPO="levi-law/redditor"

if [ ! -f "$SECRETS_FILE" ]; then
    echo "❌ Error: secrets.env not found at $SECRETS_FILE"
    exit 1
fi

echo "🔐 Uploading secrets to GitHub repository: $REPO"
echo ""

while IFS='=' read -r key value; do
    # Skip comments and empty lines
    [[ "$key" =~ ^#.*$ ]] && continue
    [[ -z "$key" ]] && continue
    
    # Skip if value is a placeholder
    if [[ "$value" == YOUR_* ]]; then
        echo "⏭️  Skipping $key (placeholder value)"
        continue
    fi
    
    echo "📤 Setting $key..."
    echo "$value" | gh secret set "$key" --repo "$REPO"
    
done < "$SECRETS_FILE"

echo ""
echo "✅ Secrets upload complete!"
echo "🔗 Verify at: https://github.com/$REPO/settings/secrets/actions"
