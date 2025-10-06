#!/bin/bash
# Quick setup script for ngrok configuration

echo "🚀 Setting up presentation with ngrok..."

# Check if ngrok URL is provided
if [ -z "$1" ]; then
    echo "❌ Error: Please provide ngrok URL"
    echo "Usage: ./setup-ngrok.sh https://abc123.ngrok.io"
    exit 1
fi

NGROK_URL=$1

# Remove trailing slash if present
NGROK_URL=${NGROK_URL%/}

# Validate URL format
if [[ ! $NGROK_URL =~ ^https://.*\.ngrok\.io$ ]]; then
    echo "⚠️  Warning: URL doesn't look like ngrok URL"
    echo "Expected format: https://abc123.ngrok.io"
fi

# Create .env.local file
echo "📝 Creating .env.local with ngrok URL..."
echo "NEXT_PUBLIC_API_BASE_URL=$NGROK_URL" > .env.local

# Show confirmation
echo "✅ Configuration saved:"
echo "   API Base URL: $NGROK_URL"
echo ""

# Prepare HTML files
echo "🔧 Preparing HTML files..."
npm run prepare-html

echo ""
echo "🎉 Setup completed!"
echo ""
echo "Next steps:"
echo "  1. Make sure your backend is running and accessible via ngrok"
echo "  2. Run: npm run dev"
echo "  3. Your presentation will use: $NGROK_URL"
echo ""
echo "To test API connectivity:"
echo "  curl $NGROK_URL/docs"