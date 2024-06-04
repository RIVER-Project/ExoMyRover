# Mock Servo classes for testing

class MockServo:
    def __init__(self, channel):
        self.channel = channel
        self.angle = None
        self.servo180_1 = None
        self.servo180_2 = None

    def set_pulse_width_range(self, servo180_1, servo180_2):
        self.servo180_1 = servo180_1
        self.servo180_2 = servo180_2
        print(f"MockServo {self.channel}: Pulse width range set to ({servo180_1}, {servo180_2})")

    def move_to_angle(self, angle):
        self.angle = angle
        print(f"MockServo {self.channel}: Moved to angle {angle}")

class MockContinuousServo:
    def __init__(self, channel):
        self.channel = channel
        self.throttle = None

    def set_throttle(self, throttle):
        self.throttle = throttle
        print(f"MockContinuousServo {self.channel}: Throttle set to {throttle}")

class MockServoKit:
    def __init__(self, channels):
        self.channels = channels
        self.servo = [MockServo(i) for i in range(channels)]
        self.continuous_servo = [MockContinuousServo(i) for i in range(channels)]

