# Redis Project – Replication, API Integration & Semantic Routing

This repository demonstrates Redis Enterprise capabilities through three focused deliverables:

1. **Replication Demo** – Build and verify source–replica synchronization  
2. **Direct API/CRUD Demo** – Manage data & users programmatically with `redis-py`  
3. **Semantic Routing (Bonus)** – Intelligent query routing with Redis Stack + RedisVL  

It’s organized for a **customer-ready demo**: quick to run, clear outputs, and easy to extend.

---

## 📂 Repository Contents

```
redis-project/
├── redis_source_replica.py                # Exercise 1: source→replica verification, 1..100 insert & reverse read
├── connect.py                             # Exercise 2: direct redis-py CRUD + user listing demo
├── semanticrouting.py                     # Bonus: semantic router using RedisVL (3 routes)
├── redis_source_replica_readme.txt        # Exercise 1 notes
├── redis_direct_connection_readme.txt     # Exercise 2 notes
├── Redis_Semantic_Router_Project_README.txt  # Bonus notes
└── README.md                              # (this file)
```

> Tip: Keep scripts runnable independently so each exercise can be demoed in isolation.

---

## 1️⃣ Exercise 1 — Source/Replica: Build & Verify

**Goal:** Create `source-db` and `replica-db`, populate `source-db` with values **1..100**, then read **100..1** from `replica-db` to validate replication.

### What the script does (`redis_source_replica.py`)
- Connects to source (e.g., `redis-12000.localhost:12000`) and replica (e.g., `redis-12001.localhost:12001`)  
- Health checks (PING + test key)  
- Inserts `key:1`…`key:100` on source using pipeline  
- Reads from replica in reverse order  
- Prints summary with counts and any missing keys  

### Run
```bash
python3 redis_source_replica.py
```

### Include memtier benchmark (customer-visible)
On the load node, run memtier to generate load and save the exact command used:

```bash
memtier_benchmark -s <SOURCE_HOST> -p <SOURCE_PORT>   --ratio=1:1 --protocol=redis --key-maximum=100000   --data-size=64 --clients=10 --threads=2 --pipeline=8   --test-time=60 > /tmp/memtier_benchmark.txt
```

**Customer value:** Demonstrates **HA/DR** and replication integrity under load.

---

## 2️⃣ Exercise 2 — Direct API/CRUD with redis-py

**Goal:** Simulate database namespace creation, add three users, list them, then cleanup.

### What the script does (`connect.py`)
- Creates a logical “namespace” via key prefixes (e.g., `db:metadata:<ns>`)  
- Adds three users as Redis hashes + tracks emails in a set (`users:all`)  
- Lists users in a clean table  
- Deletes namespace & cleans demo data  

### Run
```bash
python3 connect.py
```

**Customer value:** Shows **governance patterns** (structured keys, user list) and safe lifecycle management.

> Note: The original challenge references the Redis REST API endpoint. This script uses direct redis-py to simulate the same CRUD. If needed, add a companion script with actual REST calls (e.g., Python `requests`) to create DBs and users against the cluster endpoint.

---

## 3️⃣ Bonus — Semantic Router with RedisVL

**Goal:** Route natural language queries to the best domain:

- 🤖 `genai_programming` — AI/ML/LLMs, RAG  
- 🚀 `science_fiction` — movies, books, cyberpunk, space opera  
- 🎼 `classical_music` — composers, symphonies, theory  

### What the script does (`semanticrouting.py`)
- Uses a sentence-transformer via RedisVL to embed the query  
- Performs vector similarity search in Redis Stack  
- Returns **best route + confidence score** and (optionally) ranked alternatives  

### Run
```bash
# Install deps (example)
pip install redis redisvl sentence-transformers

python3 semanticrouting.py
```

**Customer value:** Positions Redis Stack as **GenAI-ready** for intelligent classification and routing.

---

## 🔧 Configuration (env-first)

All scripts should honor environment variables (fallback to sensible defaults):

```bash
# Source/Replica
export SOURCE_REDIS_HOST=redis-12000.localhost
export SOURCE_REDIS_PORT=12000
export REPLICA_REDIS_HOST=redis-12001.localhost
export REPLICA_REDIS_PORT=12001

# Passwords (if used)
export SOURCE_REDIS_PASSWORD=
export REPLICA_REDIS_PASSWORD=

# Semantic Router DB (Redis Stack)
export ROUTER_REDIS_URL=redis://localhost:6379
```

