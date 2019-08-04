class Topic(object):
    def __init__(self, description, summary, number, type):
        self.description = description
        self.summary = summary
        self.number = number
        self.type = type

    def __repr__(self):
        return '<Topic(name={self.description!r})>'.format(self=self)