from core.config import settings


class ApiRoutes:
    BASE_URL = settings.api.url
    EVENT_BASE = "/events"

    # GET
    LIST_EVENT = "/"
    FIND_EVENT = (
        "/{chat_id}/{event_id}"  # find by chat_id, event_id over params
    )
    STATS = "/stat/{event_id}"  # find by event_id params

    # POST
    ADD_EVENT = "/"
    USER_CHOICE = "/choice/"

    # PATCH
    CLOSE_EVENT = "/{chat_id}"
    LIMIT = "/limit"

    # DELETE
    DELETE_EVENT = "/{event_id}"

    @classmethod
    def get_full_url(cls, route: str, **kwargs):
        return f"{cls.BASE_URL + cls.EVENT_BASE}{route}".format(**kwargs)
