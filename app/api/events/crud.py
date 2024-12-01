from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.db_helper import get_session


async def new_event(db: AsyncSession = Depends(get_session()), ):
    """Create a new event."""
    pass


async def event_cancel(db: AsyncSession = Depends(get_session()), ):
    """Cancel an event."""
    pass
