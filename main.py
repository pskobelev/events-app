import logging

import uvicorn
from fastapi import FastAPI

from app.api.events.views import router
from core.config import settings

logging.basicConfig(level=logging.DEBUG, format=settings.logging.log_format)
logger = logging.getLogger(__name__)
app = FastAPI()
app.include_router(router)

db_url = settings.db.url
logger.warning("CURRENT DB URL: %s", db_url)

if __name__ == "__main__":
    try:
        uvicorn.run(
            "main:app",
            host=settings.run.host,
            port=settings.run.port,
            reload=True,
        )
    except KeyboardInterrupt:
        print("App stopped by user. Goodbye!")
