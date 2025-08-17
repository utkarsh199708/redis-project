#!/usr/bin/env python3
"""Test Redis Stack connection"""
import redis
from redisvl.extensions.router import SemanticRouter
from redisvl.utils.vectorize import HFTextVectorizer

def test_redis_connection():
    try:
        # Test basic Redis connection
        print("🔍 Testing basic Redis connection...")
        r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        r.ping()
        print("✅ Basic Redis connection successful")
        
        # Test module availability
        modules = r.execute_command('MODULE', 'LIST')
        search_found = False
        for i in range(0, len(modules), 2):
            if modules[i][1] == 'search':
                search_found = True
                version = modules[i][3]
                print(f"✅ Search module found: version {version}")
                break
        
        if not search_found:
            print("❌ Search module not found")
            return False
            
        # Test RedisVL connection
        print("🔍 Testing RedisVL connection...")
        vectorizer = HFTextVectorizer(model="sentence-transformers/all-mpnet-base-v2")
        print("✅ Vectorizer initialized successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False

if __name__ == "__main__":
    test_redis_connection()
