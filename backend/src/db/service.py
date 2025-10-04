"""
MongoDB service for async database operations.
"""
import os
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo import ASCENDING, DESCENDING
import logging

logger = logging.getLogger(__name__)


class MongoDB:
    client: Optional[AsyncIOMotorClient] = None
    db: Optional[AsyncIOMotorDatabase] = None
    
    @classmethod
    async def connect(cls):
        """Connect to MongoDB."""
        mongo_url = os.environ.get("MONGODB_URL", "mongodb://localhost:27017")
        db_name = os.environ.get("MONGODB_DB", "ai_growth_strategist")
        
        cls.client = AsyncIOMotorClient(mongo_url)
        cls.db = cls.client[db_name]
        
        # Create indexes for tasks
        await cls.db.tasks.create_index([("task_id", ASCENDING)], unique=True)
        await cls.db.tasks.create_index([("created_at", DESCENDING)])
        await cls.db.tasks.create_index([("status", ASCENDING)])
        
        # Create indexes for policy_tasks
        await cls.db.policy_tasks.create_index([("task_id", ASCENDING)], unique=True)
        await cls.db.policy_tasks.create_index([("created_at", DESCENDING)])
        await cls.db.policy_tasks.create_index([("status", ASCENDING)])
        await cls.db.policy_tasks.create_index([("platform", ASCENDING)])
        
        logger.info(f"✅ Connected to MongoDB: {db_name}")
    
    @classmethod
    async def close(cls):
        """Close MongoDB connection."""
        if cls.client:
            cls.client.close()
            logger.info("🔌 Disconnected from MongoDB")
    
    @classmethod
    def get_db(cls) -> AsyncIOMotorDatabase:
        """Get database instance."""
        if cls.db is None:
            raise RuntimeError("Database not initialized. Call MongoDB.connect() first.")
        return cls.db
