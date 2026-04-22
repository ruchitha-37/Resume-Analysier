import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

# Load env variables (for OPENROUTER_API_KEY)
load_dotenv()

# Use HuggingFace Inference API for embeddings — no local model, zero RAM cost
def get_embeddings():
    hf_token = os.getenv("HF_TOKEN", "")  # Optional: speeds up rate limits
    return HuggingFaceInferenceAPIEmbeddings(
        api_key=hf_token if hf_token else "hf_dummy",
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

def get_llm():
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key or api_key == "your_openrouter_api_key_here":
        raise ValueError("OPENROUTER_API_KEY is not set correctly in .env")
        
    return ChatOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
        model="google/gemma-3-4b-it:free",  # Free model on OpenRouter
        temperature=0.3
    )

def process_resume(file_path):
    """Parses PDF, splits text, creates and returns vector DB."""
    loader = PyPDFLoader(file_path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)

    db = FAISS.from_documents(chunks, get_embeddings())
    return db

def analyze_resume(db, query):
    """Standard QA against the resume."""
    retriever = db.as_retriever()
    relevant_docs = retriever.invoke(query)
    
    docs_text = "\n\n".join([doc.page_content for doc in relevant_docs])

    llm = get_llm()
    messages = [
        HumanMessage(content=f"System Instruction: You are a helpful AI assistant analyzing a resume.\n\nResume Context:\n{docs_text}\n\nQuestion: {query}")
    ]
    
    response = llm.invoke(messages)
    return response.content

def analyze_against_job_description(db, job_description):
    """
    Returns a score (0-100), skill gap analysis, and improvement tips 
    based on comparing the resume against a job description.
    """
    # Simply returning top chunks might not cover the whole resume for a holistic match,
    # but for this RAG scope, we can pull the top 10 chunks to get most of the resume.
    retriever = db.as_retriever(search_kwargs={"k": 10})
    
    # We query using the job description to find the most relevant parts of the resume
    relevant_docs = retriever.invoke(job_description)
    docs_text = "\n\n".join([doc.page_content for doc in relevant_docs])
    
    prompt = f"""
    You are an expert technical recruiter and ATS (Applicant Tracking System).
    Please analyze the following resume context against the provided job description.
    
    Job Description:
    {job_description}
    
    Resume Context:
    {docs_text}
    
    Provide your analysis strictly in the following format:
    
    SCORE: [Your score from 0-100]
    
    MISSING_SKILLS: 
    - [Skill 1]
    - [Skill 2]
    
    IMPROVEMENTS:
    - [Actionable tip 1]
    - [Actionable tip 2]
    
    Avoid any other commentary.
    """
    
    llm = get_llm()
    messages = [
        HumanMessage(content=f"System Instruction: You are an expert ATS and recruiter.\n\n{prompt}")
    ]
    
    response = llm.invoke(messages)
    return response.content