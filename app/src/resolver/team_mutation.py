import strawberry
from strawberry.types import Info
from typing import Annotated, Optional

from resolver.team_schema import TeamCreateRequest, TeamCreateResponse

from service.team_service import TeamService

from utils.logger import logger_config

log = logger_config(__name__)


@strawberry.type
class TeamMutation:
    @strawberry.mutation(name="create_team")
    async def create_team(
        self,
        info: Info,
        new_team: Annotated[TeamCreateRequest, strawberry.argument(name="new_team")],
    ) -> Optional[TeamCreateResponse]:
        publisher = info.context["publisher"]
        log.info(f"Creating team with data: {new_team}")
        return await TeamService.create_team(new_team, publisher)
