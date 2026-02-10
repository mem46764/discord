#!/bin/bash

# Discord Backup Bot Startup Script

echo "=========================================="
echo "  Discord Backup Bot"
echo "=========================================="
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found"
    echo ""
    echo "Please create a .env file with your Discord bot token:"
    echo "  1. Copy .env.example to .env"
    echo "  2. Edit .env and add your DISCORD_TOKEN"
    echo ""
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
    echo ""
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt

echo ""
echo "🚀 Starting Discord Backup Bot..."
echo "   Press Ctrl+C to stop"
echo ""

# Run the bot
python bot.py
