from fastapi import APIRouter

router = APIRouter(prefix="/events", tags=["events"])


@router.get("/")
async def get_events():
    """Returns all events"""
    pass


@router.post("/add")
async def add_event():
    """Add a new event"""
    pass


@router.delete("/delete")
async def delete_event():
    """Delete an event"""
    pass
