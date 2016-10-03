import usb.core

class Cooler:
    COLOR_MODE_NORMAL = 1
    COLOR_MODE_ALTERNATING = 2
    COLOR_MODE_BLINKING = 3
    COLOR_MODE_OFF = 4
    COLOR_MODES = [COLOR_MODE_NORMAL, COLOR_MODE_ALTERNATING,
                   COLOR_MODE_BLINKING, COLOR_MODE_OFF]

    @classmethod
    def _check_color(cls, color):
        if len(color) != 3 or not all(
                [isinstance(c, int) and c >= 0 and c <= 255 for c in color]
        ):
            raise ValueError("colors must be tuples of 3 ints "
                             "between 0 and 255")

    def _validate(self):
        if self.speed < 30 or self.speed > 100 or self.speed % 5 != 0:
            raise ValueError("speed must be between 30 and 100 "
                             "and divisible by 5")
        self._check_color(self.color)
        self._check_color(self.alternate_color)
        if self.interval < 1 or self.interval > 255:
            raise ValueError("interval must be between 1 and 255")
        if self.color_mode not in self.COLOR_MODES:
            raise ValueError("color_mode must be one of {}".format(
                self.COLOR_MODES
            ))

    def __init__(self, vid, pid, **kwargs):
        devices = list(usb.core.find(idVendor=vid, idProduct=pid, find_all=True))
        assert devices, "No matching USB devices found"
        if len(devices) > 1:
            print("Warning: more than one matching device found, using the first one")
        self.device = devices[0]
        #self.device.ctrl_transfer(0x40, 2, 0x0002)

        self.speed = kwargs.pop('speed', 30)
        self.color = kwargs.pop('color', (255, 0, 0))
        self.alternate_color = kwargs.pop('alternate_color', (0, 0, 255))
        self.interval = kwargs.pop('interval', 1)
        self.color_mode = kwargs.pop('color_mode', self.COLOR_MODE_NORMAL)

    def _start_transaction(self):
        self.device.ctrl_transfer(0x40, 2, 0x0001)

    def _send_pump_speed(self, speed):
        self.device.write(2, [0x13, speed])

    def _send_fan_speed(self, speed):
        self.device.write(2, [0x12, speed])

    def _send_color(self, color, alternate_color, interval, mode):
        self.device.write(2, [
            0x10,
            color[0], color[1], color[2],
            alternate_color[0], alternate_color[1], alternate_color[2],
            0xff, 0x00, 0x00, 0x3c,
            interval, interval,
            0x01 if mode != self.COLOR_MODE_OFF else 0x00,
            0x01 if mode == self.COLOR_MODE_ALTERNATING else 0x00,
            0x01 if mode == self.COLOR_MODE_BLINKING else 0x00,
            0x01, 0x00, 0x01
        ])

    def _receive_status(self):
        status = self.device.read(0x82, 64)

        fan_speed = 256 * status[0] + status[1]
        pump_speed = 256 * status[8] + status[9]
        liquid_temperature = status[10]
        return {'fan_speed': fan_speed,
                'pump_speed': pump_speed,
                'liquid_temperature': liquid_temperature}

    def update(self):
        self._validate()
        self._start_transaction()
        self._send_pump_speed(self.speed)
        self._send_color(self.color, self.alternate_color,
                         self.interval, self.color_mode)
        self._receive_status()

        self._start_transaction()
        self._send_fan_speed(self.speed)
        return self._receive_status()


