import random
import string


def generate_permutation(n: int) -> list[int]:
    a = [i for i in range(0, n)]
    random.shuffle(a)
    return a


def random_label():
    return random_string(10)


def random_string(length: int):
    return 'L' + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))
