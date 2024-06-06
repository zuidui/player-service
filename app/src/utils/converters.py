from typing import Optional

from model.team_model import Team
from model.player_model import Player

from resolver.team_schema import TeamType
from resolver.player_schema import PlayerType


def convert_team_to_teamtype(team: Optional[Team]) -> TeamType:
    if team is None:
        raise ValueError("Cannot convert None to TeamType")

    return TeamType(
        teamId=int(team.team_id),
        teamName=str(team.team_name),
        teamPassword=str(team.team_password),
        createdAt=str(team.created_at),
    )


def convert_player_to_playertype(player: Optional[Player]) -> PlayerType:
    if player is None:
        raise ValueError("Cannot convert None to PlayerType")

    return PlayerType(
        playerId=int(player.player_id),
        teamId=int(player.team_id),
        playerName=str(player.player_name),
        createdAt=str(player.created_at),
    )
