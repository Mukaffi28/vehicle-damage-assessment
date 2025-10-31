from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv

from models.damage_response import DamageResponse
from services.gemini_service import GeminiService

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Vehicle Damage Assessment API",
    description="API for detecting and assessing vehicle damage using AI",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Gemini service
try:
    gemini_service = GeminiService()
except ValueError as e:
    print(f"Warning: {str(e)}")
    gemini_service = None


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Vehicle Damage Assessment API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "assess_damage": "/api/assess-damage (POST)"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "gemini_configured": gemini_service is not None
    }


@app.post("/api/assess-damage", response_model=DamageResponse)
async def assess_damage(file: UploadFile = File(...)):
    """
    Assess vehicle damage from an uploaded image
    
    Args:
        file: Image file (JPEG, PNG, etc.)
        
    Returns:
        DamageResponse containing damage assessment details
    """
    # Validate Gemini service is initialized
    if gemini_service is None:
        raise HTTPException(
            status_code=500,
            detail="Gemini API is not configured. Please set GEMINI_API_KEY environment variable."
        )
    
    # Validate file type
    allowed_types = ["image/jpeg", "image/jpg", "image/png", "image/webp", "image/heic", "image/heif"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed types: {', '.join(allowed_types)}"
        )
    
    # Validate file size (max 10MB)
    max_size = 10 * 1024 * 1024  # 10MB
    contents = await file.read()
    if len(contents) > max_size:
        raise HTTPException(
            status_code=400,
            detail="File size exceeds 10MB limit"
        )
    
    try:
        # Assess damage using Gemini
        result = await gemini_service.assess_damage(contents)
        
        # Validate and return response
        return DamageResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error parsing AI response: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing image: {str(e)}"
        )


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc)
        }
    )


if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True
    )
