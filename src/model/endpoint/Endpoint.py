from src.constants.EndpointConstants import *
from src.utils.TimeHelper import TimeHelper

INIT_STATE = {
    IS_BUSY: False,
    IS_GENERATING: False,
    IS_FROZEN: False,
    IS_FUNCTIONING: True,
    IS_SERVICE_NEEDED: False,
}


class Endpoint:
    address = 0

    def __init__(self, channel, transmitting_line=LINES[LINE_A]):
        self.address += 1
        self.line = LINES[LINE_A]
        self.channel = channel
        self.transmitting_line = transmitting_line

        # endpoint initial characteristics
        self.characteristics = {
            CHARACTERISTICS[ANGLE]: 0,
            CHARACTERISTICS[ANGULAR_VELOCITY]: 0,
            CHARACTERISTICS[ANGULAR_ACCELERATION]: 0,
        }

        # Endpoint initial state
        self.state = {
            LINES[LINE_A]: INIT_STATE,
            LINES[LINE_B]: INIT_STATE,
        }

    # returns current endpoint state
    def get_response(self):
        if self.state[self.line][IS_BUSY] or self.state[self.line][IS_FROZEN] or not self.state[self.line][IS_FUNCTIONING]:
            TimeHelper.pause()
            return self.state[self.line]
        else:
            return self.state[self.line]

    def accept_data(self, data_array):
        self.characteristics = {
            CHARACTERISTICS[ANGLE]: 100,
            CHARACTERISTICS[ANGULAR_VELOCITY]: 100,
            CHARACTERISTICS[ANGULAR_ACCELERATION]: 100,
        }

    def get_data(self):
        return self.characteristics

    def block(self):
        self.state[self.line][IS_FROZEN] = True

    def release(self):
        self.state[self.line][IS_FROZEN] = False

    def swap_line(self):
        if self.line == LINES[LINE_A]:
            self.line = LINES[LINE_B]
        else:
            self.line = LINES[LINE_A]

    @staticmethod
    def is_endpoint_ok(state):
        return state == INIT_STATE
