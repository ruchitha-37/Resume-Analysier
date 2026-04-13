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

---

## 📁 Complete Folder & File Documentation
Below is the top-to-bottom master map documenting every single folder and file used in the project.

### The Root Directory (`/`)
This is the main project box. It acts as the configuration hub for cloud deployments and sets up the whole application.
* **`.env`** : A hidden file storing secret passwords (specifically your `OPENROUTER_API_KEY`). Kept out of version control for security.
* **`.gitignore`** : Tells GitHub which files/folders it should ignore and NOT upload to the internet (like `.env` and `__pycache__`).
* **`Procfile`** : The launch command file for cloud deployment. Tells Render to boot up the server via `web: uvicorn backend.main:app`.
* **`requirements.txt`** : The master list of Python dependencies (LangChain, FastAPI, FAISS, PyPDF, etc.).
* **`README.md`** : This instruction manual and documentation page.

### 1. `frontend/` (The User Interface)
This folder holds everything the user physically sees on their screen.
* **`index.html`** : The primary structure of the web page. Defines the text boxes, buttons, typography hierarchy, and UI layout.
* **`style.css`** : The design system. Handles the sleek colors, modern glassmorphism aesthetic, hover states, and the dynamic score circle SVG animation.
* **`script.js`** : The active behavior script. Intercepts file uploads and text inputs, sends HTTP requests to the backend server dynamically (`/upload/`, `/analyze/`, `/score/`), and renders the server's responses back onto the DOM.

### 2. `backend/` (The Server & AI Logic)
This folder holds all the Python code that processes requests, talks to the LangChain AI, and manages data flow.
* **`main.py`** : The Traffic Controller (FastAPI Server). It provides the API endpoints. It successfully mounts the `frontend/` directory so the entire project (UI + Backend) is served effortlessly from one single script.
* **`rag_pipeline.py`** : The AI Brain. Uses Langchain. It translates uploaded PDFs, converts text chunks to math using HuggingFace embeddings, stores them in FAISS, and runs conversational prompts against OpenRouter to return resume grading and answers.
* **`temp/`** : A temporary staging folder. Uploaded PDFs sit here just long enough for `rag_pipeline.py`'s PyPDFLoader to read them.
* **`db/`** : The vector memory bank. FAISS embedding files would be persisted here to allow the AI to "remember" resume contents across sessions without re-reading the PDF.
* **`__pycache__/`** : An auto-generated hidden folder created by Python to store optimized compiled code so your server starts up faster.

### 3. `notebooks/` (The Prototyping Sandbox)
* **`rag_experiments.ipynb`** : A Jupyter Notebook used by the developer as a safe "scratchpad" to build, test, and debug initial LangChain prompts and FAISS commands before finalizing them into `rag_pipeline.py`.

---

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

3. **Start the Unified Server**
   Run the FastAPI server from the project root! Because `main.py` now serves your static HTML, you don't need a separate frontend server:
   ```bash
   uvicorn backend.main:app --reload
   ```

4. **Open the Application**
   Open your browser and navigate directly to:
   ```
   http://127.0.0.1:8000
   ```

## Cloud Deployment (Render)
Because of the unified server setup and the `Procfile`, this app is ready for 1-click cloud deployments.
1. Connect this GitHub Repository in Render.
2. Build Command: `pip install -r requirements.txt`. 
3. The server automatically launches utilizing the `Procfile` command!
