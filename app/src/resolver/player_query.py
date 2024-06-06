import strawberry
from typing import Optional

from resolver.player_schema import PlayerType

from service.team_service import TeamService


@strawberry.type
class PlayerQuery:
    @strawberry.field(name="getPlayerByName", description="Get player by name")
    async def get_player_by_name(self, player_name: str) -> Optional[PlayerType]:
        return await TeamService.get_player_by_name(player_name)
