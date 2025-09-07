from fastapi import FastAPI
from gitHubInsightsAPI.api.routers.insights import router as insights_router

app = FastAPI()

app.include_router(insights_router)
