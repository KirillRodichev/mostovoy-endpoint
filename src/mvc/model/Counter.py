ENDPOINT_RESP_DELAY = 12
END_OF_DATA_TRANS_DELAY = 20
WORD_DELAY = 20
IS_BUSY_DELAY = 1000


class Counter:
    time = 0
    messages = 0

    @staticmethod
    def add_word_delay():
        Counter.time += WORD_DELAY

    @staticmethod
    def add_data_trans_delay():
        Counter.time += WORD_DELAY * 12

    @staticmethod
    def add_endpoint_resp_delay():
        Counter.time += ENDPOINT_RESP_DELAY

    @staticmethod
    def add_end_of_trans_delay():
        Counter.time += END_OF_DATA_TRANS_DELAY

    @staticmethod
    def add_is_busy_delay():
        Counter.time += IS_BUSY_DELAY

    @staticmethod
    def add_msg():
        Counter.messages += 1

    @staticmethod
    def reset():
        Counter.time = 0
