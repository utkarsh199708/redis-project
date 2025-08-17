Redis Source to Replica Script
================================

📌 Overview
-----------
This script demonstrates replication verification between a Redis source instance and its replica.

It performs the following tasks:
1. Connects to source Redis (`redis-12000.localhost:12000` by default).
2. Connects to replica Redis (`redis-12001.localhost:12001` by default).
3. Verifies replication setup using a test key.
4. Inserts values 1-100 into the source database.
5. Reads values from the replica database in reverse order (100 → 1).
6. Provides a summary of replication status and missing keys (if any).

⚙️ Prerequisites
-----------------
- Python 3.7+
- redis-py client library

Install dependencies:
    pip install redis

- Running two Redis instances:
  - Source: redis-12000.localhost:12000
  - Replica: redis-12001.localhost:12001
  - Ensure replication is configured between the two.

🚀 Usage
--------
1. Save the script as `redis_source_to_replica.py`.
2. Make the script executable:
       chmod +x redis_source_to_replica.py
3. Run the script:
       ./redis_source_to_replica.py
   or:
       python3 redis_source_to_replica.py

🔍 Script Details
-----------------
1. Connection
   - Uses retry logic (3 attempts with backoff).
   - Verifies connectivity with PING.

2. Replication Verification
   - Inserts a test key in the source (replication_test) and checks if it appears in replica.

3. Data Insertion
   - Inserts keys key:1 → key:100 into the source.
   - Uses Redis pipelines for batch performance.

4. Data Reading
   - Reads from replica in reverse order (key:100 → key:1).
   - Logs missing or failed reads.

5. Summary
   - Shows:
     - Total inserted values
     - Successfully read values
     - Missing keys (with preview)

📊 Example Output
-----------------
🚀 Redis Source to Replica Data Transfer Script
==================================================
✓ Connected to source-db at redis-12000.localhost:12000
✓ Connected to replica-db at redis-12001.localhost:12001

🔍 Verifying replication status...
Set replication_test = test_1692345678 in source-db
✓ Replication is working correctly

📝 Inserting values 1-100 into source-db...
✓ Successfully inserted 100/100 values into source-db

📖 Reading values in reverse order from replica-db...
⏳ Waiting 2 seconds for replication to sync...
key:100 = 100
key:99 = 99
...
key:1 = 1

✓ Successfully read 100/100 values from replica-db

==================================================
📊 SUMMARY:
   • Values inserted into source-db: 100
   • Values read from replica-db: 100
   • Missing/failed reads: 0

🎉 SUCCESS: All values successfully replicated and read!

🔌 Connections closed

⚠️ Notes & Troubleshooting
--------------------------
- If replication is not configured, the script will warn:
  ⚠️ Replication may not be properly configured
- If keys are missing from the replica, they will be listed in the summary.
- Update SOURCE_CONFIG and REPLICA_CONFIG in the script to match your environment.
