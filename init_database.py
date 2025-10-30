"""
Initialize PostgreSQL database with rides table matching Kafka consumer schema
"""
from sqlalchemy import create_engine, text

# Database connection
DATABASE_URL = "postgresql://user:password@localhost:5432/uberdb"
engine = create_engine(DATABASE_URL)

def create_rides_table():
    """Create the rides table matching the Kafka message structure"""
    
    # Drop existing table if it exists (optional - remove if you want to keep data)
    drop_table_query = "DROP TABLE IF EXISTS rides;"
    
    # Create table with the correct schema for your Kafka data
    create_table_query = """
    CREATE TABLE IF NOT EXISTS rides (
        pickup_datetime TIMESTAMP NOT NULL,
        latitude FLOAT NOT NULL,
        longitude FLOAT NOT NULL,
        passenger_count INTEGER NOT NULL,
        base VARCHAR(50)
    );
    """
    
    # Create index for faster queries
    create_index_query = """
    CREATE INDEX IF NOT EXISTS idx_pickup_datetime 
    ON rides (pickup_datetime DESC);
    """
    
    with engine.connect() as conn:
        print("🗑️  Dropping existing rides table (if exists)...")
        conn.execute(text(drop_table_query))
        
        print("📋 Creating rides table...")
        conn.execute(text(create_table_query))
        
        print("⚡ Creating index on pickup_datetime...")
        conn.execute(text(create_index_query))
        
        conn.commit()
    
    print("✅ Table 'rides' created successfully!")
    print("\n📊 Table schema:")
    print("   - pickup_datetime (TIMESTAMP)")
    print("   - latitude (FLOAT)")
    print("   - longitude (FLOAT)")
    print("   - passenger_count (INTEGER)")
    print("   - base (VARCHAR)")

def verify_table():
    """Verify the table was created correctly"""
    query = """
    SELECT column_name, data_type 
    FROM information_schema.columns 
    WHERE table_name = 'rides';
    """
    
    with engine.connect() as conn:
        result = conn.execute(text(query))
        columns = result.fetchall()
    
    if columns:
        print("\n✅ Verification successful!")
        print("Columns in 'rides' table:")
        for col in columns:
            print(f"   - {col[0]}: {col[1]}")
    else:
        print("\n❌ Table not found!")

def main():
    print("🚀 Initializing database for Uber streaming pipeline...\n")
    
    try:
        create_rides_table()
        verify_table()
        
        print("\n🎉 Database initialization complete!")
        print("\n📝 Next steps:")
        print("   1. Make sure your Kafka containers are running")
        print("   2. Run the producer: python producer/producer.py")
        print("   3. Run the consumer: python consumer/consumer.py")
        print("   4. Run the dashboard: streamlit run dashboard/app.py")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()