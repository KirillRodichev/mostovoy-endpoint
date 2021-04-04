import time

from src.constants.Constants import *
from src.model.Counter import Counter
from src.model.endpoint.Endpoint import Endpoint
from src.utils.TimeHelper import TimeHelper


def set_resp(success=False, data=None, error=''):
    return {
        SUCCESS: success,
        DATA: data,
        ERROR: error,
    }


class InformationTransmissionLine:

    def __init__(self, endpoints):
        self.endpoints = endpoints
        self.isBusy = False
        self.error = {}

    def set_busy_line(self, value, endpoint):
        self.isBusy = value
        endpoint.isBusy = value

    # command, [data, data ... data] (t1)=> response (t2)=>
    # returns None on error or current endpoint state
    def transfer_format1(self, command, data_array, endpoint):
        Counter.add_msg()
        if not self.isBusy:
            self.set_busy_line(True, endpoint)

            if command == COMMANDS[SEND_DATA]:
                Counter.add_word_delay()  # + 20 mcs - command word
                endpoint.accept_data(data_array)
                Counter.add_data_trans_delay()  # + 240 mcs - 12 data words
                response = endpoint.get_response()
            else:
                response = set_resp(False, None, INCOMPATIBLE_COMMAND_TYPE)

            Counter.add_word_delay()  # + 20 mcs - response word
            Counter.add_endpoint_resp_delay()  # + 12 mcs

            self.set_busy_line(False, endpoint)
            return response
        else:
            return set_resp(False, None, LINE_IS_BUSY)

    # command (t1)=> response, [data, data ... data] (t2)=>
    def transfer_format2(self, command, endpoint):
        data = None
        transfer_start = time.perf_counter()

        if command == COMMANDS[GET_DATA]:
            response = endpoint.get_response()
            if Endpoint.is_endpoint_ok(response):
                data = endpoint.get_data()
        else:
            data = None

        transfer_end = time.perf_counter()

        if TimeHelper.is_transaction_expired(transfer_end - transfer_start) or data is None:
            return None
        else:
            return data

    # command (t1)=> response (t2)=>
    def transfer_format4(command, endpoint):
        transfer_start = time.perf_counter()
        state = None

        if command == COMMANDS[GET_ANSWER]:
            state = endpoint.state
        elif command == COMMANDS[BLOCK]:
            endpoint.block()
        elif command == COMMANDS[RELEASE]:
            endpoint.release()
        elif command == COMMANDS[SWAP_LINE]:
            endpoint.swap_line()

        transfer_end = time.perf_counter()

        if TimeHelper.is_transaction_expired(transfer_end - transfer_start) or state is None:
            return None
        else:
            return state
