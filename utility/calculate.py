import random
import constants


def random_non_repeating(min, max, old):
    while True:
        current = random.randint(min, max)
        if not old == current:
            return current


def rand_non_repeat_agent(old):
    agent_num = len(constants.user_agents)
    return random_non_repeating(0, agent_num - 1, old)