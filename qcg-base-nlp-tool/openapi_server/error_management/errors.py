from connexion.exceptions import ProblemException

class BadRequestProblem(ProblemException):

    def __init__(self, type=None, title='Bad Request', detail=None):
        super(BadRequestProblem, self).__init__(type=type, status=400, title=title, detail=detail)
