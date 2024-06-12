from typing import Optional
from sqlalchemy.future import select as sql_select
from model.player_model import Player
from data.session import db
from utils.logger import logger_config

log = logger_config(__name__)


class PlayerRepository:
    @staticmethod
    async def create(player_data: Player) -> Player:
        async with db.get_db() as session:
            async with db.commit_rollback(session):
                session.add(player_data)
                await session.flush()
                await session.refresh(player_data)
                log.info(f"Player created in repository: {player_data.to_dict()}")
        return player_data

    @staticmethod
    async def get_by_name(player_name: str) -> Optional[Player]:
        async with db.get_db() as session:
            stmt = sql_select(Player).where(Player.player_name == player_name)
            result = await session.execute(stmt)
            player = result.scalars().first()
            if player:
                await session.refresh(player)
                log.info(f"Player found in repository: {player.to_dict()}")
        return player

    @staticmethod
    async def player_exists_by_name_in_team(player_name: str, team_id: int) -> bool:
        async with db.get_db() as session:
            stmt = sql_select(Player).where(
                Player.player_name == player_name, Player.team_id == team_id
            )
            result = await session.execute(stmt)
            player = result.scalars().first()
            return player is not None
