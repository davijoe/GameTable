from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "BGG_Scraper"
    base_url: str = "https://boardgamegeek.com/xmlapi2"

    api_token: str

    mongo_root_username: str
    mongo_root_password: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
