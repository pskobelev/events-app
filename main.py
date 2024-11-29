import uvicorn
from fastapi import FastAPI

from app.api.users.views import router as users_router
from app.api.events.views import router as events_router
from app.core.config import get_config
from app.db.routes import root_router

config = get_config()

app = FastAPI(title=str(config.API_NAME))
app.include_router(root_router)
app.include_router(users_router)
app.include_router(events_router)

if __name__ == "__main__":
    try:
        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    except KeyboardInterrupt:
        print("App stopped by user. Goodbye!")
