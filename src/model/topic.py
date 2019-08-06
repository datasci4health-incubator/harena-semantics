class Topic(object):
    description = ''

    def __init__(self, description, summary, number, type):
        self.description = description
        self.summary = summary
        self.number = number
        self.type = type

