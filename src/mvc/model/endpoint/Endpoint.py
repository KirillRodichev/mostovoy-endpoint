from src.constants.Constants import *
from src.mvc.model.Counter import Counter

INIT_STATE = {
    LINE: LINE_A,
    IS_BUSY: {
        LINE_A: False,
        LINE_B: False,
    },
    IS_FROZEN: {  # controller freezes endpoint when it's generating
        LINE_A: False,
        LINE_B: False,
    },
    IS_SERVICE_NEEDED: {
        LINE_A: False,
        LINE_B: False,
    },
    IS_GENERATING: {
        LINE_A: False,
        LINE_B: False,
    },
    IS_BREAKDOWN: {
        LINE_A: False,
        LINE_B: False,
    },
    IS_FAILURE: {
        LINE_A: False,
        LINE_B: False,
    },
}


class Endpoint:
    address = 0

    def __init__(self, channel, transmitting_line=LINES[LINE_A]):
        Endpoint.address += 1
        self.channel = channel

        # endpoint initial characteristics
        self.characteristics = {
            CHARACTERISTICS[ANGLE]: 0,
            CHARACTERISTICS[ANGULAR_VELOCITY]: 0,
            CHARACTERISTICS[ANGULAR_ACCELERATION]: 0,
        }

        # Endpoint initial state
        self.state = INIT_STATE
        self.state[LINE] = transmitting_line

    # returns current endpoint state
    def get_response(self):
        Counter.add_endpoint_resp_delay()  # + 12 mcs
        if self.is_functioning():
            Counter.add_word_delay()  # + 20 mcs - response word
            return self.state
        else:
            if self.state[IS_BREAKDOWN][self.state[LINE]] is True:
                self.state[IS_BREAKDOWN][self.state[LINE]] = False
            if self.state[IS_BUSY][self.state[LINE]] is True:
                self.state[IS_BUSY][self.state[LINE]] = False
                Counter.add_word_delay()
                Counter.add_is_busy_delay()
            return None

    def accept_data(self, data_array):
        Counter.add_word_delay()  # + 20 mcs - accept data command word
        Counter.add_data_trans_delay()  # + 240 mcs - 12 data messages
        # TODO: process data array if needed

    def block(self):
        if self.is_functioning():
            Counter.add_word_delay()  # + 20 mcs - command word
            self.state[IS_FROZEN][self.state[LINE]] = True
            return self.get_response()
        else:
            return None

    def block_through(self):
        opposite_line = LINE_A if self.state[LINE] == LINE_B else LINE_B
        if self.is_functioning(opposite_line):
            self.state[IS_FROZEN][opposite_line] = False
            return self.get_response()
        else:
            return None

    def release(self):
        Counter.add_word_delay()  # + 20 mcs - command word
        if self.is_functioning():
            self.state[IS_FROZEN][self.state[LINE]] = False
            return self.get_response()
        else:
            return None

    def swap_line(self):
        if self.state[LINE] == LINE_A:
            self.state[LINE] = LINE_B
        else:
            self.state[LINE] = LINE_A

    def is_functioning(self, line=''):
        if not line:
            line = self.state[LINE]
        return not (
                self.state[IS_BREAKDOWN][line] or
                self.state[IS_FAILURE][line] or
                self.state[IS_GENERATING][line] or
                self.state[IS_BUSY][line]
        )
