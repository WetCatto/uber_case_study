# 🚖 Uber Real-Time Data Streaming Pipeline

A real-time data streaming pipeline that simulates Uber ride data using Kafka, PostgreSQL, and Streamlit for live visualization.

## 📋 Architecture

```
┌─────────────┐      ┌───────┐      ┌──────────┐      ┌──────────────┐      ┌───────────┐
│ uber_sample │ ───> │ Kafka │ ───> │  Kafka   │ ───> │  PostgreSQL  │ ───> │ Streamlit │
│   .csv      │      │ Topic │      │ Consumer │      │   Database   │      │ Dashboard │
└─────────────┘      └───────┘      └──────────┘      └──────────────┘      └───────────┘
     Producer          rides_raw       Stores data       rides table         Visualizes
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

### 1. Prerequisites

This project requires **Docker** to run the pipeline's services.
- Please install **[Docker Desktop](https://www.docker.com/products/docker-desktop/)** (or Docker Engine on Linux) before you begin.

### 2. Setup & Run (All Systems)

Follow these manual steps to get the pipeline running.

**1. Start Services**

Note: if you are in linux you can run:
```bash
chmod +x script.sh
./script.sh
```

This single command starts Kafka, Zookeeper, and Postgres in the background.
```bash
docker compose up -d
```
Note: Wait about 60 seconds for the services to fully initialize.

2. Create Python Environment

Bash

python -m venv .venv
3. Activate Environment

On Windows (Command Prompt):

Bash

.venv\Scripts\activate.bat
On Windows (PowerShell):

Bash

.venv\Scripts\Activate.ps1
On macOS & Linux:

Bash

source .venv/bin/activate
4. Install Dependencies

Bash

pip install -r requirements.txt
5. Initialize Database This script connects to the Postgres container and creates the rides table.

Bash

python init_database.py### 3. Run the Pipeline

Open **3 separate terminal windows** (and make sure your virtual environment is activated in each one):

#### Terminal 1: Start Producer
```bash
python producer/producer.py
```

#### Terminal 2: Start Consumer
```bash
python consumer/consumer.py
```

#### Terminal 3: Start Dashboard
```bash
streamlit run dashboard/app.py
```

## 🌐 Access Points

Once everything is running, you can access:

- **Streamlit Dashboard**: http://localhost:8501
- **Kafka UI**: http://localhost:8080
- **PostgreSQL**: localhost:5432

## 📊 Features

- **Real-time streaming**: Simulates live ride data from CSV
- **Live map visualization**: Shows ride pickup locations
- **Auto-refresh dashboard**: Updates every 5 seconds
- **Metrics tracking**: Total rides, passengers, and timestamps

## 🧹 Cleanup

To stop all services:

```bash
docker compose down
```

To stop and remove volumes (deletes all data):

```bash
docker compose down -v
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

### Issue: "Module not found"
**Solution:** Make sure virtual environment is activated:
```bash
# On macOS/Linux:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate.bat
```

### Issue: Dashboard shows no data
**Solution:** Make sure producer and consumer are both running before starting the dashboard

---

## 📝 Notes

- The producer simulates real-time data by sending records with a 0.2s delay
- The consumer stores all incoming messages in PostgreSQL
- The dashboard auto-refreshes every 5 seconds to show new data
- Data is cached for 5 seconds to improve performance

## 📝 Quick Reference

| Component | Command | URL |
|-----------|---------|-----|
| Setup | `./script.sh` | - |
| Producer | `python producer/producer.py` | - |
| Consumer | `python consumer/consumer.py` | - |
| Dashboard | `streamlit run dashboard/app.py` | http://localhost:8501 |
| Kafka UI | - | http://localhost:8080 |
| Stop All | `docker-compose down` | - |

## 🤝 Contributing

Feel free to submit issues or pull requests for improvements!

## 📄 License

This project is for educational purposes.