import ustruct
import time


class PCA9685:
    """
    A class to control the PCA9685 PWM driver.
    """

    def __init__(self, i2c, address=0x40):
        """
        Initializes the PCA9685 driver.

        Args:
            i2c (I2C): An I2C object (e.g., created by machine.I2C).
            address (int, optional): The I2C address of the PCA9685. Defaults to 0x40.
        """
        self.i2c = i2c
        self.address = address
        self.reset()

    def _write(self, address, value):
        """
        Write a value to a specific register.

        Args:
            address (int): The register address.
            value (int): The value to write.
        """
        self.i2c.writeto_mem(self.address, address, bytearray([value]))

    def _read(self, address):
        """
        Read a value from a specific register.

        Args:
            address (int): The register address.

        Returns:
            int: The value read from the register.
        """
        return self.i2c.readfrom_mem(self.address, address, 1)[0]

    def reset(self):
        """
        Reset the PCA9685 to its default state.
        """
        self._write(0x00, 0x00)  # Set Mode1 register to 0x00 (normal mode)

    def freq(self, freq=None):
        """
        Set or get the PWM frequency.

        Args:
            freq (int, optional): The frequency to set in Hz. If None, returns the current frequency.

        Returns:
            int: The current frequency (if freq is None).
        """
        if freq is None:
            prescale = self._read(0xFE)
            return int(25000000.0 / 4096 / (prescale - 0.5))
        
        if not 24 <= freq <= 1526:
            raise ValueError("Frequency must be between 24Hz and 1526Hz")

        prescale = int(25000000.0 / 4096.0 / freq + 0.5)
        old_mode = self._read(0x00)
        self._write(0x00, (old_mode & 0x7F) | 0x10)  # Enter sleep mode
        self._write(0xFE, prescale)  # Set prescale
        self._write(0x00, old_mode)  # Exit sleep mode
        time.sleep_us(5000)
        self._write(0x00, old_mode | 0xA1)  # Enable auto-increment

    def pwm(self, index, on=None, off=None):
        """
        Set or get the PWM signal for a specific channel.

        Args:
            index (int): The channel index (0-15).
            on (int, optional): The start time of the pulse. Defaults to None.
            off (int, optional): The end time of the pulse. Defaults to None.

        Returns:
            tuple: (on, off) if on and off are None.
        """
        if not 0 <= index <= 15:
            raise ValueError("Channel index must be between 0 and 15")
        
        if on is None or off is None:
            data = self.i2c.readfrom_mem(self.address, 0x06 + 4 * index, 4)
            return ustruct.unpack('<HH', data)
        
        if not 0 <= on <= 4095 or not 0 <= off <= 4095:
            raise ValueError("PWM values must be between 0 and 4095")
        
        data = ustruct.pack('<HH', on, off)
        self.i2c.writeto_mem(self.address, 0x06 + 4 * index, data)

    def duty(self, index, value=None, invert=False):
        """
        Set or get the duty cycle for a specific channel.

        Args:
            index (int): The channel index (0-15).
            value (int, optional): The duty cycle (0-4095). Defaults to None.
            invert (bool, optional): Whether to invert the duty cycle. Defaults to False.

        Returns:
            int: The current duty cycle if value is None.
        """
        if not 0 <= index <= 15:
            raise ValueError("Channel index must be between 0 and 15")
        
        if value is None:
            pwm = self.pwm(index)
            if pwm == (0, 4096):
                return 0
            elif pwm == (4096, 0):
                return 4095
            duty_cycle = pwm[1]
            return 4095 - duty_cycle if invert else duty_cycle

        if not 0 <= value <= 4095:
            raise ValueError("Duty cycle value must be between 0 and 4095")
        
        if invert:
            value = 4095 - value
        
        if value == 0:
            self.pwm(index, 0, 4096)
        elif value == 4095:
            self.pwm(index, 4096, 0)
        else:
            self.pwm(index, 0, value)
