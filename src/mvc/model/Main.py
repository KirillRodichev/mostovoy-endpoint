from src.constants.Constants import *
from src.mvc.controller.EndpointController import Controller
from src.mvc.model.InformationTransmissionLine import InformationTransmissionLine
from src.mvc.controller.MainController import MainController


def main():
    try:
        print('Hello MOSTOVOY!')

        main_controller = MainController()
        endpoints = main_controller.generate_endpoints()

        line = InformationTransmissionLine(endpoints)
        controller = Controller(line, endpoints, CHANNELS[CHANNEL_PITCH])

        data_arr = []

        for i in range(10):
            controller.send_data_to_eo(data_arr, endpoints[i])

    except RuntimeError as err:
        print(err)


if __name__ == '__main__':
    main()
