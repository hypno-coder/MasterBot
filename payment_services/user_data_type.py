from typing import TypedDict

class UserDataType(TypedDict):
    chat_id: int
    user_id: int
    service_species: str
    fio: str
    birthday: str

user_data: UserDataType = UserDataType(
    chat_id=0,
    user_id=0,
    service_species='',
    fio='',
    birthday='',
)
