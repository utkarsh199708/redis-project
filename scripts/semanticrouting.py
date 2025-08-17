#!/usr/bin/env python3
"""
Semantic Router Application using RedisVL
Routes queries to the best matching topic: GenAI Programming, Science Fiction, or Classical Music
"""
import redis
import os
import sys
from typing import List, Optional

try:
    from redisvl.extensions.router import Route, SemanticRouter
    from redisvl.utils.vectorize import HFTextVectorizer
    from redisvl.extensions.router.schema import DistanceAggregationMethod, RoutingConfig
except ImportError:
    print("❌ Error: RedisVL not installed. Please install with: pip install redisvl")
    sys.exit(1)

# Disable tokenizers parallelism warning
os.environ["TOKENIZERS_PARALLELISM"] = "false"

class SemanticRoutingApp:
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        """
        Initialize the Semantic Router Application
        
        Args:
            redis_url: Redis connection URL
        """
        self.redis_url = redis_url
        self.router = None
        self._define_routes()
        self._initialize_router()
    
    def _define_routes(self):
        """Define the three routes with references and settings"""
        
        # Route 1: GenAI Programming Topics
        self.genai_programming = Route(
            name="genai_programming",
            references=[
                "how to build a chatbot using GPT",
                "implementing RAG with vector databases",
                "fine-tuning large language models",
                "prompt engineering best practices",
                "building AI agents with LangChain",
                "vector embeddings for search",
                "transformer architecture explained",
                "creating custom AI models",
                "machine learning model deployment",
                "neural network programming",
                "deep learning frameworks",
                "AI model optimization techniques",
                "generative AI applications",
                "LLM integration patterns",
                "semantic search implementation"
            ],
            metadata={
                "category": "technology", 
                "domain": "artificial_intelligence",
                "priority": 1
            },
            distance_threshold=0.70
        )
        
        # Route 2: Science Fiction Entertainment
        self.scifi_entertainment = Route(
            name="science_fiction",
            references=[
                "best sci-fi movies of all time",
                "classic science fiction novels",
                "space opera recommendations",
                "cyberpunk literature and films",
                "time travel stories and paradoxes",
                "alien invasion movies",
                "dystopian future narratives",
                "Star Wars vs Star Trek debate",
                "Isaac Asimov robot stories",
                "Philip K. Dick adaptations",
                "blade runner and its themes",
                "interstellar travel concepts",
                "artificial intelligence in movies",
                "virtual reality fiction",
                "post-apocalyptic scenarios",
                "quantum physics in sci-fi",
                "space exploration adventures"
            ],
            metadata={
                "category": "entertainment", 
                "genre": "science_fiction",
                "priority": 2
            },
            distance_threshold=0.68
        )
        
        # Route 3: Classical Music
        self.classical_music = Route(
            name="classical_music",
            references=[
                "Mozart symphonies and sonatas",
                "Bach fugues and cantatas",
                "Beethoven piano concertos",
                "Chopin nocturnes and etudes",
                "Vivaldi Four Seasons",
                "classical music composition techniques",
                "orchestra instrumentation guide",
                "baroque period composers",
                "romantic era classical music",
                "opera performances and arias",
                "chamber music ensembles",
                "classical music theory fundamentals",
                "famous conductors and performances",
                "classical music history timeline",
                "piano virtuoso performances",
                "string quartet repertoire",
                "classical music for beginners"
            ],
            metadata={
                "category": "arts", 
                "genre": "classical_music",
                "priority": 3
            },
            distance_threshold=0.65
        )
        
        self.routes = [self.genai_programming, self.scifi_entertainment, self.classical_music]
    
    def _initialize_router(self):
        """Initialize the SemanticRouter with defined routes"""
        try:
            print("🤖 Initializing Semantic Router...")
            print(f"📡 Connecting to Redis at: {self.redis_url}")
            
            # Initialize the SemanticRouter
            self.router = SemanticRouter(
                name="topic-classifier-router",
                vectorizer=HFTextVectorizer(model="sentence-transformers/all-mpnet-base-v2"),
                routes=self.routes,
                redis_url=self.redis_url,
                overwrite=True  # Recreate index if exists
            )
            
            # Configure routing settings
            self.router.update_routing_config(
                RoutingConfig(
                    aggregation_method=DistanceAggregationMethod.min,
                    max_k=3
                )
            )
            
            print(f"✅ Semantic Router initialized successfully!")
            print(f"📊 Total reference documents indexed: {self.router._index.info()['num_docs']}")
            
        except Exception as e:
            print(f"❌ Failed to initialize router: {e}")
            sys.exit(1)
    
    def route_query(self, query: str, return_multiple: bool = False) -> dict:
        """
        Route a query to the best matching topic
        
        Args:
            query: User query to route
            return_multiple: Whether to return multiple route matches
            
        Returns:
            Dictionary with routing results
        """
        try:
            print(f"\n🔍 Processing query: '{query}'")
            
            if return_multiple:
                # Get multiple route matches
                route_matches = self.router.route_many(query, max_k=3)
                
                if route_matches:
                    results = {
                        "query": query,
                        "matches": [
                            {
                                "route_name": match.name,
                                "distance": round(match.distance, 4),
                                "confidence": round((1 - match.distance) * 100, 2)
                            }
                            for match in route_matches
                        ]
                    }
                    
                    print(f"📍 Found {len(route_matches)} matching routes:")
                    for i, match in enumerate(route_matches, 1):
                        confidence = round((1 - match.distance) * 100, 2)
                        print(f"   {i}. {match.name} (confidence: {confidence}%)")
                    
                    return results
                else:
                    print("❌ No matching routes found")
                    return {"query": query, "matches": []}
            
            else:
                # Get single best route match
                route_match = self.router(query)
                
                if route_match.name:
                    confidence = round((1 - route_match.distance) * 100, 2)
                    result = {
                        "query": query,
                        "best_route": route_match.name,
                        "distance": round(route_match.distance, 4),
                        "confidence": confidence
                    }
                    
                    print(f"🎯 Best Route: {route_match.name}")
                    print(f"📈 Confidence: {confidence}%")
                    
                    return result
                else:
                    print("❌ No matching route found (query too dissimilar)")
                    return {"query": query, "best_route": None}
                    
        except Exception as e:
            print(f"❌ Error processing query: {e}")
            return {"query": query, "error": str(e)}
    
    def get_route_info(self):
        """Display information about all configured routes"""
        print("\n📋 Configured Routes:")
        print("=" * 60)
        
        for route in self.routes:
            print(f"\n🏷️  Route: {route.name}")
            print(f"   📊 References: {len(route.references)}")
            print(f"   🎯 Distance Threshold: {route.distance_threshold}")
            print(f"   📁 Category: {route.metadata.get('category', 'N/A')}")
            print(f"   🔢 Priority: {route.metadata.get('priority', 'N/A')}")
    
    def interactive_demo(self):
        """Run interactive demo session"""
        print("\n🎮 Interactive Semantic Router Demo")
        print("=" * 50)
        print("Enter queries to see which route they match to.")
        print("Type 'quit', 'exit', or 'q' to stop.")
        print("Type 'info' to see route information.")
        print("Type 'multi <query>' to see all matching routes.")
        print("-" * 50)
        
        while True:
            try:
                user_input = input("\n💬 Enter your query: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                if user_input.lower() == 'info':
                    self.get_route_info()
                    continue
                
                if user_input.lower().startswith('multi '):
                    query = user_input[6:].strip()
                    if query:
                        self.route_query(query, return_multiple=True)
                    else:
                        print("❌ Please provide a query after 'multi'")
                    continue
                
                if user_input:
                    self.route_query(user_input)
                else:
                    print("❌ Please enter a valid query")
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

def run_predefined_tests(app: SemanticRoutingApp):
    """Run predefined test queries"""
    print("\n🧪 Running Predefined Tests")
    print("=" * 40)
    
    test_queries = [
        # GenAI Programming queries
        "How do I implement RAG with vector databases?",
        "What are the best practices for prompt engineering?",
        "How to fine-tune a large language model?",
        
        # Science Fiction queries
        "What are the best cyberpunk movies?",
        "Recommend some good space opera novels",
        "Tell me about time travel paradoxes",
        
        # Classical Music queries
        "What are Mozart's most famous symphonies?",
        "Explain baroque music composition techniques",
        "Who are the greatest classical composers?",
        
        # Ambiguous queries
        "Tell me about artificial intelligence",
        "What's new in entertainment?",
        "I love music recommendations"
    ]
    
    for query in test_queries:
        app.route_query(query)
        print("-" * 40)

def main():
    """Main application entry point"""
    print("🚀 RedisVL Semantic Router Application")
    print("=" * 50)
    
    # Configuration - Updated to use port 6379
    redis_url = "redis://localhost:6379"
    
    try:
        # Initialize the application
        app = SemanticRoutingApp(redis_url=redis_url)
        
        # Show route information
        app.get_route_info()
        
        # Run predefined tests
        run_predefined_tests(app)
        
        # Start interactive demo
        app.interactive_demo()
        
    except KeyboardInterrupt:
        print("\n👋 Application terminated by user")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()