from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from models import (
    MessageGenerateRequest,
    MessageGenerateResponse,
    SaveMessageRequest,
    SaveMessageResponse,
    SavedMessage,
    SavedMessagesResponse
)
from message_service import MessageGenerationService

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Initialize message generation service
message_service = MessageGenerationService()

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@api_router.get("/")
async def root():
    return {"message": "MoodMate API is running"}

@api_router.post("/generate-message", response_model=MessageGenerateResponse)
async def generate_message(request: MessageGenerateRequest):
    """
    Generate an empathetic motivational message based on emotion and language.
    """
    try:
        logger.info(f"Generating message for emotion={request.emotion}, language={request.language}")
        
        # Generate message using AI
        generated_text = await message_service.generate_message(
            emotion=request.emotion,
            language=request.language
        )
        
        response = MessageGenerateResponse(
            message=generated_text,
            emotion=request.emotion,
            language=request.language
        )
        
        logger.info(f"Successfully generated message: {generated_text[:50]}...")
        return response
        
    except Exception as e:
        logger.error(f"Error in generate_message: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate message: {str(e)}")

@api_router.post("/save-message", response_model=SaveMessageResponse)
async def save_message(request: SaveMessageRequest):
    """
    Save a generated message to the database.
    """
    try:
        saved_msg = SavedMessage(
            emotion=request.emotion,
            language=request.language,
            text=request.message
        )
        
        # Save to MongoDB
        result = await db.saved_messages.insert_one(saved_msg.dict())
        
        logger.info(f"Saved message with id={saved_msg.id}")
        
        return SaveMessageResponse(
            id=saved_msg.id,
            message="Message saved successfully"
        )
        
    except Exception as e:
        logger.error(f"Error in save_message: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to save message: {str(e)}")

@api_router.get("/saved-messages", response_model=SavedMessagesResponse)
async def get_saved_messages():
    """
    Retrieve all saved messages (limited to last 50).
    """
    try:
        # Get last 50 messages, sorted by timestamp descending
        cursor = db.saved_messages.find().sort("timestamp", -1).limit(50)
        messages = await cursor.to_list(length=50)
        
        saved_messages = [SavedMessage(**msg) for msg in messages]
        
        logger.info(f"Retrieved {len(saved_messages)} saved messages")
        
        return SavedMessagesResponse(messages=saved_messages)
        
    except Exception as e:
        logger.error(f"Error in get_saved_messages: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve messages: {str(e)}")

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()