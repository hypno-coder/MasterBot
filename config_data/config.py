from dataclasses import dataclass
from environs import Env


@dataclass
class DatabaseConfig:
    database: str         
    db_host: str         
    db_user: str        
    db_password: str   


@dataclass
class TgBot:
    token: str           
    subscribe_channel: int
    channel_link: str
    admin_ids: list[int] 


@dataclass
class Config:
    _instance = None
    tg_bot: TgBot
    db: DatabaseConfig
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

def load_config(path: str | None) -> Config:

    env: Env = Env()
    env.read_env(path)

    return Config(tg_bot=TgBot(token=env('BOT_TOKEN'),
                               subscribe_channel=int(env('SUBSCRIBE_CHANNEL')),
                               channel_link=env('CHANNEL_LINK'),
                               admin_ids=list(map(int, env.list('ADMIN_IDS')))),
                  db=DatabaseConfig(database=env('DATABASE'),
                                    db_host=env('DB_HOST'),
                                    db_user=env('DB_USER'),
                                    db_password=env('DB_PASSWORD')))
