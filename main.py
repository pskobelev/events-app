import logging

import uvicorn
from fastapi import FastAPI

from core.config import settings
from app.api.events.views import router

# from app.api.users.views import router as users_router
# from app.db.routes import root_router

logging.basicConfig(
    level=logging.DEBUG,
    format=settings.logging.log_format
)

app = FastAPI()
app.include_router(router)

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