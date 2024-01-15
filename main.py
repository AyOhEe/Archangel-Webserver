from arduino import Arduino

import time


ARDUINO_PORT = "/dev/ttyACM0"
ARDUINO_BAUD = 115200
SERIAL_KWARGS = {"timeout": 0.1}


ARDUINO_INSTANCE = None
def main():
    global ARDUINO_INSTANCE

    #connect to the adruino
    ARDUINO_INSTANCE = Arduino(ARDUINO_PORT, ARDUINO_BAUD, serial_kwargs=SERIAL_KWARGS)

    value = 0
    while True:
        time.sleep(0.3)
        value = (value + 1) % 256
        ARDUINO_INSTANCE.try_send_message(bytes([value, ord("\n")]))

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        ARDUINO_INSTANCE.shutdown()
