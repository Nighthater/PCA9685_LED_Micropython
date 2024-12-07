from pca9685 import PCA9685


class LEDs:
    """
    A class to control LEDs using the PCA9685 PWM driver.
    """

    def __init__(self, i2c, address=0x40, freq=1000):
        """
        Initialize the LED controller.

        Args:
            i2c (I2C): I2C interface instance.
            address (int, optional): I2C address of the PCA9685 (default is 0x40).
            freq (int, optional): PWM frequency for the LEDs in Hz (default is 1000 Hz).
        """
        if not 24 <= freq <= 1526:
            raise ValueError("Frequency must be between 24Hz and 1526Hz")
        
        self.pca9685 = PCA9685(i2c, address)
        self.pca9685.freq(freq)

    def set_brightness(self, index, duty_cycle):
        """
        Set the brightness of an LED as a duty cycle percentage.

        Args:
            index (int): The channel index (0-15).
            duty_cycle (float): Brightness level in percentage (0.0 to 100.0).

        Raises:
            ValueError: If the channel index is out of range or duty_cycle is invalid.
        """
        if not 0 <= index <= 15:
            raise ValueError("Channel index must be between 0 and 15")
        
        if not 0.0 <= duty_cycle <= 100.0:
            raise ValueError("Duty cycle must be between 0.0 and 100.0")

        # Convert percentage to the range of 0 to 4095.
        duty = int(4095 * (duty_cycle / 100.0))
        self.pca9685.duty(index, duty)

    def turn_off(self, index):
        """
        Turn off an LED by setting its duty cycle to 0%.

        Args:
            index (int): The channel index (0-15).

        Raises:
            ValueError: If the channel index is out of range.
        """
        if not 0 <= index <= 15:
            raise ValueError("Channel index must be between 0 and 15")

        self.pca9685.duty(index, 0)
