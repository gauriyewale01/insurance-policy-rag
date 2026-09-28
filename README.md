# Insurance Policy RAG Chatbot

An AI-powered **Retrieval-Augmented Generation (RAG) chatbot** that allows users to upload insurance policy documents and ask questions about eligibility, coverage, exclusions, waiting periods, benefits, and other policy-specific information.

The system retrieves relevant information directly from the uploaded documents and uses an LLM to generate grounded responses. It is designed to minimize hallucinations by instructing the model to answer only from the retrieved policy context.

---

## Key Features

- 📄 Upload insurance policy PDFs
- 🔍 Automatically extract and process document content
- ✂️ Split documents into searchable chunks
- 🧠 Generate semantic embeddings using Sentence Transformers
- 🗄️ Store and search document embeddings using ChromaDB
- 🤖 Generate answers using Google Gemini
- 📌 Retrieve relevant policy context before answering
- 🛡️ Reduce hallucinations using document-grounded prompting
- 🌐 FastAPI backend with Swagger API documentation
- 💻 Simple frontend for document upload and policy queries
- 📚 Return source information such as document name and page number

---

## System Architecture

```text
                    ┌─────────────────────┐
                    │   Insurance PDF     │
                    │      Document       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    PDF Parsing      │
                    │     (pypdf)         │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Text Chunking     │
                    │  800 chars / 100    │
                    │      overlap        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Embeddings       │
                    │ all-MiniLM-L6-v2   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     ChromaDB        │
                    │ Vector Database     │
                    └──────────┬──────────┘
                               │
                    User Question
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Question Embedding  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Semantic Retrieval  │
                    │ Relevant Chunks     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Google Gemini     │
                    │ Context-grounded    │
                    │     Response        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   User Answer +     │
                    │   Source Metadata   │
                    └─────────────────────┘

*** Installation & Setup ***
1. Clone the repository
git clone https://github.com/gauriyewale01/insurance-policy-rag.git
cd insurance-policy-rag

2. Create a virtual environment
Windows-
python -m venv .venv
Activate it:
.venv\Scripts\activate
macOS / Linux-
python3 -m venv .venv
source .venv/bin/activate

3. Install dependencies
pip install -r requirements.txt

4. Configure the Gemini API key
Create a .env file in the project root:
GEMINI_API_KEY=your_gemini_api_key_here
The .env file is intentionally excluded from Git.

*** Running the Application ***
Start the FastAPI server:
uvicorn app.main:app --reload

The API will be available at:
http://127.0.0.1:8000

Swagger API documentation:
http://127.0.0.1:8000/docs

*** How to Test the RAG System ***
Step 1 — Upload a policy document
Open Swagger:
http://127.0.0.1:8000/docs

Find:
POST /upload
Click Try it out, select an insurance policy PDF, and execute the request.
A successful upload returns information similar to:
{
  "message": "Document added successfully",
  "chunks_added": 20
}

The document is:
Saved locally
Parsed page-by-page
Split into chunks
Converted into embeddings
Stored in ChromaDB
Step 2 — Ask a policy question

Use:
POST /chat
Request body:
{
  "message": "What is the maximum entry age for a child?"
}

The system:
Question
   ↓
Question Embedding
   ↓
ChromaDB Semantic Search
   ↓
Relevant Policy Chunks
   ↓
Gemini
   ↓
Grounded Answer

Example response:
{
  "user_message": "What is the maximum entry age for a child?",
  "retrieved_context": "...",
  "ai_response": "The maximum entry age for a child is 25 years.",
  "source": {
    "page": 1,
    "source": "Sample Insurance Policy Information Document.pdf"
  }
}

*** Example Questions ***
Eligibility
What is the maximum entry age for a child?
Who is eligible to be covered under this policy?
Can dependent parents be covered?

Coverage
What family members can be covered?
How many members can be included in the family floater?

Policy Conditions
What are the renewal conditions?
What nationality requirement is mentioned in the policy?

Grounding / Hallucination Test
Ask something that is not mentioned in the uploaded document, for example:
What is the premium amount?

If the information is unavailable, the chatbot is designed to respond:
I couldn't find that information in the uploaded policy documents.

