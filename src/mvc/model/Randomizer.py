import random

from src.constants.Constants import SESSION, PORTION


def generate(step, excluded_values):
    msgs_numbers = []
    for i in range(0, SESSION, step):
        msgs_numbers.append(random.choice([i for i in range(i, i + step) if i not in excluded_values]))

    return msgs_numbers


class Randomizer:

    def __init__(self):
        self.breakdowns = []
        self.failure = []
        self.is_busy = []
        self.generating = []

    def generate_all(self):
        self.generate_breakdowns()
        self.generate_failure()
        self.generate_is_busy()
        self.generate_generating()

    # generates 10 breakdowns for a single session (20000 msgs) from intervals:
    # [0, 1999], [2000, 3999], ... [17999, 19999]
    def generate_breakdowns(self):
        excluded_values = self.failure + self.is_busy + self.generating
        self.breakdowns = generate(PORTION * 2, excluded_values)

    # generates 4 breakdowns for a single session (20000 msgs) from intervals:
    # [0, 4999], [5000, 9999], ... [15000, 19999]
    def generate_failure(self):
        excluded_values = self.breakdowns + self.is_busy + self.generating
        self.failure = generate(PORTION * 5, excluded_values)

    # generates 10 'line is busy' for a single session (20000 msgs) from intervals:
    # [0, 1999], [2000, 3999], ... [17999, 19999]
    def generate_is_busy(self):
        excluded_values = self.breakdowns + self.failure + self.generating
        self.is_busy = generate(PORTION * 2, excluded_values)

    # generates 1 or 0 'generating' for a single session (20000 msgs) from intervals:
    # 0 or 1
    def generate_generating(self):
        excluded_values = self.breakdowns + self.is_busy + self.failure
        self.generating = generate(SESSION, excluded_values)
