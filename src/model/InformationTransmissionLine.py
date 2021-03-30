import time

from src.constants.EndpointConstants import *
from src.model.endpoint.Endpoint import Endpoint
from src.utils.TimeHelper import TimeHelper


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
        if not self.isBusy:
            self.set_busy_line(True, endpoint)

            if command == COMMANDS[SEND_DATA]:
                endpoint.accept_data(data_array)
                transfer_start = time.perf_counter()
                TimeHelper.pause()
                response = endpoint.get_response()
            else:
                transfer_start = time.perf_counter()
                response = None

            transfer_end = time.perf_counter()

            if TimeHelper.is_transaction_expired(transfer_end - transfer_start) or response is None:
                response = None

            self.set_busy_line(False, endpoint)
            return response
        else:
            return None

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
