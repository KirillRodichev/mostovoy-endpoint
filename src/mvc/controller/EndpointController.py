from src.constants.Constants import *
from src.mvc.model.Counter import Counter
from src.mvc.model.InformationTransmissionLine import InformationTransmissionLine
from src.mvc.model.Randomizer import Randomizer
from src.mvc.model.endpoint.Endpoint import Endpoint


class Controller(Endpoint):
    def __init__(self, transmission_line, endpoints, channel, line=LINES[LINE_A]):
        super().__init__(channel, line)
        # TODO: inheritance
        self.endpoints = endpoints
        self.transmission_line = transmission_line
        self.channel = channel

    def send_data_to_eo(self, data_array, endpoint):
        response = self.transmission_line.transfer_format1(COMMANDS[SEND_DATA], data_array, endpoint)
        if not response[SUCCESS] and response[ERROR] == NO_RESPONSE:
            response = self.transmission_line.transfer_format1(COMMANDS[SEND_DATA], data_array, endpoint)
        if not response[SUCCESS] and response[ERROR] == NO_RESPONSE:
            endpoint.swap_line()
            response = self.transmission_line.transfer_format1(COMMANDS[SEND_DATA], data_array, endpoint)
        if not response[SUCCESS] and response[ERROR] == NO_RESPONSE:
            response = self.transmission_line.transfer_format1(COMMANDS[SEND_DATA], data_array, endpoint)
        if not response[SUCCESS] and response[ERROR] == NO_RESPONSE:
            # endpoint is not responding on both lines
            pass
        elif response[SUCCESS]:
            pass
        return response  # for debugging

    def test_mko(self):
        has_generating_endpoint = False
        for endpoint in self.endpoints:
            response = InformationTransmissionLine.transfer_format4(COMMANDS[GET_ANSWER], endpoint)
            if not response[SUCCESS] and response[ERROR] == NO_RESPONSE:
                response = InformationTransmissionLine.transfer_format4(COMMANDS[GET_ANSWER], endpoint)
            if not response[SUCCESS] and response[ERROR] == NO_RESPONSE:
                has_generating_endpoint = True

        if has_generating_endpoint:
            for endpoint in self.endpoints:
                InformationTransmissionLine.transfer_format4(COMMANDS[SWAP_LINE], endpoint)  # to B
                InformationTransmissionLine.transfer_format4(COMMANDS[BLOCK], endpoint)

            for endpoint in self.endpoints:
                InformationTransmissionLine.transfer_format4(COMMANDS[RELEASE], endpoint)
                InformationTransmissionLine.transfer_format4(COMMANDS[SWAP_LINE], endpoint)  # to A
                response = InformationTransmissionLine.transfer_format4(COMMANDS[GET_ANSWER], endpoint)
                if not response[SUCCESS] and response[ERROR] == NO_RESPONSE:
                    InformationTransmissionLine.transfer_format4(COMMANDS[SWAP_LINE], endpoint)  # to B
                    InformationTransmissionLine.transfer_format4(COMMANDS[BLOCK], endpoint)
                    InformationTransmissionLine.transfer_format4(COMMANDS[SWAP_LINE], endpoint)

    def start_session(
            self,
            with_breakdowns=True,
            with_failure=True,
            with_is_busy=True,
            with_generating=True
    ):
        randomizer = Randomizer()
        randomizer.generate_all()

        breakdown_numbers = randomizer.breakdowns if with_breakdowns else []
        failure_numbers = randomizer.failure if with_failure else []
        is_busy_numbers = randomizer.is_busy if with_is_busy else []
        generating_number = randomizer.generating if with_generating else []

        # debugging
        print('breakdown_numbers = ', breakdown_numbers)
        print('failure_numbers = ', failure_numbers)
        print('is_busy_numbers = ', is_busy_numbers)
        print('generating_number = ', generating_number)

        endpoint_number = 0

        for message_number in range(0, SESSION, PORTION):
            endpoint_number = self.start_portion(
                message_number,
                endpoint_number,
                breakdown_numbers,
                failure_numbers,
                is_busy_numbers,
                generating_number
            )
            # debugging
            # print(Counter.time)

    def start_portion(
            self,
            begin,
            endpoint_number,
            breakdown_numbers,
            failure_numbers,
            is_busy_numbers,
            generating_number
    ):
        end = begin + PORTION
        for i in range(begin, end):
            endpoint = self.endpoints[endpoint_number]
            endpoint_state = self.endpoints[endpoint_number].state
            if breakdown_numbers and begin <= breakdown_numbers[0] <= end:
                endpoint_state[IS_BREAKDOWN] = True
                breakdown_numbers.pop(0)
            if failure_numbers and begin <= failure_numbers[0] <= end:
                endpoint_state[IS_FAILURE] = True
                failure_numbers.pop(0)
            if is_busy_numbers and begin <= is_busy_numbers[0] <= end:
                endpoint_state[endpoint_state[LINE]][IS_BUSY] = True
                is_busy_numbers.pop(0)
            if generating_number and begin <= generating_number[0] <= end:
                endpoint_state[endpoint_state[LINE]][IS_GENERATING] = True
                generating_number.pop(0)

            # debugging
            # if begin == 0:
            #     print(Counter.time / 292)

            self.send_data_to_eo([], endpoint)
            endpoint_number = (endpoint_number + 1) % (ENDPOINTS_COUNT - 1)

        return endpoint_number
