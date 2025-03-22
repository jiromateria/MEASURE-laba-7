import RPi.GPIO as gpio
import time
import matplotlib.pyplot as plt

def adc( dac, razr ):
    data = [0, 0, 0, 0, 0, 0, 0, 0 ]

    for i in range(razr):
        data[i] = 1
        gpio.output(dac, data)

        time.sleep(0.002)
        if gpio.input(comp):
            data[i] = 0

        gpio.output(dac, data)

    return bin_list_2_dec(data)

def dec2bin( value ):

    ans = [int(i) for i in bin( value)[2:]]
    while len(ans) < 8:
        ans.insert(0, 0)

    return ans

def bin_list_2_dec(data):
    s = ""
    for i in data:
        s += str(i)
    return int(s, 2)


dac = [8, 11, 7, 1, 0, 5, 12, 6]
led = [2, 3, 4, 17, 27, 22, 10, 9]
troyka = 13
comp = 14
maxV = 3.3
razr = 8

gpio.setmode(gpio.BCM)

gpio.setup(troyka, gpio.OUT)
gpio.setup(comp, gpio.IN)
gpio.setup(led, gpio.OUT)
gpio.setup(dac, gpio.OUT)

timeData = []
voltData = []

try:
    start = time.time()
    print("Zariadka")
    gpio.output(troyka, 1)
    val = 0

    while val < 0.90*(2**razr):
        val = adc(dac, razr)
        gpio.output(led, dec2bin(val))
        valV = val * maxV / 256

        #print(val)
        #print(dec2bin(val))
        #print()

        voltData.append(val/ (2**razr) * maxV )
        timeData.append(time.time() - start)

    gpio.output(troyka, 0)
    print("Razriadka")

    while val > 0.10*(2**razr):
        val = adc(dac, razr)
        gpio.output(led, dec2bin(val))
        valV = val * maxV / 256

        #print(val)
        #print(dec2bin(val))
        #print()

        voltData.append(val/ (2**razr) * maxV )
        timeData.append(time.time() - start)

    end = time.time()


    print("Продолжительность:", end - start)
    print("Период одного измерения:", (end - start) / len(voltData))
    print("Частота дискретизации:", len(voltData) / (end - start))
    print("Шаг квантования АЦП:", maxV / (2**razr-1))

    #voltData_str =  [str(item) for item in voltData]
    #timeData_str =  [str(item) for item in timeData]

    with open('/home/b01-406/Desktop/pyypyyp/volt.txt', 'w') as file:
        for value in voltData:
            file.write(f"{value}\n")

    with open('/home/b01-406/Desktop/pyypyyp/time.txt', 'w') as file:
        for value in timeData:
            file.write(f"{value}\n")

    with open('/home/b01-406/Desktop/pyypyyp/settings.txt', 'w') as file:
            file.write("Продолжительность:")
            file.write(f"{end - start}\n")
            file.write("Частота дискретизации:")
            file.write(f"{len(voltData) / (end - start)}\n")
            file.write("Период одного измерения:")
            file.write(f"{(end - start) / len(voltData)}\n")
            file.write("Шаг квантования АЦП:")
            file.write( f"{maxV / (2**razr-1)}\n")

    plt.plot(timeData, voltData)
    plt.show()



finally:
    gpio.output(dac, 0)
    gpio.output(led, 0)
    gpio.cleanup()