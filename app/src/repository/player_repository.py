from typing import Optional
from sqlalchemy.future import select as sql_select
from model.player_model import Player
from database.session import db
from utils.logger import logger_config

log = logger_config(__name__)


class PlayerRepository:
    @staticmethod
    async def create(player_data: Player) -> Player:
        async with db.get_db() as session:
            async with db.commit_rollback(session):
                session.add(player_data)
        return player_data

    @staticmethod
    async def get_by_name(player_name: str) -> Optional[Player]:
        async with db.get_db() as session:
            stmt = sql_select(Player).where(Player.player_name == player_name)
            result = await session.execute(stmt)
            player = result.scalars().first()
        return player
