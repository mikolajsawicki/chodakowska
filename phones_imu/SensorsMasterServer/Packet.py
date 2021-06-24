class Packet:
    def __init__(self, label: str, quaternions: list[float], timestamp):
        self.timestamp = timestamp
        self.label = label

        self.quaternions = quaternions

    def __str__(self):
        quaternions_str = ' '.join([str(q) for q in self.quaternions])

        elements = [str(self.timestamp), self.label, quaternions_str]

        return ' '.join(elements)
