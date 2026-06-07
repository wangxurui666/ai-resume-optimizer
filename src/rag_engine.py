"""
RAG engine: chunk resume text → embed → store in ChromaDB → retrieve.
Uses local sentence-transformers for embeddings (free, no API needed).
"""
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from src.config import CHROMA_PATH
import os


# Use a Chinese-capable embedding model, runs locally
EMBEDDING_MODEL_NAME = "shibing624/text2vec-base-chinese"


def get_embeddings():
    """Load local embedding model (cached after first download)."""
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )


def build_vectorstore(resume_text: str) -> Chroma:
    """Chunk resume text and build a ChromaDB vector store."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        separators=["\n\n", "\n", "。", ".", " ", ""],
    )
    chunks = splitter.split_text(resume_text)

    # Remove old DB if exists
    if os.path.exists(CHROMA_PATH):
        import shutil
        shutil.rmtree(CHROMA_PATH)

    embeddings = get_embeddings()
    vectorstore = Chroma.from_texts(
        texts=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PATH,
    )
    return vectorstore


def retrieve_context(vectorstore: Chroma, query: str, k: int = 5) -> str:
    """Retrieve relevant resume sections for a given query."""
    docs = vectorstore.similarity_search(query, k=k)
    return "\n\n---\n\n".join([d.page_content for d in docs])
