from tabulate import tabulate

from src.constants.Constants import *
from src.mvc.model.Counter import Counter
from src.mvc.model.InformationTransmissionLine import InformationTransmissionLine
from src.mvc.model.Randomizer import Randomizer
from src.mvc.model.endpoint.Endpoint import Endpoint
from src.utils.ExcelExporter import ExcelExporter
from src.utils.Stats import Stats


def init_events():
    return {
        IS_BREAKDOWN: False,
        IS_FAILURE: False,
        IS_BUSY: False,
        IS_GENERATING: False,
    }


def stat_output(data, avg, standard_deviation, numbers, time_sum):
    print()
    print(tabulate(
        data,
        headers=HEADERS,
        tablefmt='orgtbl'
    ))
    print()
    print('Мат ожидание = ', avg)
    print('Среднеквадратическое  = ', standard_deviation)
    print()
    print("Всего событий 'Сбой': ", numbers[IS_BREAKDOWN])
    print("Всего событий 'Отказ ОУ': ", numbers[IS_FAILURE])
    print("Всего событий 'Абонент занят': ", numbers[IS_BUSY])
    print("Всего событий 'Генерация': ", numbers[IS_GENERATING])
    print()

    ExcelExporter.store_session_data(data, avg, standard_deviation, numbers, time_sum)


def insert_event_if_needed(begin, end, event_number, endpoint_state, event, event_type):
    if event_number and begin <= event_number[0] <= end:
        endpoint_state[event_type][endpoint_state[LINE]] = True
        event_number.pop(0)
        event[event_type] = True


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
        Counter.reset()

        randomizer = Randomizer()
        randomizer.generate_all()

        breakdown_numbers = randomizer.breakdowns if with_breakdowns else []
        failure_numbers = randomizer.failure if with_failure else []
        is_busy_numbers = randomizer.is_busy if with_is_busy else []
        generating_number = randomizer.generating if with_generating else []

        time_sum = 0
        endpoint_number = 0
        stat_data = []
        times = []

        numbers = {
            IS_BREAKDOWN: 0,
            IS_FAILURE: 0,
            IS_BUSY: 0,
            IS_GENERATING: 0,
        }

        for message_number in range(0, SESSION, PORTION):
            endpoint_number, had_breakdown, had_failure, had_is_busy, had_generating, time = self.start_portion(
                message_number,
                endpoint_number,
                breakdown_numbers,
                failure_numbers,
                is_busy_numbers,
                generating_number
            )
            # debugging
            # print(Counter.time)

            portion_stat_data = [
                PORTION,
                int(had_breakdown),
                int(had_failure),
                int(had_is_busy),
                int(had_generating),
                time
            ]
            stat_data.append(portion_stat_data)
            times.append(time)
            time_sum += time

            if had_breakdown:
                numbers[IS_BREAKDOWN] += 1
            if had_failure:
                numbers[IS_FAILURE] += 1
            if had_is_busy:
                numbers[IS_BUSY] += 1
            if had_generating:
                numbers[IS_GENERATING] += 1

        avg = Stats.get_avg(times)
        standard_deviation = Stats.get_standard_deviation(times)
        stat_output(stat_data, avg, standard_deviation, numbers, time_sum)

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
        event = init_events()
        start = Counter.time

        for i in range(begin, end):
            endpoint = self.endpoints[endpoint_number]
            endpoint_state = self.endpoints[endpoint_number].state

            insert_event_if_needed(begin, end, breakdown_numbers, endpoint_state, event, IS_BREAKDOWN)
            insert_event_if_needed(begin, end, failure_numbers, endpoint_state, event, IS_FAILURE)
            insert_event_if_needed(begin, end, is_busy_numbers, endpoint_state, event, IS_BUSY)
            insert_event_if_needed(begin, end, generating_number, endpoint_state, event, IS_GENERATING)

            self.send_data_to_eo([], endpoint)
            endpoint_number = (endpoint_number + 1) % (ENDPOINTS_COUNT - 1)

        finish = Counter.time

        return (
            endpoint_number,
            event[IS_BREAKDOWN],
            event[IS_FAILURE],
            event[IS_BUSY],
            event[IS_GENERATING],
            finish - start
        )
