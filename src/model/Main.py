import time

from src.constants.Constants import *
from src.model.Controller import Controller
from src.model.InformationTransmissionLine import InformationTransmissionLine
from src.model.endpoint.Endpoint import Endpoint
from src.utils.TimeHelper import TimeHelper


def main():
    print('Hello MOSTOVOY!')

    for i in range(10):
        transfer_start = time.perf_counter()
        TimeHelper.sslip(1)
        transfer_end = time.perf_counter()

        print(transfer_end - transfer_start)

    # ep_pitch_1 = Endpoint(CHANNELS[CHANNEL_PITCH])
    # ep_pitch_2 = Endpoint(CHANNELS[CHANNEL_PITCH])
    # ep_pitch_3 = Endpoint(CHANNELS[CHANNEL_PITCH])
    #
    # ep_yaw_1 = Endpoint(CHANNELS[CHANNEL_YAW])
    # ep_yaw_2 = Endpoint(CHANNELS[CHANNEL_YAW])
    # ep_yaw_3 = Endpoint(CHANNELS[CHANNEL_YAW])
    #
    # ep_roll_1 = Endpoint(CHANNELS[CHANNEL_ROLL])
    # ep_roll_2 = Endpoint(CHANNELS[CHANNEL_ROLL])
    # ep_roll_3 = Endpoint(CHANNELS[CHANNEL_ROLL])
    #
    # endpoints = [ep_pitch_1, ep_pitch_2, ep_pitch_3, ep_roll_1, ep_roll_2, ep_roll_3, ep_yaw_1, ep_yaw_2, ep_yaw_3]
    #
    # line = InformationTransmissionLine(endpoints)
    # controller = Controller(line, endpoints, CHANNELS[CHANNEL_PITCH])
    #
    # data_arr = []
    # for i in range(12):
    #     data_arr.append({
    #         CHARACTERISTICS[ANGLE]: 150 + i,
    #         CHARACTERISTICS[ANGULAR_VELOCITY]: 100 + i,
    #         CHARACTERISTICS[ANGULAR_ACCELERATION]: 250 + i,
    #     })
    #
    # controller.send_data(data_arr, ep_roll_1)


if __name__ == '__main__':
    main()
