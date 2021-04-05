from src.constants.Constants import *
from src.mvc.controller.EndpointController import Controller
from src.mvc.model.Counter import Counter
from src.mvc.model.InformationTransmissionLine import InformationTransmissionLine
from src.mvc.controller.MainController import MainController
from src.mvc.model.Randomizer import Randomizer


def main():
    try:
        print('Hello MOSTOVOY!')

        main_controller = MainController()
        endpoints = main_controller.generate_endpoints()

        line = InformationTransmissionLine(endpoints)
        controller = Controller(line, endpoints, CHANNELS[CHANNEL_PITCH])

        # controller.start_session(False, False, False, False)
        # print(Counter.time, '\n')
        # Counter.time = 0
        # controller.start_session(True, False, False, False)
        # print(Counter.time, '\n')
        # Counter.time = 0
        # controller.start_session(False, True, False, False)
        # print(Counter.time, '\n')
        # Counter.time = 0
        controller.start_session(False, False, True, False)
        print(Counter.time, '\n')

    except RuntimeError as err:
        print(err)


if __name__ == '__main__':
    main()
