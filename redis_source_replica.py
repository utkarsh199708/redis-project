#!/usr/bin/env python3
"""
Redis Source to Replica Script
Inserts values 1-100 into source-db and reads them in reverse order from replica-db
"""

import redis
import time
import sys

# Redis connection configurations
SOURCE_CONFIG = {
    'host': 'redis-12000.localhost',  # or 'localhost' if hostname doesn't resolve
    'port': 12000,
    'decode_responses': True
}

REPLICA_CONFIG = {
    'host': 'redis-12001.localhost',  # Adjust port for replica-db
    'port': 12001,  # You'll need to update this with actual replica port
    'decode_responses': True
}

def connect_to_redis(config, db_name):
    """Connect to Redis with retry logic"""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            client = redis.Redis(**config)
            client.ping()
            print(f"✓ Connected to {db_name} at {config['host']}:{config['port']}")
            return client
        except redis.ConnectionError as e:
            print(f"✗ Connection attempt {attempt + 1} failed for {db_name}: {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
            else:
                print(f"✗ Failed to connect to {db_name} after {max_retries} attempts")
                return None
        except Exception as e:
            print(f"✗ Unexpected error connecting to {db_name}: {e}")
            return None

def insert_values_to_source(source_client):
    """Insert values 1-100 into source database"""
    print("\n📝 Inserting values 1-100 into source-db...")
    
    try:
        # Use pipeline for better performance
        pipe = source_client.pipeline()
        
        for i in range(1, 101):
            key = f"key:{i}"
            value = str(i)
            pipe.set(key, value)
        
        # Execute all commands at once
        results = pipe.execute()
        successful_inserts = sum(1 for result in results if result)
        
        print(f"✓ Successfully inserted {successful_inserts}/100 values into source-db")
        return successful_inserts == 100
        
    except Exception as e:
        print(f"✗ Error inserting values into source-db: {e}")
        return False

def read_values_from_replica(replica_client):
    """Read values in reverse order (100-1) from replica database"""
    print("\n📖 Reading values in reverse order from replica-db...")
    
    try:
        # Wait a moment for replication to sync
        print("⏳ Waiting 2 seconds for replication to sync...")
        time.sleep(2)
        
        values_read = []
        missing_keys = []
        
        # Read keys in reverse order (100 to 1)
        for i in range(100, 0, -1):
            key = f"key:{i}"
            try:
                value = replica_client.get(key)
                if value is not None:
                    values_read.append((key, value))
                    print(f"key:{i} = {value}")
                else:
                    missing_keys.append(key)
                    print(f"✗ {key} not found in replica-db")
            except Exception as e:
                print(f"✗ Error reading {key}: {e}")
                missing_keys.append(key)
        
        print(f"\n✓ Successfully read {len(values_read)}/100 values from replica-db")
        if missing_keys:
            print(f"✗ Missing keys: {len(missing_keys)}")
        
        return len(values_read), missing_keys
        
    except Exception as e:
        print(f"✗ Error reading values from replica-db: {e}")
        return 0, []

def verify_replication_status(source_client, replica_client):
    """Verify replication is working by checking a test key"""
    print("\n🔍 Verifying replication status...")
    
    try:
        test_key = "replication_test"
        test_value = f"test_{int(time.time())}"
        
        # Set in source
        source_client.set(test_key, test_value)
        print(f"Set {test_key} = {test_value} in source-db")
        
        # Wait and check in replica
        time.sleep(1)
        replica_value = replica_client.get(test_key)
        
        if replica_value == test_value:
            print("✓ Replication is working correctly")
            return True
        else:
            print(f"✗ Replication issue: source='{test_value}', replica='{replica_value}'")
            return False
            
    except Exception as e:
        print(f"✗ Error verifying replication: {e}")
        return False

def main():
    print("🚀 Redis Source to Replica Data Transfer Script")
    print("=" * 50)
    
    # Connect to source database
    source_client = connect_to_redis(SOURCE_CONFIG, "source-db")
    if not source_client:
        print("❌ Cannot proceed without source database connection")
        sys.exit(1)
    
    # Connect to replica database
    replica_client = connect_to_redis(REPLICA_CONFIG, "replica-db")
    if not replica_client:
        print("❌ Cannot proceed without replica database connection")
        sys.exit(1)
    
    # Verify replication is set up
    if not verify_replication_status(source_client, replica_client):
        print("⚠️  Replication may not be properly configured")
    
    # Insert values into source
    if not insert_values_to_source(source_client):
        print("❌ Failed to insert values into source database")
        sys.exit(1)
    
    # Read values from replica in reverse order
    values_read, missing_keys = read_values_from_replica(replica_client)
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 SUMMARY:")
    print(f"   • Values inserted into source-db: 100")
    print(f"   • Values read from replica-db: {values_read}")
    print(f"   • Missing/failed reads: {len(missing_keys)}")
    
    if values_read == 100:
        print("🎉 SUCCESS: All values successfully replicated and read!")
    else:
        print(f"⚠️  WARNING: Only {values_read}/100 values were successfully read")
        if missing_keys:
            print(f"   Missing keys: {missing_keys[:10]}{'...' if len(missing_keys) > 10 else ''}")
    
    # Clean up connections
    source_client.close()
    replica_client.close()
    print("\n🔌 Connections closed")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Script interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
