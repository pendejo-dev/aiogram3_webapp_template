from typing import Optional

from pydantic import BaseSettings, SecretStr, validator, BaseModel


class Redis(BaseModel):
    host: str
    port: int = 6379
    db: int
    password: str = "IGivgFCKBmBmETW6cyoGQi7q0JQidBPgbrGSuoOQMGS86XEG8GnnS2811pn0DLoy"


class Settings(BaseSettings):
    bot_token: Optional[str]

    moderation_group: str
    report_group: str
    support_group: str

    webhook_domain: Optional[str]
    webhook_path: Optional[str]

    app_host: Optional[str] = "0.0.0.0"
    app_port: Optional[int] = 8444

    postgres_host: Optional[str]
    postgres_port: Optional[int]
    postgres_user: Optional[str]
    postgres_database: Optional[str]
    postgres_password: Optional[str]

    fsm_mode: str

    distribution_address: str
    distribution_private: str

    sharable_secret: Optional[str]

    @validator("fsm_mode")
    def fsm_type_check(cls, v):
        if v not in ("memory", "redis"):
            raise ValueError("Incorrect fsm_mode. Must be one of: memory, redis")
        return v

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        env_nested_delimiter = '__'


config = Settings()
