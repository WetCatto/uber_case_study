import time
import json
import pandas as pd
from confluent_kafka import Producer
import random  

# Kafka Producer configuration
KAFKA_BROKER = "localhost:9092" 
TOPIC_NAME = "rides_raw"

# Load dataset
print("📂 Loading dataset...")
df = pd.read_csv("data/uber_sample.csv").head(5000)
print(f"✅ Loaded {len(df)} records")

# Initialize Kafka producer
conf = {
    'bootstrap.servers': KAFKA_BROKER,
    'client.id': 'uber-producer',
    'enable.idempotence': True
}
producer = Producer(conf)

def delivery_report(err, msg):
    """Callback for message delivery reports"""
    if err is not None:
        print(f'❌ Message delivery failed: {err}')
    else:
        print(f'✅ Message delivered to {msg.topic()} [{msg.partition()}]')

print("🚗 Kafka Producer started. Streaming Uber ride data...")
print(f"📊 Sending to topic: {TOPIC_NAME}")
print("-" * 60)

total_sent = 0
batch_sent_count = 0
current_batch_size = random.randint(5, 15)

for _, row in df.iterrows():
    message = {
        "pickup_datetime": str(row["pickup_datetime"]),
        "latitude": float(row["latitude"]),
        "longitude": float(row["longitude"]),
        "passenger_count": int(row["passenger_count"])
    }
    
    if "base" in df.columns:
        message["base"] = str(row["base"])
    
    # Serialize message to JSON
    message_json = json.dumps(message)
    
    # Send message
    producer.produce(
        TOPIC_NAME,
        value=message_json.encode('utf-8'),
        callback=delivery_report
    )
    
    batch_sent_count += 1
    total_sent += 1
    
    if batch_sent_count == current_batch_size:
        print(f"📤 Flushed batch of {batch_sent_count} messages. (Total: {total_sent})")
        producer.flush()
        
        time.sleep(random.uniform(0.5, 2.0))
        
        current_batch_size = random.randint(5, 15)
        batch_sent_count = 0 

# This catches the last few messages that didn't fill a full batch
if batch_sent_count > 0:
    print(f"📤 Flushed final batch of {batch_sent_count} messages. (Total: {total_sent})")
    producer.flush()

print("-" * 60)
print(f"✅ Finished streaming {total_sent} Uber rides!")
print(f"📊 Topic: {TOPIC_NAME}")
print(f"🔗 Kafka Broker: {KAFKA_BROKER}")