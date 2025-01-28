from core.config import settings


class ApiRoutes:
    BASE_URL = settings.api.url
    EVENT_BASE = "/events"

    ADD_EVENT = "/add"
    LIST_EVENT = "/events"
    CLOSE_EVENT = "/close"
    DELETE_EVENT = "/delete"
    FIND_EVENT = "/active"  # find by chat_id, event_id over params

    USER_CHOICE = "/user_choice"

    STATS = "/stats"  # find by event_id params

    @classmethod
    def get_full_url(cls, route: str, **kwargs):
        return f"{cls.BASE_URL + cls.EVENT_BASE}{route}".format(**kwargs)


print(ApiRoutes.get_full_url(ApiRoutes.CLOSE_EVENT, chat_id=123))
