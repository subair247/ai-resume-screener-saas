from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Resume Screener"
    DATABASE_URL: str = "mysql+pymysql://root:password@localhost:3306/resume_db"
    SECRET_KEY: str = "supersecretkey"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    GEMINI_API_KEY: str
    MAIL_USERNAME: str
    MAIL_PASSWORD: str

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()