from typing import List
import strawberry

from service.team_service import TeamService

from resolver.player_schema import PlayerDataType


@strawberry.type
class Query:
    @strawberry.field(name="get_players")
    async def get_players(self, team_id: int) -> List[PlayerDataType]:
        return await TeamService.get_players(team_id)
