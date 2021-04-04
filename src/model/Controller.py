from src.constants.Constants import *
from src.model.InformationTransmissionLine import InformationTransmissionLine
from src.model.endpoint.Endpoint import Endpoint
from src.utils.TimeHelper import TimeHelper


class Controller(Endpoint):
    def __init__(self, transmission_line, endpoints, channel, transmitting_line=LINES[LINE_A]):
        super().__init__(transmitting_line, channel)
        # TODO: inheritance
        self.endpoints = endpoints
        self.transmission_line = transmission_line
        self.channel = channel

    def send_data(self, data_array, endpoint):
        command = COMMANDS[SEND_DATA]
        response = self.transmission_line.transfer_format1(command, data_array, endpoint)
        if response is not None and (not response[IS_BUSY] or not response[IS_FROZEN] or response[IS_FUNCTIONING]):
            return response
        else:
            return None

    # format 2
    def retrieve_data(self, endpoint_address):
        pass

    def test_mko(self):
        tested_line = LINES[LINE_A]
        has_generating_endpoint = False
        for endpoint in self.endpoints:
            endpoint_state = InformationTransmissionLine.transfer_format4(COMMANDS[GET_ANSWER], endpoint)
            if not endpoint_state[IS_FUNCTIONING] or endpoint_state is None:
                endpoint_state = InformationTransmissionLine.transfer_format4(COMMANDS[GET_ANSWER], endpoint)
            if not endpoint_state[IS_FUNCTIONING] or endpoint_state is None:
                has_generating_endpoint = True

        if has_generating_endpoint:
            for endpoint in self.endpoints:
                InformationTransmissionLine.transfer_format4(COMMANDS[BLOCK], endpoint)
            for endpoint in self.endpoints:
                InformationTransmissionLine.transfer_format4(COMMANDS[RELEASE], endpoint)
                endpoint_state = InformationTransmissionLine.transfer_format4(COMMANDS[GET_ANSWER], endpoint)
                if not endpoint_state[IS_FUNCTIONING]:
                    InformationTransmissionLine.transfer_format4(COMMANDS[BLOCK], endpoint)
                    InformationTransmissionLine.transfer_format4(COMMANDS[SWAP_LINE], endpoint)
