#!/usr/bin/python3.4

import sys
from time import sleep

from common.generic import base
from GPIO.GPIOclass import GPIOpin


def fan_on():
    if not (gpio7.getGPIOoutput()):
        gpio7.setGPIOoutput(True)
    if not (gpio11.getGPIOoutput()):
        gpio11.setGPIOoutput(True)
    if gpio12.getGPIOoutput():
        gpio12.setGPIOoutput(False)


def fan_off():
    if gpio7.getGPIOoutput():
        gpio7.setGPIOoutput(False)
    if gpio11.getGPIOoutput():
        gpio11.setGPIOoutput(False)
    if not gpio12.getGPIOoutput():
        gpio12.setGPIOoutput(True)


def main():
    try:
        # Creating base class object
        gl = base()

        # localvariables
        sleepTimeFanOn = sleepTime = 30
        sleepTimeFanOff = 1800
        tempThreshold = gl.getTempThreshold()
        assert type(tempThreshold) is int or type(tempThreshold) is float, (
            "Invalid tempThreshold: %d" % tempThreshold
        )

        # Fancontroll loop
        while True:
            cpuTemp = gl.getCPUtemperature()
            time = gl.currentTime("asctime")
            if cpuTemp > tempThreshold:
                print(
                    "%s: CPU temperature crossed threshold: %s" % (time, str(cpuTemp))
                )
                fan_on()
                sleepTime = sleepTimeFanOn
            elif cpuTemp < tempThreshold:
                print("%s: CPU temperature in limit: %s" % (time, str(cpuTemp)))
                fan_off()
                sleepTime = sleepTimeFanOff
            print("%s: Rechecking in %d seconds" % (time, sleepTime))
            sleep(sleepTime)
    except (KeyboardInterrupt, Exception) as e:
        if e:
            print("%s: UnknownException: %s" % (time, str(e)))
        gpio7.resetGPIOPin()
        gpio11.resetGPIOPin()
        gpio12.resetGPIOPin()
        gpio7.cleanupGPIO()  # Can use any of the GPIOpin object to call
        return 0


if __name__ == "__main__":
    # Creating GPIOpin class objects
    gpio7 = GPIOpin(7, "OUT", "BOARD")  # Instantiatin gpio7
    gpio11 = GPIOpin(11, "OUT", "BOARD")  # Instantiatin gpio7
    gpio12 = GPIOpin(12, "OUT", "BOARD")  # Instantiatin gpio7
    print(gpio7)
    print(gpio11)
    print(gpio12)
    sys.exit(main())
