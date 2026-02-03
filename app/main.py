import subprocess
import time
from dotenv import load_dotenv
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)
load_dotenv()

def run_backend():
    try:
        logger.info("Starting backend API server...")
        return subprocess.Popen(
            ["uvicorn", "app.backend.api:app", "--host", "127.0.0.1", "--port", "9999"]
        )
    except Exception as e:
        logger.error(f"Failed to start backend server: {e}")
        raise CustomException("Backend server failed to start", e)

def run_frontend():
    try:
        logger.info("Starting frontend Streamlit app...")
        return subprocess.Popen(
            [
                "streamlit",
                "run",
                "app/frontend/ui.py",
                "--server.address=0.0.0.0",
                "--server.port=8501",
                "--server.headless=true",
                "--browser.gatherUsageStats=false"
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
    except Exception as e:
        logger.error(f"Failed to start frontend app: {e}")
        raise CustomException("Frontend app failed to start", e)


if __name__ == "__main__":
    try:
        backend = run_backend()
        time.sleep(3)  # give backend time to boot
        frontend = run_frontend()

        backend.wait()
        frontend.wait()

    except Exception as e:
        logger.error(f"Application failed to start: {e}")
        raise CustomException("Application startup failed", e)
