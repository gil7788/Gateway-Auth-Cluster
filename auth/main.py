from app import app
import uvicorn
import logging


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("uvicorn")
    uvicorn.run(app, host="0.0.0.0", port=8000)
