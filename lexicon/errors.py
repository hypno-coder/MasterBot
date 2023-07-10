from enum import Enum

class QueryErrText(Enum):
    INSERT_USER = "Ошибка добавления пользователя в БД"
    FIND_USER = "Ошибка поиска пользователя в БД"
    UPDATE_USER = "Ошибка обновления пользователя в БД"
    USERS_COUNT = "Ошибка запроса количества пользователей в Боте"

