

class Score:
    def __init__(self):
        self.TeamCarpetsWon = {0: [], 1: []}
        self.PointsOfTeams = {0: 0, 1: 0}

        self.TargetPoints = -1
        self.chasingTeam = None
        self.winningTeam = None

    @classmethod
    def initial_score(cls, target, team):
        score = cls()

        score.TargetPoints = target
        score.chasingTeam = team

        return score

    def set_winning_team(self):
        if self.PointsOfTeams[str(self.chasingTeam)] > self.TargetPoints:
            self.winningTeam = self.chasingTeam

        defending_team = 1 - self.chasingTeam

        if self.PointsOfTeams[str(defending_team)] > 904 - self.TargetPoints:
            self.winningTeam = self.chasingTeam

    def add_points(self, winning_team, carpet):
        self.PointsOfTeams[str(winning_team)] = self.PointsOfTeams[str(winning_team)] + carpet.get_points()
        self.TeamCarpetsWon[str(winning_team)].append(carpet)


# Not used
def other_team(team):
    return 1 - team

