import strawberry
from strawberry.types import Info

from typing import Optional

from resolver.player_schema import PlayerInput, PlayerType

from service.team_service import TeamService


@strawberry.type
class PlayerMutation:
    @strawberry.mutation(name="createPlayer", description="Create a new player")
    async def create_player(
        self, info: Info, new_player: PlayerInput
    ) -> Optional[PlayerType]:
        publisher = info.context["publisher"]
        return await TeamService.create_player(new_player, publisher)
