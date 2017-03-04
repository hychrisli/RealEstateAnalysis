from random import randint
import constants


def random_non_repeating(min_val, max_val, old):
    while True:
        current = randint(min_val, max_val)
        if not old == current:
            return current


def rand_non_repeat_agent(old):
    agent_num = len(constants.user_agents)
    return random_non_repeating(0, agent_num - 1, old)


def rand_batch_end_num(start_num, total_num, min_size=2, max_size=7):
    batch_size = randint(min_size, max_size)
    end_num = start_num + batch_size
    if end_num > total_num:
        end_num = total_num

    print ("Batch size: " + str(batch_size) +
           " | start: " + str(start_num) +
           " | end: " + str(end_num))

    return end_num


def rand_batch_size(min_size=2, max_size=7):
    batch_size = randint(min_size, max_size)
    print ("Batch size: " + str(batch_size))
    return batch_size
