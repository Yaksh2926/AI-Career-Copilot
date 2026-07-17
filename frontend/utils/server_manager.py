import os
import sys
import time
import requests
import subprocess
import logging
from frontend.config import API_BASE_URL

# Local Server Manager Logger
logger = logging.getLogger("AI Career Copilot ServerManager")
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

def is_backend_running() -> bool:
    """
    Checks if the FastAPI backend is running by calling the health endpoint.
    """
    try:
        response = requests.get(f"{API_BASE_URL}/resume", timeout=2)
        if response.status_code == 200:
            data = response.json()
            return data.get("success", False)
    except Exception:
        pass
    return False

def start_backend_server():
    """
    Spawns the FastAPI backend server using uvicorn in a background process.
    Uses sys.executable to ensure we run inside the same python environment.
    """
    if is_backend_running():
        logger.info("FastAPI backend is already running.")
        return True
        
    logger.info("FastAPI backend not detected. Starting backend process...")
    try:
        # Run uvicorn as a background process from the root directory
        process = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            close_fds=True
        )
        
        # Wait up to 10 seconds for the backend to start up
        for i in range(10):
            time.sleep(1)
            if is_backend_running():
                logger.info(f"FastAPI backend started successfully (PID: {process.pid})")
                return True
                
        logger.error("Failed to detect FastAPI backend after starting subprocess.")
        return False
    except Exception as e:
        logger.error(f"Error spawning backend server: {str(e)}")
        return False
