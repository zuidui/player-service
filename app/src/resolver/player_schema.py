import strawberry


@strawberry.type
class PlayerDataType:
    team_id: int = strawberry.field(name="team_id")
    player_id: int = strawberry.field(name="player_id")
    player_name: str = strawberry.field(name="player_name")


@strawberry.input
class PlayerDataInput:
    team_id: int = strawberry.field(name="team_id")
    player_name: str = strawberry.field(name="player_name")


@strawberry.type
class PlayerDataOutput:
    team_id: int = strawberry.field(name="team_id")
    player_name: str = strawberry.field(name="player_name")
