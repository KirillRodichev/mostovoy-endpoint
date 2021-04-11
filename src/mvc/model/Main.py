from src.constants.Constants import *
from src.mvc.controller.EndpointController import Controller
from src.mvc.controller.MainController import MainController
from src.mvc.model.InformationTransmissionLine import InformationTransmissionLine
from src.utils.ExcelExporter import ExcelExporter


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
