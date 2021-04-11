from tabulate import tabulate

from src.constants.Constants import *
from src.mvc.model.Counter import Counter
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


def print_stat(data, avg, standard_deviation, numbers):
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


def stat_output(data, avg, standard_deviation, numbers, time_sum):
    print_stat(data, avg, standard_deviation, numbers)
    ExcelExporter.store_session_data(data, avg, standard_deviation, numbers, time_sum)


class Controller(Endpoint):
    def __init__(self, transmission_line, endpoints, channel, line=LINES[LINE_A]):
        super().__init__(channel, line)

        self.endpoints = endpoints
        self.transmission_line = transmission_line
        self.channel = channel

    def send_data_to_eo(self, data_array, endpoint):
        swapped = False
        response = self.transmission_line.transfer_format1(COMMANDS[SEND_DATA], data_array, endpoint)
        if not response[SUCCESS] and response[ERROR] == NO_RESPONSE:
            response = self.transmission_line.transfer_format1(COMMANDS[SEND_DATA], data_array, endpoint)
        if not response[SUCCESS] and response[ERROR] == NO_RESPONSE:
            endpoint.swap_line()
            swapped = True
            response = self.transmission_line.transfer_format1(COMMANDS[SEND_DATA], data_array, endpoint)
        if not response[SUCCESS] and response[ERROR] == NO_RESPONSE:
            response = self.transmission_line.transfer_format1(COMMANDS[SEND_DATA], data_array, endpoint)
        if not response[SUCCESS] and response[ERROR] == NO_RESPONSE:
            # endpoint is not responding on both lines
            pass
        elif response[SUCCESS]:
            pass
        if swapped:
            endpoint.swap_line()
        return response  # for debugging

    def test_mko(self):
        has_generating_endpoint = False
        for endpoint in self.endpoints:
            response = self.transmission_line.transfer_format4(COMMANDS[GET_ANSWER], endpoint)
            if not response[SUCCESS] and response[ERROR] == NO_RESPONSE:
                response = self.transmission_line.transfer_format4(COMMANDS[GET_ANSWER], endpoint)
            if not response[SUCCESS] and response[ERROR] == NO_RESPONSE:
                has_generating_endpoint = True

        if has_generating_endpoint:
            # block all endpoints
            for endpoint in self.endpoints:
                self.transmission_line.transfer_format4(COMMANDS[SWAP_LINE], endpoint)  # to B
                self.transmission_line.transfer_format4(COMMANDS[BLOCK_THROUGH], endpoint)  # block on A
                self.transmission_line.set_has_generation(False)

            # release endpoints one by one
            for endpoint in self.endpoints:
                is_generating_blocked = False
                self.transmission_line.transfer_format4(COMMANDS[RELEASE_THROUGH], endpoint)  # release on A
                self.transmission_line.transfer_format4(COMMANDS[SWAP_LINE], endpoint)  # to A
                # continue asking if generating is not found
                if not is_generating_blocked:
                    response = self.transmission_line.transfer_format4(COMMANDS[GET_ANSWER], endpoint)
                    # if no response after endpoint release then it's been generating
                    if not response[SUCCESS] and response[ERROR] == NO_RESPONSE:
                        self.transmission_line.transfer_format4(COMMANDS[SWAP_LINE], endpoint)  # to B
                        self.transmission_line.transfer_format4(COMMANDS[BLOCK_THROUGH], endpoint)  # block on A
                        endpoint.state[IS_FAILURE][LINE_A] = True  # imitate block as if it's a failure
                        self.transmission_line.transfer_format4(COMMANDS[SWAP_LINE], endpoint)  # back to A
                        is_generating_blocked = True
                        endpoint.state[IS_GENERATING][LINE_A] = False  # return to initial setup

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

        breakdown_numbers = randomizer.breakdowns
        failure_numbers = randomizer.failure
        is_busy_numbers = randomizer.is_busy
        generating_endpoint_number = randomizer.generating

        time_sum = 0
        stat_data = []
        times = []

        numbers = {
            IS_BREAKDOWN: 0,
            IS_FAILURE: 0,
            IS_BUSY: 0,
            IS_GENERATING: 0,
        }

        for message_number in range(0, SESSION, PORTION):
            # print('************************portion************************')
            had_breakdown, had_failure, had_is_busy, had_generating, time = self.start_portion(
                message_number,
                breakdown_numbers,
                failure_numbers,
                is_busy_numbers,
                generating_endpoint_number
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
            breakdown_numbers,
            failure_numbers,
            is_busy_numbers,
            generating_endpoint_number
    ):
        endpoint_number = 0
        end = begin + PORTION
        event = init_events()
        start = Counter.time

        if generating_endpoint_number != -1 and begin == 0:
            event[IS_GENERATING] = True
            self.transmission_line.set_has_generation(True)
            endpoint_state = self.endpoints[generating_endpoint_number].state
            endpoint_state[IS_GENERATING][LINE_A] = True
            self.test_mko()

        for i in range(begin, end):
            # trans_data_start = Counter.time

            self.insert_event_if_needed(breakdown_numbers, endpoint_number, event, IS_BREAKDOWN, i)
            self.insert_event_if_needed(failure_numbers, endpoint_number, event, IS_FAILURE, i, begin, end)
            self.insert_event_if_needed(is_busy_numbers, endpoint_number, event, IS_BUSY, i)

            self.send_data_to_eo([], self.endpoints[endpoint_number])
            # print(endpoint_number)
            # if Counter.time - trans_data_start == 836:
            #     print(i, endpoint_number, Counter.time - trans_data_start)
            endpoint_number = (endpoint_number + 1) % ENDPOINTS_COUNT

        finish = Counter.time

        # debugging
        # self.print_endpoint_states(begin // PORTION)

        return (
            event[IS_BREAKDOWN],
            event[IS_FAILURE],
            event[IS_BUSY],
            event[IS_GENERATING],
            finish - start
        )

    def insert_event_if_needed(self, event_numbers, endpoint_number, event, event_type, iteration, begin=0, end=0):
        if (
            event_numbers and (
                (event_numbers[0] == iteration) or
                (event_type == IS_FAILURE and begin <= event_numbers[0] <= end)
            )
        ):
            # костыльный if из-за Моста
            if event_type == IS_FAILURE:
                endpoint_number = event_numbers[0] % ENDPOINTS_COUNT
            endpoint_state = self.endpoints[endpoint_number].state
            endpoint_state[event_type][endpoint_state[LINE]] = True
            event_numbers.pop(0)
            event[event_type] = True

    def print_endpoint_states(self, iteration):
        data = [[
            'LINE',
            'IS_BUSY LINE_A',
            'IS_BUSY LINE_B',
            'IS_BREAKDOWN LINE_A',
            'IS_BREAKDOWN LINE_B',
            'IS_FAILURE LINE_A',
            'IS_FAILURE LINE_B',
            'IS_GENERATING LINE_A',
            'IS_GENERATING LINE_B'
        ]]
        headers = [
            'Состояния ' + str(iteration)
        ]
        for i in range(len(self.endpoints)):
            headers.append('ОУ ' + str(i))
            data.append([
                'A' if self.endpoints[i].state[LINE] == LINE_A else 'B',
                int(self.endpoints[i].state[IS_BUSY][LINE_A]),
                int(self.endpoints[i].state[IS_BUSY][LINE_B]),
                int(self.endpoints[i].state[IS_BREAKDOWN][LINE_A]),
                int(self.endpoints[i].state[IS_BREAKDOWN][LINE_B]),
                int(self.endpoints[i].state[IS_FAILURE][LINE_A]),
                int(self.endpoints[i].state[IS_FAILURE][LINE_B]),
                int(self.endpoints[i].state[IS_GENERATING][LINE_A]),
                int(self.endpoints[i].state[IS_GENERATING][LINE_B])
            ])

        print(tabulate(
            list(zip(*data)),
            headers=headers,
            tablefmt='orgtbl'
        ))
        print()
