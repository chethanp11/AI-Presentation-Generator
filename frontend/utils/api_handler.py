import os
from functools import lru_cache

import streamlit as st


@lru_cache(maxsize=1)
def get_backend_base_url() -> str:
    """
    Resolve the backend base URL in the following priority:
    1. Environment variable BACKEND_API_BASE_URL
    2. Streamlit secrets entry BACKEND_API_BASE_URL
    3. Fallback to localhost for local development
    """
    env_url = os.getenv("BACKEND_API_BASE_URL")

    secret_url = None
    try:
        secret_url = st.secrets.get("BACKEND_API_BASE_URL")
    except Exception:
        # st.secrets may not be configured outside of Streamlit runtime
        secret_url = None

    base_url = env_url or secret_url or "http://localhost:8000"
    return base_url.rstrip("/")
