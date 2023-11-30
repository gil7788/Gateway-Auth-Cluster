from app import app
import uvicorn
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
