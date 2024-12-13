import os
import sys
from typing import Dict, List, Optional
from fastapi import APIRouter, File, UploadFile, Form, FastAPI
from pydantic import BaseModel
from ml.rag.conversation import (
    make_candidates, 
    retrieve_context, 
    generate_question, 
    reason_diagnosis, 
    diagnose, 
    eliminate_disease,
    faq
)

# Single global session variable
session = {"conversation": [], "context": None}

# Input Models
class Prompt(BaseModel):
    symptoms: str = ""

class UserResponseData(BaseModel):
    selected_element: str  # "O" or "X"

# Initialize the router
router = APIRouter()


@router.post("/initial")
async def process(
    symptoms: str = Form(...),
    image: UploadFile = File(None)
):
    # Get session
    global session
    
    session["conversation"] = []
    session["conversation"].append(symptoms)

    candidates = make_candidates(symptoms, image)
    session["context"] = retrieve_context(candidates)

    # Generate the first question based on the retrieved context
    first_question = generate_question(session["context"], session["conversation"])
    session["conversation"].append(first_question)
    print(session)

    return {"response": first_question, "context": session["context"]}


@router.post("/click")
async def handle_user_response(data: UserResponseData):
    # Get session
    global session

    # Check if context exists
    if not session["context"]:
        return {"error": "Context is not initialized. Please start with /initial."}

    # Eliminate a disease based on the user response
    user_response = f"{data.selected_element}"
    session["conversation"].append(user_response)

    eliminated_disease_eng = eliminate_disease(session["context"], session["conversation"])
    
    eliminated_disease = None
    for key in session["context"].keys():
        if key.endswith(f"({eliminated_disease_eng})"):
            eliminated_disease = key
            print(eliminated_disease)
            break
    
    print("Current context:", session["context"])
    print("Key to delete:", eliminated_disease_eng)
    # print(session["context"])
    if eliminated_disease in session["context"]:
        del session["context"][eliminated_disease]

    # If only one disease remains, finalize the diagnosis
    diseases = list(session["context"].keys())
    if len(diseases) <= 1:
        reason = reason_diagnosis(session["context"], session["conversation"])
        reason_len = len(reason.split("\n"))
        diagnosis = diagnose(session["context"])
        session["conversation"].append(diagnosis)
        print(session)
        return {
            "response": f"{diseases[0]}\n{reason_len}\n {reason} \n{diagnosis}",
            "updated_context": session["context"],
            "diagnosis_finalized": True,
        }

    # Generate new question
    else:
        new_question = generate_question(session["context"], session["conversation"])
        session["conversation"].append(new_question)
        print(session)
        return {
            "response": new_question,
            "updated_context": session["context"],
            "diagnosis_finalized": False,
        }

    # Return the updated context
    return {
        "response": "Error",
        "updated_context": session["context"],
        "diagnosis_finalized": False,
    }

@router.post("/faq")
async def handle_faq(
    symptoms: str = Form(...),
    image: Optional[UploadFile] = File(None)
):
    # Get session
    global session
    session["conversation"].append(symptoms)

    faq_response = faq(symptoms, session["context"], session["conversation"], image)
    session["conversation"].append(faq_response)

    return {
        "response": faq_response,
        "updated_context": session["context"],
        "conversation": session["conversation"],
    }


# Initialize FastAPI app and include router
app = FastAPI()
app.include_router(router)