from strawberry import Schema

from resolver.player_query import PlayerQuery
from resolver.player_mutation import PlayerMutation
from resolver.team_query import TeamQuery
from resolver.team_mutation import TeamMutation


class Query(TeamQuery, PlayerQuery):
    pass


class Mutation(TeamMutation, PlayerMutation):
    pass


schema = Schema(query=Query, mutation=Mutation)
