import strawberry


@strawberry.type
class PlayerQuery:
    @strawberry.field(name="get_players")
    async def get_players(self) -> str:
        return "get_players"
