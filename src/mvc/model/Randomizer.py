import random

from src.constants.Constants import SESSION, PORTION


class Randomizer:

    @staticmethod
    def generate(step):
        msgs_numbers = []
        for i in range(0, SESSION, step):
            msgs_numbers.append(random.randint(i, i + step))

        return msgs_numbers

    @staticmethod
    # generates 10 breakdowns for a single session (20000 msgs) from intervals:
    # [0, 1999], [2000, 3999], ... [17999, 19999]
    def generate_breakdowns():
        Randomizer.generate(PORTION * 2)

    @staticmethod
    # generates 4 breakdowns for a single session (20000 msgs) from intervals:
    # [0, 4999], [5000, 9999], ... [15000, 19999]
    def generate_failure():
        Randomizer.generate(PORTION * 5)

    @staticmethod
    # generates 10 'line is busy' for a single session (20000 msgs) from intervals:
    # [0, 1999], [2000, 3999], ... [17999, 19999]
    def generate_is_busy():
        Randomizer.generate(PORTION * 2)

    @staticmethod
    # generates 1 or 0 'generating' for a single session (20000 msgs) from intervals:
    # 0 or 1
    def generate_generating():
        Randomizer.generate(SESSION)
