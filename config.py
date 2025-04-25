from pydantic_settings import BaseSettings


class CnosDBConfig(BaseSettings):
    host: str = "127.0.0.1"
    port: int = 8902
    username: str = "root"
    password: str = ""
    database: str = "public"
    http_timeout: int = 5

    class Config:
        env_prefix = "CNOSDB_"

config = CnosDBConfig()