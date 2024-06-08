import strawberry


@strawberry.type
class TeamCreateResponse:
    team_id: int = strawberry.field(name="team_id")
    team_name: str = strawberry.field(name="team_name")


@strawberry.input
class TeamCreateRequest:
    team_name: str = strawberry.field(name="team_name")
    team_password: str = strawberry.field(name="team_password")
