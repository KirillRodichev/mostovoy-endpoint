from src.constants.Constants import *
from src.mvc.model.endpoint.Endpoint import Endpoint


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
