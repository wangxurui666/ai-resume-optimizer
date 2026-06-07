import os
from dotenv import load_dotenv

load_dotenv()


def _get(key: str, default: str = None) -> str:
    """Try Streamlit Cloud secrets first, then env vars, then default."""
    try:
        import streamlit as st
        if hasattr(st, "secrets") and key in st.secrets:
            return st.secrets[key]
    except Exception:
        pass
    return os.getenv(key, default)


DEEPSEEK_API_KEY = _get("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = _get("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
DEEPSEEK_MODEL = _get("DEEPSEEK_MODEL", "deepseek-chat")
CHROMA_PATH = _get("CHROMA_PATH", "./chroma_db")
