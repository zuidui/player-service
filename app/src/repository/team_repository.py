from typing import Optional
from sqlalchemy.future import select as sql_select
from model.team_model import Team
from database.session import db
from utils.logger import logger_config

log = logger_config(__name__)


class TeamRepository:
    @staticmethod
    async def create(team_data: Team) -> Team:
        async with db.get_db() as session:
            async with db.commit_rollback(session):
                session.add(team_data)
                await session.flush()
                await session.refresh(team_data)
                log.info(f"Team created in repository: {team_data.to_dict()}")
        return team_data

    @staticmethod
    async def get_by_name(team_name: str) -> Optional[Team]:
        async with db.get_db() as session:
            stmt = sql_select(Team).where(Team.team_name == team_name)
            result = await session.execute(stmt)
            team = result.scalars().first()
            if team:
                await session.refresh(team)
                log.info(f"Team found in repository: {team.to_dict()}")
        return team
