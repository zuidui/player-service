import strawberry


@strawberry.type
class PlayerCreateType:
    player_id: int = strawberry.field(name="player_id")
    player_name: str = strawberry.field(name="player_name")
    player_team_id: int = strawberry.field(name="player_team_id")


@strawberry.input
class PlayerCreateInput:
    player_team_id: int = strawberry.field(name="player_team_id")
    player_name: str = strawberry.field(name="player_name")
