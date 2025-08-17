#!/usr/bin/env python3
"""
Redis Direct Connection Script
Alternative approach using redis-py library to connect directly to Redis
For use with redis-12000.localhost:12000
"""

import redis
import json
import sys
import time
from typing import Dict, List, Optional

class RedisDirectClient:
    def __init__(self, host: str = 'redis-12000.localhost', port: int = 12000, password: str = None):
        """
        Initialize Redis direct client
        
        Args:
            host: Redis host
            port: Redis port
            password: Redis password (if required)
        """
        try:
            self.client = redis.Redis(
                host=host,
                port=port,
                password=password,
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5
            )
            
            # Test connection
            self.client.ping()
            print(f"✓ Successfully connected to Redis at {host}:{port}")
            
        except redis.ConnectionError as e:
            print(f"✗ Failed to connect to Redis at {host}:{port}")
            print(f"Error: {e}")
            raise
        except Exception as e:
            print(f"✗ Unexpected error connecting to Redis: {e}")
            raise
    
    def create_database_namespace(self, namespace: str) -> bool:
        """
        Create a database namespace (simulate database creation)
        Since Redis doesn't have databases in REST API sense, we'll use key namespaces
        
        Args:
            namespace: Namespace prefix for keys
            
        Returns:
            True if successful
        """
        try:
            # Create a metadata key to track this "database"
            db_key = f"db:metadata:{namespace}"
            db_info = {
                "name": namespace,
                "created_at": time.time(),
                "type": "redis",
                "status": "active"
            }
            
            result = self.client.hset(db_key, mapping=db_info)
            print(f"✓ Database namespace '{namespace}' created successfully")
            return True
            
        except Exception as e:
            print(f"✗ Error creating database namespace: {e}")
            return False
    
    def create_user_record(self, email: str, name: str, role: str) -> bool:
        """
        Create a user record (simulate user creation)
        Store user information in Redis hashes
        
        Args:
            email: User email
            name: User full name
            role: User role
            
        Returns:
            True if successful
        """
        try:
            user_key = f"user:{email}"
            user_data = {
                "email": email,
                "name": name,
                "role": role,
                "created_at": time.time(),
                "status": "active"
            }
            
            # Store user data
            result = self.client.hset(user_key, mapping=user_data)
            
            # Add to users list
            self.client.sadd("users:all", email)
            
            print(f"✓ User '{name}' ({email}) with role '{role}' created successfully")
            return True
            
        except Exception as e:
            print(f"✗ Error creating user {name}: {e}")
            return False
    
    def list_users(self) -> List[Dict]:
        """
        List all users
        
        Returns:
            List of user dictionaries
        """
        try:
            user_emails = self.client.smembers("users:all")
            users = []
            
            for email in user_emails:
                user_key = f"user:{email}"
                user_data = self.client.hgetall(user_key)
                if user_data:
                    users.append(user_data)
            
            print(f"✓ Retrieved {len(users)} users")
            return users
            
        except Exception as e:
            print(f"✗ Error fetching users: {e}")
            return []
    
    def display_users(self, users: List[Dict]):
        """
        Display users in formatted output
        
        Args:
            users: List of user dictionaries
        """
        if not users:
            print("No users to display.")
            return
        
        print("\n" + "="*60)
        print("USER LISTING")
        print("="*60)
        print(f"{'Name':<20} {'Role':<15} {'Email':<25}")
        print("-"*60)
        
        for user in users:
            name = user.get('name', 'N/A')
            role = user.get('role', 'N/A')
            email = user.get('email', 'N/A')
            print(f"{name:<20} {role:<15} {email:<25}")
        
        print("="*60)
    
    def delete_database_namespace(self, namespace: str) -> bool:
        """
        Delete database namespace and all associated keys
        
        Args:
            namespace: Namespace to delete
            
        Returns:
            True if successful
        """
        try:
            # Find all keys with this namespace
            pattern = f"db:metadata:{namespace}"
            keys_to_delete = self.client.keys(pattern)
            
            if keys_to_delete:
                deleted_count = self.client.delete(*keys_to_delete)
                print(f"✓ Database namespace '{namespace}' deleted (removed {deleted_count} keys)")
                return True
            else:
                print(f"✓ No keys found for namespace '{namespace}'")
                return True
                
        except Exception as e:
            print(f"✗ Error deleting database namespace: {e}")
            return False
    
    def cleanup_demo_data(self):
        """
        Clean up all demo data created by this script
        """
        try:
            # Get all demo users
            user_emails = self.client.smembers("users:all")
            demo_emails = [
                "john.doe@example.com",
                "mike.smith@example.com", 
                "cary.johnson@example.com"
            ]
            
            # Delete demo users
            for email in demo_emails:
                if email in user_emails:
                    user_key = f"user:{email}"
                    self.client.delete(user_key)
                    self.client.srem("users:all", email)
                    print(f"✓ Cleaned up user: {email}")
            
            # Clean up users set if empty
            if self.client.scard("users:all") == 0:
                self.client.delete("users:all")
                print("✓ Cleaned up empty users set")
                
        except Exception as e:
            print(f"✗ Error during cleanup: {e}")

def main():
    """
    Main function to execute Redis operations
    """
    print("Redis Direct Connection Script")
    print("==============================")
    print("Connecting to redis-12000.localhost:12000")
    
    try:
        # Initialize Redis client
        client = RedisDirectClient(
            host='redis-12000.localhost',
            port=12000,
            password=None  # Set password if required
        )
        
        # Step 1: Create a database namespace
        print("\nStep 1: Creating Database Namespace")
        print("-" * 40)
        success = client.create_database_namespace("test-database-exercise2")
        
        if not success:
            print("Failed to create database namespace. Exiting...")
            return 1
        
        # Step 2: Create three users
        print("\nStep 2: Creating Users")
        print("-" * 30)
        
        users_to_create = [
            {"email": "john.doe@example.com", "name": "John Doe", "role": "db_viewer"},
            {"email": "mike.smith@example.com", "name": "Mike Smith", "role": "db_member"},
            {"email": "cary.johnson@example.com", "name": "Cary Johnson", "role": "admin"}
        ]
        
        for user_data in users_to_create:
            client.create_user_record(
                email=user_data["email"],
                name=user_data["name"],
                role=user_data["role"]
            )
        
        # Step 3: List and display users
        print("\nStep 3: Listing Users")
        print("-" * 30)
        
        all_users = client.list_users()
        client.display_users(all_users)
        
        # Step 4: Delete the database namespace
        print("\nStep 4: Deleting Database Namespace")
        print("-" * 40)
        
        client.delete_database_namespace("test-database-exercise2")
        
        # Step 5: Clean up demo data
        print("\nStep 5: Cleaning Up Demo Data")
        print("-" * 35)
        
        client.cleanup_demo_data()
        
        print("\nScript execution completed successfully!")
        return 0
        
    except redis.ConnectionError:
        print("\n✗ Could not connect to Redis.")
        print("Make sure Redis is running at redis-12000.localhost:12000")
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
