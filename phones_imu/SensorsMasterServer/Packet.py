class Packet:
    def __init__(self, label: str, quaternions: list[float], timestamp):
        self.label = label

        # Zamień w kwaternionach oś Y i Z - "obrócimy" w ten sposób telefon
        self.quaternions = quaternions
        self.timestamp = timestamp
