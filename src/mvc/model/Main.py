from src.constants.Constants import *
from src.mvc.controller.EndpointController import Controller
from src.mvc.model.InformationTransmissionLine import InformationTransmissionLine
from src.mvc.model.endpoint.Endpoint import Endpoint
from src.utils.ExcelExporter import ExcelExporter


class MainController:

    def __init__(self):
        self.endpoints = []

    def generate_endpoints(self):
        self.endpoints = []
        for i in range(ENDPOINTS_COUNT):
            if 0 <= i < 6:
                self.endpoints.append(Endpoint(CHANNEL_PITCH))
            elif 6 <= i < 12:
                self.endpoints.append(Endpoint(CHANNEL_YAW))
            elif 12 <= i < 18:
                self.endpoints.append(Endpoint(CHANNEL_ROLL))

        return self.endpoints


def main():
    try:
        main_controller = MainController()

        for i in range(TESTS_NUMBER):
            endpoints = main_controller.generate_endpoints()
            line = InformationTransmissionLine(endpoints)
            controller = Controller(line, endpoints, CHANNELS[CHANNEL_PITCH])
            controller.start_session(
                with_breakdowns=True,
                with_failure=True,
                with_is_busy=True,
                with_generating=True
            )

        ExcelExporter.export_stored_data()

    except RuntimeError as err:
        print(err)


if __name__ == '__main__':
    main()
