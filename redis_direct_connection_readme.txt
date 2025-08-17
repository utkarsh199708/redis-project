Redis Direct Connection Script
==============================

This repository contains a Python script that connects directly to a Redis instance using the redis-py client.
It demonstrates how to simulate database operations such as creating namespaces, adding users, listing users,
and cleaning up data — all directly in Redis.

Features
--------
- Connects to Redis (redis-12000.localhost:12000)
- Simulates database namespaces using Redis key prefixes
- Creates and manages user records stored as Redis hashes
- Lists and displays users in a formatted table
- Deletes namespaces and cleans up demo data

Requirements
------------
- Python 3.7+
- A Redis server running on redis-12000.localhost:12000
- Dependency: redis

Install the required dependency:

    pip install redis

Running the Script
------------------
Run the script with:

    python3 redis_direct_connection.py

Example Output
--------------
Redis Direct Connection Script
==============================
Connecting to redis-12000.localhost:12000
✓ Successfully connected to Redis at redis-12000.localhost:12000

Step 1: Creating Database Namespace
----------------------------------------
✓ Database namespace 'test-database-exercise2' created successfully

Step 2: Creating Users
------------------------------
✓ User 'John Doe' (john.doe@example.com) with role 'db_viewer' created successfully
✓ User 'Mike Smith' (mike.smith@example.com) with role 'db_member' created successfully
✓ User 'Cary Johnson' (cary.johnson@example.com) with role 'admin' created successfully

Step 3: Listing Users
------------------------------
USER LISTING
============================================================
Name                 Role            Email
------------------------------------------------------------
John Doe             db_viewer       john.doe@example.com
Mike Smith           db_member       mike.smith@example.com
Cary Johnson         admin           cary.johnson@example.com
============================================================

Step 4: Deleting Database Namespace
----------------------------------------
✓ Database namespace 'test-database-exercise2' deleted (removed 1 keys)

Step 5: Cleaning Up Demo Data
-----------------------------------
✓ Cleaned up user: john.doe@example.com
✓ Cleaned up user: mike.smith@example.com
✓ Cleaned up user: cary.johnson@example.com
✓ Cleaned up empty users set

Script execution completed successfully!

Script Overview
---------------
RedisDirectClient methods:
- create_database_namespace(namespace) → creates a logical DB namespace
- create_user_record(email, name, role) → adds a user as a Redis hash
- list_users() → retrieves all users
- display_users(users) → prints user info in table format
- delete_database_namespace(namespace) → deletes namespace metadata
- cleanup_demo_data() → removes demo users and related keys

Execution Flow (main):
1. Connect to Redis
2. Create a demo database namespace
3. Insert three users
4. List and display users
5. Delete the namespace
6. Clean up demo data

Notes
-----
- Redis does not natively support multiple databases in this sense; namespaces are simulated using key prefixes.
- Users are stored in Redis hashes, with a set (users:all) tracking all user emails.
- Safe to re-run — cleanup removes demo data at the end.

License
-------
This script is provided as-is for demo and educational purposes.
