from dataclasses import dataclass
from environs import Env

env = Env()
env.read_env()


@dataclass
class FASTAPI:
    HOST: str = env.str("HOST")
    PORT: int = env.int("PORT")
    DEBUG: bool = env.bool("DEBUG")


@dataclass
class POSTGRES:
    LOGIN: str = env.str("POSTGRES_LOGIN")
    PASSWORD: str = env.str("POSTGRES_PASSWORD")
    HOST: str = env.str("POSTGRES_HOST")
    DB: str = env.str("POSTGRES_DB")
    URL: str = f"postgresql+psycopg2://{LOGIN}:{PASSWORD}@{HOST}/{DB}"


@dataclass
class EMAIL:
    ADDRESS: str = env.str("EMAIL_ADDRESS")
    PASSWORD: str = env.str("EMAIL_PASSWORD")
    SERVER: str = env.str("EMAIL_SERVER")
    PORT: int = env.int("EMAIL_PORT")


@dataclass
class SHEDULE:
    DIRECTORY: str = env.str("SHEDULE_DIRECTORY")
    URL: str = env.str("SHEDULE_URL")
    YANDEX_DOWNLOAD_URL: str = env.str("SHEDULE_YANDEX_DOWNLOAD_URL")
