from src.mvc.model.endpoint.Endpoint import Endpoint


class PitchEndpoint(Endpoint):

    def __init__(self, angle, angular_velocity, angular_acceleration, transmitting_line, channel):
        super().__init__(transmitting_line, channel)
        self.angle = angle
        self.angular_velocity = angular_velocity
        self.angular_acceleration = angular_acceleration