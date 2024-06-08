from strawberry import Schema


from resolver.team_query import TeamQuery
from resolver.team_mutation import TeamMutation


class Query(TeamQuery):
    pass


class Mutation(TeamMutation):
    pass


schema = Schema(query=TeamQuery, mutation=TeamMutation)
