import strawberry
from strawberry.types import Info
from typing import Optional

from resolver.team_schema import TeamInput, TeamType

from service.team_service import TeamService


@strawberry.type
class TeamMutation:
    @strawberry.mutation(name="createTeam", description="Create a new team")
    async def create_team(self, info: Info, new_team: TeamInput) -> Optional[TeamType]:
        publisher = info.context["publisher"]
        return await TeamService.create_team(new_team, publisher)
