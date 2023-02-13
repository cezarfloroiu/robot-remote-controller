AOUTFLG = 0b01000000
AINPRG0 = 0b00000000
AINPRG1 = 0b00010000
AINPRG2 = 0b00100000
AINPRG3 = 0b00110000
AUTOINC = 0b00000100
ACHNNL0 = 0b00000000
ACHNNL1 = 0b00000001
ACHNNL2 = 0b00000010
ACHNNL3 = 0b00000011


class PCF8591:
    def __init__(self, i2c, addr=0x48, enable_out=True, in_program=AINPRG0):
        self.i2c = i2c
        self.addr = addr
        self._aout = self.set_out(enable_out)
        self._ainprg = self.set_program(in_program)
        self._last_ctl = self._make_control()

    def _make_control(self, auto_increment=False, channel=ACHNNL0):
        return 0 | self._aout | self._ainprg | (AUTOINC if auto_increment else 0) | channel

    def _write_control(self, control):
        if control != self._last_ctl:
            self.i2c.writeto(self.addr, bytes([control]))
            self.i2c.readfrom(self.addr, 1)
            self._last_ctl = control

    def _read_raw(self):
        return self.i2c.readfrom(self.addr, 4)

    def set_out(self, enable_out):
        self._aout = AOUTFLG if enable_out else 0
        return self._aout

    def set_program(self, in_program):
        self._ainprg = in_program
        return self._ainprg

    def read(self, channel=-1):
        if channel == -1:
            self.set_out(True)
            self._write_control(self._make_control(auto_increment=True))
            return self._read_raw()
        else:
            self._write_control(self._make_control(channel=channel))
            return int(self._read_raw()[0])

    def write(self, value):
        self.set_out(True)
        control = self._make_control()
        self._last_ctl = control
        self.i2c.writeto(self.addr, bytes([control, value]))
