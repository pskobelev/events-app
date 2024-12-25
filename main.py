import uvicorn
from fastapi import FastAPI

from core.config import settings

# from app.api.users.views import router as users_router
# from app.db.routes import root_router


app = FastAPI()


if __name__ == "__main__":
    try:
        uvicorn.run("main:app",
                    host=settings.run.host,
                    port=settings.run.port, reload=True)
    except KeyboardInterrupt:
        print("App stopped by user. Goodbye!")
