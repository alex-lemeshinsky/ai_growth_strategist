import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from src.api.routes import router
from src.api.policy_routes import router as policy_router
from src.db import MongoDB

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Facebook Ads Library Parser API",
    description="API for parsing Facebook Ads Library using Apify",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router, prefix="/api/v1", tags=["ads"])
app.include_router(policy_router, prefix="/api/v1/policy", tags=["policy"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Facebook Ads Library Parser API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.on_event("startup")
async def startup_event():
    """Startup event handler."""
    logger.info("Starting Facebook Ads Library Parser API")

    # Initialize MongoDB connection
    try:
        await MongoDB.connect()
        logger.info("✅ MongoDB connected successfully")
    except Exception as e:
        logger.error(f"❌ Failed to connect to MongoDB: {e}")
        raise

    # Check for required environment variables
    if not os.environ.get('APIFY_API_KEY'):
        logger.warning("APIFY_API_KEY not set in environment variables")


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event handler."""
    logger.info("Shutting down Facebook Ads Library Parser API")
    
    # Close MongoDB connection
    try:
        await MongoDB.disconnect()
        logger.info("✅ MongoDB disconnected successfully")
    except Exception as e:
        logger.error(f"❌ Error disconnecting MongoDB: {e}")


if __name__ == "__main__":
    import uvicorn

    host = os.environ.get("API_HOST", "0.0.0.0")
    port = int(os.environ.get("API_PORT", 8000))

    logger.info(f"Starting server on {host}:{port}")
    uvicorn.run(app, host=host, port=port)
