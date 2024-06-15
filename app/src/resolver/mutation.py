import strawberry
from strawberry.types import Info
from typing import Annotated, Optional

from resolver.team_schema import TeamCreateType, TeamCreateInput, TeamDataInput, TeamDataType
from resolver.player_schema import PlayerCreateInput, PlayerCreateType

from service.team_service import TeamService

from utils.logger import logger_config

log = logger_config(__name__)


@strawberry.type
class Mutation:
    @strawberry.mutation(name="create_team")
    async def create_team(
        self,
        info: Info,
        new_team: Annotated[TeamCreateInput, strawberry.argument(name="new_team")],
    ) -> Optional[TeamCreateType]:
        publisher = info.context["publisher"]
        log.info(f"Creating team with data: {new_team}")
        return await TeamService.create_team(new_team, publisher)

    @strawberry.mutation(name="create_player")
    async def create_player(
        self,
        info: Info,
        new_player: Annotated[
            PlayerCreateInput, strawberry.argument(name="new_player")
        ],
    ) -> Optional[PlayerCreateType]:
        publisher = info.context["publisher"]
        log.info(f"Creating player with data: {new_player}")
        return await TeamService.create_player(new_player, publisher)
    
    @strawberry.mutation(name="join_team")
    async def join_team(
        self,
        info: Info,
        team_data: Annotated[ TeamDataInput, strawberry.argument(name="team_data")
        ],
    ) -> Optional[TeamDataType]:
        publisher = info.context["publisher"]
        log.info(f"Joining team with data: {team_data}")
        return await TeamService.join_team(team_data, publisher)
