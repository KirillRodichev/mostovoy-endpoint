import numpy as np


class Stats:

    @staticmethod
    def get_avg(data_list):
        data_arr = np.array(data_list)
        return data_arr.sum() / data_arr.size

    @staticmethod
    def get_standard_deviation(data_list):
        return np.std(data_list)