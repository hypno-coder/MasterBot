from typing import TypedDict


class UserDataType(TypedDict):
    chat_id: int
    user_id: int
    service_species: str
    fio: str
    gender: str | None
    month: str | None
    destiny_card: str | None
    birthday: str | None
    jantra: dict[str, str] | None
    min_delay: str
    max_delay: str


user_data: UserDataType = UserDataType(
    chat_id=0,
    user_id=0,
    service_species="",
    fio="",
    gender=None,
    month=None,
    destiny_card=None,
    birthday=None,
    jantra=None,
    min_delay="",
    max_delay="",
)
