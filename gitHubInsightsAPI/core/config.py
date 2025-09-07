from pydantic_settings import BaseSettings, SettingsConfigDict
from urllib.parse import quote_plus


class Settings(BaseSettings):
    SNOWFLAKE_USER: str
    SNOWFLAKE_PASSWORD: str
    SNOWFLAKE_ACCOUNT: str
    SNOWFLAKE_WAREHOUSE: str
    SNOWFLAKE_DATABASE: str
    SNOWFLAKE_SCHEMA: str
    SNOWFLAKE_ROLE: str

    model_config = SettingsConfigDict(
        env_file="gitHubInsightsAPI\core\.env", case_sensitive=True)

    @property
    def SNOWFLAKE_SQLALCHEMY_URL(self) -> str:
        pw = "" if not self.SNOWFLAKE_PASSWORD else ":" + \
            quote_plus(self.SNOWFLAKE_PASSWORD)
        # snowflake://user:pass@account/DATABASE/SCHEMA?warehouse=...&role=...&authenticator=...
        qs = [f"warehouse={self.SNOWFLAKE_WAREHOUSE}"]
        if self.SNOWFLAKE_ROLE:
            qs.append(f"role={self.SNOWFLAKE_ROLE}")
        return (
            f"snowflake://{self.SNOWFLAKE_USER}{pw}"
            f"@{self.SNOWFLAKE_ACCOUNT}/{self.SNOWFLAKE_DATABASE}/{self.SNOWFLAKE_SCHEMA}"
            f"?{'&'.join(qs)}"
        )


settings = Settings()
