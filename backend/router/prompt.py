import os
import sys
# Append the project directory to the sys.path
sys.path.append(os.path.abspath("/home/work/woojun/Capston/20242R0136COSE48002"))
from typing import Dict, List, Optional
from fastapi import APIRouter, File, UploadFile, Form, FastAPI
from pydantic import BaseModel
from ml.llm.rag.conversation import make_candidates, retrieve_context, generate_question

# Single global session variable
session = {"conversation": [], "context": None}

# Input Models
class Prompt(BaseModel):
    symptoms: str = ""

class UserResponseData(BaseModel):
    session_id: str
    selected_element: str  # "O" or "X"

# Initialize the router
router = APIRouter()

@router.post("/prompt")
async def process(
    symptoms: str = Form(...),
    image: UploadFile = File(None)
):
    # Get session
    global session

    # Initial conversation
    if len(session["conversation"]) < 1:
        session["conversation"].append(symptoms)
        candidates = make_candidates(symptoms, image)
        session["context"] = retrieve_context(candidates)

    # Generate the next question based on the current context
    response = generate_question(session["context"])
    session["conversation"].append(response)

    return {"response": response, "context": session["context"]}

################
# For testing ml
@router.post("/test")
async def testing(
    symptoms: str = Form(...),
    image: UploadFile = File(None)
):
    response = make_candidates(symptoms, image)

    return {"response": response}
################

@router.post("/click")
async def handle_user_response(data: UserResponseData):
    # Get session
    global session

    # Check if context exists
    if not session["context"]:
        return {"error": "Context is not initialized. Please start with /prompt."}

    # Eliminate a disease based on the user response
    context = session["context"]
    diseases = list(context.keys())

    if len(diseases) <= 1:
        diagnosis = diagnose(session["context"])
        return {"response": diagnosis}

    session["context"] = eliminate_disease(session["context"], session["conversation"], data.selected_element)

    # Check if only one disease remains
    if len(session["context"]) == 1:
        final_disease = list(session["context"].keys())[0]
        diagnosis = diagnose(session["context"])
        return {"response": diagnosis}

    # Return the updated context
    return {
        "response": "Disease eliminated. Generating next question...",
        "updated_context": session["context"]
    }

# Initialize FastAPI app and include router
app = FastAPI()
app.include_router(router)