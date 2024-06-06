import strawberry


@strawberry.type
class PlayerType:
    playerId: int
    teamId: int
    playerName: str
    createdAt: str


@strawberry.input
class PlayerInput:
    teamId: int
    playerName: str
