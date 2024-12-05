from aiogram.filters.callback_data import CallbackData


class EventsCallback(CallbackData, prefix="events"):
    action: str
