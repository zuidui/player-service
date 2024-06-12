import strawberry


@strawberry.type
class TeamQuery:
    @strawberry.field(name="get_teams")
    async def get_teams(self) -> str:
        return "placeholder for get_teams"
