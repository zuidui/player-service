import strawberry


@strawberry.type
class Query:
    @strawberry.field(name="get_teams")
    async def get_teams(self) -> str:
        return "placeholder for get_teams"

    @strawberry.field(name="get_players")
    async def get_players(self) -> str:
        return "get_players"
