from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from core.config import settings

sf_engine = create_engine(settings.SNOWFLAKE_SQLALCHEMY_URL)
SnowflakeSession = sessionmaker(
    bind=sf_engine, autoflush=False, expire_on_commit=False)


def get_snowflake_session():
    """FastAPI dependency (sync) or general context manager."""
    session = SnowflakeSession()
    try:
        with sf_engine.connect() as conn:
            result = conn.execute(text("SELECT CURRENT_VERSION()")).fetchone()
            print(f"Connected to Snowflake, version: {result[0]}")
    except Exception as e:
        print(f"Failed to connect to Snowflake: {e}")
    finally:
        session.close()
