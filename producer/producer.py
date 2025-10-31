import time
import json
import pandas as pd
from confluent_kafka import Producer

# Kafka Producer configuration
KAFKA_BROKER = "localhost:9092" 
TOPIC_NAME = "rides_raw"

# Initialize Kafka producer
conf = {
    'bootstrap.servers': KAFKA_BROKER,
    'client.id': 'uber-producer',
    'enable.idempotence': True
}

# Load dataset
print("📂 Loading dataset...")
df = pd.read_csv("data/uber_sample.csv").head(5000)
print(f"✅ Loaded {len(df)} records")

# Initialize Kafka producer
conf = {
    'bootstrap.servers': KAFKA_BROKER,
    'client.id': 'uber-producer'
}
producer = Producer(conf)

def delivery_report(err, msg):
    """Callback for message delivery reports"""
    if err is not None:
        print(f'❌ Message delivery failed: {err}')
    # Uncomment to see delivery confirmations
    # else:
    #     print(f'✅ Message delivered to {msg.topic()} [{msg.partition()}]')

print("🚗 Kafka Producer started. Streaming Uber ride data...")
print(f"📊 Sending to topic: {TOPIC_NAME}")
print("-" * 60)

sent_count = 0

for _, row in df.iterrows():
    message = {
        "pickup_datetime": str(row["pickup_datetime"]),
        "latitude": float(row["latitude"]),
        "longitude": float(row["longitude"]),
        "passenger_count": int(row["passenger_count"])
    }
    
    # Include base column if present in dataset
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
    
    sent_count += 1
    
    # Print progress every 100 messages
    if sent_count % 100 == 0:
        print(f"📤 Sent {sent_count} messages...")
        producer.flush()
    
    # Simulate live feed
    time.sleep(0.2)

# Wait for all messages to be delivered
producer.flush()

print("-" * 60)
print(f"✅ Finished streaming {sent_count} Uber rides!")
print(f"📊 Topic: {TOPIC_NAME}")
print(f"🔗 Kafka Broker: {KAFKA_BROKER}")