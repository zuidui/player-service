import strawberry
from strawberry.types import Info
from typing import Annotated, Optional

from resolver.player_schema import PlayerCreateType, PlayerCreateInput

from service.team_service import TeamService

from utils.logger import logger_config

log = logger_config(__name__)


@strawberry.type
class PlayerMutation:
    @strawberry.mutation(name="create_player")
    async def create_player(
        self,
        info: Info,
        new_player: Annotated[PlayerCreateInput, strawberry.argument(name="new_team")],
    ) -> Optional[PlayerCreateType]:
        publisher = info.context["publisher"]
        log.info(f"Creating player with data: {new_player}")
        return await TeamService.create_player(new_player, publisher)
