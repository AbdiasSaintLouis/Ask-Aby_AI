from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import logging
import ssl

# ========== SSL FIX FOR NLTK ==========
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
# ======================================

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Download NLTK data with error handling
try:
    nltk.download('punkt_tab')
    nltk.download('punkt')
    nltk.download('stopwords')
    logger.info("NLTK data downloaded successfully")
except Exception as e:
    logger.error(f"Error downloading NLTK data: {str(e)}")
    # Continue without NLTK data (basic functionality will still work)

# Workflow definitions
WORKFLOWS = {
    "password": ["senha", "password", "reset"],
    "account": ["conta", "account", "cadastro"]
}

OLLAMA_URL = "http://localhost:11434/api/generate"

class Question(BaseModel):
    pergunta: str

def get_llama_response(prompt: str) -> str:
    """Get response from LLaMA model"""
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": "tinyllama",
                "prompt": prompt,
                "stream": False
            },
            timeout=30
        )
        response.raise_for_status()
        return response.json().get("response", "No response from LLaMA")
    except requests.exceptions.Timeout:
        logger.error("LLaMA API timeout")
        raise HTTPException(
            status_code=504,
            detail="LLaMA service timeout. Please try again later."
        )
    except requests.exceptions.ConnectionError:
        logger.error("LLaMA connection failed")
        raise HTTPException(
            status_code=503,
            detail="LLaMA service unavailable. Make sure Ollama is running."
        )
    except Exception as e:
        logger.error(f"LLaMA API error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error communicating with LLaMA: {str(e)}"
        )

@app.post("/pergunta/")
async def ask_question(question: Question):
    """Process question and return response"""
    try:
        # Get LLaMA response first
        answer = get_llama_response(question.pergunta)
        
        # Then analyze for workflow if NLTK data is available
        workflow = "General"
        try:
            tokens = word_tokenize(question.pergunta.lower())
            stop_words = set(stopwords.words("portuguese"))
            keywords = [t for t in tokens if t.isalnum() and t not in stop_words]
            
            for wf, triggers in WORKFLOWS.items():
                if any(trigger in keywords for trigger in triggers):
                    workflow = wf.capitalize()
                    break
        except Exception as e:
            logger.warning(f"NLTK processing failed, using default workflow: {str(e)}")
        
        return {
            "fluxo": workflow,
            "resposta": answer
        }
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Unexpected error processing question: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while processing your question"
        )