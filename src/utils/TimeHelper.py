import time


class TimeHelper:

    @staticmethod
    def uslip(seconds):
        return time.sleep(seconds / 1000000)

    @staticmethod
    def sslip(seconds):
        return time.sleep(seconds)

    @staticmethod
    def to_microsecond(seconds):
        return seconds / 1000000

    @staticmethod
    def is_transaction_expired(time_diff):
        if time_diff > TimeHelper.to_microsecond(24):
            return True
        else:
            return False

    @staticmethod
    def pause():
        TimeHelper.uslip(12)
