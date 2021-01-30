#JDS6600 frequency counter datalogger
from jds6600 import jds6600
from time import time, strftime, sleep


def write_freq(freq):
    with open("/home/lukas/Documents/tap_project/logged_frequency.csv", "a") as log:
        log.write("{0},{1}\n".format(strftime("%Y-%m-%d %H:%M:%S"),str(freq)))        




port = input("What is the tty number?: ")
j = jds6600("/dev/tty"+port)

j.measure_setcoupling("DC")
j.measure_setgate(10)
j.measure_setmode("FREQ")

while True:
    measured = j.measure_getfreq_f()
    write_freq(measured)
    sleep(1)

