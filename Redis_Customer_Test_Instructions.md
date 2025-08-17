# 📄 Redis Technical Challenge – Customer Test Instructions

Hello,  

Thank you for the opportunity to demonstrate Redis Enterprise capabilities.  
This document provides **end-to-end steps** to set up Redis environments (Enterprise & Stack Server), run the exercises, and understand the customer value.  

---

## 🔧 Environment Setup with Docker

### 1. Redis Enterprise (for Replication – Exercise 1)  
Run Redis Enterprise in Docker:  

```bash
docker run -d   --cap-add sys_resource   --name redis-enterprise   -p 8443:8443 -p 12000-12010:12000-12010   redislabs/redis
```

- **UI:** [https://localhost:8443](https://localhost:8443)  
- **Default login:**  
  - Username: `admin@admin.com`  
  - Password: `admin`  

**Inside the UI:**  
1. Create **source-db** (2GB, no password, single-shard, port `12000`)  
2. Create **replica-db** (2GB, no password, single-shard, port `12001`, configure as *Replica Of* → `source-db`)  

---

### 2. Redis Stack Server (for CRUD & Semantic Router – Exercises 2 & 3)  
Run lightweight Redis Stack Server in Docker:  

```bash
docker run -d   --name redis-stack-server   -p 6379:6379 -p 8001:8001   redis/redis-stack-server:latest
```

- **UI:** [http://localhost:8001](http://localhost:8001) (RedisInsight)  
- Provides **Search**, **Query**, and **Vector** capabilities.  

---

## 1️⃣ Exercise 1 – Replication (Source → Replica with Redis Enterprise)

### 🎯 Objective  
Validate **HA and replication** in Redis Enterprise.  

### Steps  
1. Ensure `source-db` and `replica-db` are created in Enterprise (as above).  
2. Run the validation script:  
   ```bash
   python3 redis_source_replica.py
   ```
3. Script actions:  
   - Connects to source-db and replica-db  
   - Verifies replication with a test key  
   - Inserts values `1 → 100` into source-db  
   - Reads values `100 → 1` from replica-db  
   - Prints summary  

### (Optional) Load Testing with memtier_benchmark  
Run on load node:  
```bash
memtier_benchmark -s <SOURCE_HOST> -p 12000   --ratio=1:1 --protocol=redis --key-maximum=100000   --data-size=64 --clients=10 --threads=2 --pipeline=8   --test-time=60 > /tmp/memtier_benchmark.txt
```

### ✅ Expected Output  
```
✓ Connected to source-db
✓ Connected to replica-db
✓ Replication verified
✓ Inserted 100 values
✓ Read 100 values in reverse from replica
🎉 SUCCESS: Replication is working correctly!
```

**Customer Value:** Enterprise-grade **reliability, HA, and DR readiness**.  

---

## 2️⃣ Exercise 2 – CRUD Operations (Redis Stack Server)

### 🎯 Objective  
Show **governance patterns** with namespaces and users.  

### Steps  
1. Run the direct connection script:  
   ```bash
   python3 connect.py
   ```
2. Script actions:  
   - Creates a demo namespace (`db:metadata:test-database-exercise2`)  
   - Adds three users:  
     - John Doe – `db_viewer`  
     - Mike Smith – `db_member`  
     - Cary Johnson – `admin`  
   - Lists users in table format  
   - Deletes namespace & cleans demo data  

### ✅ Expected Output  
```
Step 1: Database namespace created
Step 2: Users created (viewer, member, admin)
Step 3: Users listed in table
Step 4: Namespace deleted
Step 5: Cleanup complete
```

**Customer Value:** Demonstrates **user lifecycle management and governance**.  

---

## 3️⃣ Exercise 3 – Semantic Router (Redis Stack Server + RedisVL)

### 🎯 Objective  
Show Redis Stack as a **GenAI-ready vector database** with semantic query routing.  

### Steps  
1. Ensure Redis Stack Server is running (port `6379`).  
2. Run the semantic router:  
   ```bash
   python3 semanticrouting.py
   ```
3. Enter queries interactively:  

- **GenAI Programming:**  
  ```
  How do I implement RAG with vector databases?
  ```
  → Route: `genai_programming` (Confidence ~87%)  

- **Science Fiction:**  
  ```
  Best cyberpunk novels
  ```
  → Route: `science_fiction`  

- **Classical Music:**  
  ```
  Mozart symphonies
  ```
  → Route: `classical_music`  

### ✅ Expected Output  
```
💬 Query: How do I implement RAG with vector databases?
🎯 Best Route: genai_programming
📈 Confidence: 87%
```

**Customer Value:** Shows Redis powering **semantic search, AI classification, and GenAI pipelines**.  

---

## 🔧 Configuration (Environment Variables)

Scripts can be configured with environment variables:  

```bash
# For Exercise 1
export SOURCE_REDIS_HOST=localhost
export SOURCE_REDIS_PORT=12000
export REPLICA_REDIS_HOST=localhost
export REPLICA_REDIS_PORT=12001

# For Exercise 2 & 3
export ROUTER_REDIS_URL=redis://localhost:6379
```

---

## ✅ Customer Takeaways

By completing these exercises:  

- **Exercise 1 (Enterprise Replication):** Confirms **HA/DR reliability** with replication.  
- **Exercise 2 (CRUD):** Shows **programmatic governance** for user and database lifecycle.  
- **Exercise 3 (Semantic Router):** Highlights Redis Stack as a **GenAI-ready vector database**.  

Redis Enterprise provides:  
- **Reliability** → replication and HA/DR  
- **Governance** → user and database lifecycle control  
- **Innovation** → GenAI & vector-enabled use cases  

---

## 📞 Support  

- Verify Redis Enterprise cluster at [https://localhost:8443](https://localhost:8443)  
- Use `rladmin status` for database health  
- For Redis Stack, check container logs:  
  ```bash
  docker logs redis-stack-server
  ```  

👨‍💻 Consultant: **Utkarsh Jha**  
📧 Email: utkarsh199708@gmail.com  
