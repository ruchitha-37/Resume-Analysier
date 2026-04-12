# Aura - Intelligent Resume Analyzer (RAG)

Welcome to **Aura**, an intelligent, premium-designed Resume Analyzer built using a RAG (Retrieval-Augmented Generation) Architecture.

## Features
- **General Q&A**: Ask any question about your resume (e.g., "What is my educational background?", "List my main Python skills").
- **Job Matching Analysis**: Paste a Job Description to get an Alignment Score (0-100), identify Missing Skills, and receive Actionable Improvement Tips.

## Tech Stack
- **Frontend**: Vanilla HTML/CSS/JS with a dark-mode glassmorphism UI.
- **Backend**: FastAPI (Python).
- **RAG Pipeline**: Langchain, FAISS (Vector DB).
- **Embeddings**: HuggingFace (`all-MiniLM-L6-v2`).
- **LLM**: OpenRouter API (`openai/gpt-3.5-turbo` by default).

## Installation & Setup

1. **Install Dependencies**
   Make sure you are in the project root directory (`resume-rag-project/`) and run:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment Variables**
   Open the `.env` file in the project root and add your OpenRouter API Key:
   ```
   OPENROUTER_API_KEY=your_actual_key_here
   ```

3. **Start the Backend Server**
   Navigate to the `backend/` directory and run the FastAPI server:
   ```bash
   cd backend
   uvicorn main:app --reload
   ```
   The backend will run on `http://127.0.0.1:8000`.

4. **Open the Frontend**
   Simply open `frontend/index.html` in your favorite web browser. You do not need a frontend server, but you can use an extension like Live Server if you prefer!

## Usage
1. Click **Select PDF Resume** and choose a valid PDF file.
2. Click **Initialize Resume** to embed your document into the Vector Database.
3. Use the tabs to either ask general QA questions or perform Job Matching.
