try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str = "change-me-to-a-secure-random-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    # MySQL Database with XAMPP
    DATABASE_URL: str = "mysql+pymysql://root:@localhost:3306/smd_db"
    
    # Google Gemini AI Configuration
    GEMINI_API_KEY: str = "YOUR_GEMINI_API_KEY_HERE"  # Get from https://makersuite.google.com/app/apikey
    GEMINI_MODEL: str = "gemini-pro"  # or "gemini-pro-vision" for image support


settings = Settings()
