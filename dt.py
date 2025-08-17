#!/usr/bin/env python3
"""
Detailed Redis Stack diagnostic script
"""
import redis
import json

def detailed_redis_test():
    """Run comprehensive Redis Stack tests"""
    
    print("🔍 Detailed Redis Stack Diagnostic")
    print("=" * 50)
    
    try:
        # Test different connection methods
        print("\n1. Testing Redis connection methods...")
        
        # Method 1: Basic Redis connection
        r1 = redis.Redis(host='localhost', port=6379, decode_responses=True)
        print(f"✅ Method 1 - Basic connection: {r1.ping()}")
        
        # Method 2: Redis from URL
        r2 = redis.Redis.from_url("redis://localhost:6379", decode_responses=True)
        print(f"✅ Method 2 - URL connection: {r2.ping()}")
        
        # Method 3: Without decode_responses
        r3 = redis.Redis(host='localhost', port=6379)
        print(f"✅ Method 3 - Binary connection: {r3.ping()}")
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False
    
    print("\n2. Testing Redis info...")
    try:
        info = r1.info()
        print(f"✅ Redis version: {info.get('redis_version', 'Unknown')}")
        print(f"✅ Redis mode: {info.get('redis_mode', 'Unknown')}")
        print(f"✅ OS: {info.get('os', 'Unknown')}")
    except Exception as e:
        print(f"❌ Info command failed: {e}")
    
    print("\n3. Testing MODULE LIST command with different methods...")
    
    # Method A: Using execute_command with decode_responses=True
    try:
        print("Method A: execute_command with decode_responses=True")
        modules_a = r1.execute_command('MODULE', 'LIST')
        print(f"Raw result type: {type(modules_a)}")
        print(f"Raw result length: {len(modules_a) if isinstance(modules_a, list) else 'Not a list'}")
        
        if isinstance(modules_a, list) and len(modules_a) > 0:
            print("First few elements:")
            for i in range(min(10, len(modules_a))):
                print(f"  [{i}]: {modules_a[i]} (type: {type(modules_a[i])})")
        
        # Try to find search module
        search_found_a = False
        if isinstance(modules_a, list):
            for i in range(0, len(modules_a), 2):
                if i + 1 < len(modules_a):
                    module_info = modules_a[i]
                    if isinstance(module_info, list) and len(module_info) >= 4:
                        if module_info[1] == 'search':
                            search_found_a = True
                            print(f"✅ Method A - Search module found: version {module_info[3]}")
                            break
        
        if not search_found_a:
            print("❌ Method A - Search module not found")
            
    except Exception as e:
        print(f"❌ Method A failed: {e}")
    
    # Method B: Using execute_command without decode_responses
    try:
        print("\nMethod B: execute_command without decode_responses")
        modules_b = r3.execute_command('MODULE', 'LIST')
        print(f"Raw result type: {type(modules_b)}")
        print(f"Raw result length: {len(modules_b) if isinstance(modules_b, list) else 'Not a list'}")
        
        if isinstance(modules_b, list) and len(modules_b) > 0:
            print("First few elements:")
            for i in range(min(10, len(modules_b))):
                elem = modules_b[i]
                if isinstance(elem, bytes):
                    elem_str = elem.decode('utf-8')
                else:
                    elem_str = str(elem)
                print(f"  [{i}]: {elem_str} (type: {type(modules_b[i])})")
        
        # Try to find search module
        search_found_b = False
        if isinstance(modules_b, list):
            for i in range(0, len(modules_b), 2):
                if i + 1 < len(modules_b):
                    module_info = modules_b[i]
                    if isinstance(module_info, list) and len(module_info) >= 4:
                        name_field = module_info[1]
                        if isinstance(name_field, bytes):
                            name_field = name_field.decode('utf-8')
                        if name_field == 'search':
                            search_found_b = True
                            version_field = module_info[3]
                            if isinstance(version_field, bytes):
                                version_field = version_field.decode('utf-8')
                            print(f"✅ Method B - Search module found: version {version_field}")
                            break
        
        if not search_found_b:
            print("❌ Method B - Search module not found")
            
    except Exception as e:
        print(f"❌ Method B failed: {e}")
    
    # Method C: Direct redis-cli equivalent
    try:
        print("\nMethod C: Using redis-py pipeline")
        pipe = r1.pipeline()
        pipe.execute_command('MODULE', 'LIST')
        result = pipe.execute()
        modules_c = result[0] if result else None
        
        print(f"Pipeline result type: {type(modules_c)}")
        if modules_c:
            print(f"Pipeline result length: {len(modules_c)}")
            
    except Exception as e:
        print(f"❌ Method C failed: {e}")
    
    print("\n4. Testing alternative module detection...")
    try:
        # Try FT.INFO to test search module directly
        try:
            ft_info = r1.execute_command('FT._LIST')
            print(f"✅ FT._LIST command works: {len(ft_info) if isinstance(ft_info, list) else 'Success'}")
        except Exception as ft_e:
            print(f"❌ FT._LIST command failed: {ft_e}")
        
        # Try module detection with different parsing
        raw_modules = r3.execute_command('MODULE', 'LIST')
        print(f"\n5. Raw module data structure analysis:")
        print(f"Type: {type(raw_modules)}")
        
        if isinstance(raw_modules, list):
            print("Attempting to parse modules manually...")
            for i, module_group in enumerate(raw_modules):
                print(f"\nModule {i}:")
                print(f"  Type: {type(module_group)}")
                print(f"  Content: {module_group}")
                
                if isinstance(module_group, list):
                    for j, field in enumerate(module_group):
                        field_value = field
                        if isinstance(field, bytes):
                            field_value = field.decode('utf-8')
                        print(f"    [{j}]: {field_value}")
                        
                        # Check if this is the name field with value 'search'
                        if j == 1 and field_value == 'search':
                            print(f"    🎯 FOUND SEARCH MODULE in group {i}")
                            if j + 2 < len(module_group):
                                version = module_group[j + 2]
                                if isinstance(version, bytes):
                                    version = version.decode('utf-8')
                                print(f"    🎯 Version: {version}")
        
    except Exception as e:
        print(f"❌ Alternative detection failed: {e}")
    
    print("\n6. Testing RedisVL compatibility...")
    try:
        import redisvl
        print(f"✅ RedisVL version: {redisvl.__version__}")
        
        from redisvl.utils.vectorize import HFTextVectorizer
        vectorizer = HFTextVectorizer(model="sentence-transformers/all-mpnet-base-v2")
        print("✅ HFTextVectorizer created successfully")
        
    except ImportError as e:
        print(f"❌ RedisVL import failed: {e}")
    except Exception as e:
        print(f"❌ RedisVL test failed: {e}")
    
    return True

if __name__ == "__main__":
    detailed_redis_test()
