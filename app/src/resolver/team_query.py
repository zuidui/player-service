import strawberry


@strawberry.type
class TeamQuery:
    @strawberry.field(name="getTeamByName")
    async def get_team_by_name(self, team_name: str) -> str:
        return "placeholder"
