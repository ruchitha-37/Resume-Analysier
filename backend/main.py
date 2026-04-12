from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil
import os
from rag_pipeline import process_resume, analyze_resume, analyze_against_job_description

app = FastAPI(title="Resume Analyzer API")

# Setup CORS so frontend can hit endpoints
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all origins for local dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory store for vector DB
# Note: In a production app, use Redis/Postgres. For simplicity, we use memory.
db_store = {}

# We mount the frontend dir at the root so it serves the index.html and static files.
# Mount correctly at the end of routing to avoid overriding endpoints, but wait, FastAPI 
# checks routes in order. Actually, let's just comment out the get("/") and we'll add mount at the end.

@app.post("/upload/")
async def upload_resume(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
        
    os.makedirs("temp", exist_ok=True)
    file_path = f"temp/{file.filename}"
    
    # Save the uploaded file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # Process and store in memory under "session_doc"
        db = process_resume(file_path)
        db_store["session_doc"] = db
        return {"message": "Resume uploaded and processed successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing resume: {str(e)}")

class QueryRequest(BaseModel):
    query: str

@app.post("/analyze/")
async def analyze(request: QueryRequest):
    db = db_store.get("session_doc")
    if not db:
        raise HTTPException(status_code=400, detail="Upload a resume first")

    try:
        result = analyze_resume(db, request.query)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

class JobDescriptionRequest(BaseModel):
    job_description: str

@app.post("/score/")
async def score(request: JobDescriptionRequest):
    db = db_store.get("session_doc")
    if not db:
        raise HTTPException(status_code=400, detail="Upload a resume first")
        
    try:
        analysis_text = analyze_against_job_description(db, request.job_description)
        
        # Simple parser to fetch Score, gaps, and improvements from text block
        # The prompt instructed: SCORE: X \n MISSING_SKILLS: ... \n IMPROVEMENTS: ...
        
        score_val = "N/A"
        gaps = ""
        improvements = ""
        
        parts = analysis_text.split("MISSING_SKILLS:")
        if len(parts) > 1:
            score_part = parts[0].replace("SCORE:", "").strip()
            score_val = score_part
            
            subparts = parts[1].split("IMPROVEMENTS:")
            gaps = subparts[0].strip()
            if len(subparts) > 1:
                improvements = subparts[1].strip()
        else:
             # Fallback if LLM format breaks
             improvements = analysis_text
             
        return {
            "score": score_val,
            "missing_skills": gaps,
            "improvements": improvements,
            "raw": analysis_text
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scoring failed: {str(e)}")

# Mount frontend at the root last so it acts as a fallback for index.html
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

