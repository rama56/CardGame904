

class Score:
    def __init__(self):
        self.TeamCarpetsWon = ([], [])
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
        if self.PointsOfTeams[self.chasingTeam] > self.TargetPoints:
            self.winningTeam = self.chasingTeam

        defending_team = 1 - self.chasingTeam

        if self.PointsOfTeams[defending_team] > 904 - self.TargetPoints:
            self.winningTeam = self.chasingTeam

    def add_points(self, points, winning_team, carpet):
        self.PointsOfTeams[winning_team] = self.PointsOfTeams[winning_team] + points
        self.TeamCarpetsWon[winning_team].append(carpet)


# Not used
def other_team(team):
    return 1 - team

