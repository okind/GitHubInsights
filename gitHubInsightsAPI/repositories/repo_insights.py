# app/repositories/insights_repo.py
from __future__ import annotations

from typing import Iterable, List, Optional
from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session
from db.snowflake_session import get_snowflake_session

from gitHubInsightsAPI.models.repo_commits_by_week_model import RepoCommitsByWeekModel


class InsightsRepository:
    """Data access for weekly repo commits stats (COMMITS.PUBLIC.REPO_COMMITS_BY_WEEK)."""

    def __init__(self) -> None:
        self.session = get_snowflake_session()

    def get_week(self, week_start: date) -> List[RepoCommitsByWeekModel]:
        """Fetch a single row by its week."""
        stmt = select(RepoCommitsByWeekModel).where(
            RepoCommitsByWeekModel.week == week_start
        )

        result = self.session.execute(stmt)
        record = result.scalars().all()
        if record:
            print(
                f"Found record for week: {record[0].week}, Commits: {record[0].repo_commits_count}")
        else:
            print("No record found for the specified week.")
        return [] if record is None else record
