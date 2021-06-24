class Packet:
    def __init__(self, label: str, quaternion: list[float], timestamp):
        self.timestamp = timestamp
        self.label = label

        self.quaternion = quaternion

    def __str__(self):
        quaternion_str = ' '.join([str(q) for q in self.quaternion])

        elements = [str(self.timestamp), self.label, quaternion_str]

        return ' '.join(elements)
