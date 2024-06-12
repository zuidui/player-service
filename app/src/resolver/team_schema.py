import strawberry


@strawberry.type
class TeamCreateType:
    team_id: int = strawberry.field(name="team_id")
    team_name: str = strawberry.field(name="team_name")


@strawberry.input
class TeamCreateInput:
    team_name: str = strawberry.field(name="team_name")
    team_password: str = strawberry.field(name="team_password")
