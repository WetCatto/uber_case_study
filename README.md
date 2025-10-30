# 🚖 Uber Real-Time Data Streaming Pipeline

A real-time data streaming pipeline that simulates Uber ride data using Kafka, PostgreSQL, and Streamlit for live visualization.

## 📋 Architecture

```
CSV Data → Kafka Producer → Kafka Topic → Kafka Consumer → PostgreSQL → Streamlit Dashboard
```

## 🛠️ Tech Stack

- **Kafka**: Message streaming platform
- **PostgreSQL**: Data storage
- **Streamlit**: Real-time dashboard
- **Python**: Data processing (pandas, kafka-python, sqlalchemy)
- **Docker**: Containerization for Kafka, Zookeeper, and PostgreSQL

## 📁 Project Structure

```
uber_case_study/
├── data/
│   ├── uber_sample.csv          # Source dataset
│   └── clean.py                 # Data cleaning script
├── producer/
│   └── producer.py              # Kafka producer
├── consumer/
│   └── consumer.py              # Kafka consumer
├── dashboard/
│   └── app.py                   # Streamlit dashboard
├── init_database.py             # Database initialization
├── script.sh                    # Environment setup script
├── requirements.txt             # Python dependencies
└── docker-compose.yml           # Docker services
```

## 🚀 Quick Start

### 1. Setup Environment

Run the setup script to install dependencies and start all services:

```bash
chmod +x script.sh
./script.sh
```

This will:
- ✅ Create Python virtual environment
- ✅ Install all Python dependencies from requirements.txt
- ✅ Start all Docker services using docker-compose:
  - PostgreSQL database
  - Zookeeper
  - Kafka broker
  - Kafka UI

### 2. Initialize Database

Create the database table:

```bash
source venv/bin/activate
python init_database.py
```

### 3. Run the Pipeline

Open **3 separate terminal windows** and run each component:

#### Terminal 1: Start Producer
```bash
cd /path/to/uber_case_study
source venv/bin/activate
python producer/producer.py
```

#### Terminal 2: Start Consumer
```bash
cd /path/to/uber_case_study
source venv/bin/activate
python consumer/consumer.py
```

#### Terminal 3: Start Dashboard
```bash
cd /path/to/uber_case_study
source venv/bin/activate
streamlit run dashboard/app.py
```

## 🌐 Access Points

Once everything is running, you can access:

- **Streamlit Dashboard**: http://localhost:8501
- **Kafka UI**: http://localhost:8080
- **PostgreSQL**: localhost:5432
  - Database: `uberdb`
  - User: `user`
  - Password: `password`

## 📊 Features

- **Real-time streaming**: Simulates live ride data from CSV
- **Live map visualization**: Shows ride pickup locations
- **Auto-refresh dashboard**: Updates every 5 seconds
- **Metrics tracking**: Total rides, passengers, and timestamps
- **Base distribution**: Bar chart showing rides per base (if available)

## 🧹 Cleanup

To stop all services:

```bash
docker-compose down
```

To stop and remove volumes (deletes all data):

```bash
docker-compose down -v
```

To deactivate virtual environment:

```bash
deactivate
```

## 📦 Dependencies

Core Python packages (see `requirements.txt`):
- pandas==2.2.3
- kafka-python==2.0.2
- sqlalchemy==2.0.36
- psycopg2-binary==2.9.9
- streamlit==1.39.0
- plotly==5.24.1
- streamlit-autorefresh==1.0.1

## 🔧 Troubleshooting

### Services not starting
```bash
# Check service status
docker-compose ps

# View logs for specific service
docker-compose logs kafka
docker-compose logs postgres
docker-compose logs zookeeper
```

### Kafka connection issues
```bash
# Restart Kafka services
docker-compose restart kafka zookeeper

# Check Kafka is accessible
docker-compose exec kafka kafka-topics --list --bootstrap-server localhost:9092
```

### Database connection issues
```bash
# Check PostgreSQL is running
docker-compose ps postgres

# Connect to database manually
docker-compose exec postgres psql -U user -d uberdb
```

### Port conflicts
If ports are in use, modify the port mappings in `docker-compose.yml`:
```yaml
ports:
  - "NEW_PORT:CONTAINER_PORT"
```

### Reset everything
```bash
# Stop and remove all containers and volumes
docker-compose down -v

# Re-run setup
./script.sh
python init_database.py
```

## 📝 Notes

- The producer simulates real-time data by sending records with a 0.2s delay
- The consumer stores all incoming messages in PostgreSQL
- The dashboard auto-refreshes every 5 seconds to show new data
- Data is cached for 5 seconds to improve performance

## 🤝 Contributing

Feel free to submit issues or pull requests for improvements!

## 📄 License

This project is for educational purposes.