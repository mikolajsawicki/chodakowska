class Packet:
    def __init__(self, label: str, quaternions: list[float], timestamp):
        self.label = label
        self.quaternions = quaternions
        self.timestamp = timestamp
