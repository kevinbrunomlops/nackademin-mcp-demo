#!/bin/bash

echo "🚀 Setting up FastMCP Server..."

# Skapa virtual environment om det inte redan finns
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
else
    echo "✅ Virtual environment already exists"
fi

# Aktivera virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Installera dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

echo "✅ Setup complete!"
echo ""
echo "To start the server:"
echo "  source venv/bin/activate"
echo "  python server.py"
echo ""
echo "To deactivate the virtual environment:"
echo "  deactivate" 