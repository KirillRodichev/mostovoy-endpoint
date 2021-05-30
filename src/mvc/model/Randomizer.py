import random

from src.constants.Constants import SESSION, PORTION, ENDPOINTS_COUNT

PROB_05 = [True, False]
PROB_02 = [True, False, False, False, False]


class Randomizer:

    def __init__(self):
        self.breakdowns = []
        self.failure = []
        self.endpoints_in_failure = [0] * ENDPOINTS_COUNT
        self.is_busy = []
        self.generating = -1

    def generate_all(self):
        self.generate_breakdowns()
        self.generate_failure()
        self.generate_is_busy()
        self.generate_generating()

    # generates 10 breakdowns for a single session (20000 msgs) from intervals:
    # [0, 1999], [2000, 3999], ... [17999, 19999]
    def generate_breakdowns(self):
        excluded_values = self.failure + self.is_busy
        self.breakdowns = self.generate(PROB_05, excluded_values)

    # generates 4 breakdowns for a single session (20000 msgs) from intervals:
    # [0, 4999], [5000, 9999], ... [15000, 19999]
    def generate_failure(self):
        excluded_values = self.breakdowns + self.is_busy
        self.failure = self.generate(PROB_02, excluded_values, is_failure=True)

    # generates 10 'line is busy' for a single session (20000 msgs) from intervals:
    # [0, 1999], [2000, 3999], ... [17999, 19999]
    def generate_is_busy(self):
        excluded_values = self.breakdowns + self.failure
        self.is_busy = self.generate(PROB_05, excluded_values)

    # generates 1 or 0 'generating' for a single session (20000 msgs) from intervals:
    # 0 or 1
    def generate_generating(self):
        if random.choice(PROB_05):
            self.generating = random.choice([j for j in range(ENDPOINTS_COUNT) if not self.endpoints_in_failure[j]])

    def generate(self, probability, excluded_values, is_failure=False):
        msgs_numbers = []
        for i in range(0, SESSION, PORTION):
            if random.choice(probability):
                if is_failure:
                    rand_num = random.choice([j for j in range(i, i + PORTION) if (
                            j not in excluded_values and not self.endpoints_in_failure[j % (ENDPOINTS_COUNT - 1)]
                    )])
                    msgs_numbers.append(rand_num)
                    self.endpoints_in_failure[rand_num % (ENDPOINTS_COUNT - 1)] = 1
                else:
                    msgs_numbers.append(random.choice([j for j in range(i, i + PORTION) if j not in excluded_values]))

        return msgs_numbers
