import strawberry


@strawberry.type
class TeamType:
    teamId: int
    teamName: str
    teamPassword: str
    createdAt: str


@strawberry.input
class TeamInput:
    teamName: str
    teamPassword: str
