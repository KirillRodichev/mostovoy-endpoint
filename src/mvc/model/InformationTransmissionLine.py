from src.constants.Constants import *
from src.mvc.model.Counter import Counter


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

    def set_busy_line(self, value, endpoint):
        self.isBusy = value
        endpoint.isBusy = value

    # command, [data, data ... data] (t1)=> response (t2)=>
    # returns None on error or current endpoint state
    def transfer_format1(self, command, data_array, endpoint):
        Counter.add_msg()
        self.set_busy_line(True, endpoint)

        if command == COMMANDS[SEND_DATA]:
            endpoint.accept_data(data_array)
            response = endpoint.get_response()

        else:
            raise RuntimeError(INCOMPATIBLE_COMMAND_TYPE)

        self.set_busy_line(False, endpoint)
        if response is not None:
            return set_resp(True, response, '')
        else:
            return set_resp(False, response, NO_RESPONSE)

    # command (t1)=> response (t2)=>
    def transfer_format4(self, command, endpoint):
        Counter.add_msg()

        if command == COMMANDS[GET_ANSWER]:
            response = endpoint.get_response()
        elif command == COMMANDS[BLOCK]:
            response = endpoint.block()
        elif command == COMMANDS[RELEASE]:
            response = endpoint.release()
        elif command == COMMANDS[SWAP_LINE]:
            response = endpoint.swap_line()
        else:
            raise RuntimeError(INCOMPATIBLE_COMMAND_TYPE)

        self.set_busy_line(False, endpoint)
        if response is not None:
            return set_resp(True, response, '')
        else:
            return set_resp(False, response, NO_RESPONSE)
