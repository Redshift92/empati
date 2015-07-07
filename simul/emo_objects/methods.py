
def env_valence(self):
    sum_valence = 0
    for neighbour in self.neighbours:
        sum_valence += neighbour.state[0]
    return sum_valence/len(self.neighbours)

def env_arousal(self):
    sum_arousal = 0
    for neighbour in self.neighbours:
        sum_arousal += neighbour.state[1]
    return sum_arousal/len(self.neighbours)

def dark_object_env_valence(self):
    return env_valence(self)

def dark_object_env_arousal(self):
    return env_arousal(self)

def artist_object_env_valence(self):
    return env_valence(self)

def artist_object_env_arousal(self):
    return env_arousal(self)
