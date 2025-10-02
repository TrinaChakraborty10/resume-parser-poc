from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from modern_resume_parser import ModernResumeParser
import tempfile
import os
from pathlib import Path
from typing import Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Resume Parser API",
    description="A modern resume parser API that extracts key information from PDF resumes",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuration
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_CONTENT_TYPES = ["application/pdf"]

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Resume Parser API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "upload_resume": "/upload-resume",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "resume-parser"}

@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Upload a PDF resume and extract key information
    
    Args:
        file: PDF file to be parsed
        
    Returns:
        JSON response with extracted resume information
        
    Raises:
        HTTPException: If file is invalid or processing fails
    """
    
    # Validate file type
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Only PDF files are allowed. Got: {file.content_type}"
        )
    
    # Check file size
    file_content = await file.read()
    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File size too large. Maximum allowed size is {MAX_FILE_SIZE // (1024*1024)}MB"
        )
    
    # Reset file pointer
    await file.seek(0)
    
    # Create temporary file to store the uploaded PDF
    temp_file = None
    try:
        # Create temporary file with PDF extension
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            temp_file.write(file_content)
            temp_file_path = temp_file.name
        
        logger.info(f"Processing uploaded file: {file.filename}")
        
        # Parse the resume using our ModernResumeParser
        parser = ModernResumeParser(temp_file_path)
        extracted_data = parser.get_extracted_data()
        
        # Add metadata about the file
        result = {
            "success": True,
            "filename": file.filename,
            "file_size_bytes": len(file_content),
            "extracted_data": extracted_data,
            "metadata": {
                "parser_version": "2.0",
                "processing_status": "completed"
            }
        }
        
        logger.info(f"Successfully processed file: {file.filename}")
        return JSONResponse(content=result)
        
    except Exception as e:
        logger.error(f"Error processing file {file.filename}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing resume: {str(e)}"
        )
    
    finally:
        # Clean up temporary file
        if temp_file and os.path.exists(temp_file_path):
            try:
                os.unlink(temp_file_path)
                logger.info(f"Cleaned up temporary file: {temp_file_path}")
            except Exception as e:
                logger.warning(f"Could not delete temporary file: {e}")

@app.post("/parse-resume")
async def parse_resume_detailed(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Alternative endpoint with more detailed response format
    
    Args:
        file: PDF file to be parsed
        
    Returns:
        Detailed JSON response with categorized information
    """
    
    # Validate file
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Only PDF files are allowed. Got: {file.content_type}"
        )
    
    file_content = await file.read()
    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File size too large. Maximum allowed size is {MAX_FILE_SIZE // (1024*1024)}MB"
        )
    
    await file.seek(0)
    
    temp_file = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            temp_file.write(file_content)
            temp_file_path = temp_file.name
        
        parser = ModernResumeParser(temp_file_path)
        raw_data = parser.get_extracted_data()
        
        # Organize data into categories
        result = {
            "success": True,
            "file_info": {
                "filename": file.filename,
                "size_bytes": len(file_content),
                "pages": raw_data.get("no_of_pages")
            },
            "personal_info": {
                "name": raw_data.get("name"),
                "email": raw_data.get("email"),
                "phone": raw_data.get("mobile_number")
            },
            "education": {
                "institution": raw_data.get("college_name"),
                "degree": raw_data.get("degree")
            },
            "professional": {
                "current_designation": raw_data.get("designation"),
                "companies": raw_data.get("company_names", []),
                "total_experience": raw_data.get("total_experience"),
                "skills": raw_data.get("skills", [])
            },
            "raw_extracted_data": raw_data
        }
        
        return JSONResponse(content=result)
        
    except Exception as e:
        logger.error(f"Error processing file {file.filename}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing resume: {str(e)}"
        )
    
    finally:
        if temp_file and os.path.exists(temp_file_path):
            try:
                os.unlink(temp_file_path)
            except Exception as e:
                logger.warning(f"Could not delete temporary file: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)