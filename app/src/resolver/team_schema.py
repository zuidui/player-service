from typing import List
import strawberry

from resolver.player_schema import PlayerDataOutput


@strawberry.type
class TeamDataType:
    team_id: int = strawberry.field(name="team_id")
    team_name: str = strawberry.field(name="team_name")


@strawberry.input
class TeamDataInput:
    team_name: str = strawberry.field(name="team_name")
    team_password: str = strawberry.field(name="team_password")


@strawberry.type
class TeamDetailsType:
    team_id: int = strawberry.field(name="team_id")
    team_name: str = strawberry.field(name="team_name")
    players_data: List[PlayerDataOutput] = strawberry.field(name="players_data")
