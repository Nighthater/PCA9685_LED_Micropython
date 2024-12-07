from machine import I2C, Pin
from pca9685 import PCA9685
from led import LEDs
import time


def main():
    """
    Main function to initialize and control LEDs in a sequence.
    """
    try:
        # Initialize I2C with specific pins
        i2c = I2C(0, scl=Pin(1), sda=Pin(0))  # Use I2C(1) if using alternate pins
        
        # Initialize the LED controller
        led_controller = LEDs(i2c, freq=1000)

        while True:
            # Cycle through each LED channel, turn it on and off sequentially
            for i in range(16):
                led_controller.set_brightness(i, 50.0)  # Set brightness to 50%
                time.sleep(0.1)  # Wait 100ms
                led_controller.turn_off(i)  # Turn off the LED

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()