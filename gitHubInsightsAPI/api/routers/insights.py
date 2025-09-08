from fastapi import APIRouter
from gitHubInsightsAPI.repositories.repo_insights import InsightsRepository


router = APIRouter(prefix="/insights", tags=["insights"])


@router.get("/repos/{repo_id}")
async def get_repo_insights(repo_id: str):
    repo_insigths = InsightsRepository()
    insights = repo_insigths.get_insights_by_repo_id(int(repo_id))

    return {"repo_id": repo_id,
            "insights": insights}


@router.get("/users/{login}/repos/{repo_id}")
async def get_user_contribution(login: str, repo_id: str):
    return {"repo_id": repo_id,
            "login": login}


@router.get("/users/{login}")
async def get_user_insights(login: str):
    return {"login": login}
