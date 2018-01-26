
def permissions(states):
    return tuple((state[1], 'Can save as {}'.format(state[1])) for state in states)
