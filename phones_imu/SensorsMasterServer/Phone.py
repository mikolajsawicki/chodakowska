class Phone:
    def __init__(self, ip, label):
        self.ip = ip
        self.label = label

    def __repr__(self):
        return ', '.join((self.ip, self.label))
