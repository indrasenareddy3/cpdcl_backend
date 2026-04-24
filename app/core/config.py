from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    model_config = SettingsConfigDict(
        env_file=".env",   # only for local
        extra="ignore"
    )

settings = Settings()



# from pydantic_settings import BaseSettings

# class Settings(BaseSettings):
#     DATABASE_URL: str
#     SECRET_KEY: str
#     ALGORITHM: str
#     ACCESS_TOKEN_EXPIRE_MINUTES: int

#     class Config:
#         env_file = ".env"

# settings = Settings()


# from pydantic import BaseSettings

# class Settings(BaseSettings):
#     DATABASE_URL: str
#     SECRET_KEY: str
#     ALGORITHM: str
#     ACCESS_TOKEN_EXPIRE_MINUTES: int

#     class Config:
#         env_file = ".env"

# settings = Settings()