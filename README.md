# Ask Aby - AI-Powered Q&A Web App ✨
Ask Aby is a sleek, interactive web application that provides AI-generated answers to user questions. Built with HTML, CSS, and JavaScript, it connects to a backend API (like Ollama or a custom LLM) to deliver intelligent responses.

🔗 Live Demo: https://askaby.github.io/ask-aby/

Features 🚀
✅ Beautiful UI – Clean, responsive design with smooth animations.
✅ Real-time AI Responses – Fetches answers from a backend LLM (Mistral, LLaMA, etc.).
✅ Error Handling – Displays troubleshooting tips if the API fails.
✅ Typing Indicator – Shows a loading animation while waiting for responses.
✅ Dark/Light Mode – Automatically adapts to user preferences.

How It Works ⚙️
User Input – Type a question in the input field.

API Call – The frontend sends the question to a backend AI service.

AI Processing – The backend generates a response using an LLM.

Display Answer – The response appears in a formatted card with smooth transitions.

Tech Stack
Frontend	Backend (Optional)
HTML5	Python (FastAPI/Flask)
CSS3 (Poppins font, animations)	Ollama / LLaMA / Mistral
JavaScript (Fetch API)	Render / Vercel (Deployment)
How I Built It 🛠️
1. Frontend (Static Site)
Minimalist UI – Card-based layout with a purple accent theme.

Dynamic Responses – Fade-in effect for AI answers.

Mobile-Friendly – Fully responsive for all devices.

2. Backend (Optional for Full Functionality)
API Endpoint – A Python server (FastAPI) processes questions and returns AI responses.

LLM Integration – Connects to Ollama (local) or cloud-based models.
# Example FastAPI Backend (simplified)
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Question(BaseModel):
    pergunta: str

@app.post("/pergunta/")
async def ask_question(question: Question):
    # Call LLM (Ollama, GPT, etc.)
    resposta = get_ai_response(question.pergunta)
    return {"resposta": resposta, "fluxo": "General"}

    Future Improvements 🔮
🔹 Add user feedback (👍/👎 buttons to improve AI).
🔹 Support voice input (Web Speech API).
🔹 Save chat history (LocalStorage or Firebase).
🔹 Deploy backend (Render/Vercel for live API).

Contribute 🤝
Feel free to fork, improve, or suggest ideas! Open an issue or submit a PR.

📜 License: MIT
Abdias Saint-Louis
