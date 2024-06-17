from typing import List
import strawberry


@strawberry.type
class PlayerDataType:
    team_id: int = strawberry.field(name="team_id")
    player_id: int = strawberry.field(name="player_id")
    player_name: str = strawberry.field(name="player_name")


@strawberry.input
class PlayerDataInput:
    team_name: str = strawberry.field(name="team_name")
    player_name: str = strawberry.field(name="player_name")


@strawberry.type
class PlayerDataOutput:
    player_id: int = strawberry.field(name="player_id")
    player_name: str = strawberry.field(name="player_name")


@strawberry.type
class PlayerDataListType:
    team_id: int = strawberry.field(name="team_id")
    team_name: str = strawberry.field(name="team_name")
    players_data: List[PlayerDataOutput] = strawberry.field(name="players_data")
