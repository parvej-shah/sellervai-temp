#!/bin/bash

# Bizzz Backend Setup Script

echo "🚀 Setting up SalesVai Backend..."

# Check if virtual environment is activated
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "⚠️  Virtual environment not activated!"
    echo "Please run: source .venv/bin/activate"
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Check if .env exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your credentials!"
else
    echo "✅ .env file already exists"
fi

# Create alembic versions directory if it doesn't exist
mkdir -p alembic/versions

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your credentials"
echo "2. Create PostgreSQL database: createdb bizzz_db"
echo "3. Run migrations: alembic upgrade head"
echo "4. Start the server: uvicorn app.main:app --reload"
echo ""
