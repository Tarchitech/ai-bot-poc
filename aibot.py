# rag_bot.py
#
# A simple, runnable script to demonstrate a Retrieval-Augmented Generation (RAG)
# bot that answers questions based on a private document.
#
# Setup Instructions:
# 1. Make sure you have Python 3.8+ installed.
# 2. Install the required libraries:
#    pip install langchain langchain_community langchain-google-genai faiss-cpu pypdf
#
# 3. Get a Google AI API Key:
#    - Go to https://aistudio.google.com/app/apikey
#    - Create a new API key.
#    - It's best practice to set this as an environment variable.
#      - For Linux/macOS: export GOOGLE_API_KEY="YOUR_API_KEY"
#      - For Windows: set GOOGLE_API_KEY="YOUR_API_KEY"
#      - Alternatively, you can paste it directly into the script for quick testing.
#
# 4. Add your document:
#    - Place a PDF file in the same directory as this script.
#    - Update the `DOCUMENT_PATH` variable below to match your file's name.

import os
from getpass import getpass
import time

# --- Core LangChain components ---
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings, GoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains.base import Chain

# --- Configuration ---
DOCUMENT_PATH = "docs/1.pdf" # IMPORTANT: Change this to your PDF file name

# --- API Key Setup ---
# Tries to get the API key from environment variables. If not found, prompts the user.
if "GOOGLE_API_KEY" not in os.environ:
    print("Google API Key not found in environment variables.")
    os.environ["GOOGLE_API_KEY"] = getpass("Please enter your Google AI API Key: ")

