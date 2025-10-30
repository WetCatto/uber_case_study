# 🚖 Step-by-Step Guide: Running the Uber Streaming Pipeline

Follow these steps exactly to get your Uber real-time streaming pipeline running.

---

## ⚙️ Prerequisites

Before you start, make sure you have:
- ✅ Python 3.8 or higher installed
- ✅ Docker and Docker Compose installed
- ✅ Terminal/Command Line access

---

## 📋 Step 1: Navigate to Project Directory

Open your terminal and go to the project folder:

```bash
cd /home/wetcatto/.code/uber_case_study
```

Or wherever your project is located.

---

## 🔧 Step 2: Run Setup Script

Make the script executable and run it:

```bash
chmod +x script.sh
./script.sh
```

**What this does:**
- Creates a Python virtual environment in `.venv/`
- Installs all required Python packages
- Starts Docker containers (Kafka, Zookeeper, Kafka UI, PostgreSQL)
- **Automatically initializes the database with the correct schema**

**Expected output:**
```
🚀 Starting Uber streaming pipeline setup...
🐍 Setting up Python virtual environment...
📚 Installing Python dependencies...
✅ Dependencies installed successfully!
🐳 Starting Docker services with docker-compose...
✅ Checking container status:
🗄️  Initializing PostgreSQL database...
📋 Creating rides table...
✅ Table 'rides' created successfully!
```

⏱️ **Wait time:** ~45 seconds

---

## ✅ Step 3: Verify Services are Running

Check that all Docker containers are up:

```bash
docker-compose ps
```

You should see 4 containers running:
- ✅ `kafka`
- ✅ `zookeeper`
- ✅ `kafka-ui`
- ✅ `postgres`

---

## 🚀 Step 4: Run the Pipeline

Now you'll run three components in **3 separate terminal windows**.

### Terminal 1: Start the Producer

```bash
cd /home/wetcatto/.code/uber_case_study
source .venv/bin/activate
python producer/producer.py
```

**What this does:**
- Reads data from `data/uber_sample.csv`
- Sends ride data to Kafka topic `rides_raw`
- Simulates real-time streaming with 0.2s delay

**Expected output:**
```
📂 Loading dataset...
✅ Loaded 5000 records
🚗 Kafka Producer started. Streaming Uber ride data...
📊 Sending to topic: rides_raw
------------------------------------------------------------
📤 Sent 100 messages...
📤 Sent 200 messages...
...
```

### Terminal 2: Start the Consumer

Open a **new terminal window**:

```bash
cd /home/wetcatto/.code/uber_case_study
source .venv/bin/activate
python consumer/consumer.py
```

**What this does:**
- Listens to Kafka topic `rides_raw`
- Stores incoming data to PostgreSQL database

**Expected output:**
```
📥 Kafka Consumer started. Listening for ride data...
🔗 Connected to: localhost:9092
📊 Topic: rides_raw
💾 Database: uberdb
------------------------------------------------------------
💾 Stored 10 rides...
💾 Stored 20 rides...
...
```

### Terminal 3: Start the Dashboard

Open a **third terminal window**:

```bash
cd /home/wetcatto/.code/uber_case_study
source .venv/bin/activate
streamlit run dashboard/app.py
```

**What this does:**
- Launches Streamlit web dashboard
- Displays real-time ride data and visualizations

**Expected output:**
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

---

## 🌐 Step 5: View the Dashboard

Open your web browser and go to:

```
http://localhost:8501
```

**What you'll see:**
- 📊 **Metrics**: Total rides, passengers, latest timestamp
- 🗺️ **Live Map**: Ride pickup locations
- 📈 **Charts**: Base distribution (if available)
- 🔄 **Auto-refresh**: Updates every 5 seconds

---

## 🎯 Step 6: Explore Kafka UI (Optional)

To see the Kafka messages in real-time, open:

```
http://localhost:8080
```

Navigate to:
1. **Topics** → `rides_raw`
2. View messages being produced and consumed

---

## 🛑 Step 7: Stop Everything

When you're done, stop the pipeline:

### Stop Producer, Consumer, and Dashboard
In each terminal window, press:
```
Ctrl + C
```

### Stop Docker Services
```bash
docker-compose down
```

### Deactivate Virtual Environment
```bash
deactivate
```

---

## 📊 What's Happening Behind the Scenes?

```
┌─────────────┐      ┌───────┐      ┌──────────┐      ┌──────────────┐      ┌───────────┐
│ uber_sample │ ───> │ Kafka │ ───> │  Kafka   │ ───> │  PostgreSQL  │ ───> │ Streamlit │
│   .csv      │      │ Topic │      │ Consumer │      │   Database   │      │ Dashboard │
└─────────────┘      └───────┘      └──────────┘      └──────────────┘      └───────────┘
     Producer          rides_raw       Stores data       rides table         Visualizes
```

---

## ❓ Common Issues & Solutions

### Issue: "Port already in use"
**Solution:** Stop conflicting services or change ports in `docker-compose.yml`

### Issue: "Cannot connect to Kafka"
**Solution:** 
```bash
docker-compose restart kafka zookeeper
sleep 10
# Then restart producer/consumer
```

### Issue: "Module not found"
**Solution:** Make sure virtual environment is activated:
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### Issue: Dashboard shows no data
**Solution:** Make sure producer and consumer are both running before starting the dashboard

---

## 🎉 Success!

If you see:
- ✅ Producer sending messages
- ✅ Consumer storing data
- ✅ Dashboard showing live updates

**Congratulations! Your real-time streaming pipeline is working!** 🚀

---

## 📝 Quick Reference

| Component | Command | URL |
|-----------|---------|-----|
| Setup | `./script.sh` | - |
| Producer | `python producer/producer.py` | - |
| Consumer | `python consumer/consumer.py` | - |
| Dashboard | `streamlit run dashboard/app.py` | http://localhost:8501 |
| Kafka UI | - | http://localhost:8080 |
| Stop All | `docker-compose down` | - |