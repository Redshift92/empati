
def illumination_system_env_valence(self):
    sum_valence = 0
    for neighbour in self.neighbours:
        sum_valence += neighbour.state[0]
    return sum_valence/len(self.neighbours)

def illumination_system_env_arousal(self):
    sum_arousal = 0
    for neighbour in self.neighbours:
        sum_arousal += neighbour.state[1]
    return sum_arousal/len(self.neighbours)
