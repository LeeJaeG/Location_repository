from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    mongo_url: str = "mongodb://192.168.15.21:27017"
    mongo_db: str = "physical_database"
    upload_dir: str = "../images"

settings = Settings()
