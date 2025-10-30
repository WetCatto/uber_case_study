import json
import pandas as pd
from confluent_kafka import Consumer, KafkaError
from sqlalchemy import create_engine

# Database connection
DB_URI = "postgresql://user:password@localhost:5432/uberdb"
engine = create_engine(DB_URI)

# Kafka Consumer configuration
conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'uber-group',
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': True
}

consumer = Consumer(conf)
consumer.subscribe(['rides_raw'])

print("📥 Kafka Consumer started. Listening for ride data...")
print("🔗 Connected to: localhost:9092")
print("📊 Topic: rides_raw")
print("💾 Database: uberdb")
print("-" * 60)

stored_count = 0

try:
    while True:
        msg = consumer.poll(timeout=1.0)
        
        if msg is None:
            continue
        
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                # End of partition
                continue
            else:
                print(f"❌ Consumer error: {msg.error()}")
                break
        
        # Decode and parse message
        data = json.loads(msg.value().decode('utf-8'))
        
        # Convert to DataFrame and store in database
        df = pd.DataFrame([data])
        df.to_sql("rides", engine, if_exists="append", index=False)
        
        stored_count += 1
        
        # Print progress every 10 messages
        if stored_count % 10 == 0:
            print(f"💾 Stored {stored_count} rides...")
        
        # Uncomment to see each message
        # print(f"Stored: {data}")

except KeyboardInterrupt:
    print("\n⚠️  Stopping consumer...")

finally:
    consumer.close()
    print("-" * 60)
    print(f"✅ Consumer stopped. Total stored: {stored_count} rides")
    print("👋 Goodbye!")