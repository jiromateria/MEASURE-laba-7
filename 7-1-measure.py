import RPi.GPIO as gpio
import matplotlib.pyplot as plt
import time

def dec2bin(value):
    return [int(i) for i in bin(value)[2:].zfill(8)]

def dac_leds(value):
    signal = dec2bin(value)
    gpio.output( dac, signal)
    return signal

def getVal():
    lvl = 0
    for i in range(bits - 1, -1, -1):
        lvl += 2**i
        gpio.output(dac, dec2bin(lvl))
        time.sleep(0.01)
        comp_value  = gpio.input(comp)
        if (comp_value == 0):
            lvl -= 2**i
    return lvl


dac = [ 8, 11, 7, 1, 0, 5, 12, 6 ]
troyka = 13
comp = 14
bits = len(dac)
lvls = 2 ** bits
max_volt = 3.3

gpio.setmode(gpio.BCM)

gpio.setup(troyka, gpio.OUT, initial=gpio.LOW)
gpio.setup(dac, gpio.OUT)
gpio.setup(comp, gpio.IN)

gpio.output(troyka, 0)

volts_data = []
times_data = []

try:
    start_time = time.time()
    value = 0
    gpio.output(troyka, 1)
    while(value < 248):
        value = getVal()
        dac_leds(value)
        volts_data.append(value*max_volt/ lvls )
        times_data.append(time.time() - start_time)

    gpio.output(troyka, 0)

    while(value > 5):
        value = getVal()
        dac_leds(value)
        volts_data.append(value*max_volt/ lvls )
        times_data.append(time.time() - start_time)

    end_time = time.time()

    with open("./settings.txt", "w") as file:
        file.write(str((end_time - start_time) / len(volts_data)))
        file.write(("\n"))
        file.write(str(max_volt / 256))

    print(end_time - start_time, " secs\n", len(volts_data) / (end_time - start_time), "\n", max_volt / lvls)

finally:
    gpio.output(dac, gpio.LOW)
    gpio.output(troyka, gpio.LOW)
    gpio.cleanup()

times_data_str = [str(item) for item in times_data]
volts_data_str = [str(item) for item in volts_data]

with open("data.txt", "w") as file:
    file.write("\n".join(volts_data_str))

plt.plot(times_data, volts_data)
plt.show()