import random


def random_non_repeating(min, max, old):
    while True:
        current = random.randint(min, max)
        if not old == current:
            return current
