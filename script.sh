#!/bin/bash
set -e
echo "🚀 Starting Uber streaming pipeline setup..."

# ---------------------------------
# Step 1: Python virtual environment
# ---------------------------------
echo "🐍 Setting up Python virtual environment..."
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
fi

echo "🔑 Activating virtual environment..."
source .venv/bin/activate

echo "📦 Upgrading pip..."
pip install --upgrade pip

echo "📂 Current directory: $(pwd)"
echo "📄 Checking for requirements.txt..."

if [ -f "requirements.txt" ]; then
    echo "📚 Installing Python dependencies..."
    pip install -r requirements.txt
    echo "✅ Dependencies installed successfully!"
else
    echo "❌ requirements.txt not found!"
    exit 1
fi

# ---------------------------------
# Step 2: Docker Compose
# ---------------------------------
echo ""
echo "🐳 Starting Docker services with docker-compose..."

if [ ! -f "docker-compose.yml" ]; then
    echo "❌ docker-compose.yml not found!"
    exit 1
fi

# Stop existing containers (both docker-compose and standalone)
echo "🧹 Stopping existing containers..."
docker compose down 2>/dev/null || true
docker stop $(docker ps -aq) 2>/dev/null || true
docker rm $(docker ps -aq) 2>/dev/null || true

# Start all services
echo "🚀 Starting all services..."
docker compose up -d

echo "⏳ Waiting for Kafka to be ready..."
sleep 10

# Create topic with 3 partitions for better parallelism
echo "🔧 Creating Kafka topic 'rides_raw' with 3 partitions..."
docker exec kafka kafka-topics \
  --create \
  --topic rides_raw \
  --partitions 3 \
  --replication-factor 1 \
  --bootstrap-server localhost:9092 \
  --if-not-exists

# ---------------------------------
# Step 3: Initialize Database
# ---------------------------------
echo ""
echo "🗄️  Initializing PostgreSQL database..."

if [ -f "init_database.py" ]; then
    python init_database.py
    echo "✅ Database initialized successfully!"
else
    echo "⚠️  init_database.py not found, skipping database initialization"
fi

# ---------------------------------
# Step 4: Verification
# ---------------------------------
echo ""
echo "✅ Checking container status:"
docker compose ps

echo ""
echo "🎉 Setup complete!"
echo ""
echo "📋 Next steps - Open 3 terminals and run:"
echo "   Terminal 1: python producer/producer.py"
echo "   Terminal 2: python consumer/consumer.py"
echo "   Terminal 3: streamlit run dashboard/app.py"
echo ""
echo "🌐 Access points:"
echo "   - Dashboard: http://localhost:8501"
echo "   - Kafka UI: http://localhost:8080"
echo "   - PostgreSQL: localhost:5432"