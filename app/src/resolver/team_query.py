import strawberry
from typing import Optional

from resolver.team_schema import TeamType

from service.team_service import TeamService


@strawberry.type
class TeamQuery:
    @strawberry.field(name="getTeamByName", description="Get team by name")
    async def get_team_by_name(self, team_name: str) -> Optional[TeamType]:
        return await TeamService.get_team_by_name(team_name)
