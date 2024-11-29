from fastapi import APIRouter

router = APIRouter(prefix="/events", tags=["events"])


@router.get("/")
async def get_events():
    pass


@router.post("/add")
async def add_event():
    pass


@router.delete("/delete")
async def delete_event():
    pass
