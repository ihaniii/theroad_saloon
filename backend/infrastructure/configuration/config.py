import os

class AppConfig:
    ENV = os.getenv("APP_ENV", "development")
    DEBUG = ENV in ["development", "testing"]
    
    # Database
    # Default is SQLite for local test/dev, but switches to PostgreSQL in staging/production
    DB_ENGINE = os.getenv("DB_ENGINE", "sqlite")  # sqlite or postgresql
    POSTGRES_USER = os.getenv("POSTGRES_USER", "theroad_admin")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "theroad_password_2026")
    POSTGRES_DB = os.getenv("POSTGRES_DB", "theroad_prod")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

    @classmethod
    def get_db_url(cls) -> str:
        if cls.DB_ENGINE == "postgresql":
            return f"postgresql://{cls.POSTGRES_USER}:{cls.POSTGRES_PASSWORD}@{cls.POSTGRES_HOST}:{cls.POSTGRES_PORT}/{cls.POSTGRES_DB}"
        return "file:theroad_test_db?mode=memory&cache=shared"
    
    # Auth
    JWT_SECRET = os.getenv("JWT_SECRET", "the_road_production_secret_key_2026")
    JWT_ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
