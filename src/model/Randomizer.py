import random

from src.constants.Constants import SESSION, PORTION


class Randomizer:

    @staticmethod
    def generate(step):
        msgs_numbers = []
        for i in range(0, SESSION, step):
            rand_from = i if i == 0 else i + 1
            msgs_numbers.append(random.randint(rand_from, i + step))

        return msgs_numbers

    @staticmethod
    # generates 10 breakdowns for a single session (20000 msgs) from intervals:
    # [0, 2000], [2001, 4000], ... [18001, 20000]
    def generate_breakdowns():
        Randomizer.generate(PORTION * 2)

    @staticmethod
    # generates 4 breakdowns for a single session (20000 msgs) from intervals:
    # [0, 5000], [5001, 10000], ... [15001, 20000]
    def generate_failure():
        Randomizer.generate(PORTION * 5)

    @staticmethod
    # generates 10 'line is busy' for a single session (20000 msgs) from intervals:
    # [0, 2000], [2001, 4000], ... [18001, 20000]
    def generate_is_busy():
        Randomizer.generate(PORTION * 2)

    @staticmethod
    # generates 1 or 0 'generating' for a single session (20000 msgs) from intervals:
    # 0 or 1
    def generate_generating():
        Randomizer.generate(SESSION)