def create_rag_chain(document_path: str) -> Chain:
    """
    Creates the entire RAG chain from a document path.
    This function handles loading, splitting, embedding, and chaining.
    """
    print(f"1. Loading document from: {document_path}")
    # Load the document. PyPDFLoader splits the PDF into pages.
    loader = PyPDFLoader(document_path)
    documents = loader.load()

    if not documents:
        raise ValueError(f"Could not load any documents from {document_path}. Check the file path and content.")

    print("2. Splitting the document into smaller chunks.")
    # Split documents into smaller, semantically meaningful chunks.
    # chunk_size: max characters in a chunk
    # chunk_overlap: characters to overlap between chunks to maintain context
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    chunks = text_splitter.split_documents(documents)

    if not chunks:
        raise ValueError("Text splitting resulted in no chunks. The document might be empty or unreadable.")

    print("3. Creating text embeddings and storing them in a FAISS vector store.")
    # Create embeddings for each chunk and store them in a FAISS vector store.
    # This is the "database" for our semantic search.
    # The Gemini embedding model "models/embedding-001" is used here.
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

    # --- RATE LIMITING & RETRY IMPLEMENTATION ---
    # The free tier for Google AI has a strict rate limit. To avoid errors,
    # we process the document chunks in small batches and add delays.
    # This is not a special "batch API"; it's a client-side strategy to
    # control the rate of standard API calls gracefully.
    batch_size = 40  # Smaller batch size for more controlled requests
    vector_store = None
    max_retries = 3

    for i in range(0, len(chunks), batch_size):
        batch_chunks = chunks[i:i + batch_size]
        current_batch_num = (i // batch_size) + 1
        total_batches = (len(chunks) + batch_size - 1) // batch_size
        print(f"  - Processing batch {current_batch_num}/{total_batches}...")

        for attempt in range(max_retries):
            try:
                if vector_store is None:
                    # Create the vector store with the first batch
                    vector_store = FAISS.from_documents(batch_chunks, embeddings)
                else:
                    # Add subsequent batches to the existing store
                    vector_store.add_documents(batch_chunks)
                
                # If successful, break the retry loop and move to the next batch
                break
            except Exception as e:
                # Check if the error is a rate limit error (429)
                if "429" in str(e) and attempt < max_retries - 1:
                    wait_time = 2 ** (attempt + 1)  # Exponential backoff: 2s, 4s
                    print(f"    Rate limit hit. Waiting for {wait_time} seconds before retrying...")
                    time.sleep(wait_time)
                else:
                    # If it's not a rate limit error or it's the final attempt, re-raise
                    print(f"    An unrecoverable error occurred during embedding: {e}")
                    raise e
        
        # Add a small delay between successful batches to respect the API limits
        if current_batch_num < total_batches:
             print("  - Waiting for 1 second before the next batch...")
             time.sleep(1)


    print("4. Creating a retriever for searching the vector store.")
    # A retriever is a component that fetches the most relevant documents
    # from the vector store based on a user's query.
    # k=3 means it will retrieve the top 3 most relevant chunks.
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    print("5. Setting up the LLM and the prompt template.")
    # Initialize the Gemini Pro model for generation.
    llm = GoogleGenerativeAI(model="models/gemini-2.5-pro")

    # The prompt template is crucial. It instructs the LLM how to behave.
    # It takes the retrieved "context" (the chunks) and the "question"
    # and formats them into a single prompt for the LLM.
    prompt_template = """
    You are a helpful assistant who answers questions based on the provided context.
    Synthesize the information from all relevant pieces of the context to provide a complete and comprehensive answer.
    If the information is not in the context, say that you cannot find the answer in the provided documents.
    Do not make up information.

    CONTEXT:
    {context}

    QUESTION:
    {question}

    ANSWER:
    """
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

    # This is where we define the RAG chain using a simplified syntax.
    # It's a pipeline that:
    # 1. Takes the user's question.
    # 2. The retriever fetches relevant context.
    # 3. The context and question are formatted by the prompt.
    # 4. The formatted prompt is sent to the LLM.
    # 5. The LLM generates the final answer.
    def rag_chain(question: str):
        retrieved_docs = retriever.invoke(question)
        # Format the retrieved docs into a single string for the context.
        formatted_context = "\n\n".join(doc.page_content for doc in retrieved_docs)
        # Fill the prompt template
        formatted_prompt = prompt.format(context=formatted_context, question=question)
        # Get the answer from the LLM
        answer = llm.invoke(formatted_prompt)
        return answer

    print("✅ RAG chain created successfully!")
    return rag_chain

def main():
    """Main function to run the Q&A bot."""
    # A simple check to see if a dummy document exists.
    # You should replace 'sample_document.pdf' with your actual file.
    if not os.path.exists(DOCUMENT_PATH):
        print(f"Error: Document not found at '{DOCUMENT_PATH}'")
        print("Please create a file named 'sample_document.pdf' or update the DOCUMENT_PATH variable in the script.")
        # Create a dummy PDF for demonstration if it doesn't exist
        try:
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import letter
            print("Creating a dummy 'sample_document.pdf' for you...")
            c = canvas.Canvas(DOCUMENT_PATH, pagesize=letter)
            c.drawString(72, 800, "RAG stands for Retrieval-Augmented Generation.")
            c.drawString(72, 780, "It is a technique for building AI applications that can answer questions")
            c.drawString(72, 760, "about private data sources without retraining the model.")
            c.drawString(72, 740, "The capital of Canada is Ottawa.")
            c.save()
            print("Dummy PDF created.")
        except ImportError:
            print("\nCould not create a dummy PDF because 'reportlab' is not installed.")
            print("Please run 'pip install reportlab' or create your own PDF file.")
            return

    try:
        chain = create_rag_chain(DOCUMENT_PATH)

        print("\n--- Document Q&A Bot ---")
        print("Ask questions about the content of your document.")
        print("Type 'exit' or 'quit' to end the session.")

        while True:
            question = input("\nYour Question: ")
            if question.lower() in ["exit", "quit"]:
                break
            if not question.strip():
                continue

            print("Thinking...")
            # Invoke the chain to get the answer
            answer = chain(question)
            print("\nAnswer:", answer)

    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("Please check your API key, file path, and internet connection.")

if __name__ == "__main__":
    main()

