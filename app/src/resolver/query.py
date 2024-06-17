from typing import Annotated, Optional
import strawberry

from service.team_service import TeamService

from resolver.player_schema import PlayerDataListType

from utils.logger import logger_config

log = logger_config(__name__)


@strawberry.type
class Query:
    @strawberry.field(name="get_players")
    async def get_players(
        self,
        team_name: Annotated[str, strawberry.argument(name="team_name")],
    ) -> Optional[PlayerDataListType]:
        log.info(f"Getting players for team {team_name}")
        return await TeamService.get_players(team_name)
