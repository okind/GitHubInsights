from fastapi import APIRouter


router = APIRouter(prefix="/insights", tags=["insights"])


@router.get("/repos/{repo_id}")
async def get_repo_insights(repo_id: str):
    return {"repo_id": repo_id}


@router.get("/users/{login}/repos/{repo_id}")
async def get_user_contribution(login: str, repo_id: str):
    return {"repo_id": repo_id,
            "login": login}


@router.get("/users/{login}")
async def get_user_insights(login: str):
    return {"login": login}
